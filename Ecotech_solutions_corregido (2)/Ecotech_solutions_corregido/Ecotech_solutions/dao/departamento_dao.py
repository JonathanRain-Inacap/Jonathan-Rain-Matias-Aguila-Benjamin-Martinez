import oracledb
from database.conexion import ConexionDB
from modelo.departamento import Departamento

class DepartamentoDAO:
    def __init__(self):
        # Instanciamos la clase de conexión para comunicarnos con Oracle
        self.base_datos = ConexionDB()

    # ==========================================
    # CREATE (Registrar)
    # ==========================================
    def registrar_departamento(self, departamento: Departamento):
        """Inserta un nuevo departamento en la base de datos.
        El id lo genera Oracle (columna IDENTITY) y se asigna al objeto."""
        conexion = self.base_datos.conectar()
        if not conexion:
            return False

        try:
            cursor = conexion.cursor()
            # id_departamento es IDENTITY: no se envía, se pide de vuelta con RETURNING
            id_generado = cursor.var(oracledb.NUMBER)
            sql = """INSERT INTO departamento (nombre) 
                     VALUES (:1)
                     RETURNING id_departamento INTO :2"""
            
            cursor.execute(sql, [departamento.nombre, id_generado])
            conexion.commit()
            departamento.id_departamento = int(id_generado.getvalue()[0])
            print(f"Éxito: Departamento '{departamento.nombre}' registrado con ID {departamento.id_departamento}.")
            return True

        except oracledb.DatabaseError as e:
            error, = e.args
            conexion.rollback()
            print(f"Error en la BD al registrar departamento: {error.message}")
            return False
        finally:
            if 'cursor' in locals(): cursor.close()
            self.base_datos.desconectar()

    # ==========================================
    # READ (Consultar)
    # ==========================================
    def obtener_departamento(self, id_departamento):
        """Busca un departamento por su ID y retorna un objeto Departamento."""
        conexion = self.base_datos.conectar()
        if not conexion:
            return None

        try:
            cursor = conexion.cursor()
            sql = "SELECT id_departamento, nombre FROM departamento WHERE id_departamento = :1"
            cursor.execute(sql, [id_departamento])
            fila = cursor.fetchone()

            if fila:
                # Instanciamos el objeto respetando la estructura del UML
                depto_encontrado = Departamento(
                    id_departamento=int(fila[0]),
                    nombre=fila[1]
                )
                print(f"\n[Departamento Encontrado] -> ID: {fila[0]} | Nombre: {fila[1]}")
                return depto_encontrado
            else:
                print(f"Aviso: No existe ningún departamento con el ID {id_departamento}.")
                return None

        except oracledb.DatabaseError as e:
            error, = e.args
            print(f"Error en la BD al consultar departamento: {error.message}")
            return None
        finally:
            if 'cursor' in locals(): cursor.close()
            self.base_datos.desconectar()

    # ==========================================
    # UPDATE (Actualizar)
    # ==========================================
    def actualizar_departamento(self, id_departamento, nuevo_nombre):
        """Actualiza el nombre de un departamento existente."""
        conexion = self.base_datos.conectar()
        if not conexion:
            return False

        try:
            cursor = conexion.cursor()
            sql = "UPDATE departamento SET nombre = :1 WHERE id_departamento = :2"
            cursor.execute(sql, [nuevo_nombre, id_departamento])
            conexion.commit()

            if cursor.rowcount > 0:
                print(f"Éxito: El departamento ID {id_departamento} ha sido renombrado a '{nuevo_nombre}'.")
            else:
                print(f"Aviso: No se pudo actualizar. El ID {id_departamento} no existe.")
            return True

        except oracledb.DatabaseError as e:
            error, = e.args
            print(f"Error en la BD al actualizar departamento: {error.message}")
            return False
        finally:
            if 'cursor' in locals(): cursor.close()
            self.base_datos.desconectar()

    # ==========================================
    # DELETE (Borrar)
    # ==========================================
    def eliminar_departamento(self, id_departamento):
        """Elimina un departamento de la base de datos."""
        conexion = self.base_datos.conectar()
        if not conexion:
            return False

        try:
            cursor = conexion.cursor()
            sql = "DELETE FROM departamento WHERE id_departamento = :1"
            cursor.execute(sql, [id_departamento])
            conexion.commit()
            
            if cursor.rowcount > 0:
                print(f"Éxito: Departamento con ID {id_departamento} eliminado.")
            else:
                print(f"Aviso: No se pudo eliminar. No existe el ID {id_departamento}.")
            return True

        except oracledb.DatabaseError as e:
            error, = e.args
            # Código de error 2292 en Oracle significa "Integrity constraint violated" (tiene empleados asignados)
            if error.code == 2292:
                print("Error de Integridad: No puedes eliminar este departamento porque aún tiene empleados asignados.")
            else:
                print(f"Error en la BD al eliminar departamento: {error.message}")
            return False
        finally:
            if 'cursor' in locals(): cursor.close()
            self.base_datos.desconectar()