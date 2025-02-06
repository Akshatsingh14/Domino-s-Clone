# Domino's Clone – Online Food Ordering System

Domino’s Clone is a food ordering platform built using **Django**. It allows users to **browse menu items, add items to their cart, place orders, and track their order history**. The application provides a seamless experience with **user authentication, dynamic cart updates, and multiple payment options**.

---

## Features  

### User Authentication  
- Custom login and registration system using Django’s built-in `User` model.  
- Secure password handling with Django’s hashing mechanism.  

### Menu & Product Browsing  
- Users can browse food items categorized as **Veg, Non-Veg, and Beverages**.  
- Search functionality to find specific items quickly.  

### Cart Management  
- Users can add/remove food items from their cart.  
- Automatic price calculation based on selected items.  

### Order Placement & Payment  
- Users can proceed to checkout and select a payment method.  
- As of now, this functionality hasn't been added.  

### Order History  
- Users can view their past orders

---

## Technologies Used  

- **Django** – Backend framework for handling authentication, orders, and database operations.  
- **MySQL** – Database system for storing users, products, and orders.  
- **HTML, CSS, JavaScript** – Frontend technologies for a clean and responsive UI.  
- **AJAX** – For dynamic updates in the cart without refreshing the page.  
- **Email Service** – Sends confirmation emails upon successful registration and order placement.  

---

## How It Works  

### User Registration  
1. Users can create an account by providing their name, email, and password.  
2. Passwords are securely stored using Django’s authentication system.  
3. A user profile is created for storing additional details like mobile number and address.  

### Login & Logout  
1. Users log in using their registered email and password.  
2. Upon login, they are redirected to the menu or their cart page.  
3. Users can log out, clearing their session.  

### Product Browsing & Cart  
1. Users can browse food items, filter by category, or search for specific products.  
2. Selected items can be added to the cart with quantity adjustments.  
3. Users can remove items and view the total bill before checkout.  

### Order History  
1. Users can view their past orders in the **Order History** section.  
2. Email notifications are sent for after **Checkout**.  

---

## Project File Structure  


dominos-clone/
│
├── dominos/          # Main Django project directory
│   ├── __init__.py
│   ├── settings.py   # Project settings, including database configuration
│   ├── urls.py       # URL routing
│   ├── wsgi.py
│
├── menu/             # App handling menu items, cart, and orders
│   ├── __init__.py
│   ├── models.py     # Database models for products, orders, and cart
│   ├── views.py      # Business logic for menu, cart, and checkout
│   ├── forms.py      # Forms for registration, login, and checkout
│   └── templates/
│       ├── register.html
│       ├── login.html
│       ├── menu.html
│       ├── cart.html
│       ├── checkout.html
│       ├── order_history.html
│
└── manage.py         # Django management script


---

## Screenshots (UI Views)  

### Home Page (Menu)  
📷 *[Insert Screenshot Here]*  

### Cart Page  
📷 *[Insert Screenshot Here]*  

### Checkout Page  
📷 *[Insert Screenshot Here]*  

---

## Installation & Setup  

### 1. Clone the Repository  
```bash
git clone https://github.com/your-username/dominos-clone.git
cd dominos-clone
```

### 2. Create a Virtual Environment  
```bash
python -m venv venv
source venv/bin/activate  # For Mac/Linux
venv\Scripts\activate      # For Windows
```

### 3. Install Dependencies  
```bash
pip install -r requirements.txt
```

### 4. Set Up the Database  
```bash
python manage.py migrate
```

### 5. Create a Superuser (Admin Access)  
```bash
python manage.py createsuperuser
```

### 6. Run the Server  
```bash
python manage.py runserver
```
Then visit **http://127.0.0.1:8000/** in your browser.  

---
