# System Monitor & Music Streaming Tools

A collection of lightweight Linux terminal utilities designed for hardware performance tracking and fandom audio streaming.

---

## 🖥️ AI Pulse Monitor (`monitor.py`)

A standalone Python terminal interface that tracks real-time CPU core load and active network interface speeds using native Linux system data.

### Features
* **Zero Dependencies:** Runs on pure Python without requiring extra library installations.
* **Granular Tracking:** Parses `/proc/stat` directly to calculate independent load balances for every CPU core.
* **Network Speed Meter:** Monitors active data usage throughput (targeted for `enp3s0`, `eth0`, or `wlan0`).
* **Interactive Controls:** Press `p` to freeze/pause the interface layout updates, `r` to resume refreshing, or `q` to quit securely.

---

## 📻 Brony Radio Streamers (`stream_radio.sh` & `listen.sh`)

Bash wrapper tools optimized for fetching and playing curated community audio stations cleanly through the command line.

### Features
* **Playlist Engine:** Reads formatting blocks from a localized `bronyradio.m3u` station directory file.
* **Interactive Search:** Pipes station metadata tags dynamically into `fzf` for smooth keyboard filtering and selection.
* **Background Playback:** Hands off selected audio stream URLs directly to `mpv` for zero-latency background audio processing.

---

## 🛠️ Quick Start

### System Prerequisites
Ensure your Linux environment has the required core streaming binaries available:
```bash
sudo apt install mpv fzf python3