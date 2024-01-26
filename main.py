from flask import Flask, render_template, request, session, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json
import os
from werkzeug.utils import secure_filename
import time


with open('templates/config.json', 'r') as file:
    params = json.load(file)["parameters"]

app = Flask(__name__)
app.secret_key = 'super secret key'

app.config["Uploader_url"] = params["file_save_url"]

DATABSE_URI = 'mysql+mysqlconnector://{user}:{password}@{server}/{database}'.format(user='root', password='',
                                                                                    server='localhost',
                                                                                    database='tourandtravel')

app.config["SQLALCHEMY_DATABASE_URI"] = params['local_url']
db = SQLAlchemy(app)


class signindetails(db.Model):
    srno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=False, nullable=False)
    email = db.Column(db.String(25), nullable=False)
    password = db.Column(db.String(20), nullable=False)
    date = db.Column(db.String(20), nullable=True)
    type_of = db.Column(db.String(20), nullable=True)


class hotelsdetails(db.Model):
    srno = db.Column(db.Integer, primary_key=True)
    hotelname = db.Column(db.String(20), unique=False, nullable=False)
    area = db.Column(db.String(25), nullable=False)
    price = db.Column(db.String(20), nullable=False)
    type = db.Column(db.String(20), nullable=False)
    hotel_slugs = db.Column(db.String(20), nullable=True)
    type_of = db.Column(db.String(20), nullable=True)
    image_src = db.Column(db.String(20), nullable=True)
    description = db.Column(db.String(20), nullable=False)


class homestayvillas(db.Model):
    srno = db.Column(db.Integer, primary_key=True)
    homestayname = db.Column(db.String(20), unique=False, nullable=False)
    area = db.Column(db.String(25), nullable=False)
    image_src = db.Column(db.String(20), nullable=False)
    price = db.Column(db.String(20), nullable=True)
    description = db.Column(db.String(50), nullable=True)
    roomsoffered = db.Column(db.String(20), nullable=True)
    helpers = db.Column(db.String(50), nullable=True)


@app.route("/hotelbooking/<string:srno>")
def hotelbooking(srno):
    hotel = hotelsdetails.query.filter_by(srno=srno).first()
    return render_template("hotelbooking.html", hotel=hotel)


@app.route("/register.html", methods={'GET', 'POST'})
def register():
    if request.method == "POST":
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        entry = signindetails(name=name, password=password, email=email, date=datetime.now())
        db.session.add(entry)
        db.session.commit()

    return render_template("register.html")


@app.route("/hotel", methods={'GET', 'POST'})
def hotel():
    if request.method == "POST":
        destination = request.form.get('destination')
        no_rooms = request.form.get('no_of_rooms')
        room_type = request.form.get('room_type')
        range = request.form.get('range')
        hotels = hotelsdetails.query.filter_by(type=room_type)

    else:

        hotels = hotelsdetails.query.filter()
    print(hotels)

    return render_template("hotel.html", hotels=hotels)


@app.route("/homestay", methods={'GET', 'POST'})
def homestayVillas():
    if request.method == "POST":
        destination = request.form.get('destination')
        helper_wanted = request.form.get('helper_wanted')
        checkin = request.form.get('checkin')
        checkout = request.form.get('checkout')
        range = request.form.get('range')
        homestays = homestayvillas.query.filter_by(area=destination)
    else:
        homestays = homestayvillas.query.filter()
    print(homestays)

    return render_template("homestays.html", homestays=homestays)


@app.route("/cabbooking", methods={'GET', 'POST'})
def cabBooking():
    if request.method == "POST":
        destination = request.form.get('destination')
        no_rooms = request.form.get('no_of_rooms')
        room_type = request.form.get('room_type')
        range = request.form.get('range')
        hotels = hotelsdetails.query.filter_by(type=room_type)
    else:
        hotels = hotelsdetails.query.filter()
    print(hotels)

    return render_template("cabbook.html", hotels=hotels)


@app.route("/")
def index():

    return render_template("index.html", )


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/blog")
def blog():
    return render_template("blog.html")


@app.route("/services")
def product():
    hotels = hotelsdetails.query.filter()[0:3]
    homestays = homestayvillas.query.filter()[0:3]
    print(hotels)
    return render_template("services.html", hotels=hotels, homestays=homestays)


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/logout")
def logout():
    session.pop('user')
    return render_template("login.html")


@app.route("/login", methods=['GET', 'POST'])
def login():
    if 'user' in session and session['user'] == params["admin_user"]:
        if request.method == "POST":
            details_of = request.form.get('details_of')
            if details_of == "hotelsdetails":
                hotels = hotelsdetails.query.filter()
                details_given = 'True'
                return render_template("adminlogin.html", details_wanted=hotels, params=params,
                                       details_given=details_given, details_type="hotels")
            elif details_of == "homestayvillas":
                homestays = homestayvillas.query.filter()
                details_given = 'True'
                return render_template("adminlogin.html", details_wanted=homestays, params=params,
                                       details_given=details_given, details_type="homestays")
            elif details_of == "signindetails":
                users = signindetails.query.filter()
                details_given = 'True'
                return render_template("adminlogin.html", details_wanted=users, params=params,
                                       details_given=details_given, details_type="users")

            else:
                return render_template("login.html")

        else:

            details = 'False'

            return render_template("adminlogin.html", params=params, details_given=details)

    elif request.method == 'POST':
        user_details = request.form.get('user_name')
        user_pass = request.form.get('user_password')
        if user_details == params["admin_user"] and user_pass == params["admin_password"]:
            session['user'] = user_details
            return render_template("adminlogin.html", params=params)

        else:
            users = signindetails.query.filter()

            for user in users:
                if user_details == user.email and user_pass == user.password:
                    return render_template("userloginpage.html")
                print(user.email)

    else:
        return render_template("login.html")


@app.route("/uploadhotels/<string:srno>", methods=['GET', 'POST'])
def hoteldetails(srno):
    if 'user' in session and session['user'] == params["admin_user"]:
        if request.method == "POST":

            hname = request.form.get('hotel_name')
            harea = request.form.get('location')
            cost = request.form.get('price')
            hotel_type = request.form.get('h_type')
            f = request.files['file_path']
            f.save(os.path.join(app.config["Uploader_url"], hname + (f.filename)))
            image_src = hname + (f.filename)
            if srno == "0":
                hotel_slug = "hotel_" + hname

                hotel_d = hotelsdetails(hotelname=hname, area=harea, price=cost, type=hotel_type,
                                        hotel_slugs=hotel_slug, image_src=image_src)
                db.session.add(hotel_d)
                db.session.commit()
            else:
                hotel = hotelsdetails.query.filter_by(srno=srno).first()
                hotel.hotelname = hname
                hotel.area = harea
                hotel.price = cost
                hotel.type = hotel_type
                hotel.image_src = image_src
                hotel.hotel_slugs = "hotel_" + hname
                db.session.commit()
                return redirect("/uploadhotels/" + srno)
        hotels = hotelsdetails.query.filter_by(srno=srno).first()

        return render_template("uploadhotels.html", hotel=hotels)


@app.route("/delete/<string:srno>", methods=['GET', 'POST'])
def delete_hotel(srno):
    if 'user' in session and session['user'] == params["admin_user"]:
        hotel = hotelsdetails.query.filter_by(srno=srno).first()
        db.session.delete(hotel)
        db.session.commit()
    return redirect("/login")


app.run(debug=True)
