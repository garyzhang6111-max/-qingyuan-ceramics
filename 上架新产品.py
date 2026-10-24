#!/usr/bin/env python3
"""上架新文件包的产品：归档图片 + 写入 products.json + 生成数据。

已识别的单件产品（53/71 张，剩余 15 张待识别）。
分类新增：茶盘 plate / 香炉 incense / 摆件 sculpture。
命名临时用「器型+特征」，后续读 PDF 目录名称再统一替换。
"""
import json, os, shutil
from PIL import Image

ROOT = '/Users/zhangge/.openclaw/workspace-personal-assistant/柴烧网站'
SRC = os.path.join(ROOT, '上架图源-新')          # 原 PNG
PROD_IMG = os.path.join(ROOT, 'site/assets/photos/product')
DATA_PATH = os.path.join(ROOT, 'data/products.json')

TARGET_W, TARGET_H = 1200, 1600  # 3:4
RATIO = TARGET_W / TARGET_H

# 新产品定义： (时间戳, slug, filter, category_zh, category_en, name_zh, name_en, desc_en)
# 时间戳对应 WPS图片20261024{t}.png
PRODUCTS = [
    # === 台灯（守光灯具，球形为主）===
    ('180912', 'lamp-sphere-ivory',    'lamp', '守光灯具', 'Light Keeper', '守光 · 球形 · 米白',     'Light Keeper · Sphere · Ivory',      'A wood-fired lamp on an ivory sphere with a white shade.'),
    ('180919', 'lamp-sphere-rock',     'lamp', '守光灯具', 'Light Keeper', '守光 · 球形 · 黑灰岩',   'Light Keeper · Sphere · Rock',       'A wood-fired lamp on a dark rock-textured sphere with a black shade.'),
    ('180926', 'lamp-sphere-yinyang',  'lamp', '守光灯具', 'Light Keeper', '守光 · 球形 · 阴阳双色', 'Light Keeper · Sphere · Yin-Yang',   'A wood-fired lamp on a two-tone sphere, half dark, half pale, with a warm shade.'),
    ('180934', 'lamp-sphere-amber',    'lamp', '守光灯具', 'Light Keeper', '守光 · 球形 · 焦黄',     'Light Keeper · Sphere · Amber',      'A wood-fired lamp on an amber sphere with a black shade.'),
    ('180939', 'lamp-jar-speckle',     'lamp', '守光灯具', 'Light Keeper', '守光 · 罐形 · 黑白斑驳', 'Light Keeper · Jar · Speckle',       'A wood-fired lamp on a black-and-white mottled jar with a black cone shade.'),
    ('180947', 'lamp-sphere-ink',      'lamp', '守光灯具', 'Light Keeper', '守光 · 球形 · 水墨',     'Light Keeper · Sphere · Ink',        'A wood-fired lamp on an ink-wash black-and-white sphere with a black shade.'),
    ('180955', 'lamp-jar-graytea',     'lamp', '守光灯具', 'Light Keeper', '守光 · 罐形 · 灰白茶点', 'Light Keeper · Jar · Grey-Tea',      'A wood-fired lamp on a grey-white tea-speckled jar with a dark grey shade.'),
    ('181001', 'lamp-jar-darkbrown',   'lamp', '守光灯具', 'Light Keeper', '守光 · 罐形 · 深黑褐',   'Light Keeper · Jar · Dark-Brown',    'A wood-fired lamp on a dark brown jar with a black shade.'),
    ('181007', 'lamp-sphere-yinyangcut','lamp', '守光灯具', 'Light Keeper', '守光 · 球形 · 阴阳斜切', 'Light Keeper · Sphere · Yin-Yang Cut','A wood-fired lamp on a diagonally split two-tone sphere with a dark grey shade.'),
    ('181013', 'lamp-jar-warmgray',    'lamp', '守光灯具', 'Light Keeper', '守光 · 罐形 · 暖灰茶点', 'Light Keeper · Jar · Warm-Grey',     'A wood-fired lamp on a warm grey tea-speckled jar with a dark grey shade.'),
    ('181021', 'lamp-jar-grayblue',    'lamp', '守光灯具', 'Light Keeper', '守光 · 罐形 · 灰蓝岩',   'Light Keeper · Jar · Grey-Blue',     'A wood-fired lamp on a grey-blue sedimentary jar with a dark grey shade.'),
    ('181028', 'lamp-sphere-vermillion','lamp', '守光灯具', 'Light Keeper', '守光 · 球形 · 朱红岩',   'Light Keeper · Sphere · Vermillion', 'A wood-fired lamp on a vermillion volcanic sphere with a black shade.'),
    ('181152', 'lamp-sphere-creamamber','lamp', '守光灯具', 'Light Keeper', '守光 · 球形 · 米白焦黄', 'Light Keeper · Sphere · Cream-Amber','A wood-fired lamp on a cream-and-amber sphere with a white shade.'),

    # === 马克杯 ===
    ('180752', 'mug-chrysanthemum',  'mug', '马克杯', 'Mugs', '马克杯 · 菊割纹',    'Mug · Chrysanthemum Cut',   'A mug with chrysanthemum-style vertical cuts and a white glaze.'),
    ('180757', 'mug-amberfire',      'mug', '马克杯', 'Mugs', '马克杯 · 黄褐火痕',  'Mug · Amber Fire',           'A low mug with amber fire marks and ash deposits.'),
    ('180802', 'mug-crackle-white',  'mug', '马克杯', 'Mugs', '马克杯 · 米白开片',  'Mug · Crackle White',        'A white crackle-glazed mug with fine speckles.'),
    ('180810', 'mug-lava',           'mug', '马克杯', 'Mugs', '马克杯 · 黑褐熔岩',  'Mug · Lava',                 'A mug with a dark lava-textured exterior.'),
    ('180817', 'mug-throwlines',     'mug', '马克杯', 'Mugs', '马克杯 · 拉坯纹',    'Mug · Throwing Lines',       'A mug with visible throwing lines and a rust-red rim.'),
    ('180826', 'mug-oildrop-olive',  'mug', '马克杯', 'Mugs', '马克杯 · 橄榄绿油滴', 'Mug · Olive Oil-Drop',      'A mug with an olive-green oil-spot crystal glaze.'),
    ('180831', 'mug-blue-ink',       'mug', '马克杯', 'Mugs', '马克杯 · 蓝彩水墨',  'Mug · Blue Ink',             'A mug with ink-wash blue brushwork over a white glaze.'),
    ('180838', 'mug-red-iron',       'mug', '马克杯', 'Mugs', '马克杯 · 红彩铁红',  'Mug · Red Iron',             'A mug with red iron brushwork and dark speckles.'),

    # === 茶器 ===
    ('180650', 'tea-saucer',            'tea', '茶器', 'Tea Ware', '茶托 · 米白',        'Tea Saucer · White',         'A white crackle-glazed tea saucer with a spiral well.'),
    ('180657', 'tea-cup-pinkwhite',     'tea', '茶器', 'Tea Ware', '茶杯 · 淡粉白',      'Tea Cup · Pink-White',       'A small cup with a pale pink-white glaze and fire blush.'),
    ('180702', 'tea-cup-crackle',       'tea', '茶器', 'Tea Ware', '品茗杯 · 米白开片',  'Tea Cup · Crackle',          'A crackle-glazed tasting cup with black iron spots.'),
    ('180708', 'fairness-cup-pointed',  'tea', '茶器', 'Tea Ware', '公道杯 · 尖嘴',      'Fairness Cup · Pointed Spout','A matte white fairness cup with a sharp pouring spout.'),
    ('180715', 'waste-bowl-round',      'tea', '茶器', 'Tea Ware', '水盂 · 鼓腹',        'Waste-Water Bowl · Round',   'A round-bellied waste-water bowl in thick white glaze.'),
    ('180721', 'waste-bowl-speckle',    'tea', '茶器', 'Tea Ware', '水盂 · 灰白黑斑',    'Waste-Water Bowl · Speckle', 'A grey-white waste-water bowl with black iron spots.'),
    ('180726', 'fairness-cup-eagle',    'tea', '茶器', 'Tea Ware', '公道杯 · 直筒鹰嘴',  'Fairness Cup · Eagle Spout', 'A straight-sided fairness cup with an eagle-beak spout.'),
    ('180735', 'waste-bowl-amber',      'tea', '茶器', 'Tea Ware', '水盂 · 暖黄',        'Waste-Water Bowl · Amber',   'A warm yellow waste-water bowl with fine crackle.'),
    ('180742', 'tea-cup-pinkgray',      'tea', '茶器', 'Tea Ware', '品茗杯 · 淡粉灰',    'Tea Cup · Pink-Grey',        'A tasting cup in pale pink-grey crackle glaze.'),
    ('180747', 'tea-cup-fire',          'tea', '茶器', 'Tea Ware', '品茗杯 · 棕褐火痕',  'Tea Cup · Fire Marks',       'A tasting cup with heavy brown fire marks against white glaze.'),
    ('181223', 'waste-bowl-gray',       'tea', '茶器', 'Tea Ware', '水盂 · 浅灰',        'Waste-Water Bowl · Grey',    'A pale grey waste-water bowl with fine crackle.'),
    ('181229', 'waste-bowl-olive',      'tea', '茶器', 'Tea Ware', '水盂 · 茶叶末',      'Waste-Water Bowl · Olive',   'A tea-dust olive waste-water bowl with flowing glaze.'),
    ('181234', 'master-cup-cream',      'tea', '茶器', 'Tea Ware', '主人杯 · 米白粉橙',  'Master Cup · Cream',         'A master cup in cream glaze with pink-orange fire blush.'),
    ('181240', 'master-cup-olive',      'tea', '茶器', 'Tea Ware', '主人杯 · 黄绿渐变',  'Master Cup · Olive',         'A master cup with a yellow-green gradient glaze.'),

    # === 花器 ===
    ('180844', 'vase-bicolor-round', 'vase', '花器', 'Vases', '花器 · 米白红褐',   'Vase · Bicolor',        'A low round vase in white and red-brown.'),
    ('180851', 'vase-rock-sphere',   'vase', '花器', 'Vases', '花器 · 黑褐岩球',   'Vase · Rock Sphere',    'A dark brown rock-textured spherical vase.'),
    ('180857', 'vase-gray-ring',     'vase', '花器', 'Vases', '花器 · 灰白环纹',   'Vase · Grey Ring',      'A large grey-white sphere with throwing rings.'),
    ('180907', 'vase-gray-grain',    'vase', '花器', 'Vases', '花器 · 灰白颗粒',   'Vase · Grey Grain',     'A grey-white grainy vase with a wide shoulder.'),
    ('181116', 'vase-woven-rock',    'vase', '花器', 'Vases', '花器 · 编织岩盆',   'Vase · Woven Rock',     'A low woven rock-textured planter.'),
    ('181121', 'vase-step-neck',     'vase', '花器', 'Vases', '花器 · 双层阶梯颈', 'Vase · Step Neck',      'A wide jar with a two-step neck.'),
    ('181126', 'vase-trumpet',       'vase', '花器', 'Vases', '花器 · 喇叭口',     'Vase · Trumpet',        'A trumpet-mouthed vase with a full belly.'),
    ('181135', 'vase-tall-carved',   'vase', '花器', 'Vases', '花器 · 长颈斜刻',   'Vase · Tall Carved',    'A tall-necked bottle with diagonal carving.'),
    ('181141', 'vase-tall-sesame',   'vase', '花器', 'Vases', '花器 · 长颈芝麻点', 'Vase · Tall Sesame',    'A tall-necked bottle with sesame-like specks.'),
    ('181147', 'vase-moon-jar',      'vase', '花器', 'Vases', '花器 · 月亮罐',     'Vase · Moon Jar',       'A moon jar with rust-red and white halves.'),

    # === 茶盘（新品类）===
    ('181033', 'plate-crackle-x',   'plate', '茶盘', 'Tea Trays', '茶盘 · 冰裂 X 纹',   'Tea Tray · Crackle X',   'A rectangular tea tray with crackle glaze and X-pattern grooves.'),
    ('181038', 'plate-fire-crackle','plate', '茶盘', 'Tea Trays', '茶盘 · 黄褐火痕',    'Tea Tray · Fire Crackle','A rectangular tea tray with amber crackle and fire marks.'),
    ('181053', 'plate-checker',     'plate', '茶盘', 'Tea Trays', '茶盘 · 四格棋盘',    'Tea Tray · Checker',     'A four-panel tea tray alternating black-brown and white glaze.'),
    ('181100', 'plate-grid-white',  'plate', '茶盘', 'Tea Trays', '茶盘 · 四格白釉',    'Tea Tray · Grid White',  'A four-panel tea tray in crackle white glaze.'),
    ('181107', 'plate-rectangle',   'plate', '茶盘', 'Tea Trays', '茶盘 · 长方熏黑',    'Tea Tray · Rectangle',   'A rounded rectangle tea tray with smoked black edges.'),

    # === 香炉（新品类）===
    ('181200', 'incense-tall-white',   'incense', '香炉', 'Incense Burners', '香炉 · 高足宽沿',   'Incense Burner · Tall White',  'A tall white incense burner with a wide rim.'),
    ('181206', 'incense-tall-brown',   'incense', '香炉', 'Incense Burners', '香炉 · 高足深茶褐', 'Incense Burner · Tall Brown',  'A tall dark tea-brown incense burner.'),
    ('181212', 'incense-tray-long',    'incense', '香炉', 'Incense Burners', '香炉 · 长条香托',   'Incense Tray · Long',          'A long incense tray in white crackle glaze.'),
    ('181218', 'incense-shallow-dish', 'incense', '香炉', 'Incense Burners', '香炉 · 高足浅盘',   'Incense Burner · Shallow Dish','A shallow-dish incense burner on a high foot.'),
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

# 读取现有数据
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
    # 归档图片
    outdir = os.path.join(PROD_IMG, slug)
    os.makedirs(outdir, exist_ok=True)
    out = os.path.join(outdir, f'{slug}-1.jpg')
    im = Image.open(src).convert('RGB')
    im = crop_to_ratio(im)
    im.save(out, quality=90)
    archived += 1

    # 产品记录
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
        'description': '',  # 中文描述待 PDF 名称确认后补
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
json.dump(data, open(DATA_PATH, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)

print(f'归档图片 {archived} 张')
print(f'新增产品 {len(new_products)} 款')
if missing:
    print(f'缺失源图 {len(missing)}: {missing}')
