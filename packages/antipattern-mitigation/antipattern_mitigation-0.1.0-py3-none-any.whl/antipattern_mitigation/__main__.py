"""Module that allows running the enrich-person service."""
import os
from .service import start_service

HOST = os.environ.get('HOST', 'localhost')
PORT = int(os.environ.get('PORT', 5000))

if __name__ == '__main__':  # pragma: no cover
    start_service(HOST, PORT)
