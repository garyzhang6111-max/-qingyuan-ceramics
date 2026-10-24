#!/usr/bin/env python3
# 产品孤品化：每件库存=1，售出即无（deny），卖的是真实展示品
import json, os, sys, urllib.request, urllib.error

cfg = json.load(open(os.path.expanduser('~/Library/Preferences/shopify-cli-store-nodejs/config.json')))
TOKEN = ''
for v in cfg.values():
    for s in v.get('sessionsByUserId', {}).values():
        if s.get('store') == '40pdrr-d1.myshopify.com':
            TOKEN = s['accessToken']
if not TOKEN:
    print('NO_TOKEN'); sys.exit(1)

STORE = '40pdrr-d1.myshopify.com'
API = f'https://{STORE}/admin/api/2024-10'
LOCATION_ID = 128259260746

def api(method, path, payload=None):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(API + path, data=data, method=method)
    req.add_header('X-Shopify-Access-Token', TOKEN)
    req.add_header('Content-Type', 'application/json')
    try:
        with urllib.request.urlopen(req) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        return {'error': e.code, 'body': e.read().decode()[:400]}

res = api('GET', '/products.json?limit=20')
products = res.get('products', [])
print(f'共 {len(products)} 个产品\n')

for p in products:
    title = p['title']
    for v in p.get('variants', []):
        vid = v['id']
        iid = v.get('inventory_item_id')
        # 1. 策略：售出即无
        upd = api('PUT', f'/variants/{vid}.json', {
            'variant': {'id': vid, 'inventory_management': 'shopify', 'inventory_policy': 'deny'}
        })
        # 2. 库存数量设为 1
        lv = api('POST', '/inventory_levels/set.json', {
            'location_id': LOCATION_ID, 'inventory_item_id': iid, 'available': 1
        })
        ok = ('error' not in upd) and ('error' not in lv)
        print(f"  {'✓' if ok else '✗'} {title[:24]} | 孤品·库存1·售出即无")

print('\n完成')
