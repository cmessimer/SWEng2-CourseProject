import jwt
from flask import Flask

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = "your_secret_key"

token = "YOUR_REAL_JWT_TOKEN"
decoded = jwt.decode(token, app.config['JWT_SECRET_KEY'], algorithms=["HS256"])
print(decoded)
