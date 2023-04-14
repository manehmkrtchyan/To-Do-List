from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from bs4 import BeautifulSoup

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)


@app.route("/")
def home():
    todo_list = Todo.query.all()
    return render_template("github.html", todo_list=todo_list)


@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title")
    new_todo = Todo(title=title, complete=False)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("home"))

#@app.route("/edit/<int:todo_id>", methods=["GET", "POST"])
#def edit(todo_id):
    # edit_title = request.form.get("title")
    # db.session.query(Todo).filter(Todo.id == todo_id).update({todo_id: edit_title})
    # db.session.commit()
    
    # return redirect(url_for("home"))
# def edit(todo_id):
#     if request.method == "POST":
#         edit_title = request.form.get("title")
#         todo = Todo.query.filter_by(id=todo_id).first()
#         todo.title = edit_title
#         db.session.commit()
#         return redirect(url_for("home"))



@app.route("/update/<int:todo_id>")
def update(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("home"))


@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("home"))

# @app.route("/edit/<int:todo_id>", methods=["GET", "POST"])
# def edit(todo_id):
#     with open('templates/github.html', 'r') as f:
#         html_doc = f.read()

#     soup = BeautifulSoup(html_doc, 'html.parser')
#     my_p = soup.find(id="task")
#     print(my_p)
#     if my_p is not None:
#         my_p['contenteditable'] = "true"
#     else:
#         print("element not found")
#     return redirect(url_for("home"))


# @app.route('/save', methods=['POST'])
# def save(todo_id):
#     todo_id = request.form['id']
#     todo_text = request.form['text']
#     todo_item = TodoItem.query.filter_by(id=todo_id).first()
#     todo_item.text = todo_text
#     db.session.commit()
#     return redirect('/')


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)