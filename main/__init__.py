import datetime
import os

from flask import Flask, request
import simplejson

SITE_URL = "https://rafaelmc.net"


def create_app(test_config=None, test_mode=False):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        # DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_mode:
        stats_path = os.path.join(app.instance_path, "stats.json")
    else:
        stats_path = os.path.join("/var/lib/rafaelmc/stats.json")

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    @app.after_request
    def after_request_handler(response):
        if response.status_code == 200:
            try:
                with open(stats_path) as f:
                    stats = simplejson.loads(f.read())
            except FileNotFoundError:
                stats = {"hits": {}}

            stats["hits"][request.url] = stats["hits"].get(request.url, 0) + 1
            stats["last_updated"] = datetime.datetime.now().isoformat()

            with open(stats_path, "w") as f:
                f.write(simplejson.dumps(stats))

        return response

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    from . import blog
    from . import main

    app.register_blueprint(blog.bp)
    app.register_blueprint(main.bp)

    return app
