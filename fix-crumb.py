#!/usr/bin/env python3
"""处理 crumb 面包屑默认文本（含 HTML，之前跳过的），并统一 product-teapot 命名。"""
import os

SITE = '/Users/zhangge/.openclaw/workspace-personal-assistant/柴烧网站/site'

# 每个文件：[(旧默认文本, 新英文文本)]
CRUMBS = {
    'checkout.html': [
        ('<a href="index.html">首页</a> / <a href="shop.html">商店</a> / 结算',
         '<a href="index.html">Home</a> / <a href="shop.html">Shop</a> / Checkout'),
    ],
    'contact.html': [
        ('<a href="index.html">首页</a> / 联系', '<a href="index.html">Home</a> / Contact'),
    ],
    'craft.html': [
        ('<a href="index.html">首页</a> / 工艺', '<a href="index.html">Home</a> / Craft'),
    ],
    'masters.html': [
        ('<a href="index.html">首页</a> / 大师', '<a href="index.html">Home</a> / Masters'),
    ],
    'product-teapot.html': [
        ('<a href="index.html">首页</a> / <a href="shop.html">商店</a> / 茶壶 No. 007',
         '<a href="index.html">Home</a> / <a href="shop.html">Shop</a> / Tea Set No. 007'),
        # data-en 属性里也把 Teapot 统一成 Tea Set
        ('data-en="<a href=\'index.html\'>Home</a> / <a href=\'shop.html\'>Shop</a> / Teapot No. 007"',
         'data-en="<a href=\'index.html\'>Home</a> / <a href=\'shop.html\'>Shop</a> / Tea Set No. 007"'),
    ],
    'shop.html': [
        ('<a href="index.html">首页</a> / 商店', '<a href="index.html">Home</a> / Shop'),
    ],
}

for fname, pairs in CRUMBS.items():
    path = os.path.join(SITE, fname)
    html = open(path, encoding='utf-8').read()
    orig = html
    for old, new in pairs:
        if old in html:
            html = html.replace(old, new)
        else:
            print(f'⚠️ {fname}: 未找到 {old[:40]}...')
    if html != orig:
        open(path, 'w', encoding='utf-8').write(html)
        print(f'已改: {fname}')
    else:
        print(f'无变化: {fname}')
