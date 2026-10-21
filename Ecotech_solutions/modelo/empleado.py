from datetime import date

from modelo.usuario import Usuario


class Empleado(Usuario):
    """Representa a un empleado del sistema EcoTech Solutions.

    Extiende a :class:`Usuario` agregando los datos laborales y de contacto
    propios del empleado. Los atributos adicionales están encapsulados
    (name mangling con doble guion bajo) y se exponen mediante propiedades.

    Attributes:
        direccion (str): Domicilio del empleado.
        telefono (str): Teléfono de contacto.
        fecha_inicio (date): Fecha de inicio de la relación laboral.
        salario (float): Remuneración del empleado.
    """

    def __init__(
        self,
        id_usuario: int,
        nombre: str,
        correo: str,
        password: str,
        direccion: str,
        telefono: str,
        fecha_inicio: date,
        salario: float,
    ) -> None:
        """Inicializa un empleado con sus datos de usuario y laborales.

        Args:
            id_usuario: Identificador único del usuario.
            nombre: Nombre completo del empleado.
            correo: Correo electrónico del empleado.
            password: Contraseña de acceso al sistema.
            direccion: Domicilio del empleado.
            telefono: Teléfono de contacto.
            fecha_inicio: Fecha de inicio laboral.
            salario: Remuneración del empleado.
        """
        super().__init__(id_usuario, nombre, correo, password)
        self.__direccion = direccion
        self.__telefono = telefono
        self.__fecha_inicio = fecha_inicio
        self.__salario = salario

    @property
    def direccion(self) -> str:
        """str: Domicilio del empleado."""
        return self.__direccion

    @direccion.setter
    def direccion(self, direccion: str) -> None:
        self.__direccion = direccion

    @property
    def telefono(self) -> str:
        """str: Teléfono de contacto del empleado."""
        return self.__telefono

    @telefono.setter
    def telefono(self, telefono: str) -> None:
        self.__telefono = telefono

    @property
    def fecha_inicio(self) -> date:
        """date: Fecha de inicio de la relación laboral."""
        return self.__fecha_inicio

    @fecha_inicio.setter
    def fecha_inicio(self, fecha_inicio: date) -> None:
        self.__fecha_inicio = fecha_inicio

    @property
    def salario(self) -> float:
        """float: Remuneración del empleado."""
        return self.__salario

    @salario.setter
    def salario(self, salario: float) -> None:
        self.__salario = salario

    def registrar_tiempo(self, horas: float, descripcion: str, proyecto: str) -> None:
        """Registra horas trabajadas por el empleado en un proyecto.

        Args:
            horas: Cantidad de horas trabajadas.
            descripcion: Detalle de la actividad realizada.
            proyecto: Nombre del proyecto al que se imputan las horas.
        """
        print(f"Registrando {horas} horas en el proyecto {proyecto}")

    def consultar_departamento(self) -> None:
        """Consulta el departamento asignado al empleado.

        Returns:
            None. Pendiente de implementar: debería devolver el departamento
            cuando exista la relación con la clase correspondiente.
        """
        print("Consultando departamento asignado...")
        return None