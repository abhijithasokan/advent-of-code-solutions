from utils import aoc_comm
import os

# --- AUTO SUBMIT SETTINGS ---
settings = {
    'day' : 22,
    'year' : 2020,
    'cookie-path' : os.path.realpath('../aoc_cookie.json')
}


def parse_input(inp_content):
    inp_content = inp_content.strip().split('\n\n')
    p1_deck, p2_deck = inp_content
    p1_deck, p2_deck = p1_deck.split('\n')[1:], p2_deck.split('\n')[1:]
    return list(map(int, p1_deck))[::-1], list(map(int, p2_deck))[::-1]


def game_l1(p1_deck, p2_deck):
    while p1_deck and p2_deck:
        card1 = p1_deck.pop()
        card2 = p2_deck.pop()
        if card1 > card2:
            p1_deck = [card2, card1] + p1_deck
        else:
            p2_deck = [card1, card2] + p2_deck
    return p1_deck, p2_deck


def get_final_num(deck):
    return sum( (ind + 1) * card for ind, card in enumerate(deck)  )

def check_cache(decks, cache_table):
    if decks in cache_table:
        #print("cache hit")
        return cache_table[decks]

    exhcanged_decks = decks[::-1]
    if exhcanged_decks in cache_table:
        #print("flip cache hit")
        return 1 - cache_table[exhcanged_decks]  # other player wins ( if winner is 1, winner after exhange is 2 (which is represented as 0) )
    return None


CALLS_TO_FUNC = 0
def game_l2(p1_deck, p2_deck, cache_table, is_sub_game = True):
    if is_sub_game:
        max_card1 = max(p1_deck)
        max_card2 = max(p2_deck)
        if max_card1 > max_card2 and (max_card1 > (len(p1_deck) + len(p2_deck) - 2) ):
            #player 1 wins!
            return 1, None, None

    cache_table_key = (tuple(p1_deck), tuple(p2_deck))
    final_winner = check_cache(cache_table_key, cache_table)
    
    if final_winner is not None:
        return final_winner, None, None

    global CALLS_TO_FUNC
    CALLS_TO_FUNC += 1
    
    seen_decks = set()
    
    while p1_deck and p2_deck:
        decks = (tuple(p1_deck), tuple(p2_deck))

        if decks in seen_decks:
            final_winner = 1
            cache_table[cache_table_key] = final_winner
            return final_winner, None, None

        seen_decks.add(decks)
        
        cache_entry = check_cache(decks, cache_table)    
        if cache_entry is not None:
            return cache_entry, None, None

        card1 = p1_deck.pop()
        card2 = p2_deck.pop()
        if card1 <= len(p1_deck) and card2 <= len(p2_deck):
            new_p1_deck, new_p2_deck  = list(p1_deck[-card1:]), list(p2_deck[-card2:])
            round_winner, _ ,_  = game_l2(new_p1_deck, new_p2_deck, cache_table, True)
        else:
            round_winner = 1 if card1 > card2 else 0
            
        if round_winner == 1:
            p1_deck = [card2, card1] + p1_deck
        else:
            p2_deck = [card1, card2] + p2_deck
            
    final_winner = 1 if p1_deck else 0
    cache_table[cache_table_key] = final_winner
    return final_winner, p1_deck, p2_deck




@aoc_comm(settings, level = 1)
def solve_l1(input_str): 
    p1_deck, p2_deck = parse_input(input_str)
    p1_deck, p2_deck = game_l1(p1_deck, p2_deck)
    return get_final_num(p1_deck or  p2_deck)


@aoc_comm(settings, level = 2)
def solve_l2(input_str):
    p1_deck, p2_deck = parse_input(input_str)
    winner, p1_deck, p2_deck = game_l2(p1_deck, p2_deck, {}, False)
    print("CALLS_TO_FUNC: " , CALLS_TO_FUNC)
    return get_final_num(p1_deck if winner == 1 else p2_deck)


def main():
    l1_status = solve_l1()
    print(l1_status)

    l2_status = solve_l2()
    print(l2_status)


if __name__ == '__main__':
    main()
