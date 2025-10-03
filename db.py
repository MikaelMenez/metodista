import sqlite3


def create_eventos_table():
    connection=sqlite3.connect('datas.db')
    cursor=connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS  eventos(id INTEGER PRIMARY KEY AUTOINCREMENT,data TEXT NOT NULL,usuario TEXT NOT NULL)")
def create_user_table():
    connection=sqlite3.connect('datas.db')
    cursor=connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT,senha TEXT NOT NULL,usuario TEXT NOT NULL,tipo TEXT NOT NULL,nome TEXT NOT NULL)")
def insert_user(senha:str,usuario:str,tipo:str,nome:str):
    connection=sqlite3.connect('datas.db')
    cursor=connection.cursor()
    cursor.execute("INSERT INTO users (senha,usuario,tipo,nome) VALUES (?,?,?,?)",(senha,usuario,tipo,nome))
    connection.commit()
def insert_eventos(data:str,usuario:str):
    connection=sqlite3.connect('datas.db')
    cursor=connection.cursor()
    cursor.execute("INSERT INTO eventos (data,usuario) VALUES (?,?)",(data,usuario))
    connection.commit()

def modify_user(id:int,senha:str,usuario:str,tipo:str,nome:str):
    connection=sqlite3.connect('datas.db')
    cursor=connection.cursor()
    cursor.execute("UPDATE users SET data=? , usuario=?,tipo=?,nome=? WHERE id=?",(senha,usuario,tipo,nome,id))
    connection.commit()
def modify_eventos(id:int,data:str,usuario:str):
    connection=sqlite3.connect('datas.db')
    cursor=connection.cursor()
    cursor.execute("UPDATE eventos SET data=? , usuario=? WHERE id=?",(data,usuario,id))
    connection.commit()
def delete_eventos(id:int):
    connection=sqlite3.connect('datas.db')
    cursor=connection.cursor()
    cursor.execute("DELETE FROM eventos WHERE id=?",(id,))
    connection.commit()
def delete_user(id:int):
    connection=sqlite3.connect('datas.db')
    cursor=connection.cursor()
    cursor.execute("DELETE FROM users WHERE id=?",(id,))
    connection.commit()
def get_eventos(id:int):
    connection=sqlite3.connect('datas.db')
    cursor=connection.cursor()
    cursor.execute("SELECT * FROM eventos WHERE id=?",(id,))
    connection.commit()
    data=cursor.fetchall()
    return data
def get_user(id:int):
    connection=sqlite3.connect('datas.db')
    cursor=connection.cursor()
    cursor.execute("SELECT * FROM users WHERE id=?",(id,))
    connection.commit()
    data=cursor.fetchall()
    return data
def get_user(usuario:str,senha:str):
    connection=sqlite3.connect('datas.db')
    cursor=connection.cursor()
    cursor.execute("SELECT * FROM users WHERE usuario=? AND senha=?",(usuario,senha))
    connection.commit()
    data=cursor.fetchall()
    return data
def get_user(usuario:str):
    connection=sqlite3.connect('datas.db')
    cursor=connection.cursor()
    cursor.execute("SELECT * FROM users WHERE usuario=?",(usuario,))
    connection.commit()
    data=cursor.fetchone()
    return data

def get_all_eventos():
    connection=sqlite3.connect('datas.db')
    cursor=connection.cursor()
    cursor.execute("SELECT * FROM eventos")
    connection.commit()
    data=cursor.fetchall()
    return data
def get_all_eventos_by_user(usuario:str):
    connection=sqlite3.connect('datas.db')
    cursor=connection.cursor()
    cursor.execute("SELECT * FROM eventos WHERE usuario=?",(usuario,))
    connection.commit()
    data=cursor.fetchall()
    return data

def get_all_users():
    connection=sqlite3.connect('datas.db')
    cursor=connection.cursor()
    cursor.execute("SELECT * FROM users")
    connection.commit()
    data=cursor.fetchall()
    return data
def verify_user(senha:str,usuario:str):
    connection=sqlite3.connect('datas.db')
    cursor=connection.cursor()
    cursor.execute("SELECT * FROM users WHERE usuario=? AND senha=?",(usuario,senha))
    connection.commit()
    user=cursor.fetchone()
    return user is not None
eventos=get_all_eventos()
lista_eventos=[]
for evento in eventos:
        print(get_user(evento[0]))
        username=get_user(evento[2])[4]
        lista_eventos.append({
            "id":evento[0],
            "title":username ,
            "start":evento[1]
            
        })
