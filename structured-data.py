#!/usr/bin/env python3
"""Phase 9 结构化数据：Organization（首页）+ Product/Offer/BreadcrumbList（产品页）。"""
import json, os

SITE = '/Users/zhangge/.openclaw/workspace-personal-assistant/柴烧网站/site'
DOMAIN = 'https://www.qingyuan-ceramics.com'  # 待确认最终域名

def inject(path, jsonld_obj):
    html = open(path, encoding='utf-8').read()
    if 'application/ld+json' in html:
        return
    script = '<script type="application/ld+json">\n' + json.dumps(jsonld_obj, ensure_ascii=False, indent=2) + '\n</script>'
    html = html.replace('</head>', script + '\n</head>', 1)
    open(path, 'w', encoding='utf-8').write(html)
    print('JSON-LD 已注入:', os.path.basename(path))

# 1. Organization → 首页
org = {
    "@context": "https://schema.org",
    "@type": "Organization",
    "name": "QINGYUAN",
    "url": DOMAIN,
    "description": "Wood-fired ceramics by masters — one-of-a-kind pieces.",
    "email": "hello@qingyuan.example",
}
inject(os.path.join(SITE, 'index.html'), org)

# 2. Product + Offer + BreadcrumbList → 产品详情页
product = [
    {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": DOMAIN + "/"},
            {"@type": "ListItem", "position": 2, "name": "Shop", "item": DOMAIN + "/shop.html"},
            {"@type": "ListItem", "position": 3, "name": "Wood-Fired Tea Set · Masterwork"},
        ],
    },
    {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": "Wood-Fired Tea Set · Masterwork",
        "description": "A complete wood-fired tea set — tray, vase and cups — with natural ash glaze.",
        "image": [DOMAIN + "/assets/photos/product/teaset-2.jpg"],
        "sku": "teaset-007",
        "brand": {"@type": "Brand", "name": "QINGYUAN"},
        "offers": {
            "@type": "Offer",
            "url": DOMAIN + "/product-teapot.html",
            "priceCurrency": "EUR",
            "price": "550.00",
            "availability": "https://schema.org/InStock",
            "itemCondition": "https://schema.org/NewCondition",
        },
    },
]
for obj in product:
    inject(os.path.join(SITE, 'product-teapot.html'), obj)
