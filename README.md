# Webapp.py
`webapp.py` is a Python script for running a basic web application.

## Usage

To start the application, use the following code:

```python
from webapp import WebApp

app = WebApp()

# import custom flask-modules
app.environment.add_module("mongo", PyMongo)

# create routes
from routes import api
app.environment.web.register_blueprint(api, url_prefix='/route')

app.run()
```

The app will be available at `http://127.0.0.1:5000` by default. Open this URL in your browser to access it.
