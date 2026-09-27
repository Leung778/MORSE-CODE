# events.py
import random
import time

def take_subway(player):
    """搭乘港鐵移動的事件"""
    cost = 20
    if player.hkd < cost:
        print("\n❌ 八達通餘額不足！")
        return
        
    player.hkd -= cost
    player.stamina -= 10
    print("\n🚇 你刷八達通進入了港鐵站...")
    time.sleep(1)
    
    # 10% 機率進入裏世界
    if random.randint(1, 100) <= 10:
        print("\n⚠️ 列車突然劇烈搖晃，燈光閃爍...")
        print("廣播傳來雜音：『下一站，裏·彩虹站...』")
        time.sleep(2)
        
        event_roll = random.randint(1, 2)
        if event_roll == 1:
            print("👻 【遭遇】你撞見了高階怨靈！")
            player.stress += 30
            player.hp -= 40
            print("你拼死逃出車廂，受了重傷 (HP -40, 壓力 +30)！")
        else:
            print("📦 【奇遇】你發現了一個無人的地下黑市攤位！")
            loot = random.randint(1000, 5000)
            player.hkd += loot
            print(f"你搜刮了攤位，獲得 HKD ${loot} 後趕緊逃離！")
    else:
        print("✅ 平安抵達目的地。")
    
    input("\n按 Enter 繼續...")
