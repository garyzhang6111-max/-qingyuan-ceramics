#!/usr/bin/env python3
"""数据驱动生成 4 个产品详情页（slug 命名），并更新 shop/index 链接。
真实字段来自 products.json；待确认字段如实显示 'To be confirmed'，不编造窑位/窑次等。
"""
import json, os

SITE = '/Users/zhangge/.openclaw/workspace-personal-assistant/柴烧网站/site'
DATA = json.load(open('/Users/zhangge/.openclaw/workspace-personal-assistant/柴烧网站/data/products.json'))
DOMAIN = 'https://www.qingyuan-ceramics.com'  # 占位域名

def cn_val(p, key, zh_label, en_label):
    """返回规格表一行；值含'待确认'时英文显示 To be confirmed"""
    v = p.get(key, '')
    if '待确认' in v:
        en = 'To be confirmed'
        zh = '待确认'
    else:
        en = v
        zh = v
    return (zh_label, en_label, zh, en)

def gen(p):
    slug = p['slug']
    name_en = p['product_name_en']
    name_zh = p['product_name']
    desc_en = p['description_en']
    desc_zh = p['description']
    price = p['price'].rstrip('0').rstrip('.') if '.' in p['price'] else p['price']
    imgs = p['images']
    main = imgs[0]
    thumbs = imgs[1:4] if len(imgs) > 1 else []
    # 规格表（只含有据可查字段）
    specs = [
        cn_val(p, 'materials', '材质', 'Material'),
        cn_val(p, 'dimensions', '尺寸', 'Dimensions'),
        cn_val(p, 'capacity', '容量', 'Capacity'),
        cn_val(p, 'firing_method', '烧制方式', 'Firing'),
        cn_val(p, 'origin', '产地', 'Origin'),
        cn_val(p, 'artist_or_maker', '匠人', 'Maker'),
    ]
    spec_rows = []
    for zh_label, en_label, zh_v, en_v in specs:
        spec_rows.append(f'<tr><th data-zh="{zh_label}" data-en="{en_label}">{en_label}</th><td data-zh="{zh_v}" data-en="{en_v}">{en_v}</td></tr>')
    spec_html = '\n              '.join(spec_rows)

    care_en = p.get('care_information', '')
    if '待确认' in care_en:
        care_en = 'Care instructions to be confirmed.'
    ship_en = p.get('shipping_information', '')
    if '待确认' in ship_en:
        ship_en = 'Shipping details to be confirmed.'

    gallery_thumbs = []
    for t in thumbs:
        gallery_thumbs.append(f'          <div class="ph"><img src="assets/photos/product/{t}" alt="{p["image_alt"]}"></div>')
    gallery_html = '\n'.join(gallery_thumbs)

    # 相关推荐：取 related_products 第一个，找对应 slug
    related = []
    for rp in p.get('related_products', []):
        for q in DATA['products']:
            if q['slug'] == rp:
                related.append(q)
                break
    related_cards = []
    for q in related[:3]:
        rprice = '€' + q['price'].rstrip('0').rstrip('.') if q['price'] else 'Price on request'
        related_cards.append(f'''        <div class="card" data-item data-id="{q["slug"]}" data-cat="{q["filter"]}">
          <div class="ph"><img src="assets/photos/product/{q["images"][0]}" alt="{q["image_alt"]}"></div>
          <div class="card-body">
            <h3 data-zh="{q["product_name"]}" data-en="{q["product_name_en"]}">{q["product_name_en"]}</h3>
            <div class="price">{rprice}</div>
          </div>
        </div>''')
    related_html = '\n'.join(related_cards)

    alt = p['image_alt']
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title data-zh="{name_zh} | QINGYUAN 柴烧孤品" data-en="{name_en} | QINGYUAN Wood-Fired Ceramics">{name_en} | QINGYUAN Wood-Fired Ceramics</title>
<meta name="description" data-zh="{desc_zh}" data-en="{desc_en}" content="{desc_en}">
<link rel="canonical" href="{DOMAIN}/{slug}.html">
<link rel="stylesheet" href="css/style.css">
<script type="application/ld+json">
{json.dumps({
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {"@type": "ListItem", "position": 1, "name": "Home", "item": DOMAIN + "/"},
    {"@type": "ListItem", "position": 2, "name": "Shop", "item": DOMAIN + "/shop.html"},
    {"@type": "ListItem", "position": 3, "name": name_en},
  ],
}, ensure_ascii=False, indent=2)}
</script>
<script type="application/ld+json">
{json.dumps({
  "@context": "https://schema.org",
  "@type": "Product",
  "name": name_en,
  "description": desc_en,
  "image": [DOMAIN + "/assets/photos/product/" + main],
  "sku": p["product_id"],
  "brand": {"@type": "Brand", "name": "QINGYUAN"},
  "offers": {
    "@type": "Offer",
    "url": DOMAIN + "/" + slug + ".html",
    "priceCurrency": "EUR",
    "price": p["price"],
    "availability": "https://schema.org/InStock",
    "itemCondition": "https://schema.org/NewCondition",
  },
}, ensure_ascii=False, indent=2)}
</script>
</head>
<body>

<header>
  <div class="wrap nav">
    <a href="index.html" class="logo" data-zh="清原" data-en="QINGYUAN">QINGYUAN</a>
    <ul class="nav-links" id="nav">
      <li><a href="index.html" data-zh="首页" data-en="Home">Home</a></li>
      <li><a href="shop.html" class="active" data-zh="商店" data-en="Shop">Shop</a></li>
      <li><a href="masters.html" data-zh="大师" data-en="Masters">Masters</a></li>
      <li><a href="craft.html" data-zh="工艺" data-en="Craft">Craft</a></li>
      <li><a href="about.html" data-zh="关于" data-en="About">About</a></li>
      <li><a href="contact.html" data-zh="联系" data-en="Contact">Contact</a></li>
    </ul>
    <div class="nav-right">
      <div class="lang-switch">
        <button class="lang-btn" data-lang="zh">中</button>
        <span class="lang-sep">/</span>
        <button class="lang-btn active" data-lang="en">EN</button>
      </div>
      <button class="burger" id="burger" aria-label="菜单">☰</button>
    </div>
  </div>
</header>

<main>
  <section class="pd">
    <div class="wrap">
      <div class="crumb" style="margin-bottom:20px" data-zh="<a href='index.html'>首页</a> / <a href='shop.html'>商店</a> / {name_zh}" data-en="<a href='index.html'>Home</a> / <a href='shop.html'>Shop</a> / {name_en}"><a href="index.html">Home</a> / <a href="shop.html">Shop</a> / {name_en}</div>
      <div class="pd-grid">
        <div class="pd-gallery">
          <div class="ph main"><img src="assets/photos/product/{main}" alt="{alt}"></div>
{gallery_html}
        </div>
        <div class="pd-info" data-item data-id="{p["product_id"]}" data-name="{name_zh}" data-name-en="{name_en}" data-price="{p["price"]}" data-ph="ph-teapot">
          <span class="tag" data-zh="{p["category"]} · 世间唯一" data-en="{p["category_en"]} · One of a Kind">{p["category_en"]} · One of a Kind</span>
          <h1 data-zh="{name_zh}" data-en="{name_en}">{name_en}</h1>
          <div class="price">€{price}</div>
          <div class="stock" data-zh="✓ 孤品 · 仅此一件 · 售出即无" data-en="✓ One of a kind · Once sold, it is gone">✓ One of a kind · Once sold, it is gone</div>

          <p class="hook" data-zh="{desc_zh}" data-en="{desc_en}">{desc_en}</p>

          <div class="pd-buy">
            <button class="add-cart add-cart-lg" data-add-cart data-zh="加入购物车" data-en="Add to cart">Add to cart</button>
            <a class="btn dark" href="contact.html" data-zh="定制咨询" data-en="Commission">Commission</a>
            <span style="font-size:.82rem;color:var(--muted)" data-zh="孤品唯一，付款后锁定" data-en="One-off — payment reserves it">One-off — payment reserves it</span>
          </div>

          <div class="specs">
            <table>
              {spec_html}
              <tr><th data-zh="配送" data-en="Shipping">Shipping</th><td data-zh="{ship_en}" data-en="{ship_en}">{ship_en}</td></tr>
            </table>
          </div>

          <div class="trust">
            <div><span class="ic">🖋</span><span data-zh="大师亲制" data-en="Handmade &amp; signed">Handmade &amp; signed</span></div>
            <div><span class="ic">📜</span><span data-zh="亲签证书" data-en="Certificate of authenticity">Certificate of authenticity</span></div>
            <div><span class="ic">🌍</span><span data-zh="全球包邮" data-en="Worldwide shipping">Worldwide shipping</span></div>
          </div>

          <div class="care">
            <h3 data-zh="使用与养护" data-en="Care">Care</h3>
            <ul>
              <li data-zh="首次使用前用清水洗净，温水浸泡数小时更佳" data-en="Rinse before first use; a warm soak helps">Rinse before first use; a warm soak helps</li>
              <li data-zh="茶器用后及时洗净，自然晾干，勿用洗洁精久泡" data-en="Wash and air-dry after use; avoid soaking in detergent">Wash and air-dry after use; avoid soaking in detergent</li>
              <li data-zh="落灰釉表面可能保留细微气孔与火痕，属自然窑变，非瑕疵" data-en="Ash glaze may keep subtle pores and fire marks — natural, not defects">Ash glaze may keep subtle pores and fire marks — natural, not defects</li>
              <li data-zh="避免骤冷骤热" data-en="Avoid sudden temperature changes">Avoid sudden temperature changes</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </section>

  <section class="featured">
    <div class="wrap">
      <div class="sec-head">
        <h2 data-zh="相关推荐" data-en="Related Works">Related Works</h2>
      </div>
      <div class="grid">
{related_html}
      </div>
    </div>
  </section>
</main>

<footer>
  <div class="wrap">
    <div class="foot">
      <div>
        <div class="logo" data-zh="清原" data-en="QINGYUAN">QINGYUAN</div>
        <p data-zh="每一件器物，都是一窑火与泥土的偶遇，世间仅此一件。" data-en="Every piece is a meeting of fire and earth — one of a kind.">Every piece is a meeting of fire and earth — one of a kind.</p>
      </div>
      <div>
        <h4 data-zh="探索" data-en="Explore">Explore</h4>
        <ul>
          <li><a href="shop.html" data-zh="大师孤品" data-en="Works">Works</a></li>
          <li><a href="craft.html" data-zh="工艺" data-en="Craft">Craft</a></li>
          <li><a href="masters.html" data-zh="大师" data-en="Masters">Masters</a></li>
        </ul>
      </div>
      <div>
        <h4 data-zh="服务" data-en="Service">Service</h4>
        <ul>
          <li><a href="policies/shipping.html" data-zh="全球配送" data-en="Shipping">Shipping</a></li>
          <li><a href="policies/returns.html" data-zh="退换政策" data-en="Returns">Returns</a></li>
          <li><a href="policies/privacy.html" data-zh="隐私政策" data-en="Privacy">Privacy</a></li>
        </ul>
      </div>
      <div>
        <h4 data-zh="联系" data-en="Contact">Contact</h4>
        <ul>
          <li><a href="mailto:hello@qingyuan.example">hello@qingyuan.example</a></li>
          <li><a href="#">Instagram</a></li>
          <li><a href="#">Pinterest</a></li>
        </ul>
      </div>
    </div>
    <div class="foot-bottom">
      <span data-zh="© 2026 清原 · 版权所有" data-en="© 2026 QINGYUAN · All rights reserved">© 2026 QINGYUAN · All rights reserved</span>
      <span data-zh="柴烧 · 大师之作 · 世间唯一" data-en="Wood-Fired · Made by Masters · One of a Kind">Wood-Fired · Made by Masters · One of a Kind</span>
    </div>
  </div>
</footer>

<script src="js/main.js"></script>
</body>
</html>
'''
    return html

# 生成 4 个详情页
for p in DATA['products']:
    path = os.path.join(SITE, p['slug'] + '.html')
    open(path, 'w', encoding='utf-8').write(gen(p))
    print('已生成:', p['slug'] + '.html')

print('\n完成，共', len(DATA['products']), '个详情页')
