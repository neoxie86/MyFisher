from flask import Flask
from app import create_app


app = create_app()


# app.add_url_rule('/',view_func=hello_world)

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
