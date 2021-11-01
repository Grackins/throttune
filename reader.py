import json
import logging
import threading
import time
from serial import Serial
from math import sin


class SerialReader:
    def __init__(self, port='COM1', baudrate=9600, timeout=1):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.capture = True
        self.ser = Serial(port, baudrate, timeout=timeout)

    def write(self, msg, end='\n'):
        self.ser.write(f'{msg}{end}'.encode())

    def save(self, name):
        with open(f'./data/{name}', 'w') as f:
            json.dump(self.buf, f)

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
        self.buf = buf
        while self.ser.is_open and self.daemon_running:
            line = self.ser.readline()
            if b'\n' not in line or not self.capture:
                continue
            try:
                value = int(line)
                if value <= 100:
                    logging.warning(f'Read bad: "{line}"')
                buf.append(value)
            except Exception:
                logging.warning(f'Ignored value "{line}"')
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

    def save(self, name):
        with open(f'./data/{name}', 'w') as f:
            json.dump(self.buf, f)

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
            x = len(buf) / 1000 * 3.14
            value = sin(x) * 500 + 500
            buf.append(value)
            time.sleep(0.001)
        logging.info('Shutting down serial reader')
        return
