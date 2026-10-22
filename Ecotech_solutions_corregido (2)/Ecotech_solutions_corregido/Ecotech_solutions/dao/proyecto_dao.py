import oracledb
from database.conexion import ConexionDB
from modelo.proyecto import Proyecto

class ProyectoDAO:
    def __init__(self):
        # Instanciamos la clase de conexión para interactuar con Oracle
        self.base_datos = ConexionDB()

    # ==========================================
    # CREATE (Registrar)
    # ==========================================
    def registrar_proyecto(self, proyecto: Proyecto):
        """Inserta un nuevo proyecto en la base de datos.
        El id_proyecto lo genera Oracle (columna IDENTITY) y se retorna."""
        conexion = self.base_datos.conectar()
        if not conexion:
            return None

        try:
            cursor = conexion.cursor()
            # id_proyecto es IDENTITY: no se envía, se pide de vuelta con RETURNING.
            # La fecha llega como objeto date, oracledb la convierte a DATE sin TO_DATE.
            id_generado = cursor.var(oracledb.NUMBER)
            sql = """INSERT INTO proyecto (nombre, descripcion, fecha_inicio) 
                     VALUES (:1, :2, :3)
                     RETURNING id_proyecto INTO :4"""
            
            cursor.execute(sql, [
                proyecto.nombre,
                proyecto.descripcion,
                proyecto.fechaInicio,
                id_generado
            ])
            conexion.commit()
            id_proyecto = int(id_generado.getvalue()[0])
            print(f"Éxito: Proyecto '{proyecto.nombre}' registrado con ID {id_proyecto}.")
            return id_proyecto

        except oracledb.DatabaseError as e:
            error, = e.args
            conexion.rollback()
            print(f"Error en la BD al registrar el proyecto: {error.message}")
            return None
        finally:
            if 'cursor' in locals(): cursor.close()
            self.base_datos.desconectar()

    # ==========================================
    # READ (Consultar)
    # ==========================================
    def obtener_proyecto(self, id_proyecto):
        """Busca un proyecto por su ID y retorna un objeto de la clase Proyecto."""
        conexion = self.base_datos.conectar()
        if not conexion:
            return None

        try:
            cursor = conexion.cursor()
            # Usamos TO_CHAR para formatear la fecha al extraerla de Oracle
            sql = """SELECT nombre, descripcion, TO_CHAR(fecha_inicio, 'YYYY-MM-DD') 
                     FROM proyecto WHERE id_proyecto = :1"""
            cursor.execute(sql, [id_proyecto])
            fila = cursor.fetchone()

            if fila:
                # Instanciamos el objeto Proyecto respetando el diagrama UML
                proyecto_encontrado = Proyecto(fila[0], fila[1], fila[2])
                print(f"\n[Proyecto Encontrado] -> Nombre: {fila[0]} | Fecha Inicio: {fila[2]}")
                return proyecto_encontrado
            else:
                print(f"Aviso: No existe ningún proyecto con el ID {id_proyecto}.")
                return None

        except oracledb.DatabaseError as e:
            error, = e.args
            print(f"Error en la BD al consultar el proyecto: {error.message}")
            return None
        finally:
            if 'cursor' in locals(): cursor.close()
            self.base_datos.desconectar()

    # ==========================================
    # UPDATE (Actualizar)
    # ==========================================
    def actualizar_proyecto(self, id_proyecto, nueva_descripcion):
        """Actualiza la descripción de un proyecto existente."""
        conexion = self.base_datos.conectar()
        if not conexion:
            return False

        try:
            cursor = conexion.cursor()
            sql = "UPDATE proyecto SET descripcion = :1 WHERE id_proyecto = :2"
            cursor.execute(sql, [nueva_descripcion, id_proyecto])
            conexion.commit()

            if cursor.rowcount > 0:
                print(f"Éxito: La descripción del proyecto ID {id_proyecto} ha sido actualizada.")
            else:
                print(f"Aviso: No se pudo actualizar. El ID {id_proyecto} no existe.")
            return True

        except oracledb.DatabaseError as e:
            error, = e.args
            conexion.rollback()
            print(f"Error en la BD al actualizar el proyecto: {error.message}")
            return False
        finally:
            if 'cursor' in locals(): cursor.close()
            self.base_datos.desconectar()

    # ==========================================
    # DELETE (Borrar)
    # ==========================================
    def eliminar_proyecto(self, id_proyecto):
        """Elimina un proyecto de la base de datos."""
        conexion = self.base_datos.conectar()
        if not conexion:
            return False

        try:
            cursor = conexion.cursor()
            sql = "DELETE FROM proyecto WHERE id_proyecto = :1"
            cursor.execute(sql, [id_proyecto])
            conexion.commit()
            
            if cursor.rowcount > 0:
                print(f"Éxito: Proyecto con ID {id_proyecto} eliminado.")
            else:
                print(f"Aviso: No se pudo eliminar. No existe el ID {id_proyecto}.")
            return True

        except oracledb.DatabaseError as e:
            error, = e.args
            conexion.rollback()
            # Código 2292: el proyecto tiene horas registradas o empleados asignados
            if error.code == 2292:
                print("Error de Integridad: No puedes eliminar este proyecto porque tiene horas registradas o empleados asignados.")
            else:
                print(f"Error en la BD al eliminar el proyecto: {error.message}")
            return False
        finally:
            if 'cursor' in locals(): cursor.close()
            self.base_datos.desconectar()