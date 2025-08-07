from flask import Flask, request, Response
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime, timezone

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///promo_codes.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
class CODES(db.Model):
    __tablename__ = "promo_code"
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(100), unique=True, nullable=False)
    status = db.Column(db.Boolean,default=False, nullable=False)
    phone_number = db.Column(db.String(100))
    time = db.Column(db.DateTime)
    reward = db.Column(db.String(300), nullable=False)

with app.app_context():
    db.create_all()
    db.session.commit()

@app.route("/submit", methods=["POST"])
def submit():
    session_id = request.form["sessionId"]
    service_code = request.form["serviceCode"]
    phone_number = request.form["phoneNumber"]
    text = request.form["text"]
    if text == "":
        response = "CON Enter the Promo Code To Claim Reward"
    else:
        splited_code = text.split("*")
        if len(splited_code) == 2:
            code = splited_code[1]
            check_code = CODES.query.filter_by(code=code).first()
            if check_code:
                if check_code.status == False:
                    check_code.status = True
                    check_code.phone_number = phone_number
                    timee = datetime.now(timezone.utc)
                    check_code.time = timee.strftime("%Y-%m-%d %H:%M:%S %Z")
                    reward = check_code.reward
                    db.session.commit()
                    response = f"END Congratulations!!! you won {reward}"
                else:
                    response = f"END Sorry the code {code} has already been used"
            else:
                response = "END Sorry Better luck next time!!"
        else:
            response = "END This not a valid Code\nTry again later."




    return Response(response, mimetype="text/plain")

if __name__ == "__main__":
    app.run(port=5000, debug=True)