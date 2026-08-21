# Deploying to Render with your domain (simalthali.com.np)

This gets your farm site live at your real domain, for free, with data that
actually persists (unlike plain Render + SQLite, which wipes your database
on every restart).

**The stack:**
- **Render** — hosts the Django app (free web service)
- **Neon** (or Supabase) — free Postgres database that doesn't get deleted
- **Cloudinary** — free image storage, so goat/product photos survive restarts
- **Your domain** — pointed at Render via DNS

---

## Part 1 — Put your code on GitHub

Render deploys from a GitHub repo, not a zip file.

1. Create a free account at https://github.com if you don't have one.
2. Create a new **private** repository (e.g. `goat-farm-website`).
3. In your project folder (with `manage.py`), run:
   ```powershell
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/goat-farm-website.git
   git push -u origin main
   ```
   (Your `.gitignore` already excludes `venv/`, `db.sqlite3`, and `media/` — good, those shouldn't be pushed.)

---

## Part 2 — Create a free Postgres database (Neon)

Render's own free Postgres gets deleted after 90 days — Neon's free tier doesn't expire.

1. Go to https://neon.tech, sign up free.
2. Create a new project (any name, e.g. `goat-farm-db`).
3. On the project dashboard, copy the **connection string** — it looks like:
   `postgresql://user:password@host/dbname?sslmode=require`
   Save this — you'll paste it into Render as `DATABASE_URL`.

---

## Part 3 — Create a free Cloudinary account (for photos)

1. Go to https://cloudinary.com, sign up free.
2. On your Cloudinary dashboard, find the **API Environment variable** — it looks like:
   `cloudinary://123456789012345:AbCdEfGhIjKlMnOpQrStUvWxYz@your_cloud_name`
   Save this — you'll paste it into Render as `CLOUDINARY_URL`.

---

## Part 4 — Deploy on Render

1. Go to https://render.com, sign up free (you can sign in with GitHub).
2. Click **New +** → **Web Service**.
3. Connect your GitHub account and select your `goat-farm-website` repo.
4. Fill in:
   - **Build Command:** `./build.sh`
   - **Start Command:** `gunicorn goat_farm.wsgi:application`
5. Under **Environment**, add these variables (see `.env.example` in your project for the full list):
   | Key | Value |
   |---|---|
   | `SECRET_KEY` | a new random string (see `.env.example` for how to generate one) |
   | `DEBUG` | `False` |
   | `ALLOWED_HOSTS` | `simalthali.com.np,www.simalthali.com.np` |
   | `DATABASE_URL` | the Neon connection string from Part 2 |
   | `CLOUDINARY_URL` | the Cloudinary URL from Part 3 |
6. Click **Create Web Service**. Render will build and deploy — this takes a few minutes.
7. Once live, it'll be reachable at `your-app-name.onrender.com`. Visit it and check the site loads.
8. Create your admin login on the live site. In Render's dashboard, open the **Shell** tab for your service and run:
   ```
   python manage.py createsuperuser
   ```

---

## Part 5 — Point simalthali.com.np at Render

1. In Render, open your web service → **Settings** → **Custom Domains** → **Add Custom Domain**.
2. Enter `simalthali.com.np` and `www.simalthali.com.np`. Render will show you DNS records to add — typically:
   - A **CNAME** record for `www` → pointing to your `onrender.com` address
   - An **A record** (or ALIAS/ANAME, if your registrar supports it) for the root domain → pointing to Render's IP
3. Log into wherever you manage DNS for `simalthali.com.np` (your domain registrar's control panel) and add exactly the records Render shows you.
4. DNS changes can take anywhere from a few minutes to a few hours to take effect.
5. Once it propagates, Render automatically issues a free SSL certificate — your site will be live at `https://simalthali.com.np`.

---

## After it's live

- Every time you `git push` new changes, Render automatically redeploys.
- Local development is unaffected — running `python manage.py runserver` on your machine still uses SQLite and local file storage exactly as before, since production settings only activate when those environment variables are present.
- Free Render web services **sleep after 15 minutes of inactivity** and take ~30-50 seconds to wake up on the next visit. That's normal on the free tier — if that becomes a problem, Render's paid tier ($7/month) removes it.
