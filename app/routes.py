from flask import flash, redirect, render_template, request, url_for, jsonify
from flask_login import current_user, login_required, login_user, logout_user

from random import choice

from app import UserManagement, app, bcrypt, db, login_manager


@app.route('/register', methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if request.method == "POST":
        fname = request.form["fname"]
        lname = request.form["lname"]
        grade = request.form["grade"]
        username = request.form["username"]
        password = request.form["password"]
        if not fname or not lname or not grade or not username or not password:
            flash("پر کردن تمام فیلدها اجباری هست!", "danger")
            return redirect(url_for('register'))
        re_password = request.form["reppass"]
        if password != re_password:
            flash("گذرواژه و تکرار گذرواژه یکسان نیست!", "danger")
            return redirect(url_for('register'))
        # Hash password
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        done = db.users.add_user(username, hashed_password, fname, lname, int(grade))
        done = db.user_state.add_user_state(db.users.get_user_id(username), 1)
        if done:
            flash("ثبت‌نام با موفقیت انجام شد!", "success")
            return redirect(url_for('login'))
        else:
            flash("خطا در ثبت‌نام، لطفا دوباره امتحان کنید.", "danger")
            return redirect(url_for('register'))
    return render_template('register.html')

@login_manager.user_loader
def load_user(user_id):
    return UserManagement(user_id)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        uid = db.users.get_user_id(username)
        if uid == 0:
            flash(' مطمئن هستی قبلا ثبت نام کردی؟!', 'warning')
            return redirect(url_for('login'))
        user = db.users.get_user(uid)
        if bcrypt.check_password_hash(user["password"], password):
            login_user(UserManagement(uid), remember=True)
            db.users.update_user_last_login(uid)
            return redirect(url_for('home'))
        else:
            flash('رمزعبور صحیح نیست!!', 'danger')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def home():
    return render_template('index.html')

@app.route('/my-galaxy')
@login_required
def galaxy():
    all_planets = db.planet.get_all_planets_basic_info()
    user_planet_id = db.user_state.get_user_planet_id(current_user.id)
    user_planet_info = db.planet.get_planet_by_id(user_planet_id)
    
    for planet in all_planets:
        planet['active'] = planet['name'] == user_planet_info['name']

    planet_info = {
        'name': user_planet_info['name'],
        'desc': user_planet_info['desc'],
        'video': user_planet_info['video'],
        'img': user_planet_info['image']
    }
    return render_template('galaxy.html', planets_list=reversed(all_planets), planet_info=planet_info)

@app.route('/mission')
def mission():
    is_solve_puzzle, is_solve_test = db.user_state.get_user_solve_status(current_user.id)
    current_planet_id = db.user_state.get_user_planet_id(current_user.id)
    if is_solve_test:
        db.user_state.update_user_planet(current_user.id, current_planet_id + 1)
        return redirect(url_for('galaxy'))
    if not is_solve_puzzle:
        return redirect(url_for('puzzle'))
    else:
        return redirect(url_for('exam'))


@app.route('/puzzle')
def puzzle():
    is_solve_puzzle, _ = db.user_state.get_user_solve_status(current_user.id)
    current_planet_id = db.user_state.get_user_planet_id(current_user.id)
    if is_solve_puzzle:
        return redirect(url_for('exam'))
    contents = db.gift_content.get_contents_by_planet(current_planet_id)
    gift_content = choice(contents) if contents else None
    return render_template('puzzle.html', gift_content=gift_content)

@app.route('/exam')
def exam():
    # TODO: Get user money and questions from db.
    # TODO: Update is_solve_puzzle from db.
    money = 10
    questions = [
        {"question": "حاصل عبارت ۳ + ۵ × ۲ کدام است؟", "options": ["۱۶", "۱۳", "۱۰", "۸"]},
        {"question": "کدام یک عدد اول است؟", "options": ["۱۵", "۲۳", "۲۷", "۳۹"]},
        {"question": "چه عددی هم مضرب ۳ است و هم مضرب ۴؟", "options": ["۱۲", "۱۵", "۱۸", "۲۴"]},
        {"question": "کدام گزینه مقدار عددی کسر ۳/۴ را به درستی نمایش می‌دهد؟", "options": ["۰.۲۵", "۰.۵", "۰.۷۵", "۱"]},
        {"question": "مساحت یک مربع با ضلع ۶ سانتی‌متر چقدر است؟", "options": ["۱۲", "۱۸", "۲۴", "۳۶"]},
        {"question": "چه عددی بین ۲۵ و ۳۵، مضرب ۵ است؟", "options": ["۲۶", "۲۷", "۳۰", "۳۳"]},
        {"question": "حاصل تفریق ۸۵ از ۱۲۳ چیست؟", "options": ["۳۸", "۴۸", "۵۸", "۶۸"]},
        {"question": "زاویه قائمه چند درجه است؟", "options": ["۴۵", "۶۰", "۹۰", "۱۸۰"]},
        {"question": "کدام گزینه برابر با ۴۵٪ از ۲۰۰ است؟", "options": ["۷۰", "۸۰", "۹۰", "۱۰۰"]},
        {"question": "اگر محیط یک مستطیل ۲۰ سانتی‌متر و طول آن ۶ سانتی‌متر باشد، عرض آن چقدر است؟", "options": ["۲", "۴", "۵", "۶"]},
    ]
    return render_template('exam.html', questions=questions, money=money)

@app.route('/check_exam', methods=['POST'])
def check_exam():
    # TODO: Get right answers from db.
    correct_answers = {
        "q1": 1, "q2": 3, "q3": 2, "q4": 4, "q5": 1,
        "q6": 2, "q7": 3, "q8": 1, "q9": 4, "q10": 2
    }
    data = request.json  # Get submitted answers from frontend
    score = sum(1 for q, ans in data.items() if correct_answers.get(q) == int(ans))
    
    return jsonify({"score": score})

@app.route('/my-rocket')
def my_rocket():
    # TODO: Get below items from db.
    money = 350
    cold_trip = False
    atomic_fuel = False
    flying_motor = False
    titanium_body = True
    return render_template(
        'my_rocket.html',
        money=money,
        cold_trip=cold_trip,
        atomic_fuel=atomic_fuel,
        flying_motor=flying_motor,
        titanium_body=titanium_body
    )

@app.route('/store')
def store():
    return render_template('store.html')


@app.route('/purchase', methods=['POST'])
def purchase():
    # TODO: Get user money from db.
    money = 100
    data = request.json
    item = data.get('item')
    cost = int(data.get('cost', 0))
    # TODO: Update is_cold_trip, etc on db.

    if money >= cost:
        money -= cost
        return jsonify({'success': True, 'message': f'قابلیت {item} به سفینت اضافه شد، میتونی بعد از بستن این پیام از منوی بالا بری سفینت رو ببینی!'})
    else:
        return jsonify({'success': False, 'message': 'سکه کافی نداری! ❌'})

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')
