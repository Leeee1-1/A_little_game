from deck import create_deck,deal
from deck import deal
from player import player_generator
from hand import evaluate_hand,compare_hands
players = player_generator()
deck = create_deck()
bet = 10
accumulated_bet = 0
deal(players,deck)
active_players = [p for p in players if p.active]
while len(active_players) > 1:
    for player in players:
        if not player.active:
            continue
        print(f"{player.name}的回合")
        pass
    active_players = [p for p in players if p.active]