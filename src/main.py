import random

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
    for _ in range(3):
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

    return hand

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

# Example usage
if __name__ == "__main__":
    
    board = create_set()
    discard_pile = []

    print("Board: ", board, "\n")
    print("Shuffling board...\n")
    
    shuffle_tiles(board)



dice = random.randint(2,12)

print(
    f"East wall: {board[:34]}\n"
    f"South wall: {board[34:68]}\n"
    f"West wall: {board[68:102]}\n"
    f"North wall: {board[102:136]}\n"
    f"Dice roll: {dice}\n"
)

EP, SP, WP, NP, board, deadwall = distribute_tiles(board, dice)
hands = [EP, SP, WP, NP]

print(
    f"East Player: {hands[0]}\n\n"
    f"South Player: {hands[1]}\n\n"
    f"West Player: {hands[2]}\n\n"
    f"North Player: {hands[3]}\n\n"
    f"Board State: {board}\n\n"
    f"DeadWall: {deadwall}(Dora is {deadwall[-6]})\n\n"
)

#Helps the count for the player's turn
turn = 0
players = ["East", "South", "West", "North"]

while board:
    current_player = players[turn % 4]
    current_hand = hands[turn % 4]

    draw_tile(board, current_hand)
    discard_pile.append(temp_discard_tile(current_hand, 0))


# TODO: check for win conditions
# if check_yaku(current_hand):
#     winner = current_player
#     break

    turn += 1  # Move to next player

print(f"Hands:\n\n"
      f"East: {hands[0]}\n\n"
      f"South: {hands[1]}\n\n"
      f"West: {hands[2]}\n\n"
      f"North: {hands[3]}\n\n"
      f"Discard: {discard_pile}\n\n"
      )




# draw_tile(board, EP)

# print(f"East Player after Draw{EP}\n\n")

# while True:
#     discard_input = input("Enter tile for discard: \n").strip()

#     discarded = discard_tile(EP, discard_input)

#     if discarded:
#         print(f"\nDiscarded {discarded}")
#         break
#     else:
#         print("Tile not found in hand. Please enter a valid tile from your hand.")


# print(f"East Player after discard: {EP}\n\n")
