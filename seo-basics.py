#!/usr/bin/env python3
"""Phase 6 SEO：加 canonical、生成 sitemap.xml、robots.txt。"""
import os, glob, re

SITE = '/Users/zhangge/.openclaw/workspace-personal-assistant/柴烧网站/site'
DOMAIN = 'https://www.qingyuan-ceramics.com'  # 待确认最终域名，先用占位

# 页面 canonical 路径（相对站根）
# 根目录页面 + policies 子目录页面
all_html = sorted(glob.glob(os.path.join(SITE, '*.html')) + glob.glob(os.path.join(SITE, 'policies', '*.html')))

def rel_path(path):
    return os.path.relpath(path, SITE).replace('\\', '/')

# 1. 加 canonical
for path in all_html:
    html = open(path, encoding='utf-8').read()
    if 'rel="canonical"' in html:
        continue
    rel = rel_path(path)
    url = f'{DOMAIN}/{rel}'
    canon = f'<link rel="canonical" href="{url}">'
    html = html.replace('</head>', f'{canon}\n</head>', 1)
    open(path, 'w', encoding='utf-8').write(html)
    print('canonical 已加:', rel)

# 2. sitemap.xml
now = '2026-10-21'
urls = []
for path in all_html:
    rel = rel_path(path)
    if rel == 'index.html':
        loc = DOMAIN + '/'
    else:
        loc = DOMAIN + '/' + rel
    urls.append(f'  <url><loc>{loc}</loc><lastmod>{now}</lastmod></url>')

sitemap = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + '\n'.join(urls) + '\n</urlset>\n'
open(os.path.join(SITE, 'sitemap.xml'), 'w', encoding='utf-8').write(sitemap)
print(f'\nsitemap.xml 已生成（{len(urls)} 个 URL）')

# 3. robots.txt
robots = f'''User-agent: *
Allow: /

Sitemap: {DOMAIN}/sitemap.xml
'''
open(os.path.join(SITE, 'robots.txt'), 'w', encoding='utf-8').write(robots)
print('robots.txt 已生成')
