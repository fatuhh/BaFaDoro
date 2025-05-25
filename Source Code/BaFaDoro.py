
import tkinter as tk
from tkinter import ttk, messagebox
import random
from pygame import mixer

class EnhancedPomodoroTimer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("BaFadoro!")
        self.root.geometry("500x750")
        self.root.resizable(False, False)

        # Modern renk paleti
        self.BG_COLOR = "#232946"
        self.ACCENT_COLOR = "#eebbc3"
        self.SECONDARY_COLOR = "#b8c1ec"
        self.WHITE = "#fffffe"
        self.GOLD = "#ffd803"
        self.BOX_COLOR = "#393e60"
        self.BUTTON_HOVER = "#f6c6ea"

        self.root.configure(bg=self.BG_COLOR)

        mixer.init()

        self.sound_paths = {
            'alarm': 'users/emirbulut/Dowloads/allert.mp3',
            'relax': 'sounds/relax.mp3',
            'complete': 'sounds/complete.mp3'
        }

        self.motivational_quotes = [
            "Her pomodoro, hedeflerine giden yolda bir adım! ",
            "Küçük adımlar, büyük başarılar getirir! 💪",
            "Odaklan ve başar! ✨",
            "Mola da başarının bir parçasıdır! 🎯",
            "Her gün biraz daha ileriye! 🚀",
            "Kendine yatırım yapıyorsun! 💎",
            "Disiplin, özgürlüğün köprüsüdür! 🌈",
            "Şimdi odaklanma zamanı! 🎯",
            "Başarı, küçük çabaların toplamıdır! ⭐",
            "Kendine inan, yapabilirsin! 🌟"
        ]

        # Varsayılan zamanlayıcı değişkenleri
        self.WORK_TIME = 25 * 60
        self.SHORT_BREAK = 5 * 60
        self.LONG_BREAK = 15 * 60

        self.current_time = self.WORK_TIME
        self.timer_running = False
        self.pomodoro_count = 0

        self.setup_gui()
        self.update_quote()

    def setup_gui(self):
        # Başlık ve Ayarlar butonu
        title_frame = tk.Frame(self.root, bg=self.BG_COLOR)
        title_frame.place(relx=0.5, rely=0.05, anchor="center")

        title_label = tk.Label(
            title_frame,
            text="BaFadoro!",
            font=("Montserrat", 32, "bold"),
            fg=self.GOLD,
            bg=self.BG_COLOR
        )
        title_label.pack(side=tk.LEFT, padx=(0, 10))

        settings_icon = tk.Label(
            title_frame,
            text="⚙️",
            font=("Arial", 20),
            bg=self.BG_COLOR,
            cursor="hand2"
        )
        settings_icon.pack(side=tk.LEFT)
        settings_icon.bind("<Button-1>", lambda e: self.open_settings())

        # Ana zamanlayıcı çemberi
        self.timer_canvas = tk.Canvas(
            self.root,
            width=300,
            height=300,
            bg=self.BG_COLOR,
            highlightthickness=0
        )
        self.timer_canvas.place(relx=0.5, rely=0.33, anchor="center")

        # Dış çember
        self.outer_circle = self.timer_canvas.create_oval(
            10, 10, 290, 290,
            outline=self.SECONDARY_COLOR,
            width=18
        )

        # İlerleme çemberi
        self.progress_circle = self.timer_canvas.create_arc(
            10, 10, 290, 290,
            start=90,
            extent=0,
            outline=self.ACCENT_COLOR,
            width=18,
            style="arc"
        )

        # Zaman etiketi
        self.time_label = tk.Label(
            self.timer_canvas,
            text="25:00",
            font=("Montserrat", 52, "bold"),
            fg=self.WHITE,
            bg=self.BG_COLOR
        )
        self.time_label.place(relx=0.5, rely=0.5, anchor="center")

        # Durum etiketi
        self.status_label = tk.Label(
            self.root,
            text="Çalışma Zamanı",
            font=("Montserrat", 18, "bold"),
            fg=self.GOLD,
            bg=self.BG_COLOR
        )
        self.status_label.place(relx=0.5, rely=0.58, anchor="center")

        # Motive edici söz kutusu
        self.quote_frame = tk.Frame(self.root, bg=self.BOX_COLOR, bd=0, highlightthickness=0)
        self.quote_frame.place(relx=0.5, rely=0.7, anchor="center", width=420, height=70)
        self.quote_label = tk.Label(
            self.quote_frame,
            text="",
            font=("Montserrat", 13, "italic"),
            fg=self.GOLD,
            bg=self.BOX_COLOR,
            wraplength=400,
            justify="center"
        )
        self.quote_label.pack(expand=True, fill="both", padx=10, pady=10)

        # Butonlar
        button_frame = tk.Frame(self.root, bg=self.BG_COLOR)
        button_frame.place(relx=0.5, rely=0.82, anchor="center")

        style = ttk.Style()
        style.theme_use('clam')
        style.configure(
            "Custom.TButton",
            padding=12,
            font=("Montserrat", 13, "bold"),
            background=self.ACCENT_COLOR,
            foreground=self.BG_COLOR,
            borderwidth=0,
            focusthickness=3,
            focuscolor=self.GOLD
        )
        style.map("Custom.TButton",
                  background=[('active', self.BUTTON_HOVER)])

        self.start_button = ttk.Button(
            button_frame,
            text="Başlat",
            style="Custom.TButton",
            command=self.toggle_timer
        )
        self.start_button.pack(side=tk.LEFT, padx=12)

        self.reset_button = ttk.Button(
            button_frame,
            text="Sıfırla",
            style="Custom.TButton",
            command=self.reset_timer
        )
        self.reset_button.pack(side=tk.LEFT, padx=12)

        # Pomodoro sayacı
        self.counter_label = tk.Label(
            self.root,
            text="Tamamlanan Pomodoro: 0",
            font=("Montserrat", 13, "bold"),
            fg=self.WHITE,
            bg=self.BG_COLOR
        )
        self.counter_label.place(relx=0.5, rely=0.93, anchor="center")

    def open_settings(self):
        settings_win = tk.Toplevel(self.root)
        settings_win.title("Ayarlar")
        settings_win.geometry("340x260")
        settings_win.configure(bg=self.BOX_COLOR)
        settings_win.resizable(False, False)
        settings_win.grab_set()

        label_style = {"font": ("Montserrat", 12), "bg": self.BOX_COLOR, "fg": self.WHITE}
        entry_style = {"font": ("Montserrat", 12), "width": 5, "justify": "center"}

        tk.Label(settings_win, text="Çalışma Süresi (dk)", **label_style).place(x=30, y=30)
        work_var = tk.IntVar(value=self.WORK_TIME // 60)
        work_entry = tk.Entry(settings_win, textvariable=work_var, **entry_style)
        work_entry.place(x=220, y=30)

        tk.Label(settings_win, text="Kısa Mola (dk)", **label_style).place(x=30, y=80)
        short_var = tk.IntVar(value=self.SHORT_BREAK // 60)
        short_entry = tk.Entry(settings_win, textvariable=short_var, **entry_style)
        short_entry.place(x=220, y=80)

        tk.Label(settings_win, text="Uzun Mola (dk)", **label_style).place(x=30, y=130)
        long_var = tk.IntVar(value=self.LONG_BREAK // 60)
        long_entry = tk.Entry(settings_win, textvariable=long_var, **entry_style)
        long_entry.place(x=220, y=130)

        def save_settings():
            try:
                w = int(work_var.get())
                s = int(short_var.get())
                l = int(long_var.get())
                assert w > 0 and s > 0 and l > 0
                self.WORK_TIME = w * 60
                self.SHORT_BREAK = s * 60
                self.LONG_BREAK = l * 60
                self.reset_timer()
                settings_win.destroy()
            except:
                messagebox.showerror("Hata", "Lütfen geçerli ve pozitif değerler girin.")

        save_btn = tk.Button(settings_win, text="Kaydet", font=("Montserrat", 12, "bold"),
                             bg=self.ACCENT_COLOR, fg=self.BG_COLOR, activebackground=self.BUTTON_HOVER,
                             relief="flat", command=save_settings)
        save_btn.place(relx=0.5, rely=0.8, anchor="center", width=120, height=38)

    def update_quote(self):
        quote = random.choice(self.motivational_quotes)
        self.quote_label.configure(text=quote)
        self.root.after(20000, self.update_quote)

    def play_sound(self, sound_type):
        try:
            mixer.music.load(self.sound_paths[sound_type])
            mixer.music.play()
        except:
            print(f"Ses dosyası yüklenemedi: {sound_type}")

    def toggle_timer(self):
        if self.timer_running:
            self.timer_running = False
            self.start_button.configure(text="Devam Et")
            if mixer.music.get_busy():
                mixer.music.stop()
        else:
            self.timer_running = True
            self.start_button.configure(text="Duraklat")
            self.update_timer()
            if "Mola" in self.status_label.cget("text"):
                self.play_sound('relax')

    def update_timer(self):
        if self.timer_running and self.current_time > 0:
            minutes = self.current_time // 60
            seconds = self.current_time % 60
            self.time_label.configure(text=f"{minutes:02d}:{seconds:02d}")
            if self.current_time == self.WORK_TIME:
                progress = 0
            else:
                if self.status_label.cget("text") == "Çalışma Zamanı":
                    progress = (1 - self.current_time / self.WORK_TIME) * 360
                elif self.status_label.cget("text") == "Kısa Mola":
                    progress = (1 - self.current_time / self.SHORT_BREAK) * 360
                else:
                    progress = (1 - self.current_time / self.LONG_BREAK) * 360
            self.timer_canvas.itemconfig(
                self.progress_circle,
                extent=progress
            )
            self.current_time -= 1
            self.root.after(1000, self.update_timer)
        elif self.timer_running and self.current_time <= 0:
            self.timer_complete()

    def timer_complete(self):
        if self.status_label.cget("text") == "Çalışma Zamanı":
            self.play_sound('complete')
            self.pomodoro_count += 1
            self.counter_label.configure(text=f"Tamamlanan Pomodoro: {self.pomodoro_count}")
            if self.pomodoro_count % 4 == 0:
                messagebox.showinfo("Tebrikler! 🎉", "Harika iş çıkardın!\nUzun mola zamanı!")
                self.current_time = self.LONG_BREAK
                self.status_label.configure(text="Uzun Mola")
            else:
                messagebox.showinfo("Tebrikler! ⭐", "Bir pomodoro daha tamamlandı!\nKısa mola zamanı!")
                self.current_time = self.SHORT_BREAK
                self.status_label.configure(text="Kısa Mola")
        else:
            self.play_sound('alarm')
            messagebox.showinfo("Mola bitti! 🎯", "Şimdi odaklanma zamanı!")
            self.current_time = self.WORK_TIME
            self.status_label.configure(text="Çalışma Zamanı")
        self.timer_running = False
        self.start_button.configure(text="Başlat")
        self.update_display()

    def reset_timer(self):
        self.timer_running = False
        self.current_time = self.WORK_TIME
        self.start_button.configure(text="Başlat")
        self.status_label.configure(text="Çalışma Zamanı")
        if mixer.music.get_busy():
            mixer.music.stop()
        self.update_display()
        self.timer_canvas.itemconfig(
            self.progress_circle,
            extent=0
        )

    def update_display(self):
        minutes = self.current_time // 60
        seconds = self.current_time % 60
        self.time_label.configure(text=f"{minutes:02d}:{seconds:02d}")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = EnhancedPomodoroTimer()
    app.run()
