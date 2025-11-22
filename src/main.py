import random
from colorama import Fore, Style, init
init(autoreset=True)

class Tile:
    def __init__(self, suit, value):

        '''
        
        Creates the tile Class

        suit: 'c'(characters), 'l'(lotus), 'b'(bamboo)
        honors: 'E'(East), 'S'(South), 'W'(West), 'N'(North), 'WH'(White Dragon), 'R'(Red Dragon), 'G'(Green Dragon)

        '''


        self.suit = suit 
        self.value = value

    def __repr__(self):
        
        '''
        
        Returns a value of the title. If it is an honor tile, it will return the honor it is. Otherwise, it will return it's value and suit

        '''

        if self.suit == 'honor':
            return self.value
        else:
            return f"{self.value}{self.suit}"
    
    def is_honor(self):
        return self.suit == 'honor'
    
    
class Player:
    def __init__(self, name, hand):

        '''
        
        Creates the tile Player

        name: The name of the player is the seat they are in. i.e East, South, West, North.
        hand: The player hand organized.

        '''
        self.name = name
        self.hand = hand

    def show_hand(self):
        '''
        
        Returns the player's hand

        '''
        return self.hand
    
    def show_seat(self):
        '''
        
        Returns the player's seat or name
        
        '''
        
              
def create_set():
    '''
    Creates the 4 of each tile and returns the board in order
    '''

    tiles = []

    for suits in ('c', 'l', 'b'): #Creates each suit four times and adds them to the table
        for value in range(1, 10):
            tiles.extend([Tile(suits, value) for amount in range(4)])

    for honors in ('E', 'S', 'W', 'N', 'WH', 'G', 'R'): #Creates each honor tiles four times and adds them to the table
        tiles.extend([Tile('honor', honors) for amount in range(4)])
    return tiles

def shuffle_tiles(tiles):
        
        '''

        Shuffles the tiles
        
        '''

        random.shuffle(tiles)


def distribute_tiles(board, dice):


    '''
    
    Sets up the walls as well as distributes all of the player's hands
    Takes in the tiles and a dice roll to indicate which wall is the starting point as well as the deadwall

    tiles: The full board
    dice: a randomized number from 2-12 to represent dice rolls to indicate the deadwall

    Returns 5 Arrays, Gives each players the hand as well as the new array.
    
    '''

    start_index = (dice * 2) % len(board)
    board = board[start_index:] + board[:start_index]

    dead_wall = board[-14:]
    live_wall = board[:-14]
    #Uses hash to make for simplier coding
    hands = {p: [] for p in ('E', 'S', 'W', 'N')}

    #Simplified to just calculate the starting indexes
    for i in range(3):
        for p in hands:
            hands[p].extend([live_wall.pop(0) for _ in range(4)])

    for p in hands:
        hands[p].append(live_wall.pop(0))
        organize_hand(hands[p])

    return hands['E'], hands['S'], hands['W'], hands['N'], live_wall, dead_wall

def organize_hand(hand):
    '''
     
     Organizes a player's hand from lotus, characters, bamboo, winds, then dragons
     For Winds, the order should be East, South, West, North
     For dragons, the order should be Red, Green, White
     Uses Recurrsion and keysort

     hand: A player's head. Expected values are an array of tiles with a size from 1 to 13

     Returns a player hand in the predetermined order. Should be the same size as inserted

    '''

    #Suit Priority
    suit_order = {'l':0, 'c':1, 'b':2, 'honor':3}

    #Honor Priority
    honor_order = {'E':0, 'S':1, 'W':2, 'N':3, 'R':4, 'G':5, 'WH':6}

    #Using the Suit/Honor priority, this should set up the tiles in a (key, key) function organize the hand
    def sort_key(tile):

        if tile.suit != 'honor':
            return (suit_order[tile.suit], [tile.value])
        else:
            return (suit_order['honor'], [tile.value])
        
    hand.sort(key = sort_key)

def draw_tile(board, hand):


    '''
    
    Removes the first tile from the board, then adds it to the hand

    Inputs: Board of the game, Player's hand

    return None

    '''

    new_tile = board.pop(0)
    hand.append(new_tile)

    organize_hand(hand)

def discard_tile(hand, tile):
    
    '''
    
    Removes a tile from players hand

    hand: Players hand
    tile: Tile to discard

    Returns the discarded tile for discard pile 

    '''

    tile_to_discard = next(
        (
            t for t in hand
            if (t.suit == 'honor' and t.value == tile)
            or (f"{t.value}{t.suit}" == tile)
        ),
        None
    )

    if tile_to_discard:
        hand.remove(tile_to_discard)

    return tile_to_discard


def temp_discard_tile(hand, index):
    
    '''

    DELETE LATER
    
    A temporary function that will only ask for index to remove

    hand:Players hand
    tile: index for tile to discard

    Returns the discarded tile for discard pile 

    '''

    tile_to_discard = hand.pop(index)

    return tile_to_discard


#Note: Sequences that are 4 or 5 will highlight all of the tiles. i.e, 1c, 2c, 3c, 4c, 5c will have all 5 highlighted. Helps the player know that they have possibly two sequences
def find_Sequence_or_Triplets(hand):
    '''
    
    Finds all of the triplets and sequences and color coat it for clarity
    If neither, return normal. Turns the hand to colors respecting if it is a sequence or triplets

    hand: Player's hand

    Return: none

    '''

    labels = {tile: None for tile in hand}

    #Checks for Triplets
    counted = {}
    for tile in hand:
        key = (tile.suit, tile.value)
        counted[key] = counted.get(key, 0) + 1
    for tile in hand:
        if counted.get((tile.suit, tile.value), 0) == 4:
            labels[tile] = "Kan"
        elif counted.get((tile.suit, tile.value), 0) == 3:
            labels[tile] = "Triplet"
        
    #Check for sequences 
    suits = {'c': [], 'l': [], 'b': []}
    for tile in hand:
        if tile.suit in suits:
            suits[tile.suit].append(tile)
    for suits, tiles in suits.items():
        tiles.sort(key = lambda t : t.value)
        values = [t.value for t in tiles]

        # detect every 3-tile consecutive sequence
        for i in range(len(values) - 2):
            a, b, c = values[i:i+3]
            if b == a + 1 and c == b + 1:
                used = {a, b, c}
                for t in tiles:
                    if t.value in used:
                        # don't overwrite triplets or kans
                        if labels[t] not in ("Triplet", "Kan"):
                            labels[t] = "Sequence"
        
    return labels

def change_hand_with_color(hand):
    labels = find_Sequence_or_Triplets(hand)
    output = []

    for tile in hand:
        tag = labels[tile]
        color = {
            "Triplet": Fore.GREEN,
            "Kan": Fore.RED,
            "Sequence": Fore.BLUE
        }.get(tag, Fore.WHITE)

        output.append(f"{color}{tile}{Style.RESET_ALL}")
    return output

#Fixes change_hand_with_color
def display_hand(hand):
    """
    Displays the player's hand in color without changing the actual hand objects.
    """
    colored_hand = change_hand_with_color(hand)
    print(" ".join(colored_hand), end = "\n\n")
    
#TODO pitch correctly
def play_game(players, board):

    #Helps the count for the player's turn
    turn = 0  

    #Draw pitch test
    while board:
        current_player = players[turn % 4]
        if (turn % 4) == 0:
            print(f"Turn: {turn}")

        draw_tile(board, current_player.hand)
        discard = random.choice(current_player.hand)
        current_player.hand.remove(discard)
        discard_pile.append(random.choice(current_player.hand))
        display_hand(current_player.hand)
    
        
        turn += 1  # Move to next player

#Counts the hand efficiently for tiles
def hand_to_counts(hand):
    counts = {}
    for t in hand:
        key = (t.suit, t.value)
        counts[key] = counts.get(key, 0) + 1
    return counts

def is_standard_hand(hand):
    if len(hand) != 14:
        return False
    
    counts = hand_to_counts(hand)

    for tile in list(counts.keys()):
        #This is for checking every possible pair in the hand. If there's not more than 2, it will ignore the tile and go next
        if counts[tile] >= 2:
            counts[tile] -= 2

            if check_with_melds(counts):
                return True

            counts[tile] += 2  # restore and try next

    return False

# --- helper: deterministic order for suits ---
_SUITS_ORDER = {'l': 0, 'c': 1, 'b': 2, 'honor': 3}

def _tile_sort_key(tile):
    suit, value = tile
    val_key = value if isinstance(value, int) else 0
    return (_SUITS_ORDER.get(suit, 99), val_key)

def check_with_melds(counts):
    '''
    
    Checks if hand has valid sequences/triplets. If a triplet/sequence/Kan is found, uses recursive with the rest of the count
    until there is nothing left or is not a valid hand

    count: The tiles in the player hands that does not include the pair

    returns Boolean
    
    '''
    #This checks if there is anything else to check
    if sum(counts.values()) == 0:
        return True
    
    #Picks the top tile to see if there is a sequence or triplet
    # pick the smallest tile (deterministic) that still has count > 0
    nonzero = [t for t, c in counts.items() if c > 0]
    if not nonzero:
        return True
    tile = min(nonzero, key=_tile_sort_key)
    suit, value = tile

    #Checks Kan
    if counts[tile] == 4:
        counts[tile] -= 4
        if check_with_melds(counts):
            return True
        counts[tile] += 4
    
    # Check triplet
    if counts[tile] >= 3:
        counts[tile] -= 3
        if check_with_melds(counts):
            return True
        counts[tile] += 3

    # Check sequence (only if suit tile)
    if suit != "honor" and isinstance(value, int) and value <= 7:
        t2 = (suit, value + 1)
        t3 = (suit, value + 2)
        if counts.get(t2, 0) > 0 and counts.get(t3, 0) > 0:
            counts[tile] -= 1
            counts[t2] -= 1
            counts[t3] -= 1
            if check_with_melds(counts):
                return True
            counts[tile] += 1
            counts[t2] += 1
            counts[t3] += 1

    return False

def is_tenpai(hand):
    '''
    
    Checks if the player is one tile away from winning

    hand: The player's hand

    Returns the waits if hand is possible to win with
    
    '''
    waits = []

    for suit in ['c', 'l', 'b', 'honor']:
        if suit == 'honor':
            possible = ['E','S','W','N', 'WH', 'G', 'R']
        else:
            possible = range(1,10)

        for tile in possible:
            fake = Tile(suit, tile)
            if check_win_with_tile(hand,fake):
                waits.append(fake)
    if len(waits) == 0:
        return "Not valid"

    # Sort waits by suit priority, then tile value
    waits.sort(key=lambda t: (
        _SUITS_ORDER[t.suit],
        t.value if isinstance(t.value, int) else 0
    ))     
    return waits

def check_win_with_tile(hand, tile):
    '''

    Adds the tile to the hand and tests it to see if it wins
    
    hand: The player's hand
    tile: The tile that is considered to win with

    return Boolean
    '''
    
    test_hand = hand[:] + [tile]
    return is_standard_hand(test_hand)

# Example usage
if __name__ == "__main__":
    
    board = create_set()
    discard_pile = []

    print("Board: ", board, "\n")
    print("Shuffling board...\n")
    
    shuffle_tiles(board)

    dice = random.randint(2,12)

    print(f"Starting hands:\n"
        f"East wall: {board[:34]}\n"
        f"South wall: {board[34:68]}\n"
        f"West wall: {board[68:102]}\n"
        f"North wall: {board[102:136]}\n"
        f"Dice roll: {dice}\n"
    )

    EP, SP, WP, NP, board, deadwall = distribute_tiles(board, dice)
    players = [
    Player("East", EP),
    Player("South", SP),
    Player("West", WP),
    Player("North", NP)
    ]

    for i in range(4):
        print(f"{players[i].name}'s hand: ", end ='')
        display_hand(players[i].hand)
        print("\n")

    play_game(players, board)

    for i in range(4):
            print(f"{players[i].name}'s hand: ", end ='')
            display_hand(players[i].hand)
    


# organize_hand(testHand)
# print(f"Test hand:", end= " ")
# display_hand(testHand)

winning_hand = [
    Tile('c', 1), Tile('c', 2), Tile('c', 3),          # 1-2-3 chars
    Tile('l', 4), Tile('l', 5), Tile('l', 6),          # 4-5-6 lotus
    Tile('b', 7), Tile('b', 8), Tile('b', 9),          # 7-8-9 bamboo
    Tile('l', 3), Tile('l', 3), Tile('l', 3),          # triplet of 3 lotus
    Tile('b', 2), Tile('b', 2)                         # pair of 2 bamboo
]

tenpai_hand = [
    Tile('c', 2), Tile('c', 3), Tile('c', 4) ,          
    Tile('c', 5), Tile('c', 6),                        # needs 6c
    Tile('l', 7), Tile('l', 8), Tile('l', 9),          # 7-8-9 lotus
    Tile('b', 2), Tile('b', 3), Tile('b', 4),          # 2-3-4 bamboo
    Tile('l', 5), Tile('l', 5)                         # pair
]

# print(is_standard_hand(winning_hand))

display_hand(tenpai_hand)
print(is_tenpai(tenpai_hand))
