import shutil
import json
import models
import shutil
import datetime
import os
from typing import ItemsView
from fastapi import FastAPI, Query, Request, Form, Depends, UploadFile, File, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from requests import Response
from database import sessionlocal, engine, conn
from models import students, country, state, city
from pathlib import Path

app = FastAPI()

models.Base.metadata.create_all(engine)

dateNow = datetime.datetime.now()
year = dateNow.strftime("%Y") #
month = dateNow.strftime("%b") #
dayofMonth = datetime.datetime.now().day #
week = (dayofMonth - 1) // 7 + 1 #

# mount methord for image and file location
app.mount(
    "/static",
    StaticFiles(directory=Path(__file__).parent.absolute() / "static"),
    name="static",
)
app.mount(
    "/home/python/Documents/registration/image_file",
    StaticFiles(directory=Path(__file__).parent.absolute() / "image_file"),
    name="image_file",
)

templates = Jinja2Templates(directory="templates")

# post method to insert form
@app.post("/createstudent")
async def createStudent(request: Request, image: UploadFile = File(...)):
    formData = await request.form() 

    insertUpdateStudent('insert', formData, image)

    url = '/'
    response = RedirectResponse(url=url)

    return response

# display data table
@app.api_route("/", response_class=HTMLResponse, methods=['GET', 'POST'])
async def showStudentData(request: Request):

    resultLength = conn.execute(students.select()).fetchall()
    resultLength = len(resultLength)

    formData = await request.form()
    pageId = formData.get('pageId')

    if pageId == None:
        pageId = 1

    pageId = int(pageId)

    limit = 5
    start = (pageId - 1) * limit

    query = f'SELECT students.*, country.name, state.name as sname, city.name as cname FROM students JOIN country on students.country = country.id JOIN state on students.state = state.id JOIN city on students.city =city.id limit {start}, {limit}'

    result = conn.execute(query).fetchall()

    return templates.TemplateResponse('display.html', {"request": request, "result": result, "resultLength": resultLength})

# get update response 
@app.get("/update/{id}", response_class=HTMLResponse)
async def getStudentData(id: int, request: Request):

    result = conn.execute(students.select().where(
        students.c.id == id)).fetchone()
    countryList = conn.execute(country.select()).fetchall()

    return templates.TemplateResponse('update.html', {"request": request, "result": result, 'country': countryList})

# put method to update data 
@app.post("/update_data", response_class=HTMLResponse)
async def updateStudentData(request: Request, image: UploadFile = File(...)):
    formData = await request.form()
    insertUpdateStudent('update', formData, image)

    url = '/'
    response = RedirectResponse(url=url)
    return response

# delete method
@app.get("/delete/{id}", response_class=HTMLResponse)
async def deleteStudentData(id: int, request: Request):

    conn.execute(students.delete().where(students.c.id == id))

    url = '/'
    response = RedirectResponse(url=url)

    return response

# send to the form page
@app.post("/form", response_class=HTMLResponse)
async def registrationPage(request: Request):

    countryList = conn.execute(country.select()).fetchall()
    return templates.TemplateResponse('form.html', {"request": request, "country": countryList})

# Get state value 
@app.api_route("/state", response_class=HTMLResponse, methods=['POST'])
async def showStateData(request: Request):

    formData = await request.form()
    getData = formData.get('countryData')

    return getDropdownList(getData, tableName = "state", columnName = "country_id")

# Get cities value 
@app.api_route("/city", response_class=HTMLResponse, methods=['POST'])
async def stateData ( request: Request):
    formData = await request.form()
    getData = formData.get('stateData')

    return getDropdownList(getData, tableName = "city", columnName = "state_id")

# Get records according to pageCount
@app.api_route("/getRecords", response_class=HTMLResponse, methods=['POST'])
async def getRecordOfStudent(request: Request):
    formData = await request.form()
    pageId = formData.get('pageId')
    input = formData.get('input')

    if input != '':
        query= f'SELECT students.*, country.name, state.name as sname, city.name as cname FROM students JOIN country on students.country = country.id JOIN state on students.state = state.id JOIN city on students.city =city.id where fname LIKE "%%{input}%%" OR lname LIKE "%%{input}%%" OR phone LIKE "%%{input}%%" OR course LIKE "%%{input}%%" OR gender LIKE "{input}" OR country LIKE "%%{input}%%" OR state LIKE "%%{input}%%" OR city LIKE "%%{input}%%" OR address LIKE "%%{input}%%" OR vehicle LIKE "%%{input}%%"'
    else:
        query = students.select()
    
    result = conn.execute(query).fetchall()
    resultLength = len(result)

    if pageId == None:
        pageId = 1

    pageId = int(pageId)

    limit = 5
    start = (pageId - 1) * limit

    query = f'SELECT students.*, country.name, state.name as sname, city.name as cname FROM students JOIN country on students.country = country.id JOIN state on students.state = state.id JOIN city on students.city =city.id limit {start}, {limit}'

    if input != '':
        query= f'SELECT students.*, country.name, state.name as sname, city.name as cname FROM students JOIN country on students.country = country.id JOIN state on students.state = state.id JOIN city on students.city =city.id where fname LIKE "%%{input}%%" OR lname LIKE "%%{input}%%" OR phone LIKE "%%{input}%%" OR course LIKE "%%{input}%%" OR gender LIKE "{input}" OR country LIKE "%%{input}%%" OR state LIKE "%%{input}%%" OR city LIKE "%%{input}%%" OR address LIKE "%%{input}%%" OR vehicle LIKE "%%{input}%%" limit {start}, {limit}'

    result = conn.execute(query).fetchall()

    dataOfStudents = {}
    k = 0
    for i in result:
        d = dict(i)
        dataOfStudents[k] = d
        k += 1
    jsonData = json.dumps({'data':dataOfStudents, 'totalCount' : resultLength})

    return jsonData

@app.api_route("/search", response_class=HTMLResponse, methods=['POST'])
async def searchRecord(request: Request):
    formData = await request.form()
    input = formData.get('input')
    pageId = formData.get('pageId')

    query= f'SELECT students.*, country.name, state.name as sname, city.name as cname FROM students JOIN country on students.country = country.id JOIN state on students.state = state.id JOIN city on students.city =city.id where fname LIKE "%%{input}%%" OR lname LIKE "%%{input}%%" OR phone LIKE "%%{input}%%" OR course LIKE "%%{input}%%" OR gender LIKE "{input}" OR country LIKE "%%{input}%%" OR state LIKE "%%{input}%%" OR city LIKE "%%{input}%%" OR address LIKE "%%{input}%%" OR vehicle LIKE "%%{input}%%"'
    result = conn.execute(query).fetchall()
    resultLength = len(result)

    if pageId == None:
        pageId = 1

    pageId = int(pageId)
    limit = 5
    start = (pageId - 1) * limit

    query= f'SELECT students.*, country.name, state.name as sname, city.name as cname FROM students JOIN country on students.country = country.id JOIN state on students.state = state.id JOIN city on students.city =city.id where fname LIKE "%%{input}%%" OR lname LIKE "%%{input}%%" OR phone LIKE "%%{input}%%" OR course LIKE "%%{input}%%" OR gender LIKE "{input}" OR country LIKE "%%{input}%%" OR state LIKE "%%{input}%%" OR city LIKE "%%{input}%%" OR address LIKE "%%{input}%%" OR vehicle LIKE "%%{input}%%" limit {start}, {limit}' 
    result = conn.execute(query).fetchall()

    dataOfStudents = {}
    k = 0
    for i in result:
        d = dict(i)
        dataOfStudents[k] = d
        k += 1
    jsonData = json.dumps({'data':dataOfStudents, 'totalCount' : resultLength})
    
    return jsonData

# dropDown For state and city
def getDropdownList(getData, tableName, columnName):
    query=f"SELECT id, name FROM {tableName} WHERE {columnName}={getData}"
    getDataRows=conn.execute(query).fetchall()
    st=dict(getDataRows)    
    jsonData = json.dumps(st)

    return jsonData

# insert and update data
def insertUpdateStudent(queryType, formData, image: UploadFile = File(...)):
    vehicleList = (formData.getlist("vehicle[]"))
    date = dateNow.strftime("%Y-%m-%d")
    imageFileName = f'{date}_'+image.filename
    
    if not os.path.isdir(f'/home/python/Documents/registration/image_file/{year}/{month}/{week}'):
        os.makedirs(
            f'/home/python/Documents/registration/image_file/{year}/{month}/{week}')

    if image.filename != '':
        with open(f'/home/python/Documents/registration/image_file/{year}/{month}/{week}/{imageFileName}', "wb+") as addressOfImage:
            shutil.copyfileobj(image.file, addressOfImage)

    imageName = f'/home/python/Documents/registration/image_file/{year}/{month}/{week}/{imageFileName}'

    fname=formData.get("firstname")
    lname=formData.get("lastname")
    phone=formData.get("phone")
    course=formData.get("course")
    gender=formData.get("gender")
    country=formData.get("country")
    state=formData.get("state")
    city=formData.get("city")
    address=formData.get("address")
    vehicle=(','.join(vehicleList))



    if queryType == 'insert':
        query = f"INSERT INTO students(fname, lname, phone, course, gender, country, state, city, address, vehicle, image)VALUES('{fname}','{lname}', '{phone}', '{course}', '{gender}', '{country}', '{state}', '{city}', '{address}', '{vehicle}', '{imageName}')"
        conn.execute(query)

        
    else:
        id = formData['id'] 
        query = f"UPDATE students SET fname='{fname}',lname='{lname}',course='{course}',gender='{gender}',phone='{phone}',country='{country}',state='{state}',city='{city}',address='{address}',vehicle='{vehicle}' WHERE id={id}"
        conn.execute(query)
        
        if image.filename != '':
            conn.execute(f"UPDATE students SET image='{imageName}' WHERE id='{id}'")

    return