# Kuramoto Metronomes Synchronization

A stunning visual simulation demonstrating the **Kuramoto synchronization phenomenon** using metronomes with realistic pendulum physics, spatial clustering, and beautiful audiovisual presentation.

![Metronomes Sync Demo](kuramoto_metronomes_complete.mp4)

## 🎯 What You'll See

Watch **36 metronomes** start chaotically, then gradually find their rhythm through the invisible force of synchronization. This isn't just a simulation—it's a window into one of nature's most beautiful mathematical phenomena.

## 🎵 Complete Experience

This project includes:
- **🎬 Professional video production** with intro/outro
- **🎵 Original soundtrack** ("Synchronized Hearts" - harmonic ambient music)
- **📚 Educational narration** in Portuguese and English
- **🎨 Pastel cluster visualization** showing synchronization groups
- **📊 Real-time physics analysis** with coupling parameters

## 🔬 The Science

### What is Kuramoto Synchronization?

In the 1970s, Japanese physicist **Yoshiki Kuramoto** discovered how independent oscillators can spontaneously synchronize through weak coupling. This phenomenon explains:

- 🔥 **Fireflies** flashing in perfect unison
- ❤️ **Heart cells** beating together
- 🧠 **Brain waves** coordinating thought
- 🌉 **Bridge oscillations** from pedestrian walking
- ⚡ **Power grids** maintaining frequency

### Our Implementation

- **36 metronomes** in a 3×12 grid formation
- **Spatial coupling** - closer metronomes influence each other more
- **Phase clustering** - metronomes form synchronized groups by color
- **Time-ramped coupling** - synchronization emerges gradually around 40 seconds
- **Hysteresis anti-flicker** - stable color assignments

## ⚙️ Technical Specifications

| Parameter | Value | Description |
|-----------|-------|-------------|
| **Metronomes** | 36 | Arranged in 3×12 grid |
| **Duration** | 46s main + 14s intro/outro = 60s total | Perfect 1-minute video |
| **Coupling Range** | 160px | Spatial influence radius |
| **Natural Frequency** | 1.1 Hz (~66 BPM) | Human-like heartbeat rhythm |
| **Max Swing** | ±22° | Realistic pendulum physics |
| **Coupling Growth** | K: 0.16 → 1.60 | Gradual synchronization |
| **Target Sync** | ~40 seconds | When global lock occurs |
| **Video Quality** | 1280×720, 30fps | HD ready for sharing |

## 🚀 Quick Start

### Prerequisites

```bash
pip install pygame numpy imageio[ffmpeg]
```

### Generate the Complete Experience

1. **Create the base animation:**
```bash
python main.py
```
*Generates: `metronomes_sync_46s_lock40_pastel_spatial_phase.mp4`*

2. **Generate the soundtrack:**
```bash
python generate_harmonic_music.py
```
*Creates: `synchronized_hearts.wav` (60-second harmonic ambient music)*

3. **Produce the final video:**
```bash
python combine_video_audio.py
```
*Outputs: `kuramoto_metronomes_complete.mp4` (final 60-second masterpiece)*

## 🎨 Visual Features

### Color-Coded Synchronization
- **🎨 Pastel clusters** - Groups of synchronized metronomes share beautiful colors
- **⚪ Neutral gray** - Independent metronomes not yet synchronized  
- **💚 Global lock** - All metronomes turn soft green when fully synchronized
- **🔄 Hysteresis** - Stable color assignments prevent flickering

### Professional Video Structure
- **🎬 4s Intro** - Elegant title sequence
- **🎯 46s Main** - Full synchronization demonstration
- **⏸️ 2s Pause** - Hold on the beautiful final synchronized state
- **🎭 8s Outro** - Complete credits and attribution

### Real-Time Analytics
- **📊 Order parameter `r`** - Measures global synchronization (0 = chaos, 1 = perfect sync)
- **📈 Coupling strength `K(t)`** - Shows how interaction strength grows over time
- **🔢 Local groups** - Count of synchronized clusters
- **⏱️ Time tracking** - Current simulation time

## 🎵 Audio Experience

The included **"Synchronized Hearts"** soundtrack features:
- **💓 Gentle heartbeat bass** - Representing the fundamental rhythm of life
- **🎼 Pure harmonic chords** - Mathematical beauty in C Major pentatonic
- **🎵 Contemplative melody** - Tells the story of finding harmony together
- **✨ Atmospheric resonance** - Subtle textures that breathe with the visuals

*Theme: The magical moment when separate rhythms become one*

## 🔧 Customization

### Key Parameters in `main.py`

```python
# System size
N = 36                  # Number of metronomes
ROWS = 3               # Grid layout

# Physics timing  
DURATION_S = 46.0      # Simulation length
T_LOCK_TARGET = 40.0   # When synchronization peaks

# Coupling dynamics
K_START = 0.16         # Initial coupling (subcritical)
K_END = 1.60          # Final coupling (supercritical) 
LAMBDA = 160.0        # Spatial coupling range (pixels)

# Clustering parameters
NEIGH_RADIUS_PX = 140     # Neighbor detection radius
PHASE_THRESH_RAD = 0.65   # Phase similarity threshold
MIN_CLUSTER_SIZE = 3      # Minimum group size
```

### Music Customization in `generate_harmonic_music.py`

```python
# Musical parameters
BPM = 72                    # Calm, heart-rate tempo
C_MAJOR_PENTATONIC = {...} # Pure, harmonic scale
HEART_MELODY = [...]       # "Synchronized Hearts" theme
```

## 🧮 The Mathematics

### Kuramoto Model with Spatial Coupling

```
dθᵢ/dt = ωᵢ + K(t) Σⱼ Wᵢⱼ sin(θⱼ - θᵢ) + ηᵢ(t)
```

**Where:**
- `θᵢ` = phase of metronome i
- `ωᵢ` = natural frequency of metronome i  
- `K(t)` = time-varying coupling strength
- `Wᵢⱼ` = spatial weight matrix (exponential decay)
- `ηᵢ(t)` = small phase noise for realism

### Clustering Algorithm

```
1. Find spatial neighbors: |rᵢ - rⱼ| < NEIGH_RADIUS_PX
2. Check phase similarity: |θᵢ - θⱼ| < PHASE_THRESH_RAD  
3. Union-find clustering of aligned neighbors
4. Validate cluster coherence: r_cluster > R_CLUSTER
5. Apply hysteresis for stable visualization
```

## 📚 Educational Applications

Perfect for teaching:
- **🔬 Physics** - Collective behavior and emergent phenomena
- **🧮 Mathematics** - Differential equations and phase dynamics  
- **💻 Complex Systems** - Self-organization and critical transitions
- **🎵 Music Theory** - Harmony, rhythm, and mathematical beauty
- **🎬 Media Production** - Scientific visualization and storytelling

### Lesson Plan Ideas
1. **Phase 1**: Show chaos → order transition
2. **Phase 2**: Explain spatial coupling mechanism  
3. **Phase 3**: Connect to real-world examples
4. **Phase 4**: Explore parameter effects
5. **Phase 5**: Discuss mathematical foundations

## 🌍 Real-World Phenomena

Kuramoto synchronization appears everywhere:

| System | Description | Sync Mechanism |
|--------|-------------|----------------|
| 🔥 **Fireflies** | Flash coordination in Southeast Asia | Visual coupling |
| ❤️ **Heart** | Pacemaker cells beating together | Electrical coupling |
| 🧠 **Brain** | Neural oscillations during sleep | Chemical synapses |
| 🌉 **Bridges** | Millennium Bridge wobble (London) | Mechanical coupling |
| ⚡ **Power Grid** | Frequency synchronization | Electrical grid |
| 🚶 **Crowds** | Pedestrian step coordination | Visual/tactile cues |
| 🦗 **Crickets** | Chirping in unison | Acoustic coupling |

## 🎯 Project Structure

```
kuramoto_metronomes/
├── main.py                           # Core simulation engine
├── generate_harmonic_music.py        # "Synchronized Hearts" soundtrack
├── combine_video_audio.py            # Professional video production
├── requirements.txt                  # Dependencies
├── README.md                         # This documentation
└── Output files:
    ├── metronomes_sync_46s_lock40_pastel_spatial_phase.mp4
    ├── synchronized_hearts.wav  
    └── kuramoto_metronomes_complete.mp4  # Final masterpiece
```

## 🏆 Key Features

✅ **Scientifically accurate** - Real Kuramoto model implementation  
✅ **Visually stunning** - Pastel clusters and smooth animations  
✅ **Educational** - Narration in Portuguese and English  
✅ **Professional quality** - HD video with original soundtrack  
✅ **Customizable** - Extensive parameter control  
✅ **Reproducible** - Deterministic rendering  
✅ **Open source** - MIT license for education  

## 🤝 Contributing

We welcome contributions! Ideas for improvements:
- 🌐 **Multi-language** narration support
- 🎮 **Interactive controls** for real-time parameter adjustment
- 📱 **Mobile version** for tablets and phones  
- 🔊 **Audio synchronization** with actual metronome sounds
- 📊 **Statistical analysis** tools for researchers
- 🎨 **Visualization modes** (3D, VR, different color schemes)

## 📖 References & Inspiration

- **Kuramoto, Y.** (1984). *Chemical Oscillations, Waves, and Turbulence*
- **Strogatz, S. H.** (2000). *From Kuramoto to Crawford: exploring the onset of synchronization*  
- **Acebrón, J. A., et al.** (2005). *The Kuramoto model: A simple paradigm for synchronization phenomena*
- **Mark Rober** - Inspiring metronome synchronization demonstration
- **3Blue1Brown** - Mathematical visualization excellence

## 📄 License

MIT License - Use freely for education, research, and inspiration.

## 🎬 Credits

- **Visualization & Physics**: Rafael Vicente Leite
- **Music Composition**: "Synchronized Hearts" original soundtrack  
- **Inspired by**: Mark Rober's metronome synchronization video
- **Based on**: Kuramoto model of coupled oscillators
- **Repository**: https://github.com/rafaelvleite/kuramoto_metronomes

---

*✨ Created with passion for the beauty of mathematics and the poetry of synchronization ✨*