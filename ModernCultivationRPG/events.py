import random
import time
from combat import battle_system, ENEMIES

def trigger_weather(player):
    """每日生成天氣"""
    roll = random.randint(1, 100)
    if roll <= 10:
        player.weather = "十號風球 🌪️"
        player.weather_mult = 0.5
    elif roll >= 95:
        player.weather = "靈氣潮汐 ✨"
        player.weather_mult = 2.0
    else:
        player.weather = "晴朗 ☀️"
        player.weather_mult = 1.0

def pass_day_logic(player):
    """換日結算與生存判定"""
    player.days_survived += 1
    player.stamina = 100
    trigger_weather(player)
    
    if "拆二代散修" in player.meta_perks:
        player.hkd += 300
        player.exp += 10
        player.mp = min(player.max_mp, player.mp + 5)
        
    if player.stress >= 100:
        dmg = random.randint(20, 50)
        player.hp -= dmg
        player.stress = max(0, player.stress - 50)
        print(f"\n💥 【走火入魔】壓力崩潰，吐血受傷 (HP -{dmg})！")
        time.sleep(1)
        
    if player.days_survived % 10 == 0: 
        player.age += 1
        if player.age > player.current_realm["max_age"]:
            print(f"\n💀 突破無望，壽元已盡...")
            player.hp = 0

def take_subway(player):
    """地鐵靈異事件"""
    if player.hkd < 20 or player.stamina < 10:
        print("\n❌ 餘額或精力不足！")
        return
        
    player.hkd -= 20
    player.stamina -= 10
    print("\n🚇 你刷八達通進入了港鐵站...")
    time.sleep(1)
    
    if random.randint(1, 100) <= 15:
        print("\n⚠️ 列車劇烈搖晃，廣播傳來雜音：『下一站，裏·彩虹站...』")
        time.sleep(1)
        if random.randint(1, 2) == 1:
            print("👻 遭遇高階怨靈！壓力暴增，受傷逃離！")
            player.stress += 30
            player.hp -= 30
        else:
            loot = random.randint(1000, 3000)
            player.hkd += loot
            print(f"📦 發現無人黑市攤位，搜刮獲得 HKD ${loot}！")
    else:
        print("✅ 平安抵達。")
    input("\n按 Enter 繼續...")
