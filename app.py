"""
====================================================
L.I.Z.A Server
Arquivo principal
====================================================
"""

# ====================================================
# CARREGA .ENV (LOCAL)
# ====================================================

try:
    from dotenv import load_dotenv

    load_dotenv()

    print("✅ dotenv carregado.")

except ModuleNotFoundError:

    print("⚠ python-dotenv não instalado.")
    print("⚠ Usando variáveis do ambiente.")

# ====================================================
# IMPORTS
# ====================================================

from flask import Flask
from flask import jsonify

from flask_cors import CORS

from database import criar_tabela

# ====================================================
# REGISTROS
# ====================================================

import agents.registry
import plugins.registry
import listeners.logger

# ====================================================
# BLUEPRINTS
# ====================================================

from api.routes.auth import auth_bp
from api.routes.chat import chat_bp
from api.routes.command import command_bp
from api.routes.voice import voice_bp
from api.routes.image import image_bp
from api.routes.android import android_bp


def create_app():

    app = Flask(__name__)

    CORS(app)

    # ==========================================
    # BANCO
    # ==========================================

    criar_tabela()

    # ==========================================
    # BLUEPRINTS
    # ==========================================

    app.register_blueprint(auth_bp)
    app.register_blueprint(chat_bp)
    app.register_blueprint(command_bp)
    app.register_blueprint(voice_bp)
    app.register_blueprint(image_bp)
    app.register_blueprint(android_bp)

    # ==========================================
    # HOME
    # ==========================================

    @app.route("/")
    def home():

        return jsonify({

            "name": "L.I.Z.A",

            "version": "3.0",

            "status": "online",

            "developer": "Beto"

        })

    # ==========================================
    # HEALTH
    # ==========================================

    @app.route("/health")
    def health():

        return jsonify({

            "success": True,

            "server": "running"

        })

    # ==========================================
    # AGENTES
    # ==========================================

    @app.route("/agents")
    def agents():

        from agents.agent_manager import agent_manager

        return jsonify({

            "agents": list(

                agent_manager.agents.keys()

            )

        })

    return app


# ====================================================
# APP
# ====================================================

app = create_app()


# ====================================================
# MAIN
# ====================================================

if __name__ == "__main__":

    app.run(

        host="0.0.0.0",

        port=5000,

        debug=True

    )