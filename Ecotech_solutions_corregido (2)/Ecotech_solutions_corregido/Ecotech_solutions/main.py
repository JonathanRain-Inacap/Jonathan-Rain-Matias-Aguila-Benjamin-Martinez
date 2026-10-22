"""Controlador principal del sistema de gestión EcoTech Solutions.

Presenta los menús de consola y delega cada operación CRUD en funciones
pequeñas, enlazadas mediante diccionarios de despacho. Los errores de entrada
del usuario se manejan en un único punto (:func:`ejecutar_seguro`).
"""
from datetime import date
from functools import partial
from getpass import getpass
from typing import Callable, Dict

from dao.departamento_dao import DepartamentoDAO
from dao.empleado_dao import EmpleadoDAO
from dao.proyecto_dao import ProyectoDAO
from dao.registro_tiempo_dao import RegistroTiempoDAO
from dao.administrador_dao import AdministradorDAO
from modelo.departamento import Departamento
from modelo.empleado import Empleado
from modelo.proyecto import Proyecto
from modelo.registro_tiempo import RegistroTiempo
from modelo.administrador import AdministradorRRHH

Accion = Callable[[], None]
OPCION_VOLVER = "5"


# ==========================================
# MENÚS
# ==========================================
def menu_principal() -> str:
    """Muestra el menú principal y devuelve la opción elegida.

    Returns:
        Texto ingresado por el usuario.
    """
    print("\n" + "=" * 45)
    print(" 🏢 SISTEMA DE GESTIÓN ECOTECH SOLUTIONS")
    print("=" * 45)
    print("1. Gestión de Empleados")
    print("2. Gestión de Departamentos")
    print("3. Gestión de Proyectos")
    print("4. Registro de Tiempos")
    print("5. Salir del sistema")
    return input("Seleccione un módulo: ")


def sub_menu(entidad: str) -> str:
    """Muestra el submenú CRUD de una entidad y devuelve la opción elegida.

    Args:
        entidad: Nombre de la entidad gestionada (por ejemplo, ``"Empleado"``).

    Returns:
        Texto ingresado por el usuario.
    """
    print("\n" + "-" * 30)
    print(f" MÓDULO: {entidad.upper()}")
    print("-" * 30)
    print(f"1. Registrar (Crear) {entidad}")
    print(f"2. Consultar (Leer) {entidad}")
    print(f"3. Actualizar {entidad}")
    print(f"4. Eliminar {entidad}")
    print("5. Volver al Menú Principal")
    return input("Seleccione una operación CRUD: ")

def iniciar_sesion_admin():
    print("\n" + "=" * 45)
    print(" INICIO DE SESIÓN - ECOTECH SOLUTIONS")
    print("=" * 45)

    correo = input("Correo: ")
    password = getpass("Contraseña: ")

    dao = AdministradorDAO()
    administrador = dao.iniciar_sesion(correo, password)

    if administrador:
        print(f"\n✅ Bienvenido, {administrador.get_nombre()}")
        return True

    print("\n❌ Credenciales incorrectas o usuario sin permisos.")
    return False


# ==========================================
# UTILIDADES DE ENTRADA Y EJECUCIÓN
# ==========================================
def leer_entero(mensaje: str) -> int:
    """Solicita un número entero por consola.

    Args:
        mensaje: Texto que se muestra al usuario.

    Returns:
        El entero ingresado.

    Raises:
        ValueError: Si el texto ingresado no es un entero.
    """
    try:
        return int(input(mensaje))
    except ValueError:
        raise ValueError("El valor ingresado debe ser un número entero.") from None


def leer_decimal(mensaje: str) -> float:
    """Solicita un número decimal por consola.

    Args:
        mensaje: Texto que se muestra al usuario.

    Returns:
        El número ingresado.

    Raises:
        ValueError: Si el texto ingresado no es numérico.
    """
    try:
        return float(input(mensaje))
    except ValueError:
        raise ValueError("El valor ingresado debe ser numérico.") from None


def leer_fecha(mensaje: str) -> date:
    """Solicita una fecha con formato ``AAAA-MM-DD``.

    Args:
        mensaje: Texto que se muestra al usuario.

    Returns:
        La fecha ingresada.

    Raises:
        ValueError: Si el texto no cumple el formato ``AAAA-MM-DD``.
    """
    try:
        return date.fromisoformat(input(mensaje))
    except ValueError:
        raise ValueError("La fecha debe tener el formato AAAA-MM-DD.") from None


def ejecutar_seguro(accion: Accion) -> None:
    """Ejecuta una acción del menú capturando los errores de entrada.

    Centraliza el manejo de ``ValueError`` para no repetir bloques
    ``try-except`` en cada operación.

    Args:
        accion: Función sin argumentos que implementa la operación.
    """
    try:
        accion()
    except ValueError as error:
        print(f"❌ ERROR: {error}")


def ejecutar_modulo(entidad: str, acciones: Dict[str, Accion]) -> None:
    """Ejecuta el bucle de un submenú CRUD usando un diccionario de despacho.

    Args:
        entidad: Nombre de la entidad que se muestra en el submenú.
        acciones: Diccionario que asocia cada opción del menú con su acción.
    """
    while True:
        opcion = sub_menu(entidad)
        if opcion == OPCION_VOLVER:
            break
        accion = acciones.get(opcion)
        if accion is None:
            print("❌ Opción inválida.")
            continue
        ejecutar_seguro(accion)


# ==========================================
# LÓGICA DE EMPLEADOS
# ==========================================
def registrar_empleado(dao: EmpleadoDAO) -> None:
    """Solicita los datos de un empleado y lo registra mediante el DAO.

    Args:
        dao: Objeto de acceso a datos de empleados.

    Raises:
        ValueError: Si el ID, la fecha o el salario tienen un formato inválido.
    """
    print("\n-- REGISTRAR EMPLEADO --")
    nombre = input("Nombre: ")
    correo = input("Correo: ")
    password = getpass("Contraseña: ")
    direccion = input("Dirección: ")
    telefono = input("Teléfono: ")
    fecha_inicio = leer_fecha("Fecha de inicio (AAAA-MM-DD): ")
    salario = leer_decimal("Salario: ")
    id_departamento = leer_entero("ID Departamento: ")

    # El ID lo genera Oracle (columna IDENTITY en USUARIO), por eso va como None
    empleado = Empleado(
        None, nombre, correo, password, direccion, telefono, fecha_inicio, salario
    )
    dao.registrar_empleado(empleado, id_departamento)


def consultar_empleado(dao: EmpleadoDAO) -> None:
    """Consulta un empleado por ID mediante el DAO.

    Args:
        dao: Objeto de acceso a datos de empleados.
    """
    dao.obtener_empleado(leer_entero("Ingrese ID del empleado a consultar: "))


def actualizar_empleado(dao: EmpleadoDAO) -> None:
    """Actualiza el salario de un empleado mediante el DAO.

    Args:
        dao: Objeto de acceso a datos de empleados.
    """
    id_act = leer_entero("Ingrese ID del empleado a actualizar: ")
    nuevo_salario = leer_decimal("Ingrese nuevo salario: ")
    dao.actualizar_empleado(id_act, nuevo_salario)


def eliminar_empleado(dao: EmpleadoDAO) -> None:
    """Elimina un empleado por ID mediante el DAO.

    Args:
        dao: Objeto de acceso a datos de empleados.
    """
    dao.eliminar_empleado(leer_entero("Ingrese ID del empleado a eliminar: "))


def gestionar_empleados() -> None:
    """Ejecuta el módulo CRUD de empleados."""
    dao = EmpleadoDAO()
    acciones: Dict[str, Accion] = {
        "1": partial(registrar_empleado, dao),
        "2": partial(consultar_empleado, dao),
        "3": partial(actualizar_empleado, dao),
        "4": partial(eliminar_empleado, dao),
    }
    ejecutar_modulo("Empleado", acciones)


# ==========================================
# LÓGICA DE DEPARTAMENTOS
# ==========================================
def registrar_departamento(dao: DepartamentoDAO) -> None:
    """Solicita el nombre de un departamento y lo registra mediante el DAO.

    Args:
        dao: Objeto de acceso a datos de departamentos.

    Raises:
        ValueError: Si el nombre está vacío o es demasiado largo.
    """
    nombre_dep = input("Nombre del Departamento: ")
    # El ID lo genera Oracle (columna IDENTITY), por eso va como None
    dao.registrar_departamento(Departamento(None, nombre_dep))


def consultar_departamento(dao: DepartamentoDAO) -> None:
    """Consulta un departamento por ID mediante el DAO.

    Args:
        dao: Objeto de acceso a datos de departamentos.
    """
    dao.obtener_departamento(leer_entero("ID a consultar: "))


def actualizar_departamento(dao: DepartamentoDAO) -> None:
    """Cambia el nombre de un departamento mediante el DAO.

    Args:
        dao: Objeto de acceso a datos de departamentos.
    """
    id_act = leer_entero("ID del departamento a actualizar: ")
    nuevo_nombre = input("Nuevo nombre: ")
    dao.actualizar_departamento(id_act, nuevo_nombre)


def eliminar_departamento(dao: DepartamentoDAO) -> None:
    """Elimina un departamento por ID mediante el DAO.

    Args:
        dao: Objeto de acceso a datos de departamentos.
    """
    dao.eliminar_departamento(leer_entero("ID del departamento a eliminar: "))


def gestionar_departamentos() -> None:
    """Ejecuta el módulo CRUD de departamentos."""
    dao = DepartamentoDAO()
    acciones: Dict[str, Accion] = {
        "1": partial(registrar_departamento, dao),
        "2": partial(consultar_departamento, dao),
        "3": partial(actualizar_departamento, dao),
        "4": partial(eliminar_departamento, dao),
    }
    ejecutar_modulo("Departamento", acciones)


# ==========================================
# LÓGICA DE PROYECTOS
# ==========================================
def registrar_proyecto(dao: ProyectoDAO) -> None:
    """Solicita los datos de un proyecto y lo registra mediante el DAO.

    Args:
        dao: Objeto de acceso a datos de proyectos.

    Raises:
        ValueError: Si el nombre está vacío o la fecha tiene un formato inválido.
    """
    nombre = input("Nombre del Proyecto: ").strip()
    if not nombre:
        raise ValueError("El nombre del proyecto no puede estar vacío.")
    descripcion = input("Descripción: ")
    fecha_inicio = leer_fecha("Fecha de inicio (AAAA-MM-DD): ")
    # El ID lo genera Oracle (columna IDENTITY)
    dao.registrar_proyecto(Proyecto(nombre, descripcion, fecha_inicio))


def consultar_proyecto(dao: ProyectoDAO) -> None:
    """Consulta un proyecto por ID mediante el DAO.

    Args:
        dao: Objeto de acceso a datos de proyectos.
    """
    dao.obtener_proyecto(leer_entero("ID del proyecto a consultar: "))


def actualizar_proyecto(dao: ProyectoDAO) -> None:
    """Actualiza la descripción de un proyecto mediante el DAO.

    Args:
        dao: Objeto de acceso a datos de proyectos.
    """
    id_act = leer_entero("ID del proyecto a actualizar: ")
    nueva_descripcion = input("Nueva descripción: ")
    dao.actualizar_proyecto(id_act, nueva_descripcion)


def eliminar_proyecto(dao: ProyectoDAO) -> None:
    """Elimina un proyecto por ID mediante el DAO.

    Args:
        dao: Objeto de acceso a datos de proyectos.
    """
    dao.eliminar_proyecto(leer_entero("ID del proyecto a eliminar: "))


def gestionar_proyectos() -> None:
    """Ejecuta el módulo CRUD de proyectos."""
    dao = ProyectoDAO()
    acciones: Dict[str, Accion] = {
        "1": partial(registrar_proyecto, dao),
        "2": partial(consultar_proyecto, dao),
        "3": partial(actualizar_proyecto, dao),
        "4": partial(eliminar_proyecto, dao),
    }
    ejecutar_modulo("Proyecto", acciones)


# ==========================================
# LÓGICA DE REGISTRO DE TIEMPOS
# ==========================================
def leer_horas(mensaje: str) -> float:
    """Solicita las horas trabajadas en un día (mayor a 0 y máximo 24).

    Args:
        mensaje: Texto que se muestra al usuario.

    Returns:
        Las horas ingresadas.

    Raises:
        ValueError: Si no es numérico o está fuera del rango permitido.
    """
    horas = leer_decimal(mensaje)
    # Igual que la restricción ck_rt_horas de la tabla REGISTRO_TIEMPO
    if not 0 < horas <= 24:
        raise ValueError("Las horas deben ser mayores a 0 y como máximo 24.")
    return horas


def registrar_tiempo(dao: RegistroTiempoDAO) -> None:
    """Solicita los datos de un registro de horas y lo guarda mediante el DAO.

    Args:
        dao: Objeto de acceso a datos de registros de tiempo.

    Raises:
        ValueError: Si algún ID, la fecha o las horas tienen un formato inválido.
    """
    id_empleado = leer_entero("ID del Empleado: ")
    id_proyecto = leer_entero("ID del Proyecto: ")
    fecha = leer_fecha("Fecha (AAAA-MM-DD): ")
    horas = leer_horas("Horas trabajadas: ")
    descripcion = input("Descripción de la actividad: ")
    dao.registrar_tiempo(RegistroTiempo(horas, descripcion), fecha, id_empleado, id_proyecto)


def consultar_tiempo(dao: RegistroTiempoDAO) -> None:
    """Consulta un registro de tiempo por ID mediante el DAO.

    Args:
        dao: Objeto de acceso a datos de registros de tiempo.
    """
    dao.obtener_registro(leer_entero("ID del registro a consultar: "))


def actualizar_tiempo(dao: RegistroTiempoDAO) -> None:
    """Actualiza las horas de un registro de tiempo mediante el DAO.

    Args:
        dao: Objeto de acceso a datos de registros de tiempo.
    """
    id_act = leer_entero("ID del registro a actualizar: ")
    nuevas_horas = leer_horas("Nuevas horas trabajadas: ")
    dao.actualizar_horas(id_act, nuevas_horas)


def eliminar_tiempo(dao: RegistroTiempoDAO) -> None:
    """Elimina un registro de tiempo por ID mediante el DAO.

    Args:
        dao: Objeto de acceso a datos de registros de tiempo.
    """
    dao.eliminar_registro(leer_entero("ID del registro a eliminar: "))


def gestionar_tiempos() -> None:
    """Ejecuta el módulo CRUD de registro de tiempos."""
    dao = RegistroTiempoDAO()
    acciones: Dict[str, Accion] = {
        "1": partial(registrar_tiempo, dao),
        "2": partial(consultar_tiempo, dao),
        "3": partial(actualizar_tiempo, dao),
        "4": partial(eliminar_tiempo, dao),
    }
    ejecutar_modulo("Registro de Tiempo", acciones)


# ==========================================
# BUCLE PRINCIPAL DEL SISTEMA
# ==========================================
MODULOS: Dict[str, Accion] = {
    "1": gestionar_empleados,
    "2": gestionar_departamentos,
    "3": gestionar_proyectos,
    "4": gestionar_tiempos,
}
OPCION_SALIR = "5"


def main() -> None:
    """Ejecuta el bucle principal del sistema hasta que el usuario decida salir."""
    while True:
        opcion = menu_principal()
        if opcion == OPCION_SALIR:
            print("\nCerrando de forma segura el sistema EcoTech Solutions... ¡Hasta pronto!")
            break
        modulo = MODULOS.get(opcion)
        if modulo is None:
            print("\n❌ OPCIÓN NO VÁLIDA. Seleccione entre 1 y 5.")
        else:
            modulo()


if __name__ == "__main__":
    try:
        if iniciar_sesion_admin():
            main()

    except (KeyboardInterrupt, EOFError):
        print("\n\nSistema interrumpido por el usuario. ¡Hasta pronto!")