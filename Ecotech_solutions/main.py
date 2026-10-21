"""Controlador principal del sistema de gestión EcoTech Solutions.

Presenta los menús de consola y delega cada operación CRUD en funciones
pequeñas, enlazadas mediante diccionarios de despacho. Los errores de entrada
del usuario se manejan en un único punto (:func:`ejecutar_seguro`).
"""
from datetime import date
from functools import partial
from getpass import getpass
from typing import Callable, Dict

from dao.empleado_dao import EmpleadoDAO
from modelo.departamento import Departamento
from modelo.empleado import Empleado

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


def accion_simulada(mensaje: str) -> Accion:
    """Crea una acción que solo imprime un mensaje (operación aún no implementada).

    Args:
        mensaje: Texto que mostrará la acción al ejecutarse.

    Returns:
        Función sin argumentos lista para usarse en un diccionario de despacho.
    """
    def accion() -> None:
        print(mensaje)

    return accion


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
    id_emp = leer_entero("ID Empleado: ")
    nombre = input("Nombre: ")
    correo = input("Correo: ")
    password = getpass("Contraseña: ")
    direccion = input("Dirección: ")
    telefono = input("Teléfono: ")
    fecha_inicio = leer_fecha("Fecha de inicio (AAAA-MM-DD): ")
    salario = leer_decimal("Salario: ")

    empleado = Empleado(
        id_emp, nombre, correo, password, direccion, telefono, fecha_inicio, salario
    )
    dao.registrar_empleado(empleado)


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
def registrar_departamento() -> None:
    """Solicita los datos de un departamento y lo crea en memoria.

    Raises:
        ValueError: Si el ID no es numérico.
    """
    id_dep = leer_entero("ID Departamento: ")
    nombre_dep = input("Nombre del Departamento: ")
    Departamento(id_dep, nombre_dep)
    # TODO: dao.registrar_departamento(departamento) cuando exista DepartamentoDAO.
    print(f"✅ Departamento '{nombre_dep}' creado en memoria.")


def consultar_departamento() -> None:
    """Simula la consulta de un departamento por ID.

    Raises:
        ValueError: Si el ID no es numérico.
    """
    id_buscar = leer_entero("ID a consultar: ")
    print(f"🔍 Buscando departamento {id_buscar}...")


def gestionar_departamentos() -> None:
    """Ejecuta el módulo CRUD de departamentos."""
    acciones: Dict[str, Accion] = {
        "1": registrar_departamento,
        "2": consultar_departamento,
        "3": accion_simulada("✏️ Simulando actualización de departamento..."),
        "4": accion_simulada("🗑️ Simulando eliminación de departamento..."),
    }
    ejecutar_modulo("Departamento", acciones)


# ==========================================
# LÓGICA DE PROYECTOS Y TIEMPO (pendientes)
# ==========================================
def gestionar_proyectos() -> None:
    """Ejecuta el módulo de proyectos (operaciones simuladas)."""
    simulada = accion_simulada("⚙️ Ejecutando acción de Proyecto (Simulación)...")
    ejecutar_modulo("Proyecto", {opcion: simulada for opcion in "1234"})


def gestionar_tiempos() -> None:
    """Ejecuta el módulo de registro de tiempos (operaciones simuladas)."""
    simulada = accion_simulada("⏳ Ejecutando acción de Registro de Tiempo (Simulación)...")
    ejecutar_modulo("Registro de Tiempo", {opcion: simulada for opcion in "1234"})


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
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n\nSistema interrumpido por el usuario. ¡Hasta pronto!")


