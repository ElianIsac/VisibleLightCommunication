import serial
import serial.tools.list_ports
import sys
import threading

def find_arduino_port():
    for port in serial.tools.list_ports.comports():
        if ("Arduino" in port.description
            or "usbmodem" in port.device
            or "usbserial" in port.device
            or "wchusbserial" in port.device):
            return port.device
    return None

def read_from_arduino(ser):
    while True:
        line = ser.readline().decode(errors="ignore").strip()
        if line:
            print(f"[ARDUINO] {line}")

def main():
    port = find_arduino_port()
    if not port:
        print("No arduino found.")
        sys.exit(1)
    
    print(f"Connected to {port}")
    ser = serial.Serial(port, 115200, timeout=1)
    
    threading.Thread(target=read_from_arduino, args=(ser, ), daemon=True).start()
    
    print("Type messages to send. Ctrl+C to exit. \n")
    try:
        while True:
            msg = input("> ")
            ser.write((msg + "\n").encode())
    except KeyboardInterrupt:
        ser.close()
        print("\nDisconnected")

if __name__ == "__main__":
    main()