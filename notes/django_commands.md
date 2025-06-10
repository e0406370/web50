## Django Commands

### `pip3 install Django`

- Installs Django using the Python package management system `pip`.

---

### `django-admin startproject <projectname>`

- Creates the initial Django **project** structure in a folder named `<projectname>`.
- This folder will contain starter files including:
  - `settings.py` for project configuration such as database settings and installed apps.
  - `urls.py` which contains directions for where users should be routed after navigating to a specific URL.
  - `manage.py` as a command-line utility for managing the project (e.g. running the server, perform migrations).

---

### `python manage.py runserver`

- Runs the Django development server locally at `http://127.0.0.1:8000/` by default.

---

### `python manage.py startapp <appname>`

- Creates the initial Django **application** structure in a folder named `<appname>`.
- This command allows the project to be split into multiple reusable apps that can work together.
  - Make sure to install the app by navigating to the list of `INSTALLED_APPS` in `settings.py` and adding `<appname>` to the list.

---

### `python manage.py makemigrations <appname>`

- Generates Python-based migration files in `migrations` directory, that define changes to the database schema based on `models.py`.
  - Note that running the `migrate` command is required to complete the migration procedure.
  - Every time changes are made in `models.py`, we must make migrations and then migrate.

---

### `python manage.py migrate`

- Applies migrations to the database, creating or updating the `db.sqlite3` file in the project directory.

---

### `python manage.py shell`

- Opens the Django shell, an interactive Python environment where commands can be executed to manipulate the database and test code.

---

### `python manage.py createsuperuser`

- Creates an administrative user for accessing Django's default admin interface.
  - Requires entering a set of`username`, `email`, `password`, and `confirmation`.
  - The admin interface allows one to view and manage database records.

- Note that models must first be imported and registered in the `admin.py` file to appear in the admin interface.
  - Example: `admin.site.register(User)`.

---