# Pico 2W CircuitPython Web-accessible Keystroke Sender

A simple CircuitPython project to send keystrokes to a USB-connected device via the web. Should work with most devices however will not send keystrokes to a Mac at FileVault login (cold boot). For MacOS FileVault login, see my Arduino-based project [https://github.com/zan73/web_usb_keyboard].

Follow these steps to set up your Raspberry Pi Pico 2W with CircuitPython and the required libraries:

## 1. Download and Flash CircuitPython

- Download the latest CircuitPython `.uf2` firmware for the Raspberry Pi Pico W from [circuitpython.org](https://circuitpython.org/board/raspberry_pi_pico_w/).
- Boot your Pico 2W into BOOTSEL mode by holding down the BOOTSEL button while plugging it into your computer via USB.
- Drag and drop the downloaded `.uf2` file onto the RPI-RP2 drive that appears. The board will reboot as a CIRCUITPY drive.

## 2. Install CircuitPython Libraries

- Download the [CircuitPython Libraries Bundle](https://circuitpython.org/libraries) that matches your CircuitPython version.
- Unzip the bundle on your computer.

## 3. Copy Required Libraries

- From the unzipped `lib` folder, copy these libraries to the `/lib` directory on your Pico 2W CIRCUITPY drive:
  - `adafruit_ble`
  - `adafruit_hid`
  - `adafruit_requests`

## 4. Upload Project Files

- Copy all project `.py` files and your customized `settings.toml` file to the root directory (`/`) of your CIRCUITPY drive.

---

Your Pico 2W is now set up to run the project.