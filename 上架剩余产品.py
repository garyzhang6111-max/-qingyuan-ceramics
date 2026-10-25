#!/usr/bin/env python3
"""上架剩余 14 张产品图：归档图片 + 新增 products.json + 茶器小件靠前大件靠后排序。

盖碗归茶器（用户明确要求）。摆件新增 sculpture 分类。
"""
import json, os
from PIL import Image

ROOT = '/Users/zhangge/.openclaw/workspace-personal-assistant/柴烧网站'
SRC = os.path.join(ROOT, '上架图源-新')          # 原 PNG
PROD_IMG = os.path.join(ROOT, 'site/assets/photos/product')
DATA_PATH = os.path.join(ROOT, 'data/products.json')

TARGET_W, TARGET_H = 1200, 1600  # 3:4
RATIO = TARGET_W / TARGET_H

# 新产品定义： (时间戳, slug, filter, 分类zh, 分类en, 名zh, 名en, 描述en)
# 时间戳对应 WPS图片20261024{t}.png
PRODUCTS = [
    # === 茶器·小件（主人杯/抹茶碗/品茗杯/盖碗/茶托，靠前）===
    ('181247', 'tea-master-cup-ash-orange', 'tea', '茶器', 'Tea Ware', '主人杯 · 灰白橙晕', 'Master Cup · Ash-Orange', 'A master cup with soft orange-red ash blush over a grey-white glaze, its high foot exposing the raw red clay.'),
    ('181253', 'tea-master-cup-brown', 'tea', '茶器', 'Tea Ware', '主人杯 · 深褐焦棕', 'Master Cup · Brown', 'A master cup in a deep amber and burnt-brown gradient, the glaze pooling at the rim, the foot showing the red clay body.'),
    ('181300', 'tea-matcha-bowl-crackle', 'tea', '茶器', 'Tea Ware', '抹茶碗 · 白灰冰裂', 'Matcha Bowl · Crackle', 'A matcha bowl in a white-grey crackle glaze with a coarse, tactile surface and a gently bulging straight mouth.'),
    ('181305', 'tea-matcha-bowl-amber', 'tea', '茶器', 'Tea Ware', '抹茶碗 · 黄褐结晶', 'Matcha Bowl · Amber', 'A low, sturdy matcha bowl with a flowing amber glaze flecked with dark crystals.'),
    ('181311', 'tea-tasting-cup-iron', 'tea', '茶器', 'Tea Ware', '品茗杯 · 乳白铁斑', 'Tasting Cup · Iron Speckle', 'A round tasting cup in milky crackle glaze with fine iron speckles, darkening to amber ash near the base.'),
    ('181317', 'tea-gaiwan-white', 'tea', '茶器', 'Tea Ware', '盖碗 · 米白金褐', 'Gaiwan · White', 'A gaiwan in milky-white fading to pale grey, with a golden-brown glaze ring on the rim and knob.'),
    ('181322', 'tea-gaiwan-brown', 'tea', '茶器', 'Tea Ware', '盖碗 · 黑褐古铜', 'Gaiwan · Brown', 'A gaiwan in deep black-brown and bronze glaze with visible throwing rings and a russet knob.'),
    ('181328', 'tea-gaiwan-crystal', 'tea', '茶器', 'Tea Ware', '盖碗 · 紫红结晶', 'Gaiwan · Crystal', 'A gaiwan with a white body and flowing brown mottling, the lid rich in purple-red crystal spots.'),
    # === 茶器·大件（公道杯，靠后）===
    ('181419', 'fairness-cup-cream', 'tea', '茶器', 'Tea Ware', '公道杯 · 米白鹰嘴', 'Fairness Cup · Cream', 'A fairness cup in warm milky-white with a blush of orange, an eagle-beak spout and a wide high foot.'),
    # === 花器 ===
    ('181333', 'vase-water-jar', 'vase', '花器', 'Vases', '水罐 · 浅褐黑斑', 'Vase · Water Jar', 'A water jar in pale brown with black speckles and red-brown fire marks, a short neck and full round belly on a foot ring.'),
    ('181340', 'vase-olive-crackle', 'vase', '花器', 'Vases', '罐缸 · 橄榄绿冰裂', 'Vase · Olive Crackle', 'A jar in olive-yellow-green glaze, fully crackled with a glossy surface, a short lip neck and full shoulder.'),
    ('181415', 'vase-white-crackle', 'vase', '花器', 'Vases', '花器 · 米白志野', 'Vase · White Crackle', 'A vase in thick milky-white glaze with bold shino-like crackle, the foot left raw in iron-red clay.'),
    # === 摆件（新分类）===
    ('181435', 'sculpture-pyramid', 'sculpture', '摆件', 'Sculptures', '摆件 · 金字塔', 'Sculpture · Pyramid', 'A pyramid-shaped sculpture in red-brown and milky-white, with drawn-line texture and an irregular opening.'),
    ('181441', 'sculpture-sphere', 'sculpture', '摆件', 'Sculptures', '摆件 · 球形', 'Sculpture · Sphere', 'A spherical sculpture in grey ash and burnt amber, with spiral-carved, rock-like texture.'),
]


def crop_to_ratio(im):
    w, h = im.size
    cur = w / h
    if abs(cur - RATIO) < 0.01:
        return im.resize((TARGET_W, TARGET_H), Image.LANCZOS)
    if cur > RATIO:
        new_w = int(h * RATIO)
        left = (w - new_w) // 2
        im = im.crop((left, 0, left + new_w, h))
    else:
        new_h = int(w / RATIO)
        top = (h - new_h) // 2
        im = im.crop((0, top, w, top + new_h))
    return im.resize((TARGET_W, TARGET_H), Image.LANCZOS)


data = json.load(open(DATA_PATH))
existing_slugs = {p['slug'] for p in data['products']}

new_products = []
archived = 0
missing = []

for ts, slug, filt, cat_zh, cat_en, name_zh, name_en, desc_en in PRODUCTS:
    src = os.path.join(SRC, f'WPS图片20261024{ts}.png')
    if not os.path.exists(src):
        missing.append(ts)
        continue
    outdir = os.path.join(PROD_IMG, slug)
    os.makedirs(outdir, exist_ok=True)
    out = os.path.join(outdir, f'{slug}-1.jpg')
    im = Image.open(src).convert('RGB')
    im = crop_to_ratio(im)
    im.save(out, quality=90)
    archived += 1

    p = {
        'product_id': slug,
        'slug': slug,
        'filter': filt,
        'category': cat_zh,
        'category_en': cat_en,
        'subcategory': '',
        'subcategory_en': '',
        'product_name': name_zh,
        'product_name_en': name_en,
        'price': '',
        'currency': 'EUR',
        'description': '',
        'description_en': desc_en,
        'materials': '待确认',
        'dimensions': '待确认',
        'capacity': '待确认',
        'weight': '待确认',
        'firing_method': '待确认',
        'origin': '待确认',
        'artist_or_maker': '待确认',
        'availability': 'in_stock',
        'variants': [],
        'images': [f'{slug}/{slug}-1.jpg'],
        'image_alt': name_zh,
        'shipping_information': '待确认',
        'care_information': '待确认',
        'seo_title': f'{name_en} | QINGYUAN Wood-Fired Ceramics',
        'meta_description': desc_en,
        'primary_keyword': name_en,
        'secondary_keywords': [],
        'locale': 'en',
        'canonical_url': f'https://www.qingyuan-ceramics.com/{slug}.html',
        'related_products': [],
    }
    if slug in existing_slugs:
        print(f'⚠️ slug 冲突（跳过）: {slug}')
        continue
    new_products.append(p)

data['products'].extend(new_products)

# ============ 茶器排序：小件靠前，大件靠后 ============
# 小件（杯类）顺序 → 大件（公道杯/水盂）顺序
tea_order = [
    # 主人杯
    'tea-master-cup', 'master-cup-cream', 'master-cup-olive',
    'tea-master-cup-ash-orange', 'tea-master-cup-brown',
    # 抹茶碗
    'tea-matcha-bowl-crackle', 'tea-matcha-bowl-amber',
    # 品茗杯
    'tea-cup-crackle', 'tea-cup-pinkgray', 'tea-cup-fire', 'tea-tasting-cup-iron',
    # 茶杯
    'tea-cup-pinkwhite',
    # 盖碗
    'tea-gaiwan-white', 'tea-gaiwan-brown', 'tea-gaiwan-crystal',
    # 茶托
    'tea-saucer',
    # 公道杯（大件）
    'tea-fairness-cup', 'fairness-cup-pointed', 'fairness-cup-eagle', 'fairness-cup-cream',
    # 水盂（大件）
    'tea-waste-water-bowl', 'tea-flared-rim-bowl',
    'waste-bowl-round', 'waste-bowl-speckle', 'waste-bowl-amber',
    'waste-bowl-gray', 'waste-bowl-olive',
]

# 拆分：茶器产品和其余产品
tea_products = [p for p in data['products'] if p['filter'] == 'tea']
other_products = [p for p in data['products'] if p['filter'] != 'tea']

# 按 tea_order 排序（不在列表里的茶器排在最后，保持原序）
tea_by_slug = {p['slug']: p for p in tea_products}
ordered_tea = []
seen = set()
for slug in tea_order:
    if slug in tea_by_slug and slug not in seen:
        ordered_tea.append(tea_by_slug[slug])
        seen.add(slug)
# 追加任何遗漏的茶器
for p in tea_products:
    if p['slug'] not in seen:
        ordered_tea.append(p)

# 重建整体顺序：保持其他分类原有相对顺序，茶器按新顺序插回茶器原位置
# 简化：其他分类保持原序，茶器整体放在 tea 首次出现的位置
result = []
tea_inserted = False
for p in data['products']:
    if p['filter'] == 'tea':
        if not tea_inserted:
            result.extend(ordered_tea)
            tea_inserted = True
    else:
        result.append(p)

data['products'] = result
json.dump(data, open(DATA_PATH, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

print(f'归档图片 {archived} 张')
print(f'新增产品 {len(new_products)} 款')
if missing:
    print(f'缺失源图 {len(missing)}: {missing}')

# 验证茶器排序
tea = [p['slug'] for p in data['products'] if p['filter'] == 'tea']
print(f'\n茶器共 {len(tea)} 款，新顺序：')
for i, s in enumerate(tea):
    print(f'  {i+1}. {s}')
