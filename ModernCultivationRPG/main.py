import time
from player import Player
from economy import CryptoMarket, work, black_market
from events import take_subway, pass_day_logic
from meta import reincarnation_system

def main():
    crypto = CryptoMarket()
    
    while True: # 輪迴大迴圈
        p = Player()
        print("【系統】歡迎來到《現代修仙生存 RPG》")
        print("生存法則：兼顧精力、壓力與房租，努力突破境界！")
        input("按 Enter 開始這一世...")
        
        while p.hp > 0:
            p.display_status()
            print("\n行動清單：")
            print("1. 💼 出門打工 (耗40精力 | 賺錢 | 有機率遇怪)")
            print("2. 🧘 在家修煉 (耗30精力 | 增修為/恢MP)")
            print("3. 🚇 搭乘港鐵 (探索奇遇/裏世界)")
            print("4. 📈 暗網交易所 (炒幣/盲盒抽卡)")
            print("5. 🛌 結束今天 (結算天氣與生存狀態)")
            print("6. 💀 自殺重開 (結算陰德)")
            
            choice = input("\n請選擇: ")
            
            if choice == '1':
                work(p)
            elif choice == '2':
                if p.stamina >= 30:
                    p.stamina -= 30
                    gain = int(25 * p.weather_mult * (1 - p.impurity/100))
                    p.exp += max(1, gain)
                    p.mp = min(p.max_mp, p.mp + 20)
                    p.stress = max(0, p.stress - 5)
                    print(f"\n🧘 吸收靈氣，修為 +{gain}，靈力恢復。")
                    p.attempt_breakthrough()
                    input("按 Enter 繼續...")
                else:
                    print("\n❌ 精力不足！")
                    time.sleep(1)
            elif choice == '3':
                take_subway(p)
            elif choice == '4':
                print("\n1. 炒作靈虛幣  2. 購買盲盒 ($1000)")
                sub = input("選擇 -> ")
                if sub == '1': crypto.open_market(p)
                elif sub == '2': black_market(p)
            elif choice == '5':
                pass_day_logic(p)
                crypto.update_price()
                # 房租邏輯
                if p.days_survived % 30 == 0 and "拆二代散修" not in p.meta_perks:
                    if p.hkd >= 4000:
                        p.hkd -= 4000
                        print("\n📅 成功繳納劏房租金 $4000。")
                    else:
                        p.hkd = 0
                        p.hp -= 30
                        p.stress += 30
                        print("\n❌ 交不出房租！流落街頭扣血增壓！")
                    time.sleep(2)
            elif choice == '6':
                p.hp = 0
        
        # 角色死亡，進入輪迴結算
        reincarnation_system(p)
        
        play_again = input("\n是否開啟下一世？(y/n): ")
        if play_again.lower() != 'y':
            print("感謝遊玩！")
            break

if __name__ == "__main__":
    main()
