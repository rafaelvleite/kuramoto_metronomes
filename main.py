# metronomes_45s_lock_at_40_with_credits.py
# - 45 s video (no audio)
# - Full synchronization around t ≈ 40 s
# - English captions (Kuramoto + low-dissipation harmony)
# - End credits (Rafael Vicente Leite, inspired by Mark Rober, GitHub URL)
# - Deterministic render to MP4 via imageio-ffmpeg

import pygame as pg
import numpy as np
import math
import imageio.v2 as imageio

# ========= Output (video) =========
W, H        = 1280, 720
VIDEO_FPS   = 30
DURATION_S  = 45.0
TOTAL_FRAMES = int(VIDEO_FPS * DURATION_S)
OUT_MP4     = "metronomes_sync_45s_lock40.mp4"

# ========= Look & feel =========
BG     = (16,16,22)
HASTE  = (235,235,245)
BOB    = (80,200,255)
BOB2   = (150,150,160)
PIN    = (190,190,200)
TXT    = (240,240,240)
FONT_SZ = 28
FONT_SZ_SMALL = 22
CAPTION_BOX = (0,0,0,140)   # semi-opaque caption box

# ========= Metronomes (phase + realistic small swing) =========
N              = 100
ROWS           = 3
A_PIX          = 72
ALPHA_MAX_DEG  = 22.0
ALPHA_MAX      = math.radians(ALPHA_MAX_DEG)

# Physics / integration
SUBSTEPS = 4
DT       = 1.0 / (VIDEO_FPS * SUBSTEPS)
SEED           = 7
OMEGA_MEAN_HZ  = 1.1
OMEGA_SPREAD   = 0.10          # wider → slower sync

# Staggered starts (more delay)
SPREAD_START_SEC = 10.0
FADEIN_SEC       = 2.5

# Spatial coupling (normalized weights)
LAMBDA   = 160.0               # shorter range → slower information flow

# Time-ramped coupling for late lock (~40 s)
K_START        = 0.16          # subcritical initially
K_END          = 1.60          # above threshold later
T_RAMP_START   = 8.0           # start ramping after initial desync
T_LOCK_TARGET  = 40.0          # reach strong coupling near 40 s

# Tiny phase noise keeps it near threshold longer (still locks)
NOISE_STD = 0.02

# ========= On-screen narration (EN) — spaced for 45 s =========
# (t_in, t_out, text)
NARRA = [
    (0.0,   7.5,  "Experiment: independent metronomes on a fixed table."),
    (7.5,   14.5, "Each starts at a different time and keeps the same swing amplitude."),
    (14.5,  22.0, "A weak ambient coupling (air/desk vibrations) lets them influence one another."),
    (22.0,  29.5, "In the 1970s, the Japanese physicist Yoshiki Kuramoto explained spontaneous synchronization."),
    (29.5, 36.5, "Coupling stays sub-critical, then crosses the Kuramoto threshold near the end."),
    (36.5,  44.5, "As phases align, the system moves to a lower-energy, low-dissipation formation—harmony.")
]
TYPE_CPS = 22  # typewriter speed (chars/sec)

# ========= Layout =========
def grid_positions(n=N, rows=ROWS):
    cols = (n + rows - 1) // rows
    margin_x = 120
    margin_y_top = 150
    spacing_x = (W - 2*margin_x) / max(1, cols - 1)
    spacing_y = 160
    xs, ys = [], []
    k = 0
    for r in range(rows):
        y = margin_y_top + r*spacing_y
        for c in range(cols):
            if k >= n: break
            x = margin_x + c*spacing_x
            xs.append(x); ys.append(y); k += 1
    return np.array(xs, float), np.array(ys, float)

# ========= Init =========
rng = np.random.default_rng(SEED)
xs, ys   = grid_positions(N, ROWS)
omega    = rng.normal(2.0*math.pi*OMEGA_MEAN_HZ, OMEGA_SPREAD, size=N)
theta    = rng.uniform(-math.pi, math.pi, size=N)
t_start  = rng.uniform(0.0, SPREAD_START_SEC, size=N)

# Spatial weights (row-normalized, no self-coupling)
X = xs.reshape(-1,1); Y = ys.reshape(-1,1)
dists   = np.sqrt((X - X.T)**2 + (Y - Y.T)**2)
weights = np.exp(-dists / LAMBDA)
np.fill_diagonal(weights, 0.0)
row_sums = np.sum(weights, axis=1, keepdims=True)
row_sums[row_sums == 0] = 1.0
Wnorm = weights / row_sums  # scaled by K_eff(t) inside step()

# ========= Pygame =========
pg.init()
screen = pg.display.set_mode((W, H))
pg.display.set_caption("Metronomes — 45s, late lock ~40s, no audio")
font  = pg.font.SysFont(None, FONT_SZ)
font2 = pg.font.SysFont(None, FONT_SZ_SMALL)

def smoothstep(z):
    z = max(0.0, min(1.0, z))
    return z*z*(3 - 2*z)

def K_eff_at(t):
    if t <= T_RAMP_START:
        return K_START
    z = (t - T_RAMP_START) / max(1e-9, (T_LOCK_TARGET - T_RAMP_START))
    s = smoothstep(z)
    return K_START + s*(K_END - K_START)

def step(theta, t, dt):
    # activation (staggered joins with fade-in)
    active = (t >= t_start)
    gain = np.zeros_like(theta, float)
    if np.any(active):
        dt_since = np.clip(t - t_start[active], 0.0, FADEIN_SEC)
        gain_active = np.clip(dt_since / FADEIN_SEC, 0.0, 1.0)
        gain[active] = gain_active
    G = np.outer(gain, gain)

    # Kuramoto with spatial weights and time-ramped coupling
    dtheta = theta.reshape(-1,1) - theta.reshape(1,-1)
    K_eff = K_eff_at(t)
    coupling = K_eff * np.sum(Wnorm * G * np.sin(-dtheta), axis=1)

    # tiny phase diffusion
    eta = NOISE_STD * math.sqrt(dt) * rng.standard_normal(size=theta.shape)

    return theta + (omega + coupling) * dt + eta

def draw_metronomes(theta, t):
    active = (t >= t_start)
    for i in range(N):
        x = xs[i]; y_top = ys[i]
        pg.draw.line(screen, PIN, (x, y_top-6), (x, y_top+6), 2)
        ang   = ALPHA_MAX * math.sin(float(theta[i]))  # realistic small swing
        x_bob = x + A_PIX * math.sin(ang)
        y_bob = y_top + A_PIX * math.cos(ang)
        pg.draw.line(screen, HASTE, (x, y_top), (x_bob, y_bob), 3)
        pg.draw.circle(screen, (BOB if active[i] else BOB2), (int(x_bob), int(y_bob)), 8)

def render_caption(t):
    for t_in, t_out, text in NARRA:
        if t_in <= t <= t_out:
            chars = int((t - t_in) * TYPE_CPS)
            chars = max(0, min(len(text), chars))
            show  = text[:chars]
            pad   = 12
            msg   = font.render(show, True, TXT)
            box_w = msg.get_width() + 2*pad
            box_h = msg.get_height() + 2*pad
            x = (W - box_w)//2
            y = H - box_h - 28
            s = pg.Surface((box_w, box_h), pg.SRCALPHA)
            s.fill(CAPTION_BOX)
            screen.blit(s, (x,y))
            screen.blit(msg, (x+pad, y+pad))
            break

def draw_hud(theta, t):
    re = float(np.mean(np.cos(theta))); im = float(np.mean(np.sin(theta)))
    r = math.hypot(re, im)
    hud1 = f"N={N}   K(t)={K_eff_at(t):.2f}   λ={int(LAMBDA)}px   f≈{OMEGA_MEAN_HZ:.2f} Hz   t={t:5.1f}s"
    hud2 = f"order parameter r={r:.3f}   swing ±{ALPHA_MAX_DEG:.0f}°"
    screen.blit(font2.render(hud1, True, TXT), (20, 16))
    screen.blit(font2.render(hud2, True, TXT), (20, 40))

def draw_credits(t):
    # show credits in the last 4 seconds
    if t < DURATION_S - 4.0:
        return
    lines = [
        "Visualization by Rafael Vicente Leite",
        "Inspired by Mark Rober's video",
        "Public on GitHub: https://github.com/rafaelvleite/kuramoto_metronomes"
    ]
    pad = 10
    spacing = 6
    msgs = [font2.render(s, True, TXT) for s in lines]
    w = max(m.get_width() for m in msgs) + 2*pad
    h = sum(m.get_height() for m in msgs) + (len(msgs)-1)*spacing + 2*pad
    x = (W - w)//2
    y = 70
    box = pg.Surface((w, h), pg.SRCALPHA)
    box.fill((0,0,0,120))
    screen.blit(box, (x,y))
    cy = y + pad
    for m in msgs:
        screen.blit(m, (x+pad, cy))
        cy += m.get_height() + spacing

# ========= Deterministic render-to-video (no audio) =========
writer = imageio.get_writer(OUT_MP4, fps=VIDEO_FPS, codec="libx264", quality=8)
t = 0.0

for frame_idx in range(TOTAL_FRAMES):
    for ev in pg.event.get():    # keep window responsive
        if ev.type == pg.QUIT:
            TOTAL_FRAMES = frame_idx + 1

    # fixed-step physics
    for _ in range(SUBSTEPS):
        theta = step(theta, t, DT)
        theta = (theta + math.pi) % (2*math.pi) - math.pi
        t += DT

    # draw & capture
    screen.fill(BG)
    draw_metronomes(theta, t)
    draw_hud(theta, t)
    render_caption(t)
    draw_credits(t)

    arr = pg.surfarray.array3d(pg.display.get_surface())  # WxHx3
    frame = np.transpose(arr, (1, 0, 2))                  # HxWx3
    writer.append_data(frame)
    pg.display.flip()

writer.close()
pg.quit()
print(f"✅ Saved MP4 (no audio): {OUT_MP4}")
