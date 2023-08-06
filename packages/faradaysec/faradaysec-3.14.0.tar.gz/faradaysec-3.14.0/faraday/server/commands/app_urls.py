"""
Faraday Penetration Test IDE
Copyright (C) 2013  Infobyte LLC (http://www.infobytesec.com/)
See the file 'doc/LICENSE' for the license information

"""
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from faraday.server.web import app
from faraday import __version__ as f_version
import json

from faraday.utils.faraday_openapi_plugin import FaradayAPIPlugin


def openapi_format(format="yaml", server="localhost", no_servers=False):
    extra_specs = {'info': {
        'description': 'The Faraday REST API enables you to interact with '
                       '[our server](https://github.com/infobyte/faraday).\n'
                       'Use this API to interact or integrate with Faraday'
                       ' server. This page documents the REST API, with HTTP'
                       ' response codes and example requests and responses.'},
        'security': {"ApiKeyAuth": []}
    }

    if not no_servers:
        extra_specs['servers'] = [{'url': f'https://{server}/_api'}]

    spec = APISpec(
        title="Faraday API",
        version="2",
        openapi_version="3.0.2",
        plugins=[FaradayAPIPlugin(), FlaskPlugin(), MarshmallowPlugin()],
        **extra_specs
    )
    api_key_scheme = {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization"
    }

    spec.components.security_scheme("API_KEY", api_key_scheme)
    response_401_unauthorized = {
        "description": "You are not authenticated or your API key is missing "
                       "or invalid"
    }
    spec.components.response("UnauthorizedError", response_401_unauthorized)

    with app.test_request_context():
        for endpoint in app.view_functions:
            spec.path(view=app.view_functions[endpoint], app=app)
        if format.lower() == "yaml":
            print(spec.to_yaml())
        else:
            print(json.dumps(spec.to_dict(), indent=2))


def show_all_urls():
    print(app.url_map)
