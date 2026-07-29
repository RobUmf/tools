# Portable MP3 Optimizer (`portableMP3.py`)

A fast, container-friendly Python tool powered by `ffmpeg` to batch-downsample, transcode, clean metadata, and restructure large audio archives.

Designed for creating lightweight, portable MP3 collections for mobile devices, legacy media players, or car stereos where high-bitrate WAV/FLAC files waste unnecessary storage space.

---

## Required Flags

* **`-i`**, **`--input`** `<PATH>`  
  * **Description:** Input directory containing audio files or a single audio file to process.  
  * **Supported Formats:** `.flac`, `.wav`, `.m4a`, `.mp3`  

* **`-o`**, **`--output`** `<PATH>`  
  * **Description:** Destination directory path where optimized MP3 files will be written.  

---

## Optional Flags

* **`-b`**, **`--bitrate`** `{128k|192k|256k|320k}`  
  * **Description:** Sets the target audio bitrate for the output MP3 files.  
  * **Default:** `128k`  
  * **Choices:** `128k`, `192k`, `256k`, `320k`  

* **`--cover`**  
  * **Description:** Preserves embedded album art or video thumbnail streams in the converted MP3 files.  
  * **Default:** Disabled (`False`)  

* **`--flat`**  
  * **Description:** Flattens the output directory hierarchy, outputting all converted files directly into the root target folder without preserving subdirectories.  
  * **Default:** Preserves folder structure (`False`)  

---

## 📋 Quick Reference Table

| Short Flag | Long Flag | Parameter Type | Default Value | Description |
| :--- | :--- | :--- | :--- | :--- |
| `-i` | `--input` | Path (File/Dir) | *(Required)* | Source input path |
| `-o` | `--output` | Path (Dir) | *(Required)* | Destination directory |
| `-b` | `--bitrate` | Choice (`128k`–`320k`) | `128k` | Target MP3 bitrate |
| *(None)* | `--cover` | Flag | `False` | Retain embedded cover art |
| *(None)* | `--flat` | Flag | `False` | Flatten subfolder structure |

---

## 💡 Example Usage

#### Standard Conversion (128k Default)
```bash
python3 portableMP3.py -i ~/Music/Unprocessed -o ~/Music/Portable
