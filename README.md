# webapp.py
`webapp.py` is a Python script for running a basic web application. It is located in the `lib` directory. The entire project follows a basic best-practice structure for a single-page web application.

## Usage of webapp.py

Take a look at `app.py` for usage examples. It also allows loading `Flask` modules:

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
For PyMongo, a `MONGO_URI` must be configured under the `mongo` section. This section will appear after the first run.

The app will be available at `http://127.0.0.1:5000` by default. Open this URL in your browser to access it.