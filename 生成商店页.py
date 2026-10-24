#!/usr/bin/env python3
"""重新生成 shop.html：27 款产品，4 类筛选，三列静态 grid。"""
import json, os

ROOT = '/Users/zhangge/.openclaw/workspace-personal-assistant/柴烧网站'
SITE = os.path.join(ROOT, 'site')
DATA = json.load(open(os.path.join(ROOT, 'data/products.json')))

CATS = [('守光灯具', 'Light Keeper', 'lamp'), ('马克杯', 'Mugs', 'mug'), ('茶器', 'Tea Ware', 'tea'), ('香炉', 'Incense Burners', 'incense'), ('花器', 'Vases', 'vase'), ('茶盘', 'Tea Trays', 'plate')]

def price_html(p):
    return '€' + p['price'].rstrip('0').rstrip('.') if p['price'] else 'Price on request'

def card(p):
    img = p['images'][0] if p['images'] else 'placeholder.jpg'
    return f'''        <div class="card" data-cat="{p['filter']}" data-item data-id="{p['slug']}" data-name="{p['product_name']}" data-name-en="{p['product_name_en']}" data-price="{p['price']}" data-ph="ph-teapot">
          <div class="ph"><img src="assets/photos/product/{img}" alt="{p['image_alt']}"></div>
          <div class="card-body">
            <h3 data-zh="{p['product_name']}" data-en="{p['product_name_en']}">{p['product_name_en']}</h3>
            <div class="price">{price_html(p)}</div>
            <p data-zh="{p['description']}" data-en="{p['description_en']}">{p['description_en']}</p>
            <div class="card-actions">
              <button class="add-cart" data-add-cart data-zh="加入购物车" data-en="Add to cart">Add to cart</button>
            </div>
          </div>
        </div>'''

filters = '      <div class="filters">\n        <button class="chip active" data-filter="all" data-zh="全部" data-en="All">All</button>\n'
for zh, en, filt in CATS:
    filters += f'        <button class="chip" data-filter="{filt}" data-zh="{zh}" data-en="{en}">{en}</button>\n'
filters += '      </div>\n'

cards = '\n'.join(card(p) for p in DATA['products'])
new_block = filters + '\n      <div class="grid">\n' + cards + '\n      </div>'

shop = open(os.path.join(SITE, 'shop.html'), encoding='utf-8').read()

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

f_start = shop.index('<div class="filters">')
# 找 filters 之后第一个 grid（可能是 shop-rows 或 grid）
search = shop[f_start:]
# 定位 shop-rows 或 grid 的结束：从 filters 开始，找到 section.shop 内主容器结束
# 直接找 </section> 前的内容块
sec_end = shop.index('</section>', f_start)
# 在 filters 和 section 结束之间，找 shop-rows 或 grid 起始
block = shop[f_start:sec_end]
if '<div class="shop-rows">' in block:
    g_open_abs = shop.index('<div class="shop-rows">', f_start)
    g_close_abs = find_matching_close(shop, g_open_abs) + len('</div>')
else:
    g_open_abs = shop.index('<div class="grid">', f_start)
    g_close_abs = find_matching_close(shop, g_open_abs) + len('</div>')

shop = shop[:f_start] + new_block + shop[g_close_abs:]
open(os.path.join(SITE, 'shop.html'), 'w', encoding='utf-8').write(shop)
print(f'shop.html 已重写：{len(DATA["products"])} 款，三列静态 grid')
