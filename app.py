from flask import Flask, render_template, request
from scryfall import ScryfallClient
from utils import *
 
app = Flask(__name__, template_folder='templates')

@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'GET':

        #client = ScryfallClient()
        #cards = client.search_cards("t:land (id<=grixis and (produces>u or produces>b or produces>r)) order:edhrec")
        #images = client.get_card_images(cards)
        return render_template("base.html")

    if request.method == 'POST':
        decklist = request.form["decklist"]
        converted = decklist_to_json(decklist)
        num_cards = len(converted)

        deck_data = deck_to_pips(converted)

        deck_counts = deck_data["counts"]
        current_cards = deck_data["cards"]

        search_string = construct_query(deck_counts)

        client = ScryfallClient()
        cards = client.search_cards(search_string)
        images = client.get_card_images(cards)

        print(deck_counts)

        suggestions = estimate_percentages(deck_counts.copy(), current_cards)

        return render_template("cards.html", images=images, deck_counts=deck_counts, suggestions=suggestions)
 
# main driver function
if __name__ == '__main__':
 
    app.run(debug=False)
