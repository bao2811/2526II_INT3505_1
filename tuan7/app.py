import os

import connexion
from dotenv import load_dotenv
from flask_cors import CORS

from db import init_db


def create_app():
    load_dotenv()
    init_db()

    cnx_app = connexion.App(__name__, specification_dir=".")
    cnx_app.add_api("openapi.yaml")

    flask_app = cnx_app.app
    CORS(flask_app)
    return cnx_app


def health_check():
    return {"status": "ok"}, 200


if __name__ == "__main__":
    app = create_app()
    port = int(os.getenv("PORT", "5000"))
    app.run(port=port, debug=True)
