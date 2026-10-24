#!/usr/bin/env python3
# 上传工艺图到 Shopify 文件库（修复版：fileCreate 只取 id，URL 最后统一查）
import json, os, sys, urllib.request, urllib.error, glob, time

cfg = json.load(open(os.path.expanduser('~/Library/Preferences/shopify-cli-store-nodejs/config.json')))
TOKEN = None
for v in cfg.values():
    for s in v.get('sessionsByUserId', {}).values():
        if s.get('store') == '40pdrr-d1.myshopify.com':
            TOKEN = s['accessToken']
if not TOKEN:
    print('NO_TOKEN'); sys.exit(1)

STORE = '40pdrr-d1.myshopify.com'
GQL = f'https://{STORE}/admin/api/2024-10/graphql.json'

def graphql(query, variables=None):
    payload = {'query': query}
    if variables:
        payload['variables'] = variables
    req = urllib.request.Request(GQL, data=json.dumps(payload).encode(), method='POST')
    req.add_header('X-Shopify-Access-Token', TOKEN)
    req.add_header('Content-Type', 'application/json')
    try:
        with urllib.request.urlopen(req) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        return {'errors': [{'message': e.read().decode()[:300]}]}

BASE = '/Users/zhangge/.openclaw/workspace-personal-assistant/柴烧网站/照片分类-web/工艺图'
OUT = '/Users/zhangge/.openclaw/workspace-personal-assistant/柴烧网站/工艺图清单.json'

CATEGORY_MAP = {'窑火': 'kiln-fire', '装窑坯体': 'loading', '手作施釉': 'glazing', '窑炉柴堆': 'kiln'}

# 已传文件（跳过：文件名以 627 开头的窑火图已经传过）
SKIP_PREFIX = ('627',)

files = []
for cat, slug in CATEGORY_MAP.items():
    d = os.path.join(BASE, cat)
    for f in sorted(glob.glob(os.path.join(d, '*.jpg'))):
        base = os.path.basename(f)
        if base.startswith(SKIP_PREFIX):
            print(f'跳过已传: {cat}/{base}')
            continue
        files.append((f, cat, slug))

print(f'待上传 {len(files)} 张工艺图')

uploaded = []  # [(filename, cat, slug, file_gid)]

for idx, (fpath, cat, slug) in enumerate(files, 1):
    name = os.path.basename(fpath)
    size = os.path.getsize(fpath)
    # 1. stagedUploadsCreate（input 是列表）
    q = '''
    mutation staged($input: [StagedUploadInput!]!) {
      stagedUploadsCreate(input: $input) {
        stagedTargets { url resourceUrl parameters { name value } }
        userErrors { field message }
      }
    }'''
    v = {'input': [{'resource': 'FILE', 'filename': name, 'mimeType': 'image/jpeg',
                    'fileSize': str(size), 'httpMethod': 'POST'}]}
    r = graphql(q, v)
    if 'errors' in r or not r.get('data', {}).get('stagedUploadsCreate', {}).get('stagedTargets'):
        print(f'[{idx}] {name} staged FAIL: {r}')
        continue
    t = r['data']['stagedUploadsCreate']['stagedTargets'][0]
    # 2. 上传文件到 staged URL
    boundary = '----Chaishao' + str(idx)
    with open(fpath, 'rb') as fh:
        fbytes = fh.read()
    parts = []
    for p in t['parameters']:
        parts.append(f'--{boundary}\r\nContent-Disposition: form-data; name="{p["name"]}"\r\n\r\n{p["value"]}\r\n'.encode())
    parts.append(f'--{boundary}\r\nContent-Disposition: form-data; name="file"; filename="{name}"\r\nContent-Type: image/jpeg\r\n\r\n'.encode())
    parts.append(fbytes)
    parts.append(f'\r\n--{boundary}--\r\n'.encode())
    body = b''.join(parts)
    req = urllib.request.Request(t['url'], data=body, method='POST')
    req.add_header('Content-Type', f'multipart/form-data; boundary={boundary}')
    try:
        with urllib.request.urlopen(req) as up:
            up.read()
    except urllib.error.HTTPError as e:
        print(f'[{idx}] {name} upload FAIL: {e.code}')
        continue
    # 3. fileCreate（只取 id + alt）
    q2 = '''
    mutation fc($files: [FileCreateInput!]!) {
      fileCreate(files: $files) {
        files { id alt }
        userErrors { field message }
      }
    }'''
    v2 = {'files': [{'originalSource': t['resourceUrl'], 'contentType': 'IMAGE', 'alt': f'{cat}-{slug}'}]}
    r2 = graphql(q2, v2)
    files_created = r2.get('data', {}).get('fileCreate', {}).get('files', [])
    if files_created:
        fid = files_created[0]['id']
        uploaded.append({'file': name, 'category': cat, 'slug': slug, 'gid': fid})
        print(f'[{idx}/{len(files)}] {cat}/{name} OK')
    else:
        print(f'[{idx}] {name} fileCreate FAIL: {r2}')
    time.sleep(0.2)

# 4. 统一查 URL（此时图片已处理完）
print(f'\n共上传 {len(uploaded)} 张，统一查 URL ...')
final = []
for u in uploaded:
    q3 = 'query($id: ID!) { file(id: $id) { alt preview { image { url } } } }'
    r3 = graphql(q3, {'id': u['gid']})
    f = r3.get('data', {}).get('file', {})
    url = ''
    try:
        url = f['preview']['image']['url']
    except (KeyError, TypeError):
        pass
    final.append({'file': u['file'], 'category': u['category'], 'slug': u['slug'], 'url': url, 'alt': u['category'] + '-' + u['slug']})
    if url:
        print(f"  {u['category']}/{u['file']}: {url[:70]}")
    time.sleep(0.1)

json.dump(final, open(OUT, 'w'), ensure_ascii=False, indent=2)
print(f'完成 {len(final)} 张，清单写入 {OUT}')
