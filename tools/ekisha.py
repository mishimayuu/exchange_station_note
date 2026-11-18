# 駅舎の内部。python3 tools/ekisha.py out.svg sakura [empty|sit|hand]
#   empty = 無人 / sit = 女性がベンチに座り、壁にノート / hand = 女性が座り、壁のノートはない
exec(open('tools/lib.py').read())
VAR = sys.argv[3] if len(sys.argv) > 3 else 'empty'
CAMX, CAM = 0.8, 1.4
XL, XR, H, ZB = -1.6, 2.8, 2.9, 6.6
room(XL, XR, H, ZB)
for X in [-1.2 + .6*i for i in range(7)]: line((X, 0, 2.8), (X, 0, ZB), .8, .45)
for Z in (3.4, 4.2, 5.0, 5.8): line((XL, 0, Z), (XR, 0, Z), .8, .4)

# ---- 奥の壁：窓口（駅員） ----
wx0, wx1, wy0, wy1 = -1.3, .1, 1.0, 1.95
quad((wx0, wy0, ZB), (wx1, wy0, ZB), (wx1, wy1, ZB), (wx0, wy1, ZB), YEL, 2.6)
# 駅員（ガラスの向こうに立っている）
hx, hy = P(-.6, 1.55, ZB); k = F/ZB
out.append(f'<path d="M{hx-.38*k:.1f} {hy+.62*k:.1f} q0 {-.5*k:.1f} {.38*k:.1f} {-.5*k:.1f} q{.38*k:.1f} 0 {.38*k:.1f} {.5*k:.1f}z" fill="{BLU}"/>')
out.append(f'<circle cx="{hx:.1f}" cy="{hy:.1f}" r="{.15*k:.1f}" fill="{YEL}" stroke="{INK}" stroke-width="1.6"/>')
out.append(f'<path d="M{hx-.17*k:.1f} {hy-.04*k:.1f} q{.17*k:.1f} {-.2*k:.1f} {.34*k:.1f} 0 v{-.07*k:.1f} q{-.17*k:.1f} {-.1*k:.1f} {-.34*k:.1f} 0z" fill="{BLU}" stroke="{INK}" stroke-width="1.4"/>')
# ガラスの桟
line(((wx0+wx1)/2, wy0, ZB), ((wx0+wx1)/2, wy1, ZB), 1.6)
quad((wx0-.08, wy0-.08, ZB), (wx1+.08, wy0-.08, ZB), (wx1+.08, wy1+.08, ZB), (wx0-.08, wy1+.08, ZB), 'none', 1.8)
box(-1.45, .35, 0, .95, 5.9, 6.6, 2.0, None)
line((-1.45, .5, 5.9), (.35, .5, 5.9), 1.0, .7)
# 切符売り場の小窓
quad((-.9, .98, 5.9), (-.4, .98, 5.9), (-.4, 1.02, 5.9), (-.9, 1.02, 5.9), YEL, 1.2)

# ---- 電光掲示板（窓口の上） ----
bx0, bx1, by0, by1 = -1.4, .2, 2.15, 2.65
(bxa, bya), (bxb, byb) = P(bx0, by1, ZB), P(bx1, by0, ZB)
out.append(f'<rect x="{bxa:.1f}" y="{bya:.1f}" width="{bxb-bxa:.1f}" height="{byb-bya:.1f}" rx="4" fill="{INK}" stroke="{INK}" stroke-width="2"/>')
fs = (byb-bya)*.55
out.append(f'<text x="{bxa+8:.1f}" y="{bya+(byb-bya)*.7:.1f}" font-family="monospace,sans-serif" font-size="{fs:.1f}" font-weight="700" fill="{YEL}" letter-spacing="1">18:50</text>')
out.append(f'<text x="{bxa+(bxb-bxa)*.72:.1f}" y="{bya+(byb-bya)*.66:.1f}" font-family="sans-serif" font-size="{fs*.42:.1f}" fill="{YEL}">普通</text>')
line((-1.2, H, ZB), (-1.2, by1, ZB), 1.2); line((0, H, ZB), (0, by1, ZB), 1.2)

# ---- 奥の壁：アナログ時計（6:30） ----
cx, cy = P(1.5, 2.15, ZB); r = .36*F/ZB
out.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="{YEL}" stroke="{INK}" stroke-width="2.4"/>')
for t in range(12):
    a_ = math.radians(t*30); L = .13 if t % 3 == 0 else .07
    out.append(f'<path d="M{cx+math.sin(a_)*r*.9:.1f} {cy-math.cos(a_)*r*.9:.1f} L{cx+math.sin(a_)*r*(.9-L*2):.1f} {cy-math.cos(a_)*r*(.9-L*2):.1f}" stroke="{INK}" stroke-width="1.4"/>')
for ang, ln, w in ((195, .5, 2.6), (180, .78, 1.8)):
    a_ = math.radians(ang)
    out.append(f'<path d="M{cx:.1f} {cy:.1f} L{cx+math.sin(a_)*r*ln:.1f} {cy-math.cos(a_)*r*ln:.1f}" stroke="{INK}" stroke-width="{w}"/>')
out.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="2.4" fill="{INK}"/>')
# 時刻表
quad((.55, 1.1, ZB), (1.25, 1.1, ZB), (1.25, 1.7, ZB), (.55, 1.7, ZB), YEL, 1.6)
for i in range(1, 4): line((.6, 1.1+.15*i, ZB), (1.2, 1.1+.15*i, ZB), .9)
# 掲示ポスター
quad((1.9, 1.0, ZB), (2.6, 1.0, ZB), (2.6, 1.65, ZB), (1.9, 1.65, ZB), YEL, 1.4)
quad((1.98, 1.08, ZB), (2.52, 1.08, ZB), (2.52, 1.4, ZB), (1.98, 1.08+.32, ZB), BLU, 0)

# ---- 左の壁：出入口（ガラス戸） ----
for z0, z1 in ((3.2, 4.1), (4.2, 5.1)):
    quad((XL, 0, z0), (XL, 0, z1), (XL, 2.0, z1), (XL, 2.0, z0), YEL, 2.0)
    line((XL, .9, z0), (XL, .9, z1), 1.0); line((XL, 1.5, z0), (XL, 1.5, z1), 1.0)
blue(W((XL, 0, 3.2), (XL, 0, 5.1), (XL, 2.0, 5.1), (XL, 2.0, 3.2))) if False else None
# 床の光
blue(W((-1.55, 0, 3.0), (-.8, 0, 3.0), (-.4, 0, 5.3), (-1.55, 0, 5.3)))

# ---- 右の壁：ベンチ ----
bz0, bz1 = 3.5, 5.0
box(XR-.55, XR, 0, .42, bz0, bz1, 2.0, BLU)             # 座面
quad((XR-.04, .42, bz0), (XR-.04, .42, bz1), (XR-.04, .95, bz1), (XR-.04, .95, bz0), YEL, 1.8)  # 背もたれ
for z in (bz0+.05, bz1-.05): line((XR-.5, 0, z), (XR-.5, .42, z), 1.8)
# ベンチの足元の影
blue(W((XR-.7, 0, bz0), (XR-.2, 0, bz0-.15), (XR-.2, 0, bz1+.2), (XR-.7, 0, bz1+.1)))

# ---- 壁のノート ----
if VAR == 'sit':
    nz0, nz1, ny0, ny1 = 5.2, 5.65, 1.15, 1.55
    quad((XR, ny0, nz0), (XR, ny0, nz1), (XR, ny1, nz1), (XR, ny1, nz0), YEL, 2.0)
    quad((XR, ny0+.05, nz0+.05), (XR, ny0+.05, nz1-.05), (XR, ny0+.2, nz1-.05), (XR, ny0+.2, nz0+.05), BLU, 0)
    line((XR, ny1, (nz0+nz1)/2), (XR, ny1+.18, (nz0+nz1)/2), 1.2)
    px, py = P(XR, ny1+.18, (nz0+nz1)/2)
    out.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="2.6" fill="{INK}"/>')

# ---- 座っている女性 ----
if VAR in ('sit', 'hand'):
    sx, sy = P(XR-.32, .42, 4.25); k = F/4.25
    # 脚（ベンチから床へ。画面左向き）
    out.append(f'<path d="M{sx+.04*k:.1f} {sy-.02*k:.1f} L{sx-.38*k:.1f} {sy-.02*k:.1f} L{sx-.4*k:.1f} {sy+.41*k:.1f} L{sx-.28*k:.1f} {sy+.41*k:.1f} L{sx-.27*k:.1f} {sy+.1*k:.1f} L{sx+.04*k:.1f} {sy+.1*k:.1f}z" fill="{YEL}" stroke="{INK}" stroke-width="1.8" stroke-linejoin="round"/>')
    out.append(f'<path d="M{sx-.4*k:.1f} {sy+.41*k:.1f} l-.1 0 q-.04 .06 .0 .06 l{.16*k:.1f} 0z" fill="{INK}" stroke="{INK}" stroke-width="3"/>')
    # 胴（ワンピース）
    out.append(f'<path d="M{sx-.17*k:.1f} {sy-.02*k:.1f} q{-.03*k:.1f} {-.35*k:.1f} {.03*k:.1f} {-.56*k:.1f} q{.15*k:.1f} {-.07*k:.1f} {.3*k:.1f} 0 q{.06*k:.1f} {.2*k:.1f} {.04*k:.1f} {.58*k:.1f}z" fill="{YEL}" stroke="{INK}" stroke-width="1.8" stroke-linejoin="round"/>')
    out.append(f'<path d="M{sx+.02*k:.1f} {sy-.58*k:.1f} q{.12*k:.1f} {.02*k:.1f} {.14*k:.1f} {.0*k:.1f} q{.06*k:.1f} {.2*k:.1f} {.04*k:.1f} {.58*k:.1f} h{-.18*k:.1f}z" fill="{BLU}"/>')
    # 腕と手（膝の上に）
    out.append(f'<path d="M{sx-.1*k:.1f} {sy-.5*k:.1f} q{-.1*k:.1f} {.2*k:.1f} {-.2*k:.1f} {.44*k:.1f}" fill="none" stroke="{INK}" stroke-width="1.8"/>')
    # 頭と髪（ボブ）
    hx, hy = sx-.01*k, sy-.7*k
    out.append(f'<circle cx="{hx:.1f}" cy="{hy:.1f}" r="{.11*k:.1f}" fill="{YEL}" stroke="{INK}" stroke-width="1.8"/>')
    out.append(f'<path d="M{hx-.12*k:.1f} {hy+.05*k:.1f} q{-.02*k:.1f} {-.2*k:.1f} {.12*k:.1f} {-.18*k:.1f} q{.13*k:.1f} {.02*k:.1f} {.13*k:.1f} {.2*k:.1f} q{-.04*k:.1f} {-.12*k:.1f} {-.1*k:.1f} {-.1*k:.1f} q{-.1*k:.1f} {.05*k:.1f} {-.1*k:.1f} {.1*k:.1f}z" fill="{INK}" stroke="{INK}" stroke-width="1.6"/>')
    out.append(f'<path d="M{hx+.1*k:.1f} {hy-.02*k:.1f} q{.03*k:.1f} {.2*k:.1f} {-.02*k:.1f} {.22*k:.1f} l{-.06*k:.1f} {-.02*k:.1f}z" fill="{INK}" stroke="{INK}" stroke-width="1.6"/>')
    # 足元のバッグ
    bx_, by_ = P(XR-.5, 0, 4.0); kk = F/4.0
    path([(bx_-.14*kk, by_), (bx_-.15*kk, by_-.18*kk), (bx_+.15*kk, by_-.18*kk), (bx_+.14*kk, by_)], YEL, 1.8, True, curve='round', r=4)
    path([(bx_-.07*kk, by_-.18*kk), (bx_-.06*kk, by_-.3*kk), (bx_+.06*kk, by_-.3*kk), (bx_+.07*kk, by_-.18*kk)], 'none', 1.8, False, curve='round', r=4)

# ---- 天井の蛍光灯 ----
for z in (4.0, 5.6):
    quad((.3, H-.02, z), (1.3, H-.02, z), (1.3, H-.02, z+.25), (.3, H-.02, z+.25), YEL, 1.6)
save(sys.argv[1])
