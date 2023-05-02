from flask import Flask,Response,request
import pymongo
import json
from bson.objectid import ObjectId
import jsonify
app=Flask(__name__)


try:
    mongo=pymongo.MongoClient(host="localhost",port=27017,serverSelectionTimeoutMS=1000)
    mongo.server_info()
    db=mongo.company
except:
    print("ERROR")

@app.route("/users/find/<id>",methods=["GET"])
def get_one_user(id):
    try:
        data=db.users.find_one({"_id":ObjectId(id)})
        if data:
            data["_id"]=str(data["_id"])
            return Response(response=json.dumps(data),
                            status=200,
                            mimetype="application/json")
        return Response(response=jsonify({"MESSAGE":"NOT FOUND"}),
                        status=200,
                        mimetype="application/json")
    except:
        return Response(
            response=json.dumps({"message":"Doesn't Exist"}),
            status=500,
            mimetype="application/json"
        )

@app.route("/users",methods=["GET"])
def get_user():
    try:
        data=list(db.users.find())
        for user in data:
            user["_id"]=str(user["_id"])
        return Response(
            response=json.dumps(data),
            status=200,
            mimetype="application/json"
        )
    except Exception as ex:
        return Response(
            response=json.dumps({"message":"Cannot Get"}),
            status=500,
            mimetype="application/json"
        )

@app.route("/users",methods=["POST"])
def create_user():
    try:
        user= {"name":request.form["name"],"email":request.form["email"],"password":request.form["password"]}
        dbresponse=db.users.insert_one(user)
        print(dbresponse.inserted_id)
        return Response(
            response=json.dumps({"message":"Created","ID":f"{dbresponse.inserted_id}"}),
            status=200,
            mimetype="application/json"
        )
    except Exception as ex:
        pass
@app.route("/users/<id>",methods=["PUT"])
def update_user(id):
    try:
        dbresponse=db.users.update_one({"_id":ObjectId(id)},
                                       {"$set":{"name":request.form["name"],"email":request.form["email"],"password":request.form["password"]}})
        if dbresponse.modified_count==1:
            return Response(
                response=json.dumps({"message":"User Updated"}),
                status=200,
                mimetype="application/json"
            )
        else:
            return Response(
                response=json.dumps({"message":"Same value"}),
                status=200,
                mimetype="application/json"
            )
    except Exception as ex:
        print(ex)
        return Response(
            response=json.dumps({"message":"Cant Update"}),
            status=500,
            mimetype="application/json"
        )


@app.route("/users/<id>",methods=["DELETE"])
def delete(id):
    try:
        dbresponse=db.users.delete_one({"_id":ObjectId(id)})
        if dbresponse.deleted_count==1:
            return Response(
                response=json.dumps({"message":"User Deleted","id":f"{id}"}),
                status=200,
                mimetype="application/json"
            )
        
        return Response(
                    response=json.dumps({"message":"User doesnt exist","id":f"{id}"}),
                    status=200,
                    mimetype="application/json"
                )   
    except Exception as ex:
        return Response(
            response=json.dumps({"message":"Cant delete"}),
            status=500,
            mimetype="application/json"
        )

if __name__=="__main__":
    app.run(port=80,debug=True)
