from flask import Flask, render_template, request, session, redirect, jsonify
import pickle

app = Flask(__name__)
app.secret_key = b'random string...'

member_data = {}
message_data = []
member_data_file = "member_data.dat"
message_data_file = "message_data.dat"

# load member_data & message_data from file.
reading_list = [member_data_file, message_data_file]
storing_list = [member_data, message_data]
for i in range(2):
    try:
        with open(reading_list[i], "rb") as f:
            m_list = pickle.load(f)
            if m_list != None:
                storing_list[i] = m_list
    except:
        pass

# access top page
@app.route('/', methods=['GET'])
def index():
    global message_data
    return render_template(
        "messages.html",
        login=False,
        title="Messages",
        message="not logined ...",
        data=message_data
    )

# post messages
@app.route('/post', methods=['POST'])
def postMsg():
    global message_data
    user_id = request.form.get("id")
    msg = request.form.get('comment')
    message_data.append((user_id, msg))
    if len(message_data) > 25:
        message_data.pop(0)
    try:
        with open(message_data_file, "wb") as f:
            pickle.dump(message_data, f)
    except:
        pass
    return "True"


# get messages
@app.route("/messages", methods=["POST"])
def getMsg():
    global message_data
    return jsonify(message_data)

# login form sended
@app.route('/login', methods=['POST'])
def login_post():
    global member_data
    user_id = request.form.get('id')
    pswd = request.form.get('pass')
    if user_id in member_data:
        if pswd == member_data[user_id]:
            flg = "True"
        else:
            flg = "False"
    else:
        member_data[user_id] = pswd
        flg = "True"
        try:
            with open(member_data_file, "wb") as f:
                pickle.dump(member_data, f)
        except:
            pass
    return flg

if __name__ == "__main__":
    app.debug = True
    app.run(host="localhost")