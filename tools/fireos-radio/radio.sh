#!/bin/bash

# --- CONFIGURATION ---
# Adjust these to tune your stream stability
BUFFER_BYTES="10M"
CACHE_SECS=60
# ---------------------

# Default runtime value in minutes
MINUTES=90

usage() { 
    echo "Usage: $0 [-m minutes]" 1>&2
    exit 1
}

while getopts "m:" opt; do
  case "${opt}" in
    m) MINUTES=${OPTARG} ;;
    *) usage ;;
  esac
done

DURATION_SECONDS=$((MINUTES * 60))

# Format: "Display Name|Stream URL|Needs Demuxer Flag"
options=(
    "Brony Radio Germany Night DJ|http://radio.bronyradiogermany.com:8003/nightdj|N"
    "PonyVilleFM Luna|https://luna.ponyvillefm.com/listen/lunaradio/radio.mp3|N"
    "Brony Radio Germany Mobile|http://radio.bronyradiogermany.com:8000/mobile|N"
    "PonyVilleFM one-MP3|https://dj.bronyradio.com/stream.mp3|N"
    "PonyVilleFM one-AAC|https://dj.bronyradio.com/pvfm1mobile.aac|Y"
    "Radio Brony France|https://radio.radiobrony.fr/ogg|N"
    "Everhoof 320 MP3|http://everhoof.ru:8000/320|N"
    "Everhoof 32 AAC+|http://everhoof.ru:8000/32|Y"
)

PS3="Select a station number (or choose Quit): "

echo "======================================"
echo "    Equestrian Radio Launcher Menu   "
echo "======================================"
echo "Session Duration: $MINUTES minutes"
echo "Cache Settings: ${CACHE_SECS}s / ${BUFFER_BYTES}"
echo "--------------------------------------"

select opt in "${options[@]%%|*}" "Quit"; do
    if [[ "$opt" == "Quit" ]]; then
        echo "Exiting."
        break
    fi
    
    for item in "${options[@]}"; do
        if [[ "$item" == "$opt"* ]]; then
            URL=$(echo "$item" | cut -d'|' -f2)
            NEED_DEMUX=$(echo "$item" | cut -d'|' -f3)
        fi
    done

    if [[ -z "$URL" ]]; then
        echo "Invalid selection. Please try again."
        continue
    fi

    echo "--------------------------------------"
    echo "Starting: $opt"
    echo "--------------------------------------"
    
    echo "[System] Requesting Android Wake Lock..."
    termux-wake-lock
    
    # Build the mpv command securely using a Bash array
    # Build the mpv command securely using a Bash array
    cmd=(
        mpv
        --ao=opensles
        --cache=yes
        --cache-secs="$CACHE_SECS"
        --demuxer-max-bytes="$BUFFER_BYTES"
        --length="$DURATION_SECONDS"
        --stream-lavf-o-add=reconnect=1
        --stream-lavf-o-add=reconnect_streamed=1
        --stream-lavf-o-add=reconnect_delay_max=5
        --msg-level=all=status
    )
    
    if [[ "$NEED_DEMUX" == "Y" ]]; then
        cmd+=(--demuxer-lavf-format=aac --demuxer=lavf)
    fi
    
    # Append the selected stream URL
    cmd+=("$URL")
    
    # Execute the array cleanly
    "${cmd[@]}"
    
    echo "[System] Stream finished. Releasing Wake Lock..."
    termux-wake-unlock
    break
done
PS3="Select a station number (or choose Quit): "

echo "======================================"
echo "    Equestrian Radio Launcher Menu   "
echo "======================================"
echo "Session Duration: $MINUTES minutes"
echo "Cache Settings: ${CACHE_SECS}s / ${BUFFER_BYTES}"
echo "--------------------------------------"

select opt in "${options[@]%%|*}" "Quit"; do
    if [[ "$opt" == "Quit" ]]; then
        echo "Exiting."
        break
    fi
    
    for item in "${options[@]}"; do
        if [[ "$item" == "$opt"* ]]; then
            URL=$(echo "$item" | cut -d'|' -f2)
            NEED_DEMUX=$(echo "$item" | cut -d'|' -f3)
        fi
    done

    if [[ -z "$URL" ]]; then
        echo "Invalid selection. Please try again."
        continue
    fi

    echo "--------------------------------------"
    echo "Starting: $opt"
    echo "--------------------------------------"
    
    echo "[System] Requesting Android Wake Lock..."
    termux-wake-lock
    
    CMD="mpv --ao=opensles \
        --cache=yes \
        --cache-secs=$CACHE_SECS \
        --demuxer-max-bytes=$BUFFER_BYTES \
        --length=$DURATION_SECONDS \
        --msg-level=all=status"
    
    if [[ "$NEED_DEMUX" == "Y" ]]; then
        CMD="$CMD --demuxer-lavf-format=aac --demuxer=lavf"
    fi
    
    $CMD "$URL"
    
    echo "[System] Stream finished. Releasing Wake Lock..."
    termux-wake-unlock
    break
done
