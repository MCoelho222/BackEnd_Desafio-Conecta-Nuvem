# import os
from src.app import app
from src.app.routes import routes

# app = create_app(os.getenv('FLASK_ENV'))
# app_on = app['app']
# print(app_on)
routes(app)

if __name__ == "__main__":
    app.run()
