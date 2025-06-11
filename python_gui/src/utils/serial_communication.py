import serial
import time
from queue import Queue
from threading import Thread

def recv(ser, x):
    time.sleep(0.01)
    if ser.in_waiting > 0:
        data = ser.read(1)
        return data + ser.read(min(x - 1, ser.in_waiting))
    return b''

class SerialHandler:
    def __init__(self, port, baudrate):
        self.serial = serial.Serial(port=port, baudrate=baudrate, timeout=1)
        self.running = True
        self.data_queue = Queue()
        self.read_thread = None
        
    def start_reading(self):
        self.read_thread = Thread(target=self._read_loop, daemon=True)
        self.read_thread.start()
        
    def _read_loop(self):
        buffer = ""
        while self.running:
            try:
                if self.serial.in_waiting > 0:
                    line = self.serial.readline().decode('utf-8')
                    if line:
                        buffer += line
                        lines = buffer.split('\n')
                        buffer = lines[-1]
                        
                        for line in lines[:-1]:
                            line = line.strip()
                            if line:
                                self.data_queue.put(line)
            except Exception as e:
                print(f"Error reading serial data: {e}")
                time.sleep(0.001)
                
    def send_command(self, command):
        self.serial.write(f"{command}\n".encode('utf-8'))
        
    def get_data(self):
        return self.data_queue.get() if not self.data_queue.empty() else None
        
    def close(self):
        self.running = False
        if self.read_thread:
            self.read_thread.join(timeout=1.0)
        if self.serial and self.serial.is_open:
            self.serial.close() 