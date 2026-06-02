# ai_dataset.py
# Оцінки camera/performance/battery/series — чим новіша і краща модель, тим вище.
# Шкала 1-10, де 10 = найкраще на ринку станом на 2025 рік.

def _clean_product(product: dict) -> dict:
    cleaned = dict(product)
    cleaned["name"] = str(cleaned["name"]).strip()
    cleaned["category"] = str(cleaned["category"]).strip()
    cleaned["price"] = int(cleaned["price"])
    cleaned["performance"] = max(1, min(10, int(cleaned["performance"])))
    cleaned["camera"] = max(1, min(10, int(cleaned["camera"])))
    cleaned["battery"] = max(1, min(10, int(cleaned["battery"])))
    cleaned["size"] = float(cleaned["size"])
    cleaned["description"] = str(cleaned["description"]).strip()

    tags = []
    seen = set()
    for tag in cleaned.get("tags", []):
        normalized = str(tag).strip()
        if normalized and normalized not in seen:
            seen.add(normalized)
            tags.append(normalized)
    cleaned["tags"] = tags

    if "year" in cleaned:
        cleaned["year"] = int(cleaned["year"])
    if "series" in cleaned:
        cleaned["series"] = int(cleaned["series"])

    return cleaned


RAW_APPLE_PRODUCTS = [

# =========================
# 📱 iPhone 17 SERIES (2025)
# =========================
{"id":"iphone-17-pro-max","name":"iPhone 17 Pro Max","category":"iPhone","series":17,"price":1299,"performance":10,"camera":10,"battery":10,"size":6.9,
 "tags":["новий","флагман","топова камера","найкраща камера","перископ","великий","потужний","ai"],
 "description":"Флагман 2025 року. Чип A19 Pro, найкраща камера з перископним зумом та екран 6.9 дюйма."},

{"id":"iphone-17-pro","name":"iPhone 17 Pro","category":"iPhone","series":17,"price":1099,"performance":10,"camera":10,"battery":9,"size":6.3,
 "tags":["новий","флагман","топова камера","найкраща камера","ai","потужний"],
 "description":"Найновіший Pro з чипом A19 Pro, революційною камерою та Apple Intelligence."},

{"id":"iphone-air-2025","name":"iPhone Air","category":"iPhone","series":17,"price":999,"performance":9,"camera":9,"battery":8,"size":6.6,
 "tags":["новий","тонкий","легкий","ai","гарна камера","2025"],
 "description":"Тонкий iPhone Air з великим дисплеєм, сучасною камерою та чипом покоління A19. Поточна преміальна легка модель Apple."},

{"id":"iphone-17e","name":"iPhone 17e","category":"iPhone","series":17,"price":599,"performance":8,"camera":7,"battery":8,"size":6.1,
 "tags":["новий","доступний","бюджетний","ai","2026"],
 "description":"Доступніший сучасний iPhone зі свіжим поколінням Apple Intelligence, хорошою автономністю та збалансованою продуктивністю."},

{"id":"iphone-17","name":"iPhone 17","category":"iPhone","series":17,"price":799,"performance":9,"camera":9,"battery":9,"size":6.1,
 "tags":["новий","сучасний","ai","гарна камера"],
 "description":"Базовий iPhone 2025 з A19, покращеною камерою та Apple Intelligence."},

# =========================
# 📱 iPhone 16 SERIES (2024)
# =========================
{"id":"iphone-16-pro-max","name":"iPhone 16 Pro Max","category":"iPhone","series":16,"price":1199,"performance":9,"camera":9,"battery":9,"size":6.9,
 "tags":["флагман","топова камера","48мп","великий","потужний","ai","titanium"],
 "description":"Чип A18 Pro, камера 48 Мп з 5x зумом, великий екран 6.9 дюйма та Apple Intelligence."},

{"id":"iphone-16-pro","name":"iPhone 16 Pro","category":"iPhone","series":16,"price":999,"performance":9,"camera":9,"battery":8,"size":6.3,
 "tags":["флагман","топова камера","48мп","потужний","ai","titanium"],
 "description":"A18 Pro, камера 48 Мп з Camera Control та Apple Intelligence."},

{"id":"iphone-16-plus","name":"iPhone 16 Plus","category":"iPhone","series":16,"price":799,"performance":8,"camera":8,"battery":10,"size":6.7,
 "tags":["великий","автономність","ai","гарна камера"],
 "description":"Великий екран, рекордна автономність та чип A18."},

{"id":"iphone-16","name":"iPhone 16","category":"iPhone","series":16,"price":699,"performance":8,"camera":8,"battery":9,"size":6.1,
 "tags":["сучасний","ai","гарна камера","camera-control"],
 "description":"Чип A18, Camera Control та якісна зйомка у базовій моделі."},

# =========================
# 📱 iPhone 15 SERIES (2023)
# =========================
{"id":"iphone-15-pro-max","name":"iPhone 15 Pro Max","category":"iPhone","series":15,"price":999,"performance":8,"camera":8,"battery":8,"size":6.7,
 "tags":["флагман","титан","гарна камера","48мп","5x зум","великий"],
 "description":"Титановий корпус, A17 Pro та унікальний 5x оптичний зум."},

{"id":"iphone-15-pro","name":"iPhone 15 Pro","category":"iPhone","series":15,"price":849,"performance":8,"camera":8,"battery":7,"size":6.1,
 "tags":["флагман","титан","гарна камера","48мп","кнопка дій"],
 "description":"Титановий корпус, A17 Pro та головний сенсор 48 Мп."},

{"id":"iphone-15-plus","name":"iPhone 15 Plus","category":"iPhone","series":15,"price":799,"performance":7,"camera":7,"battery":9,"size":6.7,
 "tags":["великий","автономність","usb-c","dynamic-island"],
 "description":"Найдовша автономність серед базових моделей та великий екран."},

{"id":"iphone-15","name":"iPhone 15","category":"iPhone","series":15,"price":699,"performance":7,"camera":7,"battery":7,"size":6.1,
 "tags":["сучасний","usb-c","dynamic-island","48мп"],
 "description":"Dynamic Island, USB-C та сенсор 48 Мп у базовій моделі."},

# =========================
# 📱 iPhone 14 SERIES (2022)
# =========================
{"id":"iphone-14-pro-max","name":"iPhone 14 Pro Max","category":"iPhone","series":14,"price":849,"performance":8,"camera":7,"battery":8,"size":6.7,
 "tags":["флагман","dynamic-island","великий","120гц"],
 "description":"Dynamic Island, Always-On дисплей та чип A16 Bionic."},

{"id":"iphone-14-pro","name":"iPhone 14 Pro","category":"iPhone","series":14,"price":749,"performance":8,"camera":7,"battery":7,"size":6.1,
 "tags":["флагман","dynamic-island","120гц"],
 "description":"Dynamic Island, ProMotion 120 Гц та A16 Bionic."},

{"id":"iphone-14-plus","name":"iPhone 14 Plus","category":"iPhone","series":14,"price":649,"performance":6,"camera":6,"battery":8,"size":6.7,
 "tags":["великий","автономність"],
 "description":"Великий екран 6.7 дюйма та хороша автономність на A15."},

{"id":"iphone-14","name":"iPhone 14","category":"iPhone","series":14,"price":549,"performance":6,"camera":6,"battery":7,"size":6.1,
 "tags":["надійний","стабільний"],
 "description":"Надійний смартфон з A15 Bionic та аварійним SOS."},

# =========================
# 📱 iPhone 13 SERIES (2021)
# =========================
{"id":"iphone-13-pro-max","name":"iPhone 13 Pro Max","category":"iPhone","series":13,"price":749,"performance":7,"camera":7,"battery":9,"size":6.7,
 "tags":["автономність","великий","макро","120гц"],
 "description":"Відмінна автономність, макрозйомка та ProMotion 120 Гц."},

{"id":"iphone-13-pro","name":"iPhone 13 Pro","category":"iPhone","series":13,"price":649,"performance":7,"camera":7,"battery":7,"size":6.1,
 "tags":["макро","120гц","лідар"],
 "description":"Макрозйомка, LiDAR та ProMotion на A15 Bionic."},

{"id":"iphone-13","name":"iPhone 13","category":"iPhone","series":13,"price":499,"performance":6,"camera":6,"battery":7,"size":6.1,
 "tags":["збалансований","ціна-якість"],
 "description":"Збалансований смартфон з A15 Bionic за розумною ціною."},

{"id":"iphone-13-mini","name":"iPhone 13 Mini","category":"iPhone","series":13,"price":399,"performance":6,"camera":6,"battery":5,"size":5.4,
 "tags":["компактний","малий","легкий","маленький"],
 "description":"Компактний смартфон 5.4 дюйма для однієї руки."},

# =========================
# 📱 iPhone 12 SERIES (2020)
# =========================
{"id":"iphone-12-pro-max","name":"iPhone 12 Pro Max","category":"iPhone","series":12,"price":649,"performance":6,"camera":6,"battery":7,"size":6.7,
 "tags":["лідар","великий","oled"],
 "description":"Великий OLED екран та LiDAR на A14 Bionic."},

{"id":"iphone-12-pro","name":"iPhone 12 Pro","category":"iPhone","series":12,"price":549,"performance":6,"camera":6,"battery":6,"size":6.1,
 "tags":["лідар","oled","преміум"],
 "description":"LiDAR та три об'єктиви на A14 Bionic."},

{"id":"iphone-12","name":"iPhone 12","category":"iPhone","series":12,"price":449,"performance":5,"camera":5,"battery":5,"size":6.1,
 "tags":["oled","5g"],
 "description":"OLED дисплей та підтримка 5G на A14 Bionic."},

{"id":"iphone-12-mini","name":"iPhone 12 Mini","category":"iPhone","series":12,"price":349,"performance":5,"camera":5,"battery":4,"size":5.4,
 "tags":["компактний","малий","oled","маленький"],
 "description":"Найменший смартфон з OLED та 5G."},

# =========================
# 📱 iPhone 11 SERIES (2019)
# =========================
{"id":"iphone-11-pro-max","name":"iPhone 11 Pro Max","category":"iPhone","series":11,"price":449,"performance":5,"camera":5,"battery":8,"size":6.5,
 "tags":["великий","автономність","oled","три об'єктиви"],
 "description":"Три об'єктиви та висока автономність на A13 Bionic."},

{"id":"iphone-11-pro","name":"iPhone 11 Pro","category":"iPhone","series":11,"price":399,"performance":5,"camera":5,"battery":6,"size":5.8,
 "tags":["oled","три об'єктиви","нічний режим"],
 "description":"Три об'єктиви з нічним режимом на A13 Bionic."},

{"id":"iphone-11","name":"iPhone 11","category":"iPhone","series":11,"price":299,"performance":4,"camera":4,"battery":6,"size":6.1,
 "tags":["доступний","бюджет","надійний"],
 "description":"Доступний та надійний смартфон з A13 Bionic."},

# =========================
# 📱 iPhone SE SERIES
# =========================
{"id":"iphone-se-3","name":"iPhone SE (2022)","category":"iPhone","series":13,"price":349,"performance":6,"camera":5,"battery":5,"size":4.7,
 "tags":["кнопка","5g","компактний","бюджет","маленький","touch-id"],
 "description":"Компактний корпус з потужним A15 та підтримкою 5G."},

{"id":"iphone-se-2","name":"iPhone SE (2020)","category":"iPhone","series":8,"price":199,"performance":5,"camera":4,"battery":4,"size":4.7,
 "tags":["кнопка","компактний","бюджет","маленький","touch-id","дешевий"],
 "description":"Класичний компактний дизайн з A13 Bionic."},

# =========================
# 📱 iPhone XR / XS / X
# =========================
{"id":"iphone-xr","name":"iPhone XR","category":"iPhone","series":10,"price":199,"performance":3,"camera":4,"battery":6,"size":6.1,
 "tags":["бюджет","стара","дешевий","доступний"],
 "description":"Доступна стара модель з LCD екраном."},

{"id":"iphone-xs","name":"iPhone XS","category":"iPhone","series":10,"price":179,"performance":3,"camera":4,"battery":4,"size":5.8,
 "tags":["oled","стара","дешевий"],
 "description":"Стара модель з OLED екраном та Face ID."},

{"id":"iphone-x","name":"iPhone X","category":"iPhone","series":10,"price":149,"performance":3,"camera":3,"battery":4,"size":5.8,
 "tags":["стара","oled","дешевий","перший безрамковий"],
 "description":"Перша безрамкова модель Apple."},

# =========================
# 📱 iPhone 8 / 7
# =========================
{"id":"iphone-8","name":"iPhone 8","category":"iPhone","series":8,"price":149,"performance":2,"camera":3,"battery":3,"size":4.7,
 "tags":["кнопка","стара","дешевий","компактний"],
 "description":"Класична модель з Touch ID та A11 Bionic."},

{"id":"iphone-7","name":"iPhone 7","category":"iPhone","series":7,"price":99,"performance":2,"camera":2,"battery":3,"size":4.7,
 "tags":["найдешевший","стара","дешевий","компактний"],
 "description":"Бюджетний варіант для базових задач."},


# ================================
# 💻 MacBook Air SERIES (2020–2024)
# ================================

{"id":"macbook-air-m1-2020","name":"MacBook Air 13\" M1 (2020)","category":"MacBook","year":2020,"series":2020,"price":649,"performance":7,"camera":4,"battery":8,"size":13.3,
 "tags":["ноутбук","m1","легкий","портативний","бюджет","дешевий","навчання","доступний","2020"],
 "description":"Перший MacBook на Apple Silicon M1 — тихий без вентилятора, швидкий, до 18 год автономності."},

{"id":"macbook-air-m2-2022","name":"MacBook Air 13\" M2 (2022)","category":"MacBook","year":2022,"series":2022,"price":899,"performance":8,"camera":5,"battery":9,"size":13.6,
 "tags":["ноутбук","m2","легкий","портативний","навчання","тонкий","magsafe","2022"],
 "description":"Новий дизайн без вентилятора, M2, MagSafe та нотч. Найпопулярніший MacBook для навчання."},

{"id":"macbook-air-m2-15-2023","name":"MacBook Air 15\" M2 (2023)","category":"MacBook","year":2023,"series":2023,"price":1099,"performance":8,"camera":5,"battery":9,"size":15.3,
 "tags":["ноутбук","m2","великий екран","легкий","навчання","робота","автономність","2023"],
 "description":"Перший 15\" Air з M2 — великий Liquid Retina екран та до 18 год без вентилятора."},

{"id":"macbook-air-m3-13-2024","name":"MacBook Air 13\" M3 (2024)","category":"MacBook","year":2024,"series":2024,"price":1099,"performance":9,"camera":6,"battery":10,"size":13.6,
 "tags":["ноутбук","m3","легкий","портативний","навчання","робота","автономність","новий","2024"],
 "description":"MacBook Air з M3 підтримує зовнішній дисплей у закритому вигляді. Wi-Fi 6E, до 18 год."},

{"id":"macbook-air-m3-15-2024","name":"MacBook Air 15\" M3 (2024)","category":"MacBook","year":2024,"series":2024,"price":1299,"performance":9,"camera":6,"battery":10,"size":15.3,
 "tags":["ноутбук","m3","великий екран","легкий","навчання","робота","автономність","новий","2024"],
 "description":"Найбільший Air з M3 — великий 15.3\" Liquid Retina, до 18 год автономності та Wi‑Fi 6E."},

{"id":"macbook-air-m5-13-2026","name":"MacBook Air 13\" M5 (2026)","category":"MacBook","year":2026,"series":2026,"price":1099,"performance":10,"camera":7,"battery":10,"size":13.6,
 "tags":["ноутбук","m5","легкий","портативний","навчання","робота","автономність","новий","2026"],
 "description":"Актуальний MacBook Air з M5, 512GB стартового сховища, Wi‑Fi 7 і покращеною камерою Center Stage."},

{"id":"macbook-air-m5-15-2026","name":"MacBook Air 15\" M5 (2026)","category":"MacBook","year":2026,"series":2026,"price":1299,"performance":10,"camera":7,"battery":10,"size":15.3,
 "tags":["ноутбук","m5","великий екран","легкий","навчання","робота","автономність","новий","2026"],
 "description":"Великий MacBook Air з M5 для тих, кому потрібні простір екрана, мобільність та довга автономність."},

{"id":"macbook-neo-2026","name":"MacBook Neo (2026)","category":"MacBook","year":2026,"series":2026,"price":599,"performance":7,"camera":6,"battery":9,"size":13.0,
 "tags":["ноутбук","neo","бюджет","навчання","доступний","портативний","новий","2026"],
 "description":"Нова доступна модель MacBook Neo з 13-дюймовим Liquid Retina дисплеєм, Apple silicon та довгою автономністю."},


# =================================
# 💻 MacBook Pro 14\" SERIES (2021–2024)
# =================================

{"id":"macbook-pro-m1-pro-14-2021","name":"MacBook Pro 14\" M1 Pro (2021)","category":"MacBook","year":2021,"series":2021,"price":899,"performance":8,"camera":6,"battery":8,"size":14.2,
 "tags":["ноутбук","m1 pro","потужний","програмування","портативний","mini-led","hdmi","sd","бюджет","2021"],
 "description":"Перший Pro 14\" на M1 Pro з Mini-LED ProMotion 120 Гц, HDMI та SD-card. Чудова ціна."},

{"id":"macbook-pro-m1-max-14-2021","name":"MacBook Pro 14\" M1 Max (2021)","category":"MacBook","year":2021,"series":2021,"price":1299,"performance":9,"camera":6,"battery":9,"size":14.2,
 "tags":["ноутбук","m1 max","потужний","відеомонтаж","3d","програмування","gpu","2021"],
 "description":"M1 Max у компактному 14\" форматі — потужна GPU для відеомонтажу та 3D за хорошою ціною."},

{"id":"macbook-pro-m2-pro-14-2023","name":"MacBook Pro 14\" M2 Pro (2023)","category":"MacBook","year":2023,"series":2023,"price":1499,"performance":9,"camera":7,"battery":9,"size":14.2,
 "tags":["ноутбук","m2 pro","потужний","програмування","відеомонтаж","портативний","бюджет","2023"],
 "description":"MacBook Pro 14\" з M2 Pro — висока продуктивність та портативність за розумною ціною."},

{"id":"macbook-pro-m2-max-14-2023","name":"MacBook Pro 14\" M2 Max (2023)","category":"MacBook","year":2023,"series":2023,"price":1999,"performance":10,"camera":7,"battery":9,"size":14.2,
 "tags":["ноутбук","m2 max","потужний","відеомонтаж","3d","рендер","програмування","2023"],
 "description":"M2 Max у 14\" форматі — топова продуктивність у компактному корпусі."},

{"id":"macbook-pro-m3-14-2023","name":"MacBook Pro 14\" M3 (2023)","category":"MacBook","year":2023,"series":2023,"price":1299,"performance":8,"camera":7,"battery":8,"size":14.2,
 "tags":["ноутбук","m3","потужний","програмування","портативний","hw-raytracing","2023"],
 "description":"Базовий MacBook Pro 14\" з M3 та апаратним ray-tracing — більше потужності ніж Air."},

{"id":"macbook-pro-m3-pro-14-2023","name":"MacBook Pro 14\" M3 Pro (2023)","category":"MacBook","year":2023,"series":2023,"price":1799,"performance":9,"camera":7,"battery":9,"size":14.2,
 "tags":["ноутбук","m3 pro","потужний","програмування","відеомонтаж","портативний","2023"],
 "description":"MacBook Pro 14\" з M3 Pro та ProMotion 120 Гц — ідеальний баланс потужності та портативності."},

{"id":"macbook-pro-m3-max-14-2023","name":"MacBook Pro 14\" M3 Max (2023)","category":"MacBook","year":2023,"series":2023,"price":2499,"performance":10,"camera":7,"battery":9,"size":14.2,
 "tags":["ноутбук","m3 max","найпотужніший","відеомонтаж","3d","рендер","2023"],
 "description":"M3 Max у 14\" форматі — максимальна потужність у компактному Pro-корпусі."},

{"id":"macbook-pro-m4-14-2024","name":"MacBook Pro 14\" M4 (2024)","category":"MacBook","year":2024,"series":2024,"price":1599,"performance":9,"camera":7,"battery":9,"size":14.2,
 "tags":["ноутбук","m4","потужний","програмування","портативний","thunderbolt5","новий","2024"],
 "description":"MacBook Pro 14\" з M4 — Thunderbolt 5, nano-texture опція та до 24 год автономності."},

{"id":"macbook-pro-m4-pro-14-2024","name":"MacBook Pro 14\" M4 Pro (2024)","category":"MacBook","year":2024,"series":2024,"price":1999,"performance":10,"camera":7,"battery":9,"size":14.2,
 "tags":["ноутбук","m4 pro","потужний","програмування","відеомонтаж","портативний","thunderbolt5","новий","2024"],
 "description":"MacBook Pro 14\" з M4 Pro та Thunderbolt 5 — найкраща портативна робоча станція 2024 року."},

{"id":"macbook-pro-m4-max-14-2024","name":"MacBook Pro 14\" M4 Max (2024)","category":"MacBook","year":2024,"series":2024,"price":2799,"performance":10,"camera":7,"battery":9,"size":14.2,
 "tags":["ноутбук","m4 max","найпотужніший","відеомонтаж","3d","рендер","програмування","новий","2024"],
 "description":"M4 Max у компактному 14\" — безкомпромісна потужність для ML та важкого відеомонтажу."},


# =================================
# 💻 MacBook Pro 16\" SERIES (2021–2024)
# =================================

{"id":"macbook-pro-m1-pro-16-2021","name":"MacBook Pro 16\" M1 Pro (2021)","category":"MacBook","year":2021,"series":2021,"price":1099,"performance":8,"camera":6,"battery":9,"size":16.2,
 "tags":["ноутбук","m1 pro","великий екран","потужний","програмування","відеомонтаж","hdmi","sd","бюджет","2021"],
 "description":"Перший Pro 16\" на M1 Pro з Mini-LED екраном ProMotion, HDMI та SD-card за чудовою ціною."},

{"id":"macbook-pro-m1-max-16-2021","name":"MacBook Pro 16\" M1 Max (2021)","category":"MacBook","year":2021,"series":2021,"price":1499,"performance":9,"camera":6,"battery":9,"size":16.2,
 "tags":["ноутбук","m1 max","великий екран","потужний","відеомонтаж","3d","рендер","бюджет","2021"],
 "description":"M1 Max у великому 16\" форматі — потужна GPU та великий екран для серйозної роботи."},

{"id":"macbook-pro-m2-pro-16-2023","name":"MacBook Pro 16\" M2 Pro (2023)","category":"MacBook","year":2023,"series":2023,"price":2099,"performance":9,"camera":7,"battery":9,"size":16.2,
 "tags":["ноутбук","m2 pro","великий екран","потужний","програмування","відеомонтаж","бюджет","2023"],
 "description":"MacBook Pro 16\" з M2 Pro — великий екран та висока продуктивність за розумною ціною."},

{"id":"macbook-pro-m2-max-16-2023","name":"MacBook Pro 16\" M2 Max (2023)","category":"MacBook","year":2023,"series":2023,"price":2799,"performance":10,"camera":7,"battery":9,"size":16.2,
 "tags":["ноутбук","m2 max","великий екран","потужний","відеомонтаж","3d","рендер","2023"],
 "description":"MacBook Pro 16\" з M2 Max — флагманська станція для відеомонтажу та складного рендерингу."},

{"id":"macbook-pro-m3-pro-16-2023","name":"MacBook Pro 16\" M3 Pro (2023)","category":"MacBook","year":2023,"series":2023,"price":2499,"performance":9,"camera":7,"battery":9,"size":16.2,
 "tags":["ноутбук","m3 pro","великий екран","потужний","програмування","відеомонтаж","2023"],
 "description":"MacBook Pro 16\" з M3 Pro та ProMotion — великий екран та висока продуктивність."},

{"id":"macbook-pro-m3-max-16-2023","name":"MacBook Pro 16\" M3 Max (2023)","category":"MacBook","year":2023,"series":2023,"price":3199,"performance":10,"camera":7,"battery":9,"size":16.2,
 "tags":["ноутбук","m3 max","великий екран","найпотужніший","відеомонтаж","3d","рендер","2023"],
 "description":"MacBook Pro 16\" з M3 Max — топова робоча станція для відеомонтажу 8K та 3D."},

{"id":"macbook-pro-m4-pro-16-2024","name":"MacBook Pro 16\" M4 Pro (2024)","category":"MacBook","year":2024,"series":2024,"price":2499,"performance":10,"camera":7,"battery":10,"size":16.2,
 "tags":["ноутбук","m4 pro","великий екран","потужний","відеомонтаж","програмування","автономність","thunderbolt5","новий","2024"],
 "description":"MacBook Pro 16\" з M4 Pro — Thunderbolt 5, до 24 год автономності та великий ProMotion екран."},

{"id":"macbook-pro-m4-max-16-2024","name":"MacBook Pro 16\" M4 Max (2024)","category":"MacBook","year":2024,"series":2024,"price":3499,"performance":10,"camera":7,"battery":10,"size":16.2,
 "tags":["ноутбук","m4 max","великий екран","найпотужніший","відеомонтаж","3d","рендер","ml","новий","2024"],
 "description":"Найпотужніший MacBook 2024 з M4 Max — для відеомонтажу 8K, складного 3D та ML задач."},


# =================================
# 🗒 iPad Pro SERIES (2020–2024)
# =================================

{"id":"ipad-pro-a12z-11-2020","name":"iPad Pro 11\" A12Z (2020)","category":"iPad","year":2020,"series":2020,"price":399,"performance":6,"camera":7,"battery":7,"size":11.0,
 "tags":["планшет","a12z","лідар","малювання","стілус","портативний","бюджет","дешевий","2020"],
 "description":"iPad Pro 11\" 2020 з A12Z Bionic та LiDAR сканером. Підтримує Magic Keyboard та Apple Pencil 2."},

{"id":"ipad-pro-a12z-12-2020","name":"iPad Pro 12.9\" A12Z (2020)","category":"iPad","year":2020,"series":2020,"price":499,"performance":6,"camera":7,"battery":8,"size":12.9,
 "tags":["планшет","a12z","великий","лідар","малювання","стілус","бюджет","2020"],
 "description":"Великий iPad Pro 2020 з A12Z та LiDAR. Підтримує Magic Keyboard та Apple Pencil 2."},

{"id":"ipad-pro-m1-11-2021","name":"iPad Pro 11\" M1 (2021)","category":"iPad","year":2021,"series":2021,"price":549,"performance":8,"camera":8,"battery":8,"size":11.0,
 "tags":["планшет","m1","малювання","стілус","портативний","thunderbolt","5g","2021"],
 "description":"iPad Pro 11\" з M1 та Thunderbolt — величезний стрибок у продуктивності для планшета."},

{"id":"ipad-pro-m1-12-2021","name":"iPad Pro 12.9\" M1 (2021)","category":"iPad","year":2021,"series":2021,"price":749,"performance":8,"camera":8,"battery":9,"size":12.9,
 "tags":["планшет","m1","великий","малювання","стілус","mini-led","liquid-retina-xdr","2021"],
 "description":"iPad Pro 12.9\" з M1 та революційним Mini-LED Liquid Retina XDR дисплеєм."},

{"id":"ipad-pro-m2-11-2022","name":"iPad Pro 11\" M2 (2022)","category":"iPad","year":2022,"series":2022,"price":649,"performance":9,"camera":8,"battery":8,"size":11.0,
 "tags":["планшет","m2","малювання","стілус","портативний","hover","prores","2022"],
 "description":"iPad Pro 11\" з M2 — підтримує Apple Pencil hover та ProRes відеозйомку."},

{"id":"ipad-pro-m2-12-2022","name":"iPad Pro 12.9\" M2 (2022)","category":"iPad","year":2022,"series":2022,"price":849,"performance":9,"camera":8,"battery":9,"size":12.9,
 "tags":["планшет","m2","великий","малювання","стілус","mini-led","hover","2022"],
 "description":"iPad Pro 12.9\" з M2 та Mini-LED Liquid Retina XDR — найкращий для дизайнерів та художників."},

{"id":"ipad-pro-m4-11-2024","name":"iPad Pro 11\" M4 (2024)","category":"iPad","year":2024,"series":2024,"price":999,"performance":10,"camera":9,"battery":9,"size":11.0,
 "tags":["планшет","m4","oled","малювання","стілус","портативний","тонкий","новий","2024"],
 "description":"Найтонший iPad з M4 та Tandem OLED Ultra Retina XDR. Підтримує Apple Pencil Pro."},

{"id":"ipad-pro-m4-13-2024","name":"iPad Pro 13\" M4 (2024)","category":"iPad","year":2024,"series":2024,"price":1299,"performance":10,"camera":9,"battery":9,"size":13.0,
 "tags":["планшет","m4","великий","oled","малювання","стілус","тонкий","новий","2024"],
 "description":"Великий iPad Pro з M4 та Tandem OLED — найяскравіший та найтонший планшет Apple."},


# =================================
# 🗒 iPad Air SERIES (2020–2024)
# =================================

{"id":"ipad-air-4-2020","name":"iPad Air 4 (2020)","category":"iPad","year":2020,"series":2020,"price":299,"performance":6,"camera":6,"battery":7,"size":10.9,
 "tags":["планшет","a14","touch-id","usb-c","малювання","стілус","бюджет","дешевий","доступний","2020"],
 "description":"iPad Air 4 — перший Air з USB-C, Touch ID у кнопці та A14 Bionic. Доступна точка входу."},

{"id":"ipad-air-5-m1-2022","name":"iPad Air 5 M1 (2022)","category":"iPad","year":2022,"series":2022,"price":399,"performance":7,"camera":7,"battery":7,"size":10.9,
 "tags":["планшет","m1","5g","usb-c","малювання","стілус","навчання","бюджет","доступний","2022"],
 "description":"iPad Air 5 з M1 та підтримкою 5G — потужність Pro-рівня за доступною ціною."},

{"id":"ipad-air-m2-11-2024","name":"iPad Air 11\" M2 (2024)","category":"iPad","year":2024,"series":2024,"price":599,"performance":8,"camera":7,"battery":8,"size":11.0,
 "tags":["планшет","m2","навчання","малювання","портативний","стілус","новий","2024"],
 "description":"iPad Air 11\" з M2 — підтримує Apple Pencil Pro та Magic Keyboard. Ідеальний для навчання."},

{"id":"ipad-air-m2-13-2024","name":"iPad Air 13\" M2 (2024)","category":"iPad","year":2024,"series":2024,"price":799,"performance":8,"camera":7,"battery":9,"size":13.0,
 "tags":["планшет","m2","великий","навчання","малювання","робота","стілус","новий","2024"],
 "description":"Перший 13\" iPad Air з M2 — великий екран та продуктивність M2 для роботи та творчості."},


# =================================
# 🗒 iPad mini SERIES (2021–2024)
# =================================

{"id":"ipad-mini-6-2021","name":"iPad mini 6 (2021)","category":"iPad","year":2021,"series":2021,"price":249,"performance":6,"camera":6,"battery":6,"size":8.3,
 "tags":["планшет","компактний","малий","портативний","читання","ігри","usb-c","touch-id","бюджет","2021"],
 "description":"iPad mini 6 з новим дизайном без рамок, USB-C та Touch ID у кнопці. Кишеньковий планшет."},

{"id":"ipad-mini-7-2024","name":"iPad mini 7 A17 Pro (2024)","category":"iPad","year":2024,"series":2024,"price":499,"performance":8,"camera":7,"battery":7,"size":8.3,
 "tags":["планшет","компактний","малий","портативний","читання","ігри","a17 pro","ai","новий","2024"],
 "description":"iPad mini 7 з A17 Pro та Apple Intelligence — найпотужніший кишеньковий планшет Apple."},


# =================================
# 🗒 iPad (базова лінійка) (2020–2022)
# =================================

{"id":"ipad-8-2020","name":"iPad 8 (2020)","category":"iPad","year":2020,"series":2020,"price":179,"performance":4,"camera":4,"battery":6,"size":10.2,
 "tags":["планшет","найдешевший","навчання","бюджет","дешевий","доступний","школа","a12","2020"],
 "description":"iPad 8 з A12 Bionic — найдоступніший iPad для навчання, читання та базових задач."},

{"id":"ipad-9-2021","name":"iPad 9 (2021)","category":"iPad","year":2021,"series":2021,"price":199,"performance":5,"camera":5,"battery":7,"size":10.2,
 "tags":["планшет","найдешевший","навчання","бюджет","дешевий","доступний","школа","true-tone","2021"],
 "description":"iPad 9 з A13 Bionic та True Tone — відмінний вибір для школярів та студентів."},

{"id":"ipad-10-2022","name":"iPad 10 (2022)","category":"iPad","year":2022,"series":2022,"price":299,"performance":6,"camera":6,"battery":7,"size":10.9,
 "tags":["планшет","бюджет","навчання","розваги","usb-c","дешевий","доступний","a14","2022"],
 "description":"iPad 10 з USB-C, новим дизайном без рамок та A14 Bionic. Сучасний базовий iPad."},

{"id":"macbook-air-retina-2018","name":"MacBook Air 13\" Retina (2018)","category":"MacBook","year":2018,"series":2018,"price":349,"performance":4,"camera":3,"battery":6,"size":13.3,
 "tags":["ноутбук","intel","retina","легкий","портативний","бюджет","офіс","навчання","2018"],
 "description":"Тонкий MacBook Air з Retina-дисплеєм та Touch ID. Підійде для браузера, офісу й навчання за мінімальний бюджет."},

{"id":"macbook-air-retina-2019","name":"MacBook Air 13\" Retina (2019)","category":"MacBook","year":2019,"series":2019,"price":399,"performance":4,"camera":3,"battery":6,"size":13.3,
 "tags":["ноутбук","intel","retina","легкий","портативний","офіс","навчання","бюджет","2019"],
 "description":"Оновлений Air з True Tone та компактним корпусом. Хороший варіант для текстів, навчання і базової роботи."},

{"id":"macbook-air-intel-2020","name":"MacBook Air 13\" Intel (2020)","category":"MacBook","year":2020,"series":2020,"price":449,"performance":5,"camera":4,"battery":6,"size":13.3,
 "tags":["ноутбук","intel","retina","легкий","портативний","офіс","навчання","бюджет","2020"],
 "description":"Останній Intel MacBook Air до переходу на Apple Silicon. Підійде для офісу, навчання та легких задач."},

{"id":"macbook-pro-13-intel-2020","name":"MacBook Pro 13\" Intel (2020)","category":"MacBook","year":2020,"series":2020,"price":499,"performance":6,"camera":4,"battery":7,"size":13.3,
 "tags":["ноутбук","intel","pro","програмування","робота","портативний","офіс","2020"],
 "description":"Компактний MacBook Pro 13 з активним охолодженням. Краще за Air для тривалішого навантаження й розробки початкового рівня."},

{"id":"macbook-pro-13-m1-2020","name":"MacBook Pro 13\" M1 (2020)","category":"MacBook","year":2020,"series":2020,"price":699,"performance":8,"camera":5,"battery":9,"size":13.3,
 "tags":["ноутбук","m1","pro","програмування","робота","автономність","портативний","2020"],
 "description":"Перший Pro на M1 з дуже сильною автономністю та стабільною продуктивністю. Один з найкращих бюджетних MacBook для коду."},

{"id":"macbook-pro-13-m2-2022","name":"MacBook Pro 13\" M2 (2022)","category":"MacBook","year":2022,"series":2022,"price":899,"performance":8,"camera":5,"battery":9,"size":13.3,
 "tags":["ноутбук","m2","pro","програмування","робота","автономність","портативний","2022"],
 "description":"MacBook Pro 13 на M2 з довгою автономністю та активним охолодженням. Добрий компроміс між Air і великими Pro-моделями."},

{"id":"macbook-pro-15-intel-2019","name":"MacBook Pro 15\" Intel (2019)","category":"MacBook","year":2019,"series":2019,"price":649,"performance":6,"camera":4,"battery":6,"size":15.4,
 "tags":["ноутбук","intel","pro","великий екран","робота","відеомонтаж","дизайн","2019"],
 "description":"Старший 15-дюймовий Pro з великим екраном. Цікавий як недорогий варіант для дизайну, монтажу та багатовіконної роботи."},

{"id":"macbook-pro-16-intel-2019","name":"MacBook Pro 16\" Intel (2019)","category":"MacBook","year":2019,"series":2019,"price":799,"performance":7,"camera":4,"battery":7,"size":16.0,
 "tags":["ноутбук","intel","pro","великий екран","відеомонтаж","3d","робота","2019"],
 "description":"Перший 16-дюймовий MacBook Pro з Intel. Має великий дисплей і підходить для монтажу, музики та професійної роботи з медіа."},

{"id":"ipad-pro-11-2018","name":"iPad Pro 11\" (2018)","category":"iPad","year":2018,"series":2018,"price":299,"performance":5,"camera":5,"battery":6,"size":11.0,
 "tags":["планшет","pro","компактний","малювання","стілус","face-id","120гц","бюджет","2018"],
 "description":"Перший сучасний iPad Pro без кнопки Home. Досі цікавий як недорогий планшет для нотаток, малювання і мультимедіа."},

{"id":"ipad-pro-12-2018","name":"iPad Pro 12.9\" (2018)","category":"iPad","year":2018,"series":2018,"price":399,"performance":5,"camera":5,"battery":7,"size":12.9,
 "tags":["планшет","pro","великий","малювання","стілус","face-id","120гц","дизайн","2018"],
 "description":"Великий iPad Pro 12.9 з ProMotion та підтримкою Apple Pencil 2. Гарний бюджетний варіант для ескізів, PDF та дизайну."},

{"id":"ipad-air-3-2019","name":"iPad Air 3 (2019)","category":"iPad","year":2019,"series":2019,"price":229,"performance":4,"camera":4,"battery":6,"size":10.5,
 "tags":["планшет","air","навчання","бюджет","стілус","легкий","доступний","2019"],
 "description":"Легкий iPad Air для навчання, читання й базових творчих задач. Хороша точка входу в екосистему iPad."},

{"id":"ipad-mini-5-2019","name":"iPad mini 5 (2019)","category":"iPad","year":2019,"series":2019,"price":219,"performance":4,"camera":4,"battery":6,"size":7.9,
 "tags":["планшет","mini","компактний","малий","читання","подорожі","бюджет","2019"],
 "description":"Компактний iPad mini для читання, поїздок і легких задач. Зручний формат, якщо потрібен максимально невеликий планшет."},

{"id":"ipad-7-2019","name":"iPad 7 (2019)","category":"iPad","year":2019,"series":2019,"price":149,"performance":3,"camera":3,"battery":5,"size":10.2,
 "tags":["планшет","базовий","найдешевший","навчання","школа","бюджет","доступний","2019"],
 "description":"Дуже доступний базовий iPad для школи, YouTube, браузера та простих щоденних задач."},

{"id":"ipad-air-11-m4-2026","name":"iPad Air 11\" M4 (2026)","category":"iPad","year":2026,"series":2026,"price":599,"performance":9,"camera":7,"battery":8,"size":11.0,
 "tags":["планшет","m4","навчання","малювання","портативний","стілус","новий","2026"],
 "description":"Актуальний iPad Air 11 з M4, 12GB пам’яті та підтримкою Apple Pencil Pro. Один з найкращих варіантів для навчання та творчості."},

{"id":"ipad-air-13-m4-2026","name":"iPad Air 13\" M4 (2026)","category":"iPad","year":2026,"series":2026,"price":799,"performance":9,"camera":7,"battery":9,"size":13.0,
 "tags":["планшет","m4","великий","навчання","малювання","робота","стілус","новий","2026"],
 "description":"Великий актуальний iPad Air 13 з M4 для малювання, навчання, нотаток і роботи в кількох застосунках."},

]

apple_products = [_clean_product(product) for product in RAW_APPLE_PRODUCTS]
