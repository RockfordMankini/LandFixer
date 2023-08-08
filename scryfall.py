import requests

class ScryfallClient:
    def search_cards(self, search_query):
        return requests.get(f"https://api.scryfall.com/cards/search?q={search_query}").json().get("data")#ssssssssssssssss

    def get_card_images(self, cards):
        
        images = []

        print(type(cards))

        for card in cards:
            print(card)
            if card.get("card_faces") is None:
                images.append(card.get("image_uris").get("large"))
            else:
                print("multifaced card")
        
        return images