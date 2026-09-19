# Skill-Squad-backend

The **REST API for the SkillSquad web app** — a small Django + Django REST Framework service that handles **user registration and login**, intended to be used by the [Skill-Squad-frontend](https://github.com/SanaAkram/Skill-Squad-frontend) React client. Data is stored in PostgreSQL.

## API

Base path: `/api/`

| Method | Endpoint | Body (JSON) | Response |
|---|---|---|---|
| `POST` | `/api/registration` | `username`, `email`, `password`, `confirm_password` | `{ "Status": true, "Message": "User register Successfully..!" }` — or `Status: false` with `User Already Exist..!` when the e-mail is already registered |
| `POST` | `/api/login` | `email`, `password` | `{ "Status": true, "Message": "Login Successfull..!" }` — or `Status: false` with `Email dose not exist..!` / `Password not Matched..!` (messages returned verbatim from the code) |
| — | `/admin/` | | Django admin |

Example:

```bash
curl -X POST http://127.0.0.1:8000/api/registration \
  -H "Content-Type: application/json" \
  -d '{"username":"sana","email":"sana@example.com","password":"S3cret!","confirm_password":"S3cret!"}'

curl -X POST http://127.0.0.1:8000/api/login \
  -H "Content-Type: application/json" \
  -d '{"email":"sana@example.com","password":"S3cret!"}'
```

## Architecture

```
React client ──HTTP/JSON──► SkillSquads/urls.py ──► api/urls.py ──► api/views.py
                                                                      │  registration() / login()
                                                                      ▼
                                                            api/models.py  User  (table users_tbl)
                                                                      ▼
                                                                PostgreSQL "SkillSquad"
```

| Path | Role |
|---|---|
| `SkillSquads/` | Django project (settings incl. CORS + database, urls, wsgi/asgi) |
| `api/` | The API app: `models.py` (`User`: username, email, password, confirm_password), `views.py`, `serializers.py`, `urls.py` |
| `templates/index.html` | Placeholder page |
| `requirements.txt` | Python dependencies |
| `package.json` | Lists front-end packages (axios, formik, yup); not needed to run the API |

## Stack

- Python 3.8+
- Django 4.0, Django REST Framework 3.13, `django-cors-headers` (so the React app on another origin can call the API), `djoser` in the dependency list
- PostgreSQL via `psycopg2`

## Setup

```bash
git clone https://github.com/SanaAkram/Skill-Squad-backend.git
cd Skill-Squad-backend

python -m venv venv
# Windows:      venv\Scripts\activate
# macOS/Linux:  source venv/bin/activate

pip install -r requirements.txt
```

### Database connection

Create a PostgreSQL database and point `DATABASES` in `SkillSquads/settings.py` at it:

```sql
CREATE DATABASE "SkillSquad";
```

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "SkillSquad",
        "USER": "<your-postgres-user>",
        "PASSWORD": "<your-postgres-password>",
        "HOST": "localhost",
        "PORT": "5432",
    }
}
```

Keep the real credentials out of git (read them from environment variables).

### Run

```bash
python manage.py migrate
python manage.py runserver
```

The API is now at <http://127.0.0.1:8000/api/>. Allow your front-end origin in the `CORS_ALLOWED_ORIGINS` / CORS settings if it is not on the default dev port.

## Security notes

- This is an early prototype: passwords are stored **as submitted (plain text)** and login compares them directly. Before using it for real users, switch to Django's `AbstractUser` / `django.contrib.auth` (hashed passwords), or Djoser + JWT — `djoser` is already listed in `requirements.txt`.
- Registration and login are `csrf_exempt` JSON endpoints; add rate limiting and HTTPS in production.
