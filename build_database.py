import json
import urllib.request

# Lista com os arquivos individuais exatos mantidos pela comunidade
FILES = [
    "Warframes.json", "Primary.json", "Secondary.json", "Melee.json",
    "Sentinels.json", "Pets.json", "Archwing.json", "Arch-Gun.json",
    "Arch-Melee.json", "Misc.json"
]
BASE_URL = "https://raw.githubusercontent.com/WFCD/warframe-items/master/data/json/"

CATEGORY_MAP = {
    "Warframes": ("equipment", "Warframes", 6000),
    "Primary": ("equipment", "Primaries", 3000),
    "Secondary": ("equipment", "Secondaries", 3000),
    "Melee": ("equipment", "Melee", 3000),
    "Sentinels": ("companions", "Sentinels", 6000),
    "Pets": ("companions", "Beasts", 6000),
    "Archwing": ("heavy", "Archwings", 6000),
    "Arch-Gun": ("heavy", "Arch-Weapons", 3000),
    "Arch-Melee": ("heavy", "Arch-Melee", 3000),
    "Necramechs": ("heavy", "Necramechs", 8000),
}

def resolve_tier(item):
    name = item.get("name", "")
    category = item.get("category", "")
    
    if any(k in name for k in ["Kuva ", "Tenet ", "Ceti "]) or name in ["Paracesis", "Voidrig", "Bonewidow"]: return 7
    if "Prime" in name or item.get("relics"): return 6
    if any(k in name for k in ["Vandal", "Wraith", "Prisma", "Telos", "Synoid", "Secura", "Rakta", "Sancti", "Vaykor"]): return 5
    if name.startswith("MK1-") or name in ["Braton", "Lato", "Lex", "Strun", "Aklato", "Sicarus", "Zenith", "Zenistar", "Azima", "Sigma & Octantis"]: return 1
    if "Research" in str(item.get("components", [])) or "Laboratory" in str(item): return 3
    if category in ["Warframes", "Archwing", "Pets", "Necramechs"]: return 4
    return 2

processed_items = []
seen_names = set()

print("Baixando e tratando dados do Warframe...")

# Faz o download de categoria por categoria
for file_name in FILES:
    url = BASE_URL + file_name
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as response:
            raw_data = json.loads(response.read().decode())
            
        for item in raw_data:
            name = item.get("name")
            category = item.get("category")
            
            if not name or name in seen_names:
                continue
            
            if item.get("productCategory") == "SpecialItems" or "PVPOnly" in str(item):
                continue
                
            if category in CATEGORY_MAP:
                group, sub, base_xp = CATEGORY_MAP[category]
                
                if any(k in name for k in ["Kuva ", "Tenet "]) or name == "Paracesis":
                    base_xp = 4000
                    
                tier = resolve_tier(item)
                item_id = item.get("uniqueName", name).replace("/", "_").replace(".", "_")

                processed_items.append({
                    "id": item_id,
                    "name": name,
                    "group": group,
                    "sub": sub,
                    "xp": base_xp,
                    "tier": tier
                })
                seen_names.add(name)
    except Exception as e:
        print(f"Aviso: Falha ao tentar baixar {file_name}. Erro: {e}")

# Inclui os nós do Star Chart condensados
starchart_entries = [
    {"id": "sc_earth", "name": "Earth Clearance", "group": "starchart", "sub": "Star Chart Nodes", "xp": 1542, "tier": 4},
    {"id": "sc_venus", "name": "Venus Clearance", "group": "starchart", "sub": "Star Chart Nodes", "xp": 1698, "tier": 4},
    {"id": "sc_mercury", "name": "Mercury Clearance", "group": "starchart", "sub": "Star Chart Nodes", "xp": 1240, "tier": 4},
    {"id": "sc_mars", "name": "Mars Clearance", "group": "starchart", "sub": "Star Chart Nodes", "xp": 1820, "tier": 4},
    {"id": "sc_phobos", "name": "Phobos Clearance", "group": "starchart", "sub": "Star Chart Nodes", "xp": 1100, "tier": 4},
    {"id": "sc_ceres", "name": "Ceres Clearance", "group": "starchart", "sub": "Star Chart Nodes", "xp": 1450, "tier": 4},
    {"id": "sc_jupiter", "name": "Jupiter Clearance", "group": "starchart", "sub": "Star Chart Nodes", "xp": 1980, "tier": 4},
    {"id": "sc_europa", "name": "Europa Clearance", "group": "starchart", "sub": "Star Chart Nodes", "xp": 1500, "tier": 4},
    {"id": "sc_saturn", "name": "Saturn Clearance", "group": "starchart", "sub": "Star Chart Nodes", "xp": 1720, "tier": 4},
    {"id": "sc_uranus", "name": "Uranus Clearance", "group": "starchart", "sub": "Star Chart Nodes", "xp": 1890, "tier": 4},
    {"id": "sc_neptune", "name": "Neptune Clearance", "group": "starchart", "sub": "Star Chart Nodes", "xp": 1750, "tier": 4},
    {"id": "sc_pluto", "name": "Pluto Clearance", "group": "starchart", "sub": "Star Chart Nodes", "xp": 1810, "tier": 4},
    {"id": "sc_sedna", "name": "Sedna Clearance", "group": "starchart", "sub": "Star Chart Nodes", "xp": 2100, "tier": 4},
    {"id": "sc_void", "name": "Void Clearance", "group": "starchart", "sub": "Star Chart Nodes", "xp": 1950, "tier": 4},
    {"id": "sc_deimos", "name": "Deimos Clearance", "group": "starchart", "sub": "Star Chart Nodes", "xp": 1200, "tier": 4},
    {"id": "sc_luacav", "name": "Lua & Zariman Clearance", "group": "starchart", "sub": "Star Chart Nodes", "xp": 2500, "tier": 4},
    
    # Steel Path condensado
    {"id": "sc_sp_earth", "name": "Steel Path: Earth", "group": "starchart", "sub": "Steel Path", "xp": 1542, "tier": 7},
    {"id": "sc_sp_venus", "name": "Steel Path: Venus", "group": "starchart", "sub": "Steel Path", "xp": 1698, "tier": 7},
    {"id": "sc_sp_mercury", "name": "Steel Path: Mercury", "group": "starchart", "sub": "Steel Path", "xp": 1240, "tier": 7},
    {"id": "sc_sp_mars", "name": "Steel Path: Mars", "group": "starchart", "sub": "Steel Path", "xp": 1820, "tier": 7},
    {"id": "sc_sp_phobos", "name": "Steel Path: Phobos", "group": "starchart", "sub": "Steel Path", "xp": 1100, "tier": 7},
    {"id": "sc_sp_ceres", "name": "Steel Path: Ceres", "group": "starchart", "sub": "Steel Path", "xp": 1450, "tier": 7},
    {"id": "sc_sp_jupiter", "name": "Steel Path: Jupiter", "group": "starchart", "sub": "Steel Path", "xp": 1980, "tier": 7},
    {"id": "sc_sp_europa", "name": "Steel Path: Europa", "group": "starchart", "sub": "Steel Path", "xp": 1500, "tier": 7},
    {"id": "sc_sp_saturn", "name": "Steel Path: Saturn", "group": "starchart", "sub": "Steel Path", "xp": 1720, "tier": 7},
    {"id": "sc_sp_uranus", "name": "Steel Path: Uranus", "group": "starchart", "sub": "Steel Path", "xp": 1890, "tier": 7},
    {"id": "sc_sp_neptune", "name": "Steel Path: Neptune", "group": "starchart", "sub": "Steel Path", "xp": 1750, "tier": 7},
    {"id": "sc_sp_pluto", "name": "Steel Path: Pluto", "group": "starchart", "sub": "Steel Path", "xp": 1810, "tier": 7},
    {"id": "sc_sp_sedna", "name": "Steel Path: Sedna", "group": "starchart", "sub": "Steel Path", "xp": 2100, "tier": 7},
    {"id": "sc_sp_void", "name": "Steel Path: Void", "group": "starchart", "sub": "Steel Path", "xp": 1950, "tier": 7},
    {"id": "sc_sp_deimos", "name": "Steel Path: Deimos", "group": "starchart", "sub": "Steel Path", "xp": 1200, "tier": 7},
    {"id": "sc_sp_luacav", "name": "Steel Path: Lua & Zariman", "group": "starchart", "sub": "Steel Path", "xp": 2500, "tier": 7},
]

# Geração de 1 a 10 para Railjack Intrinsics
rj_categories = ["Tactical", "Piloting", "Gunnery", "Engineering", "Command"]
for cat in rj_categories:
    for level in range(1, 11):
        starchart_entries.append({
            "id": f"int_rj_{cat.lower()}_{level}",
            "name": f"Railjack: {cat} Rank {level}",
            "group": "starchart",
            "sub": "Railjack Intrinsics",
            "xp": 1500,
            "tier": 4
        })

# Geração de 1 a 10 para Drifter Intrinsics
drifter_categories = ["Combat", "Riding", "Gunnery", "Endurance"]
for cat in drifter_categories:
    for level in range(1, 11):
        starchart_entries.append({
            "id": f"int_dr_{cat.lower()}_{level}",
            "name": f"Drifter: {cat} Rank {level}",
            "group": "starchart",
            "sub": "Drifter Intrinsics",
            "xp": 1500,
            "tier": 4
        })

processed_items.extend(starchart_entries)
import os

# Isso descobre exatamente em qual pasta este script (build_database.py) está salvo
pasta_atual = os.path.dirname(os.path.abspath(__file__))
caminho_arquivo = os.path.join(pasta_atual, "items.json")

with open(caminho_arquivo, "w", encoding="utf-8") as f:
    json.dump(processed_items, f, indent=2, ensure_ascii=False)

print(f"Sucesso! Gerado items.json contendo {len(processed_items)} itens de maestria na pasta: {pasta_atual}")
with open("items.json", "w", encoding="utf-8") as f:
    json.dump(processed_items, f, indent=2, ensure_ascii=False)

print(f"Sucesso! Gerado items.json contendo {len(processed_items)} itens de maestria.")