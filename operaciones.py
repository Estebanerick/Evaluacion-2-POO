from models import Owner, Pet, Veterinarian, Consultation, VeterinarySystem

# ========== OPERACIONES PARA DUEÑOS ==========
def crear_dueno(nombre, direccion, telefono, email):
    """Crear nuevo dueño"""
    owner = Owner(nombre=nombre, direccion=direccion, telefono=telefono, email=email)
    return owner.save()

def obtener_duenos():
    """Obtener todos los dueños"""
    return Owner.get_all()

def buscar_dueno_por_nombre(nombre):
    """Buscar dueños por nombre"""
    return Owner.search_by_name(nombre)

def actualizar_dueno(id_dueno, nuevos_datos):
    """Actualizar dueño"""
    owner = Owner.get_by_id(id_dueno)
    if owner:
        for key, value in nuevos_datos.items():
            if hasattr(owner, key):
                setattr(owner, key, value)
        return owner.save()
    return None

# ========== OPERACIONES PARA MASCOTAS ==========
def crear_mascota(nombre, especie, raza, fecha_nacimiento, id_dueno):
    """Crear nueva mascota"""
    pet = Pet(nombre=nombre, especie=especie, raza=raza, 
              fecha_nacimiento=fecha_nacimiento, id_dueno=id_dueno)
    return pet.save()

def obtener_mascotas():
    """Obtener todas las mascotas con info del dueño"""
    return Pet.get_all()

def obtener_mascotas_por_dueno(id_dueno):
    """Obtener mascotas de un dueño específico"""
    return Pet.get_by_owner(id_dueno)

def buscar_mascota_por_nombre(nombre):
    """Buscar mascotas por nombre"""
    return Pet.search_by_name(nombre)

# ========== OPERACIONES PARA VETERINARIOS ==========
def crear_veterinario(nombre, especialidad, telefono, email):
    """Crear nuevo veterinario"""
    vet = Veterinarian(nombre=nombre, especialidad=especialidad, 
                       telefono=telefono, email=email)
    return vet.save()

def obtener_veterinarios():
    """Obtener todos los veterinarios"""
    return Veterinarian.get_all()

# ========== OPERACIONES PARA CONSULTAS ==========
def crear_consulta(motivo, diagnostico, tratamiento, observaciones, id_mascota, id_veterinario=None):
    """Crear nueva consulta médica"""
    consultation = Consultation(motivo=motivo, diagnostico=diagnostico, 
                               tratamiento=tratamiento, observaciones=observaciones,
                               id_mascota=id_mascota, id_veterinario=id_veterinario)
    return consultation.save()

def obtener_consultas_por_mascota(id_mascota):
    """Obtener historial de consultas de una mascota"""
    return Consultation.get_by_pet(id_mascota)

def obtener_todas_consultas():
    """Obtener todas las consultas con información relacionada"""
    return Consultation.get_all()

# ========== REPORTES ESPECIALES ==========
def reporte_historial_completo(id_mascota):
    """Generar reporte completo del historial clínico"""
    return VeterinarySystem.get_complete_history(id_mascota)

def estadisticas_veterinaria():
    """Estadísticas generales de la veterinaria"""
    return VeterinarySystem.get_statistics()

# ========== EJEMPLOS DE USO ==========
def ejemplos_practicos():
    """Ejemplos de cómo usar las funciones"""
    print("🚀 Ejemplos prácticos de uso:")
    
    # 1. Crear un dueño usando la clase Owner
    # owner = Owner(nombre="Carlos López", direccion="Calle 123", 
    #               telefono="555-0001", email="carlos@email.com")
    # owner.save()
    
    # 2. Crear una mascota para ese dueño
    # pet = Pet(nombre="Max", especie="Perro", raza="Labrador", 
    #           fecha_nacimiento="2020-05-15", id_dueno=1)
    # pet.save()
    
    # 3. Obtener todas las mascotas de un dueño
    # owner_pets = Owner.get_by_id(1).get_pets()
    
    pass

if __name__ == "__main__":
    # Probar conexión y funciones básicas
    try:
        print("🔍 Probando conexión y obteniendo datos...")
        
        dueños = obtener_duenos()
        print(f"📊 Dueños en sistema: {len(dueños)}")
        
        mascotas = obtener_mascotas()
        print(f"🐕 Mascotas en sistema: {len(mascotas)}")
        
        veterinarios = obtener_veterinarios()
        print(f"👨‍⚕️ Veterinarios en sistema: {len(veterinarios)}")
        
        consultas = obtener_todas_consultas()
        print(f"📋 Consultas en sistema: {len(consultas)}")
        
    except Exception as e:
        print(f"Error en pruebas: {e}")