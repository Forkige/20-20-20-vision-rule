"""
20/20/20 Eye Rule Timer
Every 20 minutes, the screen flashes and tells you to look at something
20 feet (6 meters) away for 20 seconds. Then the timer restarts.

Run:  python eye_timer.py
Needs only Python 3 (tkinter is included with it).
"""

import tkinter as tk

WORK_SECONDS = 20 * 60   # 20 minutes of screen time
BREAK_SECONDS = 20       # 20 second eye break
FLASH_COUNT = 8          # number of flashes
FLASH_MS = 250           # speed of each flash


class EyeTimer:
    def __init__(self, root):
        self.root = root
        root.title("20-20-20")
        root.geometry("180x110")
        root.resizable(False, False)
        root.attributes("-topmost", True)

        self.remaining = WORK_SECONDS
        self.running = False
        self.job = None
        self.overlay = None

        self.label = tk.Label(root, text="20:00", font=("Arial", 22, "bold"))
        self.label.pack(pady=(10, 5))

        frame = tk.Frame(root)
        frame.pack()
        self.start_btn = tk.Button(frame, text="Start", width=7, command=self.start)
        self.start_btn.grid(row=0, column=0, padx=5)
        self.stop_btn = tk.Button(frame, text="Stop", width=7,
                                  command=self.stop, state="disabled")
        self.stop_btn.grid(row=0, column=1, padx=5)

    # ---------- main timer ----------
    def start(self):
        if self.running:
            return
        self.running = True
        self.start_btn.config(state="disabled")
        self.stop_btn.config(state="normal")
        self.tick()

    def stop(self):
        self.running = False
        if self.job:
            self.root.after_cancel(self.job)
            self.job = None
        self.close_overlay()
        self.remaining = WORK_SECONDS
        self.update_label()
        self.start_btn.config(state="normal")
        self.stop_btn.config(state="disabled")

    def tick(self):
        if not self.running:
            return
        if self.remaining <= 0:
            self.break_time()
            return
        self.update_label()
        self.remaining -= 1
        self.job = self.root.after(1000, self.tick)

    def update_label(self):
        m, s = divmod(max(self.remaining, 0), 60)
        self.label.config(text=f"{m:02d}:{s:02d}")

    # ---------- break screen ----------
    def break_time(self):
        self.label.config(text="BREAK!")
        self.overlay = tk.Toplevel(self.root)
        self.overlay.attributes("-fullscreen", True)
        self.overlay.attributes("-topmost", True)
        self.overlay.bind("<Escape>", lambda e: self.end_break())
        self.msg = tk.Label(self.overlay, text="", font=("Arial", 40, "bold"),
                            fg="white")
        self.msg.pack(expand=True)
        self.flash(0)

    def flash(self, n):
        if not self.overlay:
            return
        if n < FLASH_COUNT * 2:
            color = "white" if n % 2 == 0 else "red"
            self.overlay.config(bg=color)
            self.msg.config(bg=color, text="")
            self.job = self.root.after(FLASH_MS, self.flash, n + 1)
        else:
            self.overlay.config(bg="#102a43")
            self.msg.config(bg="#102a43")
            self.countdown(BREAK_SECONDS)

    def countdown(self, secs):
        if not self.overlay:
            return
        if secs <= 0:
            self.end_break()
            return
        self.msg.config(
            text=f"Look 20 feet (6 m) away\n\n{secs}\n\n(Esc to skip)")
        self.job = self.root.after(1000, self.countdown, secs - 1)

    def end_break(self):
        if self.job:
            self.root.after_cancel(self.job)
            self.job = None
        self.close_overlay()
        if self.running:          # restart the 20 minute cycle
            self.remaining = WORK_SECONDS
            self.tick()

    def close_overlay(self):
        if self.overlay:
            self.overlay.destroy()
            self.overlay = None


if __name__ == "__main__":
    root = tk.Tk()
    EyeTimer(root)
    root.mainloop()