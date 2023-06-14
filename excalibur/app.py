import logging
import time
import os
import argparse

from excalibur.automata.automata import Automata

# ------------------------------------------------------------------------------

EXCALIBUR_NAME="Excalibur NFC-driven media center"
EXCALIBUR_VERSION_MAJ=0
EXCALIBUR_VERSION_MIN=1


# ------------------------------------------------------------------------------

class Excalibur():

    def __init__(self):
        self.args = self.argparse()
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(levelname)-8s %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S')
        logging.info(EXCALIBUR_NAME + " v" + str(EXCALIBUR_VERSION_MAJ) + "." + str(EXCALIBUR_VERSION_MIN))
        self.automata = Automata()

        

    def start(self):
        logging.info("Excalibur start")
        self.automata.start()
        logging.info("Excalibur ready to serve")

    def terminate(self):
        self.automata.terminate()
        logging.info("Excalibur terminate")

    def load(self, pathname):
        if os.path.isdir(pathname):
            self.automata.database.loadDirectory(pathname)

    def view(self):
        print(self.automata.view())
        

    def argparse(self):
        parser = argparse.ArgumentParser(
            prog = os.path.basename(__file__),
            description = 'NFC driven media center',
            epilog = 'https://github.com/lcudenne/excalibur')
        parser.add_argument("-f", "--folder", type=str, required=False,
                            help="folder prefix to recursively load the Excalibur sound database")
        parser.add_argument("-d", "--duration", type=int, default=30, required=False,
                            help="application duration before termination given in minutes")

        return parser.parse_args()


# ------------------------------------------------------------------------------

if __name__ == '__main__':
    ex = Excalibur()

    if ex.args.folder:
        ex.load(ex.args.folder)
    else:
        ex.load("/home/"+os.getlogin()+"/Public/Excalibur/")

    ex.start()

    if ex.args.duration:
        logging.info("Now running for " + str(ex.args.duration) + " minute(s)")
        time.sleep(ex.args.duration * 60)

    ex.terminate()
    exit(0)
