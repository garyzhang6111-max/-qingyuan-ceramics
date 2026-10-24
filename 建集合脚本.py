#!/usr/bin/env python3
# 建「精选孤品」集合并收录全部产品
import json, os, urllib.request, urllib.error

cfg = json.load(open(os.path.expanduser('~/Library/Preferences/shopify-cli-store-nodejs/config.json')))
TOKEN = ''
for v in cfg.values():
    for s in v.get('sessionsByUserId', {}).values():
        if s.get('store') == '40pdrr-d1.myshopify.com':
            TOKEN = s['accessToken']

API = 'https://40pdrr-d1.myshopify.com/admin/api/2024-10'

def api(method, path, payload=None):
    data = json.dumps(payload).encode() if payload else None
    req = urllib.request.Request(API + path, data=data, method=method)
    req.add_header('X-Shopify-Access-Token', TOKEN)
    req.add_header('Content-Type', 'application/json')
    try:
        with urllib.request.urlopen(req) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        return {'error': e.code, 'body': e.read().decode()[:300]}

# 建集合
r = api('POST', '/custom_collections.json', {
    'custom_collection': {'title': '精选孤品', 'handle': 'featured', 'published': True}
})
if 'error' in r:
    print('建集合失败:', r)
else:
    cid = r['custom_collection']['id']
    print('集合已建 id =', cid)
    res = api('GET', '/products.json?limit=20')
    for p in res.get('products', []):
        cr = api('POST', '/collects.json', {'collect': {'product_id': p['id'], 'collection_id': cid}})
        ok = 'error' not in cr
        print('  加入', p['title'][:22], 'OK' if ok else 'FAIL: ' + str(cr)[:100])
