import time
from collections import deque

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from pylsl import resolve_byprop, StreamInlet

STREAM_NAME = "EEG_SIM"   # change to EEG_SIM if you're using the simulator
WINDOW_SEC = 5              # how many seconds to display
PLOT_CHANNELS = [0, 1, 2]    # which channels to plot (0-based). Use [0] for one channel.

def main():
    print(f"Resolving LSL stream name={STREAM_NAME} ...")
    streams = resolve_byprop("name", STREAM_NAME, timeout=10)
    if not streams:
        raise SystemExit(f"Stream not found: {STREAM_NAME}")

    inlet = StreamInlet(streams[0])

    # Try to infer stream properties
    info = inlet.info()
    ch = info.channel_count()
    srate = int(info.nominal_srate()) if info.nominal_srate() > 0 else 250
    maxlen = max(1, WINDOW_SEC * srate)

    # Buffers (one per plotted channel)
    tbuf = deque(maxlen=maxlen)
    ybuf = {c: deque(maxlen=maxlen) for c in PLOT_CHANNELS}

    # Prepare plot
    fig, ax = plt.subplots()
    lines = {}
    for c in PLOT_CHANNELS:
        (line,) = ax.plot([], [], label=f"ch{c}")
        lines[c] = line

    ax.set_title(f"LSL Live Plot: {STREAM_NAME}")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Value")
    ax.legend(loc="upper right")

    t0 = time.time()

    def update(_frame):
        # Pull a chunk to reduce overhead
        samples, timestamps = inlet.pull_chunk(timeout=0.0, max_samples=64)
        if timestamps:
            for ts, sample in zip(timestamps, samples):
                # Use relative time for x-axis
                t = ts - timestamps[0] + (time.time() - t0)  # stable-ish display
                tbuf.append(t)
                for c in PLOT_CHANNELS:
                    if c < len(sample):
                        ybuf[c].append(sample[c])

        if len(tbuf) < 2:
            return list(lines.values())

        t_arr = np.array(tbuf)
        # Keep x axis as last WINDOW_SEC seconds
        xmin = t_arr[-1] - WINDOW_SEC
        ax.set_xlim(xmin, t_arr[-1])

        # Update each line
        ymin, ymax = None, None
        for c in PLOT_CHANNELS:
            y_arr = np.array(ybuf[c])
            lines[c].set_data(t_arr[-len(y_arr):], y_arr)
            if len(y_arr):
                ymin = y_arr.min() if ymin is None else min(ymin, y_arr.min())
                ymax = y_arr.max() if ymax is None else max(ymax, y_arr.max())

        if ymin is not None and ymax is not None:
            pad = 0.05 * (ymax - ymin + 1e-9)
            ax.set_ylim(ymin - pad, ymax + pad)

        return list(lines.values())

    ani = FuncAnimation(fig, update, interval=30, blit=False)
    plt.show()

if __name__ == "__main__":
    main()
