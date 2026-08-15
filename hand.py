def evaluate_hand(hand):
    rank_value = []
    suit_value = []
    for card in hand:
        rank_value.append(card["rank"])
        suit_value.append(card["suit"])        
    sorted_rank = sorted(rank_value)
    if rank_value[0] == rank_value[1] == rank_value[2]:
        return (6,rank_value[0])
    elif suit_value[0] == suit_value[1] == suit_value[2]:
        if sorted_rank == [0,1,12]:
            return(5,1)
        elif sorted_rank[2]-sorted_rank[1] == 1 and sorted_rank[1]-sorted_rank[0] == 1:
            return(5,max(rank_value))
        else:
            return(4,*sorted_rank[::-1])
    elif sorted_rank == [0,1,12]:
        return(3,1)
    elif sorted_rank[2]-sorted_rank[1] == 1 and sorted_rank[1]-sorted_rank[0] == 1:
        return(3,max(rank_value))
    elif sorted_rank[0] == sorted_rank[1] or sorted_rank[1] == sorted_rank[2]:
        pair_rank = sorted_rank[1]
        kicker = sum(sorted_rank) - pair_rank*2
        return(2,pair_rank,kicker)
    else:
        return(1,*sorted(rank_value,reverse=True))

def compare_hands(opener,target):
    opener_power = evaluate_hand(opener.hand)
    target_power = evaluate_hand(target.hand)
    if opener_power > target_power:
        return opener.name
    else:
        return target.name