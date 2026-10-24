#!/usr/bin/env python3
"""数据驱动收尾：重写 shop 卡片 + index featured + 删旧页 + 重新生成 sitemap。"""
import json, os, glob

SITE = '/Users/zhangge/.openclaw/workspace-personal-assistant/柴烧网站/site'
DATA = json.load(open('/Users/zhangge/.openclaw/workspace-personal-assistant/柴烧网站/data/products.json'))
DOMAIN = 'https://www.qingyuan-ceramics.com'

CAT_FILTER = {'台灯': 'lamp', '茶器': 'tea', '茶杯': 'tea', '杯盘': 'table'}

def eur(price):
    return '€' + price.rstrip('0').rstrip('.') if '.' in price else '€' + price

def shop_card(p):
    cat, cat_en = p['category'], p['category_en']
    filt = CAT_FILTER.get(cat, 'tea')
    price = eur(p['price'])
    return f'''        <div class="card" data-cat="{filt}" data-item data-id="{p['product_id']}" data-name="{p['product_name']}" data-name-en="{p['product_name_en']}" data-price="{p['price']}" data-ph="ph-teapot">
          <div class="ph"><img src="assets/photos/product/{p['images'][0]}" alt="{p['image_alt']}"></div>
          <div class="card-body">
            <span class="tag" data-zh="{cat}" data-en="{cat_en}">{cat_en}</span>
            <h3 data-zh="{p['product_name']}" data-en="{p['product_name_en']}">{p['product_name_en']}</h3>
            <div class="price">{price}</div>
            <p data-zh="{p['description']}" data-en="{p['description_en']}">{p['description_en']}</p>
            <div class="card-actions">
              <a class="more" href="{p['slug']}.html" data-zh="查看作品 →" data-en="View work →">View work →</a>
              <button class="add-cart" data-add-cart data-zh="加入购物车" data-en="Add to cart">Add to cart</button>
            </div>
          </div>
        </div>'''

def featured_card(p):
    cat, cat_en = p['category'], p['category_en']
    price = eur(p['price'])
    return f'''        <div class="card">
          <div class="ph"><img src="assets/photos/product/{p['images'][0]}" alt="{p['image_alt']}"></div>
          <div class="card-body">
            <span class="tag" data-zh="{cat}" data-en="{cat_en}">{cat_en}</span>
            <h3 data-zh="{p['product_name']}" data-en="{p['product_name_en']}">{p['product_name_en']}</h3>
            <div class="price">{price}</div>
            <p data-zh="{p['description']}" data-en="{p['description_en']}">{p['description_en']}</p>
            <a class="more" href="{p['slug']}.html" data-zh="查看作品 →" data-en="View work →">View work →</a>
          </div>
        </div>'''

def find_matching_close(html, open_idx):
    """从 open_idx 处的 <div 开始，找匹配的 </div>（只处理 div）。"""
    depth = 0
    i = open_idx
    while i < len(html):
        if html.startswith('<div', i):
            depth += 1
            i += 4
        elif html.startswith('</div>', i):
            depth -= 1
            if depth == 0:
                return i  # 返回 </div> 的起始位置
            i += 6
        else:
            i += 1
    return -1

# ---- 1. 重写 shop.html ----
shop = open(os.path.join(SITE, 'shop.html'), encoding='utf-8').read()

filters = '''      <div class="filters">
        <button class="chip active" data-filter="all" data-zh="全部" data-en="All">All</button>
        <button class="chip" data-filter="tea" data-zh="茶器" data-en="Tea Ware">Tea Ware</button>
        <button class="chip" data-filter="table" data-zh="餐具" data-en="Tableware">Tableware</button>
        <button class="chip" data-filter="lamp" data-zh="台灯" data-en="Lamps">Lamps</button>
      </div>

      <div class="grid">'''

cards = '\n'.join(shop_card(p) for p in DATA['products'])
new_block = filters + '\n' + cards + '\n      </div>'

f_start = shop.index('<div class="filters">')
g_open = shop.index('<div class="grid">', f_start)
g_close = find_matching_close(shop, g_open) + len('</div>')
shop = shop[:f_start] + new_block + shop[g_close:]
open(os.path.join(SITE, 'shop.html'), 'w', encoding='utf-8').write(shop)
print('shop.html 已重写（4 个真实产品）')

# ---- 2. 重写 index.html featured ----
idx = open(os.path.join(SITE, 'index.html'), encoding='utf-8').read()
feat_start = idx.index('<!-- FEATURED -->')
feat_end = idx.index('<!-- CRAFT -->', feat_start)
seg = idx[feat_start:feat_end]
g_s = seg.index('<div class="grid">')
g_e = find_matching_close(seg, g_s) + len('</div>')
feat_cards = '\n'.join(featured_card(p) for p in DATA['products'][:3])
new_seg = seg[:g_s] + '<div class="grid">\n' + feat_cards + '\n      </div>' + seg[g_e:]
idx = idx[:feat_start] + new_seg + idx[feat_end:]
open(os.path.join(SITE, 'index.html'), 'w', encoding='utf-8').write(idx)
print('index.html featured 已重写（3 个真实产品）')

# ---- 3. 删除旧 product-teapot.html ----
old = os.path.join(SITE, 'product-teapot.html')
if os.path.exists(old):
    os.remove(old)
    print('已删除旧 product-teapot.html')

# ---- 4. 重新生成 sitemap.xml ----
now = '2026-10-21'
urls = []
all_html = sorted(glob.glob(os.path.join(SITE, '*.html')) + glob.glob(os.path.join(SITE, 'policies', '*.html')))
for path in all_html:
    rel = os.path.relpath(path, SITE).replace('\\', '/')
    loc = DOMAIN + '/' if rel == 'index.html' else DOMAIN + '/' + rel
    urls.append(f'  <url><loc>{loc}</loc><lastmod>{now}</lastmod></url>')
sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + '\n'.join(urls) + '\n</urlset>\n'
open(os.path.join(SITE, 'sitemap.xml'), 'w', encoding='utf-8').write(sitemap)
print(f'sitemap.xml 已重新生成（{len(urls)} 个 URL）')

print('\n收尾完成')
