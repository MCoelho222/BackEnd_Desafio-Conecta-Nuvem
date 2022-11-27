import os
from src import app
from src.routes import routes

# app = create_app(os.getenv('FLASK_ENV'))
# app_on = app['app']
# print(app_on)
routes(app)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
