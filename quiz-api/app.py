from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import hashlib
from dotenv import load_dotenv
from jwt_utils import build_token, decode_token
from question import Question, Reponse
import question_dao

app = Flask(__name__)
CORS(app)

load_dotenv()  # charge le .env
expected_password = os.getenv("ADMIN_PASSWORD", "")
expected_hash = hashlib.md5(expected_password.encode()).hexdigest()

# ----------------- Helpers -----------------


def require_auth():
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    return decode_token(token)

# --------------- Routes --------------------


@app.route('/')
def hello_world():
    return "Hello, world"


@app.route('/rebuild-db', methods=['POST'])
def rebuild_db():
    # Endpoint protégé
    if not require_auth():
        return "Unauthorized", 401

    question_dao.rebuild_db()
    return "Ok", 200


@app.route('/quiz-info', methods=['GET'])
def GetQuizInfo():
    size = question_dao.count_questions()
    scores = question_dao.get_all_participations_sorted()
    # format pour Postman tests: info.size, info.scores.length, scores entries {playerName, score}
    return {"size": size, "scores": [{"playerName": s["playerName"], "score": s["score"]} for s in scores]}, 200


@app.route('/login', methods=['POST'])
def GetLogin():
    payload = request.get_json() or {}
    password = payload.get("password", "")

    password_hash = hashlib.md5(password.encode()).hexdigest()

    if password_hash == expected_hash:
        token = build_token()
        return {"token": token}, 200
    else:
        return "Unauthorized", 401


# ---------------- QUESTIONS ------------------

@app.route('/questions', methods=['POST', 'GET', 'PUT'])
def questions_root():
    # GET with optional ?position=
    if request.method == 'GET':
        pos = request.args.get("position")
        if pos is not None:
            try:
                pos = int(pos)
            except ValueError:
                return {"error": "position must be an integer"}, 400
            q = question_dao.get_question_by_position(pos)
            if not q:
                return {"error": "Question not found"}, 404
            return q.to_dict(), 200
        else:
            # fallback: list all
            questions = question_dao.get_all_questions()
            return [q.to_dict() for q in questions], 204

    # POST -> create (token required)
    if request.method == 'POST':
        if not require_auth():
            return "Unauthorized", 401
        data = request.get_json() or {}
        question = Question.from_dict(data)
        # insert handling positions: insert_question will shift as needed
        question.id = question_dao.insert_question(question)
        answers = []
        for i, ans_data in enumerate(data.get("possibleAnswers", []), start=1):
            ans = Reponse.from_dict(ans_data, question.id)
            ans.answer_index = i
            ans.id = question_dao.insert_answer(ans)
            answers.append(ans)
        question.answers = answers
        return question.to_dict(), 200

    # PUT /questions?position=2  -> change the position of the question at that position
    if request.method == 'PUT':
        if not require_auth():
            return "Unauthorized", 401
        pos = request.args.get("position")
        if pos is None:
            return {"error": "position query parameter required for this route"}, 400
        try:
            pos = int(pos)
        except ValueError:
            return {"error": "position must be an integer"}, 400

        data = request.get_json() or {}
        new_position = data.get("position")
        if new_position is None:
            return {"error": "body must contain 'position' (new position)"}, 400
        try:
            new_position = int(new_position)
        except ValueError:
            return {"error": "position must be an integer"}, 400

        # find question at pos
        q = question_dao.get_question_by_position(pos)
        if not q:
            return {"error": "Question not found at given position"}, 404


        # perform move
        # Met à jour les champs de la question
        question_dao.update_question_fields(updated_question)

        # 🔄 Remplace toutes les réponses associées
        if updated_question.answers:
            question_dao.replace_answers_for_question(question_id, updated_question.answers)

        # Renvoie la nouvelle version complète
        q = question_dao.get_question_by_id(question_id)
        return q.to_dict(), 204



@app.route('/questions/all', methods=['GET', 'DELETE'])
def questions_all():
    if request.method == 'GET':
        questions = question_dao.get_all_questions()
        return [q.to_dict() for q in questions], 200

    # DELETE all (protected)
    if request.method == 'DELETE':
        if not require_auth():
            return "Unauthorized", 401
        question_dao.delete_all_questions()
        return {"message": "Toutes les questions supprimées"}, 204


@app.route('/questions/<int:question_id>', methods=['GET', 'PUT', 'DELETE'])
def question_by_id(question_id):
    if request.method == 'GET':
        q = question_dao.get_question_by_id(question_id)
        if not q:
            return {"error": "Question not found"}, 404
        return q.to_dict(), 200

    if not require_auth():
        return "Unauthorized", 401

    if request.method == 'PUT':
        data = request.get_json() or {}
        updated_question = Question.from_dict(data)
        updated_question.id = question_id

        # Reconstruire les objets Reponse
        updated_question.answers = [
            Reponse.from_dict(ans_data, question_id)
            for ans_data in data.get("possibleAnswers", [])
        ]

        # detect if position will change
        old_q = question_dao.get_question_by_id(question_id)
        if not old_q:
            return {"error": "Question not found"}, 404

        if updated_question.position is None:
            # if no position provided, keep old
            updated_question.position = old_q.position

        # if position differs, move accordingly
        if updated_question.position != old_q.position:
            question_dao.move_question_by_id(
                question_id, updated_question.position)
            # update other fields after move
        # update title/text/image
        

        # Met à jour les champs principaux
        question_dao.update_question_fields(updated_question)

        # 🔄 Remplace toutes les anciennes réponses par les nouvelles
        if updated_question.answers:
            question_dao.replace_answers_for_question(
                question_id, updated_question.answers)

        # Récupère la version mise à jour
        q = question_dao.get_question_by_id(question_id)
        return q.to_dict(), 204


    if request.method == 'DELETE':
        # we must delete and shift positions
        q = question_dao.get_question_by_id(question_id)
        if not q:
            return {"error": "Question not found"}, 404
        question_dao.delete_question_and_shift(question_id)
        return {"message": f"Question {question_id} supprimée"}, 204


# -------------- Participations ----------------

@app.route('/participations', methods=['POST'])
def post_participation():
    data = request.get_json() or {}
    playerName = data.get("playerName")
    answers = data.get("answers")
    if not playerName or answers is None:
        return {"error": "playerName and answers required"}, 400
    if not isinstance(answers, list):
        return {"error": "answers must be a list"}, 400

    questions = question_dao.get_all_questions()
    if len(answers) != len(questions):
        return {"error": "number of answers does not match number of questions"}, 400

    score = 0
    for i, question in enumerate(questions):
        chosen_index = answers[i]
        if question_dao.is_answer_correct(question["id"], chosen_index):
            score += 1


    # store participation
    participation_id = question_dao.insert_participation(
        playerName, score, answers)
    return {"id": participation_id, "playerName": playerName, "score": score}, 200


@app.route('/participations/all', methods=['DELETE'])
def delete_participations_all():
    # protected
    if not require_auth():
        return "Unauthorized", 401
    question_dao.delete_all_participations()
    return {"message": "Toutes les participations supprimées"}, 204


if __name__ == "__main__":
    app.run()
