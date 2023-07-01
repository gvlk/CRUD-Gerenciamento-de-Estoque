from setup_database import setup_database
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://spi:spi@localhost/crud_spi'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
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


@app.route('/')
def index() -> str:
    return render_template('index.html')


@app.route('/read')
def read() -> str:
    data = Product.query.order_by(Product.name)
    return render_template('read.html', data=data)


@app.route('/insert', methods=['GET', 'POST'])
def insert() -> str:
    if request.method == 'POST':
        name = request.form.get('name')
        price = float(request.form.get('price'))
        quantity = int(request.form.get('quantity'))

        new_product = Product(name, price, quantity)

        db.session.add(new_product)
        db.session.commit()

        return 'Produto adicionado'
    else:
        return render_template("insert.html")


if __name__ == "__main__":
    print("Criando banco de dados...")
    setup_database()
    print("Banco de dados pronto!")
    app.run(debug=True)
