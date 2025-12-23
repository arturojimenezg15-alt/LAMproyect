# L.A. Management

![Project Status](https://img.shields.io/badge/status-active-success.svg)
![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)
![Django](https://img.shields.io/badge/django-5.0%2B-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

**L.A. Management** is a robust and aesthetic web-based management platform designed to streamline e-commerce operations. It provides a seamless experience for both customers and administrators, combining a user-friendly storefront with powerful backend analytics.

---

## 🌟 Key Features

### 🛍️ Client Storefront

- **Product Catalog**: Browse a tailored selection of products with detailed descriptions and pricing.
- **User Accounts**: Secure customer registration and authentication.
- **Order Management**: Users can track their orders and interaction history.

### 📊 Admin Dashboard

- **Real-Time Analytics**: Visual insights into sales performance using **Chart.js**.
- **Key Metrics**: Instant view of Total Revenue, Total Orders, Product Count, and Unique Customers.
- **Inventory Control**: Tools to add and manage product listings directly from the dashboard.
- **Monthly Reports**: Dynamic charts showing sales trends over time.

---

## 🛠️ Technology Stack

- **Backend**: Python, Django Framework
- **Database**: SQLite (Development) / Scalable to PostgreSQL
- **Frontend**: HTML5, CSS3, JavaScript
- **Visualization**: Chart.js for data analytics
- **Styling**: Custom responsive CSS with Google Fonts (Roboto)

---

## 🚀 Getting Started

Follow these instructions to get the project up and running on your local machine.

### Prerequisites

- Python 3.8 or higher
- git

### Installation

1.  **Clone the repository**

    ```bash
    git clone <repository-url>
    cd LAMproyect
    ```

2.  **Create a Virtual Environment**

    ```bash
    # Windows
    python -m venv .venv
    .venv\Scripts\activate

    # macOS/Linux
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3.  **Install Dependencies**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Apply Database Migrations**

    ```bash
    python manage.py migrate
    ```

5.  **Create a Superuser (Admin)**

    ```bash
    python manage.py createsuperuser
    ```

6.  **Run the Development Server**

    ```bash
    python manage.py runserver
    ```

7.  **Access the Application**
    - Storefront: `http://127.0.0.1:8000/`
    - Dashboard (Login as Admin): `http://127.0.0.1:8000/dashboard/`

---

## 📂 Project Structure

```text
LAMproyect/
├── accounts/          # User authentication and profile management
├── dashboard/         # Analytics and administrative views
├── la_management/     # Project configuration (settings, urls)
├── store/             # Product catalog and ordering logic
├── static/            # Static assets (CSS, JS, Images)
├── templates/         # HTML Templates
└── manage.py          # Django command-line utility
```

---

## 🎨 UI/UX Design

The application features a modern, minimalist design focused on usability:

- **Navigation**: Clean and responsive navbar with role-based links.
- **Consistency**: Unified color palette and typography across all pages.
- **Feedback**: Interactive messages for user actions (login success, errors, etc.).

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

Developed by Luis | 2025
