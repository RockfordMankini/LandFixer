from scryfall import *
from collections import Counter
import re
import math

def decklist_to_json(card_list):
    card_list = card_list.split('\n')
    card_objects = []

    for card in card_list:
        try:
            parts = card.split(' ', 1)  # Split by the first space to separate count and name
            count = int(parts[0])
            name = parts[1]
            card_objects.append({'name': name, 'copies': count})
        except:
            continue

    return card_objects

def deck_to_pips(decklist_json):

    client = ScryfallClient()

    mana_costs = []
    cards = []
    
    for card_json in decklist_json:
        card = client.fuzzy_search(card_json['name'])
        mana_cost = client.get_mana_costs([card])

        for i in range(card_json['copies']):
            mana_costs.append(mana_cost)
            cards.append(card)

    flattened_costs = [element for sublist in mana_costs for element in sublist]
    
    flatter_costs = []

    for flat_cost in flattened_costs:
        # Extract individual characters and numbers using regular expression
        characters_and_numbers = re.findall(r'[A-Z]+|[0-9]+', flat_cost)
        flatter_costs.extend(characters_and_numbers)

    modified_costs = []
    for item in flatter_costs:
        if(item in ['W', 'U', 'B', 'R', 'G', 'C']):
            modified_costs.append(item)

    counts = Counter(modified_costs)
    total = sum(counts.values())
    counts = dict(counts)

    print(counts)

    counts["Total"] = total

    deck = {
        "cards": cards,
        "counts": counts
    }

    return(deck)

def construct_query(colors):
    
    id_str = ""
    produces_str = ""

    for color in colors.keys():
        if color != "GC" and color != "C" and color != "Total":
            id_str = id_str + color
            produces_str = produces_str + f"produces>{color} or "

    produces_str = produces_str[:-4]

    final_str = f"t:land (id<={id_str} and ({produces_str})) order:edhrec"

    return(final_str)

    #t:land (id<=grixis and (produces>u or produces>b or produces>r)) order:edhrec"

def estimate_percentages(deck_counts, decklist):
    print(deck_counts)

    num_cards = len(decklist)

    total = deck_counts.get("Total")
    
    # estimate stats for what the desired state is.
    for key in deck_counts.keys():
        deck_counts[key] = round((deck_counts[key] / total) * 100, 2)
    print(deck_counts)
    deck_counts.pop("Total")

    suggestions = {}
    suggestions["cards_left"] = f"<p>This deck has {num_cards}/100 cards. You need to add {100 - num_cards}. "

    desired = "<ul>"
    for key in deck_counts.keys():
        desired = desired + f"<li>{deck_counts[key]}% of your sources should produce {key}.</li>"
    desired = desired + "</ul>"

    suggestions["desired"] = desired

    # find out how much of the cards already generate the desired mana

    current = get_current_state(decklist, deck_counts.keys())

    suggestions["cards_left"] = suggestions["cards_left"] + f"You currently have <b>{current['producers']}</b> lands in your deck.</p>"

    current_state = "<ul>"

    for key in deck_counts.keys():

        if(key not in current.keys()):
            current_state = current_state + f"<li>0% of your lands produce {key}. ❌</li>"
        elif(current[key] >= deck_counts[key]):
            current_state = current_state + f"<li>{current[key]}% of your lands produce {key}. ✔️</li>"
        else:
            current_state = current_state + f"<li>{current[key]}% of your lands produce {key}. ❌</li>"

    current_state = current_state + "</ul>"

    suggestions["current"] = current_state

    return suggestions

def get_current_state(decklist, colors):
    
    producers = 0
    current = {}

    for card in decklist:
        card_type_line = card.get("type_line")

        if "land" in card_type_line.lower() and card.get("produced_mana") is not None:
            mana = card.get("produced_mana")

            produced_bumped = False

            for symbol in mana:
                if symbol in colors:

                    if(produced_bumped is False):
                        producers = producers + 1
                        produced_bumped = True

                    if symbol not in current.keys():
                        current[symbol] = 1
                    else:
                        current[symbol] = current[symbol] + 1

    for key in current.keys():
        current[key] = round((current[key] / producers) * 100, 2)

    current["producers"] = producers

    return(current)