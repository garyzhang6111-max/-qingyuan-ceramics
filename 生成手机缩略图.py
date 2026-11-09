#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成移动端缩略图：assets/photos/mobile/{slug}-m.jpg
卡片显示 ~180px 宽（2 列布局），2x retina → 360px 宽；比例 4:4.6 → 360x414。
只生成第一张图（网格卡用），详情页仍用原图。"""
import json, os
from PIL import Image

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(ROOT, 'site')
DATA = json.load(open(os.path.join(ROOT, 'data', 'products.json'), encoding='utf-8'))
OUT = os.path.join(SITE, 'assets', 'photos', 'mobile')
os.makedirs(OUT, exist_ok=True)

TW, TH = 360, 414  # 4 : 4.6

done = skipped = failed = 0
for p in DATA['products']:
    slug = p['slug']
    out_path = os.path.join(OUT, f'{slug}-m.jpg')
    if os.path.exists(out_path):
        skipped += 1
        continue
    src_rel = p['images'][0] if p['images'] else None
    if not src_rel:
        failed += 1
        continue
    src = os.path.join(SITE, 'assets', 'photos', 'product', src_rel.replace('/', os.sep))
    if not os.path.exists(src):
        print('缺源图:', src_rel)
        failed += 1
        continue
    try:
        im = Image.open(src).convert('RGB')
        # 居中裁到目标比例再缩放
        w, h = im.size
        target = TW / TH
        cur = w / h
        if cur > target:
            nw = int(h * target)
            x0 = (w - nw) // 2
            im = im.crop((x0, 0, x0 + nw, h))
        else:
            nh = int(w / target)
            y0 = (h - nh) // 2
            im = im.crop((0, y0, w, y0 + nh))
        im = im.resize((TW, TH), Image.LANCZOS)
        im.save(out_path, 'JPEG', quality=72, optimize=True)
        done += 1
    except Exception as e:
        print('失败:', slug, e)
        failed += 1

print(f'完成 {done} 张，跳过(已存在) {skipped} 张，失败 {failed} 张')
