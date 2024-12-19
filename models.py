from extensions import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pic = db.Column(db.String(100), nullable=False)
    filename = db.Column(db.Text, unique=True, nullable=False)
    mimetype = db.Column(db.Text, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    city = db.Column(db.String(50), nullable=False)
    education = db.relationship('Education', backref='user', lazy='dynamic')
    project = db.relationship("Project", backref='user', lazy='dynamic')

    def __repr__(self):
        return f'<User {self.name}>'


class Education(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    institution = db.Column(db.String(100), nullable=False)
    graduation_year = db.Column(db.Integer, nullable=False)
    link = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(200), nullable=False)
    project_description = db.Column(db.String(600), nullable=False)
    project_link = db.Column(db.String(200), nullable=False)
    pic = db.Column(db.String(100), nullable=False)
    filename = db.Column(db.Text, unique=True, nullable=False)
    mimetype = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
