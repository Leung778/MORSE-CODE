# economy.py
import random
import time

class CryptoMarket:
    def __init__(self):
        self.coin_name = "靈虛幣 (LXC)"
        self.current_price = 100.0  # 初始價格

    def update_daily_price(self):
        """每天價格隨機暴漲或暴跌"""
        fluctuation = random.uniform(0.5, 2.0) # 暴跌50% 到 暴漲200%
        self.current_price = int(self.current_price * fluctuation)
        # 莊家跑路機制 (極低機率歸零)
        if random.randint(1, 100) <= 2:
            self.current_price = 1
            print("\n📉 【新聞】靈虛幣莊家捲款跑路！幣價瞬間歸零！")

    def open_market(self, player):
        """開啟交易所介面"""
        print(f"\n📈 暗網交易所 - 當前 {self.coin_name} 價格: HKD ${self.current_price}")
        print(f"你的資產: HKD ${player.hkd} | 持有 {self.coin_name}: {getattr(player, 'crypto_holding', 0)} 枚")
        
        choice = input("1. 買入  2. 賣出  3. 離開 -> ")
        if choice == '1':
            amount = int(input("輸入買入數量: "))
            cost = amount * self.current_price
            if player.hkd >= cost:
                player.hkd -= cost
                player.crypto_holding = getattr(player, 'crypto_holding', 0) + amount
                print(f"✅ 成功花費 ${cost} 買入 {amount} 枚。")
            else:
                print("❌ 餘額不足！")
        elif choice == '2':
            holding = getattr(player, 'crypto_holding', 0)
            amount = int(input(f"輸入賣出數量 (最多 {holding}): "))
            if 0 < amount <= holding:
                player.crypto_holding -= amount
                earnings = amount * self.current_price
                player.hkd += earnings
                print(f"💰 成功賣出，獲得 HKD ${earnings}！")
            else:
                print("❌ 數量無效！")
        time.sleep(1)
