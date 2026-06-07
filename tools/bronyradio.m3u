#!/usr/bin/env python3
import os
import sys
import time
import subprocess
import select
import tty
import termios
from datetime import datetime

# =================================================================
# 1. CONFIGURATION
# =================================================================
PLAYLIST_FILE = "bronyradio.m3u"

class B:
    RED = '\033[38;5;131m'
    GRN = '\033[38;5;65m'
    YEL = '\033[38;5;142m'
    RESET = '\033[0m'
    CLEAR = '\033[H\033[J'
    HIDE_CURSOR = '\033[?25l'
    SHOW_CURSOR = '\033[?25h'

class PulseMonitor:
    def __init__(self, station_name, stream_url):
        self.paused = False
        self.station_name = station_name
        self.stream_url = stream_url
        self.prev_cpu_times = self.get_cpu_times()
        self.prev_net = self.get_net_bytes()
        self.mpv_process = None

    def get_net_bytes(self):
        """Reads network stats and targets active interfaces."""
        try:
            with open('/proc/net/dev', 'r') as f:
                lines = f.readlines()
                for line in lines[2:]:
                    parts = line.split(':')
                    iface = parts[0].strip()
                    # Matches typical Linux interfaces (enp, eth, wlan)
                    if iface in ['enp3s0', 'eth0', 'wlan0']: 
                        return int(parts[1].split()[0])
            # Fallback to the first non-loopback device if specific one isn't matched
            for line in lines[2:]:
                parts = line.split(':')
                if parts[0].strip() != 'lo':
                    return int(parts[1].split()[0])
        except Exception:
            return 0
        return 0

    def get_cpu_times(self):
        cores = {}
        with open('/proc/stat', 'r') as f:
            for line in f:
                if line.startswith('cpu') and line[3].isdigit():
                    parts = line.split()
                    cores[parts[0]] = (sum(float(x) for x in parts[1:]), float(parts[4]))
        return cores

    def calculate_load(self):
        new_times = self.get_cpu_times()
        loads = {}
        for name, (total, idle) in new_times.items():
            prev_total, prev_idle = self.prev_cpu_times.get(name, (0, 0))
            diff_total = total - prev_total
            diff_idle = idle - prev_idle
            loads[name] = 100 * (1 - diff_idle / diff_total) if diff_total > 0 else 0.0
        self.prev_cpu_times = new_times
        return loads

    def start_audio(self):
        """Spawns mpv in the background with output suppressed."""
        if self.stream_url:
            self.mpv_process = subprocess.Popen(
                ['mpv', '--no-video', self.stream_url],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )

    def stop_audio(self):
        """Safely stops the mpv stream."""
        if self.mpv_process:
            self.mpv_process.terminate()
            self.mpv_process.wait()

    def run(self):
        self.start_audio()
        old_settings = termios.tcgetattr(sys.stdin)
        tty.setcbreak(sys.stdin.fileno())
        sys.stdout.write(B.HIDE_CURSOR)
        
        try:
            while True:
                # Core keys: 'p' to pause interface, 'r' to resume, 'q' to quit everything
                if select.select([sys.stdin], [], [], 0)[0]:
                    key = sys.stdin.read(1)
                    if key == 'p': self.paused = True
                    elif key == 'r': self.paused = False
                    elif key == 'q': break

                if not self.paused:
                    loads = self.calculate_load()
                    curr_rx = self.get_net_bytes()
                    net_speed = (curr_rx - self.prev_net) / 1024  # KB/s
                    self.prev_net = curr_rx

                    print(B.CLEAR, end="")
                    print(f"{B.YEL}--- AI PULSE MONITOR & STATION STREAM ---{B.RESET}")
                    print(f"TIME: {datetime.now().strftime('%H:%M:%S')} | NET: {net_speed:.1f} KB/s")
                    print(f"RADIO: {B.GRN}{self.station_name}{B.RESET}")
                    print("-" * 45)
                    
                    for core in sorted(loads.keys()):
                        print(f"{core:<10} LOAD: {loads[core]:.1f}%")

                time.sleep(0.8)
        finally:
            self.stop_audio()
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
            sys.stdout.write(B.SHOW_CURSOR)

def parse_and_select_m3u(playlist_path):
    """Parses M3U tracks manually to feed into fzf selection."""
    if not os.path.exists(playlist_path):
        print(f"Error: {playlist_path} not found.")
        sys.exit(1)
        
    stations = []
    current_name = "Unknown Station"
    
    with open(playlist_path, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            line = line.strip()
            if line.startswith("#EXTINF:"):
                current_name = line.split(',', 1)[-1]
            elif line and not line.startswith("#"):
                stations.append((current_name, line))
                current_name = "Unknown Station"

    if not stations:
        print("No stations parsed from playlist file.")
        sys.exit(1)

    # Use fzf to select the stream
    fzf_input = "\n".join([f"{name} | {url}" for name, url in stations])
    try:
        process = subprocess.Popen(
            ['fzf', '--prompt=Select Radio Station: '],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            text=True
        )
        stdout, _ = process.communicate(input=fzf_input)
        if not stdout.strip():
            return None, None
        
        selected_line = stdout.strip()
        name, url = selected_line.split(" | ", 1)
        return name, url
    except FileNotFoundError:
        # Fallback if fzf is missing on the environment
        print("fzf not found. Defaulting to first available station.")
        return stations[0][0], stations[0][1]

if __name__ == "__main__":
    name, url = parse_and_select_m3u(PLAYLIST_FILE)
    if name and url:
        PulseMonitor(name, url).run()