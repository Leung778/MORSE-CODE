import tkinter as tk
from tkinter import ttk
import time
import threading
import random

# 摩斯電碼字典
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

class MorseProApp:
    def __init__(self, root):
        self.root = root
        self.root.title("INTERCO 摩斯燈號進階訓練系統")
        self.root.geometry("600x650")
        self.root.configure(bg="#1e1e1e")

        # 核心變數
        self.wpm = tk.DoubleVar(value=6.0)
        self.mode = tk.StringVar(value="single") # single 或 block
        self.group_count = tk.IntVar(value=3)    # 產生多少組
        self.char_per_group = tk.IntVar(value=5) # 每組多少字
        
        self.current_text = ""
        self.is_flashing = False
        self.cancel_flag = False

        self.setup_ui()

    def setup_ui(self):
        # 標題
        tk.Label(self.root, text="MORSE CODE FLASHING LIGHT", 
                 font=("Consolas", 16, "bold"), fg="#ffffff", bg="#1e1e1e").pack(pady=10)

        # 模擬燈泡 (Canvas)
        self.canvas = tk.Canvas(self.root, width=150, height=150, bg="#1e1e1e", highlightthickness=0)
        self.canvas.pack()
        self.lamp_body = self.canvas.create_oval(10, 10, 140, 140, fill="#2b2b2b", outline="#555555", width=4)
        self.lamp_bulb = self.canvas.create_oval(25, 25, 125, 125, fill="#151515", outline="")

        # 設定面板
        settings_frame = tk.LabelFrame(self.root, text=" 測驗設定 ", bg="#1e1e1e", fg="#00ff66", font=("微軟正黑體", 10))
        settings_frame.pack(pady=10, fill="x", padx=20)

        # -- 模式選擇
        mode_frame = tk.Frame(settings_frame, bg="#1e1e1e")
        mode_frame.pack(pady=5, anchor="w", padx=10)
        tk.Radiobutton(mode_frame, text="單字元訓練", variable=self.mode, value="single", 
                       bg="#1e1e1e", fg="#ffffff", selectcolor="#444444").pack(side=tk.LEFT)
        tk.Radiobutton(mode_frame, text="段落組合訓練", variable=self.mode, value="block", 
                       bg="#1e1e1e", fg="#ffffff", selectcolor="#444444").pack(side=tk.LEFT, padx=10)

        # -- 段落參數設定
        param_frame = tk.Frame(settings_frame, bg="#1e1e1e")
        param_frame.pack(pady=5, anchor="w", padx=10)
        tk.Label(param_frame, text="產生", bg="#1e1e1e", fg="#cccccc").pack(side=tk.LEFT)
        tk.Entry(param_frame, textvariable=self.group_count, width=3, justify="center").pack(side=tk.LEFT, padx=5)
        tk.Label(param_frame, text="組，每組", bg="#1e1e1e", fg="#cccccc").pack(side=tk.LEFT)
        tk.Entry(param_frame, textvariable=self.char_per_group, width=3, justify="center").pack(side=tk.LEFT, padx=5)
        tk.Label(param_frame, text="個字元 (段落模式適用)", bg="#1e1e1e", fg="#cccccc").pack(side=tk.LEFT)

        # -- 速度設定
        speed_frame = tk.Frame(settings_frame, bg="#1e1e1e")
        speed_frame.pack(pady=5, anchor="w", padx=10)
        tk.Label(speed_frame, text="發報速度 (WPM):", bg="#1e1e1e", fg="#cccccc").pack(side=tk.LEFT)
        tk.Scale(speed_frame, variable=self.wpm, from_=3.0, to=15.0, resolution=0.5, 
                 orient=tk.HORIZONTAL, bg="#1e1e1e", fg="#ffffff", highlightthickness=0, length=200).pack(side=tk.LEFT, padx=10)

        # 控制按鈕
        btn_frame = tk.Frame(self.root, bg="#1e1e1e")
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="發送新題目 (Next)", font=("微軟正黑體", 11, "bold"), bg="#007acc", fg="white", 
                  width=15, command=self.next_question).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="重播 (Replay)", font=("微軟正黑體", 11), bg="#444444", fg="white", 
                  width=12, command=self.replay_signal).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="強制停止 (Stop)", font=("微軟正黑體", 11), bg="#cc0000", fg="white", 
                  width=12, command=self.stop_flashing).pack(side=tk.LEFT, padx=5)

        # 作答區
        tk.Label(self.root, text="請輸入你辨識出的內容 (按 Enter 提交核對)：", bg="#1e1e1e", fg="#aaaaaa").pack(pady=5)
        self.entry = tk.Entry(self.root, font=("Consolas", 14), width=40, justify="center")
        self.entry.pack(ipady=5)
        self.entry.bind("<Return>", self.check_answer)

        # 結果提示
        self.result_label = tk.Label(self.root, text="", font=("Consolas", 12, "bold"), bg="#1e1e1e", wraplength=550)
        self.result_label.pack(pady=15)

    def light_on(self):
        self.canvas.itemconfig(self.lamp_bulb, fill="#ffff33")
        self.root.update_idletasks()

    def light_off(self):
        self.canvas.itemconfig(self.lamp_bulb, fill="#151515")
        self.root.update_idletasks()

    def generate_text(self):
        chars = list(MORSE_CODE_DICT.keys())
        if self.mode.get() == "single":
            return random.choice(chars)
        else:
            groups = []
            for _ in range(self.group_count.get()):
                group = "".join(random.choices(chars, k=self.char_per_group.get()))
                groups.append(group)
            return " ".join(groups)

    def play_morse_sequence(self, text):
        self.is_flashing = True
        self.cancel_flag = False
        
        # PARIS 標準時序計算
        dot = 1.2 / self.wpm.get()
        dash = dot * 3
        symbol_space = dot
        char_space = dot * 3
        word_space = dot * 7

        self.light_off()
        time.sleep(1) # 開始前預留一秒準備

        for i, char in enumerate(text):
            if self.cancel_flag:
                break
                
            if char == ' ':
                # 單字/群組之間的空白停頓
                time.sleep(word_space - char_space) 
                continue

            morse = MORSE_CODE_DICT.get(char, "")
            for j, symbol in enumerate(morse):
                if self.cancel_flag:
                    break
                
                self.light_on()
                time.sleep(dot if symbol == '.' else dash)
                self.light_off()
                
                # 符號間的停頓 (同一個字母內的點劃間隔)
                if j < len(morse) - 1:
                    time.sleep(symbol_space)
            
            # 字母間的停頓
            time.sleep(char_space)

        self.is_flashing = False
        self.light_off()

    def trigger_flash_thread(self):
        threading.Thread(target=self.play_morse_sequence, args=(self.current_text,), daemon=True).start()

    def next_question(self):
        if self.is_flashing:
            self.stop_flashing()
            time.sleep(0.2) # 稍等執行緒結束
            
        self.current_text = self.generate_text()
        self.result_label.config(text="")
        self.entry.delete(0, tk.END)
        self.entry.focus()
        self.trigger_flash_thread()

    def replay_signal(self):
        if self.is_flashing or not self.current_text:
            return
        self.trigger_flash_thread()

    def stop_flashing(self):
        self.cancel_flag = True

    def check_answer(self, event=None):
        if not self.current_text:
            return
        ans = self.entry.get().strip().upper()
        
        if ans == self.current_text:
            self.result_label.config(text=f"✔ 完全正確！\n答案: {self.current_text}", fg="#00ff66")
        else:
            self.result_label.config(text=f"✘ 錯誤！\n正確答案: {self.current_text}\n你的輸入: {ans}", fg="#ff4444")

if __name__ == "__main__":
    tk_root = tk.Tk()
    app = MorseProApp(tk_root)
    tk_root.mainloop()