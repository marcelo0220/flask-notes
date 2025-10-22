from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
db = SQLAlchemy(app)

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.Text)

# --- Route principale ---
@app.route('/')
def index():
    search = request.args.get('search')
    if search:
        notes = Note.query.filter(Note.title.contains(search) | Note.content.contains(search)).all()
    else:
        notes = Note.query.all()
    return render_template('index.html', notes=notes, query=search)

# --- Ajouter une note ---
@app.route('/add', methods=['POST'])
def add_note():
    title = request.form['title']
    content = request.form['content']
    new_note = Note(title=title, content=content)
    db.session.add(new_note)
    db.session.commit()
    return redirect(url_for('index'))

# --- Supprimer une note ---
@app.route('/delete/<int:id>')
def delete_note(id):
    note = Note.query.get_or_404(id)
    db.session.delete(note)
    db.session.commit()
    return redirect(url_for('index'))

# --- Éditer une note (afficher formulaire) ---
@app.route('/edit/<int:id>')
def edit_note(id):
    note = Note.query.get_or_404(id)
    return render_template('edit.html', note=note)

# --- Mettre à jour la note (soumission du formulaire) ---
@app.route('/update/<int:id>', methods=['POST'])
def update_note(id):
    note = Note.query.get_or_404(id)
    note.title = request.form['title']
    note.content = request.form['content']
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
