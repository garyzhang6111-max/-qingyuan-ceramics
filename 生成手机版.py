#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成手机版 mobile.html（方案 A 土陶风）：
首页一屏网格 + 分类胶囊 + 底部导航；详情屏 + 下单抽屉接真实 Stripe 链路。
数据来自 products.json；缩略图用 assets/photos/mobile/{slug}-m.jpg（见 generate-mobile-thumbs.sh）。"""
import json, os

ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(ROOT, 'site')
DATA = json.load(open(os.path.join(ROOT, 'data', 'products.json'), encoding='utf-8'))

CATS = [
    ('all', '全部', 'All'),
    ('lamp', '灯具', 'Lamps'),
    ('mug', '马克杯', 'Mugs'),
    ('tea', '茶器', 'Tea Ware'),
    ('incense', '香炉', 'Incense'),
    ('vase', '花瓶', 'Vases'),
    ('plate', '餐盘', 'Plates'),
    ('sculpture', '雕塑', 'Sculpture'),
]

products = []
for p in DATA['products']:
    products.append({
        'id': p['slug'],
        'name': p['product_name'],
        'nameEn': p['product_name_en'],
        'price': p['price'],
        'cat': p['filter'],
        'catZh': p['category'],
        'catEn': p['category_en'],
        'desc': (p['description'] or '')[:160],
        'descEn': (p['description_en'] or '')[:160],
        'img': f"assets/photos/mobile/{p['slug']}-m.jpg",
        'imgs': [f"assets/photos/product/{i.split('/')[-2]}/{i.split('/')[-1]}" for i in p['images'][:4]],
    })

payload = json.dumps(products, ensure_ascii=False)
cats_json = json.dumps([[c[0], c[1], c[2]] for c in CATS], ensure_ascii=False)

html = '''<!DOCTYPE html>
<html lang="zh">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title data-zh="清原 · 柴烧孤品" data-en="QINGYUAN · Wood-Fired Ceramics">清原 · 柴烧孤品</title>
<meta name="description" data-zh="柴烧孤品，木火落灰成釉，世间仅此一件。手机直接下单。" data-en="One-of-a-kind wood-fired ceramics. Order directly from your phone." content="One-of-a-kind wood-fired ceramics. Order directly from your phone.">
<link rel="stylesheet" href="css/mobile.css">
<script>(function(){try{if(localStorage.getItem('qingyuan-lang')==='zh'){document.documentElement.setAttribute('lang','zh');document.documentElement.classList.add('early-zh');setTimeout(function(){document.documentElement.classList.remove('early-zh');},1200);}}catch(e){}})();</script>
<style>html.early-zh body{visibility:hidden}</style>
<noscript><style>html.early-zh body{visibility:visible}</style></noscript>
</head>
<body>

<div class="wrap-all">

  <!-- 屏1：首页 -->
  <div class="scr on" id="scr-home">
    <header class="topbar">
      <button class="brand" id="btn-brand">清原</button>
      <div class="top-ic">
        <button class="ic-btn" id="btn-search" aria-label="搜索">🔍</button>
        <button class="ic-btn" id="btn-lang" aria-label="语言">EN</button>
        <button class="ic-btn" id="btn-cart" aria-label="购物袋">🛍️<span class="badge" id="cart-badge" hidden>0</span></button>
      </div>
    </header>
    <nav class="chips" id="chips"></nav>
    <main class="grid2" id="grid"></main>
    <nav class="tabbar">
      <button class="tab on" data-scr="home"><span class="ic">🏺</span><span data-zh="作品" data-en="Works">作品</span></button>
      <button class="tab" data-scr="craft"><span class="ic">🔥</span><span data-zh="工艺" data-en="Craft">工艺</span></button>
      <button class="tab" data-scr="about"><span class="ic">🏮</span><span data-zh="关于" data-en="About">关于</span></button>
      <button class="tab" data-scr="me"><span class="ic">👤</span><span data-zh="我的" data-en="Me">我的</span></button>
    </nav>
  </div>

  <!-- 屏：详情 -->
  <div class="scr" id="scr-detail">
    <header class="topbar">
      <button class="back" id="btn-back">←</button>
      <span class="tbar-title" data-zh="作品详情" data-en="Details">作品详情</span>
      <button class="ic-btn" id="btn-d-fav">♡</button>
    </header>
    <div class="det-ph" id="det-ph"><img id="det-main-img" src="" alt=""></div>
    <div class="det-thumbs" id="det-thumbs"></div>
    <div class="det-body">
      <div class="det-tag" data-zh="世间唯一 · 售出即无" data-en="One of a kind · Once sold, gone">世间唯一 · 售出即无</div>
      <h1 id="det-name"></h1>
      <div class="det-price" id="det-price"></div>
      <p class="det-desc" id="det-desc"></p>
    </div>
    <div class="det-foot">
      <button class="d-cart" id="btn-add-cart" data-zh="加入购物袋" data-en="Add to Bag">加入购物袋</button>
      <button class="d-buy" id="btn-buy" data-zh="立即购买" data-en="Buy Now">立即购买</button>
    </div>
  </div>

  <!-- 屏：购物袋 -->
  <div class="scr" id="scr-cart">
    <header class="topbar">
      <button class="back" data-back="home">←</button>
      <span class="tbar-title" data-zh="购物袋" data-en="Bag">购物袋</span>
      <button class="ic-btn" id="btn-cart-clear">🗑</button>
    </header>
    <main class="cart-list" id="cart-list"></main>
    <div class="cart-foot" id="cart-foot" hidden>
      <div class="cart-total"><span data-zh="合计" data-en="Total">合计</span><b id="cart-total"></b></div>
      <button class="d-buy" id="btn-cart-checkout" data-zh="结算" data-en="Checkout">结算</button>
    </div>
  </div>

  <!-- 屏：工艺 -->
  <div class="scr" id="scr-craft">
    <header class="topbar">
      <button class="back" data-back="home">←</button>
      <span class="tbar-title" data-zh="柴烧工艺" data-en="Wood Firing">柴烧工艺</span>
    </header>
    <main class="plain">
      <img src="assets/photos/craft/kiln-8.jpg" alt="柴烧窑火">
      <h2 data-zh="木火落灰成釉" data-en="Ash Glaze from Wood Fire">木火落灰成釉</h2>
      <p data-zh="不施釉药，柴木在窑中燃烧七天七夜，飞灰落在坯体上熔成独一无二的釉面。每一次开窑，都是火与土不可复制的偶遇。" data-en="No glaze is applied. For seven days and nights the wood fire burns, and flying ash settles on the clay, melting into a glaze that can never be repeated. Every kiln opening is a unique meeting of fire and earth.">不施釉药，柴木在窑中燃烧七天七夜，飞灰落在坯体上熔成独一无二的釉面。每一次开窑，都是火与土不可复制的偶遇。</p>
      <img src="assets/photos/craft/kiln-15.jpg" alt="窑火">
      <p data-zh="火焰的走向、投柴的节奏、天气的干湿，都会在器物上留下痕迹。正因为无法完全掌控，每一件柴烧器才有自己的性格。" data-en="The path of the flame, the rhythm of stoking, the humidity of the air — all leave their marks. It is precisely because fire cannot be fully controlled that every piece has a character of its own.">火焰的走向、投柴的节奏、天气的干湿，都会在器物上留下痕迹。正因为无法完全掌控，每一件柴烧器才有自己的性格。</p>
    </main>
  </div>

  <!-- 屏：关于 -->
  <div class="scr" id="scr-about">
    <header class="topbar">
      <button class="back" data-back="home">←</button>
      <span class="tbar-title" data-zh="关于清原" data-en="About">关于清原</span>
    </header>
    <main class="plain">
      <img src="assets/photos/master/master-1.jpg" alt="柴烧匠人" onerror="this.style.display='none'">
      <h2 data-zh="清原 · 木火之器" data-en="QINGYUAN · Vessels of Fire">清原 · 木火之器</h2>
      <p data-zh="我们只做柴烧。每一件器物都由匠人手工拉坯、柴窑烧制，带着署名与唯一编号。孤品售出即无，不再复烧。" data-en="We make only wood-fired ceramics. Every piece is hand-thrown and fired in a wood kiln, signed by its maker and marked with a unique number. Once a one-off is sold, it is gone forever.">我们只做柴烧。每一件器物都由匠人手工拉坯、柴窑烧制，带着署名与唯一编号。孤品售出即无，不再复烧。</p>
      <p data-zh="全球发货，满 €200 包邮含关税（DDP）。每件作品附手作证书。" data-en="Worldwide shipping. Free over €200, duties included (DDP). Every piece comes with a certificate of craft.">全球发货，满 €200 包邮含关税（DDP）。每件作品附手作证书。</p>
    </main>
  </div>

  <!-- 屏：我的 -->
  <div class="scr" id="scr-me">
    <header class="topbar">
      <button class="back" data-back="home">←</button>
      <span class="tbar-title" data-zh="我的" data-en="Me">我的</span>
    </header>
    <main class="plain">
      <h2 data-zh="收货地址簿" data-en="Saved Addresses">收货地址簿</h2>
      <div id="addr-list" class="addr-list"></div>
      <h2 data-zh="设置" data-en="Settings">设置</h2>
      <div class="set-row"><span data-zh="语言 / Language" data-en="Language">语言 / Language</span><button class="mini-btn" id="btn-lang2">EN</button></div>
      <div class="set-row"><span data-zh="切换桌面版" data-en="Desktop site">切换桌面版</span><button class="mini-btn" id="btn-desktop" data-zh="切换" data-en="Go">切换</button></div>
    </main>
  </div>

</div>

<!-- 下单抽屉 -->
<div class="mask" id="mask"></div>
<section class="sheet" id="sheet" role="dialog" aria-label="下单">
  <div class="grab"></div>
  <h3 id="sheet-name"></h3>
  <div class="qty-row">
    <span data-zh="数量" data-en="Qty">数量</span>
    <div class="qty-box">
      <button id="q-minus" aria-label="减">−</button><b id="q-val">1</b><button id="q-plus" aria-label="加">+</button>
    </div>
    <b class="q-total" id="sheet-total"></b>
  </div>
  <div class="addr-box" id="sheet-addr">
    <div class="addr-empty" data-zh="＋ 填写收货地址" data-en="+ Add shipping address">＋ 填写收货地址</div>
    <div class="addr-pick" hidden>
      <span class="pin">📍</span>
      <span class="at" id="sheet-addr-text"></span>
      <span class="arr">›</span>
    </div>
  </div>
  <div class="email-row" hidden>
    <input type="email" id="sheet-email" placeholder="you@example.com">
  </div>
  <div class="field" id="addr-form" hidden>
    <input id="f-name" placeholder="姓名 / Name">
    <input id="f-phone" placeholder="电话（可选）/ Phone (optional)">
    <input id="f-line1" placeholder="街道门牌 / Street address">
    <input id="f-line2" placeholder="公寓等（可选）/ Apt (optional)">
    <div class="f-row">
      <input id="f-city" placeholder="城市 / City" style="flex:1.2">
      <input id="f-postal" placeholder="邮编 / Postal" style="flex:1">
    </div>
    <select id="f-country">
      <option value="PT">Portugal 🇵🇹</option>
      <option value="DE">Germany 🇩🇪</option>
      <option value="FR">France 🇫🇷</option>
      <option value="ES">Spain 🇪🇸</option>
      <option value="IT">Italy 🇮🇹</option>
      <option value="NL">Netherlands 🇳🇱</option>
      <option value="BE">Belgium 🇧🇪</option>
      <option value="AT">Austria 🇦🇹</option>
      <option value="IE">Ireland 🇮🇪</option>
      <option value="CH">Switzerland 🇨🇭</option>
      <option value="GB">United Kingdom 🇬🇧</option>
      <option value="SE">Sweden 🇸🇪</option>
      <option value="NO">Norway 🇳🇴</option>
      <option value="US">United States 🇺🇸</option>
      <option value="CA">Canada 🇨🇦</option>
      <option value="CN">中国 🇨🇳</option>
      <option value="JP">日本 🇯🇵</option>
      <option value="KR">韩国 🇰🇷</option>
      <option value="AU">Australia 🇦🇺</option>
      <option value="NZ">New Zealand 🇳🇿</option>
      <option value="SG">Singapore 🇸🇬</option>
      <option value="HK">香港 🇭🇰</option>
      <option value="TW">台湾 🇹🇼</option>
      <option value="MO">澳门 🇲🇴</option>
    </select>
    <label class="save-ck"><input type="checkbox" id="f-save" checked> <span data-zh="保存此地址以备下次使用" data-en="Save this address for next time">保存此地址以备下次使用</span></label>
  </div>
  <button class="pay-cta" id="btn-pay"><span id="pay-label" data-zh="支付" data-en="Pay">支付</span> <span id="pay-amt"></span></button>
</section>

<div class="toast" id="toast"></div>

<script>window.MOBILE_PRODUCTS = ''' + payload + ''';</script>
<script>window.MOBILE_CATS = ''' + cats_json + ''';</script>
<script src="js/mobile.js"></script>
</body>
</html>
'''

open(os.path.join(SITE, 'mobile.html'), 'w', encoding='utf-8').write(html)
print(f'mobile.html 已生成：{len(products)} 款产品，{len(CATS)} 个分类')
