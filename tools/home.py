exec(open('tools/lib.py').read())
import random; random.seed(2)
CAMX, CAM = 0.3, 1.3
XL, XR, H, ZB = -3.2, 3.2, 2.6, 7.5
room(XL, XR, H, ZB)
for X in [-2.6 + .65*i for i in range(10)]: line((X, 0, 2.8), (X, 0, ZB), .8, .45)
# 左の壁：廊下への入口（影色）と額
path(W((XL, 0, 5.9), (XL, 0, 7.2), (XL, 2.05, 7.2), (XL, 2.05, 5.9)), BLU, 0, True)
quad((XL, 0, 5.9), (XL, 0, 7.2), (XL, 2.05, 7.2), (XL, 2.05, 5.9), 'none', 2.0)
for z0, z1, y0, y1 in [(4.4, 4.9, 1.4, 1.9), (4.0, 4.3, 1.1, 1.4)]:
    quad((XL, y0, z0), (XL, y0, z1), (XL, y1, z1), (XL, y1, z0), YEL, 1.5)
# 奥の壁：窓
quad((-2.2, 1.0, ZB), (-.6, 1.0, ZB), (-.6, 2.1, ZB), (-2.2, 2.1, ZB), YEL, 2.2)
line((-1.4, 1.0, ZB), (-1.4, 2.1, ZB), 1.3); line((-2.2, 1.55, ZB), (-.6, 1.55, ZB), 1.3)
line((-2.3, .95, ZB), (-.5, .95, ZB), 2.6)
for _ in range(12):
    x, y = P(random.uniform(-2.1, -.7), random.uniform(1.05, 2.0), ZB)
    out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{random.uniform(1.6,2.8):.1f}" fill="{YEL}" stroke="{INK}" stroke-width=".9"/>')
for x0, x1 in [(-2.45, -2.1), (-.7, -.35)]:
    path(W((x0, .95, ZB), (x1, .95, ZB), (x1, 2.25, ZB), (x0, 2.25, ZB)), BLU, 0, True)
# 時計
cx, cy = P(.6, 2.15, ZB); r = .22*F/ZB
out.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="{YEL}" stroke="{INK}" stroke-width="1.8"/><path d="M{cx:.1f} {cy:.1f} V{cy-r*.7:.1f} M{cx:.1f} {cy:.1f} L{cx+r*.5:.1f} {cy+r*.1:.1f}" stroke="{INK}" stroke-width="1.4" fill="none"/>')
# 冷蔵庫
blue(W((2.6, 0, 7.0), (3.6, 0, 7.0), (3.6, 0, 7.5), (2.6, 0, 7.5))) if False else None
box(1.7, 2.6, 0, 1.85, 6.9, 7.5, 2.0, BLU)
line((1.7, 1.2, 6.9), (2.6, 1.2, 6.9), 1.4)
line((2.5, 1.3, 6.9), (2.5, 1.7, 6.9), 2.2); line((2.5, .75, 6.9), (2.5, 1.1, 6.9), 2.2)
# 猫のメモ（冷蔵庫の扉）
quad((1.88, 1.42, 6.9), (2.24, 1.42, 6.9), (2.24, 1.78, 6.9), (1.88, 1.78, 6.9), YEL, 1.4)
cx, cy = P(2.06, 1.58, 6.9); k = F/6.9
out.append(f'<path d="M{cx-.05*k:.1f} {cy:.1f} q-.02 {-.07*k:.1f} .05 {-.08*k:.1f} q.07 .0 .05 {.08*k:.1f} z" fill="none" stroke="{INK}" stroke-width="1"/>'.replace('.05','%.1f'%(.05*k),0))
out.append(f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{.07*k:.1f}" ry="{.055*k:.1f}" fill="none" stroke="{INK}" stroke-width="1"/><path d="M{cx-.05*k:.1f} {cy-.04*k:.1f} l{-.01*k:.1f} {-.05*k:.1f} l{.04*k:.1f} {.03*k:.1f} M{cx+.02*k:.1f} {cy-.05*k:.1f} l{.03*k:.1f} {-.04*k:.1f} l{.01*k:.1f} {.06*k:.1f} M{cx+.07*k:.1f} {cy+.02*k:.1f} q{.06*k:.1f} {.02*k:.1f} {.03*k:.1f} {-.07*k:.1f}" fill="none" stroke="{INK}" stroke-width="1"/>')
out.append(f'<circle cx="{cx+.13*k:.1f}" cy="{cy-.1*k:.1f}" r="2.5" fill="{BLU}"/>')
# 右の壁：カウンターと吊り戸棚
box(2.6, 3.2, 0, .9, 3.8, 6.9, 2.0, None)
for i in range(4):
    z = 3.9 + .75*i; line((2.6, 0, z), (2.6, .9, z), 1.2)
    line((2.6, .55, z+.3), (2.6, .7, z+.3), 1.6)
box(2.85, 3.2, 1.6, 2.3, 3.8, 6.9, 1.8, None)
# コンロと鍋
x0, y0 = P(2.9, .92, 5.6); k = F/5.6
out.append(f'<ellipse cx="{x0:.1f}" cy="{y0:.1f}" rx="{.3*k:.1f}" ry="{.07*k:.1f}" fill="{YEL}" stroke="{INK}" stroke-width="1.4"/>')
path([(x0-.16*k, y0-.02*k), (x0-.17*k, y0-.2*k), (x0+.17*k, y0-.2*k), (x0+.16*k, y0-.02*k)], YEL, 1.8, True, curve='round', r=4)
line_ = lambda a, b: out.append(f'<path d="M{a[0]:.1f} {a[1]:.1f} L{b[0]:.1f} {b[1]:.1f}" stroke="{INK}" stroke-width="1.6"/>')
line_((x0-.17*k, y0-.2*k), (x0+.17*k, y0-.2*k))
out.append(f'<path d="M{x0-.07*k:.1f} {y0-.24*k:.1f} q{-.05*k:.1f} {-.1*k:.1f} 0 {-.18*k:.1f} q{.05*k:.1f} {-.08*k:.1f} 0 {-.16*k:.1f} M{x0+.07*k:.1f} {y0-.24*k:.1f} q{.05*k:.1f} {-.1*k:.1f} 0 {-.18*k:.1f} q{-.05*k:.1f} {-.08*k:.1f} 0 {-.16*k:.1f}" fill="none" stroke="{INK}" stroke-width="1.2"/>')

# 床のラグと影
quad((-1.9, 0, 3.4), (1.3, 0, 3.4), (1.3, 0, 6.4), (-1.9, 0, 6.4), YEL, 1.6)
quad((-1.7, 0, 3.6), (1.1, 0, 3.6), (1.1, 0, 6.2), (-1.7, 0, 6.2), 'none', 1.0)
blue(W((-1.0, 0, 4.4), (.9, 0, 4.4), (.9, 0, 5.6), (-1.0, 0, 5.6)))
blue(W((1.7, 0, 6.9), (3.2, 0, 6.9), (3.2, 0, 7.5), (1.7, 0, 7.5)))
# 奥の椅子
def chair_far(X, Z):
    for dx in (-.2, .2): line((X+dx, 0, Z), (X+dx, .45, Z), 1.6); line((X+dx, 0, Z+.4), (X+dx, .45, Z+.4), 1.5)
    quad((X-.22, .46, Z), (X+.22, .46, Z), (X+.22, .46, Z+.42), (X-.22, .46, Z+.42), YEL, 1.8)
    for dx in (-.2, .2): line((X+dx, .46, Z+.42), (X+dx, .95, Z+.42), 1.8)
    quad((X-.22, .72, Z+.42), (X+.22, .72, Z+.42), (X+.22, .92, Z+.42), (X-.22, .92, Z+.42), YEL, 1.6)
chair_far(-.4, 5.75)
# テーブル
for X, Z in [(-1.1, 4.3), (.45, 4.3), (-1.1, 5.3), (.45, 5.3)]: line((X, 0, Z), (X, .74, Z), 2.0)
quad((-1.25, .76, 4.15), (.6, .76, 4.15), (.6, .76, 5.45), (-1.25, .76, 5.45), YEL, 2.2)
quad((-1.25, .72, 4.15), (.6, .72, 4.15), (.6, .76, 4.15), (-1.25, .76, 4.15), YEL, 1.8)
# 食器
for X, Z in [(-.7, 4.5), (.1, 4.5), (-.3, 5.0)]:
    a = P(X, .77, Z); k = F/Z
    out.append(f'<ellipse cx="{a[0]:.1f}" cy="{a[1]:.1f}" rx="{.14*k:.1f}" ry="{.04*k:.1f}" fill="{YEL}" stroke="{INK}" stroke-width="1.3"/>')
m = P(-.3, .79, 4.9); k = F/4.9
out.append(f'<path d="M{m[0]-.05*k:.1f} {m[1]:.1f} v{-.1*k:.1f} h{.1*k:.1f} v{.1*k:.1f} z" fill="{YEL}" stroke="{INK}" stroke-width="1.3"/>')
chair_far(.15, 5.75)
# 観葉植物
px_, py_ = P(-2.7, 0, 5.2); k = F/5.2
path([(px_-.16*k, py_-.34*k), (px_+.16*k, py_-.34*k), (px_+.12*k, py_), (px_-.12*k, py_)], YEL, 1.8, True, curve='round', r=4)
for dx, dy, ex, ey in [(-.02, -.34, -.32, -.75), (0, -.34, .02, -.95), (.02, -.34, .34, -.7), (-.02, -.34, -.18, -.9), (.02, -.34, .2, -.88)]:
    out.append(f'<path d="M{px_+dx*k:.1f} {py_+dy*k:.1f} Q{px_+(dx+ex)*k/2-.08*k:.1f} {py_+(dy+ey)*k/2:.1f} {px_+ex*k:.1f} {py_+ey*k:.1f} Q{px_+(dx+ex)*k/2+.08*k:.1f} {py_+(dy+ey)*k/2:.1f} {px_+dx*k:.1f} {py_+dy*k:.1f}z" fill="{YEL}" stroke="{INK}" stroke-width="1.4"/>')
# ペンダントライト
line((-.3, H, 4.8), (-.3, 1.95, 4.8), 1.4)
p1 = P(-.36, 1.95, 4.8); p2 = P(-.24, 1.95, 4.8); p3 = P(-.03, 1.62, 4.8); p4 = P(-.57, 1.62, 4.8)
path([p1, p2, p3, p4], YEL, 2.0, True, curve='round', r=4)
path([p1, p2, p3, P(-.3, 1.62, 4.8)], BLU, 0, True)
save(sys.argv[1])
