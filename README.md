# Excalibur
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



## Preparing the media database

The purpose of the database is to map a set of NFC identifiers (UID)
to a set of media files so that Excalibur will play these files each
time the corresponding NFC tag is detected. NFC tags do not store any
Excalibur-related information: Excalibur only relies on the ability to
detect a tag and to retrieve its UID. Therefore, any tag can be used.

There are two methods to fill in the database:


### Method A: From a given directory

This is the simpliest way to build the media database as it only use a
regular directory in which the media files are stored. You can for
example use `/home/<your_login>/Public/Excalibur/` as a base directory
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

```
$ mkdir -p /home/<your_login>/Public/Excalibur/02391d04_Lullaby_songs
```

Will automatically map the NFC tag `02391d04` with the
`/home/<your_login>/Public/Excalibur/02391d04_Lullaby_songs`, hence
playing all the included content when the tag is detected.


### Method B: From a user-defined JSON configuration file

TODO

## Running Excalibur


Quick start using method A to build the media database:

```bash
(venv) $ PYTHONPATH+=. python3 excalibur/app.py
```
