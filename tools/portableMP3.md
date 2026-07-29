# Portable MP3 Optimizer (`portableMP3.py`)

A fast, container-friendly Python tool powered by `ffmpeg` to batch-downsample, transcode, clean metadata, and restructure large audio archives. 

Designed for creating lightweight, portable MP3 collections for mobile devices, legacy media players, or car stereos where high-bitrate WAV/FLAC files waste unnecessary storage space.

---

## 🌟 Key Features

* **Universal Audio Input:** Transcodes `.flac`, `.wav`, `.m4a`, and `.mp3` files seamlessly.
* **44.1 kHz Resampling & ID3v3 Normalization:** Standardizes output audio to a clean 44.1 kHz sample rate with ID3v3 tags for maximum compatibility across playback devices.
* **Smart Deduplication:** Automatically resolves instances where duplicate tracks exist across root and nested folders, prioritizing organized subfolder structures.
* **Flexible Directory Structuring:** Retains original folder hierarchies or flattens deeply nested catalogs into a single target directory.
* **Cover Art Preservation:** Optional support to retain embedded album art/video thumbnail streams during conversion.

---

## 📋 Requirements

* **Python 3.10+**
* **FFmpeg** installed and available in your system `PATH`.

To install FFmpeg on Debian/Ubuntu/Linux Mint:
```bash
sudo apt update && sudo apt install ffmpeg
