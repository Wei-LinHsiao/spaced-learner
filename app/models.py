from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    decks = db.relationship('Deck', backref='author', lazy='dynamic')

    def __repr__(self):
        return "User ID" + self.u_id

class Deck(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    u_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    name = db.Column(db.String(64), index=True, unique=True)
    entries = db.relationship('Entry', backref='author', lazy='dynamic')

    def __repr__(self):
        return "Deck ID " + self.id

class Entry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Do we need the u_id if we have the deck_id?
    u_id = db.Column(db.Integer, index = True)
    deck_id = db.Column(db.Integer, db.ForeignKey('deck.id'))
    e_id = db.Column(db.Integer, index = True)
    box = db.Column(db.Integer)
    level = db.Column(db.Integer)
    front_text = db.Column(db.Text)
    back_text = db.Column(db.Text)

    def __repr__(self):
        return "Entry ID " + self.id
