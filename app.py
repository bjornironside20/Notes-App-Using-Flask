from flask import Flask
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from flask import redirect,request,url_for
from datetime import datetime


app = Flask(__name__)


# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)

class Note(db.Model):
    __tablename__ = "notes"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    db.create_all()


@app.route("/")
def indexpage():
    notes = Note.query.all()
    return render_template("index.html", notes = notes)


@app.route("/add",methods=["GET", "POST"])
def addnotes():
    if request.method == "POST":
        title = request.form.get("title")
        content = request.form.get("content")

        new_note = Note(title=title, content=content)

        db.session.add(new_note)
        db.session.commit()

        return redirect(url_for("indexpage"))  # your home route
    return render_template("add.html")



@app.route("/delete/<int:id>", methods=["POST"])
def delete_note(id):
    note = Note.query.get_or_404(id)

    db.session.delete(note)
    db.session.commit()

    return redirect(url_for("indexpage"))




@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_note(id):
    note = Note.query.get_or_404(id)

    if request.method == "POST":
        note.title = request.form.get("title")
        note.content = request.form.get("content")

        db.session.commit()

        return redirect(url_for("indexpage"))

    return render_template("edit.html", note=note)




if __name__ == "__main__":
    app.run(debug=True)



