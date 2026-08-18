from deck import create_deck,deal
from deck import deal
from player import player_generator
from hand import evaluate_hand,compare_hands

RANK_LABELS = {0: "2", 1: "3", 2: "4", 3: "5", 4: "6", 5: "7", 6: "8", 7: "9", 8: "10", 9: "J", 10: "Q", 11: "K", 12: "A"}
SUIT_LABELS = {3: "♠", 2: "♥", 1: "♣", 0: "♦"}


def format_card(card):
    return SUIT_LABELS[card["suit"]] + RANK_LABELS[card["rank"]]


def format_hand(player):
    return " ".join(format_card(c) for c in player.hand)


players = player_generator()
deck = create_deck()
bet = 10
accumulated_bet = 0
deal(players,deck)
active_players = [p for p in players if p.active]
while len(active_players) > 1:
    for player in players:
        active_players = [p for p in players if p.active]
        if not player.active:
            continue
        print(f"========== {player.name} 的回合 ==========")
        if not player.seen:
            while True:
                whether_to_see = input("是否看牌:请输入yes/no")
                if whether_to_see in ["yes","no"]:
                    break
                print("非法输入,请输入yes/no")
            if whether_to_see == "yes":
                player.seen = True
                print(f"{player.name} 已看牌。")
                print("=" * 32)
                print(f"{player.name}，你的手牌是：")
                print(format_hand(player))
                print("=" * 32)
                while True:
                    action = input("做出你的选择:1.跟注 2.开人 3.弃牌")
                    if action == "1":
                        if player.chips >= bet*2:
                            player.chips -= bet*2
                            accumulated_bet += bet*2
                            print(f"{player.name} 跟注 {bet*2} chips。当前底池:{accumulated_bet}")
                            break
                        else:
                            targets = [p for p in active_players if p!= player]
                            print("您的筹码不足,必须选择一位玩家开牌,您可以选择:")
                            for i,target in enumerate(targets,start=1):
                                print(f"{i}.{target.name}")
                            while True:
                                target_choice = input("请选择")
                                if target_choice.isdigit():
                                    target_choice =  int(target_choice)
                                    if 1 <= target_choice <= len(targets):
                                        break
                                print("非法输入,请重新选择")
                            target = targets[target_choice-1]
                            open_cost = player.chips
                            player.chips = 0
                            accumulated_bet += open_cost
                            print(f"{player.name} 强开 → {target.name}")
                            winner = compare_hands(player,target)
                            if winner == player.name :
                                target.active = False
                                player.chips += open_cost*2
                                accumulated_bet -= open_cost*2
                                print(f"{target.name} 输掉比牌，{target.name} 出局！")
                            else:
                                player.active = False
                                print(f"{player.name} 比牌失败，{player.name} 出局！")
                            break
                    elif action == "2":
                        targets = [p for p in active_players if p != player]
                        print("请选择您要开的人：")
                        for i, target in enumerate(targets, start=1):
                            print(f"{i}.{target.name}")
                        while True:
                            target_choice = input("请选择")
                            if target_choice.isdigit():
                                target_choice =  int(target_choice)
                                if 1 <= target_choice <= len(targets):
                                    break
                            print("非法输入,请重新选择")
                        target = targets[target_choice-1]
                        if target.seen :
                            open_cost = 2*bet
                        else:
                            open_cost = 4*bet
                        if player.chips >= open_cost:
                            player.chips -= open_cost
                            accumulated_bet += open_cost
                            print(f"{player.name} 开牌 → {target.name}")
                            winner = compare_hands(player, target)
                            if winner == player.name:
                                target.active = False
                                print(f"{target.name} 输掉比牌，{target.name} 出局！")
                            else:
                                player.active = False
                                print(f"{player.name} 比牌失败，{player.name} 出局！")
                        break
                    elif action == "3":
                        player.active = False
                        print(f"{player.name} 选择弃牌，{player.name} 出局！")
                        break
            elif whether_to_see == "no":
                while True:
                    action = input("请做出你的选择:1.跟注 2.开人")
                    if action == "1":
                        if player.chips >= bet:
                            player.chips -= bet
                            accumulated_bet += bet
                            print(f"{player.name} 闷跟 {bet} chips。当前底池:{accumulated_bet}")
                            break
                        else:
                            print("筹码不足,无法跟注")
                            while True:
                                compulsory_settlement = input("您只能:1.闷开 2.看牌")
                                if compulsory_settlement == "1":
                                    targets = [p for p in active_players if p!= player]
                                    print("您可以选择开:")
                                    for i,target in enumerate(targets,start=1):
                                        print(f"{i}.{target.name}")
                                    while True:
                                        target_choice = input("请选择")
                                        if target_choice.isdigit():
                                            target_choice =  int(target_choice)
                                            if 1 <= target_choice <= len(targets):
                                                break
                                        print("非法输入,请重新选择")
                                    target = targets[target_choice-1]
                                    open_cost = player.chips
                                    player.chips = 0
                                    accumulated_bet += open_cost
                                    print(f"{player.name} 闷开 → {target.name}")
                                    winner = compare_hands(player,target)
                                    if winner == player.name :
                                        target.active = False
                                        player.chips += open_cost*2
                                        accumulated_bet -= open_cost*2
                                        print(f"{target.name} 输掉比牌，{target.name} 出局！")
                                    else:
                                        player.active = False
                                        print(f"{player.name} 比牌失败，{player.name} 出局！")
                                    break
                                elif compulsory_settlement == "2":
                                    player.seen = True
                                    print(f"{player.name} 已看牌。")
                                    print("=" * 32)
                                    print(f"{player.name}，你的手牌是：")
                                    print(format_hand(player))
                                    print("=" * 32)
                                    break
                            break
                    elif action == "2":
                        open_cost = min(player.chips,2*bet)
                        targets = [p for p in active_players if p != player]
                        print("请选择您要开的人：")
                        for i, target in enumerate(targets, start=1):
                            print(f"{i}.{target.name}")
                        while True:
                            target_choice = input("请选择")
                            if target_choice.isdigit():
                                target_choice =  int(target_choice)
                                if 1 <= target_choice <= len(targets):
                                    break
                            print("非法输入,请重新选择")
                        target = targets[target_choice-1]
                        player.chips -= open_cost
                        accumulated_bet += open_cost
                        print(f"{player.name} 闷开 → {target.name}")
                        winner = compare_hands(player, target)
                        if winner == player.name:
                            target.active = False
                            player.chips += open_cost
                            accumulated_bet -= open_cost
                            print(f"{target.name} 输掉比牌，{target.name} 出局！")
                        else:
                            player.active = False
                            print(f"{player.name} 比牌失败，{player.name} 出局！")
                        break
        elif player.seen:
            while True:
                action = input("做出你的选择:1.跟注 2.开人 3.弃牌")
                if action == "1":
                    if player.chips >= bet*2:
                        player.chips -= bet*2
                        accumulated_bet += bet*2
                        print(f"{player.name} 跟注 {bet*2} chips。当前底池:{accumulated_bet}")
                        break
                    else:
                        targets = [p for p in active_players if p!= player]
                        print("您的筹码不足,必须选择一位玩家开牌,您可以选择:")
                        for i,target in enumerate(targets,start=1):
                            print(f"{i}.{target.name}")
                        while True:
                            target_choice = input("请选择")
                            if target_choice.isdigit():
                                target_choice =  int(target_choice)
                                if 1 <= target_choice <= len(targets):
                                    break
                            print("非法输入,请重新选择")
                        target = targets[target_choice-1]
                        open_cost = player.chips
                        player.chips = 0
                        accumulated_bet += open_cost
                        print(f"{player.name} 强开 → {target.name}")
                        winner = compare_hands(player,target)
                        if winner == player.name :
                            target.active = False
                            player.chips += open_cost*2
                            accumulated_bet -= open_cost*2
                            print(f"{target.name} 输掉比牌，{target.name} 出局！")
                        else:
                            player.active = False
                            print(f"{player.name} 比牌失败，{player.name} 出局！")
                        break
                elif action == "2":
                    targets = [p for p in active_players if p != player]
                    print("请选择您要开的人：")
                    for i, target in enumerate(targets, start=1):
                        print(f"{i}.{target.name}")
                    while True:
                        target_choice = input("请选择")
                        if target_choice.isdigit():
                            target_choice =  int(target_choice)
                            if 1 <= target_choice <= len(targets):
                                break
                        print("非法输入,请重新选择")
                    target = targets[target_choice-1]
                    if target.seen :
                        open_cost = 2*bet
                    else:
                        open_cost = 4*bet
                    if player.chips >= open_cost:
                        player.chips -= open_cost
                        accumulated_bet += open_cost
                        print(f"{player.name} 开牌 → {target.name}")
                        winner = compare_hands(player, target)
                        if winner == player.name:
                            target.active = False
                            print(f"{target.name} 输掉比牌，{target.name} 出局！")
                        else:
                            player.active = False
                            print(f"{player.name} 比牌失败，{player.name} 出局！")
                        break
                elif action == "3":
                    player.active = False
                    print(f"{player.name} 选择弃牌，{player.name} 出局！")
                    break
    active_players = [p for p in players if p.active]
if len(active_players) == 1:
    winner = active_players[0]
    print("=" * 32)
    print("游戏结束！")
    print(f"赢家：{winner.name}")
    print(f"获得底池：{accumulated_bet} chips")
    print("=" * 32)
    winner.chips += accumulated_bet
    accumulated_bet = 0
    print("最终筹码：")
    for p in players:
        print(f"{p.name}: {p.chips} chips")
