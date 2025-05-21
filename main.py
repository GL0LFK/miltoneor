import os, random
from tabulate import tabulate

run = True
menu = True
play = False
rules = False
key = False
fight = False
standing = True
buy = False
speak = False
boss = False

HP = 500
HPMAX = HP
ATK = 3
pot = 1     # potions +30HP
elix = 0    # elixirs +50HP
gold = 0
x = 0
y = 0

        #  x = 0     x = 1       x = 2         x = 3    x = 4       x = 5          x = 6
map = [["plains",  "plains",   "plains",   "plains",  "forest", "mountain",       "cave"],  # y = 0
       ["forest",  "forest",   "forest",   "forest",  "forest",    "hills",   "mountain"],  # y = 1
       ["forest",  "fields",   "bridge",   "plains",   "hills",   "forest",      "hills"],  # y = 2
       ["plains",    "shop",     "town",    "mayor",  "plains",    "hills",   "mountain"],  # y = 3
       ["plains",  "fields",   "fields",   "plains",   "hills", "mountain",   "mountain"]]  # y = 4

y_len = len(map)-1
x_len = len(map[0])-1

biom = {
    "plains": {
        "t": "PLAINS",
        "e": True},
    "forest": {
        "t": "WOODS",
        "e": True},
    "fields": {
        "t": "FIELDS",
        "e": False},
    "bridge": {
        "t": "BRIDGE",
        "e": True},
    "town": {
        "t": "TOWN CENTRE",
        "e": False},
    "shop": {
        "t": "SHOP",
        "e": False},
    "mayor": {
        "t": "MAYOR",
        "e": False},
    "cave": {
        "t": "CAVE",
        "e": False},
    "mountain": {
        "t": "MOUNTAIN",
        "e": True},
    "hills": {
        "t": "HILLS",
        "e": True,
    }
}

class RGBColorPrint:
    RESET = '\033[0m'

    def __getattr__(self, name):
        if name.startswith('colorprint_'):
            color_name = name[len('colorprint_'):].lower()
            colors = {
                'red': (255, 0, 0),
                'green': (0, 255, 0),
                'blue': (0, 0, 255),
                'yellow': (255, 255, 0),
                'cyan': (0, 255, 255),
                'magenta': (255, 0, 255),
                'white': (255, 255, 255),
                'black': (0, 0, 0),
                'orange': (255, 165, 0),
                'truegold': (255, 215, 0),
                'silver': (192, 192, 192),
                'purple': (128, 0, 128),
                'pink': (255, 105, 180),
                'ancientyellow': (238, 207, 69),
                'arcaneviolet': (123, 104, 238),
                'mysticblue': (72, 209, 204),
                'infernored': (255, 69, 0),
                'eldritchgreen': (85, 107, 47),
                'shadowblack': (36, 36, 36),
                'celestialwhite': (245, 245, 255),
                'faeriepink': (255, 182, 193),
                'dwarvenbronze': (205, 127, 50),
                'royalblue': (65, 105, 225),
                'emberorange': (255, 140, 0),
                'forestgreen': (34, 139, 34),
            }
            rgb = colors.get(color_name, (255, 255, 255))  # default white
            def printer(*args, sep=' ', end='\n'):
                r, g, b = rgb
                text = sep.join(str(arg) for arg in args) + end
                print(f"\033[38;2;{r};{g};{b}m{text}{self.RESET}", end='')
            return printer
        raise AttributeError(f"No such method: {name}")


# Creating the color printer
cp = RGBColorPrint()

e_list = ["Goblin", "Orc", "Slime"] # we need a list because random.choice does not work with sets

mobs = {
    "Goblin": {
        "hp": 15,
        "at": 3,
        "go": 8
    },
    "Orc": {
        "hp": 35,
        "at": 5,
        "go": 18
    },
    "Slime": {
        "hp": 30,
        "at": 2,
        "go": 12
    },
    "Dragon": {
        "hp": 100,
        "at": 8,
        "go": 100
    }
}

def clear():
    os.system("cls")

def draw():
    print("xX--------------------Xx")

def save():
    list = [
        name,
        str(HP),
        str(ATK),
        str(pot),
        str(elix),
        str(gold),
        str(x),
        str(y),
        str(key)
    ]

    f = open("load.txt", "w")

    for item in list:
        f.write(item + "\n")
    f.close()

def showmap():
    global map, play, biom, x, y, x_len, y_len

    # 1. Copy the map and highlight the player's position
    display_map = []
    for y_index in range(y_len + 1):
        row = []
        for x_index in range(x_len + 1):
            field = map[y_index][x_index]
            if y_index == y and x_index == x:
                # Highlight the player's position
                row.append(f"\033[1;32m{field}\033[0m")
            else:
                row.append(field)
        display_map.append(row)

    cp.colorprint_ancientyellow("LOCATION: " + biom[map[y][x]]["t"])
    print(tabulate(display_map, tablefmt="fancy_grid", stralign="center"))

def color_health_bar(current_health, max_health, bar_length=20):
    health_ratio = max(0, current_health) / max_health
    filled_length = int(bar_length * health_ratio)
    percent = int(health_ratio * 100)
    # Color logic: green > 66%, yellow > 33%, else red
    if percent > 66:
        color = "\033[92m"  # Green
    elif percent > 33:
        color = "\033[93m"  # Yellow
    else:
        color = "\033[91m"  # Red
    bar = color + '█' * filled_length + '-' * (bar_length - filled_length) + "\033[0m"
    # return f"[{bar}] {percent}%"
    return f"[{bar}]"


def heal(amount):
    global HP
    if HP + amount < HPMAX:
        HP += amount
    else:
        HP = HPMAX
    cp.colorprint_dwarvenbronze("You healed +" + str(amount) + ".")

def battle():
    global fight, play, run, HP, pot, elix, gold, boss # we will change global variables so we call these in to the function

    if not boss:
        enemy = random.choice(e_list)
    else:
        enemy = "Dragon"

    hp = mobs[enemy]["hp"]
    hpmax = hp
    atk = mobs[enemy]["at"]
    g = mobs[enemy]["go"]

    while fight:
        clear()
        draw()
        cp.colorprint_infernored("Defeat the " + enemy + "!")
        draw()
        cp.colorprint_celestialwhite(enemy, end="")
        print(f"HP: {color_health_bar(hp, hpmax)} {hp}/{hpmax}")
        cp.colorprint_celestialwhite(name, end="")
        print(f"HP: {color_health_bar(HP, HPMAX)} {HP}/{HPMAX}")
        cp.colorprint_celestialwhite("POTIONS ", end="")
        cp.colorprint_emberorange(pot)
        cp.colorprint_celestialwhite("ELIXIRS ", end="")
        cp.colorprint_faeriepink(elix)
        draw()
        print("1 - ATTACK")
        if pot > 0:
            print("2 - USE POTION (30HP)")
        if elix > 0:
            print("3 - USE ELIXIR (50HP)")
        draw()

        choice = input("# ")

        if choice == "1":
            hp -= ATK
            print(name + " dealt " + str(ATK) + " damage to the " + enemy + ".")
            if hp > 0:
                HP -= atk
                print(enemy + " dealt " + str(atk) + " damage to the " + name + ".")
            input("> ")
        elif choice == "2":
            if pot >= 0:
                pot -= 1
                heal(30)
                HP -= atk
                print(enemy + " dealt " + str(atk) + " damage to the " + name + ".")
            else:
                print("No potions!")
            input("> ")
        elif choice == "3":
            if elix >= 0:
                elix -= 1
                heal(50)
                HP -= atk
                print(enemy + " dealt " + str(atk) + " damage to the " + name + ".")
            else:
                print("No elixirs!")
            input("> ")

        if HP <= 0:
            print(enemy + " has defeated " + name + "...")
            draw()
            fight = False
            play = False
            run = False
            print("GAME OVER")
            input("> ")

        if hp <= 0:
            print(name + " has killed the " + enemy + "!")
            draw()
            fight = False
            gold += g
            print("LOOT: " + str(g) + " gold")
            if random.randint(0, 100) < 75:
                print("LOOT: 1 potion" )
                pot += 1
            if random.randint(0, 100) < 30:
                print("LOOT: 1 elixir")
                elix += 1
            if enemy == "Dragon":
                draw()
                print("Congratulations, you've finished the game!")
                boss = False
                play = False
                run = False
            input("> ")
            clear()

def shop():
    global buy, gold, ATK, pot, elix  # we will change global variables so we call these in to the function

    while buy:
        clear()
        draw()
        print("Welcome to the shop!")
        draw()
        print("GOLD: " + str(gold))
        print("POTIONS: " + str(pot))
        print("ELIXIRS: " + str(elix))
        print("ATK: " + str(ATK))
        draw()
        print("1 - BUY POTION (30HP) - 5 GOLD")
        print("2 - BUY ELIXIR (MAXHP) - 8 GOLD")
        print("3 - UPGRADE WEAPON (+2ATK) - 10 GOLD")
        print("4 - LEAVE")
        draw()

        choice = input("# ")

        if choice == "1":
            if gold >= 5:
                gold -= 5
                pot += 1
                print("1 potion added.")
            else:
                print("Not enough gold.")
            input("> ")
        if choice == "2":
            if gold >= 8:
                gold -= 8
                elix += 1
                print("1 elixir added.")
            else:
                print("Not enough gold.")
            input("> ")
        if choice == "3":
            if gold >= 10:
                gold -= 10
                oldATK = ATK
                ATK += 2
                print("Weapon improved: " + str(oldATK) + " -> " + str(ATK))
            else:
                print("Not enough gold.")
            input("> ")
        if choice == "4":
            buy = False

def mayor():
    global speak, key

    while speak:
        clear()
        draw()
        print("Hello there: " + name + "!")
        if ATK < 10:
            print("You are not strong enough, to face the dragon yet! Keep practicing and come back later!")
            key = False
        else:
            print("You are ready to take it to the dragon! Take this key but be careful with the beast! Many od you have failed before...")
            key = True

        draw()
        print("1 - LEAVE")
        draw()

        choice = input("# ")

        if choice == "1":
            speak = False

def cave():
    global boss, key, fight

    while boss:
        clear()
        draw()
        print("Hear lies the cave of the dragon, what will you do?")
        draw()
        if key:
            print("1 - USE KEY")
        print("2 - TURN BACK")
        draw()

        choice = input("# ")

        if choice == "1":
            if key:
                fight = True
                battle()
        elif choice == "2":
            boss = False

while run:
    while menu:
        clear()
        draw()

        cp.colorprint_ancientyellow("1. NEW GAME")
        cp.colorprint_ancientyellow("2. LOAD GAME")
        cp.colorprint_ancientyellow("3. RULES")
        cp.colorprint_dwarvenbronze("4. QUIT GAME")

        if rules:
            print("Here will be the rules displayed.")
            rules = False
            choice = ""
            input("> ") # empty input
        else:
            choice = input("# ")  # empty input

        if choice == "1":
            clear()
            draw()
            name = input("What's your name, adventurer? ")
            menu = False    # We get out of the menu loop
            play = True     # We switch to the play loop
        elif choice == "2":
            try:
                f = open("load.txt", "r")
                load_list = f.readlines()
                if len(load_list) == 9:
                    name = load_list[0][:-1]
                    HP = int(load_list[1][:-1])
                    ATK = int(load_list[2][:-1])
                    pot = int(load_list[3][:-1])
                    elix = int(load_list[4][:-1])
                    gold = int(load_list[5][:-1])
                    x = int(load_list[6][:-1])
                    y = int(load_list[7][:-1])
                    key = bool(load_list[8][:-1])
                    clear()
                    print("Welcome back, " + name + "!")
                    input("> ")  # waiting for an input
                    menu = False    # We get out of the menu loop
                    play = True     # We switch to the play loop
                else:
                    cp.colorprint_infernored("Your saved game is broken, cannot be loaded")
                    input("> ")  # waiting for an input
            except OSError:
                cp.colorprint_infernored("We could find your saved game")
                input("> ")  # waiting for an input
        elif choice == "3":
            clear()
            rules = True
        elif choice == "4":
            quit()

    while play:
        save() # auto save
        clear()

        if not standing:
            if biom[map[y][x]]["e"]:
                if random.randint(0, 100) < 30:
                    fight = True
                    battle()
        if play:
            showmap()
            draw()
            cp.colorprint_celestialwhite("NAME: ", end="")
            cp.colorprint_dwarvenbronze(name)

            cp.colorprint_celestialwhite("HP: ", end="")
            cp.colorprint_infernored(f"{HP}/{HPMAX}")

            cp.colorprint_celestialwhite("ATK ", end="")
            cp.colorprint_ancientyellow(ATK)

            cp.colorprint_celestialwhite("POTIONS ", end="")
            cp.colorprint_emberorange(pot)

            cp.colorprint_celestialwhite("ELIXIRS ", end="")
            cp.colorprint_faeriepink(elix)

            cp.colorprint_celestialwhite("GOLD ", end="")
            cp.colorprint_truegold(gold)

            draw()
            cp.colorprint_dwarvenbronze("0 - SAVE AND QUIT")
            if y > 0:
                cp.colorprint_mysticblue("w - NORTH ↑ ")
            if x < x_len:
                cp.colorprint_mysticblue("d - EAST → ")
            if y < y_len:
                cp.colorprint_mysticblue("s - SOUTH ↓ ")
            if x > 0:
                cp.colorprint_mysticblue("a - WEST ← ")
            if pot > 0:
                cp.colorprint_infernored("5 - USE POTION (30HP)")
            if elix > 0:
                cp.colorprint_pink("5 - USE ELIXIR (50HP)")
            if map[y][x] == "shop" or map[y][x] == "mayor" or map[y][x] == "cave":
                cp.colorprint_forestgreen("7 - ENTER")
            draw()

            dest = input("# ")

            if dest == "0":
                play = False
                menu = True
                save()
            elif dest == "w":
                if y > 0:
                    y -= 1
                    standing = False
            elif dest == "d":
                if x < x_len:
                    x += 1
                    standing = False
            elif dest == "s":
                if y < y_len:
                    y += 1
                    standing = False
            elif dest == "a":
                if x > 0:
                    x -= 1
                    standing = False
            elif dest == "5":
                if pot > 0:
                    pot -= 1
                    heal(30)
                else:
                    cp.colorprint_eldritchgreen("No potions!")
                input("> ")
                standing = True
            elif dest == "6":
                if elix > 0:
                    elix -= 1
                    heal(50)
                else:
                    cp.colorprint_eldritchgreen("No elixirs!")
                input("> ")
                standing = True
            elif dest == "7":
                if map[y][x] == "shop":
                    buy = True
                    shop()
                elif map[y][x] == "mayor":
                    speak = True
                    mayor()
                elif map[y][x] == "cave":
                    boss = True
                    cave()
            else:
                standing = True
