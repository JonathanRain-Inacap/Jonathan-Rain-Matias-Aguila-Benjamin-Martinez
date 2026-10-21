class Proyecto:

    def __init__(self,nombre,descripcion,fechaInicio):
        self.nombre = nombre
        self.descripcion = descripcion
        self.fechaInicio = fechaInicio

#Asignar empleado
    def asignarEmpleado(self, empleado):
        if empleado not in self.empleados:
            self.empleados.append(empleado)

#Desasignar empleado
    def desasignarEmpleado(self, empleado):
        if empleado in self.empleados:
            self.empleados.remove(empleado)