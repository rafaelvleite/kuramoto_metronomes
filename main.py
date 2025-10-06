# metronomes_45s_lock_at_40_pastel_spatial_phase_final.py
# - 45 s video (no audio), cinematic gradient + vignette
# - Time-ramped coupling → global lock ~40 s
# - Spatial + phase clustering among ACTIVE metronomes only
# - Pastel cluster colors, hysteresis (no flicker), lock hold before all-green
# - English captions (Kuramoto + harmony + energy), end credits
# - Deterministic MP4 via imageio-ffmpeg
#
# Install: pip install pygame numpy imageio imageio-ffmpeg

import pygame as pg
import pygame.gfxdraw as gfx
import numpy as np
import math
import imageio.v2 as imageio

# ========= Output (video) =========
W, H         = 1280, 720
VIDEO_FPS    = 30
DURATION_S   = 46.0
TOTAL_FRAMES = int(VIDEO_FPS * DURATION_S)
OUT_MP4      = "metronomes_sync_46s_lock40_pastel_spatial_phase.mp4"

# ========= Palette (Zen Teal + Pastels) =========
BG_TOP     = (10, 14, 22)     # dark navy
BG_BOTTOM  = (18, 26, 38)     # slightly lighter
PIN        = (120, 140, 155)  # cool grey (pins)
HASTE      = (230, 240, 250)  # near-white (rods)
TXT        = (236, 246, 255)  # text
ACCENT     = (0, 204, 255)    # cyan HUD
CAPTION_BOX_RGBA = (8, 12, 18, 160)  # translucent navy for captions

# Pastel cluster colors (cycled if > len)
CLUSTER_COLORS = [
    (255, 154, 162),  # pastel red
    (255, 236, 148),  # pastel yellow
    (160, 190, 255),  # pastel blue
    (255, 200, 150),  # pastel orange
    (196, 173, 255),  # pastel purple
    (180, 235, 200),  # pastel mint
    (255, 180, 220),  # pastel pink
]
NEUTRAL_COLOR = (125, 135, 150)  # neutral gray for non-qualified dots
LOCK_COLOR    = (140, 235, 170)  # soft pastel green for global lock

# ========= Metronomes (phase + realistic small swing) =========
N              = 36
ROWS           = 3
A_PIX          = 72
ALPHA_MAX_DEG  = 22.0
ALPHA_MAX      = math.radians(ALPHA_MAX_DEG)

# ========= Physics / integration =========
SUBSTEPS        = 4
DT              = 1.0 / (VIDEO_FPS * SUBSTEPS)
SEED            = 7
OMEGA_MEAN_HZ   = 1.1
OMEGA_SPREAD    = 0.10          # wider → slower sync

# Staggered starts (more delay)
SPREAD_START_SEC = 10.0
FADEIN_SEC       = 2.5

# Spatial coupling (normalized weights)
LAMBDA   = 160.0               # shorter range → slower information flow

# Time-ramped coupling for late lock (~40 s)
K_START        = 0.16          # subcritical initially
K_END          = 1.60          # above threshold later
T_RAMP_START   = 8.0           # begin increasing coupling
T_LOCK_TARGET  = 40.0          # strong coupling reached near 40 s

# Tiny phase noise keeps system near threshold longer (still locks)
NOISE_STD = 0.02

# ========= Global lock (hold) =========
R_LOCK          = 0.985        # global r threshold
LOCK_HOLD_SEC   = 0.60         # must sustain r>=R_LOCK this long before all-green

# ========= Spatial + phase clustering knobs =========
NEIGH_RADIUS_PX  = 140         # neighbors if within this pixel radius
PHASE_THRESH_RAD = 0.65        # |Δθ| must be below this (~37°) to be “aligned”
R_CLUSTER        = 0.90        # coherence check for formed groups (0..1)
MIN_CLUSTER_SIZE = 3           # ignore tiny groups

# ========= Hysteresis (anti-flicker) =========
CLUSTER_HYST_SEC = 1.2         # color persistence

# ========= Captions (EN) =========
# (t_in, t_out, text)
NARRA = [
    (0.0,   7.0,  "No início, cada metrônomo se move sozinho — como nós, cada um em seu próprio ritmo."),
    (7.0,   14.0, "Com objetivos, crenças e começos diferentes. Às vezes, parece que nos movemos uns contra os outros."),
    (14.0,  22.0, "Mas conexões sutis — empatia, cooperação, propósito comum — começam a surgir."),
    (22.0,  30.0, "Isso reflete o que o físico japonês Yoshiki Kuramoto mostrou: sistemas podem se auto-sincronizar."),
    (30.0,  36.0, "Quando nos alinhamos, menos energia se perde. O conflito se dissolve. A harmonia é mais eficiente."),
    (36.0,  41.5, "Imagine a humanidade aprendendo essa lição — sem guerras, sem desperdício de energia."),
    (41.5,  46.0, "Apenas equilíbrio, ritmo compartilhado e paz — o estado natural de um mundo conectado.")
]

NARRA = [
    (0.0,   7.0,  "At first, every metronome moves alone — just like us, each following their own rhythm."),
    (7.0,   14.0, "Different goals, beliefs, and starts. Sometimes, it feels like we’re moving against one another."),
    (14.0,  22.0, "But subtle connections — empathy, cooperation, shared purpose — start to emerge."),
    (22.0,  30.0, "This mirrors what physicist Yoshiki Kuramoto showed: systems can self-synchronize."),
    (30.0,  36.0, "When we align, less energy is wasted. Conflict fades. Harmony is simply more efficient."),
    (36.0,  41.5, "Imagine humanity learning this lesson — no more wars, no more wasted effort."),
    (41.5,  46.0, "Just balance, shared rhythm, and peace — the natural state of a connected world.")
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
# Fonts (fallback to default if not present)
font  = pg.font.SysFont("Avenir Next, Montserrat, Inter, Helvetica, Arial", 28)
font2 = pg.font.SysFont("Avenir Next, Montserrat, Inter, Helvetica, Arial", 22)

# ========= Style helpers =========
def draw_vertical_gradient(surf, top_color, bottom_color):
    w, h = surf.get_size()
    for y in range(h):
        t = y / max(1, h-1)
        c = [int(top_color[i]*(1-t) + bottom_color[i]*t) for i in range(3)]
        pg.draw.line(surf, c, (0, y), (w, y))

def draw_vignette(surf, strength=110):
    w, h = surf.get_size()
    vign = pg.Surface((w, h), pg.SRCALPHA)
    cx, cy = w/2, h/2
    max_r2 = (cx**2 + cy**2)
    arr = pg.surfarray.pixels_alpha(vign)
    for y in range(h):
        dy2 = (y - cy)**2
        for x in range(w):
            a = int(strength * ((x - cx)**2 + dy2) / max_r2)
            if a > 0:
                arr[x, y] = min(255, a)
    del arr
    surf.blit(vign, (0,0), special_flags=pg.BLEND_RGBA_SUB)

def aa_line(surface, color, p1, p2, width=1):
    # Correct AA line using pygame.draw.aaline
    p1 = (int(p1[0]), int(p1[1]))
    p2 = (int(p2[0]), int(p2[1]))
    if width <= 1:
        pg.draw.aaline(surface, color, p1, p2)
    else:
        pg.draw.line(surface, color, p1, p2, width)  # core
        pg.draw.aaline(surface, color, p1, p2)       # AA pass

def circle_soft(surface, center, radius, color, outline=0):
    x, y = int(center[0]), int(center[1])
    gfx.aacircle(surface, x, y, radius, color)
    gfx.filled_circle(surface, x, y, radius, color)
    if outline:
        gfx.aacircle(surface, x, y, radius+outline, color)

def caption_box(surface, font, text, box_rgba, y_offset=32, pad=14):
    msg = font.render(text, True, TXT)
    box_w = msg.get_width() + 2*pad
    box_h = msg.get_height() + 2*pad
    x = (W - box_w)//2
    y = H - box_h - y_offset
    s = pg.Surface((box_w, box_h), pg.SRCALPHA)
    s.fill(box_rgba)
    surface.blit(s, (x, y))
    surface.blit(msg, (x+pad, y+pad))

# ========= Kuramoto dynamics =========
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
    # staggered activation with fade-in
    active = (t >= t_start)
    gain = np.zeros_like(theta, float)
    if np.any(active):
        dt_since = np.clip(t - t_start[active], 0.0, FADEIN_SEC)
        gain_active = np.clip(dt_since / FADEIN_SEC, 0.0, 1.0)
        gain[active] = gain_active
    G = np.outer(gain, gain)

    dtheta = theta.reshape(-1,1) - theta.reshape(1,-1)
    K_eff = K_eff_at(t)
    coupling = K_eff * np.sum(Wnorm * G * np.sin(-dtheta), axis=1)

    # tiny phase diffusion
    eta = NOISE_STD * math.sqrt(dt) * rng.standard_normal(size=theta.shape)

    return theta + (omega + coupling) * dt + eta

# ========= Spatial + phase clustering =========
class DSU:
    def __init__(self, n):
        self.p = list(range(n))
        self.r = [0]*n
    def find(self, x):
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]
            x = self.p[x]
        return x
    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb: return
        if self.r[ra] < self.r[rb]:
            self.p[ra] = rb
        elif self.r[ra] > self.r[rb]:
            self.p[rb] = ra
        else:
            self.p[rb] = ra
            self.r[ra] += 1

def phase_diff(a, b):
    """smallest signed phase difference a-b in [-pi, pi]."""
    return (a - b + math.pi) % (2*math.pi) - math.pi

def spatial_phase_clusters(active_idxs, theta):
    """
    Build clusters among ACTIVE metronomes using:
      - spatial proximity: distance < NEIGH_RADIUS_PX
      - phase similarity: |Δθ| < PHASE_THRESH_RAD
    Returns: list of clusters as lists of GLOBAL indices.
    """
    m = len(active_idxs)
    if m == 0:
        return []
    xi = xs[active_idxs]
    yi = ys[active_idxs]
    th = theta[active_idxs]
    dsu = DSU(m)
    R2  = NEIGH_RADIUS_PX * NEIGH_RADIUS_PX
    for i in range(m):
        xi_i, yi_i, th_i = xi[i], yi[i], th[i]
        for j in range(i+1, m):
            dx = xi_i - xi[j]
            dy = yi_i - yi[j]
            if dx*dx + dy*dy <= R2:
                if abs(phase_diff(th_i, th[j])) <= PHASE_THRESH_RAD:
                    dsu.union(i, j)
    comp = {}
    for i in range(m):
        r = dsu.find(i)
        comp.setdefault(r, []).append(i)
    clusters = [[int(active_idxs[i]) for i in local] for local in comp.values()]
    return clusters

def cluster_coherence(theta, idxs):
    """Circular order parameter r for a cluster (0..1)."""
    if not idxs:
        return 0.0
    ang = theta[idxs]
    re = float(np.mean(np.cos(ang)))
    im = float(np.mean(np.sin(ang)))
    return math.hypot(re, im)

# ========= State (hysteresis + lock hold) =========
color_state = {}   # i -> (rgb_tuple, ttl_seconds)
lock_timer  = 0.0  # accumulates time with r >= R_LOCK

# ========= Drawing (active-only spatial+phase clusters + hysteresis) =========
def draw_metronomes(theta, t):
    global lock_timer, color_state

    frame_dt = SUBSTEPS * DT

    # global order
    re = float(np.mean(np.cos(theta))); im = float(np.mean(np.sin(theta)))
    r  = math.hypot(re, im)

    # lock hold logic
    lock_timer = lock_timer + frame_dt if r >= R_LOCK else 0.0
    fully_locked = (lock_timer >= LOCK_HOLD_SEC)

    if fully_locked:
        # all green (with subtle outline)
        for i in range(N):
            x = xs[i]; y_top = ys[i]
            aa_line(screen, PIN, (x, y_top-6), (x, y_top+6), 2)
            ang   = ALPHA_MAX * math.sin(float(theta[i]))
            x_bob = x + A_PIX * math.sin(ang)
            y_bob = y_top + A_PIX * math.cos(ang)
            aa_line(screen, HASTE, (x, y_top), (x_bob, y_bob), 3)
            circle_soft(screen, (int(x_bob), int(y_bob)), 8, LOCK_COLOR, outline=1)
        color_state.clear()
        return

    # --- Only ACTIVE metronomes take part in clustering ---
    active_mask = (t >= t_start)
    active_idxs = np.nonzero(active_mask)[0]

    fresh_assign = {}
    if len(active_idxs) > 0:
        # spatial + phase clusters among ACTIVE ones
        clusters_global = spatial_phase_clusters(active_idxs, theta)

        # qualify clusters by size & internal coherence
        qualified = []
        for cl in clusters_global:
            if len(cl) >= MIN_CLUSTER_SIZE and cluster_coherence(theta, cl) >= R_CLUSTER:
                qualified.append(cl)

        # assign pastel colors (cycle if needed)
        color_iter = iter(CLUSTER_COLORS)
        for cl in qualified:
            try:
                col = next(color_iter)
            except StopIteration:
                color_iter = iter(CLUSTER_COLORS)
                col = next(color_iter)
            for i in cl:
                fresh_assign[i] = col

    # hysteresis update (preserve colors briefly)
    new_state = {}
    for i in range(N):
        if i in fresh_assign:
            new_state[i] = (fresh_assign[i], CLUSTER_HYST_SEC)
        else:
            prev = color_state.get(i)
            if prev:
                col, ttl = prev
                ttl -= frame_dt
                if ttl > 0:
                    new_state[i] = (col, ttl)
    color_state = new_state

    # draw all metronomes (colored if in state, else neutral)
    for i in range(N):
        x = xs[i]; y_top = ys[i]
        aa_line(screen, PIN, (x, y_top-6), (x, y_top+6), 2)
        ang   = ALPHA_MAX * math.sin(float(theta[i]))
        x_bob = x + A_PIX * math.sin(ang)
        y_bob = y_top + A_PIX * math.cos(ang)
        aa_line(screen, HASTE, (x, y_top), (x_bob, y_bob), 3)
        col = color_state.get(i, (NEUTRAL_COLOR, 0.0))[0]
        outline_px = 1 if col != NEUTRAL_COLOR else 0
        circle_soft(screen, (int(x_bob), int(y_bob)), 8, col, outline=outline_px)

def render_caption(t):
    for t_in, t_out, text in NARRA:
        if t_in <= t <= t_out:
            chars = int((t - t_in) * TYPE_CPS)
            chars = max(0, min(len(text), chars))
            show  = text[:chars]
            caption_box(screen, font, show, CAPTION_BOX_RGBA, y_offset=32, pad=14)
            break

def draw_hud(theta, t):
    re = float(np.mean(np.cos(theta))); im = float(np.mean(np.sin(theta)))
    r = math.hypot(re, im)
    if lock_timer < LOCK_HOLD_SEC:
        # count qualified local groups among ACTIVE metronomes
        active_mask = (t >= t_start)
        active_idxs = np.nonzero(active_mask)[0]
        k = 0
        if len(active_idxs) > 0:
            clusters_global = spatial_phase_clusters(active_idxs, theta)
            for cl in clusters_global:
                if len(cl) >= MIN_CLUSTER_SIZE and cluster_coherence(theta, cl) >= R_CLUSTER:
                    k += 1
        hud = f"t={t:5.1f}s   K(t)={K_eff_at(t):.2f}   r={r:.3f}   local sync groups={k}   N={N}"
    else:
        hud = f"t={t:5.1f}s   K(t)={K_eff_at(t):.2f}   r={r:.3f}   N={N}"
    msg = font2.render(hud, True, ACCENT)
    screen.blit(msg, (22, 18))

def draw_credits(t):
    # show credits in the last 4 seconds (top-center)
    if t < DURATION_S - 4.0:
        return
    lines = [
        "Visualization by Rafael Vicente Leite",
        "Inspired by Mark Rober's video about Metronomes Synchronization",
        "Animation and Physics by Rafael Vicente Leite, based on Kuramoto Model",
        "Public on GitHub: https://github.com/rafaelvleite/kuramoto_metronomes"
    ]
    pad = 10; spacing = 6
    msgs = [font2.render(s, True, TXT) for s in lines]
    w = max(m.get_width() for m in msgs) + 2*pad
    h = sum(m.get_height() for m in msgs) + (len(msgs)-1)*spacing + 2*pad
    x = (W - w)//2; y = 76
    box = pg.Surface((w, h), pg.SRCALPHA)
    box.fill((0, 0, 0, 120))
    screen.blit(box, (x, y))
    cy = y + pad
    for m in msgs:
        screen.blit(m, (x+pad, cy))
        cy += m.get_height() + spacing

# ========= Deterministic render-to-video (no audio) =========
writer = imageio.get_writer(OUT_MP4, fps=VIDEO_FPS, codec="libx264", quality=8)
t = 0.0

for frame_idx in range(TOTAL_FRAMES):
    # minimal event pump (keeps window responsive)
    for ev in pg.event.get():
        if ev.type == pg.QUIT:
            TOTAL_FRAMES = frame_idx + 1

    # fixed-step physics
    for _ in range(SUBSTEPS):
        theta = step(theta, t, DT)
        theta = (theta + math.pi) % (2*math.pi) - math.pi
        t += DT

    # background + scene
    draw_vertical_gradient(screen, BG_TOP, BG_BOTTOM)
    draw_metronomes(theta, t)
    draw_hud(theta, t)
    render_caption(t)
    draw_vignette(screen, strength=110)  # subtle edge darkening

    # capture
    arr = pg.surfarray.array3d(pg.display.get_surface())  # WxHx3
    frame = np.transpose(arr, (1, 0, 2))                  # HxWx3
    writer.append_data(frame)

    pg.display.flip()

writer.close()
pg.quit()
print(f"✅ Saved MP4 (no audio): {OUT_MP4}")
