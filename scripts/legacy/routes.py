from flask import Blueprint, render_template, request
from app.rag_service import answer_question

main = Blueprint("main", __name__)

@main.route("/", methods=["GET", "POST"])
def index():
    answer = None
    question = None

    if request.method == "POST":
        question = request.form.get("question")

        if question:
            answer = answer_question(question)

    return render_template("index.html", question=question, answer=answer)