<div align="center">

# 🧥 L.A. Management

### _Elevated Fashion E-commerce & Inventory Management_

[![Status](https://img.shields.io/badge/Status-Premium-orange.svg?style=flat-square)]()
[![Python](https://img.shields.io/badge/Python-3.11%2B-57342D.svg?style=flat-square)]()
[![Django](https://img.shields.io/badge/Django-5.0%2B-092E20.svg?style=flat-square)]()
[![Design](https://img.shields.io/badge/Design-Luxury%20Aesthetic-D4AF37.svg?style=flat-square)]()

**L.A. Management** is a state-of-the-art management platform designed for the luxury fashion resale market. It seamlessly bridges the gap between high-end curated sales and robust administrative oversight.

[Explore the Store](#-key-capabilities) • [Admin Dashboard](#-analytics--oversight) • [Installation Guide](#-quick-start)

</div>

---

## ✨ Key Capabilities

### 🏛️ The Luxury Storefront

Experience a boutique feel with a focus on editorial presentation and smooth user flow.

- **Editorial Catalog**: Dynamic grid presentation with focus on typography and high-resolution imagery.
- **Currency Intelligence**: Integrated currency converter displaying prices in USD and Bolívares (VES), using both automated API calls and manual BCV overrides.
- **Simplified Checkout**: Integrated payment modal for Pago Móvil, Zelle, and Bank Transfers with instant reference submission.
- **Order Tracking**: Comprehensive "Mis Pedidos" section for buyers to follow their pieces from payment to delivery.

### 💼 Vendor & Admin Ecosystem

Powering the business with precision tools and insightful analytics.

- **Unified Analytics**: Real-time sales monitoring through an elegant dashboard powered by **Chart.js**.
- **Inventory Control**: Role-based access for sellers to manage their own collections with luxury-styled forms.
- **Order Pipeline**: A complete "Mis Ventas" portal for sellers to coordinate deliveries and verify payments.
- **Profile Customization**: Premium user panels with real-time profile picture previews and detailed security settings.

---

## 🎨 Visual Identity

The project follows a curated design system to evoke a feeling of exclusivity and trust:

- **Palette**: Deep Chocolate (`#57342D`), Rich Cream (`#e4ded0`), and Elegant Orange (`#e67e22`).
- **Typography**: _Playfair Display_ for a serif editorial feel and _Poppins_ for modern legibility.
- **Motion**: Subtle AOS animations and micro-interactions for a polished, "fluid" experience.

---

## 🛠️ Technology Stack

| Architecture   | Technologies                                           |
| :------------- | :----------------------------------------------------- |
| **Backend**    | Python 3.11, Django 5.x                                |
| **Frontend**   | Vanilla JS, Bootstrap 5.3, CSS3 (Custom Design System) |
| **Database**   | SQLite (Production-ready for PostgreSQL/MySQL)         |
| **APIs**       | DolarAPI (BCV Fallback), Chart.js                      |
| **Animations** | AOS.js, Bootstrap Icons                                |

---

## 🚀 Quick Start

Ensure you have **Python 3.10+** and **Git** installed.

### 1. Installation

```bash
# Clone the repository
git clone https://github.com/arturojimenezg15-alt/LAMproyect.git
cd LAMproyect

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration

```bash
# Apply migrations
python manage.py migrate

# Create your admin account
python manage.py createsuperuser

# Start the luxury experience
python manage.py runserver
```

### 3. Usage

- **Storefront**: `http://localhost:8000/`
- **Admin Dashboard**: `http://localhost:8000/dashboard/`
- **Django Admin**: `http://localhost:8000/admin/`

---

## 📂 Architecture Overview

```text
LAMproyect/
├── core/              # Global project settings and URLs
├── store/             # Product catalog, pricing logic, and BCV converter
├── pedidos/           # Order management system (Purchases & Sales)
├── panel_usuario/     # User profile and dashboard management
├── dashboard/         # Administrative analytics and key metrics
├── static/            # Curated assets (Design System, JS, Icons)
└── templates/         # Premium HTML structure
```

---

<div align="center">

**Developed with precision by Luis | 2026**  
_Building the future of luxury resale management._

</div>
