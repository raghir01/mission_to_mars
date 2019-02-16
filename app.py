# import necessary libraries
from flask import Flask, render_template
from scrape_mars import get_data

# create instance of Flask app
app = Flask(__name__)

# create route that renders index.html template
@app.route("/")
def home():
    data = get_data()
    return render_template("index.html", text="Mission to Mars", data=data)


if __name__ == "__main__":
    app.run(debug=True)
