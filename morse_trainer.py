import tkinter as tk
from tkinter import ttk, messagebox
import time
import threading
import random
import string

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

CHAR_SET = list(MORSE_CODE_DICT.keys())

class MorseTrainerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("INTERCO 摩斯信號綜合訓練系統")
        self.root.geometry("620x720")
        self.root.configure(bg="#1a1a1a")

        self.wpm = 6.0  # 航海考試常用 6 WPM
        self.is_flashing = False
        self.stop_requested = False
        self.current_single_char = ""
        self.block_target_text = ""

        self.setup_ui()

    def setup_ui(self):
        # 標題
        tk.Label(self.root, text="MORSE FLASHING LIGHT TRAINER", 
                 font=("Consolas", 15, "bold"), fg="#ffffff", bg="#1a1a1a").pack(pady=10)

        # 信號燈畫布
        self.canvas = tk.Canvas(self.root, width=180, height=180, bg="#1a1a1a", highlightthickness=0)
        self.canvas.pack(pady=5)
        self.canvas.create_oval(10, 10, 170, 170, fill="#2b2b2b", outline="#555555", width=4)
        self.lamp = self.canvas.create_oval(25, 25, 155, 155, fill="#121212", outline="")

        # 速度調整
        speed_frame = tk.Frame(self.root, bg="#1a1a1a")
        speed_frame.pack(pady=5)
        tk.Label(speed_frame, text="發報速度 (WPM):", fg="#cccccc", bg="#1a1a1a", font=("Consolas", 10)).pack(side=tk.LEFT)
        self.wpm_slider = tk.Scale(speed_frame, from_=3.0, to=12.0, resolution=0.5, orient=tk.HORIZONTAL,
                                   fg="#ffffff", bg="#1a1a1a", highlightthickness=0, command=self.update_wpm)
        self.wpm_slider.set(self.wpm)
        self.wpm_slider.pack(side=tk.LEFT, padx=8)

        # 分頁切換 (Notebook)
        style = ttk.Style()
        style.theme_use('default')
        style.configure('TNotebook', background="#1a1a1a", borderwidth=0)
        style.configure('TNotebook.Tab', background="#333333", foreground="#ffffff", padding=[10, 5])
        style.map('TNotebook.Tab', background=[('selected', '#007acc')])

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # 分頁 1: 單字鍛鍊
        self.tab_single = tk.Frame(self.notebook, bg="#242424")
        self.notebook.add(self.tab_single, text="  單字元鍛鍊 (Single Char)  ")
        self.setup_single_tab()

        # 分頁 2: 60字段落鍛鍊
        self.tab_block = tk.Frame(self.notebook, bg="#242424")
        self.notebook.add(self.tab_block, text="  60 字段落測驗 (Morse Block)  ")
        self.setup_block_tab()

    # --- 單字元介面 ---
    def setup_single_tab(self):
        btn_frame = tk.Frame(self.tab_single, bg="#242424")
        btn_frame.pack(pady=15)
        
        tk.Button(btn_frame, text="下一題 (Next)", font=("Consolas", 11, "bold"),
                  bg="#007acc", fg="white", padx=10, command=self.next_single_char).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="重播燈號 (F1)", font=("Consolas", 11),
                  bg="#444444", fg="white", padx=10, command=self.replay_single_char).pack(side=tk.LEFT, padx=5)

        tk.Label(self.tab_single, text="請輸入識別出的字元 (Enter 送出):", 
                 font=("Consolas", 11), fg="#aaaaaa", bg="#242424").pack(pady=5)

        self.single_entry = tk.Entry(self.tab_single, font=("Consolas", 20, "bold"), width=5, justify="center")
        self.single_entry.pack(pady=5)
        self.single_entry.bind("<Return>", self.check_single_answer)
        self.root.bind("<F1>", lambda e: self.replay_single_char())

        self.single_result = tk.Label(self.tab_single, text="", font=("Consolas", 13, "bold"), bg="#242424")
        self.single_result.pack(pady=10)

    # --- 60字段落介面 ---
    def setup_block_tab(self):
        ctrl_frame = tk.Frame(self.tab_block, bg="#242424")
        ctrl_frame.pack(pady=10)

        self.btn_start_block = tk.Button(ctrl_frame, text="開始發報 60 字", font=("Consolas", 11, "bold"),
                                         bg="#28a745", fg="white", padx=8, command=self.start_block_transmission)
        self.btn_start_block.pack(side=tk.LEFT, padx=5)

        self.btn_stop_block = tk.Button(ctrl_frame, text="中途停止", font=("Consolas", 11),
                                        bg="#dc3545", fg="white", padx=8, state=tk.DISABLED, command=self.stop_transmission)
        self.btn_stop_block.pack(side=tk.LEFT, padx=5)

        self.block_status = tk.Label(self.tab_block, text="請準備紙筆抄報，或於結束後在下方輸入。", 
                                     font=("Consolas", 10), fg="#aaaaaa", bg="#242424")
        self.block_status.pack(pady=3)

        tk.Label(self.tab_block, text="抄報核對區 (可直接貼上或輸入 60 字後點核對):", 
                 font=("Consolas", 10), fg="#cccccc", bg="#242424").pack(pady=2)

        self.txt_user_input = tk.Text(self.tab_block, height=3, width=50, font=("Consolas", 11))
        self.txt_user_input.pack(pady=5)

        tk.Button(self.tab_block, text="核對抄報成績", font=("Consolas", 10, "bold"),
                  bg="#ffc107", fg="#000000", command=self.verify_block_result).pack(pady=5)

        self.block_result_label = tk.Label(self.tab_block, text="", font=("Consolas", 11), bg="#242424")
        self.block_result_label.pack(pady=5)

    # --- 燈號時序控制核心 ---
    def update_wpm(self, val):
        self.wpm = float(val)

    def light_on(self):
        self.canvas.itemconfig(self.lamp, fill="#ffff33")
        self.root.update_idletasks()

    def light_off(self):
        self.canvas.itemconfig(self.lamp, fill="#121212")
        self.root.update_idletasks()

    def wait(self, duration):
        start = time.time()
        while time.time() - start < duration:
            if self.stop_requested:
                break
            time.sleep(0.01)

    def play_character(self, char, dot_duration):
        pattern = MORSE_CODE_DICT.get(char, "")
        for symbol in pattern:
            if self.stop_requested:
                break
            if symbol == '.':
                self.light_on()
                self.wait(dot_duration)
            elif symbol == '-':
                self.light_on()
                self.wait(dot_duration * 3)
            self.light_off()
            self.wait(dot_duration)  # 符號內間隔

    # --- 單字模式邏輯 ---
    def next_single_char(self):
        if self.is_flashing:
            return
        self.current_single_char = random.choice(CHAR_SET)
        self.single_result.config(text="")
        self.single_entry.delete(0, tk.END)
        self.single_entry.focus()
        threading.Thread(target=self._run_single_flash, daemon=True).start()

    def replay_single_char(self):
        if self.is_flashing or not self.current_single_char:
            return
        threading.Thread(target=self._run_single_flash, daemon=True).start()

    def _run_single_flash(self):
        self.is_flashing = True
        self.stop_requested = False
        dot_duration = 1.2 / self.wpm
        self.light_off()
        self.wait(0.3)
        self.play_character(self.current_single_char, dot_duration)
        self.is_flashing = False

    def check_single_answer(self, event=None):
        if not self.current_single_char:
            return
        ans = self.single_entry.get().strip().upper()
        if ans == self.current_single_char:
            self.single_result.config(text=f"✔ 正確！ 答案是 【 {self.current_single_char} 】", fg="#00ff66")
        else:
            morse = MORSE_CODE_DICT[self.current_single_char]
            self.single_result.config(text=f"✘ 錯誤！ 答案是 【 {self.current_single_char} 】 ({morse})", fg="#ff4444")

    # --- 60字段落模式邏輯 ---
    def generate_60_chars(self):
        # 產生 60 個隨機大寫字母與數字
        raw = "".join(random.choices(CHAR_SET, k=60))
        # 航海規範：每 5 個字元分成一組 (Group)，共 12 組
        groups = [raw[i:i+5] for i in range(0, 60, 5)]
        return raw, " ".join(groups)

    def start_block_transmission(self):
        if self.is_flashing:
            return
        raw_text, formatted_text = self.generate_60_chars()
        self.block_target_text = raw_text
        self.block_result_label.config(text="")
        self.txt_user_input.delete("1.0", tk.END)

        self.btn_start_block.config(state=tk.DISABLED)
        self.btn_stop_block.config(state=tk.NORMAL)

        threading.Thread(target=self._run_block_flash, args=(formatted_text,), daemon=True).start()

    def stop_transmission(self):
        self.stop_requested = True

    def _run_block_flash(self, formatted_text):
        self.is_flashing = True
        self.stop_requested = False
        dot_duration = 1.2 / self.wpm

        self.block_status.config(text="燈號發報中... 請專注抄報", fg="#00ccff")
        self.light_off()
        self.wait(1.0)  # 發報前準備時間

        char_count = 0
        for char in formatted_text:
            if self.stop_requested:
                break
            if char == ' ':
                # 組與組之間的間隔 (標準為 7 個 dot，扣除前面已留的 3 個 dot，補 4 個)
                self.wait(dot_duration * 4)
            else:
                char_count += 1
                self.block_status.config(text=f"發報中... [{char_count}/60]", fg="#ffff33")
                self.play_character(char, dot_duration)
                # 字元與字元之間的間隔 (標準為 3 個 dot，扣除符號尾的 1 個，補 2 個)
                self.wait(dot_duration * 2)

        self.light_off()
        self.is_flashing = False
        self.btn_start_block.config(state=tk.NORMAL)
        self.btn_stop_block.config(state=tk.DISABLED)

        if self.stop_requested:
            self.block_status.config(text="已由使用者中止發報", fg="#ff4444")
        else:
            self.block_status.config(text="✔ 發報完畢！請在下方輸入抄報結果進行比對", fg="#00ff66")

    def verify_block_result(self):
        if not self.block_target_text:
            messagebox.showinfo("提示", "尚未執行任何段落測驗！")
            return

        # 忽略空格與換行，統一轉大寫比對
        user_str = self.txt_user_input.get("1.0", tk.END).strip().replace(" ", "").replace("\n", "").upper()
        target = self.block_target_text

        correct_count = 0
        for u, t in zip(user_str, target):
            if u == t:
                correct_count += 1

        accuracy = (correct_count / len(target)) * 100

        # 顯示比對結果
        report = (
            f"正確字數: {correct_count} / {len(target)} ({accuracy:.1f}%)\n\n"
            f"原始題目 (每5字一組):\n{' '.join([target[i:i+5] for i in range(0, 60, 5)])}\n\n"
            f"你的抄報 (前60字):\n{' '.join([user_str[i:i+5] for i in range(0, min(len(user_str), 60), 5)])}"
        )
        self.block_result_label.config(text=report, fg="#ffffff", justify=tk.LEFT)

if __name__ == "__main__":
    tk_root = tk.Tk()
    app = MorseTrainerApp(tk_root)
    tk_root.mainloop()