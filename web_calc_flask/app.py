from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Create BD
def init_db():
    conn = sqlite3.connect("history.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            operation TEXT,
            result TEXT
        )
    """)
    conn.commit()
    conn.close()

@app.route("/", methods=["GET", "POST"])
def calculator():
    result = None
    history = []

    # БД
    conn = sqlite3.connect("history.db")
    cursor = conn.cursor()

    if request.method == "POST":
        try:
            num1 = float(request.form["num1"])
            num2 = float(request.form["num2"])
            operation = request.form["operation"]

            # Таргет
            if operation == "add":
                result = num1 + num2
                operation_text = f"{num1} + {num2}"
            elif operation == "subtract":
                result = num1 - num2
                operation_text = f"{num1} - {num2}"
            elif operation == "multiply":
                result = num1 * num2
                operation_text = f"{num1} × {num2}"
            elif operation == "divide":
                result = num1 / num2 if num2 != 0 else "На ноль делить нельзя!"
                operation_text = f"{num1} ÷ {num2}"
            elif operation == "power":
                result = num1 ** num2
                operation_text = f"{num1} ^ {num2}"
            elif operation == "modulus":
                result = num1 % num2
                operation_text = f"{num1} % {num2}"
            elif operation == "sqrt":
                result = num1 ** (1 / num2)
                operation_text = f"√{num1} (степень {num2})"
            else:
                result = "Неверная операция!"

            # Сейв в бд
            cursor.execute("INSERT INTO history (operation, result) VALUES (?, ?)", (operation_text, str(result)))
            conn.commit()
        except ValueError:
            result = "Ошибка: введите корректные числа!"

    # Парс с бд
    cursor.execute("SELECT operation, result FROM history ORDER BY id DESC")
    history = cursor.fetchall()
    conn.close()

    return render_template("calculator.html", result=result, history=history)

# Clear
@app.route("/clear", methods=["POST"])
def clear_history():
    conn = sqlite3.connect("history.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM history")
    conn.commit()
    conn.close()
    return redirect("/")

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
