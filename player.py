class Player:
    def __init__(self,name,chips=500):
        self.name = name
        self.chips = chips
        self.hand = []
        self.actions = []
        self.seen = False
        self.active = True
def player_generator(n=4):
    players = []
    for i in range(1,n+1):
        players.append(Player(f"Player{i}"))
    return players