#!/usr/bin/env python3
import serial
import serial.tools.list_ports
import sys
import threading
import time

# --------------------------------------------------
# auto-detect the arduino ports
# --------------------------------------------------
def list_arduino_ports():
    ports = []
    for port in serial.tools.list_ports.comports():
        if ("Arduino" in port.description
            or "usbmodem" in port.device
            or "usbserial" in port.device
            or "wchusbserial" in port.device):
            ports.append(port.device)
    return ports


# --------------------------------------------------
# background reader (shows device responses)
# --------------------------------------------------
def reader_thread(ser, flag):
    while not flag["stop"]:
        try:
            line = ser.readline().decode(errors="ignore").strip()
            if not line:
                continue
            print(f"[ARDUINO] {line}")
            if line.startswith("m[D]"):
                flag["ready"] = True
        except serial.SerialException:
            break


# --------------------------------------------------
# main
# --------------------------------------------------
def run_test(addr, dest, payload_size, total_packets, ser, delay_ms, flag):
    # state flags
    
    
    payload = b"X" * payload_size["payload"]
    msg_prefix = b"m[" + payload + b"\x00," + dest.encode("ascii") + b"]\n"
    
    print(f"\n🚀 Starting saturation test: {addr} → {dest}, {payload_size} B × {total_packets}")
    sent = 0
    t0 = time.time()
    # kick-off first packet
    ser.write(msg_prefix)
    sent += 1
    print(f"[{sent}/{total_packets}]", end="", flush=True)

    try:
        while sent < total_packets:
            if flag["ready"]:
                flag["ready"] = False
                if delay_ms > 0:
                    time.sleep(delay_ms / 1000.0)
                ser.write(msg_prefix)
                sent += 1
                print(f"\r[{sent}/{total_packets}]", end="", flush=True)
        # wait a moment for final ACKs
        time.sleep(0.5)
    except KeyboardInterrupt:
        print("\n🛑 Interrupted.")

    elapsed = time.time() - t0
    print(f"\n\n✅ Done. Sent {sent} packets in {elapsed:.2f}s ({sent/elapsed:.1f} pkt/s)\n")

def main():
    ports = list_arduino_ports()
    if not ports:
        print("❌ No Arduino devices found.")
        sys.exit(1)

    # select port
    port = ports[0] if len(ports) == 1 else None
    if not port:
        print("Multiple Arduinos found:")
        for i, p in enumerate(ports):
            print(f"  [{i}] {p}")
        port = ports[int(input("Select number: "))]

    print(f"🔌 Connecting to {port} at 115200 baud…")
    try:
        ser = serial.Serial(port, 115200, timeout=0.1)
    except serial.SerialException as e:
        sys.exit(f"Failed to open {port}: {e}")

    # initialize (reset + set address)
    time.sleep(2)
    ser.write(b"r\n")
    time.sleep(0.2)
    
    print("setting retransmission number to 3")
    ser.write(b"c[1,0,3]")

    addr = input("Sender address (e.g. AA): ").strip().upper() or "AA"
    dest = input("Destination (e.g. BB): ").strip().upper() or "BB"
    total_packets = 100
    delay_ms = float(10)

    ser.write(f"a[{addr}]\n".encode())

    test_payload = [
        {"payload": 1},
        {"payload": 100},
        {"payload": 180}
    ]
    
    flag = {"stop": False, "ready": False}
    threading.Thread(target=reader_thread, args=(ser, flag), daemon=True).start()
    
    try:
        for pld in test_payload:
            run_test(addr, dest, pld, total_packets, ser, delay_ms, flag)
    except KeyboardInterrupt:
        print("\n🛑 Interrupted.")
    finally:
        flag["stop"] = True
        ser.close()
        
    print("All Tests Done.")

if __name__ == "__main__":
    main()
