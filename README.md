# excalibur
NFC driven media center

## Cold start

```bash
$ sudo apt install libnfc-bin libnfc-examples
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

