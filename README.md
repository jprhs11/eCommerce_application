🛒 Django eCommerce Ecosystem A full-stack eCommerce application featuring a dual-user system for Vendors and Buyers. This project focuses on secure role-based access, session-based shopping experiences, and automated post-purchase workflows.

🚀 Key Features:

👤 Role-Based User System Vendors: Can create and manage unique stores. Full CRUD functionality (Create, Read, Update, Delete) for store listings and product inventories. Buyers: Can browse products from various vendors, manage a persistent shopping cart, and complete checkouts.

💳 Shopping & Checkout Session-Based Cart: Tracks user items locally without requiring a database entry for every cart update, ensuring a fast browsing experience. Automated Invoicing: Upon checkout, the system clears the cart, generates a detailed invoice, and emails it directly to the buyer.

⭐ Verified Review System Smart Logic: Reviews are automatically flagged as "Verified" if the system detects the user has previously purchased that specific product. Open Feedback: Unverified users can still leave reviews, but they are clearly marked as "Unverified" for transparency.

🔒 Security & Authentication Token-Based Recovery: Secure "Forgot Password" workflow using time-sensitive, expiring tokens sent via email. Permission Guards: Custom decorators and mixins to prevent buyers from accessing vendor dashboards and vendors from editing other vendors' stores.

🛠️ Tech Stack Backend: Django (Python) Database: MariaDB (Relational) Communication: SMTP for automated invoices and password resets. Frontend: Django Templates with CSS/JavaScript.

⚙️ Getting Started Prerequisites Python 3.x MariaDB / MySQL Virtual Environment (recommended)

Installation:

Clone the repository: https://github.com/jprhs11/eCommerce_application_Part1.git

cd eCommerce_application

Database Configuration: Update your DATABASES settings in settings.py with your MariaDB credentials.

Apply Migrations: python manage.py migrate

Run the Server: python manage.py runserver
