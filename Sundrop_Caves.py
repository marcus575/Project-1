# Marcus Mah En Hao, IT01, 10 August 2025

# It is to allow the generation of random numbers
from random import randint

# It is global variables to store the game state
player = {}
game_map = []
fog = []

# It is global constants for map dimensions
MAP_WIDTH = 0
MAP_HEIGHT = 0

TURNS_PER_DAY = 20
WIN_GP = 500

# It is the game data structures
minerals = ['copper', 'silver', 'gold']
mineral_names = {'C': 'copper', 'S': 'silver', 'G': 'gold'}
pickaxe_price = [50, 150]

# It is the prices for each mineral randomised when selling (min, max)
prices = {}
prices['copper'] = (1, 3)
prices['silver'] = (5, 8)
prices['gold'] = (10, 18)

# This function loads a map structure (a nested list) from a file
# It also updates MAP_WIDTH and MAP_HEIGHT
def load_map(filename, map_struct):
    map_file = open(filename, 'r')
    global MAP_WIDTH
    global MAP_HEIGHT
    
    # It is to remove any existing map data
    map_struct.clear()
    
    # It is to load map from file and read all the lines in the file
    # and convert each line into a list of characters
    lines = map_file.readlines()
    for line in lines:
        map_struct.append(list(line.rstrip('\n')))
    
    # It is to set global dimensions based on the loaded map
    if map_struct: # Only if the map has content
        MAP_WIDTH = len(map_struct[0])
        MAP_HEIGHT = len(map_struct)

    # Close the file after reading
    map_file.close()

# This function clears the fog of war at the 3x3 square around the player
def clear_fog(fog, player):
    px, py = player['x'], player['y'] # Getting the player's current coordinates

    # It is to loop through the 3x3 grid centered on the player
    for dy in range(-1, 2):
        for dx in range(-1, 2):
            nx, ny = px + dx, py + dy # Calculating the absolute coordinates

            # It is to check if the coordinates are within the map boundaries
            # If they are, we clear the fog for that cell
            if 0 <= nx < MAP_WIDTH and 0 <= ny < MAP_HEIGHT:
                fog[ny][nx] = False

# This function initializes the game state, including the map, fog, and player
def initialize_game(game_map, fog, player):
    # initialize map
    load_map("Assignment\\level_1.txt", game_map)

    # Initialize fog - all squares start as fogged (True)
    fog.clear()
    for y in range(MAP_HEIGHT):
        fog.append([True] * MAP_WIDTH)
    
    # Initialize player with all the starting values
    player['name'] = input("Greetings, miner! What is your name? ")
    print(f"Pleased to meet you, {player['name']}. Welcome to Sundrop Town!")
    player['x'] = 0
    player['y'] = 0
    player['copper'] = 0
    player['silver'] = 0
    player['gold'] = 0
    player['GP'] = 0
    player['day'] = 1
    player['steps'] = 0
    player['turns'] = TURNS_PER_DAY
    player['pickaxe_level'] = 1
    player['backpack_capacity'] = 10
    player['portal_x'] = 0
    player['portal_y'] = 0

    # Clear the fog around the player
    clear_fog(fog, player)
    
# This function draws the entire map, covered by the fog
def draw_map(game_map, fog, player):
    print()
    print("+------------------------------+")

    # It is to loop through each row and column of the map
    for y in range(MAP_HEIGHT):
        print("|", end="")
        for x in range(MAP_WIDTH):

            # It is to check if the fog is present at the current cell
            if fog[y][x]:
                print("?", end="")
            elif x == player['x'] and y == player['y']:
                if game_map[y][x] == 'T':
                    print("M", end="")  # Miner in town
                else:
                    print("M", end="")

            # It is to check if the player has a portal at this position
            elif x == player['portal_x'] and y == player['portal_y'] and (x != 0 or y != 0):
                print("P", end="")
            else:
                print(game_map[y][x], end="")
        print("|")
    print("+------------------------------+")

# This function draws the 3x3 viewport
def draw_view(game_map, fog, player):
    print(f"DAY {player['day']}")
    print("+---+")

    # It is to get the player's current position
    px, py = player['x'], player['y']

    # It is to loop through the 3x3 grid centered on the player
    for dy in range(-1, 2):
        print("|", end="")
        for dx in range(-1, 2):
            nx, ny = px + dx, py + dy # Calculating the absolute coordinates

            # It is to check if the coordinates are within the map boundaries
            if 0 <= nx < MAP_WIDTH and 0 <= ny < MAP_HEIGHT:
                if dx == 0 and dy == 0:
                    print("M", end="")
                else:
                    print(game_map[ny][nx], end="") # Showing the map content
            else:
                print("#", end="")  # Wall
        print("|")
    print("+---+")

# This function shows the information for the player
def show_information(player):
    print()
    print("----- Player Information -----")
    print(f"Name: {player['name']}")

    # It is to show current position if in mine, otherwise show portal position if in town
    if 'current_position' in player:
        print(f"Current position: ({player['x']}, {player['y']})")
    else:
        print(f"Portal position: ({player['portal_x']}, {player['portal_y']})")
    
    # It is to show the pickaxe level and type
    pickaxe_types = {1: "copper", 2: "silver", 3: "gold"}
    print(f"Pickaxe level: {player['pickaxe_level']} ({pickaxe_types[player['pickaxe_level']]})")
    
    # It is to show the backpack capacity
    if player['gold'] > 0 or player['silver'] > 0 or player['copper'] > 0:
        if player['gold'] > 0:
            print(f"Gold: {player['gold']}")
        if player['silver'] > 0:
            print(f"Silver: {player['silver']}")
        if player['copper'] > 0:
            print(f"Copper: {player['copper']}")
    print("------------------------------")

    # It is to show the player's current load
    load = player['copper'] + player['silver'] + player['gold']
    print(f"Load: {load} / {player['backpack_capacity']}")
    print("------------------------------")
    print(f"GP: {player['GP']}")
    print(f"Steps taken: {player['steps']}")
    print("------------------------------")

# This function saves the game
def save_game(game_map, fog, player):
    try:
        with open("savegame.txt", "w") as f:
            # Save player data
            for key, value in player.items():
                f.write(f"{key}:{value}\n")
            f.write("MAP:\n")
            # Save map
            for row in game_map:
                f.write(''.join(row) + "\n") # Convert list to string
            f.write("FOG:\n")
            # Save fog
            for row in fog:
                f.write(''.join(['1' if cell else '0' for cell in row]) + "\n")
        print("Game saved.")
    except:
        print("Error saving game.")
        
# This function loads the game
def load_game(game_map, fog, player):
    try:
        with open("savegame.txt", "r") as f:
            lines = f.readlines()
            i = 0

            # Load player data
            # It is to loop through the lines until we find the "MAP:" line
            while i < len(lines) and not lines[i].startswith("MAP:"):
                line = lines[i].strip()

                # It is to split the line into key-value pairs
                # Split only on the first colon
                if ':' in line:
                    key, value = line.split(':', 1)

                    # It is to convert numeric values to integers if not keep as string
                    if key in ['x', 'y', 'copper', 'silver', 'gold', 'GP', 'day', 'steps', 'turns', 'pickaxe_level', 'backpack_capacity', 'portal_x', 'portal_y']:
                        player[key] = int(value)
                    else:
                        player[key] = value
                i += 1
            
            i += 1  # Skip "MAP": line
            game_map.clear()
            # Load map
            # It is to loop through the lines until we find the "FOG:" line
            while i < len(lines) and not lines[i].startswith("FOG:"):
                game_map.append(list(lines[i].rstrip('\n'))) # Convert string to list of characters
                i += 1
            
            i += 1  # Skip "FOG:" line
            fog.clear()
            # Load fog
            while i < len(lines):
                fog_row = []
                for char in lines[i].strip():
                    fog_row.append(char == '1') # Convert '1' to True and '0' to False
                fog.append(fog_row)
                i += 1
            
            # It is to update global dimensions based on the loaded map
            global MAP_WIDTH, MAP_HEIGHT

            # Only if the map was loaded successfully
            if game_map:
                MAP_WIDTH = len(game_map[0])
                MAP_HEIGHT = len(game_map)
            
        return True
    except:
        print("Error loading game or no save file found.")
        return False

# This function is to show the main menu options
def show_main_menu():
    print()
    print("--- Main Menu ----")
    print("(N)ew game")
    print("(L)oad saved game")
    print("(Q)uit")
    print("------------------")

# This function is to show the town menu options with the current day
def show_town_menu(player):
    print()
    print(f"DAY {player['day']}", end="\n")
    print("----- Sundrop Town -----")
    print("(B)uy stuff")
    print("See Player (I)nformation")
    print("See Mine (M)ap")
    print("(E)nter mine")
    print("Sa(V)e game")
    print("(Q)uit to main menu")
    print("------------------------")

# This function is to sell the ore collected by the player automatically
def sell_ore(player):
    total_gp = 0 # It is to keep track of total GP earned

    # It is to sell the copper ores is the player has any
    if player['copper'] > 0:
        price_per_ore = randint(prices['copper'][0], prices['copper'][1])
        copper_gp = player['copper'] * price_per_ore
        total_gp += copper_gp
        print(f"You sell {player['copper']} copper ore for {copper_gp} GP.")
        player['copper'] = 0
    
    # It is to sell the silver ores if the player has any
    if player['silver'] > 0:
        price_per_ore = randint(prices['silver'][0], prices['silver'][1])
        silver_gp = player['silver'] * price_per_ore
        total_gp += silver_gp
        print(f"You sell {player['silver']} silver ore for {silver_gp} GP.")
        player['silver'] = 0
    
    # It is to sell the gold ores if the player has any
    if player['gold'] > 0:
        price_per_ore = randint(prices['gold'][0], prices['gold'][1])
        gold_gp = player['gold'] * price_per_ore
        total_gp += gold_gp
        print(f"You sell {player['gold']} gold ore for {gold_gp} GP.")
        player['gold'] = 0
    
    # It is to add the total GP earned to the player's GP
    if total_gp > 0:
        player['GP'] += total_gp
        print(f"You now have {player['GP']} GP!")

# This function is to show the shop menu options with available upgrades and their costs
def show_shop_menu(player):
    print()
    print("----------------------- Shop Menu -------------------------")
    
    # Show pickaxe upgrade option
    if player['pickaxe_level'] < 3:
        next_level = player['pickaxe_level'] + 1
        upgrade_cost = pickaxe_price[player['pickaxe_level'] - 1]
        mineral_type = {2: "silver", 3: "gold"}[next_level]
        print(f"(P)ickaxe upgrade to Level {next_level} to mine {mineral_type} ore for {upgrade_cost} GP")
    
    # Show backpack upgrade option
    upgrade_cost = player['backpack_capacity'] * 2
    new_capacity = player['backpack_capacity'] + 2
    print(f"(B)ackpack upgrade to carry {new_capacity} items for {upgrade_cost} GP")
    
    print("(L)eave shop")
    print("-----------------------------------------------------------")
    print(f"GP: {player['GP']}")
    print("-----------------------------------------------------------")

# This function checks if the player can mine a mineral based on their pickaxe level
# It returns True if the player can mine the mineral, otherwise False
def can_mine_mineral(mineral_char, pickaxe_level):
    mineral_requirements = {'C': 1, 'S': 2, 'G': 3}
    return pickaxe_level >= mineral_requirements.get(mineral_char, 1)

# This function mines a mineral and returns the amount mined
def mine_mineral(mineral_char):
    mineral_amounts = {
        'C': (1, 5),  # copper: 1-5 pieces
        'S': (1, 3),  # silver: 1-3 pieces
        'G': (1, 2)   # gold: 1-2 pieces
    }
    return randint(*mineral_amounts[mineral_char])

# This function calculates the total items currently in the player's inventory
def get_current_load(player):
    return player['copper'] + player['silver'] + player['gold']

# This function moves the player in the specified direction
# It returns True if the move was successful, False if blocked or invalid
def move_player(game_map, fog, player, direction):
    moves = {'w': (0, -1), 'a': (-1, 0), 's': (0, 1), 'd': (1, 0)}
    if direction not in moves:
        return False
    
    # Get the new coordinates based on the direction
    dx, dy = moves[direction]
    new_x, new_y = player['x'] + dx, player['y'] + dy # It calculates the new position
    
    # Check if the new boundries are within the map
    # If not, return False to indicate the move is blocked
    if not (0 <= new_x < MAP_WIDTH and 0 <= new_y < MAP_HEIGHT):
        print("You can't go that way!")
        return False
    
    # Check if the player is stepping on anything
    target_cell = game_map[new_y][new_x]
    current_load = get_current_load(player)
    
    # If the target cell is a wall or blocked, return False
    if target_cell in ['C', 'S', 'G']:
        # Check if backpack is full
        if current_load >= player['backpack_capacity']:
            print("You can't carry any more, so you can't go that way.")
            return False
        
        # Check if the pickaxe can mine this mineral
        if not can_mine_mineral(target_cell, player['pickaxe_level']):
            print("You can't mine that with your current pickaxe!")
            return False
    
    # Update the player's position and clear the fog around the player
    player['x'] = new_x
    player['y'] = new_y
    clear_fog(fog, player)
    
    # Handle mining if the player stepped on a mineral
    # If the target cell is a mineral, mine it
    if target_cell in ['C', 'S', 'G']:
        pieces_mined = mine_mineral(target_cell)
        mineral_name = mineral_names[target_cell]
        
        # Calculate how many pieces can actually be carried
        space_left = player['backpack_capacity'] - current_load
        pieces_taken = min(pieces_mined, space_left) # It limits the pieces taken to the available space
        
        print("---------------------------------------------------")
        print(f"You mined {pieces_mined} piece(s) of {mineral_name}.")
        
        # If the player can only carry a limited amount, inform them
        if pieces_taken < pieces_mined:
            print(f"...but you can only carry {pieces_taken} more piece(s)!")
        
        # Update the player's inventory
        player[mineral_name] += pieces_taken
        
        # Remove the mineral from the map
        game_map[new_y][new_x] = ' '
    
    # Check if the player returned to town
    if target_cell == 'T':
        return 'town'
    
    return True

#--------------------------- MAIN GAME ---------------------------
# This function is the main game loop
# It handles the game state and user input
def main():
    game_state = 'main'
    print("---------------- Welcome to Sundrop Caves! ----------------")
    print("You spent all your money to get the deed to a mine, a small")
    print("  backpack, a simple pickaxe and a magical portal stone.")
    print()
    print("How quickly can you get the 500 GP you need to retire")
    print("  and live happily ever after?")
    print("-----------------------------------------------------------")

    # Main game loop, which will run until the player chooses to quit
    while True:
        if game_state == 'main':
            show_main_menu()
            choice = input("Your choice? ").lower()
            
            if choice == 'n': # Start a new game
                initialize_game(game_map, fog, player)
                game_state = 'town'
            elif choice == 'l': # Load a saved game
                if load_game(game_map, fog, player):
                    game_state = 'town'
            elif choice == 'q': # Quit the game
                break
        
        # This is the town state where the player can buy items, see information, or enter the mine
        elif game_state == 'town':
            # Auto-sell ore when returning to town
            if get_current_load(player) > 0:
                sell_ore(player)
                # This is to check if the player has won the game
                if player['GP'] >= WIN_GP:
                    print("-------------------------------------------------------------")
                    print(f"Woo-hoo! Well done, {player['name']}, you have {player['GP']} GP!")
                    print("You now have enough to retire and play video games every day.")
                    print(f"And it only took you {player['day']} days and {player['steps']} steps! You win!")
                    print("-------------------------------------------------------------")
                    game_state = 'main' # Return to main menu after winning
                    continue
            
            # Show the town menu options
            show_town_menu(player)
            choice = input("Your choice? ").lower()
            
            if choice == 'b':
                game_state = 'shop'
            elif choice == 'i':
                show_information(player)
            elif choice == 'm':
                draw_map(game_map, fog, player)
            elif choice == 'e':

                # This is to teleport the player to the portal location and reset turns
                player['x'] = player['portal_x']
                player['y'] = player['portal_y']
                player['turns'] = TURNS_PER_DAY
                clear_fog(fog, player)
                game_state = 'mine'
            elif choice == 'v':
                save_game(game_map, fog, player)
            elif choice == 'q':
                game_state = 'main'
        
        # Shop state
        elif game_state == 'shop':
            show_shop_menu(player) # Show the shop menu options
            choice = input("Your choice? ").lower()
            
            # Pickaxe upgrades
            if choice == 'p' and player['pickaxe_level'] < 3:
                upgrade_cost = pickaxe_price[player['pickaxe_level'] - 1]
                if player['GP'] >= upgrade_cost:
                    player['GP'] -= upgrade_cost
                    player['pickaxe_level'] += 1
                    mineral_type = {2: "silver", 3: "gold"}[player['pickaxe_level']]
                    print(f"Congratulations! You can now mine {mineral_type}!")
                else:
                    print("You don't have enough GP!")
            
            # Backpack upgrades
            elif choice == 'b':
                upgrade_cost = player['backpack_capacity'] * 2
                if player['GP'] >= upgrade_cost:
                    player['GP'] -= upgrade_cost
                    player['backpack_capacity'] += 2
                    print(f"Congratulations! You can now carry {player['backpack_capacity']} items!")
                else:
                    print("You don't have enough GP!")
            elif choice == 'l':
                game_state = 'town'
        
        # Mine state
        elif game_state == 'mine':
            print("---------------------------------------------------")
            print(f"                       DAY {player['day']}                         ")
            print("---------------------------------------------------")
            
            draw_view(game_map, fog, player)
            
            # It is to show the current turns left, load, and steps
            current_load = get_current_load(player)
            print(f"Turns left: {player['turns']}    Load: {current_load} / {player['backpack_capacity']}    Steps: {player['steps']}")
            print("(WASD) to move")
            print("(M)ap, (I)nformation, (P)ortal, (Q)uit to main menu")
            
            choice = input("Action? ").lower()
            
            # Handle player movement and actions
            if choice in ['w', 'a', 's', 'd']:
                result = move_player(game_map, fog, player, choice)
                player['steps'] += 1
                player['turns'] -= 1
                
                # Check if the player returned to town
                if result == 'town':
                    game_state = 'town'
                    player['day'] += 1
                    continue
                
                # Check if the player ran out of turns
                if player['turns'] <= 0:
                    print("You are exhausted.")
                    print("You place your portal stone here and zap back to town.")

                    # It is to save the current position of the player as the new portal location
                    player['portal_x'] = player['x']
                    player['portal_y'] = player['y']
                    player['day'] += 1
                    game_state = 'town'
                    
            # Handle non-movement actions
            elif choice == 'm':
                draw_map(game_map, fog, player)
            elif choice == 'i':
                player['current_position'] = True
                show_information(player)
                del player['current_position']
            elif choice == 'p':
                print("------------------------------------------------------")
                print("You place your portal stone here and zap back to town.")

                # It is to save the current position of the player as the new portal location
                player['portal_x'] = player['x']
                player['portal_y'] = player['y']
                player['day'] += 1
                game_state = 'town'
            elif choice == 'q':
                game_state = 'main'

# Only run the main function if this script is executed directly
if __name__ == "__main__":
    main()
