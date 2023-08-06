from fastapi import FastAPI
import os
import uvicorn
import sqlite3
import glob
from typing import Dict, Any

# CONSTANTS
# _DB_PATH = os.environ.get('DB_PATH', './cd_tasks/db/latest/latest.db')
# DB_CONNECTION = sqlite3.connect(_DB_PATH)

# create app object
app = FastAPI()

@app.get('/hello')
def get_hello() -> Dict[str, Any]:
	"""First page that say hello in style."""
	return {
		'message': 'Hello World'
	}


@app.get('/game/id/{game_id}')
def get_game_by_id(item_id: int, db_connection: Any) -> Dict[str, Any]: # mypy: ignore
	"""Find the game with given id."""
	print(type(db_connection))
	cursor = db_connection.cursor()
	cursor.execute(f'SELECT * FROM GAMES WHERE ID = {item_id}')
	rows = cursor.fetchall()
	result = rows[0]
	return {
		'ID': result[0],
		'NAME': result[1],
		'GENRE': result[2],
		'PUBLICATION_YEAR': result[3]
	}


def start_service(host: str, port: int) -> None:
	"""Enable starting service server from outside the package."""
	uvicorn.run('antipattern_mitigation.service:app', host=host, port=port)