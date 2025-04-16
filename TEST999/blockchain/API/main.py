import json
import os
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from flask import jsonify
import requests
import uvicorn
from fastapi import FastAPI, Form, Request
from fastapi.middleware.cors import CORSMiddleware

templates_dir = os.path.join(os.path.dirname(__file__), "templates")

'''
if not os.path.exists(templates_dir):
    os.makedirs(templates_dir)
'''

app = FastAPI(
    docs_url="/api/v1/docs/",
    title="Blockchain API",
    description="This is an API communication interface to the node blockchain.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas as origens
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory=templates_dir)
session = requests.Session()

class NodeAPI:
    def __init__(self):
        global app
        self.app = app

    def start(self, ip, api_port):
        app.state.api_port = api_port
        uvicorn.run(self.app, host=ip, port=api_port, log_config=None)

    def inject_node(self, injected_node):
        self.app.state.node = injected_node

@app.get("/")
async def main(request: Request):
    node = request.app.state.node

    return templates.TemplateResponse("hello.html", {
        "request": request,
        "status": node.blockchain.smart_contract_model.used_keys
    })

@app.get("/ping/", name="Healthcheck", tags=["Healthcheck"])
async def healthcheck():
    return {"success": "pong!"}

@app.get("/blockchain")
async def main(request: Request):
    node = request.app.state.node    
    return JSONResponse(content={"chain": [data.__dict__ for data in node.blockchain.chain]})

@app.post("/send_transaction")
async def send_transaction(request: Request,transactionData: str = Form(...)):
    node = request.app.state.node

    try:
        txData = json.loads(transactionData)
        node.blockchain.add_transaction(txData)
        print(txData)

        bloco = node.blockchain.create_block()
        bloco = node.send_block(bloco)

        return JSONResponse(content={"responseMessage": "bloco criado com sucesso", "block": bloco.__dict__}, status_code=200)
    
    except Exception as e:
        return JSONResponse(content={"responseMessage": str(e)}, status_code=500)

@app.get("/keys")
async def get_keys(request: Request):
    node = request.app.state.node
    return templates.TemplateResponse("matriz.html", {
        "request": request,
        "status": node.blockchain.smart_contract_model.used_keys
    })
