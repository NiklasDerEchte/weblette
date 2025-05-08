from lib import WebApp
import os

def make_app():
    current_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.toml")
    app = WebApp(config_filename=current_file_path)

    from app import bp as app_bp
    app.environment.web.register_blueprint(app_bp, url_prefix="/")
    return app

if __name__ == "__main__":
    app = make_app()
    app.run()
