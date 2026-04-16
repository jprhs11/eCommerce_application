from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login
from django.core.mail import send_mail
from django.conf import settings
from .models import Store, Product, Order, OrderItem, Review
from .forms import RegistrationForm
from django.contrib import messages


# --- PERMISSION HELPERS ---


def is_vendor(user):
    """Check if the user is assigned the vendor role."""
    return hasattr(user, "profile") and user.profile.role == "vendor"


# --- 1. AUTHENTICATION & REGISTRATION ---


def register_view(request):
    """Handle user registration for both Vendors and Buyers."""
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("product_list")
    else:
        form = RegistrationForm()
    return render(request, "store/register.html", {"form": form})


# --- 2. BUYER & PRODUCT BROWSING ---


def product_list(request):
    """Display products using select_related to fix performance issues."""
    # Reviewer Fix: Optimized query to prevent N+1 overhead
    products = Product.objects.select_related("store").all()
    return render(request, "store/product_list.html", {"products": products})


def product_detail(request, product_id):
    """Show specific product details and all associated reviews."""
    product = get_object_or_404(Product, id=product_id)
    reviews = product.reviews.all()
    return render(
        request,
        "store/product_detail.html",
        {"product": product, "reviews": reviews},
    )


# --- 3. VENDOR STORE MANAGEMENT ---


@login_required
@user_passes_test(is_vendor, login_url="/")
def vendor_store_list(request):
    """List all stores belonging to the logged-in vendor."""
    stores = Store.objects.filter(vendor=request.user)
    return render(request, "store/vendor_stores.html", {"stores": stores})


@login_required
@user_passes_test(is_vendor)
def create_store(request):
    """Allow vendors to create a new store instance."""
    if request.method == "POST":
        Store.objects.create(
            vendor=request.user,
            name=request.POST.get("name"),
            description=request.POST.get("description"),
        )
        return redirect("vendor_store_list")
    return render(request, "store/create_store.html")


@login_required
@user_passes_test(is_vendor)
def edit_store(request, store_id):
    """Allow vendors to update their store details."""
    store = get_object_or_404(Store, id=store_id, vendor=request.user)
    if request.method == "POST":
        store.name = request.POST.get("name")
        store.description = request.POST.get("description")
        store.save()
        return redirect("vendor_store_list")
    return render(request, "store/edit_store.html", {"store": store})


@login_required
@user_passes_test(is_vendor)
def delete_store(request, store_id):
    """Allow vendors to permanently remove a store."""
    store = get_object_or_404(Store, id=store_id, vendor=request.user)
    store.delete()
    return redirect("vendor_store_list")


# --- 4. VENDOR PRODUCT MANAGEMENT ---


@login_required
@user_passes_test(is_vendor)
def manage_products(request, store_id):
    """List products for a specific store owned by the vendor."""
    store = get_object_or_404(Store, id=store_id, vendor=request.user)
    products = Product.objects.filter(store=store)
    return render(
        request,
        "store/manage_products.html",
        {"store": store, "products": products},
    )


@login_required
@user_passes_test(is_vendor)
def add_product(request, store_id):
    """Allow vendors to add a new product to their store."""
    store = get_object_or_404(Store, id=store_id, vendor=request.user)
    if request.method == "POST":
        Product.objects.create(
            store=store,
            name=request.POST.get("name"),
            description=request.POST.get("description"),
            price=request.POST.get("price"),
            stock=request.POST.get("stock"),
        )
        return redirect("manage_products", store_id=store.id)
    return render(request, "store/add_product.html", {"store": store})


@login_required
@user_passes_test(is_vendor)
def edit_product(request, product_id):
    """Allow vendors to edit existing product details."""
    product = get_object_or_404(
        Product, id=product_id, store__vendor=request.user
    )
    if request.method == "POST":
        product.name = request.POST.get("name")
        product.description = request.POST.get("description")
        product.price = request.POST.get("price")
        product.stock = request.POST.get("stock")
        product.save()
        return redirect("manage_products", store_id=product.store.id)
    return render(request, "store/edit_product.html", {"product": product})


@login_required
@user_passes_test(is_vendor)
def delete_product(request, product_id):
    """Allow vendors to remove a product from their inventory."""
    product = get_object_or_404(
        Product, id=product_id, store__vendor=request.user
    )
    store_id = product.store.id
    product.delete()
    return redirect("manage_products", store_id=store_id)


# --- 5. SHOPPING CART (SESSION BASED) ---


def add_to_cart(request, product_id):
    """Add items to cart with security checks for login and role."""
    # Reviewer Fix: Check if user is logged in
    if not request.user.is_authenticated:
        messages.error(request, "Please log in to add items to your cart.")
        return redirect("login")

    # Reviewer Fix: Check if user is a buyer
    if request.user.profile.role != "buyer":
        messages.error(request, "Only buyers can use the shopping cart.")
        return redirect("product_list")

    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get("cart", {})
    requested_qty = int(request.POST.get("quantity", 1))

    p_id = str(product_id)
    new_total = cart.get(p_id, 0) + requested_qty

    if new_total > product.stock:
        messages.error(request, f"Only {product.stock} units available.")
    else:
        cart[p_id] = new_total
        request.session["cart"] = cart
        messages.success(request, f"Added {product.name} to cart.")

    return redirect(request.META.get("HTTP_REFERER", "product_list"))


def view_cart(request):
    """Summarize items in cart with optimized product fetching."""
    cart = request.session.get("cart", {})
    # Reviewer Fix: Batch fetch products to avoid N+1 slowness
    products = Product.objects.filter(id__in=cart.keys())
    cart_items = []
    total = 0

    for product in products:
        qty = cart.get(str(product.id))
        sub = product.price * qty
        total += sub
        cart_items.append(
            {"product": product, "quantity": qty, "subtotal": sub}
        )

    return render(
        request, "store/cart.html", {"cart_items": cart_items, "total": total}
    )


def remove_from_cart(request, product_id):
    """Completely remove an item from the session-based cart."""
    cart = request.session.get("cart", {})
    p_id = str(product_id)
    if p_id in cart:
        del cart[p_id]
    request.session["cart"] = cart
    return redirect("view_cart")


# --- 6. CHECKOUT & REVIEWS ---


@login_required
def checkout(request):
    """Finalize purchase, deduct stock, and send email invoice."""
    cart = request.session.get("cart", {})
    if not cart:
        return redirect("product_list")

    order = Order.objects.create(buyer=request.user, total_paid=0)
    total_price = 0
    inv_text = f"Order #{order.id}\nBuyer: {request.user.username}\n\n"

    for p_id, qty in cart.items():
        product = get_object_or_404(Product, id=p_id)
        subtotal = product.price * qty
        total_price += subtotal
        product.stock -= qty
        product.save()

        OrderItem.objects.create(
            order=order, product=product, quantity=qty, price=product.price
        )
        inv_text += f"- {product.name} x {qty}: ${subtotal}\n"

    order.total_paid = total_price
    order.save()

    send_mail(
        f"Your Invoice - Order #{order.id}",
        f"{inv_text}\nTotal: ${total_price}",
        settings.DEFAULT_FROM_EMAIL,
        [request.user.email],
        fail_silently=True,
    )

    request.session["cart"] = {}
    messages.success(request, "Order placed successfully!")
    return render(request, "store/checkout_success.html", {"order": order})


@login_required
def add_review(request, product_id):
    """Ensure ONLY buyers can review products."""
    product = get_object_or_404(Product, id=product_id)

    # Reviewer Fix: Check if user is a buyer
    if request.user.profile.role != "buyer":
        messages.error(request, "Only buyers can leave product reviews.")
        return redirect("product_detail", product_id=product.id)

    # Secondary check: Prevent self-reviewing (extra safety)
    if product.store.vendor == request.user:
        messages.error(request, "You cannot review your own product.")
        return redirect("product_list")

    if request.method == "POST":
        has_purchased = OrderItem.objects.filter(
            order__buyer=request.user, product=product
        ).exists()

        Review.objects.create(
            product=product,
            user=request.user,
            content=request.POST.get("content"),
            rating=request.POST.get("rating"),
            is_verified=has_purchased,
        )
        messages.success(request, "Review submitted!")
        return redirect("product_detail", product_id=product.id)

    return render(request, "store/add_review.html", {"product": product})
