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

    E_hand = []
    S_hand = []
    W_hand = []
    N_hand = []

    E_wall = board[:34]
    S_wall = board[34:68]
    W_wall = board[68:102]
    N_wall = board[102:136]


    deadwall_index = 0
    starting_index = 0
    
    if (dice == 5)or (dice == 9):

        starting_index = (dice*2)
        deadwall_index = (starting_index - 1)
        while deadwall_index < 13:
            E_wall.insert(0, N_wall.pop(-1))
            deadwall_index += 1
            starting_index += 1

        new_board = E_wall + S_wall + W_wall + N_wall

        

    elif (dice == 2) or (dice == 6) or (dice == 10):

        starting_index = (dice*2)
        deadwall_index = (starting_index - 1)
        while deadwall_index < 13:
            S_wall.insert(0, E_wall.pop(-1))
            deadwall_index += 1
            starting_index += 1

        new_board = S_wall + W_wall + N_wall + E_wall

            
    elif (dice == 3) or (dice == 7) or (dice == 11):

        starting_index = (dice*2)
        deadwall_index = (starting_index - 1)
        while deadwall_index < 13:
            W_wall.insert(0, S_wall.pop(-1))
            deadwall_index += 1
            starting_index += 1
        
        new_board = W_wall + N_wall + E_wall + S_wall


    elif (dice == 4) or (dice == 8) or (dice == 12):

        starting_index = (dice*2)
        deadwall_index = (starting_index - 1)
        while deadwall_index < 13:
            N_wall.insert(0, W_wall.pop(-1))
            deadwall_index += 1
            starting_index += 1

        new_board = N_wall + E_wall + S_wall + W_wall 


    while starting_index != 0:
            new_board.append(new_board.pop(0))
            starting_index -= 1
    
    for player in range(3):

        for i in range(4): E_hand.append(new_board.pop(0))
        for i in range(4): S_hand.append(new_board.pop(0))
        for i in range(4): W_hand.append(new_board.pop(0))
        for i in range(4): N_hand.append(new_board.pop(0))
    
    E_hand.append(new_board.pop(0))
    S_hand.append(new_board.pop(0))
    W_hand.append(new_board.pop(0))
    N_hand.append(new_board.pop(0))

    organize_hand(E_hand)
    organize_hand(S_hand)
    organize_hand(W_hand)
    organize_hand(N_hand)

    return E_hand, S_hand, W_hand, N_hand, new_board

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

    '''

    new_tile = board.pop(0)
    hand.append(new_tile)

    organize_hand(hand)

def discard_tile(hand, tile):
    
    '''
    
    Removes a tile from players hand

    hand:Players hand
    tile: index for tile to discard

    Returns the discarded tile for discard pile 

    '''

    return hand.pop(tile-1)

# Example usage
if __name__ == "__main__":
    
    board = create_set()

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

EP, SP, WP, NP, board = distribute_tiles(board, dice)

print(
    f"East Player: {EP}\n\n"
    f"South Player: {SP}\n\n"
    f"West Player: {WP}\n\n"
    f"North Player: {NP}\n\n"
    f"Board State: {board}\n\n"
)

draw_tile(board, EP)

print(f"East Player after Draw{EP}\n\n")

# ToDO: Change this to tile rather than index
index = int(input("Enter Index for discard: \n"))

discard_tile(EP, index)

print(f"East Player after discard{EP}\n\n")
