class Departamento:
    """Departamento de EcoTech Solutions (mapea a la tabla DEPARTAMENTO en Oracle)."""
 
    NOMBRE_MAX_LEN = 100  # Debe coincidir con VARCHAR2(100) en la BD
 
    def __init__(self, id_departamento: int, nombre: str) -> None:
        self.__id_departamento = self._validar_id(id_departamento)
        self.__nombre = self._validar_nombre(nombre)
        self.__empleados: list = []
 
    # --- Validaciones ---
    @staticmethod
    def _validar_id(valor: int) -> int:
        # None = departamento aún no guardado (Oracle genera el id al insertarlo)
        if valor is None:
            return None
        if isinstance(valor, bool) or not isinstance(valor, int) or valor <= 0:
            raise ValueError("id_departamento debe ser un entero positivo.")
        return valor
 
    @classmethod
    def _validar_nombre(cls, valor: str) -> str:
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("El nombre no puede estar vacío.")
        valor = valor.strip()
        if len(valor) > cls.NOMBRE_MAX_LEN:
            raise ValueError(f"El nombre excede {cls.NOMBRE_MAX_LEN} caracteres.")
        return valor
 
    # --- Propiedades ---
    @property
    def id_departamento(self) -> int:
        return self.__id_departamento
 
    @id_departamento.setter
    def id_departamento(self, valor: int) -> None:
        self.__id_departamento = self._validar_id(valor)
 
    @property
    def nombre(self) -> str:
        return self.__nombre
 
    @nombre.setter
    def nombre(self, valor: str) -> None:
        self.__nombre = self._validar_nombre(valor)
 
    @property
    def empleados(self) -> tuple:
        """Vista inmutable: la lista interna no se expone."""
        return tuple(self.__empleados)
 
    @empleados.setter
    def empleados(self, valores) -> None:
        self.__empleados = list(dict.fromkeys(valores))  # copia sin duplicados
 
    # --- Operaciones ---
    def agregar_empleado(self, empleado) -> bool:
        if empleado is None or empleado in self.__empleados:
            return False
        self.__empleados.append(empleado)
        return True
 
    def eliminar_empleado(self, empleado) -> bool:
        try:
            self.__empleados.remove(empleado)
            return True
        except ValueError:
            return False
 
    def __len__(self) -> int:
        return len(self.__empleados)
 
    def __repr__(self) -> str:
        return (f"Departamento(id={self.__id_departamento}, "
                f"nombre={self.__nombre!r}, empleados={len(self)})")
 