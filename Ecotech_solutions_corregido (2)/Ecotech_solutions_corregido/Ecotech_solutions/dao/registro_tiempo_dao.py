import oracledb
from database.conexion import ConexionDB
from modelo.registro_tiempo import RegistroTiempo

class RegistroTiempoDAO:
    def __init__(self):
        # Instanciamos la clase de conexión para interactuar con Oracle
        self.base_datos = ConexionDB()

    # ==========================================
    # CREATE (Registrar)
    # ==========================================
    def registrar_tiempo(self, registro: RegistroTiempo, fecha, id_usuario, id_proyecto):
        """Inserta un registro de horas de un empleado en un proyecto.
        El id_registro lo genera Oracle (columna IDENTITY) y se retorna."""
        conexion = self.base_datos.conectar()
        if not conexion:
            return None

        try:
            cursor = conexion.cursor()
            # id_registro es IDENTITY: no se envía, se pide de vuelta con RETURNING
            id_generado = cursor.var(oracledb.NUMBER)
            sql = """INSERT INTO registro_tiempo (fecha, horas_trabajadas, descripcion, id_usuario, id_proyecto)
                     VALUES (:1, :2, :3, :4, :5)
                     RETURNING id_registro INTO :6"""
            cursor.execute(sql, [
                fecha,
                registro.horasTrabajadas,
                registro.descripcion,
                id_usuario,
                id_proyecto,
                id_generado
            ])
            conexion.commit()
            id_registro = int(id_generado.getvalue()[0])
            print(f"Éxito: {registro.horasTrabajadas} horas registradas con ID {id_registro}.")
            return id_registro

        except oracledb.DatabaseError as e:
            error, = e.args
            conexion.rollback()
            # Código 2291: el empleado o el proyecto indicado no existe (clave foránea)
            if error.code == 2291:
                print("Error de Integridad: El empleado o el proyecto indicado no existe.")
            else:
                print(f"Error en la BD al registrar tiempo: {error.message}")
            return None
        finally:
            if 'cursor' in locals(): cursor.close()
            self.base_datos.desconectar()

    # ==========================================
    # READ (Consultar)
    # ==========================================
    def obtener_registro(self, id_registro):
        """Busca un registro de tiempo por su ID y retorna un objeto RegistroTiempo."""
        conexion = self.base_datos.conectar()
        if not conexion:
            return None

        try:
            cursor = conexion.cursor()
            sql = """SELECT TO_CHAR(fecha, 'YYYY-MM-DD'), horas_trabajadas, descripcion, id_usuario, id_proyecto
                     FROM registro_tiempo WHERE id_registro = :1"""
            cursor.execute(sql, [id_registro])
            fila = cursor.fetchone()

            if fila:
                registro_encontrado = RegistroTiempo(fila[1], fila[2])
                print(f"\n[Registro Encontrado] -> ID: {id_registro} | Fecha: {fila[0]} | Horas: {fila[1]} "
                      f"| Empleado ID: {fila[3]} | Proyecto ID: {fila[4]} | Descripción: {fila[2]}")
                return registro_encontrado
            else:
                print(f"Aviso: No existe ningún registro de tiempo con el ID {id_registro}.")
                return None

        except oracledb.DatabaseError as e:
            error, = e.args
            print(f"Error en la BD al consultar registro de tiempo: {error.message}")
            return None
        finally:
            if 'cursor' in locals(): cursor.close()
            self.base_datos.desconectar()

    # ==========================================
    # UPDATE (Actualizar)
    # ==========================================
    def actualizar_horas(self, id_registro, nuevas_horas):
        """Actualiza las horas trabajadas de un registro existente."""
        conexion = self.base_datos.conectar()
        if not conexion:
            return False

        try:
            cursor = conexion.cursor()
            sql = "UPDATE registro_tiempo SET horas_trabajadas = :1 WHERE id_registro = :2"
            cursor.execute(sql, [nuevas_horas, id_registro])
            conexion.commit()

            if cursor.rowcount > 0:
                print(f"Éxito: El registro ID {id_registro} ahora tiene {nuevas_horas} horas.")
            else:
                print(f"Aviso: No se pudo actualizar. El ID {id_registro} no existe.")
            return True

        except oracledb.DatabaseError as e:
            error, = e.args
            conexion.rollback()
            print(f"Error en la BD al actualizar registro de tiempo: {error.message}")
            return False
        finally:
            if 'cursor' in locals(): cursor.close()
            self.base_datos.desconectar()

    # ==========================================
    # DELETE (Borrar)
    # ==========================================
    def eliminar_registro(self, id_registro):
        """Elimina un registro de tiempo de la base de datos."""
        conexion = self.base_datos.conectar()
        if not conexion:
            return False

        try:
            cursor = conexion.cursor()
            sql = "DELETE FROM registro_tiempo WHERE id_registro = :1"
            cursor.execute(sql, [id_registro])
            conexion.commit()

            if cursor.rowcount > 0:
                print(f"Éxito: Registro de tiempo con ID {id_registro} eliminado.")
            else:
                print(f"Aviso: No se pudo eliminar. No existe el ID {id_registro}.")
            return True

        except oracledb.DatabaseError as e:
            error, = e.args
            conexion.rollback()
            print(f"Error en la BD al eliminar registro de tiempo: {error.message}")
            return False
        finally:
            if 'cursor' in locals(): cursor.close()
            self.base_datos.desconectar()
