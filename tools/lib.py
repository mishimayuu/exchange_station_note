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


def box(x0, x1, y0, y1, z0, z1, sw=1.8, side=None, top=True):
    """直方体。カメラから見える面だけ描く。side=BLU で側面を影色に。"""
    if x1 < CAMX:   quad((x1, y0, z0), (x1, y0, z1), (x1, y1, z1), (x1, y1, z0), side or YEL, sw)
    elif x0 > CAMX: quad((x0, y0, z0), (x0, y0, z1), (x0, y1, z1), (x0, y1, z0), side or YEL, sw)
    if top and y1 < CAM:  quad((x0, y1, z0), (x1, y1, z0), (x1, y1, z1), (x0, y1, z1), YEL, sw)
    elif top and y0 > CAM: quad((x0, y0, z0), (x1, y0, z0), (x1, y0, z1), (x0, y0, z1), YEL, sw)
    quad((x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0), YEL, sw)
    if side == BLU:
        if x1 < CAMX:   path(W((x1, y0, z0), (x1, y0, z1), (x1, y1, z1), (x1, y1, z0)), BLU, 0, True)
        elif x0 > CAMX: path(W((x0, y0, z0), (x0, y0, z1), (x0, y1, z1), (x0, y1, z0)), BLU, 0, True)

def room(xl, xr, H, zb, zn=2.6):
    quad((xl, 0, zb), (xr, 0, zb), (xr, H, zb), (xl, H, zb), YEL, 2.4)
    for x, y in [(xl, 0), (xr, 0), (xl, H), (xr, H)]: line((x, y, zb), (x, y, zn), 2.0)
    # 巾木（はばき）
    for x in (xl, xr): line((x, .12, zb), (x, .12, zn), 1.0, .7)
    line((xl, .12, zb), (xr, .12, zb), 1.0, .7)

def save(path_):
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 600" preserveAspectRatio="xMidYMax slice">
<g stroke-linecap="round" stroke-linejoin="round">
{chr(10).join(out)}
</g></svg>'''
    open(path_, 'w', encoding='utf-8').write(svg)
