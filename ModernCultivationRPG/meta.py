import os
import time

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

class MetaProgression:
    def __init__(self):
        self.karma_points = 0      # 陰德點數
        self.unlocked_perks = []   # 已解鎖天賦

# 全域單例，確保跨局繼承
META = MetaProgression()

PERKS_DB = {
    "天生神力": {"cost": 200, "desc": "100kg體重不再扣身法，每1kg轉化為0.5物攻。"},
    "拆二代散修": {"cost": 300, "desc": "自帶收租唐樓，免房租，每日自動獲得 $300 HKD，修為+10。"},
    "歐皇血統": {"cost": 250, "desc": "暗網抽卡時，SSR/SR 機率大幅提升！"},
    "水靈根": {"cost": 250, "desc": "遭遇海妖閃避大增，碼頭打工收益增加。"}
}

def reincarnation_system(player):
    """處理玩家死亡後的結算與天賦購買"""
    clear_screen()
    print("\n" + "💀"*20)
    print("【天道地府 結算中...】")
    time.sleep(1)
    
    realm_karma = (player.realm_idx + 1) * 50
    money_karma = player.hkd // 100
    kill_karma = getattr(player, 'monsters_killed', 0) * 10
    
    total_gained = realm_karma + money_karma + kill_karma
    META.karma_points += total_gained
    
    print(f"- 最終境界: {player.current_realm['name']} (+{realm_karma} 陰德)")
    print(f"- 燒毀資產: ${player.hkd} (+{money_karma} 陰德)")
    print(f"- 降妖除魔: {getattr(player, 'monsters_killed', 0)} 隻 (+{kill_karma} 陰德)")
    print(f"\n✨ 本局獲得: {total_gained} 陰德點數 | 總計持有: {META.karma_points}")
    input("\n按 Enter 走向奈何橋，準備重生...")
    
    while True:
        clear_screen()
        print("="*45)
        print(f"🏮 孟婆湯攤位 - 選擇來世天賦 (持有陰德: {META.karma_points})")
        print("="*45)
        
        options = list(PERKS_DB.keys())
        for i, perk in enumerate(options):
            status = "【已擁有】" if perk in META.unlocked_perks else f"(花費: {PERKS_DB[perk]['cost']})"
            print(f"{i+1}. {perk} {status}\n   - {PERKS_DB[perk]['desc']}")
            
        print(f"{len(options)+1}. 不買了，直接喝湯投胎")
        
        choice = input("\n請選擇要購買的天賦編號: ")
        if choice.isdigit() and int(choice) == len(options) + 1:
            print("\n你喝下孟婆湯，靈魂墜入輪迴井...")
            time.sleep(1.5)
            break
        elif choice.isdigit() and 1 <= int(choice) <= len(options):
            perk_name = options[int(choice)-1]
            if perk_name in META.unlocked_perks:
                print("❌ 你已經擁有這個天賦了！")
            elif META.karma_points >= PERKS_DB[perk_name]['cost']:
                META.karma_points -= PERKS_DB[perk_name]['cost']
                META.unlocked_perks.append(perk_name)
                print(f"\n✅ 成功購買天賦：{perk_name}！")
            else:
                print("\n❌ 陰德點數不足！")
            time.sleep(1)
