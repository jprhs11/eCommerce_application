Django eCommerce Platform
A robust eCommerce system built with Django and MariaDB, designed to support a dual-ecosystem of Vendors and Buyers.
📋 Features
User Roles & Permissions
Vendors: Create and manage stores, list products, and track inventory.
Buyers: Browse stores, manage a session-based cart, and checkout.
Authentication: Secure login/registration with custom permissions and token-based password recovery via email.
Core Functionality
Session Cart: Persistent cart management while browsing without requiring immediate database writes.
Automated Invoicing: Seamless checkout process that clears carts and sends PDF/HTML invoices to the buyer's email.
Verified Reviews: Automatic detection of "Verified Purchase" status for user reviews based on order history.
Data Integrity: Relational database architecture using MariaDB for scalable data management.
🛠️ Tech Stack
Backend: Django (Python)
Database: MariaDB / MySQL
Authentication: Django Auth & Custom Permissions
Communication: Django Mail for Invoices & Password Resets
🚀 Getting Started
Clone the repository
bash
git clone <your-repo-url>
Use code with caution.

Install dependencies
bash
pip install django mysqlclient
Use code with caution.

Configure Database
Update the DATABASES setting in settings.py with your MariaDB credentials.
Run Migrations
bash
python manage.py migrate
Use code with caution.

Start the Server
bash
python manage.py runserver
Use code with caution.