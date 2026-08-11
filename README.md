# Confectionery Enterprise

Premium qandolat ishlab chiqaruvchi korxona uchun to'liq stack e-commerce platformasi.

## Texnologiyalar

- **Frontend:** Next.js 15 (App Router), React 19, TypeScript, Tailwind CSS
- **Backend:** Django 5, Django REST Framework, SimpleJWT
- **Database:** PostgreSQL 16 (dev: SQLite)
- **Cache:** Redis 7
- **Task Queue:** Celery
- **Deployment:** Docker Compose, Nginx

---

## Tezkor ishga tushirish (Docker)

### 1. Docker o'rnatilgan bo'lishi kerak

```bash
docker --version
docker compose version
```

### 2. Loyihani clone qiling

```bash
git clone <repository-url>
cd stitch_modern_shirinliklar_do_koni_platformasi
```

### 3. Bitta buyruq bilan ishga tushiring

```bash
docker compose up --build -d
```

Bu buyruq quyidagilarni avtomatik bajaradi:
- PostgreSQL ma'lumotlar bazasini yaratadi
- Redis cache ni ishga tushiradi
- Backend (Django) containerini build qiladi va ishga tushiradi
- Frontend (Next.js) containerini build qiladi
- Nginx reverse proxy ni ishga tushiradi
- Celery worker va beat ni ishga tushiradi
- Ma'lumotlar bazasini migrate qiladi
- Demo ma'lumotlarni yuklaydi

### 4. Saytni oching

- **Asosiy sayt:** http://localhost
- **Backend API:** http://localhost/api/
- **Django Admin:** http://localhost/admin/
- **Swagger Docs:** http://localhost/api/docs/

---

## Demo hisoblar

| Login | Parol | Rol |
|-------|-------|-----|
| admin | admin123 | Super Admin |
| user1 | user1234 | Customer |
| user2 | user1234 | Customer |

---

## LAN (Local Network) ishlatish

Agar loyiha mahalliy tarmoqda boshqa qurilmalar uchun ochiq bo'lishi kerak bo'lsa:

### 1. `.env` fayl yarating (ixtiyoriy)

Loyiha ildiz papkasida `.env` fayl yarating:

```bash
# Loyiha IP manzilingizni kiriting
COMPOSE_PROJECT_NAME=confectionery
```

### 2. Docker Compose ishga tushiring

```bash
docker compose up --build -d
```

### 3. Boshqa qurilmalardan kiring

Kompyuteringizning IP manzilini toping:

```bash
# Windows
ipconfig

# Linux/Mac
ip addr show
```

Keyin boshqa qurilmalardan quyidagi manzillar orqali kiring:

- **Asosiy sayt:** `http://192.168.x.x` (masalan, `http://192.168.100.15`)
- **Backend API:** `http://192.168.x.x/api/`
- **Django Admin:** `http://192.168.x.x/admin/`
- **Swagger Docs:** `http://192.168.x.x/api/docs/`

### 4. CORS sozlamalari

Backend `ALLOWED_HOSTS` va `CORS_ALLOWED_ORIGINS` sozlamalari `*` (hamma uchun) ga o'rnatilgan. Agar xavfsizlikni kuchaytirmoqchi bo'lsangiz, `docker-compose.yml` faylida `ALLOWED_HOSTS` va `CORS_ALLOWED_ORIGINS` ni ma'lum IP manzillar bilan almashtiring:

```yaml
environment:
  - ALLOWED_HOSTS=*,localhost,192.168.100.15
  - CORS_ALLOWED_ORIGINS=http://localhost,http://localhost:3000,http://192.168.100.15
```

---

## Qo'lda ishga tushirish (Docker holda)

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env  # .env faylini sozlang
python manage.py migrate
python seed.py
python manage.py runserver
```

Backend: http://localhost:8000

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend: http://localhost:3000

---

## Docker buyruqlari

### Loyihani ishga tushirish
```bash
docker compose up --build -d
```

### Loglarni ko'rish
```bash
docker compose logs -f
```

### Backend loglarini ko'rish
```bash
docker compose logs -f backend
```

### Frontend loglarini ko'rish
```bash
docker compose logs -f frontend
```

### Nginx loglarini ko'rish
```bash
docker compose logs -f nginx
```

### Barcha containerlarni to'xtatish
```bash
docker compose down
```

### Barcha containerlarni va ma'lumotlarni o'chirish
```bash
docker compose down -v
```

### Qayta build qilish
```bash
docker compose up --build -d
```

### Backend shell ga kirish
```bash
docker compose exec backend bash
```

### Django command bajarish
```bash
docker compose exec backend python manage.py <command>
```

### Ma'lumotlar bazasiga kirish
```bash
docker compose exec db psql -U postgres -d shirinliklar_db
```

---

## API Endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/api/users/register/` | POST | Ro'yxatdan o'tish |
| `/api/users/login/` | POST | Tizimga kirish (JWT) |
| `/api/users/token/refresh/` | POST | Token yangilash |
| `/api/users/profile/` | GET/PATCH | Profil |
| `/api/users/change-password/` | POST | Parol o'zgartirish |
| `/api/users/logout/` | POST | Chiqish |
| `/api/products/` | GET | Mahsulotlar ro'yxati |
| `/api/products/{slug}/` | GET | Mahsulot tafsiloti |
| `/api/products/popular/` | GET | Mashhur mahsulotlar |
| `/api/products/featured/` | GET | Tanlangan mahsulotlar |
| `/api/products/new/` | GET | Yangi mahsulotlar |
| `/api/products/{slug}/related/` | GET | O'xshash mahsulotlar |
| `/api/categories/` | GET | Kategoriyalar |
| `/api/products/brands/` | GET | Brendlar |
| `/api/cart/` | GET | Savat |
| `/api/cart/add/` | POST | Savatga qo'shish |
| `/api/cart/item/{id}/` | PATCH/DELETE | Savat elementi |
| `/api/orders/` | GET/POST | Buyurtmalar |
| `/api/orders/{id}/` | GET | Buyurtma tafsiloti |
| `/api/orders/{id}/cancel/` | POST | Buyurtmani bekor qilish |
| `/api/orders/validate-coupon/` | POST | Kupon tekshirish |
| `/api/orders/addresses/` | GET/POST | Manzillar |
| `/api/favorites/` | GET | Sevimlilar |
| `/api/favorites/toggle/` | POST | Sevimlilarga qo'shish/olish |
| `/api/reviews/product/{id}/` | GET/POST | Sharhlar |
| `/api/notifications/` | GET | Bildirishnomalar |
| `/api/news/` | GET | Yangiliklar |
| `/api/gallery/categories/` | GET | Galereya kategoriyalari |
| `/api/gallery/images/` | GET | Galereya rasmlari |
| `/api/certificates/` | GET | Sertifikatlar |
| `/api/pages/company/` | GET | Kompaniya haqida |
| `/api/pages/partnership/` | POST | Hamkorlik arizasi |
| `/api/contacts/` | POST | Kontakt xabar |
| `/api/common/dashboard/` | GET | Admin dashboard (admin) |
| `/api/orders/admin/orders/` | GET | Barcha buyurtmalar (admin) |
| `/api/orders/admin/orders/{id}/status/` | POST | Status o'zgartirish (admin) |
| `/api/news/admin/` | GET/POST | Yangiliklar boshqaruvi (admin) |
| `/api/gallery/admin/images/` | GET/POST | Galereya boshqaruvi (admin) |
| `/api/certificates/admin/` | GET/POST | Sertifikatlar boshqaruvi (admin) |

---

## Frontend sahifalar

### Foydalanuvchi sahifalari
| Route | Sahifa |
|---|---|
| `/` | Bosh sahifa |
| `/products` | Mahsulotlar katalogi |
| `/products/[slug]` | Mahsulot tafsilotlari |
| `/cart` | Savat |
| `/checkout` | Buyurtma berish |
| `/orders` | Buyurtmalarim |
| `/wishlist` | Sevimlilar |
| `/profile` | Profil |
| `/auth/login` | Tizimga kirish |
| `/auth/register` | Ro'yxatdan o'tish |
| `/about` | Biz haqimizda |
| `/contact` | Kontakt |
| `/news` | Yangiliklar |
| `/gallery` | Galereya |

### Admin sahifalari
| Route | Sahifa |
|---|---|
| `/admin/dashboard` | Dashboard |
| `/admin/products` | Mahsulotlar boshqaruvi |
| `/admin/categories` | Kategoriyalar |
| `/admin/orders` | Buyurtmalar |
| `/admin/customers` | Mijozlar |
| `/admin/news` | Yangiliklar |
| `/admin/gallery` | Galereya |
| `/admin/certificates` | Sertifikatlar |
| `/admin/contacts` | Kontakt xabarlar |
| `/admin/partnerships` | Hamkorlik arizalari |
| `/admin/analytics` | Analytics |
| `/admin/notifications` | Bildirishnomalar |
| `/admin/settings` | Sozlamalar |
| `/admin/roles` | Rollar va ruxsatlar |

---

## Backend modellar

- **User** - Foydalanuvchilar (role, phone, avatar)
- **Category** - Mahsulot kategoriyalari
- **Brand** - Brendlar
- **Product** - Mahsulotlar (narx, reyting, SKU, zaxira)
- **ProductImage** - Mahsulot rasmlari
- **ProductVariant** - Mahsulot variantlari
- **Cart/CartItem** - Savat
- **Order/OrderItem** - Buyurtmalar (8 ta status)
- **Coupon** - Kuponlar
- **Address** - Manzillar
- **Review** - Sharhlar
- **Favorite** - Sevimlilar (Wishlist)
- **Notification** - Bildirishnomalar
- **Payment** - To'lovlar
- **News** - Yangiliklar
- **GalleryImage/GalleryCategory** - Galereya
- **Certificate** - Sertifikatlar
- **Company** - Kompaniya ma'lumotlari
- **PartnershipRequest** - Hamkorlik arizalari
- **ContactMessage** - Kontakt xabarlar
- **SiteSettings** - Sayt sozlamalari

---

## Buyurtma statuslari

1. `pending` - Kutilmoqda
2. `confirmed` - Tasdiqlandi
3. `processing` - Ishlab chiqarilmoqda
4. `packaging` - Qadoqlanmoqda
5. `delivering` - Yetkazilmoqda
6. `delivered` - Yetkazib berilgan
7. `cancelled` - Bekor qilindi
8. `refunded` - Qaytarilgan

---

## Rollar

| Rol | Tavsif |
|---|---|
| `superadmin` | To'liq boshqaruv huquqi |
| `admin` | Mahsulotlar va buyurtmalarni boshqarish |
| `manager` | Buyurtmalarni ko'rish va o'zgartirish |
| `customer` | Oddiy foydalanuvchi |

---

## Production deployment

1. `docker-compose.yml` faylida `DJANGO_SECRET_KEY` ni o'zgartiring
2. `ALLOWED_HOSTS` ga domen nomini qo'shing
3. `CORS_ALLOWED_ORIGINS` ga frontend domenini qo'shing
4. SSL sertifikat o'rnating (Let's Encrypt)
5. Nginx konfiguratsiyasini yangilang
6. Database backup tartibini o'rnating

---

## Litsenziya

Barcha huquqlar himoyalangan.
