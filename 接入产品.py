#!/usr/bin/env python3
"""接入 27 款产品：复制图片到 site/assets/photos/product/ + 生成 products.json（价格留空待确认）。"""
import os, json, shutil

ROOT = '/Users/zhangge/.openclaw/workspace-personal-assistant/柴烧网站'
SRC = os.path.join(ROOT, '产品图-新')
PROD_IMG = os.path.join(ROOT, 'site/assets/photos/product')

# 27 款：slug -> (中文名, 英文名, 分类中文, 分类英文, 特征描述)
PRODUCTS = {
    # 台灯 14 款
    'lamp-ivory-gray':     ('柴烧台灯 · 米白灰青罐形', 'Wood-Fired Lamp · Ivory-Gray', '台灯', 'Lamps', '米白与灰青双色斑驳肌理的罐形灯座'),
    'lamp-blue-gray':      ('柴烧台灯 · 深青灰罐形', 'Wood-Fired Lamp · Blue-Gray', '台灯', 'Lamps', '深青灰釉罐形灯座'),
    'lamp-red-warm':       ('柴烧台灯 · 红褐暖白罐形', 'Wood-Fired Lamp · Red-Warm', '台灯', 'Lamps', '红褐暖白斑驳罐形灯座'),
    'lamp-red-globe':      ('柴烧台灯 · 红烧圆球罐形', 'Wood-Fired Lamp · Red-Globe', '台灯', 'Lamps', '红烧色圆球罐形灯座'),
    'lamp-amber':          ('柴烧台灯 · 黄褐原木罐形', 'Wood-Fired Lamp · Amber', '台灯', 'Lamps', '黄褐原木色罐形灯座'),
    'lamp-bicolor':        ('柴烧台灯 · 黑白双色罐形', 'Wood-Fired Lamp · Bicolor', '台灯', 'Lamps', '黑白双色斜向分色罐形灯座'),
    'lamp-dark-mini':      ('柴烧台灯 · 深灰黑圆罐', 'Wood-Fired Lamp · Dark-Mini', '台灯', 'Lamps', '深灰黑小圆罐灯座'),
    'lamp-bicolor-shade':  ('柴烧台灯 · 黑白拼色', 'Wood-Fired Lamp · Bicolor-Shade', '台灯', 'Lamps', '黑白拼色灯座配米白灯罩'),
    'lamp-speckle':        ('柴烧台灯 · 斑驳黑纹', 'Wood-Fired Lamp · Speckle', '台灯', 'Lamps', '斑驳白斑黑纹灯座配黑灯罩'),
    'lamp-crater':         ('柴烧台灯 · 火山口肌理', 'Wood-Fired Lamp · Crater', '台灯', 'Lamps', '深灰火山口肌理灯座配黑灯罩'),
    'lamp-caramel':        ('柴烧台灯 · 焦糖色', 'Wood-Fired Lamp · Caramel', '台灯', 'Lamps', '焦糖黄褐灯座配黑灯罩'),
    'lamp-mottled':        ('柴烧台灯 · 米白黑褐斑驳', 'Wood-Fired Lamp · Mottled', '台灯', 'Lamps', '米白黑褐斑驳罐形灯座配黑灯罩'),
    'lamp-bicolor-sphere': ('柴烧台灯 · 黑白球形', 'Wood-Fired Lamp · Bicolor-Sphere', '台灯', 'Lamps', '黑白双色球形灯座配浅米灯罩'),
    'lamp-amber-sphere':   ('柴烧台灯 · 焦黄火痕球形', 'Wood-Fired Lamp · Amber-Sphere', '台灯', 'Lamps', '焦黄火痕球形灯座配黑灯罩'),
    # 马克杯 4 款
    'mug-ribbed-white':    ('柴烧马克杯 · 竖纹白釉', 'Wood-Fired Mug · Ribbed-White', '马克杯', 'Mugs', '竖纹压纹白釉麻点杯'),
    'mug-blue-ombre':      ('柴烧马克杯 · 蓝白渐变', 'Wood-Fired Mug · Blue-Ombre', '马克杯', 'Mugs', '蓝白渐变矮杯'),
    'mug-crackle':         ('柴烧马克杯 · 白釉黑斑开片', 'Wood-Fired Mug · Crackle', '马克杯', 'Mugs', '白釉黑斑开片杯'),
    'mug-threaded':        ('柴烧马克杯 · 螺纹堆叠', 'Wood-Fired Mug · Threaded', '马克杯', 'Mugs', '螺纹堆叠口杯'),
    # 茶具香炉 5 款
    'tea-fairness-pitcher':('柴烧公道杯 · 白釉', 'Wood-Fired Fairness Pitcher', '茶器', 'Tea Ware', '白釉公道杯，出水尖口'),
    'tea-water-basin':     ('柴烧水盂 · 白釉黑斑', 'Wood-Fired Water Basin', '茶器', 'Tea Ware', '白釉黑斑水盂'),
    'tea-rimmed-basin':    ('柴烧水盂 · 白釉折沿', 'Wood-Fired Rimmed Basin', '茶器', 'Tea Ware', '白釉折沿水盂'),
    'tea-master-cup':      ('柴烧主人杯 · 斑点束腰', 'Wood-Fired Master Cup', '茶器', 'Tea Ware', '斑点束腰主人杯'),
    'incense-amber':       ('柴烧香炉 · 黄褐釉宽沿', 'Wood-Fired Incense Burner', '茶器', 'Tea Ware', '黄褐釉宽沿香炉'),
    # 花器大罐 4 款
    'vase-ribbed-round':   ('柴烧花器 · 横纹圆腹罐', 'Wood-Fired Vase · Ribbed-Round', '花器', 'Vases', '大号横纹圆腹罐'),
    'vase-tall-neck':      ('柴烧花器 · 高颈折肩罐', 'Wood-Fired Vase · Tall-Neck', '花器', 'Vases', '高颈折肩带环饰罐'),
    'vase-light-round':    ('柴烧花器 · 浅色小口圆罐', 'Wood-Fired Vase · Light-Round', '花器', 'Vases', '浅色小口圆罐'),
    'vase-dark-fire':      ('柴烧花器 · 深色火痕圆罐', 'Wood-Fired Vase · Dark-Fire', '花器', 'Vases', '深色重火痕小口圆罐'),
}

CAT_FILTER = {'台灯': 'lamp', '马克杯': 'mug', '茶器': 'tea', '花器': 'vase'}

# 1. 复制图片到 site/assets/photos/product/{slug}/
if os.path.exists(PROD_IMG):
    shutil.rmtree(PROD_IMG)
os.makedirs(PROD_IMG, exist_ok=True)

# 分类目录映射：产品分类名 -> 归档时实际目录名
SRC_CAT = {'台灯': '台灯', '马克杯': '马克杯', '茶器': '茶具香炉', '花器': '花器大罐'}

products = []
for slug, (name_zh, name_en, cat_zh, cat_en, desc) in PRODUCTS.items():
    src_dir = os.path.join(SRC, SRC_CAT[cat_zh], slug)
    dst_dir = os.path.join(PROD_IMG, slug)
    os.makedirs(dst_dir, exist_ok=True)
    images = []
    if os.path.isdir(src_dir):
        for f in sorted(os.listdir(src_dir)):
            if f.endswith('.jpg'):
                shutil.copy(os.path.join(src_dir, f), os.path.join(dst_dir, f))
                images.append(f'{slug}/{f}')
    products.append({
        'product_id': slug,
        'slug': slug,
        'product_name': name_zh,
        'product_name_en': name_en,
        'category': cat_zh,
        'category_en': cat_en,
        'filter': CAT_FILTER[cat_zh],
        'description': f'柴烧{cat_zh}，{desc}。木火落灰成釉，每一件釉色与火痕独一无二，孤品仅此一件。',
        'description_en': f'A wood-fired {cat_en.lower().rstrip("s")} — {desc}. Ash-glazed by wood fire, each piece is one of a kind.',
        'materials': '待确认',
        'dimensions': '待确认',
        'weight': '待确认',
        'capacity': '待确认',
        'firing_method': '待确认',
        'origin': '待确认',
        'artist_or_maker': '待确认',
        'price': '',
        'currency': 'EUR',
        'availability': '1（孤品，售出即无）',
        'variants': [],
        'images': images,
        'image_alt': f'{name_zh}，柴烧{cat_zh}',
        'shipping_information': '待确认',
        'care_information': '待确认',
        'seo_title': f'{name_en} | QINGYUAN Wood-Fired Ceramics',
        'meta_description': f'{name_en} — a one-of-a-kind wood-fired {cat_en.lower().rstrip("s")} by QINGYUAN.',
        'primary_keyword': f'wood fired {cat_en.lower().rstrip("s")}',
        'secondary_keywords': ['wood fired ceramics', 'wabi-sabi', 'handmade'],
        'locale': 'en',
        'canonical_url': f'/en/shop/{slug}',
        'related_products': [],
    })
    print(f'✅ {cat_zh}/{slug}: {len(images)} 图')

# 2. 写 products.json
out = os.path.join(ROOT, 'data/products.json')
json.dump({'products': products}, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print(f'\nproducts.json 已生成（{len(products)} 款）')
