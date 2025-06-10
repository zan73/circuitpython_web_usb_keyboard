import usb_hid
from adafruit_hid.keycode import Keycode
from adafruit_hid.keyboard import Keyboard as USBKeyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS

class KeyboardSender:
    SPECIAL_KEYS = {
        "ESC":     {"order": 1, "keycode": Keycode.ESCAPE, "description": "Escape"},
        "F1":      {"order": 2, "keycode": Keycode.F1, "description": "F1"},
        "F2":      {"order": 3, "keycode": Keycode.F2, "description": "F2"},
        "F3":      {"order": 4, "keycode": Keycode.F3, "description": "F3"},
        "F4":      {"order": 5, "keycode": Keycode.F4, "description": "F4"},
        "F5":      {"order": 6, "keycode": Keycode.F5, "description": "F5"},
        "F6":      {"order": 7, "keycode": Keycode.F6, "description": "F6"},
        "F7":      {"order": 8, "keycode": Keycode.F7, "description": "F7"},
        "F8":      {"order": 9, "keycode": Keycode.F8, "description": "F8"},
        "F9":      {"order": 10, "keycode": Keycode.F9, "description": "F9"},
        "F10":     {"order": 11, "keycode": Keycode.F10, "description": "F10"},
        "F11":     {"order": 12, "keycode": Keycode.F11, "description": "F11"},
        "F12":     {"order": 13, "keycode": Keycode.F12, "description": "F12"},
        "F13":     {"order": 14, "keycode": Keycode.F13, "description": "F13"},
        "F14":     {"order": 15, "keycode": Keycode.F14, "description": "F14"},
        "F15":     {"order": 16, "keycode": Keycode.F15, "description": "F15"},
        "F16":     {"order": 17, "keycode": Keycode.F16, "description": "F16"},
        "F17":     {"order": 18, "keycode": Keycode.F17, "description": "F17"},
        "F18":     {"order": 19, "keycode": Keycode.F18, "description": "F18"},
        "F19":     {"order": 20, "keycode": Keycode.F19, "description": "F19"},
        "F20":     {"order": 21, "keycode": Keycode.F20, "description": "F20"},
        "F21":     {"order": 22, "keycode": Keycode.F21, "description": "F21"},
        "F22":     {"order": 23, "keycode": Keycode.F22, "description": "F22"},
        "F23":     {"order": 24, "keycode": Keycode.F23, "description": "F23"},
        "F24":     {"order": 25, "keycode": Keycode.F24, "description": "F24"},
        "PRTSCRN": {"order": 26, "keycode": Keycode.PRINT_SCREEN, "description": "Print Screen"},
        "SCRLLOCK":{"order": 27, "keycode": Keycode.SCROLL_LOCK, "description": "Scroll Lock"},
        "PAUSE":   {"order": 28, "keycode": Keycode.PAUSE, "description": "Pause/Break"},
        "POWER":   {"order": 29, "keycode": Keycode.POWER, "description": "Power"},
        "BKSP":    {"order": 30, "keycode": Keycode.BACKSPACE, "description": "Backspace"},
        "TAB":     {"order": 31, "keycode": Keycode.TAB, "description": "Tab"},
        "CAPS":    {"order": 32, "keycode": Keycode.CAPS_LOCK, "description": "Caps Lock"},
        "ENTER":   {"order": 33, "keycode": Keycode.ENTER, "description": "Enter"},
        "RETURN":  {"order": 34, "keycode": Keycode.ENTER, "description": "Return"},
        "SHIFT":   {"order": 35, "keycode": Keycode.SHIFT, "description": "Shift"},
        "LSHIFT":  {"order": 36, "keycode": Keycode.LEFT_SHIFT, "description": "Left Shift"},
        "RSHIFT":  {"order": 37, "keycode": Keycode.RIGHT_SHIFT, "description": "Right Shift"},
        "CTRL":    {"order": 38, "keycode": Keycode.CONTROL, "description": "Left Control"},
        "LCTRL":   {"order": 39, "keycode": Keycode.LEFT_CONTROL, "description": "Left Control"},
        "RCTRL":   {"order": 40, "keycode": Keycode.RIGHT_CONTROL, "description": "Right Control"},
        "WIN":     {"order": 41, "keycode": Keycode.GUI, "description": "Windows"},
        "OPTION":  {"order": 42, "keycode": Keycode.LEFT_ALT, "description": "Option"},
        "CMD":     {"order": 43, "keycode": Keycode.GUI, "description": "Command"},
        "ALT":     {"order": 44, "keycode": Keycode.ALT, "description": "Alt"},
        "LALT":    {"order": 45, "keycode": Keycode.LEFT_ALT, "description": "Left Alt"},
        "SPACE":   {"order": 46, "keycode": Keycode.SPACEBAR, "description": "Spacebar"},
        "RALT":    {"order": 47, "keycode": Keycode.RIGHT_ALT, "description": "Right Alt"},
        "MENU":    {"order": 48, "keycode": Keycode.APPLICATION, "description": "Menu"},
        
        "INS":     {"order": 49, "keycode": Keycode.INSERT, "description": "Insert"},
        "HOME":    {"order": 50, "keycode": Keycode.HOME, "description": "Home"},
        "PGUP":    {"order": 51, "keycode": Keycode.PAGE_UP, "description": "Page Up"},
        "DEL":     {"order": 52, "keycode": Keycode.DELETE, "description": "Delete"},
        "END":     {"order": 53, "keycode": Keycode.END, "description": "End"},
        "PGDN":    {"order": 54, "keycode": Keycode.PAGE_DOWN, "description": "Page Down"},
        
        "UP":      {"order": 55, "keycode": Keycode.UP_ARROW, "description": "Up"},
        "DOWN":    {"order": 56, "keycode": Keycode.DOWN_ARROW, "description": "Down"},
        "LEFT":    {"order": 57, "keycode": Keycode.LEFT_ARROW, "description": "Left"},
        "RIGHT":   {"order": 58, "keycode": Keycode.RIGHT_ARROW, "description": "Right"},
        
        "KEYPAD_NUMLOCK":       {"order": 59, "keycode": Keycode.KEYPAD_NUMLOCK, "description": "Num Lock"},
        "KEYPAD_ASTERISK":      {"order": 60, "keycode": Keycode.KEYPAD_ASTERISK, "description": "Keypad *"},
        "KEYPAD_BACKSLASH":     {"order": 61, "keycode": Keycode.KEYPAD_BACKSLASH, "description": "Keypad \\"},
        "KEYPAD_ENTER":         {"order": 62, "keycode": Keycode.KEYPAD_ENTER, "description": "Keypad Enter"},
        "KEYPAD_MINUS":         {"order": 63, "keycode": Keycode.KEYPAD_MINUS, "description": "Keypad -"},
        "KEYPAD_EQUALS":        {"order": 64, "keycode": Keycode.KEYPAD_EQUALS, "description": "Keypad ="},
        "KEYPAD_FORWARD_SLASH": {"order": 65, "keycode": Keycode.KEYPAD_FORWARD_SLASH, "description": "Keypad /"},
        "KEYPAD_PERIOD":        {"order": 66, "keycode": Keycode.KEYPAD_PERIOD, "description": "Keypad ."},
        "KEYPAD_PLUS":          {"order": 67, "keycode": Keycode.KEYPAD_PLUS, "description": "Keypad +"},
        "KEYPAD_ZERO":          {"order": 68, "keycode": Keycode.KEYPAD_ZERO, "description": "Keypad 0"},
        "KEYPAD_ONE":           {"order": 69, "keycode": Keycode.KEYPAD_ONE, "description": "Keypad 1"},
        "KEYPAD_TWO":           {"order": 70, "keycode": Keycode.KEYPAD_TWO, "description": "Keypad 2"},
        "KEYPAD_THREE":         {"order": 71, "keycode": Keycode.KEYPAD_THREE, "description": "Keypad 3"},
        "KEYPAD_FOUR":          {"order": 72, "keycode": Keycode.KEYPAD_FOUR, "description": "Keypad 4"},
        "KEYPAD_FIVE":          {"order": 73, "keycode": Keycode.KEYPAD_FIVE, "description": "Keypad 5"},
        "KEYPAD_SIX":           {"order": 74, "keycode": Keycode.KEYPAD_SIX, "description": "Keypad 6"},
        "KEYPAD_SEVEN":         {"order": 75, "keycode": Keycode.KEYPAD_SEVEN, "description": "Keypad 7"},
        "KEYPAD_EIGHT":         {"order": 76, "keycode": Keycode.KEYPAD_EIGHT, "description": "Keypad 8"},
        "KEYPAD_NINE":          {"order": 77, "keycode": Keycode.KEYPAD_NINE, "description": "Keypad 9"},

        "PLUS":    {"order": 78, "keycode": (Keycode.LEFT_SHIFT, Keycode.EQUALS), "description": "Plus"}
}

    def __init__(self):
        self.keyboard = None
        self.layout = None

        self.keyboard = USBKeyboard(usb_hid.devices)
        self.layout = KeyboardLayoutUS(self.keyboard)

    def send(self, input_str: str):
        try:
            segments = input_str.strip().split(" ")
            for segment in segments:
                if "+" in segment:
                    keycodes = []
                    for key in segment.split("+"):
                        key_upper = key.upper()
                        value = self.SPECIAL_KEYS.get(key_upper)["keycode"]
                        if value:
                            keycodes.append(value)
                        else:
                            for char in key:
                                code = getattr(Keycode, char.upper(), None)
                                if code:
                                    keycodes.append(code)
                    self.keyboard.press(*keycodes)
                    self.keyboard.release_all()
                else:
                    key_upper = segment.upper()
                    if key_upper in self.SPECIAL_KEYS:
                        keys = self.SPECIAL_KEYS[key_upper]["keycode"]
                        if isinstance(keys, tuple):
                            self.keyboard.press(*keys)
                        else:
                            self.keyboard.press(keys)
                        self.keyboard.release_all()
                    else:
                        self.layout.write(segment)
        except Exception as e:
            print(f"Keystroke send error: {e}")
