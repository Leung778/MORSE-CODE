import random
import time
from meta import META, clear_screen

REALMS = [
    {"name": "練氣期", "max_age": 100, "req_exp": 100, "base_atk": 15},
    {"name": "築基期", "max_age": 200, "req_exp": 500, "base_atk": 50},
    {"name": "金丹期", "max_age": 500, "req_exp": 2000, "base_atk": 200}
]

class Player:
    def __init__(self):
        self.name = "梁玄"
        self.age = 26       # 預設 2000 年出生
        self.height = 163
        self.weight = 100.0 # 初始 100kg
        
        # 經濟與資源
        self.hkd = 3000
        self.crypto_holding = 0
        
        # 戰鬥與生存狀態
        self.hp = 120
        self.max_hp = 120
        self.mp = 50
        self.max_mp = 50
        self.stamina = 100       
        self.stress = 0          
        self.impurity = 30       
        
        # 境界與進度
        self.realm_idx = 0
        self.realm_level = 1     
        self.exp = 0
        
        self.base_atk = 15 
        self.base_def = 5
        self.weapon = {"name": "赤手空拳", "atk": 0, "agi": 0}
        
        # 環境與追蹤
        self.location = "深水埗劏房"
        self.days_survived = 1
        self.weather = "晴朗"
        self.weather_mult = 1.0
        self.monsters_killed = 0
        self.meta_perks = META.unlocked_perks # 導入天賦

    @property
    def current_realm(self):
        return REALMS[self.realm_idx]

    def get_agility(self):
        base_agi = 20 + self.weapon["agi"]
        if "天生神力" in self.meta_perks:
            weight_penalty = 0
        else:
            weight_penalty = max(0, (self.weight - 70) * 0.5)
        return int(base_agi - weight_penalty)
        
    def get_attack(self):
        atk = self.base_atk + self.weapon["atk"]
        if "天生神力" in self.meta_perks:
            atk += int(self.weight * 0.5)
        return int(atk * self.get_damage_multiplier())

    def get_magic_attack(self):
        matk = (self.base_atk * 1.5) + self.weapon["atk"]
        return int(matk * self.get_damage_multiplier())

    def get_damage_multiplier(self):
        return 1.0 + max(0, (self.age - 20) * 0.015)

    def display_status(self):
        clear_screen()
        print("="*55)
        print(f"📱 修真者 App - 存活: {self.days_survived} 天 | 天氣: {self.weather}")
        print("="*55)
        print(f"【境界】 {self.current_realm['name']} {self.realm_level} 層 (進度: {self.exp}/{self.current_realm['req_exp']})")
        print(f"【肉身】 {self.age} 歲 | {self.height}cm | 體重: {self.weight:.1f}kg")
        print(f"【狀態】 氣血: {self.hp}/{self.max_hp} | 靈力: {self.mp}/{self.max_mp}")
        print(f"【戰鬥】 身法: {self.get_agility()} | 物攻: {self.get_attack()} | 法強: {self.get_magic_attack()}")
        print(f"【日常】 精力: {self.stamina}/100 | 壓力: {self.stress}/100 | 濁氣: {self.impurity}%")
        print(f"【資產】 HKD: ${self.hkd} | 地段: {self.location}")
        if self.meta_perks: print(f"【天賦】 {', '.join(self.meta_perks)}")
        print("="*55)

    def attempt_breakthrough(self):
        if self.exp >= self.current_realm["req_exp"]:
            print("\n⚡ 靈力達到瓶頸，開始嘗試突破境界！")
            time.sleep(1)
            base_chance = 85
            age_penalty = max(0, (self.age - 25) * 1.5)
            final_chance = max(5, base_chance - age_penalty - (self.impurity * 0.5) - (self.stress * 0.3))
            
            print(f"> 綜合突破成功率: {final_chance:.1f}%")
            time.sleep(1)
            
            if random.randint(1, 100) <= final_chance:
                if self.realm_level < 9:
                    self.realm_level += 1
                else:
                    self.realm_idx = min(len(REALMS)-1, self.realm_idx + 1)
                    self.realm_level = 1
                self.exp = 0
                self.max_hp += 50
                self.hp = self.max_hp
                self.impurity = max(0, self.impurity - 20)
                print(f"🎉 突破成功！當前境界：{self.current_realm['name']} {self.realm_level} 層！")
            else:
                self.hp -= 40
                self.exp = int(self.exp * 0.8)
                self.stress += 20
                print("💥 突破失敗！遭到天劫反噬，扣除 40 氣血！")
            input("\n按 Enter 繼續...")
