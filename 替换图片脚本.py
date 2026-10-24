#!/usr/bin/env python3
# 替换产品图片为 1:1 裁切版
import json, os, sys, base64, urllib.request, urllib.error, glob, time

cfg = json.load(open(os.path.expanduser('~/Library/Preferences/shopify-cli-store-nodejs/config.json')))
TOKEN = None
for v in cfg.values():
    for s in v.get('sessionsByUserId', {}).values():
        if s.get('store') == '40pdrr-d1.myshopify.com':
            TOKEN = s['accessToken']
if not TOKEN:
    print('NO_TOKEN'); sys.exit(1)

STORE = '40pdrr-d1.myshopify.com'
API = f'https://{STORE}/admin/api/2024-10'
HEADERS = {'X-Shopify-Access-Token': TOKEN, 'Content-Type': 'application/json'}

BASE = '/Users/zhangge/.openclaw/workspace-personal-assistant/柴烧网站/产品图-11'

def api(method, path, payload=None):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(API + path, data=data, headers=HEADERS, method=method)
    try:
        with urllib.request.urlopen(req) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        return {'error': e.code, 'body': e.read().decode()[:300]}

# 产品 id 与目录映射
products = [
    ('16124247736650', '台灯'),
    ('16124248523082', '茶器'),
    ('16124249145674', '茶杯'),
    ('16124249440586', '杯盘'),
]

for pid, folder in products:
    # 1. 删除旧图
    old = api('GET', f'/products/{pid}/images.json')
    if isinstance(old, dict) and 'images' in old:
        for im in old['images']:
            api('DELETE', f"/products/{pid}/images/{im['id']}.json")
    # 2. 上传新图
    imgs = sorted(glob.glob(os.path.join(BASE, folder, '*.jpg')))
    for i, img in enumerate(imgs, 1):
        with open(img, 'rb') as f:
            b64 = base64.b64encode(f.read()).decode()
        payload = {'image': {'attachment': b64, 'position': i, 'filename': os.path.basename(img)}}
        r = api('POST', f'/products/{pid}/images.json', payload)
        if 'error' in r:
            print(f'{folder} 图{i} FAIL: {r}')
    print(f'{folder} 替换完成：{len(imgs)} 张 1:1')
    time.sleep(0.3)

print('DONE')
