import time
import threading
import tkinter as tk
import pyautogui
import random

class AutoClickerApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Auto Clicker")

        self.canvas_width = 800
        self.canvas_height = 400

        self.click_interval = tk.DoubleVar(value=1.0)
        self.clicking = False
        self.stop_event = threading.Event()
        self.click_count = 0

        # Click Count Label
        self.click_count_label = tk.Label(self.root, text="Click Count: 0", font=("Helvetica", 16))
        self.click_count_label.pack(pady=10)

        # Canvas to display the balloon
        self.canvas = tk.Canvas(self.root, width=self.canvas_width, height=self.canvas_height, bg="white")
        self.canvas.pack()

        # Create the balloon object (circle and string)
        self.ballon_x = self.canvas_width // 2
        self.ballon_y = self.canvas_height // 2
        self.ballon_radius = 100
        self.ballon_color = "red"
        self.string_color = "blue"
        self.ballon = self.canvas.create_oval(self.ballon_x - self.ballon_radius,
                                              self.ballon_y - self.ballon_radius,
                                              self.ballon_x + self.ballon_radius,
                                              self.ballon_y + self.ballon_radius,
                                              fill=self.ballon_color)
        self.string = self.canvas.create_line(self.ballon_x, self.ballon_y + self.ballon_radius,
                                              self.ballon_x, self.ballon_y + 2 * self.ballon_radius,
                                              width=3, fill=self.string_color)

        # Click Interval Section
        click_interval_frame = tk.Frame(self.root)
        click_interval_frame.pack(pady=10)

        tk.Label(click_interval_frame, text="Click Interval (seconds):").grid(row=0, column=0)

        self.click_interval_entry = tk.Entry(click_interval_frame, textvariable=self.click_interval, width=10)
        self.click_interval_entry.grid(row=0, column=1)

        # Buttons Section
        buttons_frame = tk.Frame(self.root)
        buttons_frame.pack(pady=10)

        self.start_button = tk.Button(buttons_frame, text="Start", command=self.start_auto_clicking)
        self.start_button.grid(row=0, column=0)

        self.stop_button = tk.Button(buttons_frame, text="Stop", command=self.stop_auto_clicking)
        self.stop_button.grid(row=0, column=1)

        # Bind the canvas to mouse click
        self.canvas.bind("<Button-1>", self.on_canvas_click)

        # Flag to prevent click simulation while autoclicking
        self.is_autoclicking = False

    def on_canvas_click(self, event):
        x, y = event.x, event.y
        # Check if the click is inside the start button
        start_btn_x1, start_btn_y1, start_btn_x2, start_btn_y2 = self.canvas.bbox(self.start_button)
        if start_btn_x1 <= x <= start_btn_x2 and start_btn_y1 <= y <= start_btn_y2:
            if not self.clicking:
                self.start_auto_clicking()
            else:
                self.stop_auto_clicking()

    def start_auto_clicking(self):
        if not self.clicking:
            self.click_count = 0
            self.update_click_count_label()

            self.clicking = True
            self.start_button.config(text="Stop")
            self.click_interval_entry.config(state=tk.DISABLED)

            click_interval = self.click_interval.get()
            autoclick_thread = threading.Thread(target=self.clicker, args=(click_interval,))
            autoclick_thread.start()

            # Start the balloon animation
            self.animate_balloon()

    def stop_auto_clicking(self):
        if self.clicking:
            self.clicking = False
            self.stop_event.set()
            self.start_button.config(text="Start")
            self.click_interval_entry.config(state=tk.NORMAL)

    def clicker(self, click_interval):
        while self.clicking and not self.stop_event.is_set():
            pyautogui.click()
            self.click_count += 1
            self.update_click_count_label()
            time.sleep(click_interval)

        self.stop_event.clear()

    def update_click_count_label(self):
        self.click_count_label.config(text="Click Count: {}".format(self.click_count))

    def animate_balloon(self):
        if self.clicking:
            # Move the balloon randomly
            dx = random.randint(-5, 5)
            dy = random.randint(-5, 5)
            self.canvas.move(self.ballon, dx, dy)
            self.canvas.move(self.string, dx, dy)

            # Keep the balloon inside the canvas
            x1, y1, x2, y2 = self.canvas.bbox(self.ballon)
            if x1 < 0 or x2 > self.canvas_width or y1 < 0 or y2 > self.canvas_height:
                dx = -dx
                dy = -dy
                self.canvas.move(self.ballon, dx, dy)
                self.canvas.move(self.string, dx, dy)

            # Repeat the animation after a short delay
            self.root.after(50, self.animate_balloon)

if __name__ == "__main__":
    app = AutoClickerApp()
    app.root.mainloop()
