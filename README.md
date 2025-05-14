# Placement Portal

**Placement Portal** is a Django-based web application designed for managing student placement activities in educational institutions. It helps the Training and Placement Office (TPO) to store and manage student records, placement data, company details, and related activities efficiently.

## 🛠️ Technologies Used

- **Backend:** Django (Python 3)
- **Database:** SQLite (default)
- **Frontend:** HTML, CSS, JavaScript
- **Others:** Django Admin, pip, virtualenv

## 📁 Folder Structure

```
placment_portal/
├── backup_code/         # Backup version of older code (not used in current build)
├── core/                # Main Django project settings and URLs
│   ├── settings.py
│   ├── urls.py
│   └── ...
├── media/               # Media files (uploads)
├── placement/           # Main Django app for handling placement logic
│   ├── models.py
│   ├── views.py
│   ├── templates/
│   └── ...
├── venv/                # Virtual environment (should be recreated by developers)
├── db.sqlite3           # SQLite database file (included for development)
├── create_db.py         # Script to initialize or populate the database
├── manage.py            # Django management script
├── requirements.txt     # List of required Python packages
├── version_5.py         # Additional script or versioning info
├── server.log           # Server log file
└── .gitattributes       # Git settings
```

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/tentax143/placment_portal.git
cd placment_portal
```

### 2. Create a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate       # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Database Setup

The project uses an included `db.sqlite3`. If you need to recreate it:

```bash
python manage.py migrate
```

(Optional) You can also run the custom script:

```bash
python create_db.py
```

### 5. Create a Superuser

```bash
python manage.py createsuperuser
```

Follow the prompts to set admin credentials.

### 6. Collect Static Files

```bash
python manage.py collectstatic
```

## 🚀 Running the Server

Start the Django development server:

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` to view the portal.  
Admin login: `http://127.0.0.1:8000/admin/`

## 🧠 Developer Notes

- **No environment variables required.**
- **Admin panel is pre-configured** once superuser is created.
- All logic resides in the `placement/` app.
- Template files can be found inside `placement/templates/`.
- Static files (CSS, JS) are loaded via Django’s static handling.

## 📜 License

No license file is present in this repository. Assume **All Rights Reserved** unless specified otherwise.
