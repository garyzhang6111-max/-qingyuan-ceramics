#!/usr/bin/env python3
"""更新现有页面：导航加 About，footer 服务列指向政策页。"""
import os, glob

SITE = '/Users/zhangge/.openclaw/workspace-personal-assistant/柴烧网站/site'
# 只处理根目录的 7 个页面（不含 policies/ 子目录，它已含 About + 新 footer）
files = [f for f in glob.glob(os.path.join(SITE, '*.html'))]

def update(path):
    html = open(path, encoding='utf-8').read()
    orig = html
    # 1. 导航：在 craft 之后、contact 之前插入 about
    #    已有 about 链接的跳过
    if 'href="about.html"' not in html:
        html = html.replace(
            '<li><a href="contact.html" data-zh="联系" data-en="Contact">Contact</a></li>',
            '<li><a href="about.html" data-zh="关于" data-en="About">About</a></li>\n      <li><a href="contact.html" data-zh="联系" data-en="Contact">Contact</a></li>',
            1  # 只替换第一个（导航里那个）
        )
    # 2. footer 服务列：Shipping/Returns/Safety -> 政策页
    html = html.replace(
        '<li><a href="contact.html" data-zh="全球配送" data-en="Shipping">Shipping</a></li>',
        '<li><a href="policies/shipping.html" data-zh="全球配送" data-en="Shipping">Shipping</a></li>'
    )
    html = html.replace(
        '<li><a href="contact.html" data-zh="退换政策" data-en="Returns">Returns</a></li>',
        '<li><a href="policies/returns.html" data-zh="退换政策" data-en="Returns">Returns</a></li>'
    )
    html = html.replace(
        '<li><a href="contact.html" data-zh="检测认证" data-en="Safety">Safety</a></li>',
        '<li><a href="policies/privacy.html" data-zh="隐私政策" data-en="Privacy">Privacy</a></li>'
    )
    if html != orig:
        open(path, 'w', encoding='utf-8').write(html)
        return True
    return False

for f in files:
    if update(f):
        print('已改:', os.path.basename(f))
    else:
        print('无变化:', os.path.basename(f))
