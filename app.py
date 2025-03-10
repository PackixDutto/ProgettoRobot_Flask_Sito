from flask import Flask, render_template, request, redirect, url_for, make_response #Per tutto riguardante l'applicazione web
from werkzeug.security import generate_password_hash, check_password_hash #Per le password
import sqlite3
import hashlib #Per crittografare la password
from datetime import datetime, timedelta #Per gestire la scadenza dei token di autenticazione
import jwt #Per creare e verificare i token per l'accesso
#from alpha_bot import AlphaBot

#robot = AlphaBot()

app = Flask(__name__)
SECRET_KEY = "mysecretkey" #Per i token
current_left_speed = 0 #Velocita ruote robot, non utilizzato alla fine
current_right_speed = 0

@app.route("/", methods=['GET', 'POST']) #PAGINA PRINCIPALE, controllo utente autenticato tramite i token
def index():
    global current_left_speed, current_right_speed
    token = request.cookies.get("token") #Controllo se l'utente ha già fatto l'accesso (E che ha già il token) o che il token non sia scaduto
    if not token:
        return redirect(url_for('login')) #L'utente rifà il login

    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        email = decoded_token['username']
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login")) #Token scaduto
    except jwt.InvalidTokenError:
        return redirect(url_for("login")) #Errore Token invalido

    if request.method == 'POST': #L'utente clicca su uno dei pulsanti ed ha già fatto il login
        action = request.form.get('action') #Va a prenderlo da index
        if action == 'W':
            #current_left_speed -= 50
            #current_right_speed += 50
            #robot.forward()
            print("W")
        elif action == 'A':
            #current_left_speed -= 25
            #current_right_speed += 50
            #robot.left()
            print("A")
        elif action == 'S':
            #current_left_speed += 50
            #current_right_speed -= 50
            #robot.backward()
            print("S")
        elif action == 'D':
            #current_left_speed -= 50
            #current_right_speed += 25
            #robot.right()
            print("D")
        elif action == 'O':
            current_left_speed = 0
            current_right_speed = 0
            #robot.stop()
            print("O")
        elif action == 'Logout':
            response = make_response(redirect(url_for('login'))) #Creo una response HTTP e vado a generare l'url associato a login
            response.delete_cookie("token") #Cancello il token, l'utente deve rifare l'accesso
            print("Logout")
            return response
        else:
            print("Unknown action") 
    
        print(f"right: {current_right_speed}")
        print(f"left: {current_left_speed}")
        #robot.setMotor(current_left_speed, current_right_speed) 

    return render_template("index.html") #Vado nella pagina con i bottoni

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST': #Compilazione del login
        email = request.form.get('e-mail')
        psw = request.form.get('password')
        return check(email, psw) #Controlla che ci siano nel db
    return render_template('login.html')

def check(email, psw):
    db_name = "databaseLarovere2.db"
    with sqlite3.connect(db_name) as conn: #Vado nel db, metto la query
        cursor = conn.cursor()
        cursor.execute("SELECT email, password FROM users WHERE email = ? AND password = ?", (email, hashlib.sha256(psw.encode()).hexdigest()))
        result = cursor.fetchone() #Prendo un solo risultato perché può esserci solo un account con quelle credenziali
        if result is None:
            return render_template("login.html", alert="Invalid credential") #Avviso delle credenziali invalide
        else: #Creo token che dura un giorno 
            expiration = datetime.utcnow() + timedelta(days=1)
            token = jwt.encode({"username": email, "exp": expiration}, SECRET_KEY, algorithm="HS256")
            response = make_response(redirect(url_for('index')))
            response.set_cookie("token", token, max_age=60*24, httponly=True)
            return response

@app.route('/create_account', methods=['GET', 'POST']) #Creo account
def create_account():
    if request.method == 'POST':
        email = request.form.get('e-mail')
        psw = request.form.get('password')
        db_name = "databaseLarovere2.db"
        with sqlite3.connect(db_name) as conn:
            cursor = conn.cursor()
            hashed_psw = hashlib.sha256(psw.encode()).hexdigest()
            cursor.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, hashed_psw))
            conn.commit()
        return redirect(url_for('login'))
    return render_template('create_account.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='9999')