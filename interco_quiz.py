import random
import time
from colorama import init, Fore, Style

init(autoreset=True)

# 1. 題庫資料（從原程式提取的單字母與語音呼號標準資料）
INTERCO_DATA = {
    "A": {"phonetic": "Alfa", "meaning": "I have a diver down; keep well clear at slow speed."},
    "B": {"phonetic": "Bravo", "meaning": "I am taking in, or discharging, or carrying dangerous goods."},
    "C": {"phonetic": "Charlie", "meaning": "Affirmative (YES)."},
    "D": {"phonetic": "Delta", "meaning": "I am manoeuvring with difficulty; keep clear of me."},
    "E": {"phonetic": "Echo", "meaning": "I am altering my course to starboard."},
    "F": {"phonetic": "Foxtrot", "meaning": "I am disabled; communicate with me."},
    "G": {"phonetic": "Golf", "meaning": "I require a pilot. (Fishing: I am hauling nets)"},
    "H": {"phonetic": "Hotel", "meaning": "I have a pilot on board."},
    "I": {"phonetic": "India", "meaning": "I am altering my course to port."},
    "J": {"phonetic": "Juliet", "meaning": "I am on fire and have dangerous cargo; keep well clear."},
    "K": {"phonetic": "Kilo", "meaning": "I wish to communicate with you."},
    "L": {"phonetic": "Lima", "meaning": "You should stop your vessel instantly."},
    "M": {"phonetic": "Mike", "meaning": "My vessel is stopped and making no way through the water."},
    "N": {"phonetic": "November", "meaning": "Negative (NO)."},
    "O": {"phonetic": "Oscar", "meaning": "Man overboard."},
    "P": {"phonetic": "Papa", "meaning": "All persons should report on board; vessel is about to proceed to sea."},
    "Q": {"phonetic": "Quebec", "meaning": "My vessel is healthy and I request free pratique."},
    "R": {"phonetic": "Romeo", "meaning": "Has no single-letter meaning in INTERCO."},
    "S": {"phonetic": "Sierra", "meaning": "My engines are operating stern propulsion."},
    "T": {"phonetic": "Tango", "meaning": "I am engaged in pair trawling; keep clear."},
    "U": {"phonetic": "Uniform", "meaning": "You are running into danger."},
    "V": {"phonetic": "Victor", "meaning": "I require assistance."},
    "W": {"phonetic": "Whisky", "meaning": "I require medical assistance."},
    "X": {"phonetic": "X-ray", "meaning": "Stop carrying out your intentions and watch for my signals."},
    "Y": {"phonetic": "Yankee", "meaning": "I am dragging my anchor."},
    "Z": {"phonetic": "Zulu", "meaning": "I require a tug. (Fishing: I am shooting nets)"}
}

# 2. 測驗引擎
def run_quiz(mode="test", start_char="A", end_char="Z"):
    chars = [chr(c) for c in range(ord(start_char), ord(end_char) + 1)]
    pool = list(chars)
    random.shuffle(pool)
    
    total_questions = len(chars)
    score = 0
    asked = 0

    print(f"\n{Fore.CYAN}=== 國際信號代碼測驗 ({'測驗模式' if mode == 'test' else '教學模式'}) ===")
    print(f"範圍: {start_char} - {end_char} | 輸入 'Q' 可隨時退出\n")

    while pool:
        char = pool.pop(0)
        item = INTERCO_DATA[char]
        asked += 1

        # 隨機產生 4 個多選選項
        distractors = [k for k in INTERCO_DATA.keys() if k != char]
        choices = random.sample(distractors, 3) + [char]
        random.shuffle(choices)

        print(f"{Fore.YELLOW}[題目 {asked}] 信號旗字母: 【 {char} 】（語音呼號：{item['phonetic']}）")
        print("請問其代表的單字母信號意義為何？")
        for idx, key in enumerate(choices, 1):
            print(f"  {idx}. {INTERCO_DATA[key]['meaning']}")

        user_input = input(f"{Fore.GREEN}請選擇正確選項 (1-4): {Style.RESET_ALL}").strip()
        if user_input.upper() == 'Q':
            break

        correct_idx = str(choices.index(char) + 1)
        if user_input == correct_idx:
            print(f"{Fore.GREEN}✔ 正確！ +1 分\n")
            score += 1
        else:
            print(f"{Fore.RED}✘ 錯誤！ 正確答案是: {correct_idx}. {item['meaning']}")
            if mode == "tutorial":
                print(f"{Fore.YELLOW}↪ (教學模式：此題已放回題庫，稍後將再次測驗)\n")
                pool.append(char)
                random.shuffle(pool)
            else:
                print()

    print(f"{Fore.CYAN}================ 測驗結束 ================")
    print(f"總答對題數: {score} / {total_questions} ({score / total_questions * 100:.1f}%)")

# 3. 主選單
def main():
    while True:
        print(f"\n{Fore.WHITE}INTERCO 信號測驗系統 (Python 重寫版)")
        print("1. 測驗模式 (Test Mode - 單次計分)")
        print("2. 教學模式 (Tutorial Mode - 錯題重複出題)")
        print("3. 退出")
        choice = input("請輸入選項 (1-3): ").strip()

        if choice == "1":
            run_quiz(mode="test")
        elif choice == "2":
            run_quiz(mode="tutorial")
        elif choice == "3":
            break

if __name__ == "__main__":
    main()