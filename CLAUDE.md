# CLAUDE.md

Ushbu fayl ushbu repo ustida ishlaydigan Claude Code (yoki boshqa AI agent) uchun yo'riqnoma.

## Loyiha haqida

**Confectionery Enterprise** — qandolat/shirinlik ishlab chiqaruvchi korxona uchun to'liq stack
e-commerce platforma (O'zbek tilida). Asl loyiha nomi: `stitch_modern_shirinliklar_do_koni_platformasi`.

- **Backend:** Django 5 + Django REST Framework — **to'liq ishlab chiqilgan**, 15 ta app.
- **Frontend:** Next.js 15 (App Router) — **README'da to'liq tasvirlangan, lekin kodi mavjud emas**
  (`frontend/` papkasi bo'sh). Faqat `frontend_html_reference/` ichida statik HTML/dizayn
  namunalari bor — bular haqiqiy frontend emas, balki referens.
- **DB:** PostgreSQL 16 (prod/docker), SQLite (lokal dev fallback)
- **Cache/Queue:** Redis 7, Celery + Celery Beat
- **Deploy:** Docker Compose, Nginx (reverse proxy)

To'liq API va sahifalar ro'yxati uchun [README.md](README.md) ga qarang.

## Muhim: joriy holat

⚠️ **Frontend hali yozilmagan.** `docker compose up --build` frontend service'da xatolik beradi,
chunki `frontend/` papkasida na `Dockerfile`, na `package.json`, na boshqa kod bor. Backend'ni
alohida ishga tushirish mumkin (`python manage.py runserver`), lekin to'liq stack Docker orqali
ishlamaydi.

⚠️ **Testlar yo'q.** Barcha 15 ta app'dagi `tests.py` — Django'ning standart bo'sh shabloni
(3 qatordan iborat). Real test yozilmagan.

## Tez-tez ishlatiladigan buyruqlar

### Backend (lokal, Docker'siz)

```bash
cd backend
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env            # va .env ni sozlang
python manage.py migrate
python seed.py                  # demo ma'lumotlarni yuklaydi (admin + 10 user + mahsulotlar)
python manage.py runserver      # http://localhost:8000
```

Foydali qo'shimcha buyruqlar:
```bash
python manage.py createsuperuser
python manage.py clear_users        # custom command — barcha userlarni tozalaydi (users/management/commands/clear_users.py)
python manage.py makemigrations
python manage.py test               # hozircha bo'sh, lekin ishlaydi
```

### Docker (to'liq stack — frontend tayyor bo'lgach ishlaydi)

```bash
docker compose up --build -d        # barcha servislarni ishga tushiradi
docker compose logs -f backend      # yoki: frontend / nginx / celery
docker compose exec backend bash
docker compose exec backend python manage.py <command>
docker compose exec db psql -U postgres -d shirinliklar_db
docker compose down                 # to'xtatish
docker compose down -v              # + volume'larni (DB ma'lumotlarini) o'chirish
```

### Frontend (yozilgach)

```bash
cd frontend
npm install
npm run dev                         # http://localhost:3000
```

## Repo tuzilishi

```
backend/            Django loyiha — config/ (settings/urls/celery) + 15 domain app
  users/ products/ categories/ cart/ orders/ favorites/ reviews/ payments/
  notifications/ common/ news/ gallery/ certificates/ pages/ contacts/
  seed.py            Demo ma'lumotlar generatori (~640 qator)
frontend/            BO'SH — Next.js kodi hali yozilmagan
frontend_html_reference/   Statik HTML dizayn namunalari (haqiqiy frontend emas, referens)
nginx/nginx.conf     Reverse proxy config (/, /api/, /django-admin/, /admin/* marshrutlash)
docker-compose.yml   db, redis, backend, celery, celery-beat, frontend, nginx servislari
```

## Konventsiyalar

- Foydalanuvchiga ko'rinadigan matn, model `verbose_name`lari, xato xabarlari — **o'zbek tilida**.
- `AUTH_USER_MODEL = users.User`, rollar: `customer`, `staff`, `manager`, `admin`, `superadmin`.
- Django admin `/django-admin/` da (odatiy `/admin/` emas — u Next.js admin panelga ajratilgan,
  `settings.py`dagi `ADMIN_URL` orqali sozlangan).
- Cache backend: Redis mavjud bo'lsa Django'ning ichki `RedisCache`, aks holda `LocMemCache`
  (`django-redis` paketi `requirements.txt`da bor, lekin ishlatilmaydi — Django 4+ ichki redis
  backend'i ishlatiladi).

## Demo login/parollar (seed.py orqali yaratiladi)

| Login | Parol | Rol |
|---|---|---|
| `admin` | `admin123` | Super Admin |
| `user1` ... `user10` | `user1234` | Customer |

Faqat lokal/dev muhit uchun. Productionga chiqarishdan oldin albatta o'zgartiring.
