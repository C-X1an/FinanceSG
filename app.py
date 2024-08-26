import os

from cs50 import SQL
from flask import Flask, render_template, redirect, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps

app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///financesg.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return render_template("login.html", nousername=True)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return render_template("login.html", nopassword=True)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return render_template("login.html", accounterror=True)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        if not username or not password:
            return render_template("register.html", invalid=True)
        if len(password) < 8:
            return render_template("register.html", insufficentlength=True)
        if password != confirm_password:
            return render_template("register.html", passnomatch=True)
        usernames_check = []
        for user in db.execute("SELECT username FROM users"):
            usernames_check.append(user["username"])
        if username in usernames_check:
            return render_template("register.html", nametaken=True)
        hash_password = generate_password_hash(password)
        db.execute("INSERT INTO users SET VALUES (?, ?, ?, datetime['now'])", session["user_id"], username, hash_password)
        return redirect("/")
    else:
        return render_template("register.html")

@app.route("/university", methods=["GET", "POST"])
def university():
    if request.method == "POST":
        annual_fee = float(request.form.get("annual_cost"))
        academic_years = request.form.get("academic_years")
        total_payment = (annual_fee * academic_years) - loan_amount
        if request.form.get("loan_checkbox") == True:
            loan_amount = request.form.get("loan")
            monthly_repayment = request.form.get("loan_repayment")
            loan_interest = request.form.get("loan_interest")
            while loan_amount > 0:
                total_payment += monthly_repayment
                loan_amount -= monthly_repayment
                repayment_period += 1
                if repayment_period % 12 == 0:
                    loan_amount *= ((loan_interest / 100) + 1)
            total_payment += loan_amount
        if request.form.get("scholarship_checkbox") == True:
            annual_subsidy = request.form.get("scholarship_grant")
            total_subsidy = annual_subsidy * academic_years
            total_payment -= total_subsidy
        if total_payment < 0:
            total_payment = 0
        db.execute("INSERT INTO annually VALUES (?, 'University', ?, ?)", session["user_id"], total_payment, annual_fee)
    else:
        return render_template("university.html")

@app.route("/vehicle", methods=["GET", "POST"])
def vehicle():
    if request.method == "POST":
        type = "Vehicle"
        omv = float(request.form.get("omv"))
        category = request.form.get("category")
        veh_age = request.form.get("veh_age")
        engine_capacity = request.form.get("engine_capacity")
        usage_duration = request.form.get("usage_duration")
        if category in ['A', 'B', 'E']:
            if category == 'A':
                coe = 76000
            elif category == 'B':
                coe = 97000
            elif category == 'E':
                coe = 94000
            total_cost = (omv + 350 + coe + (omv * 0.2))
            if omv <= 20000:
                total_cost += omv
            rates = [1, 1.4, 1.9, 2.5, 3.2]
            for rate in rates:
                if omv > 20000:
                    total_cost += rate * 20000
                    omv -= 20000
                else:
                    total_cost += omv * rate
                    break
            if veh_age > 3:
                total_cost += 10000
            if engine_capacity <= 600:
                total_cost += (((200 * 0.782) * 2) * usage_duration)
            elif 600 < engine_capacity <= 1000:
                total_cost += ((200 + 0.125 * (engine_capacity - 600)) * 0.782) * 2 * usage_duration
            elif 1000 < engine_capacity <= 1600:
                total_cost += (250 + 0.375 * (engine_capacity - 1000)) * 0.782 * 2 * usage_duration
            elif 1600 < engine_capacity <= 3000:
                total_cost += ((475 + 0.75) * (engine_capacity)) * 0.782 * 2 * usage_duration
            elif engine_capacity > 3000:
                total_cost += (1,525 + engine_capacity - 3000) * 0.782 * 2 * usage_duration
        else:
            coe = 9000
            total_cost = 350 + omv + (omv * 0.12)
            rates = [0.15, 0.5, 1]
            for rate in rates:
                if omv > 5000:
                    total_cost +=  (5000 * rate)
                    omv -= 5000
                else:
                    total_cost += (omv * rate)
                    break
            if engine_capacity <= 200:
                total_cost += (40 * 0.782 * 2 * usage_duration)
            elif 200 < engine_capacity <= 1000:
                total_cost += (40 + 0.15 * (engine_capacity - 200)) * 0.782 * 2 * usage_duration
            else:
                total_cost += (160 + 0.3 * (engine_capacity - 1000)) * 0.782 * 2 * usage_duration
        db.execute("INSERT INTO anually VALUES (?, ?, ?, ?)", session["user_id"], type, total_cost, (total_cost / (usage_duration * 12)))
        return redirect("/vehicle")
    else:
        return render_template("vehicle.html")

@app.route("/property", methods=["GET", "POST"])
def property():
    if request.method == "POST":
        type = "property"
        property_price = request.form.get("property_price")
        downpayment = request.form.get("downpayment")
        loan_amount = request.form.get("loan_amount")
        loan_interest = request.form.get("loan_interest")
        loan_tenure = request.form.get("loan_tenure")
        reno_cost = request.form.get("reno_cost")
        insurance = request.form.get("insurance")
        agent_fee = request.form.get("agent_fee")
        if request.form.get("bto_checkbox") == False:
            absd = request.form.get("absd")
            downpayment = request.form.get("downpayment")
        else:
            absd = 0
            downpayment = 2.5
        if not loan_tenure:
            loan_tenure = 25
        total_cost = property_price * (downpayment /100 + 1) + reno_cost + (insurance * 25) + property_price(agent_fee/100) -  loan_amount + absd
        if loan_amount > 0:
            monthly_repayable = (loan_amount * (loan_interest / 1200) * pow(1 + (loan_interest / 1200), loan_tenure * 12)) / (pow(1 + (loan_interest / 1200)) - 1)
            while loan_amount > monthly_repayable:
                loan_amount -= monthly_repayable
                loan_amount *= (1 + (loan_interest / 1200))
                total_cost += monthly_repayable
            total_cost += monthly_repayable
        monthly_cost = total_cost / (loan_tenure * 12)
        db.execute("INSERT INTO monthly VALUES (?, ?, ?, ?)", session["user_id"], type, total_cost, monthly_cost)
        return redirect("/calculated")
    else:
        return render_template("property.html")

@app.route("/salary", methods=["GET", "POST"])
def salary():
    if request.method == "POST":
        type = "salary"
        citizenships = ["Singapore Citizen", "First Year PR", "Second Year PR", "Third Year+ PR"]
        citizenship = request.form.get("citizensip")
        OW = request.form.get("salary")
        AW = request.form.get("additional_wage")
        TW = OW + AW
        age = request.form.get("age")
        if OW > 6800:
            OW = 6800
        if citizenship in citizenships:
            contribution = 0
            if citizenship == "Singapore Citizen" or citizenship == "Third Year+ PR":
                rate = [0.2, 0.16, 0.105, 0.075, 0.05]
                if age <= 55:
                    if 750 >= TW  and TW > 500:
                        contribution = 0.6 * (TW - 500)
                    elif TW > 750:
                        contribution = rate[0] * (TW)
                elif age > 55 and age <= 60:
                    if 750 >= TW  and TW > 500:
                        contribution = 0.48 * (TW - 500)
                    elif TW > 750:
                        contribution = rate[1] * TW
                elif age > 60 and age <= 65:
                    if 750 >= TW  and TW > 500:
                        contribution = 0.315 * (TW - 500)
                    elif TW > 750:
                        contribution = rate[2] * TW
                elif age > 65 and age <= 70:
                    if 750 >= TW  and TW > 500:
                        contribution = 0.225 * (TW - 500)
                    elif TW > 750:
                        contribution = rate[3] * TW
                elif age > 70:
                    if 750 >= TW  and TW > 500:
                        contribution = 0.15 * (TW - 500)
                    elif TW > 750:
                        contribution = rate[4] * TW
            elif citizenship == "First Year PR":
                rate = 0.05
                if 750 >= TW  and TW > 500:
                    contribution = 0.15 * (TW - 500)
                elif TW > 750:
                    contribution = rate * (TW)
            elif citizenship == "Second Year PR":
                rate = [0.15, 0.125, 0.075, 0.05]
                if age <= 55:
                    if 750 >= TW  and TW > 500:
                        contribution = 0.45 * (TW - 500)
                    elif TW > 750:
                        contribution = rate[0] * (TW)
                elif age > 55 and age <= 60:
                    if 750 >= TW  and TW > 500:
                        contribution = 0.375 * (TW - 500)
                    elif TW > 750:
                        contribution = rate[1] * TW
                elif age > 60 and age <= 65:
                    if 750 >= TW  and TW > 500:
                        contribution = 0.225 * (TW - 500)
                    elif TW > 750:
                        contribution = rate[2] * TW
                elif age > 65:
                    if 750 >= TW  and TW > 500:
                        contribution = 0.15 * (TW - 500)
                    elif TW > 750:
                        contribution = rate[3] * TW
            db.execute("INSERT INTO monthly VALUES (?, ?, ?, ?)", session["user_id"], type, '-', contribution)
            return redirect("/calculated")
    else:
        return render_template("salary.html")

@app.route("/income_tax", methods=["GET"])
def income_tax():
    return render_template("income_tax.html")

@app.route("/budget", methods=["GET", "POST"])
def budget():
    if request.method == "POST":
        if request.form.get("maintainance_checkbox") == True:
            inflow = int(request.form.get("income")) + int(request.form.get("maintainance"))
        else:
            inflow = int(request.form.get("income"))
        mandatory = int(request.form.get("mandatory_expenses"))
        discretionary = int(request.form.get("wants_cost"))
        savings = int(request.form.get("savings"))
        mandatory_expenses_percent = round((mandatory / inflow) * 100, 2)
        discretionary_expenses_percent = round((discretionary / inflow) * 100, 2)
        savings_percent = round((savings / inflow) * 100, 2)
        mandatory_over = False
        discretionary_over = False
        savings_under = False
        if mandatory_expenses_percent > 54.7:
            mandatory_over = True
        if discretionary_expenses_percent > 38.4:
            discretionary_over = True
        if savings_percent < 6.9:
            savings_under = True
        return render_template("budget_calculated.html", mandatory_over=mandatory_over, discretionary_over=discretionary_over, savings_under=savings_under, mandatory_expenses_percent=mandatory_expenses_percent,
                               discretionary_expenses_percent=discretionary_expenses_percent, savings_percent=savings_percent)
    else:
        return render_template("budget.html")


