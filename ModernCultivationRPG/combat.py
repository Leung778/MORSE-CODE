import time
import random

class Enemy:
    def __init__(self, name, hp, atk, def_stat, agi, drop_money, exp):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.atk = atk
        self.def_stat = def_stat
        self.agi = agi
        self.drop_money = drop_money
        self.drop_exp = exp

# 都市妖獸圖鑑
ENEMIES = {
    "下水道噬靈鼠": lambda: Enemy("下水道噬靈鼠", hp=40, atk=8, def_stat=2, agi=35, drop_money=150, exp=20),
    "變異古惑仔": lambda: Enemy("變異古惑仔(妖化)", hp=80, atk=15, def_stat=5, agi=20, drop_money=300, exp=40),
    "重訓室虎妖": lambda: Enemy("重訓室虎妖", hp=150, atk=30, def_stat=10, agi=15, drop_money=800, exp=100),
    "變異海妖": lambda: Enemy("維港變異海妖", hp=250, atk=45, def_stat=20, agi=25, drop_money=2000, exp=300)
}

def battle_system(player, enemy):
    """回合制戰鬥判定，包含物理與法術攻擊"""
    import os
    os.system('cls' if os.name == 'nt' else 'clear')
    print("="*40)
    print(f"🚨 遭遇戰鬥！ {enemy.name} 出現了！")
    print("="*40)
    time.sleep(1)

    while player.hp > 0 and enemy.hp > 0:
        print(f"\n[{player.name}] HP: {player.hp}/{player.max_hp} | MP: {player.mp}/{player.max_mp} | 身法: {player.get_agility()}")
        print(f"[{enemy.name}] HP: {enemy.hp}/{enemy.max_hp} | 身法: {enemy.agi}")
        
        choice = input("\n選擇行動: (1) 物理攻擊 (2) 法術(耗20MP) (3) 逃跑 -> ")

        if choice == '3':
            if random.randint(1, 100) <= max(10, 50 + (player.get_agility() - enemy.agi) * 2):
                print("🏃 成功甩開了妖怪！")
                return True
            print("💥 逃跑失敗！")
        
        elif choice in ['1', '2']:
            # 玩家攻擊
            if choice == '2':
                if player.mp >= 20:
                    player.mp -= 20
                    dmg = max(1, player.get_magic_attack() - int(enemy.def_stat * 0.2)) # 法術貫穿部分防禦
                    enemy.hp -= dmg
                    print(f"⚡ 釋放法術！對 {enemy.name} 造成了 {dmg} 點穿透傷害！")
                else:
                    print("❌ 靈力不足，施法失敗！(損失一回合)")
            else:
                if random.randint(1, 100) <= 90:
                    dmg = max(1, player.get_attack() - enemy.def_stat)
                    enemy.hp -= dmg
                    print(f"⚔️ 物理攻擊命中！對 {enemy.name} 造成了 {dmg} 點傷害！")
                else:
                    print("💨 你的攻擊被閃避了！")

            # 妖怪反擊
            if enemy.hp > 0:
                time.sleep(0.5)
                # 水靈根對海妖閃避加成
                dodge_bonus = 20 if "水靈根" in getattr(player, 'meta_perks', []) and "海妖" in enemy.name else 0
                if random.randint(1, 100) <= max(5, 80 - player.get_agility() + dodge_bonus):
                    edmg = max(1, enemy.atk - player.base_def)
                    player.hp -= edmg
                    print(f"💥 {enemy.name} 反擊，對你造成 {edmg} 點傷害！")
                else:
                    print(f"💨 你閃避了 {enemy.name} 的攻擊！")

    time.sleep(1)
    if player.hp > 0:
        print(f"\n🎉 戰鬥勝利！獲得 HKD ${enemy.drop_money}，修為 +{enemy.drop_exp}。")
        player.hkd += enemy.drop_money
        player.exp += enemy.drop_exp
        player.monsters_killed = getattr(player, 'monsters_killed', 0) + 1
        input("\n按 Enter 繼續...")
        return True
    return False
