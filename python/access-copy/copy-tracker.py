from pynput import keyboard
import pyperclip
import platform
import time
import pandas as pd
import os
import pyautogui

class ClipboardListener:
    def __init__(self, csv_file="copy-data.csv"):
        self.dfindex=0
        self.csv_file = csv_file
       
        # Detect OS and set modifier
        system = platform.system()
        self.is_mac = system == "Darwin"
        self.modifier_name = "Cmd" if self.is_mac else "Ctrl"
        self.modifier_key = keyboard.Key.cmd if self.is_mac else keyboard.Key.ctrl_l
        self.shift_key = keyboard.Key.shift

        # Key tracking
        self.current_keys = set()

        # Hotkey combinations
        self.copy_combo = {self.modifier_key, keyboard.KeyCode.from_char('c')}
        self.undo_paste_combo = {self.modifier_key,self.shift_key, keyboard.KeyCode.from_char('k')}
        self.print_combo = {self.modifier_key, keyboard.KeyCode.from_char('p')}

        # Listener reference (for potential future control)
        self.listener = None

        print(f"Clipboard Listener started on {system}")
        print(f"  - {self.modifier_name} + C → Save copied text to '{self.csv_file}'")
        print(f"  - {self.modifier_name} + P → Trigger custom action (print all saved)")
        print("  - Press Esc to stop\n")

        


    def _save_to_csv(self, text):
        new_data = pd.DataFrame({"content": [text]})
        new_data.to_csv(self.csv_file, mode="a", header=not os.path.exists(self.csv_file), index=False)

    def read_and_print_csv(self):
        df = pd.read_csv('copy-data.csv')
        dflength = len(df)
        index = dflength-self.dfindex 
        if index<0:
            index = 0
            self.dfindex = 0
        content = df.loc[index,'content']
        pyperclip.copy(content)  
    def on_press(self, key):
        self.current_keys.add(key)

        # Detect Copy (Cmd+C or Ctrl+C)
        if self.copy_combo.issubset(self.current_keys):
            time.sleep(0.1)  # Wait for clipboard update
            copied_text = pyperclip.paste()
            if copied_text:
                print(f"\n[{self.modifier_name} + C] Copy detected!")
                print("Copied:", repr(copied_text))
                self.dfindex = 0
                self._save_to_csv(copied_text)
            else:
                print(f"\n[{self.modifier_name} + C] Copy detected (empty or non-text)")

        # Detect Custom Command (Cmd+P or Ctrl+P)
        elif self.undo_paste_combo.issubset(self.current_keys):
            print(f"\n[{self.modifier_name} + P] Custom command triggered!")
            self.dfindex+=1
            self.read_and_print_csv()
            

    def on_release(self, key):
        time.sleep(0.1)
        if key in self.current_keys:
            self.current_keys.remove(key)

        # Stop listener on Escape
        if key == keyboard.Key.esc:
            print("\nEsc pressed. Stopping listener...")
            return False  # Stops the listener

    def start(self):
        """Start the global keyboard listener"""
        self.listener = keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release
        )
        self.listener.start()
        self.listener.join()  # Blocks until stopped

    def stop(self):
        """Stop the listener (if needed externally)"""
        if self.listener:
            self.listener.stop()


# === Usage ===
if __name__ == "__main__":
    listener = ClipboardListener(csv_file="copy-data.csv")
    try:
        listener.start()
    except KeyboardInterrupt:
        print("\nListener stopped by user.")