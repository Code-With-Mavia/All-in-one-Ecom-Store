## 🛍️ MyEcomStoreNew

A full-featured **Django-based eCommerce and Blogging Web Application** with integrated user authentication, shopping cart, product search, and content management. Built for scalability, modularity, and user-friendliness.

---

## 🚀 Features

### 🛒 Shop (DukaanPak.pk Inspired)
- Category-wise product listing  
- Product search functionality  
- Shopping cart using sessions  
- Checkout system with order tracking  
- Clean and responsive Bootstrap 5 UI  

### 👤 User Accounts
- User registration & login  
- Profile management  
- Email & password change  
- Account deletion  

### 📝 Blog
- Create, edit, and delete blog posts  
- Tag support  
- Comment and rating system  
- "About" and "Contact Us" pages  

---

## 🗂️ Project Structure

```

├── accounts/            # User authentication and profile management
├── blog/                # Blog functionality with tagging and feedback
├── shop/                # E-commerce system: products, cart, checkout
├── media/               # Uploaded images (products, blog, profiles)
├── staticfiles/         # Static assets (admin, vendor)
├── templates/           # Shared and app-specific HTML templates
├── MyEcomStoreNew/      # Project settings and root configuration
├── api/                 # Deployment configurations (e.g., vercel.json)
├── db.sqlite3           # SQLite database (development)
├── manage.py            # Django management utility
├── requirements.txt     # Python dependencies
└── .gitattributes       # Git settings

````

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/code-with-mavia/All-in-one-Ecom-Store.git
cd MyEcomStoreNew
````

### 2. Create and Activate a Virtual Environment

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create a Superuser

```bash
python manage.py createsuperuser
```

### 6. Run the Development Server

```bash
python manage.py runserver
```

Visit: [http://localhost:8000]

---

## 🖼️ Media & Static Files

* Uploaded product/blog/profile images are stored in the `/media/` directory.
* Static assets (CSS/JS/images) for Django Admin and other components are in `/staticfiles/`.

In `settings.py`, ensure:

```python
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

In `urls.py`:

```python
from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

---
## 👨‍💻 Admin Panel

Visit the Django Admin Panel at:

```
http://localhost:8000/admin/
```

Use the superuser credentials to manage products, blog posts, users, etc.

---

## 📌 Tips

* Keep `DEBUG = False` in production
* Use `.env` for secret keys and configs
* Regularly back up your database
* Use production-ready tools like Gunicorn, Whitenoise, and Django Storages

---

## 📬 Contact

* GitHub: [github.com/code-with-mavia](https://github.com/code-with-mavia)
* Email: `maviaqaiser09@gmail.com`

---

## 📝 License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).

