from flask import Flask, render_template, request, redirect, url_for, session, flash
import sqlite3
import os
import joblib
import pandas as pd

from werkzeug.security import generate_password_hash, check_password_hash


# =========================================================
# FLASK APP
# =========================================================

app = Flask(__name__)

app.secret_key = "forgetmenot_secret_key_2026"


# =========================================================
# PROJECT PATHS
# =========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATABASE = os.path.join(BASE_DIR, "database.db")
MODEL_FILE = os.path.join(BASE_DIR, "model.pkl")


# =========================================================
# LOAD ML MODEL
# =========================================================

ml_model = None

if os.path.exists(MODEL_FILE):

    try:
        ml_model = joblib.load(MODEL_FILE)

        print("\n========================================")
        print("AI MODEL LOADED SUCCESSFULLY")
        print("========================================")
        print("Model:", MODEL_FILE)

    except Exception as e:

        print("\nERROR LOADING MODEL:")
        print(e)

else:

    print("\nWARNING: model.pkl NOT FOUND")
    print("Please run train_model.py first.")


# =========================================================
# RECOMMENDATION DATABASE
# =========================================================

RECOMMENDATIONS = {

    # ---------------- COLLEGE ----------------

    "college_study": [
        "College ID Card",
        "Notebook",
        "Textbooks",
        "Pens",
        "Pencil",
        "Water Bottle",
        "College Bag",
        "Bus Pass"
    ],

    "college_exam": [
        "College ID Card",
        "Hall Ticket",
        "Pens",
        "Pencils",
        "Eraser",
        "Calculator",
        "Water Bottle",
        "Exam Materials"
    ],

    "college_presentation": [
        "College ID Card",
        "Laptop",
        "Laptop Charger",
        "Presentation File",
        "Pen Drive",
        "Notebook",
        "Pen",
        "Water Bottle"
    ],

    "college_project": [
        "College ID Card",
        "Laptop",
        "Laptop Charger",
        "Project Files",
        "Pen Drive",
        "Notebook",
        "Extension Cable",
        "Water Bottle"
    ],


    # ---------------- SCHOOL ----------------

    "school_study": [
        "School ID Card",
        "Books",
        "Notebook",
        "Pens",
        "Pencils",
        "Eraser",
        "Water Bottle",
        "School Bag"
    ],

    "school_exam": [
        "School ID Card",
        "Hall Ticket",
        "Pens",
        "Pencils",
        "Eraser",
        "Calculator",
        "Water Bottle"
    ],

    "school_sports": [
        "Sports Shoes",
        "Sports Dress",
        "Water Bottle",
        "Towel",
        "Sports Equipment",
        "Extra Clothes"
    ],


    # ---------------- OFFICE ----------------

    "office_work": [
        "Office ID Card",
        "Laptop",
        "Laptop Charger",
        "Notebook",
        "Pen",
        "Water Bottle",
        "Office Documents"
    ],

    "office_meeting": [
        "Office ID Card",
        "Laptop",
        "Laptop Charger",
        "Meeting Documents",
        "Notebook",
        "Pen",
        "Water Bottle"
    ],

    "office_presentation": [
        "Office ID Card",
        "Laptop",
        "Laptop Charger",
        "Presentation File",
        "Pen Drive",
        "Notebook",
        "Pen"
    ],

    "office_interview": [
        "Resume",
        "ID Card",
        "Certificates",
        "Formal Clothes",
        "Pen",
        "Notebook",
        "Phone",
        "Water Bottle"
    ],


    # ---------------- GYM ----------------

    "gym_workout": [
        "Gym Shoes",
        "Workout Clothes",
        "Water Bottle",
        "Towel",
        "Headphones",
        "Gym Membership Card",
        "Extra Clothes"
    ],

    "gym_yoga": [
        "Yoga Mat",
        "Comfortable Clothes",
        "Water Bottle",
        "Towel",
        "Headband"
    ],


    # ---------------- HOSPITAL ----------------

    "hospital_appointment": [
        "Hospital Registration Card",
        "Previous Medical Reports",
        "Prescription",
        "Health Insurance Card",
        "Phone",
        "Water Bottle"
    ],

    "hospital_checkup": [
        "Hospital ID",
        "Previous Medical Reports",
        "Prescription",
        "Medical Documents",
        "Health Insurance Card",
        "Phone"
    ],

    "hospital_emergency": [
        "ID Card",
        "Medical Documents",
        "Previous Reports",
        "Emergency Contact Details",
        "Phone",
        "Phone Charger"
    ],


    # ---------------- BEACH ----------------

    "beach_relax": [
        "Water Bottle",
        "Sunglasses",
        "Sunscreen",
        "Hat",
        "Phone",
        "Power Bank",
        "Towel"
    ],

    "beach_swimming": [
        "Swimwear",
        "Towel",
        "Sunscreen",
        "Sunglasses",
        "Water Bottle",
        "Extra Clothes",
        "Waterproof Phone Pouch"
    ],

    "beach_picnic": [
        "Food",
        "Water Bottle",
        "Picnic Mat",
        "Sunscreen",
        "Sunglasses",
        "Hat",
        "Tissues",
        "Trash Bags"
    ],


    # ---------------- TRAVEL ----------------

    "travel_trip": [
        "ID Card",
        "Phone",
        "Phone Charger",
        "Power Bank",
        "Clothes",
        "Toiletries",
        "Wallet",
        "Travel Documents"
    ],

    "travel_vacation": [
        "ID Card",
        "Travel Tickets",
        "Clothes",
        "Toiletries",
        "Phone Charger",
        "Power Bank",
        "Sunscreen",
        "Wallet"
    ],

    "travel_business": [
        "ID Card",
        "Laptop",
        "Laptop Charger",
        "Business Documents",
        "Formal Clothes",
        "Wallet",
        "Phone",
        "Power Bank"
    ],

    "travel_family": [
        "ID Card",
        "Travel Tickets",
        "Clothes",
        "Toiletries",
        "Phone Charger",
        "Snacks",
        "Water Bottle",
        "Medicines"
    ],


    # ---------------- AIRPORT ----------------

    "airport_flight": [
        "Passport",
        "Flight Ticket",
        "Boarding Pass",
        "ID Card",
        "Phone",
        "Phone Charger",
        "Power Bank",
        "Wallet",
        "Travel Documents"
    ],


    # ---------------- LIBRARY ----------------

    "library_study": [
        "Library Card",
        "Books",
        "Notebook",
        "Pens",
        "Laptop",
        "Charger",
        "Water Bottle"
    ],

    "library_reading": [
        "Library Card",
        "Book",
        "Notebook",
        "Pen",
        "Reading Glasses",
        "Water Bottle"
    ],


    # ---------------- SHOPPING ----------------

    "shopping": [
        "Wallet",
        "Phone",
        "Shopping List",
        "Reusable Bag",
        "Keys",
        "Payment Card"
    ],

    "shopping_grocery": [
        "Wallet",
        "Phone",
        "Grocery List",
        "Reusable Bags",
        "Payment Card",
        "Keys"
    ],


    # ---------------- INTERVIEW ----------------

    "interview_job": [
        "Resume",
        "ID Card",
        "Certificates",
        "Formal Clothes",
        "Pen",
        "Notebook",
        "Phone",
        "Wallet"
    ]
}


# =========================================================
# DATABASE
# =========================================================

def init_db():

    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    connection.commit()

    connection.close()


init_db()


# =========================================================
# DESTINATION NORMALIZATION
# =========================================================

DESTINATION_ALIASES = {

    "college": "college",
    "school": "school",
    "office": "office",
    "gym": "gym",
    "hospital": "hospital",
    "beach": "beach",
    "travel": "travel",
    "airport": "airport",
    "library": "library",
    "shopping": "shopping",
    "interview": "interview"

}


# =========================================================
# ACTIVITY NORMALIZATION
# =========================================================

ACTIVITY_ALIASES = {

    "study": "study",
    "class": "class",
    "lecture": "lecture",

    "exam": "exam",
    "test": "test",
    "semester exam": "semester exam",
    "internal exam": "internal exam",
    "exam preparation": "exam preparation",

    "presentation": "presentation",
    "seminar": "seminar",

    "project": "project",
    "project work": "project work",

    "sports": "sports",
    "football": "football",
    "cricket": "cricket",

    "work": "work",
    "office work": "office work",

    "meeting": "meeting",
    "team meeting": "team meeting",

    "interview": "interview",
    "job interview": "job interview",
    "job": "job",

    "workout": "workout",
    "exercise": "exercise",
    "training": "training",

    "yoga": "yoga",
    "meditation": "meditation",

    "appointment": "appointment",
    "doctor appointment": "doctor appointment",

    "checkup": "checkup",
    "health checkup": "health checkup",

    "emergency": "emergency",

    "relax": "relax",
    "relaxing": "relaxing",
    "sunset": "sunset",

    "swimming": "swimming",
    "swim": "swimming",

    "picnic": "picnic",

    "trip": "trip",
    "travel": "travel",
    "road trip": "road trip",

    "vacation": "vacation",
    "holiday": "holiday",

    "business": "business",
    "business trip": "business trip",

    "family": "family",
    "family trip": "family trip",

    "flight": "flight",
    "boarding": "boarding",

    "reading": "reading",
    "read book": "read book",

    "shopping": "shopping",
    "grocery": "grocery",
    "grocery shopping": "grocery shopping"

}


# =========================================================
# LOGIN REQUIRED
# =========================================================

def login_required():

    return "user_id" in session


# =========================================================
# HOME
# =========================================================

@app.route("/")
def home():

    if not login_required():

        return redirect(url_for("login"))

    return render_template(
        "index.html",
        name=session.get("name")
    )


# =========================================================
# REGISTER
# =========================================================

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form.get(
            "name",
            ""
        ).strip()

        email = request.form.get(
            "email",
            ""
        ).strip().lower()

        password = request.form.get(
            "password",
            ""
        )

        confirm_password = request.form.get(
            "confirm_password",
            ""
        )


        # Check empty fields

        if not name or not email or not password:

            flash("Please fill in all fields.")

            return redirect(
                url_for("register")
            )


        # Check passwords

        if password != confirm_password:

            flash("Passwords do not match.")

            return redirect(
                url_for("register")
            )


        # Password length

        if len(password) < 6:

            flash(
                "Password must contain at least 6 characters."
            )

            return redirect(
                url_for("register")
            )


        connection = sqlite3.connect(
            DATABASE
        )

        cursor = connection.cursor()


        # Check existing email

        cursor.execute(
            "SELECT id FROM users WHERE email = ?",
            (email,)
        )

        existing_user = cursor.fetchone()


        if existing_user:

            connection.close()

            flash(
                "An account with this email already exists."
            )

            return redirect(
                url_for("login")
            )


        # Hash password

        hashed_password = generate_password_hash(
            password
        )


        # Save user

        cursor.execute(
            """
            INSERT INTO users
            (name, email, password)
            VALUES (?, ?, ?)
            """,
            (
                name,
                email,
                hashed_password
            )
        )


        connection.commit()

        connection.close()


        flash(
            "Registration successful! Please login."
        )

        return redirect(
            url_for("login")
        )


    return render_template(
        "register.html"
    )


# =========================================================
# LOGIN
# =========================================================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form.get(
            "email",
            ""
        ).strip().lower()

        password = request.form.get(
            "password",
            ""
        )


        if not email or not password:

            flash(
                "Please enter email and password."
            )

            return redirect(
                url_for("login")
            )


        connection = sqlite3.connect(
            DATABASE
        )

        cursor = connection.cursor()


        cursor.execute(
            """
            SELECT id, name, email, password
            FROM users
            WHERE email = ?
            """,
            (email,)
        )


        user = cursor.fetchone()

        connection.close()


        # Check login

        if user and check_password_hash(
            user[3],
            password
        ):

            session["user_id"] = user[0]

            session["name"] = user[1]

            session["email"] = user[2]


            return redirect(
                url_for("home")
            )


        flash(
            "Invalid email or password."
        )

        return redirect(
            url_for("login")
        )


    return render_template(
        "login.html"
    )


# =========================================================
# LOGOUT
# =========================================================

@app.route("/logout")
def logout():

    session.clear()

    flash(
        "You have been logged out."
    )

    return redirect(
        url_for("login")
    )


# =========================================================
# AI RECOMMENDATION
# =========================================================

@app.route(
    "/recommend",
    methods=["POST"]
)
def recommend():

    # -----------------------------------------
    # CHECK LOGIN
    # -----------------------------------------

    if not login_required():

        return redirect(
            url_for("login")
        )


    # -----------------------------------------
    # CHECK MODEL
    # -----------------------------------------

    if ml_model is None:

        return """
        <html>
        <body style="font-family: Arial; padding: 40px;">

        <h2>AI Model Not Found</h2>

        <p>
        The machine learning model has not been created yet.
        </p>

        <p>
        Open VS Code Terminal and run:
        </p>

        <pre>python train_model.py</pre>

        <br>

        <a href="/">
        Back to Home
        </a>

        </body>
        </html>
        """


    # -----------------------------------------
    # GET FORM VALUES
    # -----------------------------------------

    destination = request.form.get(
        "destination",
        ""
    ).strip().lower()

    activity = request.form.get(
        "activity",
        ""
    ).strip().lower()


    # -----------------------------------------
    # VALIDATION
    # -----------------------------------------

    if not destination or not activity:

        flash(
            "Please enter both destination and activity."
        )

        return redirect(
            url_for("home")
        )


    # -----------------------------------------
    # NORMALIZE DESTINATION
    # -----------------------------------------

    destination = DESTINATION_ALIASES.get(
        destination,
        destination
    )


    # -----------------------------------------
    # NORMALIZE ACTIVITY
    # -----------------------------------------

    activity = ACTIVITY_ALIASES.get(
        activity,
        activity
    )


    # -----------------------------------------
    # CREATE ML INPUT
    # -----------------------------------------

    input_data = pd.DataFrame(
        [
            {
                "destination": destination,
                "activity": activity
            }
        ]
    )


    print("\n========================================")
    print("FORGETMENOT AI PREDICTION")
    print("========================================")

    print(
        "Destination:",
        destination
    )

    print(
        "Activity:",
        activity
    )

    print(
        "Input Data:"
    )

    print(
        input_data
    )


    # -----------------------------------------
    # AI PREDICTION
    # -----------------------------------------

    try:

        predicted_category = ml_model.predict(
            input_data
        )[0]


    except Exception as e:

        print(
            "MODEL PREDICTION ERROR:",
            e
        )

        return f"""
        <html>
        <body style="font-family: Arial; padding: 40px;">

        <h2>AI Prediction Error</h2>

        <p>{e}</p>

        <br>

        <a href="/">
        Back to Home
        </a>

        </body>
        </html>
        """


    print(
        "Predicted Category:",
        predicted_category
    )

    print("========================================\n")


    # -----------------------------------------
    # GET CHECKLIST
    # -----------------------------------------

    recommendations = RECOMMENDATIONS.get(
        predicted_category
    )


    # -----------------------------------------
    # FALLBACK
    # -----------------------------------------

    if recommendations is None:

        recommendations = [
            "Phone",
            "Wallet",
            "ID Card",
            "Water Bottle",
            "Keys"
        ]


    # -----------------------------------------
    # DISPLAY CHECKLIST
    # -----------------------------------------

    return render_template(
        "checklist.html",

        destination=destination.title(),

        activity=activity.title(),

        recommendations=recommendations,

        category=predicted_category,

        name=session.get("name")
    )


# =========================================================
# RUN APPLICATION
# =========================================================

if __name__ == "__main__":

    print("\n")
    print("========================================")
    print("       FORGETMENOT AI APPLICATION")
    print("========================================")

    print(
        "Database:",
        DATABASE
    )

    print(
        "Model:",
        MODEL_FILE
    )


    if ml_model is not None:

        print(
            "AI Model: READY"
        )

    else:

        print(
            "AI Model: NOT FOUND"
        )


    print("========================================")

    print(
        "Open in browser:"
    )

    print(
        "http://127.0.0.1:5000"
    )

    print("========================================")

    print("\n")


    app.run(
        debug=True
    )