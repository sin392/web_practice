from flask import Flask, render_template, request, session, redirect, jsonify, g
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///sample.sqlite3")
Base = declarative_base()

app = Flask(__name__)
app.secret_key = b'random string...'

class Mydata(Base):
    __tablename__ = "mydata"

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    mail = Column(String(255))
    age = Column(Integer)

    def toDict(self):
        return {
            "id": int(self.id),
            "name":str(self.name),
            "mail":str(self.mail),
            "age":int(self.age)
        }

def getByList(arr):
    res = []
    for item in arr:
        res.append(item.toDict())
    return res

def getAll():
    Session = sessionmaker(bind=engine)
    ses = Session()
    res = ses.query(Mydata).all()
    ses.close()
    return res


@app.route('/', methods=['GET'])
def index():
    return render_template(
        "index.html",
        title="Index",
        message="※SQLite3 Database",
        # alert="This is SQLite3 DataBase Sample!"
        )

@app.route('/ajax', methods=['GET'])
def ajax():
    mydata = getAll()
    return jsonify(getByList(mydata))

@app.route('/form', methods=['POST'])
def form():
    name = request.form.get("name")
    mail = request.form.get("mail")
    age = int(request.form.get("age"))
    print("@", name, mail, age)
    mydata = Mydata(name=name, mail=mail, age=age)
    Session = sessionmaker(bind=engine)
    ses = Session()
    ses.add(mydata)
    ses.commit()
    ses.close()
    return "ok"

if __name__ == "__main__":
    app.debug = True
    app.run(host="localhost")