from flask import Flask, render_template, request, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

with open('templates/config.json', 'r') as file:
    params = json.load(file)["parameters"]

app = Flask(__name__)
app.secret_key = 'super secret key'
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
    price = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(50), nullable=False)
    roomsoffered = db.Column(db.String(20), nullable=False)

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
    price = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(50), nullable=False)
    days= db.Column(db.String(20), nullable=False)

class user_bookings(db.Model):
    srno = db.Column(db.Integer, primary_key=True)
    e_name = db.Column(db.String(20), unique=False, nullable=False)
    service_name = db.Column(db.String(20), unique=False, nullable=False)
    check_in = db.Column(db.String(25), nullable=False)
    days = db.Column(db.String(20), nullable=True)
    rooms = db.Column(db.String(20), nullable=True)
    from_des = db.Column(db.String(50), nullable=True)
    to_des = db.Column(db.String(20), nullable=True)
    days = db.Column(db.String(20), nullable=True)
    time = db.Column(db.String(20), nullable=True)
    people = db.Column(db.String(20), nullable=True)
    total = db.Column(db.String(20), nullable=True)
    type_of = db.Column(db.String(20), nullable=False)

@app.route("/hotelbooking/<string:srno>",methods=["GET","POST"])
def hotelbooking(srno):
    if "users" in session:
        if request.method=="POST":
            no_rooms=request.form.get("rooms")
            check_in=request.form.get("checkin")
            days=request.form.get("days")
            hotel = hotelsdetails.query.filter_by(srno=srno).first()
            hotel_name=hotel.hotelname
            from_des=hotel.area
            total=int(hotel.price)*int(no_rooms)*int(days)
            booking=user_bookings(e_name=session['users'],service_name=hotel_name,rooms=no_rooms,check_in=check_in,days=days,total=total,type_of="hotel",from_des=from_des)
            db.session.add(booking)
            db.session.commit()
    hotel = hotelsdetails.query.filter_by(srno=srno).first()
    return render_template("hotelbooking.html", hotel=hotel)

@app.route("/homestaybooking/<string:srno>",methods=["GET","POST"])
def homestaybooking(srno):
    if "users" in session:
        if request.method == "POST":
            check_in = request.form.get("checkin")
            days = request.form.get("days")
            homestay = homestayvillas.query.filter_by(srno=srno).first()
            homestay_name=homestay.homestayname
            from_des=homestay.area
            total = int(homestay.price) * int(days)
            booking = user_bookings(e_name=session['users'], service_name=homestay_name, check_in=check_in,
                                    days=days, total=total, type_of="homestay",from_des=from_des,rooms=homestay.roomsoffered)
            db.session.add(booking)
            db.session.commit()
    homestay = homestayvillas.query.filter_by(srno=srno).first()
    return render_template("homestaybooking.html", homestay=homestay)

@app.route("/cabbook/<string:srno>",methods=["GET","POST"])
def cabbook(srno):
    if "users" in session:
        if request.method == "POST":
            days = request.form.get("days")
            print(days)
            from_des = request.form.get("from")
            to_des= request.form.get("to")
            check_in = request.form.get("checkin")
            time = request.form.get("time")
            cabs = tourcabs.query.filter_by(srno=srno).first()
            cab_name = cabs.cab_name
            booking = user_bookings(e_name=session['users'], service_name=cab_name, check_in=check_in,from_des=from_des,to_des=to_des,time=time,
                                    days=days, type_of="cabs",rooms=cabs.seats_available)
            db.session.add(booking)
            db.session.commit()
    cabs = tourcabs.query.filter_by(srno=srno).first()
    return render_template("cabbook.html", cab=cabs)

@app.route("/tourpackbook/<string:srno>",methods=["GET","POST"])
def tourpackbook(srno):
    if request.method == "POST":
        people = request.form.get("people")
        check_in = request.form.get("checkin")
        time = request.form.get("time")
        tours = tourpackages.query.filter_by(srno=srno).first()
        days=tours.days
        tour_name = tours.tourname
        from_des=tours.area
        total=int(tours.price)*int(people)
        booking = user_bookings(e_name=session['users'], service_name=tour_name, check_in=check_in, time=time,
                                people=people, type_of="tourpack",total=total,days=days,from_des=from_des)
        db.session.add(booking)
        db.session.commit()

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
        room_type = request.form.get('room_type')
        hotels = hotelsdetails.query.filter_by(type=room_type)
    else:
        hotels = hotelsdetails.query.filter()

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
    session.pop('user',None)
    return redirect("/login")

@app.route("/logout_user")
def logout_user():
    session.pop('users',None)
    return redirect("/login")

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
    elif 'users' in session:
        logged_user=session['users']
        print(logged_user)
        login_user=signindetails.query.filter_by(email=logged_user).first()
        bookings=user_bookings.query.filter_by(e_name=session["users"])
        return render_template("userdashboard.html", params=params, invalid="False",user_data=login_user,details_wanted=bookings)
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
                    logged_user=signindetails.query.filter_by(email=user_details).first()
                    return render_template("userdashboard.html",invalid="False", params=params,user_data=logged_user)

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

@app.route("/delete_hotel/<string:srno>", methods=['GET', 'POST'])
def delete_hotel(srno):
    if 'user' in session and session['user'] == params["admin_user"]:
        hotel = hotelsdetails.query.filter_by(srno=srno).first()
        db.session.delete(hotel)
        db.session.commit()
    return redirect("/login")

@app.route("/delete_homestay/<string:srno>", methods=['GET', 'POST'])
def delete_homestay(srno):
    if 'user' in session and session['user'] == params["admin_user"]:
        homestay = homestayvillas.query.filter_by(srno=srno).first()
        db.session.delete(homestay)
        db.session.commit()
    return redirect("/login")

@app.route("/delete_tour/<string:srno>", methods=['GET', 'POST'])
def delete_tour(srno):
    if 'user' in session and session['user'] == params["admin_user"]:
        tours = tourpackages.query.filter_by(srno=srno).first()
        db.session.delete(tours)
        db.session.commit()
    return redirect("/login")

@app.route("/delete_cab/<string:srno>", methods=['GET', 'POST'])
def delete_cab(srno):
    if 'user' in session and session['user'] == params["admin_user"]:
        cabes = tourcabs.query.filter_by(srno=srno).first()
        db.session.delete(cabes)
        db.session.commit()
    return redirect("/login")

@app.route("/delete_user/<string:srno>", methods=['GET', 'POST'])
def delete_user(srno):
    if 'user' in session and session['user'] == params["admin_user"]:
        users = signindetails.query.filter_by(srno=srno).first()
        db.session.delete(users)
        db.session.commit()
    return redirect("/login")

@app.route("/delete_booking/<string:srno>", methods=['GET', 'POST'])
def delete_booking(srno):
    if 'users' in session :
        details = user_bookings.query.filter_by(srno=srno).first()
        db.session.delete(details)
        db.session.commit()
    return redirect("/login")

app.run(debug=True)
