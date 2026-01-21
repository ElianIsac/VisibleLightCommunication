# Visible Light Communication

This is a project developed during a Wireless Networking course at ETHZ, using arduino boards with a ETH developed VLC firmware.

### Prerequisites
You'll need Python and a few libraries.
```bash
pip install pyserial pandas matplotlib scipy
```

### How to Run It

#### 1. Fire up the Sender
Connect your Arduino(s) and run the sender script. It'll ask you which port to use if it finds a few.
```bash
python vlc_sender.py
```
It will start sending packets.

#### 2. Check the Stats
Once you've done a few runs, you'll have some CSV logs in the `logs/` folder. Time to visualize them!
```bash
python analyze_logs.py
```
This script will look through your `logs/`, crunch the numbers, and save some graphs in the `img/` folder.

## Output
Check the `img/` folder for:
- **Throughput vs Payload**: See how fast you're going.
- **Delay PDF/CDF**: For when you want to know *exactly* how long those packets took.
- **Time Series**: Watch the performance over time.
