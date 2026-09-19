import tkinter as tk
import time
import threading
import random

# 1. 摩斯電碼字典
MORSE_CODE_DICT = {
    'A': '.-',    'B': '-...',  'C': '-.-.',  'D': '-..',   'E': '.',
    'F': '..-.',  'G': '--.',   'H': '....',  'I': '..',    'J': '.---',
    'K': '-.-',   'L': '.-..',  'M': '--',    'N': '-.',    'O': '---',
    'P': '.--.',  'Q': '--.-',  'R': '.-.',   'S': '...',   'T': '-',
    'U': '..-',   'V': '...-',  'W': '.--',   'X': '-..-',  'Y': '-.--',
    'Z': '--..',  '1': '.----', '2': '..---', '3': '...--', '4': '....-',
    '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.',
    '0': '-----'
}

class MorseLightApp:
    def __init__(self, root):
        self.root = root
        self.root.title("INTERCO 摩斯燈號訓練系統 (Visual Signal)")
        self.root.geometry("450x550")
        self.root.configure(bg="#1e1e1e")

        # 預設參數
        self.wpm = 6.0  # 考證標準速度 6 WPM
        self.is_flashing = False
        self.current_char = ""

        # UI 元件
        self.title_label = tk.Label(
            root, text="WATCH THE SIGNAL LIGHT...", 
            font=("Consolas", 14, "bold"), fg="#ffffff", bg="#1e1e1e"
        )
        self.title_label.pack(pady=15)

        # 模擬燈泡 (Canvas)
        self.canvas = tk.Canvas(root, width=200, height=200, bg="#1e1e1e", highlightthickness=0)
        self.canvas.pack(pady=10)
        # 外圈金屬框與燈心
        self.lamp_body = self.canvas.create_oval(15, 15, 185, 185, fill="#2b2b2b", outline="#555555", width=4)
        self.lamp_bulb = self.canvas.create_oval(30, 30, 170, 170, fill="#151515", outline="")

        # 速度控制區
        speed_frame = tk.Frame(root, bg="#1e1e1e")
        speed_frame.pack(pady=5)
        tk.Label(speed_frame, text="速度 (WPM):", fg="#cccccc", bg="#1e1e1e", font=("Consolas", 10)).pack(side=tk.LEFT)
        self.wpm_slider = tk.Scale(speed_frame, from_=3.0, to=12.0, resolution=0.5, orient=tk.HORIZONTAL,
                                   fg="#ffffff", bg="#1e1e1e", highlightthickness=0, command=self.update_wpm)
        self.wpm_slider.set(self.wpm)
        self.wpm_slider.pack(side=tk.LEFT, padx=10)

        # 控制按鈕
        btn_frame = tk.Frame(root, bg="#1e1e1e")
        btn_frame.pack(pady=10)
        
        self.start_btn = tk.Button(btn_frame, text="下一題 (Next)", font=("Consolas", 11, "bold"),
                                   bg="#007acc", fg="white", padx=10, command=self.next_question)
        self.start_btn.pack(side=tk.LEFT, padx=5)

        self.repeat_btn = tk.Button(btn_frame, text="重播燈號 (F1)", font=("Consolas", 11),
                                    bg="#444444", fg="white", padx=10, command=self.replay_signal)
        self.repeat_btn.pack(side=tk.LEFT, padx=5)

        # 使用者輸入與作答區
        self.prompt_label = tk.Label(root, text="你看到的字母/數字是？ (輸入後按 Enter)", 
                                     font=("Consolas", 11), fg="#aaaaaa", bg="#1e1e1e")
        self.prompt_label.pack(pady=10)

        self.entry = tk.Entry(root, font=("Consolas", 18, "bold"), width=6, justify="center")
        self.entry.pack()
        self.entry.bind("<Return>", self.check_answer)
        self.root.bind("<F1>", lambda event: self.replay_signal())

        # 結果提示
        self.result_label = tk.Label(root, text="", font=("Consolas", 13, "bold"), bg="#1e1e1e")
        self.result_label.pack(pady=15)

    def update_wpm(self, val):
        self.wpm = float(val)

    def light_on(self):
        self.canvas.itemconfig(self.lamp_bulb, fill="#ffff33")  # 亮黃色
        self.root.update_idletasks()

    def light_off(self):
        self.canvas.itemconfig(self.lamp_bulb, fill="#151515")  # 暗黑色
        self.root.update_idletasks()

    def play_morse_sequence(self, morse_pattern):
        """依標準 WPM 計算每個點劃時序並播放閃光"""
        self.is_flashing = True
        dot_duration = 1.2 / self.wpm  # PARIS 標準：1 個 dot 時間 (秒)
        dash_duration = dot_duration * 3
        symbol_pause = dot_duration

        # 閃爍前先暗 0.5 秒讓學員準備
        self.light_off()
        time.sleep(0.5)

        for symbol in morse_pattern:
            if not self.is_flashing:
                break
            if symbol == '.':
                self.light_on()
                time.sleep(dot_duration)
            elif symbol == '-':
                self.light_on()
                time.sleep(dash_duration)
            
            self.light_off()
            time.sleep(symbol_pause)

        self.is_flashing = False

    def trigger_flash_thread(self):
        morse = MORSE_CODE_DICT.get(self.current_char, "")
        if morse:
            threading.Thread(target=self.play_morse_sequence, args=(morse,), daemon=True).start()

    def next_question(self):
        if self.is_flashing:
            return
        self.current_char = random.choice(list(MORSE_CODE_DICT.keys()))
        self.result_label.config(text="")
        self.entry.delete(0, tk.END)
        self.entry.focus()
        self.trigger_flash_thread()

    def replay_signal(self):
        if self.is_flashing or not self.current_char:
            return
        self.trigger_flash_thread()

    def check_answer(self, event=None):
        if not self.current_char:
            return
        ans = self.entry.get().strip().upper()
        if ans == self.current_char:
            self.result_label.config(text=f"✔ 正確！ 答案是 【 {self.current_char} 】", fg="#00ff66")
        else:
            morse = MORSE_CODE_DICT[self.current_char]
            self.result_label.config(
                text=f"✘ 錯誤！ 答案是 【 {self.current_char} 】 (代碼: {morse})", 
                fg="#ff4444"
            )

if __name__ == "__main__":
    tk_root = tk.Tk()
    app = MorseLightApp(tk_root)
    tk_root.mainloop()