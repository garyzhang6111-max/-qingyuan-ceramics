#!/usr/bin/env python3
"""台灯细分：按底座造型分「罐形 Jar」/「球形 Sphere」，写入 products.json 细分字段。"""
import json

DATA_PATH = '/Users/zhangge/.openclaw/workspace-personal-assistant/柴烧网站/data/products.json'
data = json.load(open(DATA_PATH))

# 台灯细分映射（按底座造型）
# 罐形 jar（圆腹罐形底座，含小圆罐）
JAR = [
    'lamp-ivory-gray',   # 米白灰青双色斑驳罐形
    'lamp-blue-gray',    # 深青灰釉罐形
    'lamp-red-warm',     # 红褐暖白罐形
    'lamp-amber',        # 黄褐原木罐形
    'lamp-bicolor',      # 黑白双色斜向罐形
    'lamp-bicolor-shade',# 黑白拼色罐形
    'lamp-speckle',      # 斑驳白斑黑纹罐形
    'lamp-caramel',      # 焦糖黄褐罐形
    'lamp-mottled',      # 米白黑褐斑驳罐形
    'lamp-dark-mini',    # 深灰黑小圆罐
]
# 球形 sphere（正球体/卵石体底座，含火山口肌理球）
SPHERE = [
    'lamp-red-globe',     # 红烧圆球
    'lamp-bicolor-sphere',# 黑白双色球形
    'lamp-amber-sphere',  # 焦黄火痕球形
    'lamp-crater',        # 火山口肌理球形
]

n = 0
for p in data['products']:
    if p['slug'] in JAR:
        p['subcategory'] = '罐形'
        p['subcategory_en'] = 'Jar'
        n += 1
    elif p['slug'] in SPHERE:
        p['subcategory'] = '球形'
        p['subcategory_en'] = 'Sphere'
        n += 1

json.dump(data, open(DATA_PATH, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print(f'已给 {n} 款台灯写入细分字段')
print(f'  罐形 Jar: {len(JAR)} 款')
print(f'  球形 Sphere: {len(SPHERE)} 款')
