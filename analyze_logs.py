#!/usr/bin/env python3
import os, glob, pandas as pd, matplotlib.pyplot as plt

plt.style.use("ggplot")

def load_all_logs():
    files = sorted(glob.glob("logs/test_payload*.csv"))
    if not files:
        print("❌ No CSV files found in ./logs/")
        return []
    datasets = []
    for f in files:
        df = pd.read_csv(f)
        df["file"] = os.path.basename(f)
        # infer payload size from filename or column
        try:
            df["payload_B"] = int(f.split("payload")[1].split("_")[0])
        except Exception:
            pass
        datasets.append(df)
    return datasets

def plot_delay_histograms(datasets):
    plt.figure(figsize=(8,5))
    for df in datasets:
        plt.hist(df["rtt_ms"].astype(float), bins=30, alpha=0.5, label=f"{df['payload_B'].iloc[0]} B")
    plt.xlabel("Round-trip delay [ms]")
    plt.ylabel("Count")
    plt.title("Packet delay distribution")
    plt.legend()
    plt.tight_layout()
    plt.savefig("delay_histograms.png", dpi=200)
    plt.show()

def plot_throughput_over_time(datasets):
    plt.figure(figsize=(8,5))
    for df in datasets:
        df = df.sort_values("t_ack")
        t0 = df["t_ack"].iloc[0]
        t = df["t_ack"] - t0
        thr = df["throughput_Bps"]
        plt.plot(t, thr, label=f"{df['payload_B'].iloc[0]} B")
    plt.xlabel("Time [s]")
    plt.ylabel("Throughput [B/s]")
    plt.title("Throughput over time")
    plt.legend()
    plt.tight_layout()
    plt.savefig("throughput_time.png", dpi=200)
    plt.show()

def plot_summary_bar(datasets):
    summary = []
    for df in datasets:
        payload = df["payload_B"].iloc[0]
        thr_mean = df["throughput_Bps"].mean()
        thr_std = df["throughput_Bps"].std()
        delay_mean = df["rtt_ms"].mean()
        summary.append((payload, thr_mean, thr_std, delay_mean))
    s = pd.DataFrame(summary, columns=["payload_B","thr_mean","thr_std","delay_mean"])
    s = s.sort_values("payload_B")

    fig, ax1 = plt.subplots(figsize=(7,4))
    ax1.bar(s["payload_B"], s["thr_mean"], yerr=s["thr_std"], alpha=0.7, width=40)
    ax1.set_xlabel("Payload size [B]")
    ax1.set_ylabel("Throughput [B/s]")
    ax1.set_title("Average throughput per payload")
    for x, y in zip(s["payload_B"], s["thr_mean"]):
        ax1.text(x, y+10, f"{y:.0f}", ha="center", fontsize=8)
    plt.tight_layout()
    plt.savefig("summary_throughput.png", dpi=200)
    plt.show()

def main():
    datasets = load_all_logs()
    if not datasets:
        return
    plot_delay_histograms(datasets)
    plot_throughput_over_time(datasets)
    plot_summary_bar(datasets)

if __name__ == "__main__":
    main()
