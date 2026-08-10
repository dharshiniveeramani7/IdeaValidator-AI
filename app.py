from flask import Flask, render_template, request
from ai_engine import analyze_startup_idea
import traceback

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/analyze", methods=["POST"])
def analyze():

    idea = request.form["startup_idea"]

    try:
        ai_report = analyze_startup_idea(idea)
    except Exception:
        traceback.print_exc()
        ai_report = "Internal Server Error"

    return render_template(
        "result.html",
        idea=idea,
        report=ai_report
    )


if __name__ == "__main__":
    app.run(debug=True)