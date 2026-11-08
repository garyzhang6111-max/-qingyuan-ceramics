#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""给所有 HTML 页面注入语言防闪脚本：zh 用户加载时先隐藏内容，语言应用后再显示，
避免「先闪英文再切中文」。带 1.2s 兜底：脚本加载失败也自动解除隐藏。"""
import glob

SNIPPET = '''<script>(function(){try{if(localStorage.getItem('qingyuan-lang')==='zh'){document.documentElement.setAttribute('lang','zh');document.documentElement.classList.add('early-zh');setTimeout(function(){document.documentElement.classList.remove('early-zh');},1200);}}catch(e){}})();</script>
<style>html.early-zh body{visibility:hidden}</style>
<noscript><style>html.early-zh body{visibility:visible}</style></noscript>'''

files = sorted(glob.glob('site/*.html') + glob.glob('site/policies/*.html'))
changed = 0
skipped = 0
for f in files:
    s = open(f, encoding='utf-8').read()
    if '</head>' not in s:
        print('跳过（无 </head>）:', f)
        continue
    # 替换旧版注入（若有），否则全新注入
    if 'early-zh' in s:
        import re
        s = re.sub(
            r'<script>\(function\(\)\{try\{if\(localStorage\.getItem\(\'qingyuan-lang\'\)===\'zh\'\).*?</noscript>\n',
            '', s, flags=re.S)
        skipped += 1
    s = s.replace('</head>', SNIPPET + '\n</head>', 1)
    open(f, 'w', encoding='utf-8').write(s)
    changed += 1

print(f'已注入 {changed} 个页面')
