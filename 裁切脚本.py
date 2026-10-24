#!/usr/bin/env python3
# 批量裁成 1:1 正方形（中心裁切，1200x1200）
from PIL import Image
import os, glob

SRC = '/Users/zhangge/.openclaw/workspace-personal-assistant/柴烧网站/照片分类-web/产品图'
DST = '/Users/zhangge/.openclaw/workspace-personal-assistant/柴烧网站/产品图-11'
os.makedirs(DST, exist_ok=True)

SIZE = 1200
total = 0
for root, dirs, files in os.walk(SRC):
    for f in files:
        if not f.lower().endswith('.jpg'):
            continue
        p = os.path.join(root, f)
        rel = os.path.relpath(p, SRC)
        out = os.path.join(DST, rel)
        os.makedirs(os.path.dirname(out), exist_ok=True)
        try:
            im = Image.open(p).convert('RGB')
            w, h = im.size
            s = min(w, h)
            left = (w - s) // 2
            top = (h - s) // 2
            im = im.crop((left, top, left + s, top + s))
            im = im.resize((SIZE, SIZE), Image.LANCZOS)
            im.save(out, 'JPEG', quality=85, optimize=True)
            total += 1
        except Exception as e:
            print(f'FAIL {f}: {e}')
print(f'裁切完成 {total} 张 -> {DST}')
