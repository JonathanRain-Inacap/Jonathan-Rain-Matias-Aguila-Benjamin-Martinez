
import oracledb

class ConexionDB:

    def __init__(self):
        # La conexión no se abre aquí: los DAO la abren con conectar()
        # al inicio de cada operación y la cierran con desconectar() al final.
        self.conexion = None

    def conectar(self):
        """Abre la conexión a Oracle y la retorna (None si falla)."""
        try:
            self.conexion = oracledb.connect(
                user="PRUEBADEPOO",
                password="2001",
                host="localhost",
                port=1521,
                service_name="xe"
            )
            return self.conexion

        except Exception as e:
            print(f"ERROR CRÍTICO DE CONEXIÓN: Detalle: {e}")
            self.conexion = None
            return None

    def desconectar(self):
        """Cierra la conexión si está abierta."""
        if self.conexion is not None:
            try:
                self.conexion.close()
            except oracledb.Error:
                pass
            self.conexion = None
