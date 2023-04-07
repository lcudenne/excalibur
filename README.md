# excalibur
NFC driven media center

## Cold start

```bash
$ sudo apt install libnfc-bin libnfc-examples vlc libvlc-bin libvlc-dev
```

Connect the NFC device. The following command should be able to open the interface:

```bash
$ nfc-list
```

Create the Python virtualenv:

```bash
$ python3 -m venv venv
$ source venv/bin/activate
(venv) $ pip install -r excalibur/requirements.txt
```

Check that the Python NFC wrapper can detect the NFC device and read different tags:

```bash
(venv) $ python3 excalibur/nfc/nfcwrapper.py
```

Check that the Python bindings for VLC can play media files (copy some audio files into your `$HOME/Music` folder):

```bash
(venv) $ python3 excalibur/player/player.py
```
