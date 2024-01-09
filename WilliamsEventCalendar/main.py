from website import create_app
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = create_app()


if __name__ == '__main__':
    app.run(debug=True)