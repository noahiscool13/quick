from pynput import keyboard
import shell

# The key combination to check
COMBINATION = {keyboard.Key.ctrl_l,keyboard.Key.shift_l,keyboard.KeyCode.from_char('q')}

# The currently active modifiers
current = set()


def on_press(key):
    global current

    if key in COMBINATION:
        current.add(key)
        if all(k in current for k in COMBINATION):
            current = set()
            shell.run()
    # if key == keyboard.Key.esc:
    #     print("close")
    #     # shell.close()



def on_release(key):
    try:
        current.remove(key)
    except KeyError:
        pass


with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()