from flask import Flask, render_template, request, redirect
import sqlite3


app = Flask(__name__)

# إنشاء قاعدة البيانات
def init_db():

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_name TEXT,
        book_name TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()


# الصفحات الأساسية
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/books")
def books():
    return render_template("books.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


# صفحة الطلب
@app.route("/order/", methods=["GET", "POST"])
def order():

    message = ""

    prices = {
        "The Silent Patient": 20,
        "Atomic Habits": 15,
        "Harry Potter": 25
    }

    if request.method == "POST":

        customer_name = request.form["customer_name"]
        book_name = request.form["book_name"]

        price = prices[book_name]

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO orders (customer_name, book_name)
        VALUES (?, ?)
        """, (customer_name, book_name))

        conn.commit()
        conn.close()

        message = f"Book purchased successfully! The price is ${price}"

    return render_template("order.html", message=message)


# صفحة الادمن
@app.route("/admin/")
def admin():
   
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM orders")

    orders = cursor.fetchall()

    conn.close()

    return render_template("admin.html", orders=orders)


if __name__ == "__main__":
    app.run(debug=True,)