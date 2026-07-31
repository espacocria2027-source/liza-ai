"""
====================================================
Android Bridge
====================================================
"""

import uuid

from flask import Blueprint
from flask import request
from flask import jsonify

from android.execution_manager import manager


android_bp = Blueprint(

    "android",

    __name__

)


@android_bp.route("/android/result", methods=["POST"])
def result():

    dados = request.json or {}

    execution_id = dados.get("execution_id")

    manager.finish(

        execution_id,

        dados

    )

    return jsonify({

        "success": True

    })


def create_execution(package):

    execution_id = str(uuid.uuid4())

    manager.create(

        execution_id,

        package

    )

    return {

        "execution_id": execution_id,

        "package": package

    }