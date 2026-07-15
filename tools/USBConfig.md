# USBtoUSB Transfer Utility

## The Problem
When transferring massive amounts of data directly between two external USB drives, hardware limitations often cause frustrating interruptions. Specifically, power constraints on the USB bus can cause external drives to temporarily disconnect, throttle, or stall under heavy, sustained I/O loads. When using standard terminal commands (like `cp` or `mv`), these drops result in incomplete transfers, corrupted media, and no easy way to resume the process without starting over or manually hunting down which files failed.

## The Solution
`USBtoUSB.py` is a robust Python wrapper designed to handle unstable external drive transfers by prioritizing data integrity, safety, and resume capabilities. 

*   **Resilient Transfers:** By utilizing `rsync` as the backend engine, the script gracefully handles unexpected drive disconnects. If the power dips and the transfer fails, simply running the script again will pick up exactly where it left off by ignoring already existing files.
*   **Data Verification:** It enforces strict file integrity using the `--checksum` flag, guaranteeing that the destination files are exact, uncorrupted 1:1 copies of the raw source data.
*   **Safe Batching:** To prevent overwhelming the USB controller, the script supports batch processing folders by prefix or keyword, allowing you to move massive libraries in manageable chunks.
*   **Controlled Deletion:** It acts as a strict safety net by defaulting to a "COPY" mode. It will only purge source files if explicitly authorized via a manually typed `delete` command during runtime, and only *after* the checksums have successfully matched.

---
## Setup Instructions
Setting Permissions chmod +x USBtoUSB.py
python3 USBtoUSB.py -c

---

## Configuration Keys (`USBConfig.txt`)

The script relies on a configuration file to define the storage pathways for file transfers. This file is generated automatically when you run the script with the `-c` flag, but it can also be edited manually.

Below are the required keys:

*   **`source`**: The absolute path to the directory containing the files or folders you want to transfer.
    *   *Example*: `source=/media/user/Drive_A/Music_Backup`
*   **`internal_buffer`**: The absolute path to a fast internal drive (like an NVMe SSD) used to stage or track transfers. The script will calculate the available free space on this drive during setup to ensure you have enough headroom before executing a move.
    *   *Example*: `internal_buffer=/media/user/Internal_NVMe/0buffer`
*   **`final_dest`**: The absolute path to the target external drive or final resting place for the files.
    *   *Example*: `final_dest=/media/user/Drive_B/Main_Archive`
*   **`max_chunk`**: A reference value (e.g., `150G`) to remind you of the maximum batch size you intend to move at once, preventing buffer overflow or overwhelming the system's I/O capacity.

## Example `USBConfig.txt`

```text
source=/media/robumf/Seagate Basic/UltraStar_Songs_Backup
internal_buffer=/media/robumf/1.5nvme61/0buffer
final_dest=/media/robumf/Sea_Media/USDX_MLK
max_chunk=150G
