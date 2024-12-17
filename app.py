import os

from flask import Flask, render_template, redirect, request, Response
from extensions import db
from models import User, Education
from werkzeug.utils import secure_filename

secret_key = os.urandom(32)


def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = secret_key

    db.init_app(app)

    # Создаем таблицы здесь, внутри контекста приложения
    with app.app_context():
        db.create_all()

    return app


app = create_app()


@app.route('/create', methods=['GET', 'POST'])
def create_user_and_education():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        city = request.form['city']

        pic = request.files["pic"]
        filename = secure_filename(pic.filename)
        mimetype = pic.mimetype

        user = User(name=name, age=age, city=city, pic=pic.read(), filename=filename, mimetype=mimetype)

        education = Education(institution=request.form['education_institution'],
                              graduation_year=request.form['graduation_year'],
                              link=request.form['link'],
                              user=user)


        user.education.append(education)
        try:
            db.session.add(user)
            db.session.commit()
            return redirect("/")
        except:
            return 'При добавлении поста произошла ошибка'
    else:
        return render_template("create.html")


@app.route("/<int:id>")
def get_img(id):
    pic = User.query.filter_by(id=id).first()
    if not pic:
        return 'Нет изображения с таким id', 404

    return Response(pic.pic, mimetype=pic.mimetype)

@app.route("/profile/<int:id>")
def posts_detail(id):
    user = User.query.get(id)
    users = User.query.all()
    educations = user.education.all() if user else None
    return render_template('index.html', user=user, educations=educations, users=users)


@app.route("/")
def index():
    user = User.query.first()
    users = User.query.all()
    educations = user.education.all() if user else None
    return render_template('index.html', user=user, educations=educations, users=users)


if __name__ == "__main__":
    app.run(debug=True)
