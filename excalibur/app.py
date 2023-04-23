import logging
import time
import os

from excalibur.automata.automata import Automata

# ------------------------------------------------------------------------------

EXCALIBUR_NAME="Excalibur NFC-driven media center"
EXCALIBUR_VERSION_MAJ=0
EXCALIBUR_VERSION_MIN=1


# ------------------------------------------------------------------------------

class Excalibur():

    def __init__(self):
        self.automata = Automata()
        
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(levelname)-8s %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S')
        logging.info(EXCALIBUR_NAME + " v" + str(EXCALIBUR_VERSION_MAJ) + "." + str(EXCALIBUR_VERSION_MIN))
        

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
        
            
        
# ------------------------------------------------------------------------------

if __name__ == '__main__':
    ex = Excalibur()
    ex.load("/home/"+os.getlogin()+"/Public/Excalibur/")
    ex.start()
    time.sleep(10)
    ex.terminate()
    exit(0)
