#!/usr/bin/env python3
# 批量创建 Shopify 产品并上传图片
import json, os, sys, base64, urllib.request, urllib.error, glob, time

# 从 CLI 配置读取 token（不打印）
cfg = json.load(open(os.path.expanduser('~/Library/Preferences/shopify-cli-store-nodejs/config.json')))
TOKEN = None
for v in cfg.values():
    sessions = v.get('sessionsByUserId', {})
    for s in sessions.values():
        if s.get('store') == '40pdrr-d1.myshopify.com':
            TOKEN = s['accessToken']
if not TOKEN:
    print('NO_TOKEN'); sys.exit(1)

STORE = '40pdrr-d1.myshopify.com'
API = f'https://{STORE}/admin/api/2024-10'
HEADERS = {'X-Shopify-Access-Token': TOKEN, 'Content-Type': 'application/json'}

BASE = '/Users/zhangge/.openclaw/workspace-personal-assistant/柴烧网站/照片分类-web/产品图'

def api(method, path, payload=None):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(API + path, data=data, headers=HEADERS, method=method)
    try:
        with urllib.request.urlopen(req) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        return {'error': e.code, 'body': e.read().decode()[:500]}

def upload_image(product_id, img_path, position):
    with open(img_path, 'rb') as f:
        b64 = base64.b64encode(f.read()).decode()
    payload = {'image': {'attachment': b64, 'position': position, 'filename': os.path.basename(img_path)}}
    return api('POST', f'/products/{product_id}/images.json', payload)

products = [
    {
        'title': '柴烧台灯 · 窑变暖釉',
        'body_html': '<p>柴烧粗陶灯座，窑火在器身留下的暖黄釉面，透过灯罩晕成一方安静的夜。大师手作，落灰成釉，每一件都独一无二。</p>',
        'vendor': '陈师傅',
        'product_type': '台灯',
        'tags': '台灯, 孤品, 柴烧',
        'price': '385.00',
        'folder': '台灯',
        'sku': 'CS-LAMP-021'
    },
    {
        'title': '柴烧茶具套组 · 大师之作',
        'body_html': '<p>含茶盘、花器与茶杯的完整茶席套组。柴烧自然落灰釉，窑位、火候、灰烬的偶遇，让每一件器物的釉色都不可复制。</p>',
        'vendor': '陈师傅',
        'product_type': '茶器',
        'tags': '茶器, 套组, 孤品, 柴烧',
        'price': '550.00',
        'folder': '茶器',
        'sku': 'CS-TEASET-001'
    },
    {
        'title': '柴烧茶杯 · 青灰窑变',
        'body_html': '<p>柴烧茶杯，青灰窑变釉面，开片纹理自然。一只养出来的茶味，越用越温润。</p>',
        'vendor': '阿明',
        'product_type': '茶杯',
        'tags': '茶器, 茶杯, 柴烧',
        'price': '165.00',
        'folder': '茶杯',
        'sku': 'CS-CUP-063'
    },
    {
        'title': '柴烧杯盘 · 方形系列',
        'body_html': '<p>柴烧方形马克杯与盘托系列，开片纹理与手作痕迹清晰可见。粗陶与窑火的温度，落在日常三餐。</p>',
        'vendor': '阿明',
        'product_type': '杯盘',
        'tags': '餐具, 杯盘, 柴烧',
        'price': '85.00',
        'folder': '杯盘',
        'sku': 'CS-MUG-058'
    },
]

for p in products:
    folder = os.path.join(BASE, p['folder'])
    imgs = sorted(glob.glob(os.path.join(folder, '*.jpg')))
    payload = {
        'product': {
            'title': p['title'],
            'body_html': p['body_html'],
            'vendor': p['vendor'],
            'product_type': p['product_type'],
            'tags': p['tags'],
            'status': 'active',
            'variants': [{'price': p['price'], 'sku': p['sku']}]
        }
    }
    res = api('POST', '/products.json', payload)
    if 'error' in res:
        print(f"FAIL {p['title']}: {res}")
        continue
    pid = res['product']['id']
    print(f"OK {p['title']} (id={pid}, {len(imgs)} 图)")
    for i, img in enumerate(imgs, 1):
        r = upload_image(pid, img, i)
        if 'error' in r:
            print(f"  图{i} FAIL: {r}")
        else:
            print(f"  图{i} OK")
        time.sleep(0.3)

print('DONE')
