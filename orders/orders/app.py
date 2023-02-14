from pathlib import Path
from fastapi import FastAPI

import yaml

app = FastAPI(debug=True, openapi_url='/openapi/orders.json',
              docs_url='/docs/orders')

oas_doc = yaml.safe_load(
    (Path(__file__).parent / '../oas.yaml').read_text()
)

app.open_api = lambda: oas_doc

from orders.api import api
