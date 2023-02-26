from flask import Flask
from flask_smorest import Api

from pathlib import Path
from apispec import APISpec
import yaml

from config import BaseConfig

from api.api import blueprint

app = Flask(__name__)
app.config.from_object(BaseConfig)

kitchen_api = Api(app)
kitchen_api.register_blueprint(blueprint)

api_spec = yaml.safe_load((Path(__file__).parent / "oas.yaml").read_text())
spec = APISpec(
    title=api_spec["info"]["title"],
    version=api_spec["info"]["version"],
    openapi_version=api_spec["openapi"],
)
spec.to_dict = lambda: api_spec
kitchen_api.spec = spec
