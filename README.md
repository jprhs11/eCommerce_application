# ShopSmart eCommerce Application - Part 1

A robust Django-based marketplace allowing Vendors to manage digital stores and Buyers to browse, purchase, and review products.

## 🚀 Installation & Setup

Please follow these steps exactly to get the project running locally:

### 1. Clone and Enter the Project
Navigate to the project folder in your terminal:
`cd eCommerce_application_Part1`

### 2. Create and Activate Virtual Environment
**Create the environment:**
`python -m venv .venv`

**Activate on Windows:**
`.venv\Scripts\activate`

**Activate on Mac/Linux:**
`source .venv/bin/activate`

### 3. Install Dependencies
`pip install -r requirements.txt`

### 4. Database Configuration
Ensure your MySQL server is running and a database named `ecommerce_db` exists. Run the migrations to create the tables:
`python manage.py migrate`

### 5. Run the Application
`python manage.py runserver`

Visit the application at: `http://127.0.0`

---

## 📂 Project Structure Note

As requested by the project requirements, a **Planning** folder has been included in the root directory. It contains four separate files addressing:
1. **1_Requirements.txt**: User roles and system needs.
2. **2_UI_UX_Plan.txt**: Layout and user journey.
3. **3_Access_Security.txt**: RBAC and data protection.
4. **4_Failure_Recovery.txt**: Stock validation and SMTP resilience.

---

## 🛠️ Key Improvements Made

*   **Performance:** Implemented `select_related` and cached template loaders to fix major rendering delays.
*   **Security:** Corrected logic to prevent duplicate email registrations and blocked vendors from reviewing any products.
*   **UI/UX:** Added quantity selectors directly to product blocks on the list page and streamlined the guest-to-buyer workflow.
*   **PEP 8:** All code has been formatted to strictly follow the 79-character line limit.

