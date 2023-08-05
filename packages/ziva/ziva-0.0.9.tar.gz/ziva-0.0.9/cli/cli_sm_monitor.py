import argparse
import logging
import os
import sys
from concurrent.futures import ThreadPoolExecutor
sys.path.append('..')
sys.path.append('.')
from ziva.serialib import serial_ports, autodetermine_port
from ziva.sm_monitor import SmMonitor

logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser()
parser.add_argument('-port', help="Serial port. Port is automatically set by default")
parser.add_argument('-baud', default=38400, help="Serial port baudrate")
parser.add_argument('-dir', default='', help="Directory to store data in")
parser.add_argument('-loglevel', default='debug', choices=["debug", "info", "warning", "error", "exception"],
                    help="Loglevel")
args = parser.parse_args()


def get_input_text():
    input_text = 'Press key for specific task: \n' \
                 's) Start monitoring \n' \
                 't) Terminate/stop monitoring \n' \
                 'q) Quit\n'
    return input_text


def main(port, baud, directory):
    if not port:
        if len(serial_ports()) == 0:
            print('No serial port detected')
            return

        elif len(serial_ports()) > 1:
            print('Multiple serial ports detected. Please select one:')
            for i, p in enumerate(serial_ports()):
                print(f"{i+1}) {p}")
            port_number = int(input(""))
            port = serial_ports()[port_number - 1].split(' - ')[0]
        else:
            port = autodetermine_port()

    executor = ThreadPoolExecutor(max_workers=1)
    sm = SmMonitor()
    sm.directory = directory
    while True:
        try:
            key = input(get_input_text())
            if key == 's':
                try:
                    if sm.running:
                        raise Exception('Already running')
                    if not os.path.exists(directory):
                        raise Exception('Directory does not exists')
                    sm.set(port=port, baudrate=baud, timeout=1)
                    sm.test_router()
                    executor.submit(sm.start)
                except Exception as e:
                    logger.exception(e)
            elif key == 't':
                sm.stop()
            elif key == 'q':
                if sm.running:
                    sm.stop()
                break
        except KeyboardInterrupt:
            if sm.running:
                sm.stop()
            break


if __name__ == '__main__':
    formatter = "[%(asctime)s] %(name)s {%(filename)s:%(lineno)d} %(levelname)s - %(message)s"
    logging.basicConfig(format=formatter)
    logging.root.setLevel(args.loglevel.upper())
    main(port=args.port, baud=args.baud, directory=args.dir)
