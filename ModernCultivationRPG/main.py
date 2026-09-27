# main.py
import time
from player import Player
from economy import CryptoMarket
from events import take_subway

def main():
    p = Player() # 假設 player.py 中已定義 Player 類別
    crypto_market = CryptoMarket()
    
    while p.hp > 0:
        p.display_status()
        print("\n行動清單：")
        print("1. 🚇 搭乘港鐵探索 (耗精力10, $20, 有機率遇靈異事件)")
        print("2. 📈 登入暗網炒幣 (高風險投資)")
        print("3. 🛌 結束今天")
        
        choice = input("\n請選擇: ")
        
        if choice == '1':
            take_subway(p)
        elif choice == '2':
            crypto_market.open_market(p)
        elif choice == '3':
            # 換日結算，並更新虛擬幣價格
            p.pass_day()
            crypto_market.update_daily_price()
            
    print("\n💀 你死了。遊戲結束。")

if __name__ == "__main__":
    main()
