# generate_harmonic_music.py
# Simple, beautiful, harmonic 8-bit music
# Theme: "Synchronized Hearts" - The beauty of coming together in harmony
# Less complexity, more pure musical beauty

import numpy as np
import wave
import math

# Audio parameters
SAMPLE_RATE = 44100
DURATION = 60.0  # seconds - intro(4) + main(46) + pause(2) + outro(8) = exactly 60s
TOTAL_SAMPLES = int(SAMPLE_RATE * DURATION)
MAX_AMPLITUDE = 32767 // 4  # Gentle volume

# Musical parameters - simple and beautiful
BPM = 72  # Calm, heart-rate tempo
BEAT_LENGTH = 60.0 / BPM
MEASURE_LENGTH = BEAT_LENGTH * 4

# Simple, pure waveforms
def pure_sine(freq, t):
    """Pure sine wave - the most harmonic sound"""
    return math.sin(2 * math.pi * freq * t)

def soft_square(freq, t):
    """Soft square wave with rounded edges"""
    sine = math.sin(2 * math.pi * freq * t)
    return math.copysign(1.0, sine) * (abs(sine) ** 0.3)

# Beautiful, simple harmony - C Major pentatonic (no harsh intervals)
# The most universally pleasing scale
C_MAJOR_PENTATONIC = {
    'C4': 261.63,
    'D4': 293.66, 
    'E4': 329.63,
    'G4': 392.00,
    'A4': 440.00,
    'C5': 523.25,
    'D5': 587.33,
    'E5': 659.25
}

# Simple, beautiful chord progression - the "Circle of Fifths" in C Major
# This is mathematically perfect harmony
BEAUTIFUL_CHORDS = [
    # C Major - Home, peace, stability
    [C_MAJOR_PENTATONIC['C4'], C_MAJOR_PENTATONIC['E4'], C_MAJOR_PENTATONIC['G4']],
    # A Minor - Gentle emotion, introspection  
    [C_MAJOR_PENTATONIC['A4'], C_MAJOR_PENTATONIC['C5'], C_MAJOR_PENTATONIC['E5']],
    # F Major - Warmth, comfort, embrace
    [174.61, 220.00, 261.63],  # F3, A3, C4
    # G Major - Joy, uplift, resolution
    [C_MAJOR_PENTATONIC['G4'], 246.94, C_MAJOR_PENTATONIC['D5']]  # G4, B4, D5
]

# Simple, memorable melody - "Synchronized Hearts" theme
# Like a lullaby that represents metronomes finding harmony
HEART_MELODY = [
    # Phrase 1: "Two hearts beating..."
    C_MAJOR_PENTATONIC['C4'], C_MAJOR_PENTATONIC['E4'], C_MAJOR_PENTATONIC['G4'], C_MAJOR_PENTATONIC['E4'],
    # Phrase 2: "Finding their rhythm..."
    C_MAJOR_PENTATONIC['D4'], C_MAJOR_PENTATONIC['G4'], C_MAJOR_PENTATONIC['A4'], C_MAJOR_PENTATONIC['G4'],
    # Phrase 3: "Coming together..."
    C_MAJOR_PENTATONIC['E4'], C_MAJOR_PENTATONIC['C5'], C_MAJOR_PENTATONIC['A4'], C_MAJOR_PENTATONIC['G4'],
    # Phrase 4: "In perfect harmony"
    C_MAJOR_PENTATONIC['C4'], C_MAJOR_PENTATONIC['D4'], C_MAJOR_PENTATONIC['E4'], C_MAJOR_PENTATONIC['C4']
]

def generate_synchronized_hearts():
    """Generate simple, beautiful, harmonic music about synchronization"""
    print("💝 Generating 'Synchronized Hearts' - Simple & Beautiful")
    print("   Theme: The magic moment when separate rhythms become one")
    
    # Initialize audio
    audio = np.zeros(TOTAL_SAMPLES)
    
    # === FOUNDATION: Gentle Bass Heart Beat ===
    print("  💓 Adding gentle heartbeat bass...")
    bass_note = 130.81  # C3 - fundamental, grounding
    
    for i in range(TOTAL_SAMPLES):
        t = i / SAMPLE_RATE
        
        # Simple, steady heartbeat pattern
        beat_position = (t / BEAT_LENGTH) % 2
        if beat_position < 0.1:  # Heartbeat on 1 and 3
            heartbeat_env = math.exp(-beat_position * 20)  # Quick decay
            bass_tone = pure_sine(bass_note, t) * heartbeat_env * 0.15
        else:
            bass_tone = pure_sine(bass_note, t) * 0.03  # Gentle sustain
        
        audio[i] += bass_tone
    
    # === HARMONY: Pure Chord Progression ===
    print("  🎵 Adding pure harmonic chords...")
    
    for i in range(TOTAL_SAMPLES):
        t = i / SAMPLE_RATE
        
        # Simple chord timing - one chord per measure
        measure_pos = (t / MEASURE_LENGTH) % len(BEAUTIFUL_CHORDS)
        chord_index = int(measure_pos)
        
        chord = BEAUTIFUL_CHORDS[chord_index]
        
        # Pure sine wave chords for maximum harmony
        chord_sound = 0
        for note_freq in chord:
            chord_sound += pure_sine(note_freq, t) * 0.08
        
        # Gentle swell within each measure
        measure_progress = (measure_pos - chord_index)
        swell = 0.7 + 0.3 * math.sin(measure_progress * math.pi)
        
        audio[i] += chord_sound * swell
    
    # === MELODY: "Synchronized Hearts" Theme ===
    print("  🎼 Adding 'Synchronized Hearts' melody...")
    
    note_duration = MEASURE_LENGTH / 2  # Half notes for a gentle pace
    melody_start_time = 8.0  # Start after intro
    
    # Play the melody multiple times with variations
    for cycle in range(3):  # 3 cycles of the melody
        cycle_start = melody_start_time + cycle * len(HEART_MELODY) * note_duration
        
        if cycle_start < DURATION - 8.0:  # Leave room for outro
            for note_idx, freq in enumerate(HEART_MELODY):
                note_start = cycle_start + note_idx * note_duration
                
                if note_start < DURATION - 8.0:
                    start_sample = int(note_start * SAMPLE_RATE)
                    note_samples = int(note_duration * SAMPLE_RATE)
                    
                    for i in range(note_samples):
                        if start_sample + i >= TOTAL_SAMPLES:
                            break
                        
                        t = (start_sample + i) / SAMPLE_RATE
                        
                        # Gentle envelope like breathing
                        progress = i / note_samples
                        if progress < 0.3:  # Gentle attack
                            envelope = progress / 0.3
                        elif progress > 0.7:  # Gentle release
                            envelope = (1.0 - progress) / 0.3
                        else:
                            envelope = 1.0
                        
                        # Different timbres for different cycles
                        if cycle == 0:  # Pure sine
                            melody_tone = pure_sine(freq, t) * envelope * 0.12
                        elif cycle == 1:  # Octave doubling
                            melody_tone = (pure_sine(freq, t) + pure_sine(freq * 2, t) * 0.3) * envelope * 0.10
                        else:  # Soft harmony
                            melody_tone = (pure_sine(freq, t) + pure_sine(freq * 1.5, t) * 0.4) * envelope * 0.09
                        
                        audio[start_sample + i] += melody_tone
    
    # === ATMOSPHERE: Gentle Resonance ===
    print("  ✨ Adding gentle atmospheric resonance...")
    
    for i in range(TOTAL_SAMPLES):
        t = i / SAMPLE_RATE
        
        if t > 12.0 and t < 48.0:  # Only during main section
            # Very slow, gentle resonance like a distant church bell
            resonance = pure_sine(C_MAJOR_PENTATONIC['C5'] * 2, t * 0.1) * 0.02
            resonance += pure_sine(C_MAJOR_PENTATONIC['G4'] * 2, t * 0.07) * 0.015
            
            audio[i] += resonance
    
    # === MASTER ENVELOPE: Natural Breathing ===
    print("  🌬️  Adding natural breathing dynamics...")
    
    for i in range(TOTAL_SAMPLES):
        t = i / SAMPLE_RATE
        
        # Main envelope
        fade_factor = 1.0
        if t < 6.0:  # Slow, natural fade in
            fade_factor = (t / 6.0) ** 0.7
        elif t > DURATION - 8.0:  # Gentle fade out
            fade_factor = ((DURATION - t) / 8.0) ** 0.5
        
        # Gentle breathing throughout (very subtle)
        breathing = 1.0 + 0.05 * math.sin(t * 0.2)  # Very slow breathing
        
        audio[i] *= fade_factor * breathing
    
    # === FINAL TOUCH: Warm Limiting ===
    print("  🔥 Adding warm, gentle processing...")
    
    # Soft, musical limiting
    for i in range(len(audio)):
        if abs(audio[i]) > 0.8:
            audio[i] = 0.8 * np.sign(audio[i]) * math.tanh(abs(audio[i]))
    
    # Gentle normalization
    max_val = np.max(np.abs(audio))
    if max_val > 0:
        audio = audio / max_val * 0.75
    
    # Convert to 16-bit
    audio_16bit = (audio * MAX_AMPLITUDE).astype(np.int16)
    
    print("  💝 'Synchronized Hearts' complete - Simple, beautiful, harmonic!")
    return audio_16bit

def save_harmonic_music(audio_data, filename="synchronized_hearts.wav"):
    """Save the beautiful harmonic music"""
    with wave.open(filename, 'w') as wav_file:
        wav_file.setnchannels(1)  # Mono
        wav_file.setsampwidth(2)  # 16-bit  
        wav_file.setframerate(SAMPLE_RATE)
        wav_file.writeframes(audio_data.tobytes())
    
    print(f"✅ Saved: {filename}")
    print(f"   Duration: {DURATION}s")
    print(f"   Theme: Synchronized Hearts")
    print(f"   Style: Simple, harmonic, beautiful")
    print(f"   Harmony: Pure pentatonic scales")

if __name__ == "__main__":
    print("💝 Synchronized Hearts - Harmonic Music Generator")
    print("=" * 55)
    print("🎵 Theme: The beautiful moment when rhythms synchronize")
    print("💓 Like two hearts finding the same beat")
    print("🎼 Simple melodies, pure harmony, gentle beauty")
    print("✨ Perfect for Kuramoto synchronization visualization")
    print()
    
    # Generate the beautiful music
    heart_music = generate_synchronized_hearts()
    
    # Save to file
    save_harmonic_music(heart_music)
    
    print("\n💝 Your 'Synchronized Hearts' track is ready!")
    print("   A simple, beautiful song about finding harmony together.")
    print("   Pure musical mathematics - just like the Kuramoto model!")
    print("   🎵 Simple • 💝 Beautiful • ✨ Harmonic")