import logging
import json
import os
import glob

from enum import Enum

from excalibur.nfc.nfcwrapper import NFCWrapper
from excalibur.player.player import Player


# ------------------------------------------------------------------------------

class AutomataState(str, Enum):
    IDLE="IDLE"
    NOW_PLAYING="NOW_PLAYING"

class AutomataAction(str, Enum):
    PLAY="PLAY"
    PAUSE="PAUSE"
    NEXT="NEXT"


# ------------------------------------------------------------------------------

class Entry():

    def __init__(self, uid, action : AutomataAction, parameters=None):
        self.uid = uid
        self.action = action
        self.parameters = parameters


class Database():

    def __init__(self):
        self.entries = dict()

    def add(self, uid, action : AutomataAction, parameters=None):
        logging.info("Database add " + str(uid) + " " + str(parameters))
        entry = Entry(uid, action, parameters)
        self.entries[uid] = entry

    def loadJSONFiles(self, filenames):
        for filename in filenames:
            with open(filename) as fd:
                db_json = json.load(fd)
                if db_json["database"]:
                    for entry in db_json["database"]:
                        action = None
                        if entry["action"] == "PLAY":
                            action = AutomataAction.PLAY
                        if entry["action"] == "PAUSE":
                            action = AutomataAction.PAUSE
                        if action is None:
                            logging.info("JSON load unknown action")
                        self.add(entry["uid"], action, entry["parameters"])

    # Load from a directory containing subdirectories with normalized names:
    # <NFC_UID>_<directory_name>
    # Example:
    # 047ba72cd06c80_Lullaby_songs
    # Will automatically map the NFC card 047ba72cd06c80 with the content of the
    # '047ba72cd06c80_Lullaby_songs' directory
    def loadDirectory(self, dirname):
        expath = dirname + "/**/*"
        globfiles = glob.glob(expath, recursive=True)
        for gf in globfiles:
            if os.path.isdir(gf):
                gf_split = os.path.basename(gf).split('_', 1)
                if len(gf_split) > 1:
                    gf_id = gf_split[0].split('/')[-1]
                    gf_name = gf_split[1]
                    self.add(gf_id, AutomataAction.PLAY, [gf])

        
# ------------------------------------------------------------------------------

class Automata():
    
    def __init__(self, args=None):
        self.args = args
        self.state = AutomataState.IDLE
        self.database = Database()
        self.player = None
        self.nfc = None

    def start(self):
        logging.info("Automata start")
        self.player = Player(args=self.args)
        self.nfc = NFCWrapper(self.trigger)
        self.player.bell()

    def terminate(self):
        self.player.bell()
        if self.nfc:
            self.nfc.setRunning(False)
        if self.player:
            self.player.setRunning(False)
        logging.info("Automata terminate")
        
    def trigger(self, tag):
        uid = tag["nfc_uid"]
        if self.database.entries and uid in self.database.entries:
            entry = self.database.entries[uid]
            if entry.action == AutomataAction.PLAY:
                self.state = AutomataState.NOW_PLAYING
                logging.info("Automata now playing " + str(entry.parameters))
                if self.player:
                    self.player.enqueue(entry.parameters)
            if entry.action == AutomataAction.PAUSE:
                if self.state == AutomataState.NOW_PLAYING:
                    logging.info("Automata pause")

        else:
            logging.info("Automata unknown NFC UID " + str(uid))

    def view(self):
        output = str(self.database.entries)
        return output

# ------------------------------------------------------------------------------

if __name__ == '__main__':
    automata = Automata()
    exit(0)

