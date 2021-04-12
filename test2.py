from os import abort

from flask import Flask, request, jsonify, redirect, render_template
from neo4j import GraphDatabase
import csv, json

# establish the connection
with open("cred.txt") as f1:
    data = csv.reader(f1, delimiter=",")
    for row in data:
        username = row[0]
        pwd = row[1]
        uri = row[2]
print(username, pwd, uri)
driver = GraphDatabase.driver(uri=uri, auth=(username, pwd))
session = driver.session()
api = Flask(__name__)


@api.route("/create/<string:user>", methods=["GET","POST"])
def create_user(user):
    if not request.json or not 'name' in request.json:
        abort(400)
    user = {
        'id': users[-1]['id'] + 1,
        'name': request.json['name'],
        'email':request.json['email'],
        'gender':request.json['gender'],
        'dob':request.json['dob'],
        'mobilenumber':request.json["mobilenumber"],
        'city':request.json['city'],
        'country':request.json['country'],
        'qualdetails':request.json['qualdetails'],
        'unidetails':request.json['unidetails'],
        'studydetails':request.json['studyfield'],
        'position':request.json['position'],
        'description': request.json.get('description', ""),
        'done': False
    }


    q1 = """
    create (n:User{NAME:$name,EMAIL:$email,GENDER:$gender,DOB:$dob,MOBILENUMBER:$mobilenumber,CITY:$city,COUNTRY:$country,qualdetails:$qualdetails,unidetails:$unidetails,studyfield:$studyfield,position:$position})
    """

    try:
        session.run(q1, user)
        return (
            f"user node is created with username ")
    except Exception as e:
        return (str(e))


@api.route("/update/<string:nodename>&<string:newname>", methods=["GET", "POST"])
def update_nodename(nodename, newname):
    q1 = f"""
    match (n) where n.name="{nodename}" set n.name="{newname}" return n.name
    """
    results = session.run(q1)
    return (f" node name is updated to {newname}")


if __name__ == "__main__":
    api.run(port=5050)
