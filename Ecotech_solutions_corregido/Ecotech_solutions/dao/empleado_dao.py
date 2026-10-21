import oracledb
from database.conexion import ConexionDB 
from modelo.empleado import Empleado

class EmpleadoDAO:
    def __init__(self):
        self.base_datos = ConexionDB()

    #================================================
    # CREATE (registrar)
    #================================================
    def registrar_empleado(self, Empleado):
        """
        Inserta un nuevo empleado en la base de datos de oracle.
        """
        conexion = self.base_datos.conectar()
        if not conexion:
            print("No se pudo establecer la conexión a la base de datos.")
            return False
        try:
            cursor = conexion.cursor()
            sql = """
                INSERT INTO empleados (id_usuario, nombre, correo, password, direccion, telefono, fecha_inicio, salario)
                VALUES (:id_usuario, :nombre, :correo, :password, :direccion, :telefono, :fecha_inicio, :salario)
            """
            valores = (
                Empleado.get_id(),
                Empleado.get_nombre(),
                Empleado.get_correo(),
                Empleado.get_password(),
                Empleado.get_direccion(),
                Empleado.get_telefono(),
                Empleado.get_fecha_inicio(),
                Empleado.get_salario()
            )
            
            cursor.execute(sql, valores)
            conexion.commit()
            print(f"Empleado registrado exitosamente: {Empleado.get_nombre()} registrado en la base de datos.")
            return True

        except oracledb.DatabaseError as e:
            error, = e.args
            print(f"Error al registrar empleado: {error.message}")
            return False
        finally:
            if "cursor" in locals():
                cursor.close()
            self.base_datos.desconectar()


    # ==========================================
    # READ (Consultar)
    # ==========================================
    def obtener_empleado(self, id_empleado):
        """Busca un empleado por su ID y retorna un objeto de la clase Empleado."""
        conexion = self.base_datos.conectar()
        if not conexion:
            return None

        try:
            cursor = conexion.cursor()
            sql = "SELECT * FROM empleados WHERE id_empleado = :1"
            cursor.execute(sql, [id_empleado])
            fila = cursor.fetchone() # Obtenemos el primer registro que coincida

            if fila:
                # Si encuentra los datos, instanciamos un nuevo objeto Empleado respetando el UML
                # fila = (id, nombre, correo, password, direccion, telefono, fecha_inicio, salario)
                empleado_encontrado = Empleado(
                    id_usuario=fila[0],
                    nombre=fila[1],
                    correo=fila[2],
                    password=fila[3],
                    direccion=fila[4],
                    telefono=fila[5],
                    fecha_inicio=fila[6],
                    salario=fila[7]
                )
                print(f"\n[Datos Encontrados] -> ID: {fila[0]} | Nombre: {fila[1]} | Salario: ${fila[7]}")
                return empleado_encontrado
            else:
                print(f"Aviso: No existe ningún empleado con el ID {id_empleado}.")
                return None

        except oracledb.DatabaseError as e:
            error, = e.args
            print(f"Error en la BD al consultar: {error.message}")
            return None
        finally:
            if 'cursor' in locals(): cursor.close()
            self.base_datos.desconectar()

    # ==========================================
    # UPDATE (Actualizar)
    # ==========================================
    def actualizar_empleado(self, id_empleado, nuevo_salario):
        """Actualiza el salario de un empleado existente."""
        conexion = self.base_datos.conectar()
        if not conexion:
            return False

        try:
            cursor = conexion.cursor()
            sql = "UPDATE empleados SET salario = :1 WHERE id_empleado = :2"
            cursor.execute(sql, [nuevo_salario, id_empleado])
            conexion.commit()

            if cursor.rowcount > 0:
                print(f"Éxito: El salario del empleado ID {id_empleado} ha sido actualizado a ${nuevo_salario}.")
            else:
                print(f"Aviso: No se pudo actualizar. El ID {id_empleado} no existe.")
            return True

        except oracledb.DatabaseError as e:
            error, = e.args
            print(f"Error en la BD al actualizar: {error.message}")
            return False
        finally:
            if 'cursor' in locals(): cursor.close()
            self.base_datos.desconectar()

    # ==========================================
    # DELETE (Borrar)
    # ==========================================
    def eliminar_empleado(self, id_empleado):
        """Elimina un empleado de la base de datos de manera definitiva."""
        conexion = self.base_datos.conectar()
        if not conexion:
            return False

        try:
            cursor = conexion.cursor()
            sql = "DELETE FROM empleados WHERE id_empleado = :1"
            cursor.execute(sql, [id_empleado])
            conexion.commit()
            
            if cursor.rowcount > 0:
                print(f"Éxito: Empleado con ID {id_empleado} dado de baja permanentemente.")
            else:
                print(f"Aviso: No se pudo eliminar. No existe un empleado con el ID {id_empleado}.")
            return True

        except oracledb.DatabaseError as e:
            error, = e.args
            print(f"Error en la BD al eliminar: {error.message}")
            return False
        finally:
            if 'cursor' in locals(): cursor.close()
            self.base_datos.desconectar()       