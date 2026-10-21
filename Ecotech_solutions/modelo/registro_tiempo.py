class RegistroTiempo:
    def __init__(self, horasTrabajadas, descripcion):
        self.horasTrabajadas = horasTrabajadas
        self.descripcion = descripcion
        self.empleado = None

#Registrar un empleado asociado al registro de tiempo
    def registrarEmpleado(self, empleado):
        self.empleado = empleado

# Generar un informe del registro de tiempo
    def generarInforme(self, empleado):
        return f"Empleado: {empleado.nombre} - Horas: {self.horasTrabajadas} - {self.descripcion}"