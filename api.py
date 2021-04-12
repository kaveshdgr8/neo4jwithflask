from flask import Flask,request,jsonify,redirect,render_template
from neo4j import GraphDatabase
import csv

#establish the connection
with open("cred.txt") as f1:
    data=csv.reader(f1,delimiter=",")
    for row in data:
        username=row[0]
        pwd=row[1]
        uri=row[2]
print(username,pwd,uri)
driver=GraphDatabase.driver(uri=uri,auth=(username,pwd))
session=driver.session()
api=Flask(__name__)
@api.route("/create/<string:name>&<string:email>&<string:gender>&<string:dob>&<string:mobilenumber>&<string:city>&<string:country>&<string:qualdetails>&<string:unidetails>&<string:studyfield>&<string:position>",methods=["GET","POST"])
def create_user (name,email,gender,dob,mobilenumber,city,country,qualdetails,unidetails,studyfield,position):
    q1="""
    create (n:User{NAME:$name,EMAIL:$email,GENDER:$gender,DOB:$dob,MOBILENUMBER:$mobilenumber,CITY:$city,COUNTRY:$country,qualdetails:$qualdetails,unidetails:$unidetails,studyfield:$studyfield,position:$position})
    """
    map={"name":name,"email":email,"gender":gender,"dob":dob,"mobilenumber":mobilenumber,"city":city,"country":country,"qualdetails":qualdetails,"unidetails":unidetails,"studyfield":studyfield,"position":position}
    try:
        session.run(q1,map)
        return (f"user node is created with username name={name},email={email},gender={gender},dob={dob},mobilenumber={mobilenumber},city={city},country={country},qualdetails={qualdetails},unidetails={unidetails},studyfield={studyfield},position={position}")
    except Exception as e:
        return (str(e))



@api.route("/update/<string:nodename>&<string:newname>",methods=["GET","POST"])
def update_nodename(nodename,newname):
    q1=f"""
    match (n) where n.name="{nodename}" set n.name="{newname}" return n.name
    """
    results=session.run(q1)
    return(f" node name is updated to {newname}")


if __name__=="__main__":
    api.run(port=5050)