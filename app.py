from flask import Flask, render_template
from scryfall import ScryfallClient
 
app = Flask(__name__, template_folder='templates')

@app.route('/')
def index():
    client = ScryfallClient()
    cards = client.search_cards("t:land (id<=grixis and (produces>u or produces>b or produces>r)) order:edhrec")
    images = client.get_card_images(cards)
    return render_template("base.html", images=images)
 
# main driver function
if __name__ == '__main__':
 
    app.run(debug=True)