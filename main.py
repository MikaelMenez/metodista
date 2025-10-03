from fastapi import FastAPI,Request,Form,Cookie
from fastapi.responses import HTMLResponse,JSONResponse,RedirectResponse
from fastapi.templating import Jinja2Templates
import calendar
import datetime
from db import *

app=FastAPI()
templates=Jinja2Templates(directory="templates")
create_eventos_table()
create_user_table()


@app.get('/')
def landing_page(request:Request):
    return templates.TemplateResponse('index.html',context={"request":request})
@app.get("/calendar",response_class=RedirectResponse)
async def calendar(request:Request,permissoes:str=Cookie(...)):
   if permissoes== 'admin':
    return RedirectResponse("/calendar_admin")
   else:
    return RedirectResponse("/calendar_user")

@app.get('/eventos')
def eventos(request:Request):
    return templates.TemplateResponse("eventos.html",context={"request":request})

@app.get("/diasproibidos")
async def dias_proibidos(request:Request):
    dias=get_all_eventos()
    lista_dias=[]
    for dia in dias:
        lista_dias.append(
            dia[1])

    return JSONResponse(lista_dias)
@app.post("/marca_consulta")
async def marca_consulta(data:str=Form(...),usuario:str=Cookie(...)):
    insert_eventos(data,usuario)
    return RedirectResponse("/calendar",status_code=303)

@app.get("/calendar_admin",response_class=HTMLResponse)
async def calendar_admin(request:Request):
    return templates.TemplateResponse("calendar_admin.html",context={"request":request})

@app.get("/calendar_user",response_class=HTMLResponse)
async def calendar_user(request:Request):
    return templates.TemplateResponse("calendar_user.html",context={"request":request})

@app.get("/sign_in",response_class=HTMLResponse)
def register(request:Request,usuario:str=Cookie(None)):
    if not usuario:
        return templates.TemplateResponse('signin.html',context={'request':request})
    else: 
        return RedirectResponse("/calendar")

@app.post('/signin')
async def register_post(request:Request,email:str=Form(...),nome:str=Form(...),senha:str=Form(...)):
    
    insert_user(senha=senha,usuario=email,tipo='usuario',nome=nome)
    response= RedirectResponse("/calendar",status_code=303)

    response.set_cookie(key="usuario",value=email,max_age=3600,httponly=True)
    tipo=get_user(usuario=email)
    response.set_cookie(key="permissoes",value=tipo[3],max_age=3600,httponly=True)
    return response

@app.get('/log_in',response_class=HTMLResponse)
def log_in(request:Request,usuario:str=Cookie(None)):
    if not usuario:
        return templates.TemplateResponse('login.html',context={'request':request})
    else: 
        return RedirectResponse("/calendar")
    
@app.post("/login")
def login(request:Request,email:str=Form(...),senha:str=Form(...)):
    if verify_user(senha,email):
        response= RedirectResponse("/calendar",status_code=303)

        response.set_cookie(key="usuario",value=email,max_age=3600,httponly=True)
        tipo=get_user(usuario=email)
        response.set_cookie(key="permissoes",value=tipo[3],max_age=3600,httponly=True)
        return response
    else:   
        return templates.TemplateResponse('login.html',context={'request':request,'login_error':True})
    
@app.post("/register",response_class=HTMLResponse)
def register(request:Request,senha:str= Form(...),email:str =Form(...),nome:str=Form(...)):
    insert_user(senha=senha,usuario=email,tipo='usuario')
    return RedirectResponse('/',status_code=303)

@app.get("/events_by_user")
async def get_eventos(usuario:str=Cookie(...)):
    eventos=get_all_eventos()
    lista_eventos=[]
    for evento in eventos:
        if evento[2]== usuario:
            lista_eventos.append({
            "id":evento[0],
            "title":"sua consulta",
            "start":evento[1]
            })
        else:
            lista_eventos.append({
            "id":evento[0],
            "title":"ocupado",
            "start":evento[1]
            })
    print(lista_eventos)
    return JSONResponse(lista_eventos)
@app.get("/events")
async def get_eventos():
    eventos=get_all_eventos()
    lista_eventos=[]
    for evento in eventos:
        
        lista_eventos.append({
            "id":evento[0],
            "title":evento[2] ,
            "start":evento[1]
            
        })
    print(lista_eventos)
    return JSONResponse(lista_eventos)

@app.get('/users')
async def get_users():
    users=get_all_users()
    lista_users=[]
    for user in users:
        lista_users.append({
            "id":user[0],
            "email":user[2],
            "permissões":user[3],
            "nome":user[4]
            
        })
    print(lista_users)
    return JSONResponse(lista_users)

