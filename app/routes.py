from random import choice

from flask import flash, jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from app import UserManagement, app, bcrypt, db, login_manager

# مسیر ثبت‌نام کاربران جدید
@app.route('/register', methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    if request.method == "POST":
        # گرفتن اطلاعات از فرم ثبت‌نام
        fname = request.form["fname"]
        lname = request.form["lname"]
        grade = request.form["grade"]
        username = request.form["username"]
        password = request.form["password"]

        # بررسی کامل بودن همه فیلدها
        if not fname or not lname or not grade or not username or not password:
            flash("پر کردن تمام فیلدها اجباری هست!", "danger")
            return redirect(url_for('register'))

        # بررسی تطابق گذرواژه و تکرار آن
        re_password = request.form["reppass"]
        if password != re_password:
            flash("گذرواژه و تکرار گذرواژه یکسان نیست!", "danger")
            return redirect(url_for('register'))

        # هش کردن گذرواژه
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # اضافه کردن کاربر به دیتابیس
        done = db.users.add_user(username, hashed_password, fname, lname, int(grade))
        done = db.rocket.add_user_rocket(user_id=db.users.get_user_id(username))
        done = db.user_state.add_user_state(user_id=db.users.get_user_id(username), planet_id=1)

        if done:
            flash("ثبت‌نام با موفقیت انجام شد!", "success")
            return redirect(url_for('login'))
        else:
            flash("خطا در ثبت‌نام، لطفا دوباره امتحان کنید.", "danger")
            return redirect(url_for('register'))

    return render_template('register.html')

# بارگذاری اطلاعات کاربر برای مدیریت نشست
@login_manager.user_loader
def load_user(user_id):
    return UserManagement(user_id)

# مسیر ورود کاربران
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    if request.method == "POST":
        # گرفتن نام کاربری و گذرواژه
        username = request.form["username"]
        password = request.form["password"]
        uid = db.users.get_user_id(username)

        # بررسی وجود کاربر
        if uid == 0:
            flash(' مطمئن هستی قبلا ثبت نام کردی؟!', 'warning')
            return redirect(url_for('login'))

        # بررسی درستی گذرواژه
        user = db.users.get_user(uid)
        if bcrypt.check_password_hash(user["password"], password):
            login_user(UserManagement(uid), remember=True)
            db.users.update_user_last_login(uid)
            return redirect(url_for('home'))
        else:
            flash('رمزعبور صحیح نیست!!', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html')

# مسیر خروج از حساب کاربری
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

# صفحه خانه (نیاز به ورود دارد)
@app.route('/')
@login_required
def home():
    return render_template('index.html')

# صفحه کهکشان من
@app.route('/my-galaxy')
@login_required
def galaxy():
    all_planets = db.planet.get_all_planets_basic_info()
    user_planet_id = db.user_state.get_user_planet_id(current_user.id)
    user_planet_info = db.planet.get_planet_by_id(user_planet_id)

    # تعیین سیاره فعال کاربر
    for planet in all_planets:
        planet['active'] = planet['name'] == user_planet_info['name']

    planet_info = {
        'name': user_planet_info['name'],
        'desc': user_planet_info['desc'],
        'video': user_planet_info['video'],
        'img': user_planet_info['image']
    }
    return render_template('galaxy.html', planets_list=reversed(all_planets), planet_info=planet_info)

# مسیر انجام مأموریت
@app.route('/mission')
@login_required
def mission():
    is_solve_puzzle, is_solve_test = db.user_state.get_user_solve_status(current_user.id)
    current_planet_id = db.user_state.get_user_planet_id(current_user.id)

    # در صورت حل آزمون، رفتن به سیاره بعدی
    if is_solve_test:
        next_planet = current_planet_id + 1
        if next_planet > 4:
            next_planet = 4
        db.user_state.update_user_planet(current_user.id, next_planet)
        return redirect(url_for('galaxy'))

    # اگر معما حل نشده باشد، به صفحه پازل هدایت شود
    if not is_solve_puzzle:
        return redirect(url_for('puzzle'))
    else:
        return redirect(url_for('exam'))

# نمایش پازل‌ها برای سیاره جاری
@app.route('/puzzle')
@login_required
def puzzle():
    is_solve_puzzle, _ = db.user_state.get_user_solve_status(current_user.id)
    current_planet_id = db.user_state.get_user_planet_id(current_user.id)
    
    if is_solve_puzzle:
        return redirect(url_for('exam'))

    # انتخاب تصادفی یک محتوا به عنوان جایزه
    contents = db.gift_content.get_contents_by_planet(current_planet_id)
    gift_content = choice(contents) if contents else None
    return render_template('puzzle.html', gift_content=gift_content)

# نمایش آزمون برای سیاره فعلی
@app.route('/exam')
@login_required
def exam():
    db.user_state.update_user_puzzle_solve_status(current_user.id, True)
    current_planet_id = db.user_state.get_user_planet_id(current_user.id)
    questions = db.exam.get_exam_questions(current_planet_id)
    teach_note = db.exam.get_teach_note(current_planet_id)
    money = db.rocket.get_user_money(current_user.id)

    return render_template('exam.html', questions=questions, money=money, note=teach_note)

# بررسی پاسخ‌های ارسال‌شده از سمت کاربر
@app.route('/check_exam', methods=['POST'])
def check_exam():
    current_planet_id = db.user_state.get_user_planet_id(current_user.id)
    correct_answers = db.exam.get_correct_answers(current_planet_id)
    data = request.json  # گرفتن پاسخ‌ها از فرانت‌اند

    # محاسبه امتیاز
    score = sum(1 for q, ans in data.items() if correct_answers.get(q) == int(ans))

    if score > 9:
        # افزایش سکه در صورت قبولی
        money = db.rocket.get_user_money(current_user.id)
        db.rocket.update_user_money(current_user.id, money + 50)
        db.user_state.update_user_puzzle_solve_status(current_user.id, False)
        next_planet = current_planet_id + 1
        if next_planet > 4:
            next_planet = 4
        db.user_state.update_user_planet(current_user.id, next_planet)

    return jsonify({"score": score})

# نمایش وضعیت سفینه کاربر
@app.route('/my-rocket')
def my_rocket():
    user_id = current_user.id
    money = db.rocket.get_user_money(user_id)
    rocket_abilities = db.rocket.get_user_rocket_features(user_id)

    # بررسی ویژگی‌های فعال سفینه
    cold_trip = rocket_abilities.get('cold_trip', False)
    atomic_fuel = rocket_abilities.get('atomic_fuel', False)
    flying_motor = rocket_abilities.get('flying_motor', False)
    titanium_body = rocket_abilities.get('titanium_body', True)

    return render_template(
        'my_rocket.html',
        money=money,
        cold_trip=cold_trip,
        atomic_fuel=atomic_fuel,
        flying_motor=flying_motor,
        titanium_body=titanium_body
    )

# نمایش فروشگاه
@app.route('/store')
def store():
    return render_template('store.html')

# خرید آیتم از فروشگاه
@app.route('/purchase', methods=['POST'])
def purchase():
    user_id = current_user.id
    money = db.rocket.get_user_money(user_id)
    data = request.json
    item = data.get('item')
    cost = int(data.get('cost', 0))

    if money >= cost:
        money -= cost

        # اعمال ویژگی‌های خریداری‌شده روی سفینه
        if item == "سفر در سرما":
            db.rocket.update_rocket_feature(user_id, "cold_trip", True)
        if item == "سوخت اتمی":
            db.rocket.update_rocket_feature(user_id, "atomic_fuel", True)
        if item == "موتور پرنده":
            db.rocket.update_rocket_feature(user_id, "flying_motor", True)
        if item == "بدنه تیتانیومی":
            db.rocket.update_rocket_feature(user_id, "titanium_body", True)

        db.rocket.update_user_money(user_id, money)
        return jsonify({'success': True, 'message': f'قابلیت {item} به سفینت اضافه شد، میتونی بعد از بستن این پیام از منوی بالا بری سفینت رو ببینی!'})
    else:
        return jsonify({'success': False, 'message': 'سکه کافی نداری! ❌'})

# درباره ما
@app.route('/about')
def about():
    return render_template('about.html')

# تماس با ما
@app.route('/contact')
def contact():
    return render_template('contact.html')
