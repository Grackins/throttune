import logging
import random
import threading
import time
from serial import Serial


class SerialReader:
    def __init__(self, port='COM1', baudrate=9600, timeout=1):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.capture = True
        self.ser = Serial(port, baudrate, timeout=timeout)

    def write(self, msg, end='\n'):
        self.ser.write(f'{msg}{end}'.encode())

    def start_daemon(self, buf):
        self.daemon_running = True
        self.thread = threading.Thread(
            target=self._daemon_routine,
            args=(buf,),
            daemon=True,
        )
        self.thread.start()

    def pause_daemon(self):
        self.capture = False

    def continue_daemon(self):
        self.capture = True

    def stop_daemon(self):
        self.daemon_running = False
        self.thread.join()

    def _daemon_routine(self, buf):
        while self.ser.is_open and self.daemon_running:
            line = self.ser.readline()
            if '\n' not in line or not self.capture:
                continue
            value = int(line)
            buf.append(value)
        logging.info('Shutting down serial reader')
        return


class FakeReader:
    def __init__(self, port='COM1', baudrate=9600, timeout=1):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.capture = True

    def write(self, msg, end='\n'):
        pass

    def start_daemon(self, buf):
        self.daemon_running = True
        self.thread = threading.Thread(
            target=self._daemon_routine,
            args=(buf,),
            daemon=True,
        )
        self.thread.start()

    def pause_daemon(self):
        self.capture = False

    def continue_daemon(self):
        self.capture = True

    def stop_daemon(self):
        self.daemon_running = False
        self.thread.join()

    def _daemon_routine(self, buf):
        while self.daemon_running:
            if not self.capture:
                continue
            value = random.randint(100, 900)
            buf.append(value)
            time.sleep(0.001)
        logging.info('Shutting down serial reader')
        return
