"""
Divinity: Original Sin Enhanced Edition - Music Taxonomy
Contains metadata for all 106 in-game music tracks referenced by the Wwise audio engine.
Clean, emoji-free, multi-language definitions.
"""

import json
import os
import sys

CATEGORIES = [
    {
        "id": "menu",
        "name_en": "Main Menu",
        "name_ru": "Главное меню",
        "name_pl": "Menu główne",
        "name_it": "Menu principale",
        "name_de": "Hauptmenü",
        "name_fr": "Menu principal",
        "name_es": "Menú principal",
        "icon": "fa-crown",
        "description_en": "Title theme played at the launch screen",
        "description_ru": "Заглавная музыка при запуске игры"
    },
    {
        "id": "combat",
        "name_en": "Combat & Bosses",
        "name_ru": "Битвы и боссы",
        "name_pl": "Walka i bossowie",
        "name_it": "Combattimenti e boss",
        "name_de": "Kämpfe & Bosse",
        "name_fr": "Combats et boss",
        "name_es": "Combate y jefes",
        "icon": "fa-shield-halved",
        "description_en": "Battle themes and major boss encounters",
        "description_ru": "Музыка сражений с врагами и главными боссами"
    },
    {
        "id": "tavern",
        "name_en": "Taverns & Bards",
        "name_ru": "Таверны и барды",
        "name_pl": "Tawerny i bardowie",
        "name_it": "Taverne e bardi",
        "name_de": "Tavernen & Barden",
        "name_fr": "Tavernes et bardes",
        "name_es": "Tabernas y bardos",
        "icon": "fa-beer-mug-empty",
        "description_en": "Lively tavern tunes and bard performances",
        "description_ru": "Весёлая музыка таверн и песни бардов"
    },
    {
        "id": "town",
        "name_en": "Towns & Settlements",
        "name_ru": "Города и мирные зоны",
        "name_pl": "Miasta i osady",
        "name_it": "Città e insediamenti",
        "name_de": "Städte & Siedlungen",
        "name_fr": "Villes et colonies",
        "name_es": "Ciudades y asentamientos",
        "icon": "fa-landmark",
        "description_en": "Peaceful music for Cyseal, markets, and villages",
        "description_ru": "Сайсил, рынки, Сильверглен и мирные дома"
    },
    {
        "id": "nature",
        "name_en": "Nature & Exploration",
        "name_ru": "Природа и локации",
        "name_pl": "Natura i eksploracja",
        "name_it": "Natura ed esplorazione",
        "name_de": "Natur & Erkundung",
        "name_fr": "Nature et exploration",
        "name_es": "Naturaleza y exploración",
        "icon": "fa-tree",
        "description_en": "Wilderness, beaches, lush forests, and snowy peaks",
        "description_ru": "Пляжи Сайсила, Лес Лукуллы, Хибергейм"
    },
    {
        "id": "dungeon",
        "name_en": "Dungeons & Graveyards",
        "name_ru": "Подземелья и нежить",
        "name_pl": "Lochy i cmentarze",
        "name_it": "Dungeon e cimiteri",
        "name_de": "Dungeons & Gräber",
        "name_fr": "Donjons et cimetières",
        "name_es": "Mazmorras y cementerios",
        "icon": "fa-skull",
        "description_en": "Dark ambient themes for crypts, tombs, and ruins",
        "description_ru": "Склепы, пещеры, Чёрная бухта, гробницы"
    },
    {
        "id": "homestead",
        "name_en": "Homestead & Astral",
        "name_ru": "Обитель и Чертоги",
        "name_pl": "Siedziba i wymiar astralny",
        "name_it": "Dimora e piano astrale",
        "name_de": "Heimstätte & Astral",
        "name_fr": "Demeure et plan astral",
        "name_es": "Morada y plano astral",
        "icon": "fa-sparkles",
        "description_en": "Mystical realms, End of Time, Hall of Heroes",
        "description_ru": "Обитель на краю времени, Зал Героев, создание героя"
    },
    {
        "id": "story",
        "name_en": "Story Moments",
        "name_ru": "Сюжетные моменты",
        "name_pl": "Wydarzenia fabularne",
        "name_it": "Momenti narrativi",
        "name_de": "Handlungsmomente",
        "name_fr": "Moments d'histoire",
        "name_es": "Momentos de la historia",
        "icon": "fa-book-open",
        "description_en": "Narrative cutscenes, companion quests, emotional peaks",
        "description_ru": "Эмоциональные сюжетные сцены спутников и финал"
    },
    {
        "id": "other",
        "name_en": "Miscellaneous",
        "name_ru": "Прочее",
        "name_pl": "Różne",
        "name_it": "Varie",
        "name_de": "Verschiedenes",
        "name_fr": "Divers",
        "name_es": "Varios",
        "icon": "fa-ellipsis",
        "description_en": "Credits and transitional tracks",
        "description_ru": "Титры и переходные сцены"
    }
]

def get_data_path():
    p1 = os.path.join(os.path.dirname(__file__), "tracks_data.json")
    if os.path.exists(p1):
        return p1
    if getattr(sys, 'frozen', False):
        base = getattr(sys, '_MEIPASS', os.path.dirname(sys.executable))
        p2 = os.path.join(base, "core", "tracks_data.json")
        if os.path.exists(p2):
            return p2
        p3 = os.path.join(base, "tracks_data.json")
        if os.path.exists(p3):
            return p3
    return p1

DATA_PATH = get_data_path()

def load_tracks():
    path = get_data_path()
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

TRACKS = load_tracks()

def get_track_by_wid(wid):
    wid_str = str(wid)
    for t in TRACKS:
        if t["wid"] == wid_str:
            return t
    return None

def get_tracks_by_category(category_id):
    return [t for t in TRACKS if t["category"] == category_id]
