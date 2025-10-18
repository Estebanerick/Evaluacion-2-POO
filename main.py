from supabase_client import test_conexion, db_connection
from models import Owner, Pet, Veterinarian, Consultation, VeterinarySystem

class VeterinaryMenu:
    """Clase para manejar el menú interactivo del sistema veterinario"""
    
    def __init__(self):
        self.system = VeterinarySystem()
    
    def show_main_menu(self):
        print("\n" + "="*50)
        print("       SISTEMA DE GESTIÓN VETERINARIA")
        print("="*50)
        print("1. Gestionar Registros")
        print("2. Buscar por Nombre")
        print("3. Reporte de Historial Clínico")
        print("4. Ver Estadísticas")
        print("5. Listar Todos los Registros")
        print("6. Salir")
        print("="*50)
    
    def show_records_submenu(self):
        print("\n--- GESTIÓN DE REGISTROS ---")
        print("1. Registrar Dueño")
        print("2. Registrar Mascota")
        print("3. Registrar Veterinario")
        print("4. Registrar Consulta Médica")
        print("5. Volver al Menú Principal")
        print("="*50)
    
    def manage_records_interactive(self):
        while True:
            self.show_records_submenu()
            opcion = input("Seleccione una opción (1-5): ").strip()

            if opcion == "1":
                self.register_owner_interactive()
            elif opcion == "2":
                self.register_pet_interactive()
            elif opcion == "3":
                self.register_veterinarian_interactive()
            elif opcion == "4":
                self.register_consultation_interactive()
            elif opcion == "5":
                print("Volviendo al menú principal...")
                break
            else:
                print("Opción inválida. Intente de nuevo.")
            
            input("\nPresione Enter para continuar...")
    
    def register_owner_interactive(self):
        print("\n--- REGISTRAR NUEVO DUEÑO ---")
        nombre = input("Nombre completo: ").strip()
        if not nombre:
            print("El nombre es obligatorio")
            return
        
        direccion = input("Dirección: ").strip() or None
        telefono = input("Teléfono: ").strip() or None
        email = input("Email: ").strip() or None
        
        owner = Owner(nombre=nombre, direccion=direccion, telefono=telefono, email=email)
        owner.save()
    
    def register_pet_interactive(self):
        print("\n--- REGISTRAR NUEVA MASCOTA ---")
        
        # Verificar que hay dueños registrados
        owners = Owner.get_all()
        if not owners:
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
        for owner in owners:
            print(f"  ID: {owner.id_dueno} - {owner.nombre}")
        
        try:
            id_dueno = int(input("\nID del dueño: ").strip())
            
            # Verificar que el dueño existe
            owner_exists = any(owner.id_dueno == id_dueno for owner in owners)
            if not owner_exists:
                print("ID de dueño no válido")
                return
                
            pet = Pet(nombre=nombre, especie=especie, raza=raza, 
                     fecha_nacimiento=fecha_nacimiento, id_dueno=id_dueno)
            pet.save()
        except ValueError:
            print("El ID debe ser un número")
    
    def register_veterinarian_interactive(self):
        print("\n--- REGISTRAR NUEVO VETERINARIO ---")
        nombre = input("Nombre completo: ").strip()
        if not nombre:
            print("El nombre es obligatorio")
            return
        
        especialidad = input("Especialidad: ").strip() or None
        telefono = input("Teléfono: ").strip() or None
        email = input("Email: ").strip() or None
        
        vet = Veterinarian(nombre=nombre, especialidad=especialidad, 
                          telefono=telefono, email=email)
        vet.save()
    
    def register_consultation_interactive(self):
        print("\n--- REGISTRAR CONSULTA MÉDICA ---")
        
        # Verificar que hay mascotas registradas
        pets = Pet.get_all()
        if not pets:
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
        for pet in pets:
            owner_name = pet.owner_data.get('nombre', 'N/A') if pet.owner_data else "N/A"
            print(f"  ID: {pet.id_mascota} - {pet.nombre} (Dueño: {owner_name})")
        
        try:
            id_mascota = int(input("\nID de la mascota: ").strip())
            
            # Verificar veterinarios disponibles
            veterinarians = Veterinarian.get_all()
            id_veterinario = None
            if veterinarians:
                print("\nVeterinarios disponibles (opcional):")
                for vet in veterinarians:
                    print(f"  ID: {vet.id_veterinario} - {vet.nombre}")
                
                vet_input = input("ID del veterinario (enter para omitir): ").strip()
                if vet_input:
                    id_veterinario = int(vet_input)
            
            consultation = Consultation(motivo=motivo, diagnostico=diagnostico, 
                                      tratamiento=tratamiento, observaciones=observaciones,
                                      id_mascota=id_mascota, id_veterinario=id_veterinario)
            consultation.save()
        except ValueError:
            print("Los IDs deben ser números")
    
    def search_by_name_interactive(self):
        print("\n--- BÚSQUEDA POR NOMBRE ---")
        nombre = input("Ingrese nombre a buscar: ").strip()
        if not nombre:
            print("Debes ingresar un nombre para buscar")
            return
        
        print("\n🔍 BUSCANDO DUEÑOS...")
        owners = Owner.search_by_name(nombre)
        if owners:
            for owner in owners:
                print(f"{owner.id_dueno} | {owner.nombre} | {owner.telefono} | {owner.email}")
                pets = owner.get_pets()
                if pets:
                    print("   Mascotas:")
                    for pet in pets:
                        print(f"     - {pet.nombre} ({pet.especie} - {pet.raza})")
                else:
                    print("   No tiene mascotas registradas")
                print()
        else:
            print("  No se encontraron dueños")
        
        print("\n🔍 BUSCANDO MASCOTAS...")
        pets = Pet.search_by_name(nombre)
        if pets:
            for pet in pets:
                owner_name = pet.owner_data.get('nombre', 'N/A') if pet.owner_data else "N/A"
                print(f" {pet.id_mascota} | {pet.nombre} | {pet.especie} | Dueño: {owner_name}")
        else:
            print("  No se encontraron mascotas")
    
    def report_history_interactive(self):
        print("\n--- REPORTE DE HISTORIAL CLÍNICO ---")
        
        pets = Pet.get_all()
        if not pets:
            print("No hay mascotas registradas")
            return
        
        print("Mascotas disponibles:")
        for pet in pets:
            owner_name = pet.owner_data.get('nombre', 'N/A') if pet.owner_data else "N/A"
            print(f"  ID: {pet.id_mascota} - {pet.nombre} (Dueño: {owner_name})")
        
        try:
            id_mascota = int(input("\nID de la mascota: ").strip())
            report = self.system.get_complete_history(id_mascota)
            
            if report:
                pet = report['mascota']
                owner = report['dueno']
                consultations = report['consultas']
                
                print(f"\nHISTORIAL CLÍNICO COMPLETO")
                print(f"Mascota: {pet.nombre} (ID: {pet.id_mascota})")
                print(f"Especie/Raza: {pet.especie} / {pet.raza}")
                print(f"F. Nacimiento: {pet.fecha_nacimiento}")
                print(f"Dueño: {owner.nombre} | {owner.telefono}")
                
                print(f"\nCONSULTAS REGISTRADAS: {len(consultations)}")
                for i, consultation in enumerate(consultations, 1):
                    vet_name = consultation.veterinario_data.get('nombre', 'No asignado') if consultation.veterinario_data else "No asignado"
                    print(f"\n  {i}. {consultation.fecha_consulta} | {vet_name}")
                    print(f"      Motivo: {consultation.motivo}")
                    print(f"      Diagnóstico: {consultation.diagnostico}")
                    print(f"      Tratamiento: {consultation.tratamiento}")
                    print(f"      Observaciones: {consultation.observaciones}")
            else:
                print("No se pudo generar el reporte")
        except ValueError:
            print("El ID debe ser un número")
    
    def view_statistics_interactive(self):
        print("\n--- ESTADÍSTICAS DEL SISTEMA ---")
        stats = self.system.get_statistics()
        
        if stats:
            print(f"Total Dueños: {stats['total_dueños']}")
            print(f"Total Mascotas: {stats['total_mascotas']}")
            print(f"Total Veterinarios: {stats['total_veterinarios']}")
            print(f"Total Consultas: {stats['total_consultas']}")
        else:
            print("No se pudieron obtener las estadísticas")
    
    def list_records_interactive(self):
        print("\n--- LISTAR TODOS LOS REGISTROS ---")
        print("1. Dueños")
        print("2. Mascotas") 
        print("3. Veterinarios")
        print("4. Consultas")
        
        opcion = input("Seleccione: ").strip()
        
        if opcion == "1":
            owners = Owner.get_all()
            print(f"\n DUEÑOS ({len(owners)}):")
            for owner in owners:
                print(f"  🆔 {owner.id_dueno} | {owner.nombre} | {owner.telefono} | {owner.email}")
        
        elif opcion == "2":
            pets = Pet.get_all()
            print(f"\n MASCOTAS ({len(pets)}):")
            for pet in pets:
                owner_name = pet.owner_data.get('nombre', 'N/A') if pet.owner_data else "N/A"
                print(f"  {pet.id_mascota} |  {pet.nombre} |  {pet.especie} |  Dueño: {owner_name}")
        
        elif opcion == "3":
            veterinarians = Veterinarian.get_all()
            print(f"\n VETERINARIOS ({len(veterinarians)}):")
            for vet in veterinarians:
                print(f"  {vet.id_veterinario} | {vet.nombre} | {vet.especialidad} | {vet.telefono}")
        
        elif opcion == "4":
            consultations = Consultation.get_all()
            print(f"\n CONSULTAS ({len(consultations)}):")
            for consultation in consultations:
                pet_name = consultation.mascota_data.get('nombre', 'N/A') if consultation.mascota_data else "N/A"
                vet_name = consultation.veterinario_data.get('nombre', 'No asignado') if consultation.veterinario_data else "No asignado"
                print(f"   {consultation.id_consulta} | {consultation.fecha_consulta} | {pet_name} | {vet_name}")
    
    def test_connection(self):
        """Probar conexión a la base de datos"""
        return test_conexion()
    
    def run(self):
        """Ejecutar el sistema principal"""
        if not self.test_connection():
            print("No se pudo conectar a la base de datos. Verifica tu conexión y credenciales.")
            return
        
        while True:
            self.show_main_menu()
            opcion = input("Seleccione una opción (1-6): ").strip()
            
            if opcion == "1":
                self.manage_records_interactive()
            elif opcion == "2":
                self.search_by_name_interactive()
            elif opcion == "3":
                self.report_history_interactive()
            elif opcion == "4":
                self.view_statistics_interactive()
            elif opcion == "5":
                self.list_records_interactive()
            elif opcion == "6":
                print("\n ¡Gracias por usar el Sistema de Gestión Veterinaria!")
                break
            else:
                print("Opción inválida. Intente de nuevo.")
            
            input("\nPresione Enter para continuar...")


def main():
    """Función principal"""
    menu = VeterinaryMenu()
    menu.run()


if __name__ == "__main__":
    main()