from pynput import keyboard
import pyperclip
import platform
import time
import pandas as pd

# Detect OS
system = platform.system()
is_mac = system == "Darwin"  # macOS
is_windows = system == "Windows"

# Define modifier keys
if is_mac:
    MODIFIER = keyboard.Key.cmd  # Cmd key on macOS
    MODIFIER_NAME = "Cmd"
else:
    MODIFIER = keyboard.Key.ctrl_l  # Ctrl on Windows/Linux
    MODIFIER_NAME = "Ctrl"

# Track currently pressed keys
current_keys = set()

# Define combinations to detect
COPY_COMBO = {MODIFIER, keyboard.KeyCode.from_char('c')}
PRINT_COMBO = {MODIFIER, keyboard.KeyCode.from_char('p')}  # Cmd+P or Ctrl+P
file_name = "copy-data.csv"
def read_csv():
    df = pd.read_csv(file_name)
    content = df['content']
    for i in content:
        print(i)
read_csv()
def on_press(key):
    current_keys.add(key)

    # Detect Copy: Cmd+C (macOS) or Ctrl+C (Windows)
    if all(k in current_keys for k in COPY_COMBO):
        time.sleep(0.1)  # Small delay to ensure copy completes
        copied_text = pyperclip.paste()
        print(f"\n[{MODIFIER_NAME} + C] Copy detected!")
        print("Copied content:", repr(copied_text) if copied_text else "(empty or non-text)")
        df = pd.DataFrame({"content":[copied_text]})
        df.to_csv(file_name,mode="a",index=False)
        # Add your custom action here (e.g., save, process, send to API)

    # Detect Print/Command: Cmd+P (macOS) or Ctrl+P (Windows)
    elif all(k in current_keys for k in PRINT_COMBO):
        print(f"\n[{MODIFIER_NAME} + P] Custom command detected! (Cmd+P / Ctrl+P)")
        # Add your custom action here
        # Example: print("Running custom print logic...")

def on_release(key):
    if key in current_keys:
        current_keys.remove(key)

    # Stop the listener with Esc
    if key == keyboard.Key.esc:
        print("\nStopping listener...")
        return False

print(f"Listening globally on {system}...")
print(f"  - {MODIFIER_NAME} + C → Detect copy and read clipboard")
print(f"  - {MODIFIER_NAME} + P → Custom command trigger")
print("Press Esc to stop.\n")

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()