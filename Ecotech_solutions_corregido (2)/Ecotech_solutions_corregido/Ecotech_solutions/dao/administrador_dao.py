import oracledb

from database.conexion import ConexionDB
from modelo.administrador import AdministradorRRHH


class AdministradorDAO:

    def __init__(self):
        self.base_datos = ConexionDB()

    def iniciar_sesion(self, correo, password):
        conexion = self.base_datos.conectar()

        if not conexion:
            return None

        try:
            cursor = conexion.cursor()

            sql = """
                SELECT u.id,
                       u.nombre,
                       u.correo,
                       u.password,
                       a.nivel_acceso
                FROM usuario u
                JOIN administrador_rrhh a
                    ON u.id = a.id_usuario
                WHERE u.correo = :1
                AND u.password = :2
            """

            cursor.execute(sql, [correo, password])

            fila = cursor.fetchone()

            if fila:
                administrador = AdministradorRRHH(
                    id_usuario=fila[0],
                    nombre=fila[1],
                    correo=fila[2],
                    password=fila[3],
                    nivel_acceso=fila[4]
                )

                return administrador

            return None

        except oracledb.DatabaseError as e:
            error, = e.args
            print(f"Error al iniciar sesión: {error.message}")
            return None

        finally:
            if "cursor" in locals():
                cursor.close()

            self.base_datos.desconectar()