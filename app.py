import flask_sqlalchemy.query

from setup_database import setup_database
from flask import Flask, render_template, request, redirect, url_for, flash, Response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from secrets import token_hex
from random import choices, uniform, randint
from string import ascii_uppercase, ascii_lowercase

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://spi:spi@localhost/crud_spi'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = token_hex(32)
db = SQLAlchemy(app)


class Product(db.Model):
    __tablename__ = 'Product'

    productid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200))
    price = db.Column(db.Float)
    quantity = db.Column(db.Integer)
    lastupdated = db.Column(db.DateTime, default=func.now())

    def __init__(self, name, price, quantity) -> None:
        self.name = name
        self.price = price
        self.quantity = quantity


@app.route("/")
def index() -> str:
    return render_template("index.html", data=get_data())


@app.route("/insert", methods=["GET", "POST"])
def insert() -> str | Response:
    if request.method == "POST":
        name = request.form.get("name")
        price = float(request.form.get("price"))
        quantity = int(request.form.get("quantity"))

        new_product = Product(name, price, quantity)

        db.session.add(new_product)
        db.session.commit()

        return redirect(url_for("index"))

    else:
        return render_template("index.html", data=get_data(), insert=True)


@app.route("/remove", methods=["GET", "POST"])
def remove() -> str | Response:
    if request.method == "POST":
        product_id = request.form.get("product_id")
        product = Product.query.get(product_id)

        if product:
            db.session.delete(product)
            db.session.commit()

        return redirect(url_for("index"))

    else:
        return render_template("index.html", data=get_data(), remove=True)


@app.route('/update', methods=['GET', 'POST'])
def update() -> str | tuple[str, int]:
    if request.method == "POST":
        product_id = request.form.get('product_id')
        name = request.form.get('name')
        price = float(request.form.get('price'))
        quantity = int(request.form.get('quantity'))

        product = Product.query.get(product_id)

        if product:
            product.name = name
            product.price = price
            product.quantity = quantity
            product.lastupdated = func.now()
            db.session.commit()

        return '', 204

    else:
        return render_template("index.html", data=get_data(), update=True)


@app.route("/generate-random-data")
def generate_random_data() -> Response:
    for _ in range(10):
        name = ''.join(choices(ascii_uppercase + ascii_lowercase, k=10))
        price = round(uniform(0.01, 100.0), 2)
        quantity = randint(1, 100)

        new_product = Product(name, price, quantity)
        db.session.add(new_product)
        db.session.commit()

    return redirect(url_for("index"))


def get_data() -> flask_sqlalchemy.query.Query:
    return Product.query.order_by(Product.name)


if __name__ == "__main__":
    print("Criando banco de dados...")
    setup_database()
    print("Banco de dados pronto!")
    app.run(debug=True)
