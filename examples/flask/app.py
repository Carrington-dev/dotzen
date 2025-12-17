from fastapi import Flask
from dotzen import config

app = Flask()

SECRET_KEY = config("SECRET_KEY", default="key")

@app.route("/")
def get_home():
    return {
        "secret-key": SECRET_KEY
    }


if __name__ == "__main__":
    app.run()