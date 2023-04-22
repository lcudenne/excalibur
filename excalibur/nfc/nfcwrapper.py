import logging
import pexpect
import threading
import time


# ------------------------------------------------------------------------------

class NFCWrapper():

    def __init__(self, handler=None):
        logging.info("NFCWrapper init")

        self.handler = handler
        
        nfclib = self.which("nfc-list")
        nfcbin = self.which("nfc-poll")
        if not nfclib:
            logging.warning("nfc-list not found. please install the libnfc-bin package")
        if not nfcbin:
            logging.warning("nfc-poll not found. please install the libnfc-examples package")


        self.pid_poll = None
        self.running_lock = threading.Lock()
        self.setRunning(False)
        
        if nfclib and nfcbin:
            self.setRunning(True)
            self.pid_poll = threading.Thread(target=self.run_poll)
            self.pid_poll.start()


    def getRunning(self):
        self.running_lock.acquire()
        res = self.running
        self.running_lock.release()
        return res

    def setRunning(self, running):
        self.running_lock.acquire()
        self.running = running
        self.running_lock.release()

    def which(self, binary):
        res = False
        child = pexpect.spawn("which " + binary)
        child.expect(pexpect.EOF)
        output = child.before.decode("utf-8").rstrip('\r\n')
        res = output != ""
        return res

    def nfclist(self):
        res = False
        child = pexpect.spawn("nfc-list")
        child.expect(pexpect.EOF)
        output = child.before.decode("utf-8").rstrip('\r\n')
        res = output != ""
        return res
    
    def poll(self):
        res = False
        tag = dict()
        child = pexpect.spawn("nfc-poll")
        child.expect(pexpect.EOF)
        output = child.before.decode("utf-8").rstrip('\r\n')
        if not "ERROR" in output:
            output_split = output.split('\r\n')
            for line in output_split:
                if "NFC reader:" in line:
                    tag["nfc_reader"] = line.split(': ')[1]
                if "UID" in line:
                    res = True
                    tag["nfc_uid"] = line.split(': ')[1].replace(' ', '')
        return res, tag

    def run_poll(self):
        logging.info("NFCWrapper running")
        while self.getRunning():
            res, tag = self.poll()
            if res:
                if self.handler:
                    self.handler(tag)
                else:
                    logging.info(tag)
        logging.info("NFCWrapper terminated")

# ------------------------------------------------------------------------------

if __name__ == '__main__':
    nfcwrapper = NFCWrapper()
    if nfcwrapper.getRunning():
        logging.info("NFCWrapper waiting to read NFC tags for 20 seconds")
        time.sleep(20)
        nfcwrapper.setRunning(False)
    exit(0)

