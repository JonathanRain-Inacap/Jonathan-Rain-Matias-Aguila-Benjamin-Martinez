from modelo.empleado import Empleado
from modelo.usuario import Usuario


class AdministradorRRHH(Usuario):
    """Representa a un administrador de Recursos Humanos de EcoTech Solutions.

    Extiende a :class:`Usuario` agregando el nivel de acceso y las operaciones
    de gestión de personal. El atributo propio está encapsulado (name mangling
    con doble guion bajo) y se expone mediante una propiedad.

    Attributes:
        nivel_acceso (int): Nivel de privilegios del administrador en el sistema.
    """

    def __init__(
        self,
        id_usuario: int,
        nombre: str,
        correo: str,
        password: str,
        nivel_acceso: int,
    ) -> None:
        """Inicializa un administrador con sus datos de usuario y su nivel de acceso.

        Args:
            id_usuario: Identificador único del usuario.
            nombre: Nombre completo del administrador.
            correo: Correo electrónico del administrador.
            password: Contraseña de acceso al sistema.
            nivel_acceso: Nivel de privilegios asignado.
        """
        super().__init__(id_usuario, nombre, correo, password)
        self.__nivel_acceso = nivel_acceso

    @property
    def nivel_acceso(self) -> int:
        """int: Nivel de privilegios del administrador en el sistema."""
        return self.__nivel_acceso

    @nivel_acceso.setter
    def nivel_acceso(self, nivel_acceso: int) -> None:
        self.__nivel_acceso = nivel_acceso

    def registrar_empleado(self, empleado: Empleado) -> None:
        """Registra un nuevo empleado en el sistema.

        Args:
            empleado: Instancia de :class:`Empleado` a registrar.
        """
        print("Registrando nuevo empleado en el sistema...")

    def generar_informe(self) -> str:
        """Genera el informe de recursos humanos.

        Returns:
            Nombre del archivo del informe generado.
        """
        print("Generando informe de recursos humanos...")
        return "informe_rrhh.pdf"
    