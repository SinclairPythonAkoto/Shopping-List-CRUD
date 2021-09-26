import os

from flask import Flask
from flask import render_template 
from flask import request
from flask import redirect

from flask_sqlalchemy import SQLAlchemy

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "shoppinglistdatabase.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True


db = SQLAlchemy(app)

# create new db table 
class ShoppingList(db.Model):
	foodList = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
	
	# this allows us to print book title
	def __repr__(self):
		return f"<Title: {self.foodList}>" # or .format(self.foodList)

@app.route('/', methods=["GET", "POST"])
def home():
	if request.form:
		food = ShoppingList(foodList=request.form.get("item"))
		db.session.add(food)
		db.session.commit()
	foods = ShoppingList.query.all()
	return render_template("home.html", foods=foods)

@app.route("/update", methods=["POST"])
def update():
	newItem = request.form.get("newItem")
	oldItem = request.form.get("oldItem")
	food = ShoppingList.query.filter_by(foodList=oldItem).first()
	food.foodList= newItem
	db.session.commit()
	return redirect("/")

@app.route("/delete", methods=["POST"])
def delete():
	item = request.form.get("item")
	food = ShoppingList.query.filter_by(foodList=item).first()
	db.session.delete(food)
	db.session.commit()
	return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
