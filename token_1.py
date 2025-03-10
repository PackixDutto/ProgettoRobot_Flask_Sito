import jwt 

SECRET_KEY = ("mysecretkey")

IMPORT: 
#token = request.headers.get("Authorization")
#token = token.split(" ")[1]
decoded_token = jwt.decode(token, SECRET_KEY, algorithms = ["HS256"])
username = decoded_token["username"]

    except jwt.ExpiredSignatureError:
            return redirect(url_for("login")) #token scaduto 
    except jwt.InvalidTokenError:
            return redirect(url_for("login")) #token non valido 

Creazione:
expiration = datetime.utcnow() + timedelta(days=1)
token = jwt.encode({"username": username, "exp": expiration}, SECRET_KEY, algorithm = "HS256")
#response.headers["Authorization"] = f"Bearer {token}"

