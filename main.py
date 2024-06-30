from fastapi import FastAPI
from pydantic import BaseModel
import mysql.connector
from dotenv import load_dotenv
import os


load_dotenv()

def get_db_connection():
    cnx = mysql.connector.connect(
        host = os.getenv("MYSQL_HOST"),
        user = os.getenv("MYSQL_USERNAME"),
        password = os.getenv("MYSQL_PASSWORD"),
        database = os.getenv("MYSQL_DATABASE")
    )
    return cnx

app = FastAPI()

class Attraction(BaseModel):
    name : str
    detail : str
    coverimage : str
    latitude : float
    longitude : float

@app.post('/attractions')
def create_attraction(attraction : Attraction):
    cnx = get_db_connection()
    cursor = cnx.cursor()
    query = '''
    INSERT INTO attractions (name, detail, coverimage, latitude, longitude)
    VALUES (%s, %s, %s, %s, %s)
    '''
    cursor.execute(query,(attraction.name, attraction.detail, attraction.coverimage, 
                         attraction.latitude, attraction.longitude))
    cnx.commit()
    attraction_id = cursor.lastrowid
    cursor.close()
    cnx.close()
    return {"id" : attraction_id}

@app.get('/attractions')
def get_attractions():
    cnx = get_db_connection()
    cursor = cnx.cursor()
    query = "SELECT * FROM attractions"
    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()
    cnx.close

    attractions = []
    for row in rows:
        attractions.append({
            "id" : row[0],
            "name" : row[1],
            "detail" : row[2],
            "coverimage" : row[3]
        })
    return attractions

@app.get('/')
def read_root():
    return {"message" : "Hello World"}

@app.get('/hello')
def read_hello():
    return {"message":"Hello"}

@app.get('/items/{id}')
def read_item(id:int):
    return {"item":id}
