#!/usr/bin/env python3
"""首页 featured 改为 6 款代表产品 + 无缝滚动结构。"""
import json, os

ROOT = '/Users/zhangge/.openclaw/workspace-personal-assistant/柴烧网站'
SITE = os.path.join(ROOT, 'site')
DATA = json.load(open(os.path.join(ROOT, 'data/products.json')))

# 10 款代表产品（覆盖全部品类，颜色深、摆正、主体突出；顺序交错打乱）
SLUGS = [
    'lamp-sphere-rock',       # 台灯 · 黑灰岩
    'mug-lava',               # 马克杯 · 黑褐熔岩
    'tea-gaiwan-brown',       # 茶器 · 盖碗黑褐古铜
    'lamp-sphere-vermillion', # 台灯 · 朱红岩（红）
    'vase-olive-crackle',     # 花器 · 橄榄绿冰裂
    'mug-oildrop-olive',      # 马克杯 · 橄榄绿油滴（绿）
    'plate-checker',          # 茶盘 · 四格棋盘
    'incense-tall-brown',     # 香炉 · 高足深茶褐
    'mug-red-iron',           # 马克杯 · 红彩铁红（红）
    'sculpture-sphere',       # 摆件 · 球形
]

prods = {p['slug']: p for p in DATA['products']}

def price_html(p):
    return '€' + p['price'].rstrip('0').rstrip('.') if p['price'] else 'Price on request'

def card(p):
    img = p['images'][0] if p['images'] else 'placeholder.jpg'
    return f'''        <div class="card" data-item data-id="{p['slug']}" data-cat="{p['filter']}" data-name="{p['product_name']}" data-name-en="{p['product_name_en']}" data-price="{p['price']}" data-ph="ph-teapot">
          <div class="ph"><img src="assets/photos/product/{img}" alt="{p['image_alt']}"></div>
          <div class="card-body">
            <h3 data-zh="{p['product_name']}" data-en="{p['product_name_en']}">{p['product_name_en']}</h3>
            <div class="price">{price_html(p)}</div>
            <p data-zh="{p['description']}" data-en="{p['description_en']}">{p['description_en']}</p>
          </div>
        </div>'''

cards = '\n'.join(card(prods[s]) for s in SLUGS)

# 新结构：marquee 容器 + 轨道（内容由 JS 复制实现无缝）
new_block = '''        <div class="featured-marquee">
        <div class="featured-track" data-marquee-track>
''' + cards + '''
        </div>
      </div>'''

# 读 index.html，替换 featured 区块里的商品容器
idx = open(os.path.join(SITE, 'index.html'), encoding='utf-8').read()

# 定位 featured section
f_start = idx.index('<section class="featured">')

# 兼容两种状态：已有 featured-marquee / featured-track，或旧的 grid
def find_open(html, start):
    mq = html.find('<div class="featured-marquee">', start)
    grid = html.find('<div class="grid">', start)
    candidates = [p for p in [mq, grid] if p != -1]
    return min(candidates) if candidates else -1

g_open = find_open(idx, f_start)
if g_open == -1:
    raise SystemExit('❌ 找不到 featured 商品容器')

def find_matching_close(html, open_idx):
    depth = 0
    i = open_idx
    while i < len(html):
        if html.startswith('<div', i):
            depth += 1
            i += 4
        elif html.startswith('</div>', i):
            depth -= 1
            if depth == 0:
                return i
            i += 6
        else:
            i += 1
    return -1

g_close = find_matching_close(idx, g_open) + len('</div>')
idx = idx[:g_open] + new_block + idx[g_close:]
open(os.path.join(SITE, 'index.html'), 'w', encoding='utf-8').write(idx)
print(f'index.html featured 已改为 {len(SLUGS)} 款代表产品 + 无缝滚动结构')
