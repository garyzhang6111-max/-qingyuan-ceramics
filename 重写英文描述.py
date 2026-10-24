#!/usr/bin/env python3
"""重写 27 款产品 description_en：地道英文、意译、句式自然。"""
import json

DATA_PATH = '/Users/zhangge/.openclaw/workspace-personal-assistant/柴烧网站/data/products.json'
data = json.load(open(DATA_PATH))

# slug -> 地道英文描述
DESC = {
    # 守光灯具 · 罐形
    'lamp-ivory-gray':    'A wood-fired table lamp on a rounded jar base, glazed in soft ivory and grey-green with a mottled, organic surface.',
    'lamp-blue-gray':     'A wood-fired table lamp on a rounded jar base, finished in a deep blue-grey glaze.',
    'lamp-red-warm':      'A wood-fired table lamp on a rounded jar base, in warm red-brown mottled with cream.',
    'lamp-amber':         'A wood-fired table lamp on a rounded jar base, glazed in a warm amber, wood-toned finish.',
    'lamp-bicolor':       'A wood-fired table lamp on a rounded jar base, split diagonally between black and white.',
    'lamp-bicolor-shade': 'A wood-fired table lamp with a two-tone black-and-white body and a soft cream shade.',
    'lamp-speckle':       'A wood-fired table lamp with a speckled body and a black shade.',
    'lamp-caramel':       'A wood-fired table lamp in a caramel-toned body with a black shade.',
    'lamp-mottled':       'A wood-fired table lamp with a mottled cream, black and brown body and a black shade.',
    'lamp-dark-mini':     'A compact wood-fired table lamp on a dark grey-black round jar.',
    # 守光灯具 · 球形
    'lamp-red-globe':     'A wood-fired table lamp on a globular base, fired to a rich red.',
    'lamp-bicolor-sphere': 'A wood-fired table lamp on a black-and-white sphere, finished with a pale cream shade.',
    'lamp-amber-sphere':  'A wood-fired table lamp on an amber sphere marked by the fire, topped with a black shade.',
    'lamp-crater':        'A wood-fired table lamp with a cratered, volcanic-textured body and a black shade.',
    # 马克杯
    'mug-ribbed-white':   'A ribbed white-glazed mug flecked with iron spots, thrown by hand on the wheel.',
    'mug-blue-ombre':     'A low mug with a blue-to-white ombré glaze.',
    'mug-crackle':        'A crackle-glazed white mug speckled with dark flecks.',
    'mug-threaded':       'A mug with a spiral of throwing lines around its rim.',
    # 茶器
    'tea-fairness-pitcher': 'A white-glazed fairness pitcher with a fine pouring spout.',
    'tea-water-basin':      'A white-glazed water basin speckled with dark flecks.',
    'tea-rimmed-basin':     'A white-glazed basin with a flared rim.',
    'tea-master-cup':       'A waisted master cup speckled across its body.',
    'incense-amber':        'An amber-glazed incense burner with a wide, rounded rim.',
    # 花器
    'vase-ribbed-round':  'A large round-bellied vase with horizontal ribs.',
    'vase-tall-neck':     'A tall-necked vase with a shouldered form and an applied ring.',
    'vase-light-round':   'A pale, small-mouthed round jar.',
    'vase-dark-fire':     'A dark, heavily fire-marked jar with a small mouth.',
}

n = 0
for p in data['products']:
    slug = p['slug']
    if slug in DESC:
        p['description_en'] = DESC[slug]
        n += 1

json.dump(data, open(DATA_PATH, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print(f'已重写 {n} 款产品英文描述')
