from lib import WebApp
import os

def setup():
    current_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.toml")
    app = WebApp(config_filename=current_file_path)

    from app import bp as app_bp
    app.environment.web.register_blueprint(app_bp, url_prefix="/")
    return app

def docker(): # docker - production
    app = setup()
    return app.make_app()

if __name__ == "__main__": # debug
    app = setup()
    app.run()
