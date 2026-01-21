import serial
import serial.tools.list_ports
import sys
import threading

def list_arduino_ports():
    ports = []
    for port in serial.tools.list_ports.comports():
        if ("Arduino" in port.description
            or "usbmodem" in port.device
            or "usbserial" in port.device
            or "wchusbserial" in port.device):
            ports.append(port.device)
    return ports

def read_from_arduino(ser):
    while True:
        line = ser.readline().decode(errors="ignore").strip()
        if line:
            print(f"[ARDUINO] {line}")

def main():
    ports = list_arduino_ports()
    if not ports:
        print("No Arduino devices found.")
        sys.exit(1)

    # automatic if only one
    if len(ports) == 1:
        port = ports[0]
        print(f"Automatically selected {port}")
    else:
        print("Multiple Arduinos detected:\n")
        for i, p in enumerate(ports):
            print(f"  [{i}] {p}")
        choice = input("\nSelect device number: ")
        try:
            port = ports[int(choice)]
        except (ValueError, IndexError):
            print("Invalid choice.")
            sys.exit(1)

    print(f"Connecting to {port} at 115200 baud...")
    try:
        ser = serial.Serial(port, 115200, timeout=1)
    except serial.SerialException as e:
        print(f"Failed to open {port}: {e}")
        sys.exit(1)

    threading.Thread(target=read_from_arduino, args=(ser,), daemon=True).start()
    
    ser.write(b"r\n");
    ser.write(b"c[1,0,3]"); ser.write(b"c[1,1,0]"); ser.write(b"c[1,2,1]")
    ser.write(b"c[1,3,1]"); ser.write(b"c[0,3,1]"); ser.write(b"c[0,1,0]")
    ser.write(b"c[0,2,255]")

    print("Type messages to send. Ctrl+C to exit.\n")
    try:
        while True:
            msg = input("> ")
            if msg.startswith("m[") and "\\0" in msg:
                msg = msg.replace("\\0", "\x00")
            ser.write((msg + "\n").encode("latin1"))
            if msg.strip().lower() == "clear":
                print("\033c", end="")
    except KeyboardInterrupt:
        print(f"\nDisconnected from {port}")
        ser.close()

if __name__ == "__main__":
    main()
