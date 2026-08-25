# ====================================================
# L.I.Z.A. SERVER
# ====================================================


# ====================================================
# CARREGA .ENV
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

from flask import (
    Flask,
    jsonify,
    send_from_directory
)

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
from services.research.research import research_bp


# ====================================================
# APP
# ====================================================

def create_app():

    app = Flask(

        __name__,

        static_folder="web",

        static_url_path=""

    )

    CORS(app)


    # ==========================================
    # BANCO
    # ==========================================

    criar_tabela()


    # ==========================================
    # BLUEPRINTS
    # ==========================================

    app.register_blueprint(
        auth_bp
    )

    app.register_blueprint(
        chat_bp
    )

    app.register_blueprint(
        command_bp
    )

    app.register_blueprint(
        voice_bp
    )

    app.register_blueprint(
        image_bp
    )

    app.register_blueprint(
        android_bp
    )

    app.register_blueprint(
        research_bp
    )


    # ==========================================
    # FRONT-END
    # ==========================================

    @app.route("/")
    def index():

        return send_from_directory(

            app.static_folder,

            "index.html"

        )


    @app.route("/style.css")
    def style():

        return send_from_directory(

            app.static_folder,

            "style.css"

        )


    @app.route("/script.js")
    def script():

        return send_from_directory(

            app.static_folder,

            "script.js"

        )


    @app.route("/assets/<path:filename>")
    def assets(filename):

        return send_from_directory(

            "web/assets",

            filename

        )


    # ==========================================
    # HEALTH
    # ==========================================

    @app.get("/health")
    def health():

        return jsonify({

            "server": "running",

            "success": True

        }), 200


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