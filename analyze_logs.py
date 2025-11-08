#!/usr/bin/env python3
import os, glob, pandas as pd, matplotlib.pyplot as plt
import numpy as np
import scipy.stats as st
from scipy.stats import gaussian_kde

plt.style.use("ggplot")

IMG_DIR = "img"

def make_dir(path):
    os.makedirs(path, exist_ok=True)

def next_run_dir(base="img"):
    os.makedirs(base, exist_ok=True)
    runs = [d for d in os.listdir(base) if d.startswith("run")]
    if not runs:
        return os.path.join(base, "run01")
    last = sorted(runs)[-1]
    last_num = int(last.replace("run", ""))
    new_dir = os.path.join(base, f"run{last_num+1:02d}")
    return new_dir


def load_all_logs():
    files = sorted(glob.glob("logs/test_payload*.csv"))
    if not files:
        print("❌ No CSV files found in ./logs/")
        return []
    datasets = []
    for f in files:
        df = pd.read_csv(f)
        df["file"] = os.path.basename(f)
        try:
            df["payload_B"] = int(f.split("payload")[1].split("_")[0])
        except Exception:
            pass
        datasets.append(df)
    return datasets

# === PLOTTING HELPERS ===

from scipy.stats import gaussian_kde

def plot_pdf_cdf(df, outdir):
    """Smooth PDF and CDF of RTTs on shared x-axis."""
    delays = df["rtt_ms"].astype(float).dropna()
    if len(delays) < 5:
        print(f"⚠️ Not enough data points for smooth PDF/CDF in {outdir}")
        return

    # Smooth density estimate
    kde = gaussian_kde(delays)
    xs = np.linspace(delays.min(), delays.max(), 200)
    pdf_y = kde(xs)
    cdf_y = np.cumsum(pdf_y)
    cdf_y /= cdf_y[-1]  # normalize to [0,1]

    fig, ax1 = plt.subplots(figsize=(7,4))
    color1 = "tab:blue"
    ax1.plot(xs, pdf_y, color=color1, linewidth=1.5, label="PDF")
    ax1.set_xlabel("Round-trip delay [ms]")
    ax1.set_ylabel("Probability density", color=color1)
    ax1.tick_params(axis="y", labelcolor=color1)
    ax1.grid(True, linestyle="--", alpha=0.3)

    ax2 = ax1.twinx()
    color2 = "tab:orange"
    ax2.plot(xs, cdf_y, color=color2, linewidth=1.5, linestyle="--", label="CDF")
    ax2.set_ylabel("Cumulative probability", color=color2)
    ax2.tick_params(axis="y", labelcolor=color2)

    fig.suptitle("Delay PDF and CDF")
    fig.tight_layout()
    plt.savefig(f"{outdir}/delay_pdf_cdf.png", dpi=200)
    plt.close()



def plot_throughput_delay_time(df, outdir):
    """Plot throughput and delay over time (dual y-axes, scaled out, smooth)."""
    df = df.sort_values("t_ack")
    t0 = df["t_ack"].iloc[0]
    t = df["t_ack"] - t0

    thr = df["throughput_Bps"].astype(float)
    delay = df["rtt_ms"].astype(float)

    # Optional: smooth throughput slightly (window=10 samples)
    if len(thr) > 10:
        thr_smooth = thr.rolling(window=10, min_periods=1).mean()
    else:
        thr_smooth = thr

    fig, ax1 = plt.subplots(figsize=(8,4.5))
    color1 = "tab:blue"
    ax1.plot(t, thr_smooth, color=color1, label="Throughput", linewidth=1.2, alpha=0.9)
    ax1.set_xlabel("Time [s]")
    ax1.set_ylabel("Throughput [B/s]", color=color1)
    ax1.tick_params(axis="y", labelcolor=color1)
    ax1.grid(True, linestyle="--", alpha=0.3)

    # Expand y-limits by 10% for visual breathing room
    thr_min, thr_max = thr.min(), thr.max()
    ax1.set_ylim(thr_min - 0.1*(thr_max - thr_min),
                 thr_max + 0.1*(thr_max - thr_min))

    ax2 = ax1.twinx()
    color2 = "tab:red"
    ax2.plot(t, delay, color=color2, label="Delay", linewidth=1.0, alpha=0.7)
    ax2.set_ylabel("Round-trip delay [ms]", color=color2)
    ax2.tick_params(axis="y", labelcolor=color2)

    # Expand delay limits by 10%
    dmin, dmax = delay.min(), delay.max()
    ax2.set_ylim(dmin - 0.1*(dmax - dmin),
                 dmax + 0.1*(dmax - dmin))

    fig.suptitle("Throughput and Delay over Time")
    fig.tight_layout()
    plt.savefig(f"{outdir}/throughput_delay_time.png", dpi=200)
    plt.close()


def plot_throughput_vs_payload(datasets, outdir):
    summary = []
    for df in datasets:
        payload = df["payload_B"].iloc[0]
        thr = df["throughput_Bps"].astype(float)
        thr_mean = thr.mean()
        thr_std = thr.std()
        ci = st.t.interval(0.95, len(thr)-1, loc=thr_mean, scale=st.sem(thr))
        summary.append((payload, thr_mean, thr_std, ci[0], ci[1]))

    s = pd.DataFrame(summary, columns=["payload_B","mean","std","ci_low","ci_high"]).sort_values("payload_B")

    plt.figure(figsize=(6.5,4))
    plt.errorbar(s["payload_B"], s["mean"],
                 yerr=[s["mean"]-s["ci_low"], s["ci_high"]-s["mean"]],
                 fmt='o-', capsize=5, lw=1.5)
    plt.xlabel("Payload size [B]")
    plt.ylabel("Throughput [B/s]")
    plt.title("Throughput vs Payload (95% CI)")
    plt.grid(True, linestyle="--", alpha=0.3)
    plt.tight_layout()
    plt.savefig(f"{outdir}/throughput_vs_payload.png", dpi=200)
    plt.close()

def plot_summary_with_ci(df, outdir):
    thr = df["throughput_Bps"].dropna().astype(float)
    delay = df["rtt_ms"].dropna().astype(float)
    thr_mean, delay_mean = thr.mean(), delay.mean()
    thr_std, delay_std = thr.std(), delay.std()
    n_thr, n_delay = len(thr), len(delay)

    ci_thr = st.t.interval(0.95, n_thr-1, loc=thr_mean, scale=st.sem(thr))
    ci_delay = st.t.interval(0.95, n_delay-1, loc=delay_mean, scale=st.sem(delay))

    stats = pd.DataFrame({
        "metric": ["Throughput [B/s]", "Delay [ms]"],
        "mean": [thr_mean, delay_mean],
        "std": [thr_std, delay_std],
        "ci_low": [ci_thr[0], ci_delay[0]],
        "ci_high": [ci_thr[1], ci_delay[1]]
    })
    print(f"\n📊 Stats for {os.path.basename(outdir)}:")
    print(stats.round(2))

    # simple bar summary
    plt.figure(figsize=(6,4))
    plt.bar(["Throughput","Delay"], [thr_mean, delay_mean],
            yerr=[thr_std, delay_std], capsize=5, alpha=0.7)
    plt.title("Mean and Std per Metric")
    plt.tight_layout()
    plt.savefig(f"{outdir}/summary_bar.png", dpi=200)
    plt.close()
    
def plot_delay_per_byte_vs_payload(datasets, outdir):
    summary = []
    for df in datasets:
        payload = df["payload_B"].iloc[0]
        delay_per_byte = (df["rtt_ms"].astype(float) / df["payload_B"]).dropna()
        mean = delay_per_byte.mean()
        ci = st.t.interval(0.95, len(delay_per_byte)-1, loc=mean, scale=st.sem(delay_per_byte))
        summary.append((payload, mean, ci[0], ci[1]))

    s = pd.DataFrame(summary, columns=["payload_B","mean","ci_low","ci_high"]).sort_values("payload_B")

    plt.figure(figsize=(6.5,4))
    plt.errorbar(s["payload_B"], s["mean"],
                 yerr=[s["mean"]-s["ci_low"], s["ci_high"]-s["mean"]],
                 fmt='o-', color="tab:red", capsize=5, lw=1.5)
    plt.xlabel("Payload size [B]")
    plt.ylabel("Delay per byte [ms/B]")
    plt.title("Normalized delay vs payload (95% CI)")
    plt.grid(True, linestyle="--", alpha=0.3)
    plt.tight_layout()
    plt.savefig(f"{outdir}/delay_per_byte_vs_payload.png", dpi=200)
    plt.close()



# === MAIN ===

def main():
    datasets = load_all_logs()
    if not datasets:
        return

    run_dir = next_run_dir(IMG_DIR)
    make_dir(run_dir)

    for df in datasets:
        payload = df["payload_B"].iloc[0]
        payload_dir = os.path.join(run_dir, f"{payload}B")
        make_dir(payload_dir)
        print(f"🧪 Processing payload={payload}B → {payload_dir}")
        plot_pdf_cdf(df, payload_dir)
        plot_throughput_delay_time(df, payload_dir)
        plot_summary_with_ci(df, payload_dir)
        
    plot_throughput_vs_payload(datasets, run_dir)
    plot_delay_per_byte_vs_payload(datasets, run_dir)

    print(f"\n✅ All graphs saved in: {run_dir}/")

if __name__ == "__main__":
    main()
