from flask import Flask, request, make_response
from flask_cors import CORS, cross_origin
import pymongo
from dotenv import load_dotenv
import os
import urllib.parse as urllib

load_dotenv()
app = Flask(__name__)

api_v1_cors_config = {
  "origins": ["http://localhost:5000"]
}

CORS(app)


main_messages = []


def db_connect():
    """
    :return: returns the connection to the user
    """
    try:
        client = pymongo.MongoClient("mongodb+srv://dbUser:"+urllib.quote(os.environ.get("pass"))+"@mongodbsandbox-cluster0.vxs0w.mongodb.net/auto?retryWrites=true&w=majority")
        mydb = client["auto"]
    except Exception as e:
        print("(-) Error in Connecting to the DB")
        print(e)
        return None
    else:
        return mydb


@app.route("/", methods=["GET"])
def main_route():
    return {"message": "Hello Welcome to the Sample App"}, 200


@app.route("/get", methods=["GET"])
@cross_origin(headers=['Content-Type','Access-Control-Allow-Origin'])
def get():

    global main_messages
    if db_connect() is not None:
        db = db_connect()["messages"]
    else:
        return {"message":"Servers are Down"}, 500
    try:
        all_messages = []
        for i in db.find():
            all_messages.append({"id":str(i["_id"]),"m":i["message"]})

        print(all_messages)
    except Exception as e:
        return {"message": "Error in Getting the Messages"}, 200
    else:
        # result = set(all_messages) - set(main_messages)
        # result = [i for i in result]
        # main_messages = all_messages
        return {"message": all_messages}, 200


@app.route("/post", methods=["POST"])
def post():
    if db_connect() is not None:
        db = db_connect()["messages"]
    else:
        return {"message": "Servers are Down"}, 500

    json = request.get_json(force=True)
    print(json)
    try:
        db.insert_one({"message": json["msg"]})
    except Exception as e:
        return {"message":"Failed in Sending, Try again"}, 200
    else:
        return {"message": "Success"}, 200


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
