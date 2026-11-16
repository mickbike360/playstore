# Captures Play Store de DictéePS : 1080x1920, titre en haut, écran réel dans un cadre de téléphone.
import sys, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
BR, OUT, POL = sys.argv[1], sys.argv[2], sys.argv[3]
def police(t, g=b'Bold'):
    f = ImageFont.truetype(POL + '/Roboto-Regular.ttf', t); f.set_variation_by_name(g); return f
def degrade(w, h, c1, c2):
    im = Image.new('RGB', (w // 8, h // 8)); px = im.load()
    for y in range(h // 8):
        for x in range(w // 8):
            t = (x / (w / 8)) * 0.35 + (y / (h / 8)) * 0.65
            px[x, y] = tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))
    return im.resize((w, h), Image.BICUBIC)
BLEU1, BLEU2 = (0x42, 0xA5, 0xF5), (0x0D, 0x47, 0xA1)
ECRANS = [  # fichier, (haut, bas) de la zone utile de l'écran 1080x2400
    ('dictee.png', (110, 2270)),
    ('zs1.png', (110, 2270)),
    ('zs3.png', (110, 2270)),
    ('zs5.png', (110, 2270)),
    ('zs7.png', (110, 2270)),
]
TITRES = {
    'fr': [('Tu parles,', 'ça s\'écrit. Partout.'), ('Une bulle micro', 'dans toutes tes applis'),
           ('Prête en quatre étapes,', '100 % hors ligne'), ('Ta bulle,', 'à ton goût'),
           ('Choisis ta', 'reconnaissance vocale')],
    'en': [('Speak,', 'and it\'s written. Anywhere.'), ('A mic bubble', 'in all your apps'),
           ('Ready in four steps,', '100% offline'), ('Your bubble,', 'your way'),
           ('Pick your', 'speech recognition')],
    'es': [('Hablas', 'y se escribe. En cualquier sitio.'), ('Una burbuja de micrófono', 'en todas tus apps'),
           ('Lista en cuatro pasos,', '100 % sin conexión'), ('Tu burbuja,', 'a tu gusto'),
           ('Elige tu', 'reconocimiento de voz')],
}
W, H = 1080, 1920
for lang, titres in TITRES.items():
    os.makedirs(f'{OUT}/{lang}', exist_ok=True)
    for n, ((fich, (h0, h1)), (t1, t2)) in enumerate(zip(ECRANS, titres), 1):
        if not os.path.exists(f'{BR}/{fich}'): continue
        im = degrade(W, H, BLEU1, BLEU2); d = ImageDraw.Draw(im)
        f1, f2 = police(70, b'Black'), police(70, b'Black')
        for y, t, f, c in ((90, t1, f1, (255, 255, 255)), (180, t2, f2, (0xFF, 0xE0, 0x82))):
            while d.textlength(t, font=f) > W - 100: f = police(f.size - 4, b'Black')
            d.text(((W - d.textlength(t, font=f)) / 2, y), t, font=f, fill=c)
        ec = Image.open(f'{BR}/{fich}').convert('RGB').crop((0, h0, 1080, h1))
        lw = 820; lh = int(ec.height * lw / ec.width)
        ec = ec.resize((lw, lh), Image.LANCZOS)
        x0, y0, bord = (W - lw) // 2, 330, 22
        # ombre + cadre de téléphone
        om = Image.new('L', (W, H), 0)
        ImageDraw.Draw(om).rounded_rectangle([x0 - bord + 10, y0 - bord + 24, x0 + lw + bord + 10, y0 + lh + bord + 24], 70, fill=150)
        im.paste((5, 25, 70), (0, 0), om.filter(ImageFilter.GaussianBlur(28)))
        d.rounded_rectangle([x0 - bord, y0 - bord, x0 + lw + bord, y0 + lh + bord], 70, fill=(18, 18, 22))
        masque = Image.new('L', (lw, lh), 0); ImageDraw.Draw(masque).rounded_rectangle([0, 0, lw, lh], 50, fill=255)
        im.paste(ec, (x0, y0), masque)
        im.save(f'{OUT}/{lang}/{n}.png')
print('ok')
