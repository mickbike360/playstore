# Icône 512 et images de présentation 1024x500 de Sentier.
# Usage : python3 visuels.py <dossier_sortie> <dossier_polices_roboto>
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
OUT = sys.argv[1]; POL = sys.argv[2]

def police(taille, graisse=b'Bold'):
    f = ImageFont.truetype(POL + '/Roboto-Regular.ttf', taille)
    f.set_variation_by_name(graisse); return f

def degrade(w, h, c1, c2):
    im = Image.new('RGB', (w, h)); px = im.load()
    for y in range(h):
        for x in range(w):
            t = (x / w) * 0.35 + (y / h) * 0.65
            px[x, y] = tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))
    return im

def bezier(p0, p1, p2, p3, n=200):
    pts = []
    for i in range(n + 1):
        t = i / n; u = 1 - t
        pts.append(tuple(u**3 * p0[k] + 3 * u * u * t * p1[k] + 3 * u * t * t * p2[k] + t**3 * p3[k] for k in range(2)))
    return pts

def dense(pts, pas=1.0):
    out = [pts[0]]
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        n = max(1, int(((x1 - x0) ** 2 + (y1 - y0) ** 2) ** 0.5 / pas))
        out += [(x0 + (x1 - x0) * i / n, y0 + (y1 - y0) * i / n) for i in range(1, n + 1)]
    return out

def trait(d, pts, coul, w):
    # Trait rond et lisse : des disques serrés le long de la courbe.
    r = w / 2
    for x, y in dense(pts, max(1.0, w / 8)):
        d.ellipse([x - r, y - r, x + r, y + r], fill=coul)

VERT_FONCE, VERT, OR = (0x1B, 0x5E, 0x4A), (0x2E, 0x7D, 0x63), (0xFF, 0xD1, 0x66)

def dessin_icone(d, ox, oy, s):
    """Le dessin de l'icône de l'appli (viewport 108), (ox, oy) = coin du viewport, s = échelle."""
    P = lambda x, y: (ox + x * s, oy + y * s)
    d.polygon([P(0, 78), P(26, 52), P(44, 68), P(70, 38), P(108, 74), P(108, 108), P(0, 108)], fill=VERT)
    g = lambda x, y: P(20.5 + x * 0.62, 20.5 + y * 0.62)   # groupe réduit de l'avant-plan
    d.polygon([g(54, 14), g(78, 58), g(66, 58), g(54, 36), g(42, 58), g(30, 58)], fill='white')
    pts = bezier(g(22, 90), g(40, 90), g(34, 74), g(52, 74)) + bezier(g(52, 74), g(70, 74), g(64, 62), g(86, 62))[1:]
    trait(d, pts, OR, 7 * 0.62 * s)

# --- Icône 512 : la zone visible de l'icône adaptative (Google arrondit lui-même) ---
K = 4; N = 512 * K
ic = Image.new('RGB', (N, N), VERT_FONCE); d = ImageDraw.Draw(ic)
s = N / 74; dessin_icone(d, -17 * s, -17 * s, s)
ic.resize((512, 512), Image.LANCZOS).save(OUT + '/icone-512.png')

# --- Images de présentation 1024 x 500 ---
TEXTES = {
    'fr': ('Ta randonnée,', 'mesurée juste.', ['Cartes IGN', 'Cardio Bluetooth', 'Météo de montagne', 'Survol 3D']),
    'en': ('Your hikes,', 'measured right.', ['IGN maps', 'Bluetooth heart rate', 'Mountain weather', '3D flyover']),
    'es': ('Tu ruta,', 'bien medida.', ['Mapas IGN', 'Pulso Bluetooth', 'Meteo de montaña', 'Vuelo 3D']),
}
for lang, (l1, l2, puces) in TEXTES.items():
    W, H = 2048, 1000
    im = degrade(W // 8, H // 8, (0x27, 0x8A, 0x6C), (0x0F, 0x3D, 0x30)).resize((W, H), Image.BICUBIC)
    d = ImageDraw.Draw(im)
    # chaînes de montagnes en arrière-plan, de la plus lointaine à la plus proche
    for (pts, coul) in (
        ([(0, 640), (260, 470), (420, 560), (640, 380), (900, 600), (1100, 520), (1300, 640), (2048, 700)], (0x3B, 0x94, 0x75)),
        ([(0, 780), (300, 600), (520, 700), (760, 540), (1050, 760), (2048, 860)], (0x22, 0x68, 0x52)),
        ([(0, 900), (350, 760), (700, 860), (1000, 820), (2048, 980)], (0x1A, 0x55, 0x43)),
    ):
        d.polygon(pts + [(2048, 1000), (0, 1000)], fill=coul)
    # sommet enneigé de la grande montagne
    d.polygon([(640, 380), (705, 432), (672, 455), (640, 425), (604, 458), (580, 424)], fill=(0xF4, 0xF7, 0xF5))
    # le sentier doré qui serpente jusqu'au col, avec une ombre douce
    sentier = (bezier((80, 990), (420, 960), (230, 790), (560, 760)) + bezier((560, 760), (820, 735), (600, 600), (880, 590))[1:]
               + bezier((880, 590), (1000, 585), (950, 520), (1040, 515))[1:])
    om = Image.new('L', (W, H), 0); trait(ImageDraw.Draw(om), [(x + 6, y + 10) for x, y in sentier], 150, 26)
    im.paste((5, 30, 22), (0, 0), om.filter(ImageFilter.GaussianBlur(10)))
    trait(d, sentier, OR, 22)
    # point de départ et repère d'arrivée
    d.ellipse([60, 968, 100, 1008], fill='white')
    d.ellipse([1020, 495, 1060, 535], fill='white'); d.ellipse([1029, 504, 1051, 526], fill=OR)
    # icône de l'appli en médaillon
    m = Image.new('RGB', (230, 230), VERT_FONCE); dm = ImageDraw.Draw(m)
    sm = 230 / 74; dessin_icone(dm, -17 * sm, -17 * sm, sm)
    masque = Image.new('L', (230, 230), 0); ImageDraw.Draw(masque).rounded_rectangle([0, 0, 229, 229], radius=60, fill=255)
    om = Image.new('L', (W, H), 0); ImageDraw.Draw(om).rounded_rectangle([1140, 150, 1370, 380], radius=60, fill=130)
    im.paste((5, 30, 22), (0, 0), om.filter(ImageFilter.GaussianBlur(18)))
    im.paste(m, (1130, 135), masque)
    x = 1130
    d.text((x + 262, 165), 'Sentier', font=police(150, b'Black'), fill='white')
    d.text((x, 420), l1, font=police(70, b'Bold'), fill='white')
    d.text((x, 502), l2, font=police(70, b'Bold'), fill=OR)
    y = 650; xx = x
    for p in puces:
        f = police(36, b'Medium'); tw = d.textlength(p, font=f)
        if xx + tw + 48 > W - 50: xx = x; y += 84
        d.rounded_rectangle([xx, y, xx + tw + 48, y + 64], radius=32, fill='white')
        d.text((xx + 24, y + 11), p, font=f, fill=VERT_FONCE)
        xx += tw + 68
    im.resize((1024, 500), Image.LANCZOS).convert('RGB').save(OUT + f'/presentation-1024x500-{lang}.png')
print('ok')
