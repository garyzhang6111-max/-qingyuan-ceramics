#!/usr/bin/env python3
"""台灯 → 守光灯具系列，产品名加细分（罐形/球形）。"""
import json

DATA_PATH = '/Users/zhangge/.openclaw/workspace-personal-assistant/柴烧网站/data/products.json'
data = json.load(open(DATA_PATH))

# 特征部分（去掉原有"柴烧台灯 · "前缀，保留特征）
FEAT = {
    'lamp-ivory-gray':     ('米白灰青', 'Ivory-Gray'),
    'lamp-blue-gray':      ('深青灰', 'Blue-Gray'),
    'lamp-red-warm':       ('红褐暖白', 'Red-Warm'),
    'lamp-red-globe':      ('红烧圆球', 'Red-Globe'),
    'lamp-amber':          ('黄褐原木', 'Amber'),
    'lamp-bicolor':        ('黑白双色', 'Bicolor'),
    'lamp-dark-mini':      ('深灰黑', 'Dark-Mini'),
    'lamp-bicolor-shade':  ('黑白拼色', 'Bicolor-Shade'),
    'lamp-speckle':        ('斑驳黑纹', 'Speckle'),
    'lamp-crater':         ('火山口肌理', 'Crater'),
    'lamp-caramel':        ('焦糖色', 'Caramel'),
    'lamp-mottled':        ('米白黑褐', 'Mottled'),
    'lamp-bicolor-sphere': ('黑白球形', 'Bicolor-Sphere'),
    'lamp-amber-sphere':   ('焦黄火痕', 'Amber-Sphere'),
}

n = 0
for p in data['products']:
    if p['filter'] != 'lamp':
        continue
    sc = p.get('subcategory', '罐形')       # 罐形/球形
    sc_en = p.get('subcategory_en', 'Jar')
    feat_zh, feat_en = FEAT.get(p['slug'], ('', ''))
    p['category'] = '守光灯具'
    p['category_en'] = 'Light Keeper'
    p['product_name'] = f'守光 · {sc} · {feat_zh}'
    p['product_name_en'] = f'Light Keeper · {sc_en} · {feat_en}'
    p['seo_title'] = f"{p['product_name_en']} | QINGYUAN Wood-Fired Ceramics"
    p['meta_description'] = f"{p['product_name_en']} — a one-of-a-kind wood-fired lamp by QINGYUAN."
    n += 1

json.dump(data, open(DATA_PATH, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print(f'已更新 {n} 款台灯 → 守光灯具系列（含罐形/球形细分）')
