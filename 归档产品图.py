#!/usr/bin/env python3
"""重新归档：保持原图本色，只做缩放（不裁切主体、不改色调）。"""
import os, shutil
from PIL import Image

SRC = '/Users/zhangge/.openclaw/workspace-personal-assistant/柴烧网站/上架图源'
DST = '/Users/zhangge/.openclaw/workspace-personal-assistant/柴烧网站/产品图-新'

GROUPS = {
    'lamp-ivory-gray':      [165, 166, 170],
    'lamp-blue-gray':       [176],
    'lamp-red-warm':        [177],
    'lamp-red-globe':       [167, 168, 169],
    'lamp-amber':           [173],
    'lamp-bicolor':         [174],
    'lamp-dark-mini':       [175],
    'lamp-bicolor-shade':   [184, 185],
    'lamp-speckle':         [186, 187, 188],
    'lamp-crater':          [189, 190],
    'lamp-caramel':         [183],
    'lamp-mottled':         [211, 213, 214],
    'lamp-bicolor-sphere':  [210],
    'lamp-amber-sphere':    [212],
    'mug-ribbed-white':     [178, 198, 199, 200, 201],
    'mug-blue-ombre':       [196, 197],
    'mug-crackle':          [179],
    'mug-threaded':         [195],
    'tea-fairness-pitcher': [202, 203],
    'tea-water-basin':      [204],
    'tea-rimmed-basin':     [205],
    'tea-master-cup':       [220],
    'incense-amber':        [218, 219],
    'vase-ribbed-round':    [180, 182, 208, 209],
    'vase-tall-neck':       [181, 206, 207],
    'vase-light-round':     [215],
    'vase-dark-fire':       [216],
}

CATEGORY = {'lamp': '台灯', 'mug': '马克杯', 'tea': '茶具香炉', 'incense': '茶具香炉', 'vase': '花器大罐'}

def cat_of(slug):
    return CATEGORY.get(slug.split('-')[0], '其他')

if os.path.exists(DST):
    shutil.rmtree(DST)

total = 0
for slug, nums in GROUPS.items():
    cat = cat_of(slug)
    outdir = os.path.join(DST, cat, slug)
    os.makedirs(outdir, exist_ok=True)
    for i, n in enumerate(nums, 1):
        src = os.path.join(SRC, f'WechatIMG{n}.jpg')
        if not os.path.exists(src):
            print(f'⚠️ 缺失: {n}')
            continue
        im = Image.open(src).convert('RGB')
        w, h = im.size
        # 不裁切主体：保持原比例，统一缩放到宽度 1200（竖图）或高度 1200（横图）
        if w >= h:
            # 横图：按高度缩放
            new_h = 1200
            new_w = int(w * new_h / h)
        else:
            # 竖图：按宽度缩放
            new_w = 1200
            new_h = int(h * new_w / w)
        im = im.resize((new_w, new_h), Image.LANCZOS)
        im.save(os.path.join(outdir, f'{slug}-{i}.jpg'), quality=90)
        total += 1
    print(f'✅ {cat}/{slug}: {len(nums)} 图')

print(f'\n共处理 {total} 张（{len(GROUPS)} 款）')
