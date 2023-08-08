import requests

class ScryfallClient:
    def search_cards(self, search_query):
        resp = requests.get(f"https://api.scryfall.com/cards/search?q={search_query}").json()#ss

        if resp.get("total_cards") <= 175:
            return resp.get("data")
        else:
            cards_left = resp.get("total_cards") - 175

            cards = []

            for card in resp.get("data"):
                cards.append(card)

            while cards_left > 0:
                resp = requests.get(resp.get("next_page")).json()

                cards_left = cards_left - 175
                
                for card in resp.get("data"):
                    cards.append(card)

            return(cards)

    def fuzzy_search(self, name):
        resp = requests.get(f"https://api.scryfall.com/cards/named?fuzzy={name}")
        return(resp.json())

    def get_card_images(self, cards):
        
        images = []

        for card in cards:
            if card.get("card_faces") is None:
                images.append(card.get("image_uris").get("large"))
            else:
                print("multifaced card")
        
        return images

    def get_mana_costs(self, cards):

        mana_costs = []
    
        for card in cards:
            if card.get("card_faces") is None:
                mana_costs.append(card.get("mana_cost"))
            else:
                print("multifaced card")
        return mana_costs