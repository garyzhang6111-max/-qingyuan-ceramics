#!/usr/bin/env python3
"""批量生成 4 个政策页（shipping/returns/privacy/terms），英语主线。"""
import os

SITE = '/Users/zhangge/.openclaw/workspace-personal-assistant/柴烧网站/site'
P = os.path.join(SITE, 'policies')
os.makedirs(P, exist_ok=True)

def page(en_title, zh_title, en_h1, zh_h1, en_desc, zh_desc, sections):
    """sections: list of (en_h2, zh_h2, en_p, zh_p)"""
    sec_html = []
    for en_h2, zh_h2, en_p, zh_p in sections:
        sec_html.append(
            f'      <div class="val">\n'
            f'        <h3 data-zh="{zh_h2}" data-en="{en_h2}">{en_h2}</h3>\n'
            f'        <p data-zh="{zh_p}" data-en="{en_p}">{en_p}</p>\n'
            f'      </div>'
        )
    body = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title data-zh="{zh_title}" data-en="{en_title}">{en_title}</title>
<meta name="description" data-zh="{zh_desc}" data-en="{en_desc}" content="{en_desc}">
<link rel="stylesheet" href="../css/style.css">
</head>
<body>

<header>
  <div class="wrap nav">
    <a href="../index.html" class="logo" data-zh="清原" data-en="QINGYUAN">QINGYUAN</a>
    <ul class="nav-links" id="nav">
      <li><a href="../index.html" data-zh="首页" data-en="Home">Home</a></li>
      <li><a href="../shop.html" data-zh="商店" data-en="Shop">Shop</a></li>
      <li><a href="../masters.html" data-zh="大师" data-en="Masters">Masters</a></li>
      <li><a href="../craft.html" data-zh="工艺" data-en="Craft">Craft</a></li>
      <li><a href="../about.html" data-zh="关于" data-en="About">About</a></li>
      <li><a href="../contact.html" data-zh="联系" data-en="Contact">Contact</a></li>
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
  <section class="page-hero">
    <div class="ph ph-craft"><img src="../assets/photos/craft/kiln-8.jpg" alt="柴烧窑火"></div>
    <div class="wrap">
      <div class="crumb" data-zh="<a href='../index.html'>首页</a> / {zh_title}" data-en="<a href='../index.html'>Home</a> / {en_title}"><a href="../index.html">Home</a> / {en_title}</div>
      <div class="kicker" data-zh="政策" data-en="Policy">Policy</div>
      <h1 data-zh="{zh_h1}" data-en="{en_h1}">{en_h1}</h1>
    </div>
  </section>

  <section class="values">
    <div class="wrap">
      <div class="vals">
{chr(10).join(sec_html)}
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
          <li><a href="../shop.html" data-zh="大师孤品" data-en="Works">Works</a></li>
          <li><a href="../craft.html" data-zh="工艺" data-en="Craft">Craft</a></li>
          <li><a href="../masters.html" data-zh="大师" data-en="Masters">Masters</a></li>
        </ul>
      </div>
      <div>
        <h4 data-zh="服务" data-en="Service">Service</h4>
        <ul>
          <li><a href="shipping.html" data-zh="全球配送" data-en="Shipping">Shipping</a></li>
          <li><a href="returns.html" data-zh="退换政策" data-en="Returns">Returns</a></li>
          <li><a href="privacy.html" data-zh="隐私政策" data-en="Privacy">Privacy</a></li>
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

<script src="../js/main.js"></script>
</body>
</html>
'''
    return body

pages = {
    'shipping.html': page(
        'Shipping Policy', '全球配送',
        'Shipping', '全球配送',
        'QINGYUAN 柴烧陶瓷的全球配送政策。',
        'QINGYUAN wood-fired ceramics shipping policy.',
        [
            ('Processing Time', '处理时间',
             'Each piece is one of a kind and ships from our studio. Orders are processed and dispatched within 2–4 business days of payment confirmation.',
             '每件孤品均从工作室发出。付款确认后 2–4 个工作日内处理并发货。'),
            ('Worldwide Shipping', '全球配送',
             'We ship worldwide with tracked, fully insured delivery. Shipping costs and estimated delivery times are shown at checkout.',
             '我们提供全球配送，全程可追踪、全额保险。运费与预计时效在结算页显示。'),
            ('Packaging', '包装',
             'Every piece is packed in custom, shock-proof packaging to survive the journey. (Final packaging details to be confirmed.)',
             '每件器物使用定制防震包装，确保运输安全。（最终包装细节待确认。）'),
            ('Customs & Duties', '关税',
             'International orders may be subject to customs duties and import taxes, which are the responsibility of the recipient.',
             '国际订单可能产生关税与进口税，由收件方承担。'),
        ],
    ),
    'returns.html': page(
        'Returns Policy', '退换政策',
        'Returns', '退换政策',
        'QINGYUAN 柴烧陶瓷的退换政策。',
        'QINGYUAN wood-fired ceramics returns policy.',
        [
            ('One-of-a-Kind Items', '孤品说明',
             'Each piece is unique and sold as-is. Because no two are alike, returns for exchange are not possible — but we will always make it right if your piece arrives damaged.',
             '每件皆为孤品，售出即无。因孤品无法换货，但若运输途中损坏，我们负责到底。'),
            ('Damaged on Arrival', '运输损坏',
             'If your piece arrives damaged, contact us within 48 hours with photos, and we will arrange a refund or repair.',
             '若器物运输中损坏，请在 48 小时内联系我们并提供照片，我们将安排退款或修复。'),
            ('Refund Process', '退款流程',
             'Approved refunds are returned to the original payment method within 5–10 business days.',
             '批准的退款将在 5–10 个工作日内原路退回。'),
        ],
    ),
    'privacy.html': page(
        'Privacy Policy', '隐私政策',
        'Privacy', '隐私政策',
        'QINGYUAN 柴烧陶瓷的隐私政策。',
        'QINGYUAN wood-fired ceramics privacy policy.',
        [
            ('Data We Collect', '收集的数据',
             'We collect only the information needed to process your order: name, shipping address, email, and payment details (handled by our payment processor).',
             '我们仅收集处理订单所需的信息：姓名、收货地址、邮箱，以及支付信息（由支付服务商处理）。'),
            ('How We Use It', '数据用途',
             'Your information is used solely to fulfill orders and provide customer service. We never sell your data.',
             '你的信息仅用于完成订单和提供客服。我们绝不售卖你的数据。'),
            ('GDPR Rights', 'GDPR 权利',
             'EU customers have the right to access, correct, or delete their personal data at any time. Contact us to exercise these rights.',
             '欧盟客户有权随时访问、更正或删除个人数据。联系我们即可行使这些权利。'),
        ],
    ),
    'terms.html': page(
        'Terms of Service', '服务条款',
        'Terms', '服务条款',
        'QINGYUAN 柴烧陶瓷的服务条款。',
        'QINGYUAN wood-fired ceramics terms of service.',
        [
            ('Orders & Payment', '订单与支付',
             'Orders are confirmed upon successful payment. Prices are listed in EUR and may include applicable taxes.',
             '订单在支付成功后确认。价格以欧元标示，可能包含适用税费。'),
            ('Product Description', '产品说明',
             'Each piece is handcrafted and unique; natural variations in glaze and fire marks are not defects.',
             '每件皆为手工孤品，釉色与火痕的天然差异并非瑕疵。'),
            ('Liability', '责任条款',
             'Our liability is limited to the purchase price of the item. (Full legal terms to be confirmed.)',
             '我方责任以商品购买价为限。（完整法律条款待确认。）'),
        ],
    ),
}

for fname, content in pages.items():
    open(os.path.join(P, fname), 'w', encoding='utf-8').write(content)
    print('已生成:', fname)

print('\n共生成', len(pages), '个政策页')
