exec(open('tools/lib.py').read())
import random; random.seed(4)
CAMX, CAM = 0.0, 1.4
XL, XR, H, ZB = -2.8, 2.8, 2.7, 6.2
room(XL, XR, H, ZB)
for X in [-2.4 + .6*i for i in range(9)]: line((X, 0, 2.8), (X, 0, ZB), .8, .45)
# 窓口（外に桜）
wx0, wx1, wy0, wy1 = -1.5, 1.1, 1.0, 2.0
quad((wx0, wy0, ZB), (wx1, wy0, ZB), (wx1, wy1, ZB), (wx0, wy1, ZB), YEL, 2.6)
a, b, c, d = W((wx0, wy0, ZB), (wx1, wy0, ZB), (wx1, wy1, ZB), (wx0, wy1, ZB))
out.append(f'<clipPath id="win"><path d="M{a[0]:.1f} {a[1]:.1f} L{b[0]:.1f} {b[1]:.1f} L{c[0]:.1f} {c[1]:.1f} L{d[0]:.1f} {d[1]:.1f}z"/></clipPath><g clip-path="url(#win)">')
tx, ty = P(.1, .9, ZB); k = F/ZB
out.append(f'<path d="M{tx-.12*k:.1f} {ty+.4*k:.1f} q{.04*k:.1f} {-.5*k:.1f} {.03*k:.1f} {-.8*k:.1f} h{.18*k:.1f} q{-.02*k:.1f} {.3*k:.1f} {.05*k:.1f} {.8*k:.1f}" fill="{YEL}" stroke="{INK}" stroke-width="1.4"/>')
pts = []
for i in range(0, 361, 8):
    t = math.radians(i); r_ = .62*k*(1+.1*math.sin(6*t)); pts.append((tx+.05*k + r_*math.cos(t), ty-.55*k + r_*.85*math.sin(t)))
path(pts, YEL, 1.8, True, curve='smooth')
for _ in range(24):
    out.append(f'<circle cx="{tx+random.uniform(-.45,.5)*k:.1f}" cy="{ty-.55*k+random.uniform(-.4,.4)*k:.1f}" r="2.2" fill="{YEL}" stroke="{INK}" stroke-width=".9"/>')
out.append(f'<path d="M{a[0]:.1f} {a[1]+(d[1]-a[1])*0+(c[1]-b[1])*0:.1f}" fill="none"/>')
out.append('</g>')
line(((wx0+wx1)/2, wy0, ZB), ((wx0+wx1)/2, wy1, ZB), 1.6)
quad((wx0-.08, wy0-.08, ZB), (wx1+.08, wy0-.08, ZB), (wx1+.08, wy1+.08, ZB), (wx0-.08, wy1+.08, ZB), 'none', 1.8)
# 時計・カレンダー
cx, cy = P(1.8, 2.25, ZB); r = .24*F/ZB
out.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="{YEL}" stroke="{INK}" stroke-width="1.8"/><path d="M{cx:.1f} {cy:.1f} V{cy-r*.7:.1f} M{cx:.1f} {cy:.1f} L{cx+r*.55:.1f} {cy+r*.15:.1f}" stroke="{INK}" stroke-width="1.4" fill="none"/>')
quad((-2.4, 1.3, ZB), (-1.9, 1.3, ZB), (-1.9, 2.0, ZB), (-2.4, 2.0, ZB), YEL, 1.4)
line((-2.4, 1.85, ZB), (-1.9, 1.85, ZB), 1.0)
# 窓口カウンター
box(-1.7, 1.3, 0, .95, 5.5, 6.2, 2.0, None)
line((-1.7, .5, 5.5), (1.3, .5, 5.5), 1.0, .7)
# 左：書類棚
box(-2.8, -2.3, 0, 2.1, 3.0, 5.6, 2.0, BLU) if False else None
quad((-2.3, 0, 3.0), (-2.3, 0, 5.6), (-2.3, 2.1, 5.6), (-2.3, 2.1, 3.0), YEL, 2.2)
for Y in (.5, 1.0, 1.55): line((-2.3, Y, 3.0), (-2.3, Y, 5.6), 1.6)
random.seed(9)
for Y0 in (.5, 1.0, 1.55, 2.1)[:3]:
    z = 3.1
    while z < 5.45:
        w = random.uniform(.12, .22); h = random.uniform(.28, .44)
        quad((-2.3, Y0, z), (-2.3, Y0, z+w), (-2.3, Y0+h, z+w), (-2.3, Y0+h, z), YEL, 1.1)
        z += w + .03
# 右：時刻表と制帽
quad((2.8, 1.25, 3.6), (2.8, 1.25, 5.0), (2.8, 2.15, 5.0), (2.8, 2.15, 3.6), YEL, 1.8)
for i in range(1, 5): line((2.8, 1.25+.18*i, 3.65), (2.8, 1.25+.18*i, 4.95), .9)
line((2.8, 1.25, 4.3), (2.8, 2.15, 4.3), .9)
hat = [P(2.78, 1.9, 5.45), P(2.78, 1.9, 5.85), P(2.78, 1.75, 5.9), P(2.78, 1.75, 5.4)]
path(hat, YEL, 1.8, True, curve='round', r=4); path(W((2.78, 1.75, 5.35), (2.78, 1.75, 5.95)), 'none', 2.4)
# 右：ストーブとやかん
box(2.0, 2.8, 0, .8, 3.6, 4.8, 2.0, BLU)
kx, ky = P(2.4, .8, 4.2); k = F/4.2
path([(kx-.14*k, ky), (kx-.15*k, ky-.16*k), (kx-.06*k, ky-.26*k), (kx+.06*k, ky-.26*k), (kx+.15*k, ky-.16*k), (kx+.14*k, ky)], YEL, 1.8, True, curve='round', r=5)
path([(kx+.15*k, ky-.15*k), (kx+.26*k, ky-.2*k)], 'none', 2.0)
# ベンチなしの机
blue(W((.5, 0, 4.0), (1.4, 0, 4.0), (1.4, 0, 4.7), (.5, 0, 4.7)))
box(-1.0, .5, 0, .76, 4.0, 4.7, 2.2, None)
line((-1.0, .5, 4.0), (.5, .5, 4.0), 1.0); line((-.25, 0, 4.0), (-.25, .5, 4.0), 1.0)
line((-.6, .62, 4.0), (-.4, .62, 4.0), 1.8); line((.0, .62, 4.0), (.2, .62, 4.0), 1.8)
# 机の上：ペン立て（万年筆）、書類、卓上ライト
quad((-.9, .77, 4.1), (-.5, .77, 4.1), (-.5, .77, 4.55), (-.9, .77, 4.55), YEL, 1.4)
quad((-.8, .775, 4.15), (-.45, .775, 4.15), (-.45, .775, 4.6), (-.8, .775, 4.6), YEL, 1.2)
px, py = P(.2, .77, 4.3); k = F/4.3
path([(px-.06*k, py), (px-.065*k, py-.12*k), (px+.065*k, py-.12*k), (px+.06*k, py)], YEL, 1.6, True, curve='round', r=2)
out.append(f'<path d="M{px-.01*k:.1f} {py-.12*k:.1f} L{px+.02*k:.1f} {py-.3*k:.1f} M{px+.02*k:.1f} {py-.12*k:.1f} L{px+.05*k:.1f} {py-.27*k:.1f}" stroke="{INK}" stroke-width="1.8" fill="none"/><path d="M{px+.02*k:.1f} {py-.3*k:.1f} l.8 -5" stroke="{BLU}" stroke-width="3" fill="none"/>')
lx, ly = P(-.2, .77, 4.6)
out.append(f'<path d="M{lx:.1f} {ly:.1f} l8 0 M{lx+4:.1f} {ly:.1f} l-6 -30 l18 -10" stroke="{INK}" stroke-width="1.8" fill="none"/>')
path([(lx+10, ly-44), (lx+30, ly-36), (lx+22, ly-26), (lx+6, ly-34)], YEL, 1.6, True, curve='round', r=3)
# 椅子
for dx in (-.2, .2): line((-.25+dx, 0, 3.5), (-.25+dx, .46, 3.5), 1.8)
quad((-.5, .46, 3.5), (0, .46, 3.5), (0, .46, 3.95), (-.5, .46, 3.95), YEL, 1.8)
quad((-.48, .5, 3.5), (-.02, .5, 3.5), (-.02, .95, 3.5), (-.48, .95, 3.5), YEL, 1.8)
# 天井ランプ
line((0, H, 4.8), (0, 2.25, 4.8), 1.4)
p1 = P(-.08, 2.25, 4.8); p2 = P(.08, 2.25, 4.8); p3 = P(.35, 1.95, 4.8); p4 = P(-.35, 1.95, 4.8)
path([p1, p2, p3, p4], YEL, 2.0, True, curve='round', r=4); path([p1, p2, p3, P(0, 1.95, 4.8)], BLU, 0, True)
save(sys.argv[1])
