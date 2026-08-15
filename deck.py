#rank点数0-12对应2到A，参照规则中单牌大小，便于进行数学上的大小比较，suit花色3-黑桃；2-红桃；1-梅花；0-方块，主要用于比较金花，后续可以用于单牌大小比较
#这个函数用于生成一副完整牌堆
def create_deck():
    deck = []
    for rank in range(13):
        for suit in range(4):
            deck.append({"rank":rank,"suit":suit})
    return deck

#规则中发牌采取了一次性发一位玩家的牌，下列deal函数用于给Players发牌
from player import player_generator
import random
def deal(players,deck):
    for player in players:
        for i in range(3):
            index = random.randint(0,len(deck)-1)
            card = deck[index]
            player.hand.append(card)
            deck.pop(index)


