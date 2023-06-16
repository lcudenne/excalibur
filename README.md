# Excalibur
NFC driven media center

## Cold start

```bash
$ sudo apt install libnfc-bin libnfc-examples vlc libvlc-bin libvlc-dev python3-venv pulseaudio
```

On some systems you might need to reboot.

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



## Preparing the media database

The purpose of the database is to map a set of NFC identifiers (UID)
to a set of media files so that Excalibur will play these files each
time the corresponding NFC tag is detected. NFC tags do not store any
Excalibur-related information: Excalibur only relies on the ability to
detect a tag and to retrieve its UID. Therefore, any tag can be used.

There are two methods to fill in the database:


### Method A: From a given directory

This is the simpliest way to build the media database as it only uses
a regular directory in which the media files are stored. You can for
example use `$HOME/Public/Excalibur/` as a base directory
to host media files. If shared among the network, you will be able to
update the database without logging to the computer running Excalibur.

In this directory, you can create (recursively) subdirectories with
the following normalized names:

```
<NFC_UID>_<directory_name>
```

Where `<NFC_UID>` is the UID of the NFC tag (without spaces,
eg. `02391d04`) and `<directory_name>` is an arbitrary name. For
example:

```bash
$ mkdir -p $HOME/Public/Excalibur/02391d04_Lullaby_songs
```

Will automatically map the NFC tag `02391d04` with the
`$HOME/Public/Excalibur/02391d04_Lullaby_songs`, hence
playing all the included content when the tag is detected.


### Method B: From a user-defined JSON configuration file

TODO

## Running Excalibur


Quick start using method A to build the media database:

```bash
(venv) $ PYTHONPATH+=. python3 excalibur/app.py
```

Folder `$HOME/Public/Excalibur/` is automatically loaded when starting
Excalibur. To override this option and select a different directory,
you can use the `--folder` option:

```bash
$ (venv) $ PYTHONPATH+=. python3 excalibur/app.py --folder /media/$USER/usbstorage/Excalibur/
```

By default, Excalibur runs for 30 minutes then terminates. You can
modify this duration using the following parameter (in minutes):

```bash
(venv) $ PYTHONPATH+=. python3 excalibur/app.py --duration 120
```

## Automatic start at boot time

Starting Excalibur at startup can be achieved by editing the `rc.local` file:

```bash
$ sudo nano /etc/rc.local
```

Add the following lines, do not forget the `exit 0` at the end of the file:

```
pulseaudio --start
bash -c 'cd /home/path/to/excalibur/ && ./start.sh --duration 120 --folder /media/path/to/sound/library/' &

exit 0
```