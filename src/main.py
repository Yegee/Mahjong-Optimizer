import random

class Tile:
    def __init__(self, suit, value):
        self.suit = suit #This will be for 'c', 'l', 'b'(characters, lotus, bamboo)
        self.value = value #This will be 1-9 for the suits, 'E', 'S', 'W', 'N', 'WH', 'R', 'G' for honor titles
    
    def __repr__(self):
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

    for i in range(4): 
        random.shuffle(tiles)

def distribute_tiles(tiles, number):

    E_hand = []
    S_hand = []
    W_hand = []
    N_hand = []


    #for hands in range(1, 4):
        

    return "nothing"

# Example usage
if __name__ == "__main__":
    
    board = create_set()

    print("Board: ", board, "\n")
    print("Shuffling board...\n")
    
    shuffle_tiles(board)

print(
    f"East wall: {board[:34]}\n"
    f"South wall: {board[34:68]}\n"
    f"West wall: {board[68:102]}\n"
    f"North wall: {board[102:136]}\n"
    f"Dice roll: {random.randint(1,12)}"
)
