# Icône 512 et images de présentation 1024x500 de DictéePS.
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
OUT = sys.argv[1]; POL = sys.argv[2]
def police(taille, graisse=b'Bold'):
    f = ImageFont.truetype(POL + '/Roboto-Regular.ttf', taille)
    f.set_variation_by_name(graisse); return f

def degrade(w, h, c1, c2, diag=True):
    im = Image.new('RGB', (w, h)); px = im.load()
    for y in range(h):
        for x in range(w):
            t = ((x / w) * 0.6 + (y / h) * 0.4) if diag else y / h
            px[x, y] = tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))
    return im

def micro(d, cx, cy, s, coul=(255, 255, 255)):
    # Même dessin que l'icône de l'appli (viewport 24) ; (cx, cy) = centre visuel du micro.
    ox, oy = cx - 12 * s, cy - 11.7 * s
    P = lambda x, y: (ox + x * s, oy + y * s)
    d.rounded_rectangle([P(10, 4.5), P(14, 13.5)], radius=2 * s, fill=coul)
    w = max(1, int(1.4 * s))
    d.arc([P(7.6, 6.8), P(16.4, 15.6)], 0, 180, fill=coul, width=w)
    d.line([P(12, 15.6), P(12, 18.2)], fill=coul, width=w)
    d.line([P(9.6, 18.2), P(14.4, 18.2)], fill=coul, width=w)
    for x, y in (P(9.6, 18.2), P(14.4, 18.2), P(8.3, 11.2), P(15.7, 11.2)):
        d.ellipse([x - w / 2, y - w / 2, x + w / 2, y + w / 2], fill=coul)

BLEU1, BLEU2 = (0x42, 0xA5, 0xF5), (0x15, 0x65, 0xC0)

# --- Icône 512 (carré plein : Google arrondit lui-même les coins) ---
K = 4; N = 512 * K
ic = degrade(N // 8, N // 8, BLEU1, BLEU2).resize((N, N), Image.BICUBIC)
d = ImageDraw.Draw(ic)
micro(d, N / 2, N / 2 + 6 * K, 21.5 * K)
ic.resize((512, 512), Image.LANCZOS).save(OUT + '/icone-512.png')

# --- Images de présentation 1024 x 500 ---
TEXTES = {
    'fr': ('Tu parles, ça s\'écrit.', 'Partout.', ['100 % hors ligne', 'Garde ton clavier', 'Sans abonnement']),
    'en': ('Speak, and it\'s written.', 'Anywhere.', ['100% offline', 'Keep your keyboard', 'No subscription']),
    'es': ('Hablas y se escribe.', 'En cualquier sitio.', ['100 % sin conexión', 'Conserva tu teclado', 'Sin suscripción']),
}
for lang, (l1, l2, puces) in TEXTES.items():
    W, H = 1024 * 2, 500 * 2
    im = degrade(W // 8, H // 8, BLEU1, BLEU2).resize((W, H), Image.BICUBIC)
    # halo doux derrière la bulle
    halo = Image.new('L', (W, H), 0); ImageDraw.Draw(halo).ellipse([120, 180, 820, 880], fill=90)
    halo = halo.filter(ImageFilter.GaussianBlur(90))
    im.paste((255, 255, 255), (0, 0), halo)
    d = ImageDraw.Draw(im)
    # bulle micro (comme dans l'appli) avec une ombre
    cx, cy, r = 470, 530, 250
    om = Image.new('L', (W, H), 0); ImageDraw.Draw(om).ellipse([cx - r + 10, cy - r + 30, cx + r + 10, cy + r + 30], fill=120)
    im.paste((10, 40, 90), (0, 0), om.filter(ImageFilter.GaussianBlur(30)))
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 255, 255))
    d.ellipse([cx - r + 26, cy - r + 26, cx + r - 26, cy + r - 26], fill=(0x1E, 0x88, 0xE5))
    micro(d, cx, cy + 8, 17)
    # ondes de voix
    for i, a in enumerate((70, 50, 30)):
        rr = r + 60 + i * 55
        d.arc([cx - rr, cy - rr, cx + rr, cy + rr], -40, 40, fill=(255, 255, 255, 255), width=14 - i * 3)
    x = 1060
    d.text((x, 190), 'DictéePS', font=police(150, b'Black'), fill='white')
    d.text((x, 400), l1, font=police(66, b'Bold'), fill='white')
    d.text((x, 480), l2, font=police(66, b'Bold'), fill=(0xFF, 0xE0, 0x82))
    y = 640; xx = x
    for p in puces:
        f = police(38, b'Medium'); tw = d.textlength(p, font=f)
        if xx + tw + 60 > W - 40: xx = x; y += 86
        d.rounded_rectangle([xx, y, xx + tw + 48, y + 66], radius=33, fill=(255, 255, 255))
        d.text((xx + 24, y + 12), p, font=f, fill=(0x15, 0x65, 0xC0))
        xx += tw + 70
    im.resize((1024, 500), Image.LANCZOS).convert('RGB').save(OUT + f'/presentation-1024x500-{lang}.png')
print('ok')
