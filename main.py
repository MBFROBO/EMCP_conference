from typing import Union, List
from typing_extensions import Annotated

from fastapi import (
    Cookie,
    Depends,
    FastAPI,
    Query,
    WebSocket,
    WebSocketDisconnect,
    status,
    Request,
    logger
)

from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
from lib.heandler import Heandler, Solver
import time


app = FastAPI()

app.mount(
    "/ui",
    StaticFiles(directory=Path(__file__).parent.absolute() / "ui", html= True),
    name="ui",
)

templates = Jinja2Templates(directory="templates")

@app.get("/")
async def get(request:Request):
    H = Heandler()
    models = H.models()
    return templates.TemplateResponse('index.html', context={'request':request,
                                                                'models':models[0]})

class ConnectionManager:

    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_json(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()


@app.websocket("/")
async def read_root(websocket:WebSocket):
    await manager.connect(websocket)
    HEANDLER = Heandler()
    DATA = []
    try:
        while True:
            data = await websocket.receive_json()
            print(data)
            if 'model' in data.keys():
                
                SOLVER = Solver()
                
                SOLVER.SQL_variables(data['model'])

                RESISTANCE   =    data['InductResistance']
                BASE_POWER   =    data['BasePower']
                BASE_VOLTAGE =    data['BaseVoltage']
                KZ_TIME      =    data['KZ_time']
                
                SOLVER.Variable_determinate()
                DATA = SOLVER.main(IndRes   = RESISTANCE,
                                BasePower   = BASE_POWER,
                                BaseVoltage = BASE_VOLTAGE,
                                kzTime      = KZ_TIME,
                                DEBUG       = True)
                
                if DATA[0] == 0:
                    ERRORS = DATA[1]
                else:
                    ERRORS = 'None'
                
                await manager.send_personal_message({'DATA': f'{DATA[0]}',
                                                     'ERRORS':f'{ERRORS}',
                                                     'I_kz':f'{DATA[2]}',}, websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        
    except KeyError:
        pass
    except IndexError:
        pass



    
