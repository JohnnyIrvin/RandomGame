# Copyright (c) 2021 Johnathan P. Irvin
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
from fastapi import APIRouter, FastAPI, Request, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.websockets import WebSocketDisconnect
from src.api.connection_manager import ConnectionManager
from src.game import Game

route = APIRouter()

TEMPLATES = Jinja2Templates(directory="src/templates")
CONNECTION_MANAGER = ConnectionManager()
GAME = Game()

@route.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return TEMPLATES.TemplateResponse("game.html", { "request": request })

@route.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    global GAME, CONNECTION_MANAGER

    await CONNECTION_MANAGER.add_connection(websocket)

    while True:
        try:
            data = await websocket.receive_text()
        except WebSocketDisconnect:
            await CONNECTION_MANAGER.remove_connection(websocket)
            break

        if data.isnumeric():
            if GAME.guess(int(data)):
                await CONNECTION_MANAGER.broadcast(f"{data} was correct!")
                await CONNECTION_MANAGER.broadcast("Starting new game!")
            else:
                await CONNECTION_MANAGER.broadcast(f"Incorrect! You have {GAME.attempts} attempts left.")

            if GAME.is_over:
                await CONNECTION_MANAGER.broadcast(f"Game over! Answer was {GAME.answer}")
                await CONNECTION_MANAGER.broadcast("Starting new game!")
                GAME._new_game()
        else:
            await CONNECTION_MANAGER.broadcast(f"Message: {data}")

def create_api():
    api = FastAPI()
    api.include_router(route)

    return api
