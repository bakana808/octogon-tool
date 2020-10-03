"""
Lookup Map for Smash.gg IDs
"""


def get_portrait_url(character_name: str = None, color: int = 0) -> str:
    if character_name:
        return f"/assets/portraits/{character_name}/Default.png"
    else:
        return "/assets/portraits/Random CPU.png"


characters = {
    1: "Bowser",
    2: "Captain Falcon",
    3: "Donkey Kong",
    4: "Dr Mario",
    5: "Falco",
    6: "Fox",
    7: "Ganondorf",
    8: "Ice Climbers",
    9: "Jigglypuff",
    10: "Kirby",
    11: "Link",
    12: "Luigi",
    13: "Mario",
    14: "Marth",
    15: "Mewtwo",
    16: "Mr Game & watch",
    17: "Ness",
    18: "Peach",
    19: "Pichu",
    20: "Pikachu",
    21: "Roy",
    22: "Samus",
    23: "Sheik",
    24: "Yoshi",
    25: "Young Link",
    26: "Zelda",
    628: "Zelda/Sheik",
    1744: "Random",
}
