#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""给桌面版页面注入移动端跳转：手机 UA 且未选桌面版 → 跳 mobile.html。
逃生通道：mobile.html「我的 → 切换桌面版」设 qy-desktop=1。mobile.html 本身不注入。"""
import glob, re

SNIPPET = '''<script>(function(){try{if(/Android|iPhone|iPad|iPod|Mobile/i.test(navigator.userAgent)&&!localStorage.getItem('qy-desktop')){location.replace('/mobile.html'+location.search);}}catch(e){}})();</script>'''

files = sorted(glob.glob('site/*.html') + glob.glob('site/policies/*.html'))
changed = 0
for f in files:
    if f.endswith('/mobile.html'):
        print('跳过 mobile.html')
        continue
    s = open(f, encoding='utf-8').read()
    if 'qy-desktop' in s:
        continue
    if '</head>' not in s:
        print('跳过（无 </head>）:', f)
        continue
    s = s.replace('</head>', SNIPPET + '\n</head>', 1)
    open(f, 'w', encoding='utf-8').write(s)
    changed += 1

print(f'已注入 {changed} 个桌面版页面')
