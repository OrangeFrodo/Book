import serial, struct, time
import numpy as np
from pylsl import StreamInfo, StreamOutlet

PORT = "/dev/ttyACM0"     # change if needed
BAUD = 230400

NUM_CHANNELS = 6
HEADER_LEN = 3
SYNC1 = 0xC7
SYNC2 = 0x7C
END  = 0x01
PACKET_LEN = (NUM_CHANNELS * 2 + HEADER_LEN + 1)

STREAM_NAME = "EEG_SIM"   # your choice
STREAM_TYPE = "EEG"          # or "EMG" etc
SAMPLE_RATE = 500            # matches firmware SAMP_RATE

def read_packet(ser):
    # find sync bytes
    while True:
        b = ser.read(1)
        if not b:
            return None
        if b[0] == SYNC1:
            b2 = ser.read(1)
            if b2 and b2[0] == SYNC2:
                rest = ser.read(PACKET_LEN - 2)
                if len(rest) != PACKET_LEN - 2:
                    return None
                pkt = bytes([SYNC1, SYNC2]) + rest
                if pkt[-1] != END:
                    continue
                return pkt

def main():
    info = StreamInfo(STREAM_NAME, STREAM_TYPE, NUM_CHANNELS, SAMPLE_RATE, 'float32', 'uno-r4-udl-01')
    outlet = StreamOutlet(info)

    with serial.Serial(PORT, BAUD, timeout=1) as ser:
        # handshake / start
        ser.write(b"WHORU\n")
        time.sleep(0.1)
        ser.reset_input_buffer()
        ser.write(b"START\n")

        print(f"Streaming LSL: {STREAM_NAME} ({NUM_CHANNELS}ch @ {SAMPLE_RATE}Hz) from {PORT}")
        while True:
            pkt = read_packet(ser)
            if not pkt:
                continue
            # counter = pkt[2]  # optional
            samples = []
            base = HEADER_LEN
            for ch in range(NUM_CHANNELS):
                hi = pkt[base + 2*ch]
                lo = pkt[base + 2*ch + 1]
                val = (hi << 8) | lo      # 14-bit stored in 16-bit
                samples.append(float(val))
            outlet.push_sample(samples)

if __name__ == "__main__":
    main()
