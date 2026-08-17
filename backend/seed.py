import os
import sys
import django
import random
from datetime import timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.contrib.auth import get_user_model
from django.utils import timezone
from categories.models import Category
from products.models import Product, ProductImage, Brand
from orders.models import Order, OrderItem, Coupon, Address
from reviews.models import Review
from favorites.models import Favorite

User = get_user_model()

# ─── Create Superadmin (sex/zavod egasi) ───────────────────────
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@shirinliklar.uz', 'admin123', phone='+998901234567', role='superadmin')
    print('Superadmin user created (admin / admin123)')

# ─── Create demo Admin (hodim) ──────────────────────────────────
if not User.objects.filter(username='admin1').exists():
    admin1 = User.objects.create_user(
        'admin1', 'admin1@shirinliklar.uz', 'admin1234',
        first_name='Farrux', last_name='Nazarov', phone='+998901230000', role='admin',
    )
    print('Admin (hodim) user created (admin1 / admin1234)')

# ─── Create Demo Users (online mijozlar — staff roli) ──────────
demo_users = [
    {'username': 'user1', 'email': 'user1@example.com', 'first_name': 'Aziz', 'last_name': 'Karimov', 'phone': '+998901112233', 'password': 'user1234'},
    {'username': 'user2', 'email': 'user2@example.com', 'first_name': 'Nodira', 'last_name': 'Aliyeva', 'phone': '+998902223344', 'password': 'user1234'},
    {'username': 'user3', 'email': 'user3@example.com', 'first_name': 'Sardor', 'last_name': 'Rahimov', 'phone': '+998903334455', 'password': 'user1234'},
    {'username': 'user4', 'email': 'user4@example.com', 'first_name': 'Gulnora', 'last_name': 'Toshmatova', 'phone': '+998904445566', 'password': 'user1234'},
    {'username': 'user5', 'email': 'user5@example.com', 'first_name': 'Jamshid', 'last_name': 'Oripov', 'phone': '+998905556677', 'password': 'user1234'},
    {'username': 'user6', 'email': 'user6@example.com', 'first_name': 'Dilnoza', 'last_name': 'Yuldasheva', 'phone': '+998906667788', 'password': 'user1234'},
    {'username': 'user7', 'email': 'user7@example.com', 'first_name': 'Bobur', 'last_name': 'Mirzayev', 'phone': '+998907778899', 'password': 'user1234'},
    {'username': 'user8', 'email': 'user8@example.com', 'first_name': 'Malika', 'last_name': 'Ergasheva', 'phone': '+998908889900', 'password': 'user1234'},
    {'username': 'user9', 'email': 'user9@example.com', 'first_name': 'Suhrob', 'last_name': 'Jumayev', 'phone': '+998909990011', 'password': 'user1234'},
    {'username': 'user10', 'email': 'user10@example.com', 'first_name': 'Nilufar', 'last_name': 'Rashidova', 'phone': '+998900001122', 'password': 'user1234'},
]

users = []
for u_data in demo_users:
    user, created = User.objects.get_or_create(
        username=u_data['username'],
        defaults={
            'email': u_data['email'],
            'first_name': u_data['first_name'],
            'last_name': u_data['last_name'],
            'phone': u_data['phone'],
        }
    )
    if created:
        user.set_password(u_data['password'])
        user.save()
        print(f'  Created user: {user.username}')
    users.append(user)
print(f'Users ready ({len(users)} total)')

# ─── Create Brands ────────────────────────────────────────────
brands_data = [
    {'name': 'Shirinliklar Dunyosi', 'slug': 'shirinliklar-dunyosi', 'description': 'Asosiy brend - premium shirinliklar'},
    {'name': 'ChocoLux', 'slug': 'chocolux', 'description': 'Premium shokolad mahsulotlari'},
    {'name': 'PastryArt', 'slug': 'pastryart', 'description': 'Professional konditerlik mahsulotlari'},
    {'name': 'SweetHome', 'slug': 'sweethome', 'description': 'Uyda tayyorlangan shirinliklar'},
    {'name': 'MacaronHouse', 'slug': 'macaronhouse', 'description': 'Fransuz makaronlari'},
]

brands = []
for b_data in brands_data:
    brand, _ = Brand.objects.get_or_create(slug=b_data['slug'], defaults=b_data)
    brands.append(brand)
print(f'Brands created ({len(brands)})')

# ─── Create Categories ────────────────────────────────────────
categories_data = [
    {'name': 'Tortlar', 'slug': 'tortlar', 'description': 'Turli xillarda mazali tortlar'},
    {'name': 'Shokoladlar', 'slug': 'shokoladlar', 'description': 'Premium shokolad mahsulotlari'},
    {'name': 'Pechenyelar', 'slug': 'pechenyelar', 'description': 'Yangi pishirilgan pechenyelar'},
    {'name': 'Makaronlar', 'slug': 'makaronlar', 'description': 'Fransuz uslubida makaronlar'},
    {'name': 'Pishiriqlar', 'slug': 'pishiriqlar', 'description': 'Turli xillarda pishiriqlar'},
]
categories = {}
for cat_data in categories_data:
    cat, _ = Category.objects.get_or_create(slug=cat_data['slug'], defaults=cat_data)
    categories[cat.slug] = cat
print('Categories created')

# ─── Create Products ──────────────────────────────────────────
products_data = [
    {
        'name': 'Shokoladli Muxlisa Torti', 'slug': 'shokoladli-muxlisa-torti',
        'description': 'Premium shokoladli tort — haqiqiy qora shokolad va mascarpone kremidan tayyorlangan. Har bir bo\'lagi og\'izda eriydi.',
        'price': 127500, 'old_price': 150000, 'category_slug': 'tortlar', 'brand_slug': 'shirinliklar-dunyosi',
        'badge': 'Yangi', 'rating': 4.5, 'is_popular': True, 'sku': 'TRT-001', 'stock': 50,
        'ingredients': 'Qora shokolad, mascarpone, tuxum, un, sariyog\', shakar',
        'image': 'https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=800&h=600&fit=crop',
        'gallery': ['https://images.unsplash.com/photo-1606313564200-e75d5e30476c?w=800&h=600&fit=crop', 'https://images.unsplash.com/photo-1571115177098-24ec42ed204d?w=800&h=600&fit=crop', 'https://images.unsplash.com/photo-1563729784474-d77dbb933a9e?w=800&h=600&fit=crop'],
    },
    {
        'name': 'Fransuz Makaronlari', 'slug': 'fransuz-makaronlari',
        'description': 'Fransuz uslubida tayyorlangan rang-barang makaronlar. Badem qobi va kremli ichlik bilan.',
        'price': 85000, 'category_slug': 'makaronlar', 'brand_slug': 'macaronhouse',
        'badge': 'Yangi', 'rating': 5.0, 'is_popular': True, 'sku': 'MRN-001', 'stock': 100,
        'ingredients': 'Badem, tuxum oqi, shakar, krem, ranglar',
        'image': 'https://images.unsplash.com/photo-1569864358642-9d1684040f43?w=800&h=600&fit=crop',
        'gallery': ['https://images.unsplash.com/photo-1558326567-98ae2405596b?w=800&h=600&fit=crop', 'https://images.unsplash.com/photo-1612203985729-70726954388c?w=800&h=600&fit=crop'],
    },
    {
        'name': 'Klassik Shokoladli Pechenye', 'slug': 'klassik-shokoladli-pechenye',
        'description': 'Klassik uslubda pishirilgan shokoladli pechenye. Yong\'oq bo\'laklari bilan boyitilgan.',
        'price': 45000, 'category_slug': 'pechenyelar', 'brand_slug': 'sweethome',
        'rating': 4.0, 'sku': 'PCH-001', 'stock': 200,
        'ingredients': 'Un, shokolad, sariyog\', tuxum, shakar, vanilin',
        'image': 'https://images.unsplash.com/photo-1499636136210-6f4ee915583e?w=800&h=600&fit=crop',
        'gallery': ['https://images.unsplash.com/photo-1558961363-fa8fdf82db35?w=800&h=600&fit=crop', 'https://images.unsplash.com/photo-1548365328-8c850f1e7b83?w=800&h=600&fit=crop'],
    },
    {
        'name': 'Shokoladli Tiramisu', 'slug': 'shokoladli-tiramisu',
        'description': 'Klassik italyan shirinligining eksklyuziv talqini. Mascarpone va espresso bilan.',
        'price': 120000, 'category_slug': 'tortlar', 'brand_slug': 'pastryart',
        'is_popular': True, 'rating': 4.8, 'sku': 'TRT-002', 'stock': 30,
        'ingredients': 'Mascarpone, espresso, savoiardi, shokolad, kakao',
        'image': 'https://images.unsplash.com/photo-1571877227200-a0d98ea607e9?w=800&h=600&fit=crop',
        'gallery': ['https://images.unsplash.com/photo-1587314168485-3236d6710814?w=800&h=600&fit=crop', 'https://images.unsplash.com/photo-1542124948-dc391252a940?w=800&h=600&fit=crop'],
    },
    {
        'name': 'Qizil Baxmal', 'slug': 'qizil-baxmal',
        'description': 'Malinali qizil baxmal tort — yumshoq qizil biskvit va malinali krem bilan.',
        'price': 110000, 'category_slug': 'tortlar', 'brand_slug': 'shirinliklar-dunyosi',
        'rating': 4.7, 'sku': 'TRT-003', 'stock': 25,
        'ingredients': 'Malina, krem, un, tuxum, shakar, kakao',
        'image': 'https://images.unsplash.com/photo-1621303837174-89787a7d4729?w=800&h=600&fit=crop',
        'gallery': ['https://images.unsplash.com/photo-1614707267537-b85aaf00c4b7?w=800&h=600&fit=crop'],
    },
    {
        'name': 'Tryufel Tort', 'slug': 'tryufel-tort',
        'description': 'Qora shokoladli tryufel — boy va qora shokoladli mousse qatlamlari.',
        'price': 145000, 'category_slug': 'tortlar', 'brand_slug': 'chocolux',
        'rating': 4.9, 'sku': 'TRT-004', 'stock': 20,
        'ingredients': 'Qora shokolad, krem, sariyog\', tuxum, shakar',
        'image': 'https://images.unsplash.com/photo-1606890658317-7d14490b76fd?w=800&h=600&fit=crop',
        'gallery': ['https://images.unsplash.com/photo-1551024601-bec78aea704b?w=800&h=600&fit=crop'],
    },
    {
        'name': 'Klassik Chizkeyk', 'slug': 'klassik-chizkeyk',
        'description': 'Mevali klassik chizkeyk — yumshoq pishloqli teginish va yangi mevalar.',
        'price': 130000, 'category_slug': 'tortlar', 'brand_slug': 'pastryart',
        'rating': 4.6, 'sku': 'TRT-005', 'stock': 35,
        'ingredients': 'Pishloq, mevalar, shakar, tuxum, vanilin',
        'image': 'https://images.unsplash.com/photo-1533134486753-c833f0ed4866?w=800&h=600&fit=crop',
        'gallery': ['https://images.unsplash.com/photo-1524351199678-941a58a3df50?w=800&h=600&fit=crop'],
    },
    {
        'name': 'Asalli Tort', 'slug': 'asalli-tort',
        'description': 'An\'anaviy asalli tort — tabiiy asal bilan boyitilgan yumshoq pishiriq.',
        'price': 90000, 'category_slug': 'tortlar', 'brand_slug': 'sweethome',
        'rating': 4.3, 'sku': 'TRT-006', 'stock': 40,
        'ingredients': 'Asal, un, tuxum, sariyog\', yong\'oq',
        'image': 'https://images.unsplash.com/photo-1558961363-fa8fdf82db35?w=800&h=600&fit=crop',
        'gallery': ['https://images.unsplash.com/photo-1464305795204-6f5bbfc7fb81?w=800&h=600&fit=crop'],
    },
    {
        'name': 'Shokoladli Fondan', 'slug': 'shokoladli-fondan',
        'description': 'Premium qora shokoladli fondan — eriydigan teginish va boy ta\'m.',
        'price': 75000, 'old_price': 95000, 'category_slug': 'shokoladlar', 'brand_slug': 'chocolux',
        'badge': '-21%', 'rating': 4.8, 'sku': 'SHK-001', 'stock': 60,
        'ingredients': 'Qora shokolad, krem, sariyog\', kakao',
        'image': 'https://images.unsplash.com/photo-1549007994-cb92caebd54b?w=800&h=600&fit=crop',
        'gallery': ['https://images.unsplash.com/photo-1511381939415-e44015466834?w=800&h=600&fit=crop'],
    },
    {
        'name': 'Vanil Muffin', 'slug': 'vanil-muffin',
        'description': 'Yumshoq vanil muffin — shokolad bo\'laklari va qaymoqli ustki qism bilan.',
        'price': 35000, 'category_slug': 'pishiriqlar', 'brand_slug': 'sweethome',
        'rating': 4.4, 'sku': 'PSH-001', 'stock': 150,
        'ingredients': 'Un, vanil, tuxum, sariyog\', shakar, shokolad',
        'image': 'https://images.unsplash.com/photo-1607114910221-3b4b6c1d4b97?w=800&h=600&fit=crop',
        'gallery': ['https://images.unsplash.com/photo-1550617931-e17a7b70dce2?w=800&h=600&fit=crop'],
    },
    {
        'name': 'Qulupnay Mousse', 'slug': 'qulupnay-mousse',
        'description': 'Yangi qulupnay bilan tayyorlangan mousse — yengil va mazali desert.',
        'price': 95000, 'category_slug': 'tortlar', 'brand_slug': 'pastryart',
        'is_featured': True, 'rating': 4.7, 'sku': 'TRT-007', 'stock': 28,
        'ingredients': 'Qulupnay, krem, tuxum, shakar, gelatin',
        'image': 'https://images.unsplash.com/photo-1488477181946-6428a0291777?w=800&h=600&fit=crop',
        'gallery': ['https://images.unsplash.com/photo-1563805042-7684c019e1cb?w=800&h=600&fit=crop'],
    },
    {
        'name': 'Karamelli Keks', 'slug': 'karamelli-keks',
        'description': 'Karamel bilan boyitilgan yumshoq keks — bayram uchun ajoyib tanlov.',
        'price': 65000, 'category_slug': 'pishiriqlar', 'brand_slug': 'sweethome',
        'badge': 'Mashhur', 'rating': 4.5, 'sku': 'PSH-002', 'stock': 45,
        'ingredients': 'Un, karamel, tuxum, sariyog\', shakar',
        'image': 'https://images.unsplash.com/photo-1558961363-fa8fdf82db35?w=800&h=600&fit=crop',
        'gallery': ['https://images.unsplash.com/photo-1509440159596-0249088772ff?w=800&h=600&fit=crop'],
    },
    {
        'name': 'Qulupnay Chizkeyk', 'slug': 'qulupnay-chizkeyk',
        'description': 'Yangi qulupnay bilan bezatilgan mazali chizkeyk — yumshoq pishloqli asos.',
        'price': 115000, 'old_price': 140000, 'category_slug': 'tortlar', 'brand_slug': 'pastryart',
        'badge': '-18%', 'rating': 4.6, 'sku': 'TRT-008', 'stock': 22,
        'ingredients': 'Pishloq, qulupnay, shakar, tuxum, vanilin, pechene',
        'image': 'https://images.unsplash.com/photo-1533134486753-c833f0ed4866?w=800&h=600&fit=crop',
        'gallery': ['https://images.unsplash.com/photo-1524351199678-941a58a3df50?w=800&h=600&fit=crop'],
    },
    {
        'name': 'Shokoladli Kukus', 'slug': 'shokoladli-kukus',
        'description': 'Boy shokoladli kukus — ichida eriydigan shokolad bilan.',
        'price': 38000, 'category_slug': 'pechenyelar', 'brand_slug': 'chocolux',
        'rating': 4.7, 'sku': 'PCH-002', 'stock': 180,
        'ingredients': 'Un, shokolad, sariyog\', tuxum, shakar, vanilin',
        'image': 'https://images.unsplash.com/photo-1499636136210-6f4ee915583e?w=800&h=600&fit=crop',
        'gallery': ['https://images.unsplash.com/photo-1558961363-fa8fdf82db35?w=800&h=600&fit=crop'],
    },
    {
        'name': 'Yashil Choyli Makaron', 'slug': 'yashil-choyli-makaron',
        'description': 'Yashil choy ta\'mida tayyorlangan noyob makaron — kremli ganash bilan.',
        'price': 92000, 'category_slug': 'makaronlar', 'brand_slug': 'macaronhouse',
        'badge': 'Noyob', 'rating': 4.9, 'sku': 'MRN-002', 'stock': 40,
        'ingredients': 'Badem, yashil choy, tuxum oqi, shakar, krem',
        'image': 'https://images.unsplash.com/photo-1558326567-98ae2405596b?w=800&h=600&fit=crop',
        'gallery': ['https://images.unsplash.com/photo-1569864358642-9d1684040f43?w=800&h=600&fit=crop'],
    },
    {
        'name': 'Banana Pudding', 'slug': 'banana-pudding',
        'description': 'Klassik banana pudding — vanil krem va yangi banan qatlamlari.',
        'price': 55000, 'category_slug': 'pishiriqlar', 'brand_slug': 'sweethome',
        'rating': 4.4, 'sku': 'PSH-003', 'stock': 30,
        'ingredients': 'Banan, vanil krem, pechene, shakar, tuxum',
        'image': 'https://images.unsplash.com/photo-1488477181946-6428a0291777?w=800&h=600&fit=crop',
        'gallery': ['https://images.unsplash.com/photo-1563805042-7684c019e1cb?w=800&h=600&fit=crop'],
    },
    {
        'name': 'Qora Shokolad Seti', 'slug': 'qora-shokolad-seti',
        'description': '70%, 80% va 90% kakao bilan tayyorlangan premium shokolad to\'plami.',
        'price': 185000, 'old_price': 220000, 'category_slug': 'shokoladlar', 'brand_slug': 'chocolux',
        'badge': '-16%', 'rating': 4.8, 'sku': 'SHK-002', 'stock': 15,
        'ingredients': 'Qora shokolad (70%, 80%, 90%), kakao, sariyog\'',
        'image': 'https://images.unsplash.com/photo-1511381939415-e44015466834?w=800&h=600&fit=crop',
        'gallery': ['https://images.unsplash.com/photo-1549007994-cb92caebd54b?w=800&h=600&fit=crop'],
    },
    {
        'name': 'Lavashak Roll', 'slug': 'lavashak-roll',
        'description': 'Lavashak va qaymoq bilan tayyorlangan mazali roll — tez tayyorlanadigan desert.',
        'price': 42000, 'category_slug': 'pishiriqlar', 'brand_slug': 'sweethome',
        'rating': 4.3, 'sku': 'PSH-004', 'stock': 60,
        'ingredients': 'Lavashak, qaymoq, shakar, vanilin',
        'image': 'https://images.unsplash.com/photo-1509440159596-0249088772ff?w=800&h=600&fit=crop',
        'gallery': ['https://images.unsplash.com/photo-1550617931-e17a7b70dce2?w=800&h=600&fit=crop'],
    },
    {
        'name': 'Mango Mousse', 'slug': 'mango-mousse',
        'description': 'Tropik mango bilan tayyorlangan yengil mousse — issiq kunlar uchun ideal.',
        'price': 88000, 'category_slug': 'tortlar', 'brand_slug': 'pastryart',
        'is_featured': True, 'rating': 4.6, 'sku': 'TRT-009', 'stock': 18,
        'ingredients': 'Mango, krem, tuxum, shakar, gelatin',
        'image': 'https://images.unsplash.com/photo-1563805042-7684c019e1cb?w=800&h=600&fit=crop',
        'gallery': ['https://images.unsplash.com/photo-1488477181946-6428a0291777?w=800&h=600&fit=crop'],
    },
    {
        'name': 'Yong\'oqli Croissant', 'slug': 'yong-oqli-croissant',
        'description': 'Fransuz uslubida pishirilgan croissant — yong\'oq va asal bilan boyitilgan.',
        'price': 28000, 'category_slug': 'pishiriqlar', 'brand_slug': 'pastryart',
        'rating': 4.5, 'sku': 'PSH-005', 'stock': 100,
        'ingredients': 'Un, sariyog\', yong\'oq, asal, tuxum',
        'image': 'https://images.unsplash.com/photo-1555507036-ab1f4038024a?w=800&h=600&fit=crop',
        'gallery': ['https://images.unsplash.com/photo-1509440159596-0249088772ff?w=800&h=600&fit=crop'],
    },
    {
        'name': 'Klubnika Tort', 'slug': 'klubnika-tort',
        'description': 'Yangi klubnika bilan bezatilgan mazali tort — qaymoqli qatlamlar bilan.',
        'price': 135000, 'category_slug': 'tortlar', 'brand_slug': 'shirinliklar-dunyosi',
        'rating': 4.8, 'sku': 'TRT-010', 'stock': 20,
        'ingredients': 'Klubnika, qaymoq, un, tuxum, shakar, vanilin',
        'image': 'https://images.unsplash.com/photo-1565958011703-44f9829ba187?w=800&h=600&fit=crop',
        'gallery': ['https://images.unsplash.com/photo-1488477181946-6428a0291777?w=800&h=600&fit=crop'],
    },
    {
        'name': 'Nutella Pechenye', 'slug': 'nutella-pechenye',
        'description': 'Nutella bilan to\'ldirilgan mazali pechenye — bolalar va kattalar sevimlisi.',
        'price': 52000, 'old_price': 65000, 'category_slug': 'pechenyelar', 'brand_slug': 'chocolux',
        'badge': '-20%', 'rating': 4.6, 'sku': 'PCH-003', 'stock': 120,
        'ingredients': 'Un, Nutella, sariyog\', tuxum, shakar',
        'image': 'https://images.unsplash.com/photo-1558961363-fa8fdf82db35?w=800&h=600&fit=crop',
        'gallery': ['https://images.unsplash.com/photo-1548365328-8c850f1e7b83?w=800&h=600&fit=crop'],
    },
    {
        'name': 'Tiramisu Porsiyon', 'slug': 'tiramisu-porsiyon',
        'description': 'Shaxsiy porsiyadagi tiramisu — ofis yoki uy uchun ideal.',
        'price': 45000, 'category_slug': 'tortlar', 'brand_slug': 'pastryart',
        'rating': 4.7, 'sku': 'TRT-011', 'stock': 50,
        'ingredients': 'Mascarpone, espresso, savoiardi, kakao',
        'image': 'https://images.unsplash.com/photo-1587314168485-3236d6710814?w=800&h=600&fit=crop',
        'gallery': ['https://images.unsplash.com/photo-1542124948-dc391252a940?w=800&h=600&fit=crop'],
    },
    {
        'name': 'Shokoladli Fondyu', 'slug': 'shokoladli-fondyu',
        'description': 'Iste\'mol qilish uchun tayyor shokoladli fondyu — mevalar bilan.',
        'price': 78000, 'category_slug': 'shokoladlar', 'brand_slug': 'chocolux',
        'is_popular': True, 'rating': 4.9, 'sku': 'SHK-003', 'stock': 25,
        'ingredients': 'Qora shokolad, sut krem, vanilin',
        'image': 'https://images.unsplash.com/photo-1587132137056-bfbf0166836e?w=800&h=600&fit=crop',
        'gallery': ['https://images.unsplash.com/photo-1549007994-cb92caebd54b?w=800&h=600&fit=crop'],
    },
    {
        'name': 'Pista Mousse', 'slug': 'pista-mousse',
        'description': 'Pista yong\'oq bilan tayyorlangan noyob mousse — yashil rang va boy ta\'m.',
        'price': 105000, 'category_slug': 'tortlar', 'brand_slug': 'pastryart',
        'rating': 4.5, 'sku': 'TRT-012', 'stock': 15,
        'ingredients': 'Pista yong\'oq, krem, tuxum, shakar, vanilin',
        'image': 'https://images.unsplash.com/photo-1571877227200-a0d98ea607e9?w=800&h=600&fit=crop',
        'gallery': ['https://images.unsplash.com/photo-1563805042-7684c019e1cb?w=800&h=600&fit=crop'],
    },
    {
        'name': 'Qulupnay Tart', 'slug': 'qulupnay-tart',
        'description': 'Pechene asosida tayyorlangan qulupnay tart — mazali va chiroyli.',
        'price': 98000, 'category_slug': 'pishiriqlar', 'brand_slug': 'pastryart',
        'is_featured': True, 'rating': 4.7, 'sku': 'PSH-006', 'stock': 20,
        'ingredients': 'Pechene, qulupnay, qaymoq, shakar, jele',
        'image': 'https://images.unsplash.com/photo-1563805042-7684c019e1cb?w=800&h=600&fit=crop',
        'gallery': ['https://images.unsplash.com/photo-1488477181946-6428a0291777?w=800&h=600&fit=crop'],
    },
    {
        'name': 'Shokoladli Eclair', 'slug': 'shokoladli-eclair',
        'description': 'Fransuz eclair — shokoladli glazura va krem bilan to\'ldirilgan.',
        'price': 32000, 'category_slug': 'pishiriqlar', 'brand_slug': 'pastryart',
        'rating': 4.4, 'sku': 'PSH-007', 'stock': 80,
        'ingredients': 'Un, shokolad, krem, tuxum, sariyog\'',
        'image': 'https://images.unsplash.com/photo-1509440159596-0249088772ff?w=800&h=600&fit=crop',
        'gallery': ['https://images.unsplash.com/photo-1555507036-ab1f4038024a?w=800&h=600&fit=crop'],
    },
    {
        'name': 'Limon Chizkeyk', 'slug': 'limon-chizkeyk',
        'description': 'Limon ta\'mida tayyorlangan yengil chizkey — issiq kunlar uchun ideal.',
        'price': 110000, 'category_slug': 'tortlar', 'brand_slug': 'pastryart',
        'rating': 4.5, 'sku': 'TRT-013', 'stock': 25,
        'ingredients': 'Pishloq, limon, shakar, tuxum, pechene',
        'image': 'https://images.unsplash.com/photo-1524351199678-941a58a3df50?w=800&h=600&fit=crop',
        'gallery': ['https://images.unsplash.com/photo-1533134486753-c833f0ed4866?w=800&h=600&fit=crop'],
    },
    {
        'name': 'Malina Makaron', 'slug': 'malina-makaron',
        'description': 'Malinali makaron — yangi malina va qaymoqli ganash bilan.',
        'price': 88000, 'category_slug': 'makaronlar', 'brand_slug': 'macaronhouse',
        'rating': 4.8, 'sku': 'MRN-003', 'stock': 35,
        'ingredients': 'Badem, malina, tuxum oqi, shakar, qaymoq',
        'image': 'https://images.unsplash.com/photo-1612203985729-70726954388c?w=800&h=600&fit=crop',
        'gallery': ['https://images.unsplash.com/photo-1569864358642-9d1684040f43?w=800&h=600&fit=crop'],
    },
    {
        'name': 'Kokos Pechenye', 'slug': 'kokos-pechenye',
        'description': 'Kokos bo\'laklari bilan boyitilgan mazali pechenye — tropik ta\'m.',
        'price': 40000, 'category_slug': 'pechenyelar', 'brand_slug': 'sweethome',
        'rating': 4.3, 'sku': 'PCH-004', 'stock': 90,
        'ingredients': 'Un, kokos, sariyog\', tuxum, shakar',
        'image': 'https://images.unsplash.com/photo-1548365328-8c850f1e7b83?w=800&h=600&fit=crop',
        'gallery': ['https://images.unsplash.com/photo-1558961363-fa8fdf82db35?w=800&h=600&fit=crop'],
    },
    {
        'name': 'Shokoladli Croissant', 'slug': 'shokoladli-croissant',
        'description': 'Fransuz croissant — ichida qora shokolad bilan to\'ldirilgan.',
        'price': 35000, 'category_slug': 'pishiriqlar', 'brand_slug': 'pastryart',
        'badge': 'Yangi', 'rating': 4.6, 'sku': 'PSH-008', 'stock': 70,
        'ingredients': 'Un, sariyog\', shokolad, tuxum, shakar',
        'image': 'https://images.unsplash.com/photo-1555507036-ab1f4038024a?w=800&h=600&fit=crop',
        'gallery': ['https://images.unsplash.com/photo-1509440159596-0249088772ff?w=800&h=600&fit=crop'],
    },
    {
        'name': 'Yong\'oqli Tort', 'slug': 'yong-oqli-tort',
        'description': 'Turli xillarda yong\'oq bilan bezatilgan mazali tort.',
        'price': 155000, 'category_slug': 'tortlar', 'brand_slug': 'shirinliklar-dunyosi',
        'rating': 4.7, 'sku': 'TRT-014', 'stock': 18,
        'ingredients': 'Yong\'oq, shokolad, krem, un, tuxum, shakar',
        'image': 'https://images.unsplash.com/photo-1563729784474-d77dbb933a9e?w=800&h=600&fit=crop',
        'gallery': ['https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=800&h=600&fit=crop'],
    },
    {
        'name': 'Vanil Pirog', 'slug': 'vanil-pirog',
        'description': 'Vanil krem bilan to\'ldirilgan mazali pirog — pechene asosida.',
        'price': 72000, 'category_slug': 'pishiriqlar', 'brand_slug': 'sweethome',
        'rating': 4.4, 'sku': 'PSH-009', 'stock': 35,
        'ingredients': 'Un, vanil, tuxum, sariyog\', shakar, pechene',
        'image': 'https://images.unsplash.com/photo-1464305795204-6f5bbfc7fb81?w=800&h=600&fit=crop',
        'gallery': ['https://images.unsplash.com/photo-1551024506-0bccd828d307?w=800&h=600&fit=crop'],
    },
    {
        'name': 'Qora Shokolad Trufel', 'slug': 'qora-shokolad-trufel',
        'description': 'Qo\'lda tayyorlangan premium qora shokolad trufellar — 12 dona.',
        'price': 165000, 'old_price': 195000, 'category_slug': 'shokoladlar', 'brand_slug': 'chocolux',
        'badge': '-15%', 'rating': 4.9, 'sku': 'SHK-004', 'stock': 12,
        'ingredients': 'Qora shokolad, krem, kakao, vanilin',
        'image': 'https://images.unsplash.com/photo-1549007994-cb92caebd54b?w=800&h=600&fit=crop',
        'gallery': ['https://images.unsplash.com/photo-1511381939415-e44015466834?w=800&h=600&fit=crop'],
    },
    {
        'name': 'Apelsin Mousse', 'slug': 'apelsin-mousse',
        'description': 'Apelsin ta\'mida tayyorlangan yengil mousse — sitrusli yozgi desert.',
        'price': 82000, 'category_slug': 'tortlar', 'brand_slug': 'pastryart',
        'rating': 4.5, 'sku': 'TRT-015', 'stock': 22,
        'ingredients': 'Apelsin, krem, tuxum, shakar, gelatin',
        'image': 'https://images.unsplash.com/photo-1563805042-7684c019e1cb?w=800&h=600&fit=crop',
        'gallery': ['https://images.unsplash.com/photo-1571877227200-a0d98ea607e9?w=800&h=600&fit=crop'],
    },
    {
        'name': 'Makaron To\'plami', 'slug': 'makaron-toplami',
        'description': '12 xil makaron — turli rang va ta\'mlarda. Bayram uchun ideal.',
        'price': 250000, 'old_price': 300000, 'category_slug': 'makaronlar', 'brand_slug': 'macaronhouse',
        'badge': '-17%', 'rating': 4.8, 'sku': 'MRN-004', 'stock': 10,
        'ingredients': 'Badem, tuxum oqi, shakar, krem, turli ta\'mlar',
        'image': 'https://images.unsplash.com/photo-1569864358642-9d1684040f43?w=800&h=600&fit=crop',
        'gallery': ['https://images.unsplash.com/photo-1558326567-98ae2405596b?w=800&h=600&fit=crop'],
    },
    {
        'name': 'Qulupnay Pechenye', 'slug': 'qulupnay-pechenye',
        'description': 'Qulupnay bo\'laklari bilan boyitilgan mazali pechenye.',
        'price': 48000, 'category_slug': 'pechenyelar', 'brand_slug': 'sweethome',
        'rating': 4.5, 'sku': 'PCH-005', 'stock': 75,
        'ingredients': 'Un, qulupnay, sariyog\', tuxum, shakar',
        'image': 'https://images.unsplash.com/photo-1558961363-fa8fdf82db35?w=800&h=600&fit=crop',
        'gallery': ['https://images.unsplash.com/photo-1548365328-8c850f1e7b83?w=800&h=600&fit=crop'],
    },
    {
        'name': 'Karamel Fondan', 'slug': 'karamel-fondan',
        'description': 'Karamel bilan boyitilgan premium fondan — eriydigan teginish.',
        'price': 85000, 'category_slug': 'shokoladlar', 'brand_slug': 'chocolux',
        'rating': 4.7, 'sku': 'SHK-005', 'stock': 30,
        'ingredients': 'Karamel, sut shokolad, krem, sariyog\'',
        'image': 'https://images.unsplash.com/photo-1587132137056-bfbf0166836e?w=800&h=600&fit=crop',
        'gallery': ['https://images.unsplash.com/photo-1549007994-cb92caebd54b?w=800&h=600&fit=crop'],
    },
    {
        'name': 'Qora Shokoladli Keks', 'slug': 'qora-shokoladli-keks',
        'description': 'Boy qora shokoladli keks — shokolad ishqibozlari uchun.',
        'price': 58000, 'category_slug': 'pishiriqlar', 'brand_slug': 'chocolux',
        'rating': 4.6, 'sku': 'PSH-010', 'stock': 40,
        'ingredients': 'Un, qora shokolad, tuxum, sariyog\', shakar',
        'image': 'https://images.unsplash.com/photo-1558961363-fa8fdf82db35?w=800&h=600&fit=crop',
        'gallery': ['https://images.unsplash.com/photo-1509440159596-0249088772ff?w=800&h=600&fit=crop'],
    },
]

products = []
for p_data in products_data:
    cat_slug = p_data.pop('category_slug')
    brand_slug = p_data.pop('brand_slug', '')
    gallery_urls = p_data.pop('gallery', [])
    cat = categories.get(cat_slug)
    brand = next((b for b in brands if b.slug == brand_slug), None)
    product, created = Product.objects.get_or_create(
        slug=p_data['slug'],
        defaults={**p_data, 'category': cat, 'brand': brand}
    )
    if created:
        for i, url in enumerate(gallery_urls):
            ProductImage.objects.create(product=product, image=url, order=i, alt_text=f'{product.name} - rasm {i+1}')
    products.append(product)
print(f'Products ready ({len(products)} total)')

# ─── Create Coupons ───────────────────────────────────────────
coupons_data = [
    {'code': 'CHEGIRMA10', 'discount_percent': 10, 'min_order_amount': 50000, 'max_uses': 100},
    {'code': 'YANGIYIL', 'discount_percent': 15, 'min_order_amount': 100000, 'max_uses': 50},
    {'code': 'MEGA20', 'discount_percent': 20, 'min_order_amount': 200000, 'max_uses': 30},
]
for c_data in coupons_data:
    Coupon.objects.get_or_create(code=c_data['code'], defaults=c_data)
print('Coupons created')

# ─── Create Demo Orders ──────────────────────────────────────
if Order.objects.count() == 0:
    statuses = ['pending', 'confirmed', 'processing', 'packaging', 'delivering', 'delivered', 'cancelled']
    payment_methods = ['cash', 'card']
    now = timezone.now()

    for i in range(20):
        user = random.choice(users)
        product = random.choice(products)
        qty = random.randint(1, 5)
        subtotal = float(product.price) * qty
        delivery_fee = 15000
        total = subtotal + delivery_fee

        order = Order.objects.create(
            user=user,
            status=random.choice(statuses),
            full_name=f'{user.first_name} {user.last_name}',
            phone=user.phone,
            address_text='Toshkent sh., Amir Temur ko\'chasi, 15-uy',
            payment_method=random.choice(payment_methods),
            subtotal=subtotal,
            delivery_fee=delivery_fee,
            total_amount=total,
            created_at=now - timedelta(days=random.randint(0, 60)),
        )
        OrderItem.objects.create(order=order, product=product, product_name=product.name, quantity=qty, price=product.price)
    print('20 demo orders created')
else:
    print('Orders already exist, skipping')

# ─── Create Demo Reviews ──────────────────────────────────────
if Review.objects.count() == 0:
    review_comments = [
        'Juda mazali! Bolalar ham juda yoqtirishdi.',
        'Sifati ajoyib, yana buyurtma beraman.',
        'Yetkazib berish tez va professional.',
        'Mening sevimli mahsulotimga aylandi.',
        'Do\'stlarga tavsiya qildim, hammasi mamnun.',
        'Narx-sifat jihatidan juda yaxshi.',
        'Bayram uchun buyurtma qildim, hamma hayratda qoldi.',
        'Tarkibi tabiiy ekanligi juda yoqdi.',
        'Har safar yangi ta\'m sinab ko\'raman.',
        'Professional konditerlik mahsuloti.',
        'Klubnika tort juda mazali edi.',
        'Shokoladli trufel — haqiqiy lazzat!',
        'Makaronlari Fransuz restoranlaridan kam emas.',
        'Yetkazib berish juda tez bo\'ldi.',
        'Doimiy mijozman, sifat doim yuqori.',
        'Onam tug\'un kuni uchun tort buyurtma qildim.',
        'Cheesecake — eng yaxshisi shu yerda!',
        'Asalli tort tabiiy va mazali.',
        'Pechenyelar yangi va mazali.',
        'Mousse juda yengil va yoqimli.',
        'Yong\'oqli croissant — nonushta uchun ideal.',
        'Karamel fondan — eriydi og\'izda!',
        'Eclair — fransuz uslubida.',
        'Banana pudding bolalar sevimlisi.',
        'Pista mousse — noyob ta\'m.',
    ]

    for i in range(50):
        user = random.choice(users)
        product = random.choice(products)
        rating = random.choice([3, 4, 4, 4, 5, 5, 5])
        comment = random.choice(review_comments)

        review, created = Review.objects.get_or_create(
            user=user, product=product,
            defaults={'rating': rating, 'comment': comment}
        )
        if created:
            product.review_count = product.reviews.count()
            avg = sum(r.rating for r in product.reviews.all()) / product.review_count
            product.rating = round(avg, 1)
            product.save()
    print('50 demo reviews created')
else:
    print('Reviews already exist, skipping')

# ─── Create Demo Favorites ────────────────────────────────────
if Favorite.objects.count() == 0:
    for user in users[:5]:
        fav_products = random.sample(products, min(5, len(products)))
        for product in fav_products:
            Favorite.objects.get_or_create(user=user, product=product)
    print('Demo favorites created')
else:
    print('Favorites already exist, skipping')

# ─── Create Demo Addresses ────────────────────────────────────
from orders.models import Address as OrderAddress
if OrderAddress.objects.count() == 0:
    for user in users[:5]:
        OrderAddress.objects.get_or_create(
            user=user, title='Asosiy manzil',
            defaults={
                'full_name': f'{user.first_name} {user.last_name}',
                'phone': user.phone,
                'city': 'Toshkent',
                'district': 'Yunusobod',
                'street': 'Amir Temur ko\'chasi',
                'building': '15',
                'apartment': '2-qavat',
                'landmark': 'Metro yaqinida',
                'is_default': True,
            }
        )
    print('Demo addresses created')
else:
    print('Addresses already exist, skipping')

# ─── Create News ─────────────────────────────────────────────
from news.models import News
if News.objects.count() == 0:
    news_data = [
        {'title': 'Yangi ishlab chiqarish liniyasi ishga tushirildi', 'slug': 'yangi-ishlab-chiqarish-liniyasi', 'summary': 'Germaniya texnologiyasi asosida yangi avtomatlashtirilgan liniya ishga tushirildi.', 'content': 'Bizning kompaniyamiz yangi ishlab chiqarish liniyasini ishga tushirdi. Bu liniya yiliga 1000 tonna mahsulot ishlab chiqarish quvvatiga ega.', 'is_published': True},
        {'title': 'Xalqaro sertifikat olindi', 'slug': 'xalqaro-sertifikat', 'summary': 'ISO 22000:2018 xalqaro oziq-ovqat xavfsizligi sertifikati olindi.', 'content': 'Bizning kompaniyamiz ISO 22000:2018 xalqaro oziq-ovqat xavfsizligi menejmenti tizimi sertifikatini oldi.', 'is_published': True},
        {'title': 'Eksport hajmi 30% ga oshdi', 'slug': 'eksport-hajmi-oshdi', 'summary': 'Joriy yilda eksport hajmi 30% ga oshdi.', 'content': 'Bizning mahsulotlarimiz endi 10 dan ortiq davlatga eksport qilinmoqda.', 'is_published': True},
    ]
    for n_data in news_data:
        News.objects.get_or_create(slug=n_data['slug'], defaults=n_data)
    print('3 news articles created')

# ─── Create Gallery Categories & Images ─────────────────────
from gallery.models import GalleryCategory, GalleryImage
if GalleryCategory.objects.count() == 0:
    gc1, _ = GalleryCategory.objects.get_or_create(slug='ishlab-chiqarish', defaults={'name': 'Ishlab chiqarish', 'sort_order': 1})
    gc2, _ = GalleryCategory.objects.get_or_create(slug='mahsulotlar', defaults={'name': 'Mahsulotlar', 'sort_order': 2})
    gc3, _ = GalleryCategory.objects.get_or_create(slug='korxona', defaults={'name': 'Korxona', 'sort_order': 3})
    gallery_data = [
        {'title': 'Ishlab chiqarish liniyasi', 'image': 'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=800&h=600&fit=crop', 'category': gc1},
        {'title': 'Laboratoriya', 'image': 'https://images.unsplash.com/photo-1532187863486-abf9dbad1b69?w=800&h=600&fit=crop', 'category': gc1},
        {'title': 'Shokolad ishlab chiqarish', 'image': 'https://images.unsplash.com/photo-1481391319762-47dff72954d9?w=800&h=600&fit=crop', 'category': gc2},
        {'title': 'Tort tayyorlash', 'image': 'https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=800&h=600&fit=crop', 'category': gc2},
        {'title': 'Korxona binosi', 'image': 'https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?w=800&h=600&fit=crop', 'category': gc3},
    ]
    for g_data in gallery_data:
        GalleryImage.objects.get_or_create(title=g_data['title'], defaults=g_data)
    print('Gallery categories and images created')

# ─── Create Certificates ────────────────────────────────────
from certificates.models import Certificate
if Certificate.objects.count() == 0:
    cert_data = [
        {'title': 'ISO 9001:2015', 'description': 'Sifat menejmenti tizimi', 'issued_by': 'ISO', 'is_active': True},
        {'title': 'ISO 22000:2018', 'description': 'Oziq-ovqat xavfsizligi menejmenti', 'issued_by': 'ISO', 'is_active': True},
        {'title': 'Halal Certification', 'description': 'Halol sertifikat', 'issued_by': 'Halal Board', 'is_active': True},
        {'title': 'HACCP', 'description': 'Xavfli nuqtalar nazorati', 'issued_by': 'HACCP International', 'is_active': True},
    ]
    for c_data in cert_data:
        Certificate.objects.get_or_create(title=c_data['title'], defaults=c_data)
    print('Certificates created')

# ─── Create Company ─────────────────────────────────────────
from pages.models import Company
company, _ = Company.objects.get_or_create(pk=1, defaults={
    'name': 'Confectionery Enterprise',
    'tagline': 'Sifat va an\'analar uyg\'unligi',
    'description': '1999-yilda asos solingan "Confectionery Enterprise" fabrikasi kichik oilaviy korxonadan Markaziy Osiyodagi eng yirik ishlab chiqarish quvvatlaridan biriga aylandi.',
    'mission': 'Sifatli shirinliklar orqali hayotingizga quvonch ulashish.',
    'founded_year': 1999,
    'employee_count': '500+',
    'phone': '+998 71 123 45 67',
    'email': 'info@confectionery.uz',
    'address': 'Toshkent sh., Yunusobod tumani, 5-mavze.',
    'experience_years': '25+',
    'product_types': '100+',
    'export_countries': '10+',
    'partner_stores': '100+',
})
print('Company info created')

print('\n=== Seed completed successfully! ===')
print('Admin: admin / admin123')
print('User: user1 / user1234 (or user2-user10 / user1234)')
