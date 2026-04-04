from flask import Flask, render_template, request, redirect

app = Flask(__name__)

expenses = []

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        name = request.form["name"]
        amount = request.form["amount"]

        expenses.append({"name": name, "amount": float(amount)})

        return redirect("/")

    total = sum(exp["amount"] for exp in expenses)

    return render_template("index.html", expenses=expenses, total=total)

if __name__ == "__main__":
    app.run(debug=True)