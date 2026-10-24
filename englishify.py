#!/usr/bin/env python3
"""英语主线：把默认显示文本从中文换成英文（data-en 值）。
策略：
- html lang zh->en
- meta description 的 content -> data-en 值
- input/textarea 的 placeholder -> data-en 值
- 纯文本元素（data-en 后紧跟 >）：默认文本 -> data-en 值
- data-en 值含 < 的（crumb 面包屑）：跳过，之后手动处理
"""
import re, glob, os

SITE = '/Users/zhangge/.openclaw/workspace-personal-assistant/柴烧网站/site'

def process(path):
    html = open(path, encoding='utf-8').read()
    orig = html

    # 1. html lang
    html = html.replace('<html lang="zh">', '<html lang="en">')

    # 2. meta description content -> data-en
    def meta(m):
        return f'data-zh="{m.group(1)}" data-en="{m.group(2)}" content="{m.group(2)}"'
    html = re.sub(r'<meta name="description" data-zh="([^"]*)" data-en="([^"]*)" content="[^"]*"', meta, html)

    # 3. placeholder -> data-en（placeholder 在 data-en 之前）
    def ph(m):
        return f'placeholder="{m.group(2)}" data-zh="{m.group(1)}" data-en="{m.group(2)}"'
    html = re.sub(r'placeholder="[^"]*" data-zh="([^"]*)" data-en="([^"]*)"', ph, html)

    # 4. 纯文本元素：data-en 后紧跟 > 的，默认文本 -> data-en
    def txt(m):
        en = m.group(1)
        if '<' in en:          # crumb 含 HTML，跳过
            return m.group(0)
        return f'data-en="{en}">{en}<'
    html = re.sub(r'data-en="([^"]*)"\s*>([^<]*)<', txt, html)

    if html != orig:
        open(path, 'w', encoding='utf-8').write(html)
        return True
    return False

changed = 0
for f in sorted(glob.glob(os.path.join(SITE, '*.html'))):
    if process(f):
        changed += 1
        print('已改:', os.path.basename(f))
print(f'\n共改 {changed} 个文件')
