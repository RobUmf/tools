# FireOS Equestrian Radio Launcher

A lightweight Bash script optimized for running `mpv` inside Termux on an Amazon Fire Tablet. It includes robust audio caching to handle local network congestion and automated wake-lock management to prevent FireOS from killing the stream when the screen turns off.

## Features
*   **Persistent Playback:** Uses `termux-wake-lock` to keep the audio stream active during sleep state.
*   **WiFi Jitter Buffer:** Configured with a deep 60-second / 100MiB cache to smooth over local network traffic spikes.
*   **Custom Sleep Timer:** Built-in sleep duration flag (defaults to 90 minutes).
*   **Pre-configured Streams:** Streamlined for major fandom stations including PonyVilleFM and Brony Radio Germany.

## Installation & Setup

1. Clone or copy `radio.sh` into your Termux environment (recommended path: `~/storage/shared/scripts/`).
2. Ensure the script has executable permissions:
   ```bash
   chmod +x radio.sh

# Run for the default 90 minutes
bash radio.sh

# Run for a 5-minute test or short session
bash radio.sh -m 5

Quick Access Tip
To bypass navigating directories every time, add an alias to your ~/.bashrc:
