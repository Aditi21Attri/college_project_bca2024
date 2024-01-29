from flask import Flask, render_template, request, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json


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
    description = db.Column(db.String(300), nullable=False)


class homestayvillas(db.Model):
    srno = db.Column(db.Integer, primary_key=True)
    homestayname = db.Column(db.String(20), unique=False, nullable=False)
    area = db.Column(db.String(25), nullable=False)
    image_src = db.Column(db.String(20), nullable=False)
    price = db.Column(db.String(20), nullable=True)
    description = db.Column(db.String(50), nullable=True)
    roomsoffered = db.Column(db.String(20), nullable=True)

class tourcabs(db.Model):
    srno = db.Column(db.Integer, primary_key=True)
    cab_name = db.Column(db.String(20), unique=False, nullable=False)
    cab_type = db.Column(db.String(25), nullable=False)
    price = db.Column(db.String(20), nullable=False)
    seats_available= db.Column(db.String(20), nullable=False)
    cab_description = db.Column(db.String(300), nullable=False)
    image_src= db.Column(db.String(300), nullable=False)

class tourpackages(db.Model):
    srno = db.Column(db.Integer, primary_key=True)
    tourname = db.Column(db.String(20), unique=False, nullable=False)
    area = db.Column(db.String(25), nullable=False)
    image_src = db.Column(db.String(20), nullable=False)
    price = db.Column(db.String(20), nullable=True)
    description = db.Column(db.String(50), nullable=True)
    days= db.Column(db.String(20), nullable=True)

@app.route("/hotelbooking/<string:srno>")
def hotelbooking(srno):
    hotel = hotelsdetails.query.filter_by(srno=srno).first()
    return render_template("hotelbooking.html", hotel=hotel)

@app.route("/homestaybooking/<string:srno>")
def homestaybooking(srno):
    homestay = homestayvillas.query.filter_by(srno=srno).first()
    return render_template("homestaybooking.html", homestay=homestay)

@app.route("/cabbook/<string:srno>")
def cabbook(srno):
    cabs = tourcabs.query.filter_by(srno=srno).first()
    return render_template("cabbook.html", cab=cabs)

@app.route("/tourpackbook/<string:srno>")
def tourpackbook(srno):
    tours = tourpackages.query.filter_by(srno=srno).first()
    return render_template("tourpackbook.html", tour=tours)

@app.route("/register.html", methods={'GET', 'POST'})
def register():
    if request.method == "POST":
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        entry = signindetails(name=name, password=password, email=email, date=datetime.now(), type_of="users")
        db.session.add(entry)
        db.session.commit()

    return render_template("register.html")


@app.route("/hotel", methods={'GET', 'POST'})
def hotel():
    if request.method == "POST":
        destination = request.form.get('destination')
        room_type = request.form.get('room_type')
        print("des:" + destination)
        print("loc:" +room_type)
        if destination != "none" and room_type != "none":
            hotels = hotelsdetails.query.filter_by(type=room_type, area=destination)
        elif room_type != "none" and destination=="none" :
            hotels = hotelsdetails.query.filter_by(type=room_type)
        elif destination != "none" and room_type=="none":
            hotels = hotelsdetails.query.filter_by(area=destination)
        else:
            hotels = hotelsdetails.query.filter()
    else:
        hotels = hotelsdetails.query.filter()
    return render_template("hotel.html", hotels=hotels)


@app.route("/homestay", methods={'GET', 'POST'})
def homestayVillas():
    if request.method == "POST":
        destination = request.form.get('destination')
        if destination=="none":
            homestays = homestayvillas.query.filter()
        else:
            homestays = homestayvillas.query.filter_by(area=destination)
    else:
        homestays = homestayvillas.query.filter()
    return render_template("homestays.html", homestays=homestays)

@app.route("/cabs", methods={'GET', 'POST'})
def cabs():
    cab_all = tourcabs.query.all()
    return render_template("cabs.html", cabes=cab_all)

@app.route("/tour", methods={'GET', 'POST'})
def tour():
    if request.method == "POST":
        destination = request.form.get('destination')
        if destination=="none":
            tours = tourpackages.query.filter()
        else:
            tours = tourpackages.query.filter_by(area=destination)
    else:
        tours = tourpackages.query.all()
    return render_template("tour.html", tours=tours)

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
    if 'user' in session and session['user'] == params["admin_user"]:
        session.pop('user',None)
        res=app.make_response(render_template("login"))
        res.set_cookie('user',expires=0)
    return res


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
            elif details_of == "cabs":
                cab = tourcabs.query.filter()
                details_given = 'True'
                return render_template("adminlogin.html", details_wanted=cab, params=params,
                                       details_given=details_given, details_type="cabs")

            elif details_of == "signindetails":
                users = signindetails.query.filter()
                details_given = 'True'
                return render_template("adminlogin.html", details_wanted=users, params=params,
                                       details_given=details_given, details_type="users")
            elif details_of == "tourpackages":
                tours = tourpackages.query.filter()
                details_given = 'True'
                return render_template("adminlogin.html", details_wanted=tours, params=params,
                                       details_given=details_given, details_type="tourpackages")

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
            return render_template("adminlogin.html", params=params,invalid="False")


        elif user_details!="" and user_pass!="":
            users = signindetails.query.filter()
            for user in users:
                if user_details == user.email and user_pass == user.password:
                    session["users"]=user_details
                    return render_template("userdashboard.html",invalid="False")

        else:
            return render_template("login.html",params=params,invalid="True")

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
            description = request.form.get('description')
            image_src = request.form.get('file_path')
            if srno == "0":
                hotel_slug = "hotel" + hname
                hotel_d = hotelsdetails(hotelname=hname, area=harea, price=cost, type=hotel_type,
                                        hotel_slugs=hotel_slug, image_src=image_src, description=description,
                                        type_of="hotels")
                db.session.add(hotel_d)
                db.session.commit()
            else:
                hotel = hotelsdetails.query.filter_by(srno=srno).first()
                hotel.hotelname = hname
                hotel.area = harea
                hotel.price = cost
                hotel.type = hotel_type
                hotel.image_src = image_src
                hotel.description = description
                hotel.hotel_slugs = "hotel_" + hname
                db.session.commit()
                return redirect("/uploadhotels/" + srno)
        hotels = hotelsdetails.query.filter_by(srno=srno).first()
        return render_template("uploadhotels.html", hotel=hotels, is_new=True, is_old=True)


@app.route("/uploadhomestay/<string:srno>", methods=['GET', 'POST'])
def uploadhomesstay(srno):
    if 'user' in session and session['user'] == params["admin_user"]:
        if request.method == "POST":
            hname = request.form.get('home_name')
            harea = request.form.get('location')
            cost = request.form.get('price')
            image_src = request.form.get('file_path')
            description = request.form.get('description')
            rooms = request.form.get('rooms_offered')
            if srno == "0":
                home_stay = homestayvillas(homestayname=hname,area=harea,price=cost,description=description,image_src=image_src,roomsoffered=rooms)
                db.session.add(home_stay)
                db.session.commit()

            else:
                homes = homestayvillas.query.filter_by(srno=srno).first()
                homes.homestayname = hname
                homes.area = harea
                homes.price = cost
                homes.description = description
                homes.image_src= image_src
                homes.roomsffered=rooms
                db.session.commit()
                return redirect("/uploadhomestay/" + srno)
        homes = homestayvillas.query.filter_by(srno=srno).first()
        return render_template("uploadhomes.html", home=homes)

@app.route("/uploadcabs/<string:srno>", methods=['GET', 'POST'])
def uploadcabs(srno):
    if 'user' in session and session['user'] == params["admin_user"]:
        if request.method == "POST":
            cab_name = request.form.get('cab_name')
            cab_type =request.form.get('ctype')
            price = request.form.get('price')
            image_src=request.form.get('file_path')
            seats_available = request.form.get('seats')
            cab_description = request.form.get('description')
            if srno == "0":
                cab=tourcabs(cab_name=cab_name,cab_type=cab_type,price=price,image_src=image_src,seats_available=seats_available,cab_description=cab_description)
                db.session.add(cab)
                db.session.commit()

            else:
                cab = tourcabs.query.filter_by(srno=srno).first()
                cab.cab_name = cab_name
                cab.cab_type=cab_type
                cab.cab_description=cab_description
                cab.price=price
                cab.image_src=image_src
                cab.seats_available=seats_available
                db.session.commit()
                return redirect("/uploadcabs/" + srno)
        cab = tourcabs.query.filter_by(srno=srno).first()
        return render_template("uploadcabs.html", cab=cab)

@app.route("/uploadtourpack/<string:srno>", methods=['GET', 'POST'])
def uploadtourpack(srno):
    if 'user' in session and session['user'] == params["admin_user"]:
        if request.method == "POST":
            tour_name = request.form.get('tour_name')
            area =request.form.get('area')
            price = request.form.get('price')
            image_src=request.form.get('file_path')
            days = request.form.get('days')
            tour_description = request.form.get('description')
            if srno == "0":
                tour=tourpackages(tourname=tour_name,area=area,price=price,image_src=image_src,days=days,description=tour_description)
                db.session.add(tour)
                db.session.commit()

            else:
                tours = tourpackages.query.filter_by(srno=srno).first()
                tours.tourname = tour_name
                tours.area=area
                tours.description=tour_description
                tours.price=price
                tours.image_src=image_src
                tours.days=days
                db.session.commit()
                return redirect("/uploadtourpack/" + srno)
        tours = tourpackages.query.filter_by(srno=srno).first()
        return render_template("uploadtourpack.html", tour=tours)



@app.route("/delete/<string:srno>", methods=['GET', 'POST'])
def delete_hotel(srno):
    if 'user' in session and session['user'] == params["admin_user"]:
        hotel = hotelsdetails.query.filter_by(srno=srno).first()
        db.session.delete(hotel)
        db.session.commit()
    return redirect("/login")
@app.route("/adminlogin", methods=['GET', 'POST'])
def delete_hotel():
    return render_template("adminlogin.html")

app.run(debug=True)
