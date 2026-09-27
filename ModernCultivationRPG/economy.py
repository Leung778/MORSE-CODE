import random
import time
from combat import battle_system, ENEMIES

class CryptoMarket:
    def __init__(self):
        self.coin_name = "靈虛幣 (LXC)"
        self.price = 100.0

    def update_price(self):
        fluctuation = random.uniform(0.5, 2.0)
        self.price = int(self.price * fluctuation)
        if random.randint(1, 100) <= 2:
            self.price = 1 # 莊家跑路

    def open_market(self, player):
        print(f"\n📈 暗網交易所 - {self.coin_name} 價格: HKD ${self.price}")
        print(f"你的資金: ${player.hkd} | 持有: {player.crypto_holding} 枚")
        c = input("1. 買入 2. 賣出 3. 離開 -> ")
        if c == '1':
            amt = int(input("買入數量: "))
            if player.hkd >= amt * self.price:
                player.hkd -= amt * self.price
                player.crypto_holding += amt
                print("✅ 買入成功。")
            else:
                print("❌ 餘額不足！")
        elif c == '2':
            amt = int(input(f"賣出數量 (最多 {player.crypto_holding}): "))
            if 0 < amt <= player.crypto_holding:
                player.crypto_holding -= amt
                player.hkd += amt * self.price
                print("💰 賣出成功。")
        time.sleep(1)

def work(player):
    if player.stamina < 40:
        print("\n❌ 精力不足！")
        return
    if "十號風球" in player.weather:
        print("\n❌ 颱風天停工！")
        return

    player.stamina -= 40
    player.stress += 15
    player.impurity = min(100, player.impurity + 5)
    
    # 碼頭打工遇怪機率
    if random.randint(1, 100) <= 25:
        enemy_type = random.choice(list(ENEMIES.keys()))
        survived = battle_system(player, ENEMIES[enemy_type]())
        if not survived: return
    else:
        earned = random.randint(500, 1000)
        if "水靈根" in player.meta_perks: earned = int(earned * 1.5)
        player.hkd += earned
        player.weight -= 0.5
        print(f"\n📦 打工完成，獲得 HKD ${earned}，體重微降。壓力/濁氣上升。")
        input("按 Enter 繼續...")

def black_market(player):
    if player.hkd < 1000:
        print("\n❌ 餘額不足 $1000！")
        return
    
    player.hkd -= 1000
    pool = [
        {"name": "改裝壺鈴", "atk": 20, "agi": -5, "type": "equip"},
        {"name": "戰術飛劍", "atk": 45, "agi": 10, "type": "equip"},
        {"name": "洗髓丹", "hp": 50, "impurity": -30, "type": "pill"}
    ]
    item = random.choice(pool)
    print(f"\n📦 盲盒開啟！獲得：{item['name']}")
    if item['type'] == 'equip':
        player.weapon = {"name": item["name"], "atk": item["atk"], "agi": item["agi"]}
        print("⚔️ 已自動裝備！")
    else:
        player.hp = min(player.max_hp, player.hp + item["hp"])
        player.impurity = max(0, player.impurity + item["impurity"])
        print("💊 吞服丹藥，狀態改變！")
    input("\n按 Enter 繼續...")
