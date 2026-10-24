#!/usr/bin/env python3
"""统一详情页照片为 3:4 竖构图(1200x1600) + 填充 related_products 内链。"""
import json, os
from PIL import Image

ROOT = '/Users/zhangge/.openclaw/workspace-personal-assistant/柴烧网站'
PROD_IMG = os.path.join(ROOT, 'site/assets/photos/product')
DATA_PATH = os.path.join(ROOT, 'data/products.json')

TARGET_W, TARGET_H = 1200, 1600  # 3:4
RATIO = TARGET_W / TARGET_H      # 0.75

data = json.load(open(DATA_PATH))
products = data['products']

# 1. 统一裁切照片
total = 0
for p in products:
    for img in p['images']:
        fp = os.path.join(PROD_IMG, img)
        if not os.path.exists(fp):
            print(f'⚠️ 缺失: {img}')
            continue
        im = Image.open(fp).convert('RGB')
        w, h = im.size
        cur = w / h
        if abs(cur - RATIO) < 0.005 and w == TARGET_W and h == TARGET_H:
            continue  # 已是目标，跳过
        if cur > RATIO:
            # 更宽 → 裁宽度
            new_w = int(h * RATIO)
            left = (w - new_w) // 2
            im = im.crop((left, 0, left + new_w, h))
        else:
            # 更窄/更竖长 → 裁高度
            new_h = int(w / RATIO)
            top = (h - new_h) // 2
            im = im.crop((0, top, w, top + new_h))
        im = im.resize((TARGET_W, TARGET_H), Image.LANCZOS)
        im.save(fp, quality=90)
        total += 1
print(f'统一裁切 {total} 张照片为 {TARGET_W}x{TARGET_H}')

# 2. 填充 related_products：同分类的其他产品，取前 2 个
by_cat = {}
for p in products:
    by_cat.setdefault(p['filter'], []).append(p['slug'])

changed = 0
for p in products:
    siblings = [s for s in by_cat[p['filter']] if s != p['slug']]
    # 取前 2 个（循环取，确保至少 1 个）
    rel = siblings[:2] if len(siblings) >= 2 else siblings
    if p.get('related_products') != rel:
        p['related_products'] = rel
        changed += 1

json.dump(data, open(DATA_PATH, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print(f'填充 related_products：{changed} 款')
