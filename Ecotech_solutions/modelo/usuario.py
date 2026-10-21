class Usuario:
    def __init__(self, id_usuario, nombre, correo, password):
        # Encapsulamiento estricto (atributos privados)
        self.__id = id_usuario
        self.__nombre = nombre
        self.__correo = correo
        self.__password = password

    # --------------------------------------------------------
    # Getters y Setters para acceder a los datos encapsulados
    # --------------------------------------------------------
    def get_id(self):
        return self.__id

    def get_nombre(self):
        return self.__nombre

    def set_nombre(self, nombre):
        self.__nombre = nombre

    def get_correo(self):
        return self.__correo

    def set_correo(self, correo):
        self.__correo = correo

    # Por seguridad, no creamos un getter que devuelva la contraseña, 
    # pero sí un setter por si necesita ser actualizada.
    def set_password(self, nueva_password):
        self.__password = nueva_password

    # --------------------------------------------------------
    # Métodos del negocio definidos en el diagrama UML
    # --------------------------------------------------------
    def iniciar_sesion(self, correo_ingresado, password_ingresada):
        """
        Valida las credenciales del usuario.
        Retorna True si coinciden, False en caso contrario.
        """
        if self.__correo == correo_ingresado and self.__password == password_ingresada:
            print(f"Sesión iniciada correctamente para: {self.__nombre}")
            return True
        else:
            print("Credenciales incorrectas.")
            return False

    def recuperar_password(self):
        """
        Simula la lógica para enviar un correo de recuperación.
        """
        print(f"Se ha enviado un enlace de recuperación al correo: {self.__correo}")