from supabase_client import db_connection
from datetime import datetime

class BaseModel:
    """Clase base para todos los modelos"""
    
    @classmethod
    def _execute_query(cls, query):
        """Ejecutar consulta y manejar errores"""
        try:
            return query.execute()
        except Exception as e:
            print(f"❌ Error en {cls.__name__}: {e}")
            return type('MockResponse', (), {'data': []})()
    
    @classmethod
    def get_all(cls):
        """Obtener todos los registros"""
        raise NotImplementedError("Método get_all debe ser implementado")
    
    @classmethod
    def search_by_name(cls, name):
        """Buscar por nombre"""
        raise NotImplementedError("Método search_by_name debe ser implementado")

class Owner(BaseModel):
    """Clase para manejar dueños"""
    
    def __init__(self, id_dueno=None, nombre=None, direccion=None, telefono=None, email=None):
        self.id_dueno = id_dueno
        self.nombre = nombre
        self.direccion = direccion
        self.telefono = telefono
        self.email = email
    
    def save(self):
        """Guardar dueño (crear o actualizar)"""
        data = {
            "nombre": self.nombre,
            "direccion": self.direccion,
            "telefono": self.telefono,
            "email": self.email
        }
        
        client = db_connection.get_client()
        if not client:
            return None
        
        if self.id_dueno:
            # Actualizar
            result = self._execute_query(
                client.table("dueno").update(data).eq("id_dueno", self.id_dueno)
            )
            if result.data:
                print(f"✅ Dueño '{self.nombre}' actualizado")
            return result.data
        else:
            # Crear nuevo
            result = self._execute_query(
                client.table("dueno").insert(data)
            )
            if result.data:
                self.id_dueno = result.data[0]['id_dueno']
                print(f"✅ Dueño '{self.nombre}' creado con ID: {self.id_dueno}")
                return self.id_dueno
        return None
    
    @classmethod
    def get_all(cls):
        """Obtener todos los dueños"""
        client = db_connection.get_client()
        if not client:
            return []
        
        result = cls._execute_query(
            client.table("dueno").select("*").order("id_dueno")
        )
        return [cls(**item) for item in result.data]
    
    @classmethod
    def search_by_name(cls, name):
        """Buscar dueños por nombre"""
        client = db_connection.get_client()
        if not client:
            return []
        
        result = cls._execute_query(
            client.table("dueno").select("*").ilike("nombre", f"%{name}%")
        )
        return [cls(**item) for item in result.data]
    
    @classmethod
    def get_by_id(cls, owner_id):
        """Obtener dueño por ID"""
        client = db_connection.get_client()
        if not client:
            return None
        
        result = cls._execute_query(
            client.table("dueno").select("*").eq("id_dueno", owner_id)
        )
        if result.data:
            return cls(**result.data[0])
        return None
    
    def get_pets(self):
        """Obtener mascotas del dueño"""
        return Pet.get_by_owner(self.id_dueno)
    
    def __str__(self):
        return f"Dueño {self.id_dueno}: {self.nombre} - {self.telefono}"

class Pet(BaseModel):
    """Clase para manejar mascotas"""
    
    def __init__(self, id_mascota=None, nombre=None, especie=None, raza=None, 
                 fecha_nacimiento=None, id_dueno=None, owner_data=None):
        self.id_mascota = id_mascota
        self.nombre = nombre
        self.especie = especie
        self.raza = raza
        self.fecha_nacimiento = fecha_nacimiento
        self.id_dueno = id_dueno
        self.owner_data = owner_data
    
    def save(self):
        """Guardar mascota (crear o actualizar)"""
        data = {
            "nombre": self.nombre,
            "especie": self.especie,
            "raza": self.raza,
            "fecha_nacimiento": self.fecha_nacimiento,
            "id_dueno": self.id_dueno
        }
        
        client = db_connection.get_client()
        if not client:
            return None
        
        if self.id_mascota:
            # Actualizar
            result = self._execute_query(
                client.table("mascota").update(data).eq("id_mascota", self.id_mascota)
            )
            if result.data:
                print(f"✅ Mascota '{self.nombre}' actualizada")
            return result.data
        else:
            # Crear nueva
            result = self._execute_query(
                client.table("mascota").insert(data)
            )
            if result.data:
                self.id_mascota = result.data[0]['id_mascota']
                print(f"✅ Mascota '{self.nombre}' creada con ID: {self.id_mascota}")
                return self.id_mascota
        return None
    
    @classmethod
    def get_all(cls):
        """Obtener todas las mascotas con info del dueño"""
        client = db_connection.get_client()
        if not client:
            return []
        
        result = cls._execute_query(
            client.table("mascota").select("*, dueno(nombre, telefono)").order("id_mascota")
        )
        pets = []
        for item in result.data:
            owner_data = item.pop('dueno', {})
            pets.append(cls(owner_data=owner_data, **item))
        return pets
    
    @classmethod
    def get_by_owner(cls, owner_id):
        """Obtener mascotas de un dueño específico"""
        client = db_connection.get_client()
        if not client:
            return []
        
        result = cls._execute_query(
            client.table("mascota").select("*").eq("id_dueno", owner_id)
        )
        return [cls(**item) for item in result.data]
    
    @classmethod
    def search_by_name(cls, name):
        """Buscar mascotas por nombre"""
        client = db_connection.get_client()
        if not client:
            return []
        
        result = cls._execute_query(
            client.table("mascota").select("*, dueno(nombre, telefono)").ilike("nombre", f"%{name}%")
        )
        pets = []
        for item in result.data:
            owner_data = item.pop('dueno', {})
            pets.append(cls(owner_data=owner_data, **item))
        return pets
    
    @classmethod
    def get_by_id(cls, pet_id):
        """Obtener mascota por ID"""
        client = db_connection.get_client()
        if not client:
            return None
        
        result = cls._execute_query(
            client.table("mascota").select("*, dueno(*)").eq("id_mascota", pet_id)
        )
        if result.data:
            item = result.data[0]
            owner_data = item.pop('dueno', {})
            return cls(owner_data=owner_data, **item)
        return None
    
    def get_owner(self):
        """Obtener dueño de la mascota"""
        if self.id_dueno:
            return Owner.get_by_id(self.id_dueno)
        return None
    
    def get_consultations(self):
        """Obtener consultas de la mascota"""
        return Consultation.get_by_pet(self.id_mascota)
    
    def __str__(self):
        owner_name = self.owner_data.get('nombre', 'N/A') if self.owner_data else 'N/A'
        return f"Mascota {self.id_mascota}: {self.nombre} ({self.especie}) - Dueño: {owner_name}"

class Veterinarian(BaseModel):
    """Clase para manejar veterinarios"""
    
    def __init__(self, id_veterinario=None, nombre=None, especialidad=None, telefono=None, email=None):
        self.id_veterinario = id_veterinario
        self.nombre = nombre
        self.especialidad = especialidad
        self.telefono = telefono
        self.email = email
    
    def save(self):
        """Guardar veterinario (crear o actualizar)"""
        data = {
            "nombre": self.nombre,
            "especialidad": self.especialidad,
            "telefono": self.telefono,
            "email": self.email
        }
        
        client = db_connection.get_client()
        if not client:
            return None
        
        if self.id_veterinario:
            # Actualizar
            result = self._execute_query(
                client.table("veterinario").update(data).eq("id_veterinario", self.id_veterinario)
            )
            if result.data:
                print(f"✅ Veterinario '{self.nombre}' actualizado")
            return result.data
        else:
            # Crear nuevo
            result = self._execute_query(
                client.table("veterinario").insert(data)
            )
            if result.data:
                self.id_veterinario = result.data[0]['id_veterinario']
                print(f"✅ Veterinario '{self.nombre}' creado con ID: {self.id_veterinario}")
                return self.id_veterinario
        return None
    
    @classmethod
    def get_all(cls):
        """Obtener todos los veterinarios"""
        client = db_connection.get_client()
        if not client:
            return []
        
        result = cls._execute_query(
            client.table("veterinario").select("*").order("id_veterinario")
        )
        return [cls(**item) for item in result.data]
    
    @classmethod
    def search_by_name(cls, name):
        """Buscar veterinarios por nombre"""
        client = db_connection.get_client()
        if not client:
            return []
        
        result = cls._execute_query(
            client.table("veterinario").select("*").ilike("nombre", f"%{name}%")
        )
        return [cls(**item) for item in result.data]
    
    @classmethod
    def get_by_id(cls, vet_id):
        """Obtener veterinario por ID"""
        client = db_connection.get_client()
        if not client:
            return None
        
        result = cls._execute_query(
            client.table("veterinario").select("*").eq("id_veterinario", vet_id)
        )
        if result.data:
            return cls(**result.data[0])
        return None
    
    def __str__(self):
        return f"Veterinario {self.id_veterinario}: {self.nombre} - {self.especialidad}"

class Consultation(BaseModel):
    """Clase para manejar consultas médicas"""
    
    def __init__(self, id_consulta=None, motivo=None, diagnostico=None, tratamiento=None,
                 observaciones=None, fecha_consulta=None, id_mascota=None, id_veterinario=None,
                 mascota_data=None, veterinario_data=None):
        self.id_consulta = id_consulta
        self.motivo = motivo
        self.diagnostico = diagnostico
        self.tratamiento = tratamiento
        self.observaciones = observaciones
        self.fecha_consulta = fecha_consulta
        self.id_mascota = id_mascota
        self.id_veterinario = id_veterinario
        self.mascota_data = mascota_data
        self.veterinario_data = veterinario_data
    
    def save(self):
        """Guardar consulta (crear o actualizar)"""
        data = {
            "motivo": self.motivo,
            "diagnostico": self.diagnostico,
            "tratamiento": self.tratamiento,
            "observaciones": self.observaciones,
            "id_mascota": self.id_mascota,
            "id_veterinario": self.id_veterinario
        }
        
        client = db_connection.get_client()
        if not client:
            return None
        
        if self.id_consulta:
            # Actualizar
            result = self._execute_query(
                client.table("consulta").update(data).eq("id_consulta", self.id_consulta)
            )
            if result.data:
                print(f"✅ Consulta actualizada con ID: {self.id_consulta}")
            return result.data
        else:
            # Crear nueva
            result = self._execute_query(
                client.table("consulta").insert(data)
            )
            if result.data:
                self.id_consulta = result.data[0]['id_consulta']
                print(f"✅ Consulta creada con ID: {self.id_consulta}")
                return self.id_consulta
        return None
    
    @classmethod
    def get_all(cls):
        """Obtener todas las consultas con información relacionada"""
        client = db_connection.get_client()
        if not client:
            return []
        
        result = cls._execute_query(
            client.table("consulta").select("*, mascota(nombre, especie), veterinario(nombre)").order("fecha_consulta", desc=True)
        )
        consultations = []
        for item in result.data:
            mascota_data = item.pop('mascota', {})
            veterinario_data = item.pop('veterinario', {})
            consultations.append(cls(mascota_data=mascota_data, veterinario_data=veterinario_data, **item))
        return consultations
    
    @classmethod
    def get_by_pet(cls, pet_id):
        """Obtener historial de consultas de una mascota"""
        client = db_connection.get_client()
        if not client:
            return []
        
        result = cls._execute_query(
            client.table("consulta").select("*, veterinario(nombre, especialidad)").eq("id_mascota", pet_id).order("fecha_consulta", desc=True)
        )
        consultations = []
        for item in result.data:
            veterinario_data = item.pop('veterinario', {})
            consultations.append(cls(veterinario_data=veterinario_data, **item))
        return consultations
    
    def __str__(self):
        pet_name = self.mascota_data.get('nombre', 'N/A') if self.mascota_data else 'N/A'
        vet_name = self.veterinario_data.get('nombre', 'No asignado') if self.veterinario_data else 'No asignado'
        return f"Consulta {self.id_consulta}: {pet_name} - {self.motivo} - {vet_name}"

class VeterinarySystem:
    """Clase principal del sistema veterinario"""
    
    @staticmethod
    def get_statistics():
        """Obtener estadísticas generales del sistema"""
        try:
            total_owners = len(Owner.get_all())
            total_pets = len(Pet.get_all())
            total_vets = len(Veterinarian.get_all())
            total_consultations = len(Consultation.get_all())
            
            return {
                "total_dueños": total_owners,
                "total_mascotas": total_pets,
                "total_veterinarios": total_vets,
                "total_consultas": total_consultations
            }
        except Exception as e:
            print(f"Error obteniendo estadísticas: {e}")
            return {}
    
    @staticmethod
    def get_complete_history(pet_id):
        """Generar reporte completo del historial clínico"""
        try:
            pet = Pet.get_by_id(pet_id)
            if not pet:
                print("Mascota no encontrada")
                return None
            
            owner = pet.get_owner()
            consultations = pet.get_consultations()
            
            return {
                "mascota": pet,
                "dueno": owner,
                "consultas": consultations
            }
        except Exception as e:
            print(f"Error generando reporte: {e}")
            return None

# No ejecutar models.py directamente
if __name__ == "__main__":
    print("⚠️  Este archivo contiene las clases del modelo y no debe ejecutarse directamente.")
    print("💡 Ejecuta 'python main.py' en su lugar.")