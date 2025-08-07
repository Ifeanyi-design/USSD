from flask import Flask, request, Response

app = Flask(__name__)

@app.route("/submit", methods=["POST"])
def submit():
    session_id = request.form["sessionId"]
    service_code = request.form["serviceCode"]
    phone_number = request.form["phoneNumber"]
    text = request.form["text"]
    if text == "":
        response = "CON What would you want\n"
        response += "1. My Account No\n"
        response += "2. My Phone Number"
    elif text == "1":
        response = "CON Choose account information you want to view\n"
        response += "1. Account Number\n"
        response += "2. Account Balance"

    elif text == "2":
        response = f"END your phone number is {phone_number}"

    elif text == "1*1":
        account_no = "922842242"
        response = f"END your account number is {account_no}"

    elif text == "1*2":
        balance = "NG 10000"
        response = f"END you account balance is {balance}"

    return Response(response, mimetype="text/plain")

if __name__ == "__main__":
    app.run(port=5000, debug=True)