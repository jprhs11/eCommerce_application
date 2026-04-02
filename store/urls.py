from django.urls import path
from . import views

urlpatterns = [
    # --- Home / Buyer Routes ---
    path('', views.product_list, name='product_list'),
    path(
        'product/<int:product_id>/',
        views.product_detail,
        name='product_detail'
    ),
    path('cart/', views.view_cart, name='view_cart'),
    path(
        'cart/add/<int:product_id>/',
        views.add_to_cart,
        name='add_to_cart'
    ),
    path(
        'cart/remove/<int:product_id>/',
        views.remove_from_cart,
        name='remove_from_cart'
    ),
    path('checkout/', views.checkout, name='checkout'),
    path(
        'product/<int:product_id>/review/',
        views.add_review,
        name='add_review'
    ),

    # --- Vendor Store Management ---
    path('my-stores/', views.vendor_store_list, name='vendor_store_list'),
    path('my-stores/create/', views.create_store, name='create_store'),
    path(
        'my-stores/edit/<int:store_id>/',
        views.edit_store,
        name='edit_store'
    ),
    path(
        'my-stores/delete/<int:store_id>/',
        views.delete_store,
        name='delete_store'
    ),

    # --- Vendor Product Management ---
    path(
        'store/<int:store_id>/products/',
        views.manage_products,
        name='manage_products'
    ),
    path(
        'store/<int:store_id>/products/add/',
        views.add_product,
        name='add_product'
    ),
    path(
        'product/<int:product_id>/edit/',
        views.edit_product,
        name='edit_product'
    ),
    path(
        'product/<int:product_id>/delete/',
        views.delete_product,
        name='delete_product'
    ),
]

