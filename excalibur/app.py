import logging
import time

from automata.automata import Automata

# ------------------------------------------------------------------------------

class Excalibur():

    def __init__(self):
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(levelname)-8s %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S')
        logging.info("Excalibur start")
        self.automata = Automata()
        self.automata.start()

    def terminate(self):
        self.automata.terminate()
        logging.info("Excalibur terminate")

# ------------------------------------------------------------------------------

if __name__ == '__main__':
    ex = Excalibur()
    time.sleep(10)
    ex.terminate()
    exit(0)
