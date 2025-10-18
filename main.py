#inportamos libreria de supabase para que se conecte con la base de datos
from supabase_client import test_conexion
#importamos las clases y funciones desde modelos.py
from modelos import Dueno, Mascota, Veterinario, Consulta, \
                    reporte_historial_completo, estadisticas_veterinaria

#apartado visual del menu
def mostrar_menu():
    print("\n" + "="*50)
    print("       SISTEMA DE GESTIÓN VETERINARIA ")
    print("="*50)
    print("1. Gestionar Registros ")
    print("2. Buscar pacientes por Nombre")
    print("3. Reporte de Historial Clínico")
    print("4. Ver Estadísticas")
    print("5. Listar Todos los Registros")
    print("6. Salir")
    print("="*50)

#apartado visual del submenu_registros
def mostrar_submenu_registros():
    print("\n--- GESTIÓN DE REGISTROS  ---")
    print("1. Registrar ")
    print("2. Actualizar ")
    print("3. Eliminar ")
    print("4. Volver al Menú Principal")
    print("="*50)

#apartado visual del submenu_entidades
def mostrar_submenu_entidades(accion):
    print(f"\n--- {accion.upper()} REGISTRO ---")#{accion.upper()} Se usa para crear un título de menú dinámico que siempre esté en mayúsculas.
    print("1. Dueño")
    print("2. Mascota")
    print("3. Veterinario")
    print("4. Consulta (Solo Registrar)")
    print("5. Volver")
    print("="*50)

#funciones de registros, actualizar y eliminar
def gestionar_registros_interactivo():
    while True:
        mostrar_submenu_registros()
        opcion_crud = input("Seleccione una opción (1-4): ").strip()
#crear registros        
        if opcion_crud == "1":#(opcion_crud) es una variable que almacena la elección del usuario del submenú "Gestión de Registros".
            accion = "Registrar"
            while True:
                mostrar_submenu_entidades(accion)
                opcion_entidad = input(f"¿Qué desea {accion}? (1-5): ").strip()
                if opcion_entidad == "1": registrar_dueno_interactivo()
                elif opcion_entidad == "2": registrar_mascota_interactivo()
                elif opcion_entidad == "3": registrar_veterinario_interactivo()
                elif opcion_entidad == "4": registrar_consulta_interactivo()
                elif opcion_entidad == "5": break
                else: print("Opción inválida.")
                if opcion_entidad in ["1", "2", "3", "4"]:
                    input("\nPresione Enter para continuar...")
#apartado de actualizar       
        elif opcion_crud == "2":
            accion = "Actualizar"
            while True:
                mostrar_submenu_entidades(accion)
                opcion_entidad = input(f"¿Qué desea {accion}? (1-5): ").strip()
                if opcion_entidad == "1": actualizar_dueno_interactivo()
                elif opcion_entidad == "2": actualizar_mascota_interactivo()
                elif opcion_entidad == "3": actualizar_veterinario_interactivo()
                elif opcion_entidad == "4": print("La actualización de consultas no está implementada.")
                elif opcion_entidad == "5": break
                else: print("Opción inválida.")
                if opcion_entidad in ["1", "2", "3"]:
                    input("\nPresione Enter para continuar...")
#apartado de eliminar
        elif opcion_crud == "3":
            accion = "Eliminar"
            while True:
                mostrar_submenu_entidades(accion)
                opcion_entidad = input(f"¿Qué desea {accion}? (1-5): ").strip()
                if opcion_entidad == "1": eliminar_dueno_interactivo()
                elif opcion_entidad == "2": eliminar_mascota_interactivo()
                elif opcion_entidad == "3": eliminar_veterinario_interactivo()
                elif opcion_entidad == "4": print("La eliminación de consultas no está implementada.")
                elif opcion_entidad == "5": break
                else: print("Opción inválida.")
                if opcion_entidad in ["1", "2", "3"]:
                    input("\nPresione Enter para continuar...")

        elif opcion_crud == "4":
            print("Volviendo al menú principal...")
            break
        else:
            print("Opción inválida. Intente de nuevo.")


#funcion para registrar dueños
def registrar_dueno_interactivo():
    print("\n--- REGISTRAR NUEVO DUEÑO ---")
    nombre = input("Nombre completo: ").strip()
    if not nombre:
        print("El nombre es obligatorio")
        return
    
    direccion = input("Dirección: ").strip() or None
    telefono = input("Teléfono: ").strip() or None
    email = input("Email: ").strip() or None
    
#usamos la Clase
    nuevo_dueno = Dueno(nombre, direccion, telefono, email)
    nuevo_dueno.guardar() 

#funcion para registrar mascotas
def registrar_mascota_interactivo():
    print("\n--- REGISTRAR NUEVA MASCOTA ---")
    dueños = Dueno.obtener_todos()
    if not dueños:
        print("No hay dueños registrados. Registra un dueño primero.")
        return
    
    nombre = input("Nombre de la mascota: ").strip()
    if not nombre:
        print("El nombre es obligatorio")
        return
    
    especie = input("Especie: ").strip() or None
    raza = input("Raza: ").strip() or None
    fecha_nacimiento = input("Fecha nacimiento (YYYY-MM-DD): ").strip() or None
    
    print("\nDueños disponibles:")
    for d in dueños:
        print(f"  ID: {d.id_dueno} - {d.nombre}") 
    
    try:
        id_dueno = int(input("\nID del dueño: ").strip())
        if not any(d.id_dueno == id_dueno for d in dueños):
            print("ID de dueño no válido")
            return
        
#usamos la Clase
        nueva_mascota = Mascota(nombre=nombre, especie=especie, raza=raza, 
                                fecha_nacimiento=fecha_nacimiento, id_dueno=id_dueno)
        nueva_mascota.guardar()
    except ValueError:
        print("El ID debe ser un número")

#funcion para registrar veterinario
def registrar_veterinario_interactivo():
    print("\n--- REGISTRAR NUEVO VETERINARIO ---")
    nombre = input("Nombre completo: ").strip()
    if not nombre:
        print("El nombre es obligatorio")
        return
    
    especialidad = input("Especialidad: ").strip() or None
    telefono = input("Teléfono: ").strip() or None
    email = input("Email: ").strip() or None
    
#usamos la Clase
    nuevo_vet = Veterinario(nombre, especialidad, telefono, email)
    nuevo_vet.guardar()


#funcion para registrar consultas
def registrar_consulta_interactivo():
    print("\n--- REGISTRAR CONSULTA MÉDICA ---")
    mascotas = Mascota.obtener_todas()
    if not mascotas:
        print("No hay mascotas registradas.")
        return
    
    motivo = input("Motivo de la consulta: ").strip()
    if not motivo:
        print("El motivo es obligatorio")
        return
    
    diagnostico = input("Diagnóstico: ").strip() or None
    tratamiento = input("Tratamiento: ").strip() or None
    observaciones = input("Observaciones: ").strip() or None
    
    print("\nMascotas disponibles:")
    for m in mascotas:
        dueño_nombre = m.dueno['nombre'] if m.dueno else "N/A" 
        print(f"  ID: {m.id_mascota} - {m.nombre} (Dueño: {dueño_nombre})")
    
    try:
        id_mascota = int(input("\nID de la mascota: ").strip())
        
        veterinarios = Veterinario.obtener_todos()
        id_veterinario = None
        if veterinarios:
            print("\nVeterinarios disponibles (opcional):")
            for v in veterinarios:
                print(f"  ID: {v.id_veterinario} - {v.nombre}")
            
            vet_input = input("ID del veterinario (enter para omitir): ").strip()
            if vet_input:
                id_veterinario = int(vet_input)
        
#usamos la Clase
        nueva_consulta = Consulta(id_mascota, motivo, diagnostico, tratamiento, 
                                  observaciones, id_veterinario)
        nueva_consulta.guardar()
    except ValueError:
        print("Los IDs deben ser números")

#funcion actualizar dueño
def actualizar_dueno_interactivo():
    print("\n--- ACTUALIZAR DUEÑO ---")
    try:
        id_dueno = int(input("ID del dueño a actualizar: ").strip())
        dueno = Dueno.buscar_por_id(id_dueno)
        
        if not dueno:
            print("Dueño no encontrado.")
            return

        print(f"Actualizando a: {dueno.nombre}")
        nombre = input(f"Nombre ({dueno.nombre}): ").strip() or dueno.nombre
        direccion = input(f"Dirección ({dueno.direccion}): ").strip() or dueno.direccion
        telefono = input(f"Teléfono ({dueno.telefono}): ").strip() or dueno.telefono
        email = input(f"Email ({dueno.email}): ").strip() or dueno.email
        
        dueno.nombre = nombre
        dueno.direccion = direccion
        dueno.telefono = telefono
        dueno.email = email
        dueno.guardar() 

    except ValueError:
        print("El ID debe ser un número")

#funcion actualizar mascota
def actualizar_mascota_interactivo():
    print("\n--- ACTUALIZAR MASCOTA ---")
    try:
        id_mascota = int(input("ID de la mascota a actualizar: ").strip())
        mascota = Mascota.buscar_por_id(id_mascota)
        
        if not mascota:
            print("Mascota no encontrada.")
            return

        print(f"Actualizando a: {mascota.nombre}")
        mascota.nombre = input(f"Nombre ({mascota.nombre}): ").strip() or mascota.nombre
        mascota.especie = input(f"Especie ({mascota.especie}): ").strip() or mascota.especie
        mascota.raza = input(f"Raza ({mascota.raza}): ").strip() or mascota.raza
        mascota.fecha_nacimiento = input(f"F. Nacimiento ({mascota.fecha_nacimiento}): ").strip() or mascota.fecha_nacimiento
            
        mascota.guardar()

    except ValueError:
        print("El ID debe ser un número")


#funcion actualizar veterinario
def actualizar_veterinario_interactivo():
    print("\n--- ACTUALIZAR VETERINARIO ---")
    try:
        id_vet = int(input("ID del veterinario a actualizar: ").strip())
        vet = Veterinario.buscar_por_id(id_vet)
        
        if not vet:
            print("Veterinario no encontrado.")
            return

        print(f"Actualizando a: {vet.nombre}")
        vet.nombre = input(f"Nombre ({vet.nombre}): ").strip() or vet.nombre
        vet.especialidad = input(f"Especialidad ({vet.especialidad}): ").strip() or vet.especialidad
        vet.telefono = input(f"Teléfono ({vet.telefono}): ").strip() or vet.telefono
        vet.email = input(f"Email ({vet.email}): ").strip() or vet.email
        
        vet.guardar()

    except ValueError:
        print("El ID debe ser un número")

#funcion eliminar dueño
def eliminar_dueno_interactivo():
    print("\n--- ELIMINAR DUEÑO ---")
    try:
        id_dueno = int(input("ID del dueño a eliminar: ").strip())
        if input(f"¿Seguro que desea eliminar al dueño ID {id_dueno}? (s/n): ").lower() == 's':
            Dueno.eliminar(id_dueno)
    except ValueError:
        print("El ID debe ser un número")

#funcion eliminar mascota
def eliminar_mascota_interactivo():
    print("\n--- ELIMINAR MASCOTA ---")
    try:
        id_mascota = int(input("ID de la mascota a eliminar: ").strip())
        if input(f"¿Seguro que desea eliminar la mascota ID {id_mascota}? (s/n): ").lower() == 's':
            Mascota.eliminar(id_mascota)
    except ValueError:
        print("El ID debe ser un número")


#funcion eliminar veterinario
def eliminar_veterinario_interactivo():
    print("\n--- ELIMINAR VETERINARIO ---")
    try:
        id_vet = int(input("ID del veterinario a eliminar: ").strip())
        if input(f"¿Seguro que desea eliminar al veterinario ID {id_vet}? (s/n): ").lower() == 's':
            Veterinario.eliminar(id_vet)
    except ValueError:
        print("El ID debe ser un número")


#funcion buscar por nombre
def buscar_por_nombre_interactivo():
    print("\n--- BÚSQUEDA POR NOMBRE ---")
    nombre = input("Ingrese nombre a buscar: ").strip()
    if not nombre:
        print("Debes ingresar un nombre para buscar")
        return
    
    print("\n🔍 BUSCANDO DUEÑOS...")
    dueños = Dueno.buscar_por_nombre(nombre) #usa el método de clase
    if dueños:
        for d in dueños:
            print(f"🆔 {d.id_dueno} | {d.nombre} | {d.telefono} | {d.email}")
            mascotas_del_dueño = Mascota.obtener_por_dueno(d.id_dueno)
            if mascotas_del_dueño:
                print("   Mascotas:")
                for mascota in mascotas_del_dueño:
                    print(f"     - {mascota.nombre} ({mascota.especie} - {mascota.raza})")
    else:
        print("  No se encontraron dueños")
    
    print("\n🔍 BUSCANDO MASCOTAS...")
    mascotas = Mascota.buscar_por_nombre(nombre) #usa el método de clase
    if mascotas:
        for m in mascotas:
            dueño_nombre = m.dueno['nombre'] if m.dueno else "N/A"
            print(f"  {m.id_mascota} | {m.nombre} | {m.especie} | Dueño: {dueño_nombre}")
    else:
        print("  No se encontraron mascotas")


#funcion historial
def reporte_historial_interactivo():
    print("\n--- REPORTE DE HISTORIAL CLÍNICO ---")
    mascotas = Mascota.obtener_todas()
    if not mascotas:
        print("No hay mascotas registradas")
        return
    
    print("Mascotas disponibles:")
    for m in mascotas:
        dueño_nombre = m.dueno['nombre'] if m.dueno else "N/A"
        print(f"  ID: {m.id_mascota} - {m.nombre} (Dueño: {dueño_nombre})")
    
    try:
        id_mascota = int(input("\nID de la mascota: ").strip())
        reporte = reporte_historial_completo(id_mascota) #usa la función de modelos.py
        
        if reporte:
            mascota = reporte['mascota']
            dueno = reporte['dueno']
            consultas = reporte['consultas']
            
            print(f"\nHISTORIAL CLÍNICO COMPLETO")
            print(f"Mascota: {mascota.nombre} (ID: {mascota.id_mascota})")
            print(f"Especie/Raza: {mascota.especie} / {mascota.raza}")
            print(f"F. Nacimiento: {mascota.fecha_nacimiento}")
            if dueno:
                print(f"Dueño: {dueno.nombre} | {dueno.telefono}")
            
            print(f"\nCONSULTAS REGISTRADAS: {len(consultas)}")
            for i, c in enumerate(consultas, 1):
                vet_nombre = c.veterinario['nombre'] if c.veterinario else "No asignado"
                print(f"\n  {i}. {c.fecha_consulta} | {vet_nombre}")
                print(f"      Motivo: {c.motivo}")
                print(f"      Diagnóstico: {c.diagnostico}")
                print(f"      Tratamiento: {c.tratamiento}")
                print(f"      Observaciones: {c.observaciones}")
        else:
            print("No se pudo generar el reporte")
    except ValueError:
        print("El ID debe ser un número")

#funcion ver estadisticas
def ver_estadisticas_interactivo():
    print("\n--- ESTADÍSTICAS DEL SISTEMA ---")
    stats = estadisticas_veterinaria() #usa la función de modelos.py
    
    if stats:
        print(f"Total Dueños: {stats['total_dueños']}")
        print(f"Total Mascotas: {stats['total_mascotas']}")
        print(f"Total Veterinarios: {stats['total_veterinarios']}")
        print(f"Total Consultas: {stats['total_consultas']}")
    else:
        print("No se pudieron obtener las estadísticas")

#funcion lista de registros
def listar_registros_interactivo():
    print("\n--- LISTAR TODOS LOS REGISTROS ---")
    print("1. Dueños")
    print("2. Mascotas") 
    print("3. Veterinarios")
    print("4. Consultas")
    
    opcion = input("Seleccione: ").strip()
    
    if opcion == "1":
        dueños = Dueno.obtener_todos()
        print(f"\n DUEÑOS ({len(dueños)}):")
        for d in dueños:
            print(f"  🆔 {d.id_dueno} | {d.nombre} | {d.telefono} | {d.email}")
    
    elif opcion == "2":
        mascotas = Mascota.obtener_todas()
        print(f"\n MASCOTAS ({len(mascotas)}):")
        for m in mascotas:
            dueño_nombre = m.dueno['nombre'] if m.dueno else "N/A"
            print(f"  {m.id_mascota} | {m.nombre} | {m.especie} | Dueño: {dueño_nombre}")
    
    elif opcion == "3":
        veterinarios = Veterinario.obtener_todos()
        print(f"\n VETERINARIOS ({len(veterinarios)}):")
        for v in veterinarios:
            print(f"  {v.id_veterinario} | {v.nombre} | {v.especialidad} | {v.telefono}")
    
    elif opcion == "4":
        consultas = Consulta.obtener_todas()
        print(f"\n CONSULTAS ({len(consultas)}):")
        for c in consultas:
            mascota_nombre = c.mascota['nombre'] if c.mascota else "N/A"
            vet_nombre = c.veterinario['nombre'] if c.veterinario else "No asignado"
            print(f"   {c.id_consulta} | {c.fecha_consulta} | {mascota_nombre} | {vet_nombre}")

#funcion del menu
def main():
    if not test_conexion():
        print("Saliendo del programa.")
        return
    
    print("🎉 ¡Sistema de Gestión Veterinaria conectado correctamente!")
    
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción (1-6): ").strip()
        
        if opcion == "1":
            gestionar_registros_interactivo()
        elif opcion == "2":
            buscar_por_nombre_interactivo()
        elif opcion == "3":
            reporte_historial_interactivo()
        elif opcion == "4":
            ver_estadisticas_interactivo()
        elif opcion == "5":
            listar_registros_interactivo()
        elif opcion == "6":
            print("\n ¡Gracias por usar el Sistema de Gestión Veterinaria!")
            break
        else:
            print("Opción inválida. Intente de nuevo.")
        
        input("\nPresione Enter para continuar...")

if __name__ == "__main__":
    main()