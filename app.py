"""
====================================================
L.I.Z.A Server
Arquivo principal
====================================================
"""

from flask import Flask, jsonify
from flask_cors import CORS

from database import criar_tabela

# ==========================
# BLUEPRINTS
# ==========================

from api.routes.auth import auth_bp
from api.routes.chat import chat_bp
from api.routes.command import command_bp
from api.routes.voice import voice_bp
from api.routes.image import image_bp
from api.android.android import android_bp
import listeners.logger
import plugins.registry


def create_app():

    app = Flask(__name__)

    CORS(app)

    # ==========================
    # BANCO DE DADOS
    # ==========================

    criar_tabela()

    # ==========================
    # ROTAS
    # ==========================

    app.register_blueprint(auth_bp)

    app.register_blueprint(chat_bp)

    app.register_blueprint(command_bp)

    app.register_blueprint(voice_bp)

    app.register_blueprint(image_bp)

    app.register_blueprint(android_bp)
    

    # ==========================
    # HOME
    # ==========================

    @app.route("/", methods=["GET"])
    def home():

        return jsonify({

            "name": "L.I.Z.A",

            "status": "online",

            "version": "2.0",

            "developer": "Beto"

        })

    # ==========================
    # HEALTH CHECK
    # ==========================

    @app.route("/health", methods=["GET"])
    def health():

        return jsonify({

            "success": True,

            "server": "running"

        })

    return app


# ==========================
# APP
# ==========================

app = create_app()


# ==========================
# MAIN
# ==========================

if __name__ == "__main__":

    app.run(

        host="0.0.0.0",

        port=5000,

        debug=True

    )