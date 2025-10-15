from supabase_client import test_conexion
from operaciones import *

def mostrar_menu():
    print("\n" + "="*50)
    print("       SISTEMA DE GESTIÓN VETERINARIA")
    print("="*50)
    print("1. Registrar Dueño")
    print("2. Registrar Mascota")
    print("3. Registrar Veterinario")
    print("4. Registrar Consulta Médica")
    print("5. Buscar por Nombre")
    print("6. Reporte de Historial Clínico")
    print("7. Ver Estadísticas")
    print("8. Listar Todos los Registros")
    print("9. Salir")
    print("="*50)

def registrar_dueno_interactivo():
    print("\n--- REGISTRAR NUEVO DUEÑO ---")
    nombre = input("Nombre completo: ").strip()
    if not nombre:
        print("El nombre es obligatorio")
        return
    
    direccion = input("Dirección: ").strip() or None
    telefono = input("Teléfono: ").strip() or None
    email = input("Email: ").strip() or None
    
    crear_dueno(nombre, direccion, telefono, email)

def registrar_mascota_interactivo():
    print("\n--- REGISTRAR NUEVA MASCOTA ---")
    
    # Verificar que hay dueños registrados
    dueños = obtener_duenos()
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
    
    # Mostrar dueños disponibles
    print("\nDueños disponibles:")
    for d in dueños:
        print(f"  ID: {d['id_dueno']} - {d['nombre']}")
    
    try:
        id_dueno = int(input("\nID del dueño: ").strip())
        
        # Verificar que el dueño existe
        dueño_existe = any(d['id_dueno'] == id_dueno for d in dueños)
        if not dueño_existe:
            print("ID de dueño no válido")
            return
            
        crear_mascota(nombre, especie, raza, fecha_nacimiento, id_dueno)
    except ValueError:
        print("El ID debe ser un número")

def registrar_veterinario_interactivo():
    print("\n--- REGISTRAR NUEVO VETERINARIO ---")
    nombre = input("Nombre completo: ").strip()
    if not nombre:
        print("El nombre es obligatorio")
        return
    
    especialidad = input("Especialidad: ").strip() or None
    telefono = input("Teléfono: ").strip() or None
    email = input("Email: ").strip() or None
    
    crear_veterinario(nombre, especialidad, telefono, email)

def registrar_consulta_interactivo():
    print("\n--- REGISTRAR CONSULTA MÉDICA ---")
    
    # Verificar que hay mascotas registradas
    mascotas = obtener_mascotas()
    if not mascotas:
        print("No hay mascotas registradas. Registra una mascota primero.")
        return
    
    motivo = input("Motivo de la consulta: ").strip()
    if not motivo:
        print("El motivo es obligatorio")
        return
    
    diagnostico = input("Diagnóstico: ").strip() or None
    tratamiento = input("Tratamiento: ").strip() or None
    observaciones = input("Observaciones: ").strip() or None
    
    # Mostrar mascotas disponibles
    print("\nMascotas disponibles:")
    for m in mascotas:
        dueño_nombre = m['dueno']['nombre'] if m['dueno'] else "N/A"
        print(f"  ID: {m['id_mascota']} - {m['nombre']} (Dueño: {dueño_nombre})")
    
    try:
        id_mascota = int(input("\nID de la mascota: ").strip())
        
        # Verificar veterinarios disponibles
        veterinarios = obtener_veterinarios()
        id_veterinario = None
        if veterinarios:
            print("\nVeterinarios disponibles (opcional):")
            for v in veterinarios:
                print(f"  ID: {v['id_veterinario']} - {v['nombre']}")
            
            vet_input = input("ID del veterinario (enter para omitir): ").strip()
            if vet_input:
                id_veterinario = int(vet_input)
        
        crear_consulta(motivo, diagnostico, tratamiento, observaciones, id_mascota, id_veterinario)
    except ValueError:
        print("Los IDs deben ser números")

def buscar_por_nombre_interactivo():
    print("\n--- BÚSQUEDA POR NOMBRE ---")
    nombre = input("Ingrese nombre a buscar: ").strip()
    if not nombre:
        print("Debes ingresar un nombre para buscar")
        return
    
    print("\n🔍 BUSCANDO DUEÑOS...")
    dueños = buscar_dueno_por_nombre(nombre)
    if dueños:
        for d in dueños:
            mascotas_del_dueño = obtener_mascotas_por_dueno(d['id_dueno'])
            print(f"{d['id_dueno']} | {d['nombre']} | {d['telefono']} | {d['email']}")
            if mascotas_del_dueño:
                print("   Mascotas:")
                for mascota in mascotas_del_dueño:
                    print(f"     - {mascota['nombre']} ({mascota['especie']} - {mascota['raza']})")
            else:
                print("   No tiene mascotas registradas")
            print()
    else:
        print("  No se encontraron dueños")
    
    print("\n🔍 BUSCANDO MASCOTAS...")
    mascotas = buscar_mascota_por_nombre(nombre)
    if mascotas:
        for m in mascotas:
            dueño_nombre = m['dueno']['nombre'] if m['dueno'] else "N/A"
            print(f" {m['id_mascota']} | {m['nombre']} | {m['especie']} | Dueño: {dueño_nombre}")
    else:
        print("  No se encontraron mascotas")

def reporte_historial_interactivo():
    print("\n--- REPORTE DE HISTORIAL CLÍNICO ---")
    
    mascotas = obtener_mascotas()
    if not mascotas:
        print("No hay mascotas registradas")
        return
    
    print("Mascotas disponibles:")
    for m in mascotas:
        dueño_nombre = m['dueno']['nombre'] if m['dueno'] else "N/A"
        print(f"  ID: {m['id_mascota']} - {m['nombre']} (Dueño: {dueño_nombre})")
    
    try:
        id_mascota = int(input("\nID de la mascota: ").strip())
        reporte = reporte_historial_completo(id_mascota)
        
        if reporte:
            mascota = reporte['mascota']
            dueno = reporte['dueno']
            consultas = reporte['consultas']
            
            print(f"\nHISTORIAL CLÍNICO COMPLETO")
            print(f"Mascota: {mascota['nombre']} (ID: {mascota['id_mascota']})")
            print(f"Especie/Raza: {mascota['especie']} / {mascota['raza']}")
            print(f"F. Nacimiento: {mascota['fecha_nacimiento']}")
            print(f"Dueño: {dueno['nombre']} | {dueno['telefono']}")
            
            print(f"\nCONSULTAS REGISTRADAS: {len(consultas)}")
            for i, c in enumerate(consultas, 1):
                vet_nombre = c['veterinario']['nombre'] if c['veterinario'] else "No asignado"
                print(f"\n  {i}. {c['fecha_consulta']} | {vet_nombre}")
                print(f"      Motivo: {c['motivo']}")
                print(f"      Diagnóstico: {c['diagnostico']}")
                print(f"      Tratamiento: {c['tratamiento']}")
                print(f"      Observaciones: {c['observaciones']}")
        else:
            print("No se pudo generar el reporte")
    except ValueError:
        print("El ID debe ser un número")

def ver_estadisticas_interactivo():
    print("\n--- ESTADÍSTICAS DEL SISTEMA ---")
    stats = estadisticas_veterinaria()
    
    if stats:
        print(f"Total Dueños: {stats['total_dueños']}")
        print(f"Total Mascotas: {stats['total_mascotas']}")
        print(f"Total Veterinarios: {stats['total_veterinarios']}")
        print(f"Total Consultas: {stats['total_consultas']}")
    else:
        print("No se pudieron obtener las estadísticas")

def listar_registros_interactivo():
    print("\n--- LISTAR TODOS LOS REGISTROS ---")
    print("1. Dueños")
    print("2. Mascotas") 
    print("3. Veterinarios")
    print("4. Consultas")
    
    opcion = input("Seleccione: ").strip()
    
    if opcion == "1":
        dueños = obtener_duenos()
        print(f"\n DUEÑOS ({len(dueños)}):")
        for d in dueños:
            print(f"  🆔 {d['id_dueno']} | {d['nombre']} | {d['telefono']} | {d['email']}")
    
    elif opcion == "2":
        mascotas = obtener_mascotas()
        print(f"\n MASCOTAS ({len(mascotas)}):")
        for m in mascotas:
            dueño_nombre = m['dueno']['nombre'] if m['dueno'] else "N/A"
            print(f"  {m['id_mascota']} |  {m['nombre']} |  {m['especie']} |  Dueño: {dueño_nombre}")
    
    elif opcion == "3":
        veterinarios = obtener_veterinarios()
        print(f"\n VETERINARIOS ({len(veterinarios)}):")
        for v in veterinarios:
            print(f"  {v['id_veterinario']} | {v['nombre']} | {v['especialidad']} | {v['telefono']}")
    
    elif opcion == "4":
        consultas = obtener_todas_consultas()
        print(f"\n CONSULTAS ({len(consultas)}):")
        for c in consultas:
            mascota_nombre = c['mascota']['nombre'] if c['mascota'] else "N/A"
            vet_nombre = c['veterinario']['nombre'] if c['veterinario'] else "No asignado"
            print(f"   {c['id_consulta']} | {c['fecha_consulta']} | {mascota_nombre} | {vet_nombre}")

def main():
    # Verificar conexión
    if not test_conexion():
        print("No se pudo conectar a la base de datos. Verifica tu conexión y credenciales.")
        return
    
    print("🎉 ¡Sistema de Gestión Veterinaria conectado correctamente!")
    
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción (1-9): ").strip()
        
        if opcion == "1":
            registrar_dueno_interactivo()
        elif opcion == "2":
            registrar_mascota_interactivo()
        elif opcion == "3":
            registrar_veterinario_interactivo()
        elif opcion == "4":
            registrar_consulta_interactivo()
        elif opcion == "5":
            buscar_por_nombre_interactivo()
        elif opcion == "6":
            reporte_historial_interactivo()
        elif opcion == "7":
            ver_estadisticas_interactivo()
        elif opcion == "8":
            listar_registros_interactivo()
        elif opcion == "9":
            print("\n ¡Gracias por usar el Sistema de Gestión Veterinaria!")
            break
        else:
            print("Opción inválida. Intente de nuevo.")
        
        input("\nPresione Enter para continuar...")

if __name__ == "__main__":
    main()
