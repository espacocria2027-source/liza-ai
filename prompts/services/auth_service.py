from database import conectar


def registrar_usuario(

    usuario: str,

    senha: str

):

    if not usuario or not senha:

        return {

            "success": False,

            "message": "Preencha usuário e senha."

        }

    try:

        conn = conectar()

        cursor = conn.cursor()

        cursor.execute(

            """
            INSERT INTO usuarios
            (usuario, senha)
            VALUES (?, ?)
            """,

            (

                usuario,

                senha

            )

        )

        conn.commit()

        conn.close()

        return {

            "success": True,

            "message": "Usuário criado com sucesso."

        }

    except Exception:

        return {

            "success": False,

            "message": "Usuário já existe."

        }


def login_usuario(

    usuario: str,

    senha: str

):

    conn = conectar()

    cursor = conn.cursor()

    cursor.execute(

        """
        SELECT *
        FROM usuarios
        WHERE usuario=?
        AND senha=?
        """,

        (

            usuario,

            senha

        )

    )

    resultado = cursor.fetchone()

    conn.close()

    if resultado:

        return {

            "success": True,

            "message": "Login realizado.",

            "usuario": usuario

        }

    return {

        "success": False,

        "message": "Usuário ou senha incorretos."

    }