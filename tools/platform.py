import math, sys
VPX, VPY, F, CAM = 400, 250, 600, 1.5
CAMX = 1.2
PAL = {'yellow': ('#1c1c1c', '#f8e98c', '#3a7fb0'), 'sakura': ('#262033', '#f6e2da', '#4d5b98')}
INK, YEL, BLU = PAL[sys.argv[2] if len(sys.argv) > 2 else 'sakura']
def P(X, Y, Z): return (VPX + (X-CAMX)*F/Z, VPY - (Y-CAM)*F/Z)
out = []
def _rd(pts, r, closed):
    n = len(pts)
    def mv(a, b, d):
        L = math.hypot(b[0]-a[0], b[1]-a[1]) or 1
        k = min(d, L/2)/L
        return (a[0]+(b[0]-a[0])*k, a[1]+(b[1]-a[1])*k)
    if closed:
        d = ''
        for i in range(n):
            p0, v, p1 = pts[i-1], pts[i], pts[(i+1) % n]
            a, b = mv(v, p0, r), mv(v, p1, r)
            d += (f'M{a[0]:.1f} {a[1]:.1f}' if i == 0 else f'L{a[0]:.1f} {a[1]:.1f}') + f'Q{v[0]:.1f} {v[1]:.1f} {b[0]:.1f} {b[1]:.1f}'
        return d + 'z'
    d = f'M{pts[0][0]:.1f} {pts[0][1]:.1f}'
    for i in range(1, n-1):
        p0, v, p1 = pts[i-1], pts[i], pts[i+1]
        a, b = mv(v, p0, r), mv(v, p1, r)
        d += f'L{a[0]:.1f} {a[1]:.1f}Q{v[0]:.1f} {v[1]:.1f} {b[0]:.1f} {b[1]:.1f}'
    return d + f'L{pts[-1][0]:.1f} {pts[-1][1]:.1f}'
def _cr(pts, closed):
    n = len(pts); g = lambda i: pts[i % n] if closed else pts[max(0, min(n-1, i))]
    d = f'M{pts[0][0]:.1f} {pts[0][1]:.1f}'
    for i in range(n if closed else n-1):
        p0, p1, p2, p3 = g(i-1), g(i), g(i+1), g(i+2)
        c1 = (p1[0]+(p2[0]-p0[0])/6, p1[1]+(p2[1]-p0[1])/6); c2 = (p2[0]-(p3[0]-p1[0])/6, p2[1]-(p3[1]-p1[1])/6)
        d += f'C{c1[0]:.1f} {c1[1]:.1f} {c2[0]:.1f} {c2[1]:.1f} {p2[0]:.1f} {p2[1]:.1f}'
    return d + ('z' if closed else '')
def path(pts, fill='none', sw=1.8, close=False, op=None, curve=None, r=5):
    if curve == 'round': d = _rd(pts, r, close)
    elif curve == 'smooth': d = _cr(pts, close)
    else: d = 'M' + ' L'.join(f'{x:.1f} {y:.1f}' for x, y in pts) + ('z' if close else '')
    s = f'<path d="{d}" fill="{fill}" stroke="{"none" if fill==BLU else INK}" stroke-width="{sw}"'
    if op: s += f' opacity="{op}"'
    out.append(s + '/>')
def W(*pts): return [P(*p) for p in pts]
def quad(a, b, c, d, fill=YEL, sw=1.8): path(W(a, b, c, d), fill, sw, True)
_n = [0]
def line(a, b, sw=1.4, op=None):
    (x0, y0), (x1, y1) = W(a, b)
    L = math.hypot(x1-x0, y1-y0)
    if L < 70: path([(x0, y0), (x1, y1)], 'none', sw, False, op); return
    _n[0] += 1; k = (1 if _n[0] % 2 else -1) * min(L*.006, 2.2)
    mx, my = (x0+x1)/2 + (y0-y1)/L*k, (y0+y1)/2 + (x1-x0)/L*k
    s_ = f'<path d="M{x0:.1f} {y0:.1f} Q{mx:.1f} {my:.1f} {x1:.1f} {y1:.1f}" fill="none" stroke="{INK}" stroke-width="{sw}"'
    out.append(s_ + (f' opacity="{op}"' if op else '') + '/>')
def blue(pts): path(pts, BLU, 0, True)

# ---- 遠景 ----
# 雲
for cx, cy, s in [(90, 62, 1.0), (205, 100, .7)]:
    path([(cx-60*s, cy), (cx-48*s, cy-16*s), (cx-22*s, cy-22*s), (cx-2*s, cy-34*s), (cx+26*s, cy-24*s),
          (cx+50*s, cy-26*s), (cx+66*s, cy-8*s), (cx+60*s, cy)], 'none', 1.4, True, curve='smooth')
# 山の稜線
hill = [(x, 236 - 10*math.sin(x/90) - 6*math.sin(x/37+1)) for x in range(-10, 830, 10)]
path(hill + [(830, 252), (-10, 252)], YEL, 1.4, True)
# 遠くの家並み
import random; random.seed(3)
x = 0
while x < 800:
    w = random.randint(16, 30); h = random.randint(9, 18); by = 250
    path([(x, by), (x, by-h), (x+w/2, by-h-7), (x+w, by-h), (x+w, by)], YEL, 1.1, True, curve='round', r=1.8)
    if random.random() < .6: path([(x+w*.3, by), (x+w*.3, by-h*.5), (x+w*.6, by-h*.5), (x+w*.6, by)], 'none', .9)
    x += w + random.randint(2, 14)

# 電柱と電線
poles = [(-7.8, 11), (-7.8, 19), (-7.8, 29), (-7.8, 44)]
tops = []
for X, Z in poles:
    line((X, -1.1, Z), (X, 5.2, Z), 2.0 if Z < 20 else 1.4)
    line((X-.9, 4.7, Z), (X+.9, 4.7, Z), 1.6 if Z < 20 else 1.1)
    tops.append(Z)
for off in (-.8, 0, .8):
    pts = []
    zs = [11, 19, 29, 44, 70]
    for a, b in zip(zs, zs[1:]):
        pa, pb = P(-7.8+off, 4.7, a), P(-7.8+off, 4.7, b)
        mx, my = (pa[0]+pb[0])/2, (pa[1]+pb[1])/2 + 6*(11/a)
        pts.append(f'M{pa[0]:.1f} {pa[1]:.1f} Q{mx:.1f} {my:.1f} {pb[0]:.1f} {pb[1]:.1f}')
    out.append(f'<path d="{" ".join(pts)}" fill="none" stroke="{INK}" stroke-width="1"/>')

# ---- 線路 ----
for Z in [3.6 + .8*i for i in range(34)]:
    line((-4.5, -1.1, Z), (-7.3, -1.1, Z), 1.3 if Z < 14 else .9)
for X in (-5.2, -6.64):
    line((X, -1.1, 3.4), (X, -1.1, 90), 2.0)
    line((X, -1.02, 3.4), (X, -1.02, 90), 1.0)
# 線路の向こうのフェンス
for Z in [5 + 2.5*i for i in range(30)]:
    line((-9.5, -1.1, Z), (-9.5, 0.1, Z), 1.4 if Z < 25 else 1)
line((-9.5, 0.1, 5), (-9.5, 0.1, 90), 1.3); line((-9.5, -.5, 5), (-9.5, -.5, 90), 1.0)
# 向こう側の木立（青い影のシルエット）
for cx, r in [(30, 28), (110, 20), (520, 24), (610, 18), (720, 26), (780, 20)]:
    pts = [(cx + r*math.cos(t)*(1+.15*math.sin(5*t)), 246 - r*0.8*abs(math.sin(t))*(1+.12*math.sin(7*t))) for t in [i*math.pi/18 for i in range(19)]]
    path(pts + [(cx+r, 250), (cx-r, 250)], YEL, 1.2, True, curve='round', r=7)

# ---- ホームの床 ----
edge = W((-2.4, 0, 90), (-2.4, 0, 3.0))
path(edge + [(-60, 720), (900, 720), (900, 360), P(8, 0, 90)], YEL, 0, True)
path(edge, 'none', 2.8)
line((8, 0, 90), (8, 0, 9.3), 1.5)
# 点字ブロック
line((-2.05, 0, 90), (-2.05, 0, 3.0), 1.2)
for Z in [3.2 + .55*i for i in range(32)]:
    path(W((-2.3, 0, Z), (-1.8, 0, Z), (-1.8, 0, Z+.22), (-2.3, 0, Z+.22)), 'none', 1.0 if Z < 15 else .7, True)
# 床の目地
for Z in [3.5 + 2.2*i for i in range(30)]:
    line((-1.7, 0, Z), (8, 0, Z), .8, .6)
for X in (1.4, 4.6):
    line((X, 0, 3.0), (X, 0, 60), .8, .6)

# ---- 桜の木（屋根より奥）----
tZ = 11.0; tX = 4.0
b0 = P(tX, 0, tZ); sc = F/tZ
trunk = [(b0[0]-.38*sc, b0[1]), (b0[0]-.24*sc, b0[1]-1.0*sc), (b0[0]-.26*sc, b0[1]-2.3*sc), (b0[0]+.26*sc, b0[1]-2.3*sc), (b0[0]+.24*sc, b0[1]-1.0*sc), (b0[0]+.38*sc, b0[1])]
cc = (b0[0]+.1*sc, b0[1]-3.5*sc); R = 2.1*sc
def blob(c, R, k=0.0):
    pts = []
    for i in range(0, 361, 4):
        t = math.radians(i)
        r = R*(1 + .10*math.sin(6*t+k) + .05*math.sin(11*t+2*k))
        pts.append((c[0]+r*math.cos(t), c[1]+r*math.sin(t)*.92))
    return pts
path(trunk, YEL, 2.4, True, curve='round', r=22)
path([(b0[0]+.02*sc, b0[1]), (b0[0]+.01*sc, b0[1]-1.0*sc), (b0[0]+.0*sc, b0[1]-2.3*sc), (b0[0]+.26*sc, b0[1]-2.3*sc), (b0[0]+.24*sc, b0[1]-1.0*sc), (b0[0]+.38*sc, b0[1])], BLU, 0, True, curve='round', r=22)
# 枝
for a, b in [((0,-1.9),(-0.9,-2.8)), ((0,-2.0),(0.9,-2.9)), ((0,-2.1),(0,-3.0))]:
    path([(b0[0]+a[0]*sc, b0[1]+a[1]*sc), (b0[0]+b[0]*sc, b0[1]+b[1]*sc)], 'none', 1.6)
crown = blob(cc, R)
path(crown, YEL, 2.4, True)
# 影（三日月）
low = [(cc[0]+R*(1+.10*math.sin(6*math.radians(i)))*math.cos(math.radians(i)), cc[1]+R*(1+.10*math.sin(6*math.radians(i)))*math.sin(math.radians(i))*.92) for i in range(10, 171, 4)]
inner = [(cc[0]+(R*.94)*math.cos(math.radians(i)), cc[1]-.12*R+(R*.9)*math.sin(math.radians(i))*.92) for i in range(170, 9, -4)]
blue(low + inner)
random.seed(7)
for _ in range(34):
    a = random.uniform(0, 2*math.pi); d = random.uniform(.1, .82)*R
    x, y = cc[0]+d*math.cos(a), cc[1]+d*math.sin(a)*.8
    r = random.uniform(2.5, 4.5)
    out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{YEL}" stroke="{INK}" stroke-width="1.1"/>')
for _ in range(7):   # 舞う花びら
    x, y = random.uniform(430, 790), random.uniform(190, 400)
    out.append(f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="4" ry="2.3" transform="rotate({random.randint(-40,40)} {x:.1f} {y:.1f})" fill="{YEL}" stroke="{INK}" stroke-width="1"/>')
# 木陰（地面）
blue(W((tX-1.0, 0, tZ-1.2), (tX+3.0, 0, tZ-1.2), (tX+3.0, 0, tZ+1.2), (tX-1.0, 0, tZ+1.2)))
# 地面の花びら
for _ in range(14):
    X, Z = random.uniform(2.2, 7), random.uniform(7, 13)
    x, y = P(X, 0, Z); out.append(f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="3" ry="1.4" fill="{YEL}" stroke="{INK}" stroke-width=".9"/>')

# ---- 屋根（キャノピー）----
RX0, RX1, RZ0, RZ1, RY = -2.0, 1.8, 3.0, 8.5, 3.4
quad((RX0, RY, RZ1), (RX1, RY, RZ1), (RX1, RY, RZ0), (RX0, RY, RZ0), YEL, 2.4)
for X in (-0.9, 0.2, 1.3):
    line((X, RY, RZ1), (X, RY, RZ0), 1.2, .8)
for Z in (4.2, 5.6, 7.0):
    line((RX0, RY, Z), (RX1, RY, Z), 1.2, .8)
quad((RX0, RY, RZ1), (RX1, RY, RZ1), (RX1, RY+.35, RZ1), (RX0, RY+.35, RZ1), YEL, 2.4)
quad((RX0, RY, RZ1), (RX0, RY+.35, RZ1), (RX0, RY+.35, RZ0), (RX0, RY, RZ0), YEL, 2.0)
quad((RX1, RY, RZ1), (RX1, RY+.35, RZ1), (RX1, RY+.35, RZ0), (RX1, RY, RZ0), YEL, 2.0)

# ---- 柱 ----
def post(X, Z, w=.17):
    x0, x1 = X-w/2, X+w/2
    quad((x0, 0, Z), (x1, 0, Z), (x1, RY, Z), (x0, RY, Z), YEL, 2.0)
    path(W((x1, 0, Z), (x1, RY, Z), (x1, RY, Z+w), (x1, 0, Z+w)), BLU, 0, True) if X < 1 else path(W((x0, 0, Z), (x0, RY, Z), (x0, RY, Z+w), (x0, 0, Z+w)), BLU, 0, True)
for Z in (8.2, 5.4):
    for X in (-1.8, 1.8):
        blue(W((X+.08, 0, Z), (X+1.5, 0, Z), (X+1.5, 0, Z+.17), (X+.08, 0, Z+.17)))
    post(-1.8, Z); post(1.8, Z)
# 時刻表（右奥の柱）
quad((-1.55, 1.3, 8.18), (-1.0, 1.3, 8.18), (-1.0, 2.2, 8.18), (-1.55, 2.2, 8.18), YEL, 1.6)
for Y in (1.6, 1.9): line((-1.55, Y, 8.16), (-1.0, Y, 8.16), .9)
line((-1.27, 1.3, 8.16), (-1.27, 2.2, 8.16), .9)

# ---- 駅名看板 ----
SZ = 6.0
for X in (-.3, .9): line((X, RY, SZ), (X, 2.95, SZ), 1.4)
quad((-.5, 2.35, SZ), (1.1, 2.35, SZ), (1.1, 2.95, SZ), (-.5, 2.95, SZ), YEL, 2.2)
tx, ty = P(.3, 2.5, SZ)
out.append(f'<text x="{tx:.1f}" y="{ty:.1f}" text-anchor="middle" font-family="Zen Maru Gothic, Hiragino Maru Gothic ProN, sans-serif" font-size="{.36*F/SZ:.0f}" font-weight="700" fill="{INK}">あさなぎ</text>')

# ---- ベンチ ----
bx0, bx1, bz0, bz1 = 2.7, 3.35, 6.0, 8.0
sy, by_ = .46, 1.0
blue(W((bx0, 0, bz0), (bx1+1.0, 0, bz0), (bx1+1.0, 0, bz1), (bx0, 0, bz1)))
# 背もたれ
quad((bx1, sy, bz1), (bx1, by_, bz1), (bx1, by_, bz0), (bx1, sy, bz0), YEL, 2.0)
for Y in (.62, .78): line((bx1, Y, bz0), (bx1, Y, bz1), 1.2)
# 脚（奥側）
for Z in (bz0+.12, bz1-.12): line((bx1-.08, 0, Z), (bx1-.08, sy, Z), 2.0)
# 座面
quad((bx0, sy, bz1), (bx1, sy, bz1), (bx1, sy, bz0), (bx0, sy, bz0), YEL, 2.2)
quad((bx0, sy, bz0), (bx0, sy, bz1), (bx0, sy-.06, bz1), (bx0, sy-.06, bz0), YEL, 2.0)
for Z in (bz0+.12, bz1-.12): quad((bx0+.06, 0, Z), (bx0+.1, 0, Z), (bx0+.1, sy-.06, Z), (bx0+.06, sy-.06, Z), YEL, 1.8)
# 座面の板目
for X in (bx0+.22, bx0+.43): line((X, sy, bz0), (X, sy, bz1), 1.0)

# ---- ベンチの下の青いノート ----
nx, nz = 2.95, 6.5
quad((nx, 0.005, nz), (nx+.34, 0.005, nz), (nx+.34, 0.005, nz+.26), (nx, 0.005, nz+.26), YEL, 1.5)
path(W((nx, 0.005, nz), (nx+.34, 0.005, nz), (nx+.34, 0.005, nz+.26), (nx, 0.005, nz+.26)), BLU, 0, True)
path(W((nx, 0.005, nz), (nx+.34, 0.005, nz), (nx+.34, 0.005, nz+.26), (nx, 0.005, nz+.26)), 'none', 1.6, True)
line((nx+.04, 0.006, nz), (nx+.04, 0.006, nz+.26), 1.0)

# ---- 猫 ----
cx0, cy0 = P(0.1, 0, 4.4); s = 1.9
def C(pts): return [(cx0+x*s, cy0+y*s) for x, y in pts]
tail = C([(14, -2), (24, -4), (30, -14), (24, -22), (18, -20), (22, -15), (20, -9), (12, -6)])
path(tail, YEL, 1.8, True, curve='round', r=6)
body = C([(-12, 0), (-13, -10), (-9, -22), (-4, -26), (4, -26), (9, -20), (12, -8), (14, 0)])
path(body, YEL, 2.0, True, curve='round', r=9)
head = C([(-9, -27), (-9.5, -33), (-6.5, -40), (-2.5, -35), (2.5, -35), (6.5, -40), (9.5, -33), (9, -27), (6, -23), (0, -21.5), (-6, -23)])
path(head, YEL, 2.0, True, curve='round', r=5)
path(C([(-3, -29), (-3, -28.5)]), 'none', 2.4); path(C([(3, -29), (3, -28.5)]), 'none', 2.4)
path(C([(-5, 0), (-5, -9)]), 'none', 1.2); path(C([(3, 0), (3, -9)]), 'none', 1.2)
blue([(cx0-6*s, cy0), (cx0+26*s, cy0), (cx0+34*s, cy0+3*s), (cx0-2*s, cy0+3*s)])

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 600" preserveAspectRatio="xMidYMax slice">
<g stroke-linecap="round" stroke-linejoin="round">
{chr(10).join(out)}
</g></svg>'''
open(sys.argv[1], 'w', encoding='utf-8').write(svg)
