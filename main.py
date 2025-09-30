from fastapi import FastAPI,Request,Form
from fastapi.responses import HTMLResponse,JSONResponse,RedirectResponse
from fastapi.templating import Jinja2Templates
import calendar
import datetime
from db import *

app=FastAPI()
templates=Jinja2Templates(directory="templates")

@app.get('/index.html')
def landing_page(request:Request):
    return templates.TemplateResponse('index.html',context={"request":request})
@app.get("/calendar",response_class=HTMLResponse)
async def calendar(request:Request):
   
    return templates.TemplateResponse(name="calendar.html",request=request)
@app.get("/signin",response_class=HTMLResponse)
def register(request:Request):
    return templates.TemplateResponse('/signin.html',context={'request':request})
@app.get('/log_in',response_class=HTMLResponse)
def log_in(request:Request):
    return templates.TemplateResponse('login.html',context={'request':request,"login_error":False})
@app.post("/login")
def login(request:Request,email:str=Form(...),senha:str=Form(...)):
    if verify_user(senha,email):
        return templates.TemplateResponse(name="calendar.html",request=request)
    else:   
        return templates.TemplateResponse('login.html',context={'request':request,'login_error':True})
@app.post("/register",response_class=HTMLResponse)
def register(request:Request,senha:str= Form(...),email:str =Form(...),nome:str=Form(...)):
    insert_user(senha=senha,usuario=email,tipo='usuario')
    return RedirectResponse('/index.html')
@app.get("/events")
async def get_eventos():
    eventos=get_all_eventos()
    lista_eventos=[]
    for evento in eventos:
        lista_eventos.append({
            "id":evento[0],
            "title":evento[2],
            "start":evento[1]
            
        })
    print(lista_eventos)
    return JSONResponse(lista_eventos)
