#!/usr/bin/env python3
"""方案A：首页滚动图 + hero 图压缩优化。
滚动图：4:5 居中裁切 → 640x800，JPEG 质量 72
hero 图：保持比例，最长边 1600，JPEG 质量 70
只生成新文件到 assets/photos/featured/，不改详情页原图。
"""
import os
from PIL import Image

SITE = '/Users/zhangge/.openclaw/workspace-personal-assistant/柴烧网站/site'
FEATURED_DIR = os.path.join(SITE, 'assets/photos/featured')
os.makedirs(FEATURED_DIR, exist_ok=True)

# 首页滚动区 11 张图（slug -> 原图路径）
ROLL = {
    'lamp-sphere-rock': 'assets/photos/product/lamp-sphere-rock/lamp-sphere-rock-1.jpg',
    'mug-lava': 'assets/photos/product/mug-lava/mug-lava-1.jpg',
    'tea-gaiwan-brown': 'assets/photos/product/tea-gaiwan-brown/tea-gaiwan-brown-1.jpg',
    'lamp-sphere-vermillion': 'assets/photos/product/lamp-sphere-vermillion/lamp-sphere-vermillion-1.jpg',
    'vase-olive-crackle': 'assets/photos/product/vase-olive-crackle/vase-olive-crackle-1.jpg',
    'mug-oildrop-olive': 'assets/photos/product/mug-oildrop-olive/mug-oildrop-olive-1.jpg',
    'plate-checker': 'assets/photos/product/plate-checker/plate-checker-1.jpg',
    'incense-tall-brown': 'assets/photos/product/incense-tall-brown/incense-tall-brown-1.jpg',
    'mug-red-iron': 'assets/photos/product/mug-red-iron/mug-red-iron-1.jpg',
    'vase-bicolor-round': 'assets/photos/product/vase-bicolor-round/vase-bicolor-round-1.jpg',
    'sculpture-sphere': 'assets/photos/product/sculpture-sphere/sculpture-sphere-1.jpg',
}

def crop_to_ratio(im, ratio):
    """居中裁切到目标宽高比 ratio (w/h)。"""
    w, h = im.size
    cur = w / h
    if cur > ratio:  # 太宽，裁宽度
        new_w = int(h * ratio)
        left = (w - new_w) // 2
        return im.crop((left, 0, left + new_w, h))
    elif cur < ratio:  # 太高，裁高度
        new_h = int(w / ratio)
        top = (h - new_h) // 2
        return im.crop((0, top, w, top + new_h))
    return im

def make_roll(src, dst, size=(640, 800), quality=72):
    im = Image.open(os.path.join(SITE, src)).convert('RGB')
    im = crop_to_ratio(im, size[0] / size[1])
    im = im.resize(size, Image.LANCZOS)
    im.save(dst, quality=quality, optimize=True)
    return os.path.getsize(dst)

print('=== 滚动图压缩（640x800, q72）===')
total = 0
for slug, src in ROLL.items():
    dst = os.path.join(FEATURED_DIR, slug + '.jpg')
    sz = make_roll(src, dst)
    total += sz
    print(f'  {slug}: {sz//1024} KB')

print(f'  滚动图合计: {total//1024} KB')

# hero 图压缩
print('\n=== hero 图压缩 ===')
hero_src = os.path.join(SITE, 'assets/photos/hero/home-221.jpg')
hero_dst = os.path.join(FEATURED_DIR, 'home-221.jpg')
im = Image.open(hero_src).convert('RGB')
w, h = im.size
if max(w, h) > 1600:
    scale = 1600 / max(w, h)
    im = im.resize((int(w * scale), int(h * scale)), Image.LANCZOS)
im.save(hero_dst, quality=70, optimize=True)
print(f'  home-221.jpg: {os.path.getsize(hero_dst)//1024} KB（原 371 KB）')

print('\n全部完成')
