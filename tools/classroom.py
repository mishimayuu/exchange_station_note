exec(open('tools/lib.py').read())
CAMX, CAM = 0.0, 1.35
XL, XR, H, ZB = -4.0, 4.0, 3.0, 8.5
room(XL, XR, H, ZB)

# 床・天井の線
for X in (-3, -1.5, 0, 1.5, 3):
    line((X, 0, 2.8), (X, 0, ZB), .8, .5)
for Z in [3.4 + 1.2*i for i in range(5)]:
    line((XL, 0, Z), (XR, 0, Z), .8, .5)
for X in (-2, 0, 2): line((X, H, 2.8), (X, H, ZB), .8, .5)

# 左の壁：窓
for z0, z1 in [(3.3, 5.0), (5.3, 7.0), (7.3, 8.3)]:
    quad((XL, .95, z0), (XL, .95, z1), (XL, 2.4, z1), (XL, 2.4, z0), YEL, 2.0)
    line((XL, 1.675, z0), (XL, 1.675, z1), 1.2); line((XL, .95, (z0+z1)/2), (XL, 2.4, (z0+z1)/2), 1.2)
    line((XL, .9, z0-.05), (XL, .9, z1+.05), 2.2)
# 窓の外の桜
random.seed(5) if False else None
import random; random.seed(11)
for _ in range(16):
    x, y = P(XL, random.uniform(1.0, 2.3), random.uniform(5.35, 6.95))
    out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{random.uniform(1.8,3.2):.1f}" fill="{YEL}" stroke="{INK}" stroke-width="1"/>')
line((XL, 1.0, 5.3), (XL, 1.9, 6.4), 1.4)
# カーテン（影色）
path(W((XL, .95, 4.95), (XL, .95, 5.35), (XL, 2.45, 5.35), (XL, 2.45, 4.95)), BLU, 0, True)
path(W((XL, .95, 6.65), (XL, .95, 7.05), (XL, 2.45, 7.05), (XL, 2.45, 6.65)), BLU, 0, True)

# 右の壁：ロッカー
for i in range(6):
    z = 3.4 + .8*i
    quad((3.6, 0, z), (3.6, 0, z+.8), (3.6, 1.8, z+.8), (3.6, 1.8, z), YEL, 1.6)
    line((3.6, .9, z), (3.6, .9, z+.8), 1.0)
    line((3.6, 1.35, z+.12), (3.6, 1.5, z+.12), 1.6)
quad((3.6, 1.8, 3.4), (3.6, 1.8, 8.2), (4.0, 1.8, 8.2), (4.0, 1.8, 3.4), YEL, 1.2) if False else None

# 奥の壁：黒板（影色で塗る）
quad((-2.6, .85, ZB), (1.4, .85, ZB), (1.4, 2.25, ZB), (-2.6, 2.25, ZB), BLU, 2.4)
quad((-2.72, .8, ZB), (1.52, .8, ZB), (1.52, 2.32, ZB), (-2.72, 2.32, ZB), 'none', 1.6)
line((-2.7, .8, ZB-.02), (1.5, .8, ZB-.02), 3.0)
def chalk(pts):
    pp = W(*pts)
    out.append('<path d="M' + ' L'.join(f'{x:.1f} {y:.1f}' for x, y in pp) + f'" fill="none" stroke="{YEL}" stroke-width="1.4" opacity=".9"/>')
chalk([(-2.3, 1.9, ZB), (-1.2, 1.9, ZB)]); chalk([(-2.3, 1.7, ZB), (-.6, 1.7, ZB)]); chalk([(-2.3, 1.5, ZB), (-1.5, 1.5, ZB)])
chalk([(.2, 1.9, ZB), (.9, 1.5, ZB), (.6, 1.2, ZB)])
# 時計
cx, cy = P(2.1, 2.55, ZB); r = .3*F/ZB
out.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="{YEL}" stroke="{INK}" stroke-width="2"/>')
out.append(f'<path d="M{cx:.1f} {cy:.1f} V{cy-r*.7:.1f} M{cx:.1f} {cy:.1f} L{cx+r*.5:.1f} {cy+r*.2:.1f}" stroke="{INK}" stroke-width="1.6" fill="none"/>')
# 扉
quad((2.5, 0, ZB), (3.4, 0, ZB), (3.4, 2.05, ZB), (2.5, 2.05, ZB), YEL, 2.2)
quad((2.65, 1.2, ZB), (3.25, 1.2, ZB), (3.25, 1.85, ZB), (2.65, 1.85, ZB), 'none', 1.4)
# 掲示物
for x0, y0, w_, h_ in [(-3.7, 1.0, .5, .7), (-3.1, 1.2, .5, .6)]:
    quad((x0, y0, ZB), (x0+w_, y0, ZB), (x0+w_, y0+h_, ZB), (x0, y0+h_, ZB), YEL, 1.3)
    line((x0+.08, y0+h_*.7, ZB), (x0+w_-.08, y0+h_*.7, ZB), .9)

# 天井の蛍光灯
for X in (-2, 0, 2):
    for Z in (4.6, 6.8):
        quad((X-.7, H-.02, Z), (X+.7, H-.02, Z), (X+.7, H-.02, Z+.28), (X-.7, H-.02, Z+.28), YEL, 1.4)

# 先生の机
box(-.4, 1.3, 0, .76, 7.3, 7.9, 1.8, BLU)

# 生徒の机と椅子（奥→手前）
def desk(X, Z):
    blue(W((X-.25, 0, Z+.05), (X+.55, 0, Z+.05), (X+.55, 0, Z+.42), (X-.25, 0, Z+.42)))
    for dx in (-.28, .28):
        for dz in (.04, .38):
            line((X+dx, 0, Z+dz), (X+dx, .72, Z+dz), 1.6)
    quad((X-.33, .74, Z), (X+.33, .74, Z), (X+.33, .74, Z+.44), (X-.33, .74, Z+.44), YEL, 1.8)
    quad((X-.33, .70, Z), (X+.33, .70, Z), (X+.33, .74, Z), (X-.33, .74, Z), YEL, 1.6)
    # 椅子
    for dx in (-.2, .2): line((X+dx, 0, Z-.45), (X+dx, .42, Z-.45), 1.5); line((X+dx, 0, Z-.12), (X+dx, .42, Z-.12), 1.3)
    quad((X-.23, .42, Z-.5), (X+.23, .42, Z-.5), (X+.23, .42, Z-.1), (X-.23, .42, Z-.1), YEL, 1.6)
    quad((X-.2, .5, Z-.5), (X+.2, .5, Z-.5), (X+.2, .82, Z-.5), (X-.2, .82, Z-.5), YEL, 1.6)
for Z in (6.6, 5.6, 4.6):
    for X in (-2.4, -.8, .8, 2.4):
        desk(X, Z)
# 机の上の青いノート（主人公の席）
quad((.65, .745, 4.65), (.95, .745, 4.65), (.95, .745, 5.0), (.65, .745, 5.0), YEL, 1.5)
path(W((.65, .745, 4.65), (.95, .745, 4.65), (.95, .745, 5.0), (.65, .745, 5.0)), BLU, 0, True)
path(W((.65, .745, 4.65), (.95, .745, 4.65), (.95, .745, 5.0), (.65, .745, 5.0)), 'none', 1.6, True)

save(sys.argv[1])
