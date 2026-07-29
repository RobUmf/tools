import os
import argparse
import subprocess
from pathlib import Path

def run_ffmpeg(input_file, output_file, bitrate, include_cover, start=None, duration=None):
    """Core Engine: Optimized for UltraSinger 3.10 Sweet Spot."""
    clean_name = Path(input_file).stem 
    cmd = ['ffmpeg', '-y', '-hide_banner', '-loglevel', 'error', '-i', str(input_file)]
    
    if start: 
        cmd.insert(cmd.index('-i'), '-ss')
        cmd.insert(cmd.index('-ss')+1, start)
    if duration: 
        cmd.extend(['-t', str(duration)])
        
    cmd.extend(['-map', '0:a'])

    if include_cover:
        # Maps embedded video/image streams if they exist
        cmd.extend(['-map', '0:v?', '-c:v', 'copy']) 
    
    cmd.extend([
        '-map_metadata', '0', 
        '-id3v2_version', '3', 
        '-metadata', f'title={clean_name}', 
        '-b:a', bitrate, 
        '-ar', '44100',                     
        str(output_file)
    ])
    
    try:
        subprocess.run(cmd, check=True)
        return True
    except:
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="UltraSinger Portable MP3 Optimizer")
    parser.add_argument("-i", "--input", required=True, help="Input Root")
    parser.add_argument("-o", "--output", required=True, help="Target Root")
    parser.add_argument("-b", "--bitrate", default="128k", choices=["128k", "192k", "256k", "320k"], help="Bitrate")
    parser.add_argument("--cover", action="store_true", help="Include Cover Art")
    parser.add_argument("--flat", action="store_true", help="Flatten all files into a single output folder")
    
    args = parser.parse_args()
    input_root = Path(args.input).resolve()
    output_root = Path(args.output).resolve()

    if input_root.is_file():
        files_to_process = [input_root]
    else:
        extensions = ('.mp3', '.wav', '.flac', '.m4a')
        # Use a list to maintain order, but we will check for duplicates
        all_found = [f for f in input_root.rglob('*') if f.suffix.lower() in extensions]
        
        # --- DEDUPLICATION LOGIC ---
        # If the same filename exists in root and subfolder, we prioritize the one in the subfolder (usually better organized)
        files_to_process = []
        seen_filenames = {}
        
        for f in all_found:
            if f.name not in seen_filenames:
                seen_filenames[f.name] = f
                files_to_process.append(f)
            else:
                # If current file is deeper in the tree, replace the shallower one
                if len(f.parts) > len(seen_filenames[f.name].parts):
                    files_to_process.remove(seen_filenames[f.name])
                    seen_filenames[f.name] = f
                    files_to_process.append(f)

    print(f"🚀 Processing {len(files_to_process)} unique tracks into {output_root}...")

    for f in files_to_process:
        if args.flat:
            relative_path = Path(f.name)
        elif input_root.is_dir():
            relative_path = Path(input_root.name) / f.relative_to(input_root)
        else:
            relative_path = Path(f.name)

        target_path = output_root / relative_path.with_suffix('.mp3')
        target_path.parent.mkdir(parents=True, exist_ok=True)
        
        print(f"    Converting: {relative_path}")
        run_ffmpeg(f, target_path, args.bitrate, args.cover)

    print(f"\n✅ Clean Migration Complete to: {output_root}")
