# combine_video_audio.py
# Complete video production pipeline:
# 1. Combines the Kuramoto metronomes video with the mystic ambient music
# 2. Adds professional intro and outro sections
# 3. Creates a final audiovisual experience ready for sharing

import subprocess
import os
import tempfile
from pathlib import Path

# File paths
VIDEO_FILE = "metronomes_sync_46s_lock40_pastel_spatial_phase.mp4"
AUDIO_FILE = "synchronized_hearts.wav"
TEMP_VIDEO_WITH_AUDIO = "temp_video_with_audio.mp4"
FINAL_OUTPUT = "kuramoto_metronomes_complete.mp4"

# Video settings
VIDEO_WIDTH = 1280
VIDEO_HEIGHT = 720
VIDEO_FPS = 30

# Intro/Outro timing
INTRO_DURATION = 4.0    # seconds
PAUSE_DURATION = 2.0    # seconds - hold last frame
OUTRO_DURATION = 8.0    # seconds (more time for credits since video is shorter)

# Colors (matching your video's palette)
BG_COLOR = "0a0e16"     # Dark navy (hex)
TEXT_COLOR = "ecf6ff"   # Light text
ACCENT_COLOR = "00ccff" # Cyan accent

# Text content
INTRO_TITLE = "Kuramoto Synchronization"
INTRO_SUBTITLE = "The Mathematics of Emergent Harmony"
INTRO_CREDIT = "Visualization by Rafael Vicente Leite"

OUTRO_TITLE = "Thank You for Watching"
OUTRO_SUBTITLE = "Visualization by Rafael Vicente Leite"
OUTRO_FOOTER = "Inspired by Mark Rober • Based on Kuramoto Model • Music: 'Synchronized Hearts'"
OUTRO_GITHUB = "github.com/rafaelvleite/kuramoto_metronomes"

# Audio settings
SAMPLE_RATE = 44100        # For audio looping calculations
AUDIO_FADE_IN = 2.0        # seconds
AUDIO_FADE_OUT = 3.0       # seconds
AUDIO_VOLUME = 0.7         # 0.0 to 1.0 (70% volume for ambient feel)

def check_dependencies():
    """Check if required tools are available"""
    print("🔍 Checking dependencies...")
    
    try:
        result = subprocess.run(["ffmpeg", "-version"], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("  ✅ FFmpeg found")
            return True
        else:
            print("  ❌ FFmpeg not working properly")
            return False
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("  ❌ FFmpeg not found")
        print("     Install with: brew install ffmpeg (macOS)")
        return False

def check_input_files():
    """Verify input files exist"""
    print("📁 Checking input files...")
    
    video_exists = Path(VIDEO_FILE).exists()
    audio_exists = Path(AUDIO_FILE).exists()
    
    if video_exists:
        print(f"  ✅ Video found: {VIDEO_FILE}")
    else:
        print(f"  ❌ Video missing: {VIDEO_FILE}")
        print("     Run main.py first to generate the video")
    
    if audio_exists:
        print(f"  ✅ Audio found: {AUDIO_FILE}")
    else:
        print(f"  ❌ Audio missing: {AUDIO_FILE}")
        print("     Run generate_music.py first to create the music")
    
    return video_exists and audio_exists

def get_video_duration():
    """Get video duration using ffprobe"""
    try:
        cmd = [
            "ffprobe", "-v", "quiet", "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1", VIDEO_FILE
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            duration = float(result.stdout.strip())
            print(f"  📊 Video duration: {duration:.1f}s")
            return duration
        else:
            print("  ⚠️  Could not determine video duration, using 45s")
            return 45.0
    except Exception as e:
        print(f"  ⚠️  Error getting duration: {e}, using 45s")
        return 45.0

def create_intro():
    """Create intro video segment"""
    print("🎬 Creating intro...")
    
    intro_file = os.path.abspath("temp_intro.mp4")
    
    # Create temporary text files to avoid escaping issues
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        title_file = f.name
        f.write(INTRO_TITLE)
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        subtitle_file = f.name
        f.write(INTRO_SUBTITLE)
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        credit_file = f.name
        f.write(INTRO_CREDIT)
    
    try:
        # Use textfile option to avoid escaping issues
        cmd = [
            "ffmpeg", "-y",
            "-f", "lavfi",
            "-i", f"color=c={BG_COLOR}:size={VIDEO_WIDTH}x{VIDEO_HEIGHT}:duration={INTRO_DURATION}:rate={VIDEO_FPS}",
            "-vf", f"drawtext=fontfile=/System/Library/Fonts/Helvetica.ttc:textfile={title_file}:fontsize=64:fontcolor={TEXT_COLOR}:x=(w-text_w)/2:y=h/2-100:alpha='if(lt(t,0.5),0,if(lt(t,1.0),(t-0.5)*2,1))',drawtext=fontfile=/System/Library/Fonts/Helvetica.ttc:textfile={subtitle_file}:fontsize=28:fontcolor={ACCENT_COLOR}:x=(w-text_w)/2:y=h/2-20:alpha='if(lt(t,1.0),0,if(lt(t,1.5),(t-1.0)*2,1))',drawtext=fontfile=/System/Library/Fonts/Helvetica.ttc:textfile={credit_file}:fontsize=20:fontcolor={TEXT_COLOR}:x=(w-text_w)/2:y=h/2+60:alpha='if(lt(t,2.0),0,if(lt(t,2.5),(t-2.0)*2,1))'",
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            intro_file
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        # Clean up text files
        for temp_file in [title_file, subtitle_file, credit_file]:
            if os.path.exists(temp_file):
                os.unlink(temp_file)
        
        if result.returncode == 0:
            print(f"  ✅ Intro created: {intro_file}")
            return intro_file
        else:
            print(f"  ❌ Failed to create intro: {result.stderr}")
            return None
            
    except Exception as e:
        print(f"  ❌ Error creating intro: {e}")
        # Clean up on error
        for temp_file in [title_file, subtitle_file, credit_file]:
            if os.path.exists(temp_file):
                try:
                    os.unlink(temp_file)
                except:
                    pass
        return None

def create_pause_segment():
    """Create a pause segment holding the last frame"""
    print("📷 Creating pause segment...")
    
    pause_file = os.path.abspath("temp_pause.mp4")
    
    try:
        # Extract last frame from ORIGINAL video (not the one with audio fade)
        # This ensures we get the bright, unfaded last frame
        cmd = [
            "ffmpeg", "-y",
            "-sseof", "-1",  # Seek to last frame
            "-i", VIDEO_FILE,  # Use original video, not temp_video_with_audio
            "-vf", f"scale={VIDEO_WIDTH}:{VIDEO_HEIGHT}",
            "-t", str(PAUSE_DURATION),
            "-r", str(VIDEO_FPS),
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            pause_file
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print(f"  ✅ Pause segment created: {pause_file}")
            return pause_file
        else:
            print(f"  ❌ Failed to create pause: {result.stderr}")
            return None
            
    except Exception as e:
        print(f"  ❌ Error creating pause: {e}")
        return None

def create_outro():
    """Create outro video segment"""
    print("🎬 Creating outro...")
    
    outro_file = os.path.abspath("temp_outro.mp4")
    
    # Create temporary text files to avoid escaping issues
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        title_file = f.name
        f.write(OUTRO_TITLE)
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        subtitle_file = f.name
        f.write(OUTRO_SUBTITLE)
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        footer_file = f.name
        f.write(OUTRO_FOOTER)
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        github_file = f.name
        f.write(OUTRO_GITHUB)
    
    try:
        # Use textfile option to avoid escaping issues
        cmd = [
            "ffmpeg", "-y",
            "-f", "lavfi",
            "-i", f"color=c={BG_COLOR}:size={VIDEO_WIDTH}x{VIDEO_HEIGHT}:duration={OUTRO_DURATION}:rate={VIDEO_FPS}",
            "-vf", f"drawtext=fontfile=/System/Library/Fonts/Helvetica.ttc:textfile={title_file}:fontsize=48:fontcolor={TEXT_COLOR}:x=(w-text_w)/2:y=h/2-100:alpha='if(lt(t,0.5),0,if(lt(t,1.0),(t-0.5)*2,1))',drawtext=fontfile=/System/Library/Fonts/Helvetica.ttc:textfile={subtitle_file}:fontsize=24:fontcolor={ACCENT_COLOR}:x=(w-text_w)/2:y=h/2-30:alpha='if(lt(t,1.0),0,if(lt(t,1.5),(t-1.0)*2,1))',drawtext=fontfile=/System/Library/Fonts/Helvetica.ttc:textfile={footer_file}:fontsize=16:fontcolor={TEXT_COLOR}:x=(w-text_w)/2:y=h/2+40:alpha='if(lt(t,2.0),0,if(lt(t,2.5),(t-2.0)*2,1))',drawtext=fontfile=/System/Library/Fonts/Helvetica.ttc:textfile={github_file}:fontsize=18:fontcolor={ACCENT_COLOR}:x=(w-text_w)/2:y=h/2+80:alpha='if(lt(t,3.0),0,if(lt(t,3.5),(t-3.0)*2,1))'",
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            outro_file
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        # Clean up text files
        for temp_file in [title_file, subtitle_file, footer_file, github_file]:
            if os.path.exists(temp_file):
                os.unlink(temp_file)
        
        if result.returncode == 0:
            print(f"  ✅ Outro created: {outro_file}")
            return outro_file
        else:
            print(f"  ❌ Failed to create outro: {result.stderr}")
            return None
            
    except Exception as e:
        print(f"  ❌ Error creating outro: {e}")
        # Clean up on error
        for temp_file in [title_file, subtitle_file, footer_file, github_file]:
            if os.path.exists(temp_file):
                try:
                    os.unlink(temp_file)
                except:
                    pass
        return None

def combine_video_audio():
    """Combine video and audio using FFmpeg (creates temp file)"""
    print("� Adding music to video...")
    
    # Get video duration for audio processing
    video_duration = get_video_duration()
    
    # Check if we need to loop the audio
    audio_needs_looping = video_duration > 30.0  # Assume audio might be shorter
    
    # Build FFmpeg command with audio looping if needed
    if audio_needs_looping:
        # Loop audio to match video duration
        audio_filter = f"aloop=loop=-1:size={int(SAMPLE_RATE*video_duration)},volume={AUDIO_VOLUME},afade=t=in:st=0:d={AUDIO_FADE_IN},afade=t=out:st={video_duration-AUDIO_FADE_OUT}:d={AUDIO_FADE_OUT}"
        print("  🔄 Audio will be looped to match video duration")
    else:
        audio_filter = f"volume={AUDIO_VOLUME},afade=t=in:st=0:d={AUDIO_FADE_IN},afade=t=out:st={video_duration-AUDIO_FADE_OUT}:d={AUDIO_FADE_OUT}"
    
    cmd = [
        "ffmpeg",
        "-i", VIDEO_FILE,           # Input video
        "-i", AUDIO_FILE,           # Input audio
        "-c:v", "copy",             # Copy video stream (no re-encoding)
        "-c:a", "aac",              # Encode audio as AAC
        "-b:a", "128k",             # Audio bitrate
        "-t", str(video_duration),  # Set output duration to match video
        "-filter:a", audio_filter,
        "-y",                       # Overwrite output file
        TEMP_VIDEO_WITH_AUDIO
    ]
    
    print(f"  🔧 Running: {' '.join(cmd[:6])} ... (+ audio filters)")
    
    try:
        # Run FFmpeg with progress
        process = subprocess.Popen(
            cmd, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            text=True
        )
        
        # Monitor progress
        stdout, stderr = process.communicate()
        
        if process.returncode == 0:
            print(f"  ✅ Success! Created: {TEMP_VIDEO_WITH_AUDIO}")
            return True
        else:
            print(f"  ❌ FFmpeg failed with return code {process.returncode}")
            print(f"  Error output: {stderr}")
            return False
            
    except Exception as e:
        print(f"  ❌ Error running FFmpeg: {e}")
        return False

def create_complete_video():
    """Create complete video with intro, main content, pause, and outro"""
    print("🎬 Creating complete video with intro, pause, and outro...")
    
    # Create intro, pause, and outro
    intro_file = create_intro()
    pause_file = create_pause_segment()
    outro_file = create_outro()
    
    if not intro_file or not pause_file or not outro_file:
        print("  ❌ Failed to create intro/pause/outro sections")
        return False
    
    # Create a temporary file list for FFmpeg concat with absolute paths
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        concat_file = f.name
        f.write(f"file '{os.path.abspath(intro_file)}'\n")
        f.write(f"file '{os.path.abspath(TEMP_VIDEO_WITH_AUDIO)}'\n")
        f.write(f"file '{os.path.abspath(pause_file)}'\n")
        f.write(f"file '{os.path.abspath(outro_file)}'\n")
    
    try:
        # Use separate inputs with continuous music throughout
        total_duration = INTRO_DURATION + 45.0 + PAUSE_DURATION + OUTRO_DURATION
        
        cmd = [
            "ffmpeg", "-y",
            "-i", intro_file,                    # Input 0: intro (video only)
            "-i", TEMP_VIDEO_WITH_AUDIO,         # Input 1: main video (video + audio)
            "-i", pause_file,                    # Input 2: pause (video only)
            "-i", outro_file,                    # Input 3: outro (video only)
            "-i", AUDIO_FILE,                    # Input 4: full music track
            "-filter_complex", f"""
            [0:v][1:v][2:v][3:v]concat=n=4:v=1:a=0[outv];
            [4:a]volume={AUDIO_VOLUME},afade=t=in:st=0:d={AUDIO_FADE_IN},afade=t=out:st={total_duration-AUDIO_FADE_OUT}:d={AUDIO_FADE_OUT}[outa]
            """.replace('\n', '').replace('            ', ''),
            "-map", "[outv]",
            "-map", "[outa]",
            "-c:v", "libx264",
            "-c:a", "aac",
            "-t", str(total_duration),  # Ensure exact duration
            FINAL_OUTPUT
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        
        # Clean up temporary files
        for temp_file in [concat_file, intro_file, pause_file, outro_file, TEMP_VIDEO_WITH_AUDIO]:
            if os.path.exists(temp_file):
                os.unlink(temp_file)
        
        if result.returncode == 0:
            print(f"  ✅ Complete video created: {FINAL_OUTPUT}")
            return True
        else:
            print(f"  ❌ Failed to create complete video: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"  ❌ Error creating complete video: {e}")
        # Clean up on error
        for temp_file in [concat_file, intro_file, outro_file, TEMP_VIDEO_WITH_AUDIO]:
            if os.path.exists(temp_file):
                try:
                    os.unlink(temp_file)
                except:
                    pass
        return False

def get_file_info():
    """Display information about the final file"""
    if not Path(FINAL_OUTPUT).exists():
        return
    
    print("\n📊 Final file information:")
    
    try:
        # Get file size
        size_mb = Path(FINAL_OUTPUT).stat().st_size / (1024 * 1024)
        print(f"  📁 File size: {size_mb:.1f} MB")
        
        # Get video info
        cmd = [
            "ffprobe", "-v", "quiet", "-show_entries", 
            "stream=codec_name,width,height,duration",
            "-of", "csv=p=0", FINAL_OUTPUT
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')
            for line in lines:
                if line:
                    parts = line.split(',')
                    if len(parts) >= 3:
                        codec, width, height = parts[:3]
                        if codec in ['h264', 'aac']:
                            if codec == 'h264':
                                print(f"  🎬 Video: {width}x{height} ({codec})")
                            else:
                                print(f"  🎵 Audio: {codec}")
        
    except Exception as e:
        print(f"  ⚠️  Could not get file info: {e}")

def main():
    """Main execution flow"""
    print("🎵🎬 Kuramoto Metronomes - Complete Video Production")
    print("=" * 60)
    
    # Check if we have everything we need
    if not check_dependencies():
        return False
    
    if not check_input_files():
        print("\n❌ Missing required files. Please ensure you have:")
        print(f"   1. {VIDEO_FILE} (run main.py)")
        print(f"   2. {AUDIO_FILE} (run generate_music.py)")
        return False
    
    # Step 1: Combine video with audio
    print("\n📝 Step 1: Adding music to video...")
    if not combine_video_audio():
        print("❌ Failed to add music to video")
        return False
    
    # Step 2: Add intro, pause, and outro
    print("\n📝 Step 2: Adding intro, pause, and outro...")
    if not create_complete_video():
        print("❌ Failed to create complete video")
        return False
    
    # Show final results
    get_file_info()
    print(f"\n🎉 Complete video ready: {FINAL_OUTPUT}")
    print("   ✨ Professional intro and outro added!")
    print("   🎵 Hope and Harmony music throughout!")
    print("   🌍 A vision of peace and global unity!")
    print("   🎬 Ready for sharing and presentations!")
    
    # Calculate total duration
    total_duration = INTRO_DURATION + 45.0 + PAUSE_DURATION + OUTRO_DURATION  # ~57 seconds
    print(f"\n📊 Video structure:")
    print(f"   🎬 Intro: {INTRO_DURATION}s")
    print(f"   🎵 Main content: ~45s (with music)")
    print(f"   📷 Pause: {PAUSE_DURATION}s (last frame hold)")
    print(f"   🎭 Outro: {OUTRO_DURATION}s")
    print(f"   ⏱️  Total: ~{total_duration}s")
    print(f"   🎵 Music: Continuous throughout entire video")
    
    # Suggest next steps
    print("\n💡 Next steps:")
    print("   • Preview the video to ensure quality")
    print("   • Share on educational platforms")
    print("   • Use in presentations about complex systems")
    print("   • Upload to YouTube with science/education tags")
    
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)