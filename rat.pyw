import ctypes
import sys
import tkinter as tk
from tkinter import messagebox
import os
import cv2
import numpy as np
import mss
import threading
import time
import keyboard 
from datetime import datetime

# --- CONSOLE STEALTH FUNCTIONS ---
kernel32 = ctypes.WinDLL('kernel32')
user32 = ctypes.WinDLL('user32')

def hide_console():
    hWnd = kernel32.GetConsoleWindow()
    if hWnd != 0:
        user32.ShowWindow(hWnd, 0) # 0 = SW_HIDE

def show_console():
    hWnd = kernel32.GetConsoleWindow()
    if hWnd != 0:
        user32.ShowWindow(hWnd, 5) # 5 = SW_SHOW

def is_admin():
    try: return ctypes.windll.shell32.IsUserAnAdmin()
    except: return False

def run_as_admin():
    if not is_admin():
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 0)
        return False
    return True

class RaceRatRocket:
    def __init__(self, root):
        self.root = root
        self.root.title("Race Rat Rocket - PE v8.9")
        self.root.geometry("980x620")
        self.root.configure(bg="#0f0f0f")
        
        # --- FIXED ICON LOGIC (MUST BE INSIDE __INIT__) ---
        if os.path.exists("icon.ico"):
            try:
                self.root.iconbitmap("icon.ico")
            except:
                pass # Prevents crash if icon is invalid
        
        self.is_recording = False
        self.viewlog_path = None
        self.save_count = 0
        self.fps = 15.0 
        self.trigger_save = False 
        
        self.status_var = tk.StringVar(value="System: Standby")
        self.folder_status = tk.StringVar(value="Folder: Not Checked")
        self.timer_var = tk.StringVar(value="Trigger: Waiting for Alt+Tab")
        self.current_file_var = tk.StringVar(value="Target: None")
        self.notif_var = tk.StringVar(value="0")
        
        self.setup_ui()
        self.setup_shortcuts()

    def setup_ui(self):
        header = tk.Frame(self.root, bg="#1a1a1a", height=80)
        header.pack(fill="x", side="top")
        tk.Label(header, text="RACE RAT ROCKET v8.9", font=("Impact", 32), bg="#1a1a1a", fg="#00ffcc").pack(pady=10)

        console_frame = tk.Frame(self.root, bg="#0f0f0f", padx=50, pady=20)
        console_frame.pack(fill="both", expand=True)

        scan_frame = tk.LabelFrame(console_frame, text=" Security Verification ", fg="#ffcc00", bg="#0f0f0f", font=("Arial", 10, "bold"), padx=20, pady=15)
        scan_frame.pack(fill="x", pady=5)
        tk.Label(scan_frame, textvariable=self.folder_status, font=("Consolas", 11), bg="#0f0f0f", fg="white").pack(side="left")
        tk.Button(scan_frame, text="ALLOW & SCAN", command=self.handle_initialization, bg="#333", fg="#00ffcc", font=("Arial", 10, "bold"), relief="flat", padx=20).pack(side="right")

        stats_frame = tk.Frame(console_frame, bg="#0f0f0f")
        stats_frame.pack(fill="x", pady=20)
        
        t_box = tk.Frame(stats_frame, bg="#1a1a1a", highlightthickness=1, highlightbackground="#333")
        t_box.pack(side="left", fill="both", expand=True, padx=(0, 10))
        tk.Label(t_box, textvariable=self.timer_var, font=("Consolas", 14, "bold"), bg="#1a1a1a", fg="#ffcc00").pack(pady=15)
        tk.Label(t_box, text="SAVE TRIGGER: [ALT+TAB]", font=("Arial", 8), bg="#1a1a1a", fg="#666").pack()

        f_box = tk.Frame(stats_frame, bg="#1a1a1a", highlightthickness=1, highlightbackground="#333")
        f_box.pack(side="right", fill="both", expand=True)
        tk.Label(f_box, textvariable=self.current_file_var, font=("Consolas", 10), bg="#1a1a1a", fg="#00ffcc").pack(pady=15)
        tk.Label(f_box, text="ACTIVE BUFFER", font=("Arial", 8), bg="#1a1a1a", fg="#666").pack()

        self.start_btn = tk.Button(console_frame, text="START RECORDING", command=self.toggle_recording, font=("Arial", 16, "bold"), bg="#222", fg="#444", state="disabled", relief="flat", height=2)
        self.start_btn.pack(fill="x", pady=20)

        footer = tk.Frame(self.root, bg="#00ffcc")
        footer.pack(side="bottom", fill="x")
        tk.Label(footer, textvariable=self.status_var, bg="#00ffcc", fg="#000", font=("Arial", 10, "bold")).pack(side="left", padx=10)
        notif_f = tk.Frame(footer, bg="#ff3333", width=30, height=30)
        notif_f.pack(side="right", padx=10, pady=2)
        notif_f.pack_propagate(False)
        tk.Label(notif_f, textvariable=self.notif_var, bg="#ff3333", fg="white", font=("Arial", 12, "bold")).pack()

    def setup_shortcuts(self):
        keyboard.add_hotkey('ctrl+tab', self.hide_all)
        keyboard.add_hotkey('ctrl+tab+e', self.show_all)
        keyboard.add_hotkey('alt+tab', self.trigger_manual_save)

    def hide_all(self):
        self.root.withdraw() 
        hide_console() 

    def show_all(self):
        self.root.deiconify()
        show_console()
        self.root.lift()

    def handle_initialization(self):
        if not is_admin():
            if messagebox.askyesno("Admin", "Elevate to Admin?"):
                run_as_admin()
                self.root.destroy()
        else:
            self.scan_folders()

    def scan_folders(self):
        path = "C:\\Program Files\\viewlog"
        if not os.path.exists(path): os.makedirs(path, exist_ok=True)
        self.viewlog_path = path
        self.folder_status.set(f"ADMIN ACTIVE: {path}")
        self.start_btn.config(state="normal", bg="#2ecc71", fg="white")

    def toggle_recording(self):
        if not self.is_recording:
            self.is_recording = True
            self.start_btn.config(text="STOP RECORDING", bg="#e74c3c")
            threading.Thread(target=self.record_loop, daemon=True).start()
        else:
            self.is_recording = False
            self.start_btn.config(text="START RECORDING", bg="#2ecc71")

    def trigger_manual_save(self):
        if self.is_recording:
            self.trigger_save = True

    def record_loop(self):
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        with mss.mss() as sct:
            monitor = sct.monitors[1]
            width, height = int(monitor["width"]), int(monitor["height"])
            
            while self.is_recording:
                ts = datetime.now().strftime("%H%M%S")
                filename = os.path.join(self.viewlog_path, f"RAT_{ts}.avi")
                self.current_file_var.set(os.path.basename(filename))
                
                out = cv2.VideoWriter(filename, fourcc, self.fps, (width, height))
                self.trigger_save = False 
                
                while self.is_recording and not self.trigger_save:
                    loop_start = time.time()
                    img = sct.grab(monitor)
                    frame = cv2.cvtColor(np.array(img), cv2.COLOR_BGRA2BGR)
                    out.write(frame)

                    time_diff = time.time() - loop_start
                    if time_diff < (1.0 / self.fps):
                        time.sleep((1.0 / self.fps) - time_diff)
                
                out.release()
                if self.is_recording or self.trigger_save:
                    self.save_count += 1
                    self.notif_var.set(str(self.save_count))
                    self.status_var.set(f"Saved: RAT_{ts}.avi")

if __name__ == "__main__":
    root = tk.Tk()
    app = RaceRatRocket(root)
    root.mainloop()
    