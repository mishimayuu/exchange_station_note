# 田舎の駅前。python3 tools/ekimae.py out.svg sakura
exec(open('tools/lib.py').read())
CAMX, CAM = 0.4, 1.5
# ---- 遠くの山 ----
def mount(pts, fill=YEL): path(pts, fill, 1.8, True, curve='smooth')
mount([(-60, 252), (80, 190), (210, 150), (330, 196), (430, 250)])
blue([(210, 150), (330, 196), (430, 250), (300, 252), (250, 190)])
mount([(300, 252), (470, 205), (620, 160), (760, 215), (880, 252)])
blue([(620, 160), (760, 215), (880, 252), (730, 253), (680, 200)])
# 雲
for cx, cy, s in ((150, 70, 1.0), (560, 45, 1.3), (700, 120, .8)):
    path([(cx-60*s, cy+14*s), (cx-40*s, cy-6*s), (cx-8*s, cy-18*s), (cx+26*s, cy-8*s), (cx+58*s, cy+2*s), (cx+48*s, cy+16*s)], YEL, 1.6, True, curve='smooth')
# ---- 地面：道路の縁 ----
Z0, Z1 = 2.4, 40
for X in (-3.2, 3.4): line((X, 0, Z0), (X, 0, Z1), 1.8)
for X in (-3.5, 3.7): line((X, 0, Z0), (X, 0, Z1), 1.0, .6)
z = 3.0
while z < 24:                                   # 中央線（破線）
    line((0, 0, z), (0, 0, z+.9), 1.6); z += 2.2
blue(W((-9, 0, 2.4), (-3.5, 0, 2.4), (-3.5, 0, 40), (-9, 0, 40)))
# ---- 駅舎 ----
Zs = 14.0
xa, xb = -1.8, 4.6
quad((xa, 0, Zs), (xb, 0, Zs), (xb, 3.0, Zs), (xa, 3.0, Zs), YEL, 2.4)
quad((xa-.5, 3.0, Zs), (xb+.5, 3.0, Zs), (xb-.4, 4.2, Zs), (xa+.4, 4.2, Zs), YEL, 2.4)   # 屋根
for i in range(1, 6):
    t = i/6; line((xa-.5+.5*t*0+(xb-xa+1)*t, 3.0, Zs), (xa+.4+(xb-xa-.8)*t, 4.2, Zs), .9, .6)
line((xa-.5, 3.0, Zs), (xb+.5, 3.0, Zs), 2.8)
blue(W((xa-.5, 2.9, Zs), (xb+.5, 2.9, Zs), (xb+.5, 3.0, Zs), (xa-.5, 3.0, Zs)))
# 看板
quad((.2, 2.35, Zs), (3.0, 2.35, Zs), (3.0, 2.85, Zs), (.2, 2.85, Zs), YEL, 2.0)
sx, sy = P(1.6, 2.5, Zs); k = F/Zs
out.append(f'<text x="{sx:.1f}" y="{sy:.1f}" text-anchor="middle" font-family="Hiragino Mincho ProN,serif" font-size="{.34*k:.1f}" font-weight="700" fill="{INK}" letter-spacing="3">大野七尾駅</text>')
# ガラス戸
quad((.5, 0, Zs), (2.7, 0, Zs), (2.7, 2.2, Zs), (.5, 2.2, Zs), YEL, 2.2)
line((1.6, 0, Zs), (1.6, 2.2, Zs), 1.8); line((.5, 1.0, Zs), (2.7, 1.0, Zs), 1.0)
blue(W((.58, .05, Zs), (1.0, .05, Zs), (1.5, 2.15, Zs), (.58, 2.15, Zs)))
# 窓
for x0 in (-1.4, 3.3):
    quad((x0, .8, Zs), (x0+1.0, .8, Zs), (x0+1.0, 2.1, Zs), (x0, 2.1, Zs), YEL, 1.8)
    line((x0+.5, .8, Zs), (x0+.5, 2.1, Zs), 1.2)
# 自転車置き場の屋根と自転車
for X in (-1.2, 0.0): line((X, 0, 10.8), (X, 1.7, 10.8), 1.8)
quad((-1.5, 1.7, 10.8), (0.3, 1.7, 10.8), (0.3, 1.8, 10.8), (-1.5, 1.8, 10.8), YEL, 1.8)
bx, by = P(-.6, 0, 10.8); k = F/10.8
for dx in (-.28, .28):
    out.append(f'<circle cx="{bx+dx*k:.1f}" cy="{by-.28*k:.1f}" r="{.28*k:.1f}" fill="none" stroke="{INK}" stroke-width="1.6"/>')
out.append(f'<path d="M{bx-.28*k:.1f} {by-.28*k:.1f} L{bx-.05*k:.1f} {by-.62*k:.1f} L{bx+.28*k:.1f} {by-.28*k:.1f} M{bx-.05*k:.1f} {by-.62*k:.1f} L{bx+.2*k:.1f} {by-.68*k:.1f}" stroke="{INK}" stroke-width="1.6" fill="none"/>')
# 木（右奥）
def tree(X, Z, s=1.0):
    tx, ty = P(X, 0, Z); k = F/Z*s
    out.append(f'<path d="M{tx-.1*k:.1f} {ty:.1f} q{.03*k:.1f} {-.8*k:.1f} {.02*k:.1f} {-1.3*k:.1f} h{.18*k:.1f} q{-.02*k:.1f} {.5*k:.1f} {.05*k:.1f} {1.3*k:.1f}z" fill="{YEL}" stroke="{INK}" stroke-width="1.6"/>')
    pts = []
    for i in range(0, 361, 10):
        t = math.radians(i); r_ = 1.0*k*(1+.09*math.sin(5*t)); pts.append((tx+r_*math.cos(t), ty-1.9*k+r_*.8*math.sin(t)))
    path(pts, YEL, 1.8, True, curve='smooth')
    path([(tx+.05*k, ty-1.15*k), (tx+.8*k, ty-1.5*k), (tx+.85*k, ty-2.2*k), (tx+.4*k, ty-2.6*k), (tx+.35*k, ty-1.9*k)], BLU, 0, True, curve='smooth')
tree(6.0, 12, 1.0); tree(-5.0, 17, .9); tree(9.5, 22, .9); tree(-9, 11, 1.1)
# ---- 電柱 ----
polesX = -2.6
zs_ = [4.4, 7.5, 12.5, 20]
for z in zs_:
    line((polesX, 0, z), (polesX, 7.2, z), 2.2)
    line((polesX-.6, 6.6, z), (polesX+.6, 6.6, z), 1.8); line((polesX-.5, 6.1, z), (polesX+.5, 6.1, z), 1.4)
for a_, b_ in zip(zs_, zs_[1:]):
    for dx, y in ((-.6, 6.6), (.6, 6.6), (-.5, 6.1), (.5, 6.1)):
        line((polesX+dx, y-.12, a_), (polesX+dx, y-.12, b_), .9, .7)
# ---- 通行人2人（後ろ姿・駅へ向かう） ----
def person(X, Z, fill, step):
    px, py = P(X, 0, Z); k = F/Z
    for dx, dz in ((-.07, step), (.07, -step)):
        out.append(f'<path d="M{px+dx*k:.1f} {py-.82*k:.1f} L{px+(dx+dz*.5)*k:.1f} {py:.1f}" stroke="{INK}" stroke-width="2" fill="none"/>')
    out.append(f'<path d="M{px-.17*k:.1f} {py-.82*k:.1f} q{-.02*k:.1f} {-.42*k:.1f} {.03*k:.1f} {-.62*k:.1f} q{.14*k:.1f} {-.06*k:.1f} {.28*k:.1f} 0 q{.05*k:.1f} {.2*k:.1f} {.03*k:.1f} {.62*k:.1f}z" fill="{fill}" stroke="{INK}" stroke-width="1.8" stroke-linejoin="round"/>')
    out.append(f'<circle cx="{px:.1f}" cy="{py-1.62*k:.1f}" r="{.11*k:.1f}" fill="{INK}" stroke="{INK}" stroke-width="1.4"/>')
person(-.9, 6.6, YEL, .08)
person(-1.6, 5.6, BLU, -.08)
save(sys.argv[1])
