import tkinter as tk
from tkinter import ttk
import time

class CountdownTimerApp:
    def __init__(self, master, countdown_time):
        self.master = master
        self.master.title("Countdown Timer")

        self.countdown_time = countdown_time
        self.remaining_time = tk.StringVar()
        self.remaining_time.set(self.format_time(self.countdown_time))

        self.label = ttk.Label(self.master, textvariable=self.remaining_time, font=('Helvetica', 48))
        self.label.grid(row=0, column=0, padx=20, pady=20)

        self.start_button = ttk.Button(self.master, text="Start", command=self.start_timer)
        self.start_button.grid(row=1, column=0, pady=10)

    def start_timer(self):
        while self.countdown_time:
            mins, secs = divmod(self.countdown_time, 60)
            timer_format = f'{mins:02d}:{secs:02d}'
            self.remaining_time.set(timer_format)
            self.master.update()
            time.sleep(1)
            self.countdown_time -= 1

        self.remaining_time.set("Time's up!")

    @staticmethod
    def format_time(seconds):
        mins, secs = divmod(seconds, 60)
        return f'{mins:02d}:{secs:02d}'

if __name__ == "__main__":
    countdown_time = 20  # Change this to the desired countdown time

    root = tk.Tk()
    app = CountdownTimerApp(root, countdown_time)
    root.mainloop()