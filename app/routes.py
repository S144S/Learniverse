from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

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
    current_planet_name = 'زمین'
    current_planet_desc = 'زمین همون جاییه که توش زندگی می‌کنیم، سیاره‌ای پر از دریاها، کوه‌ها و جنگل‌های سرسبز که هوای مناسب برای نفس کشیدن داره. اینجا خونه‌ی میلیون‌ها موجود زنده‌ست، از ریزترین باکتری‌ها گرفته تا بزرگ‌ترین نهنگ‌ها. آدم‌ها روی زمین شهر ساختن، تکنولوژی پیشرفت دادن و مدام دارن رازهای جدیدی درباره‌ش کشف می‌کنن. با اینکه خیلی چیزا رو درباره‌ش می‌دونیم، ولی هنوز کلی ماجراجویی و کشف جدید تو دل این سیاره منتظر ماست!'
    # خورشید قلب تپنده‌ی منظومه شمسیه! یه توپ آتشین غول‌پیکر که با نور و گرماش به زمین و بقیه‌ی سیاره‌ها زندگی می‌بخشه. این ستاره‌ی داغ از گازهای هیدروژن و هلیوم ساخته شده و همیشه در حال فوران و انفجاره. بدون خورشید، روز و شب بی‌معنی می‌شدن و زمین یه سیاره‌ی یخ‌زده بود. خلاصه که این غول آتشین حسابی سرنوشت ما رو تو دستاش داره!
    # عطارد، کوچیک‌ترین و سریع‌ترین سیاره‌ی منظومه شمسیه! این فسقلی انقدر به خورشید نزدیکه که دماش تو روز به حدی می‌رسه که آهن رو ذوب می‌کنه، ولی شب‌ها یخ می‌زنه. هیچ جوی برای حفظ گرما نداره، برای همین بین روز و شبش یه اختلاف دمای عجیب‌غریب هست. یه دور کامل دور خورشید رو فقط تو ۸۸ روز تموم می‌کنه، پس تو تقویم عطارد، سال خیلی سریع‌تر از زمین می‌گذره!
    # اگه فکر می‌کنی زمین گرمه، زهره رو ببین! این سیاره‌ی درخشان که به “خواهر زمین” معروفه، یه جهنم واقعی به حساب میاد. جو فوق‌العاده ضخیمش مثل یه پتو گرما رو تو خودش نگه می‌داره و باعث می‌شه دماش حتی از عطارد هم بیشتر بشه! بارون‌های اسیدی و طوفان‌های وحشتناک هم باعث شده هیچ شانسی برای زندگی روی زهره نباشه. خلاصه که ظاهرش قشنگه، ولی اصلاً جای زندگی نیست!
    current_planet_video = 'https://www.aparat.com/video/video/embed/videohash/uog9690/vt/frame'
    current_planet_img = 'earth2.png'
    planet_info = {
        'name': current_planet_name,
        'desc': current_planet_desc,
        'video': current_planet_video,
        'img': current_planet_img
    }
    return render_template('galaxy.html', planet_info=planet_info)

@app.route('/mission')
def mission():
    return render_template('mission.html')

# @app.route('/planet')
# def planet():
#     return render_template('planet.html')
