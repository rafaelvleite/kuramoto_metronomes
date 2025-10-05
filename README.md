# Kuramoto Metronomes Synchronization

A visual simulation demonstrating the **Kuramoto synchronization phenomenon** using metronomes with realistic pendulum physics and spatial coupling.

![Metronomes Sync Demo](metronomes_sync_english.mp4)

## Overview

This experiment simulates multiple independent metronomes placed on a fixed table, each starting at slightly different times and phases. Through weak spatial coupling based on the **Kuramoto model**, the metronomes gradually synchronize their oscillations, creating a beautiful demonstration of emergent collective behavior.

### What is Kuramoto Synchronization?

In the 1970s, Japanese physicist **Yoshiki Kuramoto** described how oscillators can spontaneously synchronize through weak coupling. This phenomenon explains everything from fireflies flashing in unison to the coordinated beating of heart cells.

## Features

- **90 metronomes** arranged in a 3-row grid
- **Realistic pendulum physics** with ±22° swing amplitude
- **Spatial coupling** - closer metronomes influence each other more strongly
- **Staggered start times** to show the synchronization process
- **Real-time visualization** with order parameter tracking
- **Educational narration** explaining the physics
- **High-quality MP4 export** for presentations and sharing

## Physics Parameters

| Parameter | Value | Description |
|-----------|-------|-------------|
| `N` | 90 | Number of metronomes |
| `K0` | 1.5 | Base coupling strength |
| `LAMBDA` | 200px | Spatial coupling range |
| `OMEGA_MEAN_HZ` | 1.1 Hz | Natural frequency (~66 BPM) |
| `ALPHA_MAX` | 22° | Maximum swing angle |

## Installation

### Requirements

```bash
pip install pygame numpy imageio[ffmpeg]
```

### Dependencies

- **Python 3.7+**
- **pygame** - for real-time visualization and rendering
- **numpy** - for efficient numerical computations
- **imageio** - for MP4 video export
- **ffmpeg** - for video encoding (installed automatically with imageio[ffmpeg])

## Usage

Simply run the simulation:

```bash
python main.py
```

The program will:
1. Display a real-time visualization window
2. Show educational narration explaining the physics
3. Export a clean MP4 video (`metronomes_sync_english.mp4`)

### Output

The simulation generates a 25-second MP4 video showing:
- Individual metronomes starting at different times
- Gradual phase alignment through coupling
- Final synchronized state
- Real-time order parameter (synchronization measure)

## Understanding the Visualization

### Visual Elements

- **Blue circles**: Active metronome bobs
- **Gray circles**: Inactive metronomes (not yet started)
- **White lines**: Pendulum rods
- **HUD display**: Shows coupling parameters and order parameter

### Order Parameter

The **order parameter** `r` measures synchronization:
- `r ≈ 0`: Complete disorder (random phases)
- `r ≈ 1`: Perfect synchronization (all in phase)

Watch as `r` grows from ~0 to ~1 during the simulation!

## Customization

You can modify various parameters in `main.py`:

```python
# Number and layout
N = 90              # Number of metronomes
ROWS = 3            # Grid rows

# Physics
K0 = 1.5            # Coupling strength (higher = faster sync)
LAMBDA = 200.0      # Spatial range (pixels)
OMEGA_MEAN_HZ = 1.1 # Base frequency

# Timing
DURATION_S = 25.0   # Video duration
SPREAD_START_SEC = 6.0  # Stagger start times
```

## The Mathematics

The simulation implements the **Kuramoto model** with spatial coupling:

```
dθᵢ/dt = ωᵢ + Σⱼ Kᵢⱼ sin(θⱼ - θᵢ)
```

Where:
- `θᵢ` = phase of metronome i
- `ωᵢ` = natural frequency of metronome i  
- `Kᵢⱼ` = coupling strength between metronomes i and j
- Coupling strength decreases exponentially with distance

## Educational Applications

This simulation is perfect for:
- **Physics courses** - demonstrating collective behavior
- **Complex systems** - showing emergence and self-organization
- **Mathematics** - visualizing coupled oscillator dynamics
- **Presentations** - clean MP4 export ready for talks

## Real-World Examples

Kuramoto synchronization appears in:
- 🔥 **Fireflies** flashing in unison
- ❤️ **Cardiac pacemaker cells** coordinating heartbeats
- 🧠 **Neural networks** in the brain
- 🌉 **Pedestrians** walking across bridges
- ⚡ **Power grid** frequency synchronization

## Technical Details

### Performance
- **Deterministic rendering** ensures reproducible videos
- **Substep physics** (4 substeps per frame) for stability
- **Efficient spatial coupling** using pre-computed weight matrices
- **30 FPS export** with smooth animations

### Coordinate System
- Metronomes arranged in a regular grid
- Spatial coupling uses Euclidean distance
- Pendulum physics with realistic small-angle approximation

## License

This project is open source. Feel free to use, modify, and share for educational purposes.

## References

- Kuramoto, Y. (1984). *Chemical Oscillations, Waves, and Turbulence*
- Strogatz, S. H. (2000). *From Kuramoto to Crawford: exploring the onset of synchronization in populations of coupled oscillators*
- Acebrón, J. A., et al. (2005). *The Kuramoto model: A simple paradigm for synchronization phenomena*

## Contributing

Contributions welcome! Ideas for improvements:
- Interactive parameter controls
- Different coupling topologies  
- 3D visualization
- Audio synchronization
- Comparison with real metronome experiments

---

*Created with ❤️ for science education and the beauty of emergent phenomena*