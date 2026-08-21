# Simalthali Agro Pvt. Ltd. — Full Project (up to date)

This is a **complete, clean copy** of everything built so far:

1. **Public website** — Home, About (editable from admin), Our Goats, Products, Blog, Contact form
2. **Django admin panel** (`/admin/`) — manage all website content, styled with the farm's colors and fonts
3. **Internal farm app** (`farmapp`) — Health, Milk, Breeding, and Feed record tracking
4. **Staff dashboard** (`/dashboard/`) — ear-tag style stat cards, alerts, upcoming kiddings, recent activity

Nothing from earlier steps is missing — this replaces any previous copy you have.

## First-time setup (do this exactly, in order)

Open a terminal in this folder (the one with `manage.py` in it), then:

```powershell
# 1. Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Create database tables — run BOTH app migrations
python manage.py makemigrations core
python manage.py makemigrations farmapp
python manage.py migrate

# 4. Create your admin login
python manage.py createsuperuser

# 5. Run the server
python manage.py runserver
```

## Where everything lives

| URL | What it is |
|---|---|
| `http://127.0.0.1:8000/` | Public website |
| `http://127.0.0.1:8000/admin/` | Admin panel (log in with your superuser) |
| `http://127.0.0.1:8000/dashboard/` | Staff dashboard (also needs login) |

## Adding your first content

Log into `/admin/` and add, in this order:
1. A **Breed** or two
2. A few **Goats** (mark a couple "Featured" so they show on the homepage)
3. Some **Products**
4. Your **About Page** story (there's only ever one — the admin takes you straight to it)
5. A **Blog Post**
6. Try the **Contact form** on the site — submissions land under "Contact messages" in admin

Then, in the internal app, log a few:
- **Health records** (`/admin/farmapp/healthrecord/add/`)
- **Milk records** (`/admin/farmapp/milkrecord/add/`)
- **Breeding records** (`/admin/farmapp/breedingrecord/add/`) — expected kidding date auto-fills ~150 days after mating date if left blank
- **Feed records** (`/admin/farmapp/feedrecord/add/`)

Visit `/dashboard/` afterward to see them summarized.

## Project structure

```
goat_farm_website/
├── manage.py
├── requirements.txt
├── goat_farm/              ← project settings, urls
├── core/                    ← public website app
│   ├── models.py              (Breed, Goat, Product, BlogPost, AboutPage, ContactMessage)
│   ├── admin.py
│   ├── views.py / urls.py
│   ├── templates/core/
│   └── static/core/css/       (site styling)
│   └── static/admin/css/      (admin panel theme override)
├── farmapp/                 ← internal tracking app
│   ├── models.py               (HealthRecord, MilkRecord, BreedingRecord, FeedRecord)
│   ├── admin.py
│   ├── views.py / urls.py      (staff-only dashboard)
│   └── templates/farmapp/
└── templates/admin/          ← overrides Django's default admin look
```

## What's next: Step 3 — ML predictions

Once you've logged a few weeks of real health and milk records, the next
stage will:
1. Use pandas to pull that data out of the database into a clean table
2. Train a first regression model (milk yield prediction) with scikit-learn
3. Wire the trained model into the dashboard as a "Predict" page

Keep logging data in the meantime — that's the actual bottleneck for this
step, not the code.

## Before deploying live (not needed for local development)

- Move `SECRET_KEY` in `goat_farm/settings.py` into an environment variable
- Set `DEBUG = False`
- Set `ALLOWED_HOSTS` to your real domain
- Run `python manage.py collectstatic`
