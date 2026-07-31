"""
====================================================
Android Route
====================================================
"""

from flask import Blueprint
from flask import jsonify
from flask import request

from android.android_client import android_clients

android_bp = Blueprint(

    "android",

    __name__

)


@android_bp.route("/android/connect", methods=["POST"])
def connect():

    dados = request.json or {}

    device_id = dados.get("device_id")

    if not device_id:

        return jsonify({

            "success": False,

            "error": "device_id obrigatório"

        }), 400

    android_clients.connect(

        device_id,

        dados

    )

    return jsonify({

        "success": True,

        "message": "Android conectado."

    })


@android_bp.route("/android/devices", methods=["GET"])
def devices():

    return jsonify(

        android_clients.all()

    )