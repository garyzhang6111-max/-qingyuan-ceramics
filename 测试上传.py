#!/usr/bin/env python3
# 上传工艺图到 Shopify 文件库（Files）
import json, os, sys, urllib.request, urllib.error, glob, uuid, time

cfg = json.load(open(os.path.expanduser('~/Library/Preferences/shopify-cli-store-nodejs/config.json')))
TOKEN = None
for v in cfg.values():
    for s in v.get('sessionsByUserId', {}).values():
        if s.get('store') == '40pdrr-d1.myshopify.com':
            TOKEN = s['accessToken']
if not TOKEN:
    print('NO_TOKEN'); sys.exit(1)

API = 'https://40pdrr-d1.myshopify.com/admin/api/2024-10/files.json'

def upload_file(path, alt=''):
    boundary = '----Chaishao' + uuid.uuid4().hex
    with open(path, 'rb') as f:
        filebytes = f.read()
    name = os.path.basename(path)
    parts = []
    parts.append(f'--{boundary}\r\nContent-Disposition: form-data; name="filename"\r\n\r\n{name}\r\n'.encode())
    parts.append(f'--{boundary}\r\nContent-Disposition: form-data; name="alt"\r\n\r\n{alt}\r\n'.encode())
    parts.append(f'--{boundary}\r\nContent-Disposition: form-data; name="file"; filename="{name}"\r\nContent-Type: image/jpeg\r\n\r\n'.encode())
    parts.append(filebytes)
    parts.append(f'\r\n--{boundary}--\r\n'.encode())
    body = b''.join(parts)
    req = urllib.request.Request(API, data=body, method='POST')
    req.add_header('X-Shopify-Access-Token', TOKEN)
    req.add_header('Content-Type', f'multipart/form-data; boundary={boundary}')
    try:
        with urllib.request.urlopen(req) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        return {'error': e.code, 'body': e.read().decode()[:300]}

# 测试一张
test = glob.glob('/Users/zhangge/.openclaw/workspace-personal-assistant/柴烧网站/照片分类-web/工艺图/窑火/*.jpg')[0]
r = upload_file(test, '窑火测试')
print(json.dumps(r, ensure_ascii=False)[:500])
