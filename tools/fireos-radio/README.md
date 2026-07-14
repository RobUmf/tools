# FireOS / Termux Radio Launcher

A lightweight, menu-driven Bash script designed to stream Equestrian and Brony radio stations directly inside Termux on Amazon FireOS or Android tablets. 

This tool is specifically optimized to maintain rock-solid stream stability in high-traffic wireless environments without draining your battery or letting the device fall asleep.

---

## Features

*   **Android Wake Lock Integration:** Automatically requests an Android wake lock (`termux-wake-lock`) when a stream starts, preventing FireOS from aggressively killing the audio process when the screen turns off or goes dim.
*   **Shock-Absorber Buffering:** Customized `mpv` caching parameters engineered to smooth out network jitter and sudden drops in signal.
*   **Dynamic Session Timer:** Run streams with a customizable time limit using standard flags (e.g., timed listening before bed).
*   **Automatic Demuxing:** Smart handling for different stream types (MP3, OGG, OPUS, and AAC+ formats).

---

## Technical Edge & Lessons Learned

During development and testing in high-interference environments, a few critical adjustments were made to bypass `mpv` and Bash constraints:

### 1. The 10M Buffer "Sweet Spot"
While it is tempting to throw a massive buffer limit (like `100MiB` or `1200MiB`) at a choppy network connection, **`mpv` optimizes live network streams aggressively**. If the buffer ceiling is set impossibly high for a live audio stream, `mpv` panics, bypasses the cache rule completely, and defaults to an unbuffered, low-latency live mode (hovering around 400KB–550KB). 
*   **The Fix:** Setting `--demuxer-max-bytes=10M` matches the physical reality of a 128kbps/320kbps radio feed. It gives the player a generous 5-10 minute safety cushion while keeping the cache logic active and stable.

### 2. Deprecation of `--force-cache`
Older `mpv` workarounds utilized `--force-cache=yes` to force a buffer on non-seekable streams. In modern versions of `mpv` (packaged in newer Termux environments), this flag has been completely removed. Including it will cause a **fatal parsing error** and crash the script immediately. 
*   **The Fix:** The script relies on a tuned `--cache=yes` alongside realistic byte/second ceilings.

### 3. Avoid System Variable Shadowing
In Bash, `SECONDS` is a reserved internal shell variable that counts the seconds elapsed since the shell shell session started. Re-assigning it to track stream duration alters the system counter and causes erratic timing behavior. 
*   **The Fix:** Migrated the logic to a custom variable name: `DURATION_SECONDS`.

---

## Installation & Dependencies

Ensure your Termux environment has `mpv` and `termux-api` utilities installed:

```bash
pkg update
pkg install mpv termux-api
