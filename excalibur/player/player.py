import logging
import vlc
import time
import queue
import threading
import os
import glob
import random


# ------------------------------------------------------------------------------

class Player():

    def __init__(self, args=None):
        self.args = args
        self.vlc_instance = vlc.Instance()
        self.vlcplayer = self.vlc_instance.media_player_new()
        self.media = None
        self.filename = None
        self.mediaqueue = queue.Queue()

        self.pid_play = None
        self.running_lock = threading.Lock()
        self.setRunning(True)
        self.pid_play = threading.Thread(target=self.run_play)
        self.pid_play.start()

    def bell(self):
        vlcplayer = self.vlc_instance.media_player_new()
        media = self.vlc_instance.media_new("excalibur/data/333695__khrinx__thin-bell-ding-2.wav")
        vlcplayer.set_media(media)
        vlcplayer.play()
        time.sleep(4)
        vlcplayer.stop()
        vlcplayer.release()


    def getRunning(self):
        self.running_lock.acquire()
        res = self.running
        self.running_lock.release()
        return res

    def setRunning(self, running):
        self.running_lock.acquire()
        self.running = running
        self.running_lock.release()


    def run_play(self):
        logging.info("Player running")
        while self.getRunning():
            if not self.vlcplayer.is_playing() and not self.mediaqueue.empty():
                self.filename = self.mediaqueue.get()
                self.media = self.vlc_instance.media_new(self.filename)
                self.vlcplayer.set_media(self.media)
                self.vlcplayer.play()
                logging.info("Player now playing " + self.filename)
            time.sleep(1)
        self.vlcplayer.stop()
        self.vlcplayer.release()
        logging.info("Player terminated")


        
    def enqueue(self, pathlist):
        vlcplayer = self.vlc_instance.media_player_new()
        media = self.vlc_instance.media_new("excalibur/data/333695__khrinx__thin-bell-ding-2.wav")
        vlcplayer.set_media(media)
        vlcplayer.play()
        
        with self.mediaqueue.mutex:
            self.mediaqueue.queue.clear()
            if self.vlcplayer.is_playing():
                self.vlcplayer.stop()
        for path in pathlist:
            if os.path.isfile(path):
                self.mediaqueue.put(path)
                logging.info("Player enqueue " + path)
            if os.path.isdir(path):
                audiotypes = ["mp3", "wav", "aif", "aiff", "ogg"]
                globfiles = []
                for audiotype in audiotypes:
                    expath = path + "/*." + audiotype
                    globfiles.extend(glob.glob(expath, recursive=True))
                if self.args.shuffle:
                    random.shuffle(globfiles)
                for gf in globfiles:
                    if os.path.isfile(gf):
                        self.mediaqueue.put(gf)
                        logging.info("Player enqueue " + gf)
        
        time.sleep(4)
        vlcplayer.stop()
        vlcplayer.release()
        
# ------------------------------------------------------------------------------

if __name__ == '__main__':
    logging.info("Copy some audio files into the /home/"+os.getlogin()+"/Music folder for testing purpose")
    player = Player()
    time.sleep(4)
    player.enqueue(["/home/"+os.getlogin()+"/Music"])
    time.sleep(6)
    player.enqueue(["/home/"+os.getlogin()+"/Music"])
    time.sleep(10)
    player.setRunning(False)
    exit(0)
    
