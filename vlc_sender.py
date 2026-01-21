#!/usr/bin/env python3
import serial, serial.tools.list_ports, sys, threading, time, csv, os, itertools
from datetime import datetime
from collections import deque

#  auto-detect the arduino ports
def list_arduino_ports():
    return [
        p.device for p in serial.tools.list_ports.comports()
        if ("Arduino" in p.description
            or "usbmodem" in p.device
            or "usbserial" in p.device
            or "wchusbserial" in p.device)
    ]

#  background reader — collects delivery messages
def reader_thread(ser, flag):
    q = flag["rx"]
    while not flag["stop"]:
        try:
            line = ser.readline().decode(errors="ignore").strip()
            if not line:
                continue
            q.append((time.time(), line))
            if line.startswith("m[D]"):
                flag["ready"] = True
        except serial.SerialException:
            break

#  CSV helper
def make_logger(payload_size):
    os.makedirs("logs", exist_ok=True)
    now = datetime.now().strftime("%Y%m%d-%H%M%S")
    fname = f"logs/test_payload{payload_size}_{now}.csv"
    f = open(fname, "w", newline="")
    w = csv.writer(f)
    w.writerow(["seq","t_send","t_ack","rtt_ms","status","payload_B","throughput_Bps"])
    return f, w, fname

#  single experiment
def run_test(addr, dest, payload_B, total_packets, ser, delay_ms, flag):
    msg = b"m[" + (b"X" * payload_B) + b"\x00," + dest.encode("ascii") + b"]\n"

    f, w, path = make_logger(payload_B)
    print(f"\n=== {payload_B}-byte payload test — logging to {path} ===")
    spinner = itertools.cycle("⠋⠙⠹⠸⠼⠴⠦⠧⠇⠏")

    sent = 0
    delivered = 0
    t_first, t_last = None, None
    sent_time = {}
    seq = 0
    flag["rx"].clear()

    ser.write(msg)
    sent_time[seq] = time.time()
    t_first = sent_time[seq]
    sent += 1

    try:
        last_update = 0
        last_ack_time = time.time()
        idle_timeout = 1.0  # seconds without new ack before ending

        while delivered < total_packets:
            # check if new delivery lines arrived
            while flag["rx"]:
                t_rx, line = flag["rx"].popleft()
                if line.startswith("m[D]"):
                    t_ack = t_rx
                    if not sent_time:
                        continue
                    seq_i, t_send = max(sent_time.items(), key=lambda kv: kv[1])
                    rtt = (t_ack - t_send) * 1000
                    delivered += 1
                    t_last = t_ack
                    throughput = (payload_B * delivered) / (t_last - t_first)
                    w.writerow([seq_i, t_send, t_ack, f"{rtt:.3f}", "ok", payload_B, f"{throughput:.2f}"])
                    f.flush()
                    sent_time.pop(seq_i, None)
                    flag["ready"] = True
                    last_ack_time = time.time()

            # if no ack for >idle_timeout and everything sent, break
            if sent >= total_packets and (time.time() - last_ack_time) > idle_timeout:
                break

            if flag["ready"] and sent < total_packets:
                flag["ready"] = False
                if delay_ms > 0:
                    time.sleep(delay_ms / 1000.0)
                seq += 1
                ser.write(msg)
                sent_time[seq] = time.time()
                sent += 1

            now = time.time()
            if now - last_update > 0.1:
                sys.stdout.write(f"\r{next(spinner)}  {delivered}/{total_packets}")
                sys.stdout.flush()
                last_update = now

        print(f"\rDone — {delivered}/{total_packets} packets delivered.")
    except KeyboardInterrupt:
        print("\nInterrupted.")
    finally:
        if t_first and t_last:
            duration = t_last - t_first
            thr = (payload_B * delivered) / duration
            print(f"   Duration: {duration:.2f}s   ⚡ Throughput: {thr:.1f} B/s")
        f.close()
        time.sleep(0.5)


#  main
def main():
    ports = list_arduino_ports()
    if not ports:
        sys.exit("No Arduino devices found.")
    port = ports[0] if len(ports) == 1 else None
    if not port:
        for i, p in enumerate(ports):
            print(f"  [{i}] {p}")
        port = ports[int(input("Select number: "))]

    print(f"Connecting to {port} at 115200 baud…")
    try:
        ser = serial.Serial(port, 115200, timeout=0.1)
    except serial.SerialException as e:
        sys.exit(f"Failed to open {port}: {e}")

    # init + config
    time.sleep(2)
    ser.write(b"r\n"); time.sleep(0.2)
    ser.write(b"c[1,0,3]"); ser.write(b"c[1,1,0]"); ser.write(b"c[1,2,1]")
    ser.write(b"c[1,3,1]"); ser.write(b"c[0,3,1]"); ser.write(b"c[0,1,0]")
    ser.write(b"c[0,2,255]")

    addr = input("Sender address (default AA): ").strip().upper() or "AA"
    dest = input("Destination (default BB): ").strip().upper() or "BB"
    ser.write(f"a[{addr}]\n".encode())

    total_packets = 50
    delay_ms = 10.0
    test_payloads = [1, 100, 180]

    flag = {"stop": False, "ready": False, "rx": deque(maxlen=4096)}
    threading.Thread(target=reader_thread, args=(ser, flag), daemon=True).start()

    try:
        for p in test_payloads:
            run_test(addr, dest, p, total_packets, ser, delay_ms, flag)
    finally:
        flag["stop"] = True
        ser.close()
        print("\nAll tests complete. Logs saved in ./logs/")
        

if __name__ == "__main__":
    main()
