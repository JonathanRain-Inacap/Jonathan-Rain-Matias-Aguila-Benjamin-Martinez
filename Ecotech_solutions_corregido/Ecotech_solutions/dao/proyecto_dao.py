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
    def registrar_proyecto(self, id_proyecto, proyecto: Proyecto):
        """Inserta un nuevo proyecto en la base de datos."""
        conexion = self.base_datos.conectar()
        if not conexion:
            return False

        try:
            cursor = conexion.cursor()
            # Se usa TO_DATE para asegurar que Oracle entienda el formato de la fecha insertada
            sql = """INSERT INTO proyectos (id_proyecto, nombre, descripcion, fecha_inicio) 
                     VALUES (:1, :2, :3, TO_DATE(:4, 'YYYY-MM-DD'))"""
            
            # Extraemos los datos encapsulados del objeto usando los getters
            valores = (
                id_proyecto,
                proyecto.get_nombre(),
                proyecto.get_descripcion(),
                proyecto.get_fecha_inicio()
            )
            
            cursor.execute(sql, valores)
            conexion.commit()
            print(f"Éxito: Proyecto '{proyecto.get_nombre()}' registrado correctamente.")
            return True

        except oracledb.DatabaseError as e:
            error, = e.args
            print(f"Error en la BD al registrar el proyecto: {error.message}")
            return False
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
                     FROM proyectos WHERE id_proyecto = :1"""
            cursor.execute(sql, [id_proyecto])
            fila = cursor.fetchone()

            if fila:
                # Instanciamos el objeto Proyecto respetando el diagrama UML
                proyecto_encontrado = Proyecto(
                    nombre=fila[0],
                    descripcion=fila[1],
                    fecha_inicio=fila[2]
                )
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
            sql = "UPDATE proyectos SET descripcion = :1 WHERE id_proyecto = :2"
            cursor.execute(sql, [nueva_descripcion, id_proyecto])
            conexion.commit()

            if cursor.rowcount > 0:
                print(f"Éxito: La descripción del proyecto ID {id_proyecto} ha sido actualizada.")
            else:
                print(f"Aviso: No se pudo actualizar. El ID {id_proyecto} no existe.")
            return True

        except oracledb.DatabaseError as e:
            error, = e.args
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
            sql = "DELETE FROM proyectos WHERE id_proyecto = :1"
            cursor.execute(sql, [id_proyecto])
            conexion.commit()
            
            if cursor.rowcount > 0:
                print(f"Éxito: Proyecto con ID {id_proyecto} eliminado.")
            else:
                print(f"Aviso: No se pudo eliminar. No existe el ID {id_proyecto}.")
            return True

        except oracledb.DatabaseError as e:
            error, = e.args
            print(f"Error en la BD al eliminar el proyecto: {error.message}")
            return False
        finally:
            if 'cursor' in locals(): cursor.close()
            self.base_datos.desconectar()