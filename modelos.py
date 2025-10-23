#este archivo reemplaza a operaciones.py

#todas las interacciones con la BD en este archivo dependen de esta variable
from supabase_client import supabase

#clase base para herencia clase padre
class Persona:
    """Clase base para Dueno y Veterinario (Herencia)"""
    def __init__(self, nombre, telefono=None, email=None):
        self.nombre = nombre
        self.telefono = telefono
        self.email = email
    
    def get_descripcion(self):
        """Método para Polimorfismo"""
        return f"Persona: {self.nombre} | Tel: {self.telefono}"

#clase dueno que hereda de persona clase hijo 
class Dueno(Persona):
    """Maneja la entidad Dueno (Encapsulamiento)"""
    def __init__(self, nombre, direccion=None, telefono=None, email=None, id_dueno=None):
#esta es una herencia
#llama al constructor de la clase Persona
        super().__init__(nombre, telefono, email) #super() te permite extender la funcionalidad del padre en lugar de tener que reescribirla por completo
        self.direccion = direccion
        self.__id_dueno = id_dueno #el __ ase que sea privado 
    
    @property #convierte un método en un atributo de solo lectura, esto te da un atributo que se puede leer pero no se puede modificar desde fuera
    def id_dueno(self):
        """Getter para el ID privado (Encapsulamiento)"""
        return self.__id_dueno

    def get_descripcion(self):
        """Sobrescritura del método (Polimorfismo)"""
#este método existe en Persona, pero Dueno le da una implementación diferente
        return f"Dueño:{self.nombre} | Dir:{self.direccion}"
    
    def guardar(self):
        """Crea o actualiza un dueño en la BD (CRUD: Create/Update)"""
        try:
            datos = {
                "nombre": self.nombre,
                "direccion": self.direccion,
                "telefono": self.telefono,
                "email": self.email
            }
            
#esta es la forma clave del método guardar
            if self.__id_dueno:
#si el objeto ya tiene un id, actualiza el registro existente en la BD.
                resultado = supabase.table("dueno").update(datos).eq("id_dueno", self.__id_dueno).execute()
                print(f"✅ Dueño '{self.nombre}' actualizado con ID: {self.__id_dueno}")
            else:
#si el objeto mo tiene id, inserta un nuevo registro en la BD.
                resultado = supabase.table("dueno").insert(datos).execute()
                self.__id_dueno = resultado.data[0]['id_dueno']#asigna el nuevo id
                print(f"✅ Dueño '{self.nombre}' creado con ID: {self.__id_dueno}")

            return True
        except Exception as e:
            print(f"✘ Error guardando dueño: {e}")#manejo de errores
            return False
    
    @staticmethod #es la forma correcta de agrupar funciones dentro de una clase cuando esas funciones no dependen del estado de ningún objeto en particular
    def eliminar(id_dueno):
        """Elimina un dueño por ID (CRUD: Delete)"""
        try:
            supabase.table("dueno").delete().eq("id_dueno", id_dueno).execute()
            print(f"✅ Dueño ID {id_dueno} eliminado.")
            return True
        except Exception as e:
            print(f"✘ Error eliminando dueño: {e}")
            return False

    @staticmethod
    def obtener_todos():
        """Obtiene todos los dueños (CRUD: Read)"""
        try:
            resultado = supabase.table("dueno").select("*").order("id_dueno").execute()
            return [Dueno(**datos) for datos in resultado.data]
        except Exception as e:
            print(f"✘ Error obteniendo dueños: {e}")
            return []

    @staticmethod
    def buscar_por_nombre(nombre):
        """Busca dueños por nombre (CRUD: Read)"""
        try:
#.ilike() es un 'LIKE' de SQL insensible a mayúsculas/minúsculas.
            resultado = supabase.table("dueno").select("*").ilike("nombre", f"%{nombre}%").execute()
#convierte los resultados en objetos 'Dueno'
            return [Dueno(**datos) for datos in resultado.data]
        except Exception as e:
            print(f"✘ Error buscando dueño: {e}")
            return []
            
    @staticmethod
    def buscar_por_id(id_dueno):
        """Busca un dueño por su ID"""
        try:
            resultado = supabase.table("dueno").select("*").eq("id_dueno", id_dueno).execute()
            if resultado.data:
#crea y retorna una sola instancia de 'Dueno' con los datos
                return Dueno(**resultado.data[0])
            return None
        except Exception as e:
            print(f"✘ Error buscando dueño por ID: {e}")
            return None

#case veterinario es hijo de persona
class Veterinario(Persona):
#esta clase sigue exactamente el mismo patrón que Dueño
#Herencia, Encapsulamiento, Getters, Upsert, Staticmethods
    
    def __init__(self, nombre, especialidad=None, telefono=None, email=None, id_veterinario=None):
        super().__init__(nombre, telefono, email)
        self.especialidad = especialidad
        self.__id_veterinario = id_veterinario
    
    @property
    def id_veterinario(self):
        return self.__id_veterinario

    def get_descripcion(self):
#implementación específica de veterinario
        return f"Vet: {self.nombre} | Esp: {self.especialidad}"
    
    def guardar(self):
        try:
            datos = {
                "nombre": self.nombre,
                "especialidad": self.especialidad,
                "telefono": self.telefono,
                "email": self.email
            }

            if self.__id_veterinario:
                resultado = supabase.table("veterinario").update(datos).eq("id_veterinario", self.__id_veterinario).execute()
                print(f"✅ Veterinario '{self.nombre}' actualizado.")
            else:
                resultado = supabase.table("veterinario").insert(datos).execute()
                self.__id_veterinario = resultado.data[0]['id_veterinario']
                print(f"✅ Veterinario '{self.nombre}' creado con ID: {self.__id_veterinario}")
            return True
        except Exception as e:
            print(f"✘ Error guardando veterinario: {e}")
            return False
            
    @staticmethod
    def eliminar(id_veterinario):
        try:
            supabase.table("veterinario").delete().eq("id_veterinario", id_veterinario).execute()
            print(f"✅ Veterinario ID {id_veterinario} eliminado.")
            return True
        except Exception as e:
            print(f"✘ Error eliminando veterinario: {e}")
            return False

    @staticmethod
    def obtener_todos():
        try:
            resultado = supabase.table("veterinario").select("*").order("id_veterinario").execute()
            return [Veterinario(**datos) for datos in resultado.data]
        except Exception as e:
            print(f"✘ Error obteniendo veterinarios: {e}")
            return []

    @staticmethod
    def buscar_por_id(id_veterinario):
        try:
            resultado = supabase.table("veterinario").select("*").eq("id_veterinario", id_veterinario).execute()
            if resultado.data:
                return Veterinario(**resultado.data[0])
            return None
        except Exception as e:
            print(f"✘ Error buscando veterinario por ID: {e}")
            return None

#clse mascota
class Mascota:
#esta clase no hereda de Persona, es una entidad independiente pero esta relacionada con Dueno a través de 'id_dueno' (Foreign Key) en la base de datos
    
    def __init__(self, nombre, id_dueno, especie=None, raza=None, fecha_nacimiento=None, id_mascota=None, dueno=None):
        self.__id_mascota = id_mascota
        self.nombre = nombre
        self.especie = especie
        self.raza = raza
        self.fecha_nacimiento = fecha_nacimiento
        self.id_dueno = id_dueno #este es el Foreign Key
#este atributo es para almacenar el objeto Dueno completo,
#no solo su id sino tambien es util para mostrar el nombre del dueño.
        self.dueno = dueno #para almacenar el objeto dueño
    
    @property
    def id_mascota(self):
        return self.__id_mascota

    def guardar(self):
        try:
            datos = {
                "nombre": self.nombre,
                "especie": self.especie,
                "raza": self.raza,
                "fecha_nacimiento": self.fecha_nacimiento,
                "id_dueno": self.id_dueno
            }
            if self.__id_mascota:
                resultado = supabase.table("mascota").update(datos).eq("id_mascota", self.__id_mascota).execute()
                print(f"✅ Mascota '{self.nombre}' actualizada.")
            else:
                resultado = supabase.table("mascota").insert(datos).execute()
                self.__id_mascota = resultado.data[0]['id_mascota']
                print(f"✅ Mascota '{self.nombre}' creada con ID: {self.__id_mascota}")
            return True
        except Exception as e:
            print(f"✘ Error guardando mascota: {e}")
            return False
            
    @staticmethod
    def eliminar(id_mascota):
        try:
            supabase.table("mascota").delete().eq("id_mascota", id_mascota).execute()
            print(f"✅ Mascota ID {id_mascota} eliminada.")
            return True
        except Exception as e:
            print(f"✘ Error eliminando mascota: {e}")
            return False

    @staticmethod
    def obtener_todas():
        try:
#join en supabase
            resultado = supabase.table("mascota").select("*, dueno(nombre)").order("id_mascota").execute()
            return [Mascota(**datos) for datos in resultado.data]
        except Exception as e:
            print(f"✘ Error obteniendo mascotas: {e}")
            return []
            
    @staticmethod
    def buscar_por_id(id_mascota):
        try:
#trae todos los campos de mascota Y todos los campos del dueño.
            resultado = supabase.table("mascota").select("*, dueno(*)").eq("id_mascota", id_mascota).execute()
            if resultado.data:
                datos = resultado.data[0]
                
#constuccion de objetos anidados
#si supabase devolvio un diccionario dueno dentro de los datos crea un objeto Dueno con ese diccionario y luego crea el objeto mascota, pasandole el objeto dueno anidado.
                if datos.get('dueno'):
                    datos['dueno'] = Dueno(**datos['dueno'])
                return Mascota(**datos)
            return None
        except Exception as e:
            print(f"✘ Error buscando mascota por ID: {e}")
            return None
            
    @staticmethod
    def obtener_por_dueno(id_dueno):
#metodo simple para encontrar mascotas por el ID de su dueño
        try:
            resultado = supabase.table("mascota").select("*").eq("id_dueno", id_dueno).execute()
            return [Mascota(**datos) for datos in resultado.data]
        except Exception as e:
            print(f"✘ Error obteniendo mascotas del dueño: {e}")
            return []

    @staticmethod
    def buscar_por_nombre(nombre):
        try:
#busca mascotas por nombre, trayendo tambien el nombre del dueño
            resultado = supabase.table("mascota").select("*, dueno(nombre)").ilike("nombre", f"%{nombre}%").execute()
            return [Mascota(**datos) for datos in resultado.data]
        except Exception as e:
            print(f"✘ Error buscando mascota: {e}")
            return []

#clase consulta
class Consulta:
#añade costo al __init__
    def __init__(self, id_mascota, motivo, diagnostico=None, tratamiento=None, observaciones=None, id_veterinario=None, costo=None, id_consulta=None, fecha_consulta=None, mascota=None, veterinario=None):
        self.__id_consulta = id_consulta
        self.id_mascota = id_mascota #foreign key a mascota
        self.motivo = motivo
        self.diagnostico = diagnostico
        self.tratamiento = tratamiento
        self.observaciones = observaciones
        self.id_veterinario = id_veterinario # foreign key a veterinario
        self.costo = costo 
        self.fecha_consulta = fecha_consulta #la bd asigna este valor 
        self.mascota = mascota #para almacenar el objeto mascota
        self.veterinario = veterinario #para almacenar el objeto veterinario 
    
    @property
    def id_consulta(self):
        return self.__id_consulta
    
    def guardar(self):
        try:
            datos = {
                "motivo": self.motivo,
                "diagnostico": self.diagnostico,
                "tratamiento": self.tratamiento,
                "observaciones": self.observaciones,
                "id_mascota": self.id_mascota,
                "id_veterinario": self.id_veterinario,
                "costo": self.costo #se añade el costo a los datos a guardar
            }

            if self.__id_consulta:
                resultado = supabase.table("consulta").update(datos).eq("id_consulta", self.__id_consulta).execute()
                print(f"✅ Consulta ID {self.__id_consulta} actualizada.")
            
            else:
                #si no tiene id, crea una nueva consulta
                resultado = supabase.table("consulta").insert(datos).execute()
                #guarda el nuevo id en el objeto
                self.__id_consulta = resultado.data[0]['id_consulta']
                print(f"✅ Consulta creada con ID: {self.__id_consulta}")
            
            return True
        except Exception as e:
            print(f"✘ Error creando consulta: {e}")
            return False
#añade un metodo para buscar consultas
    @staticmethod
    def buscar_por_id(id_consulta):
        """Busca una consulta por su ID"""
        try:
#trae la consulta, el nombre de la mascota y el nombre del veterinario
            resultado = supabase.table("consulta").select("*, mascota(nombre), veterinario(nombre)").eq("id_consulta", id_consulta).execute()
            if resultado.data:
#convierte el diccionario de bd en un objeto Consulta
                return Consulta(**resultado.data[0])
            return None
        except Exception as e:
            print(f"✘ Error buscando consulta por ID: {e}")
            return None

    @staticmethod
    def obtener_todas():
        """Obtiene todas las consultas (CRUD: Read)"""
        try:
#hacemos un join para traer nombres de mascota y veterinario
            resultado = supabase.table("consulta").select("*, mascota(nombre), veterinario(nombre)").order("fecha_consulta", desc=True).execute()
            return [Consulta(**datos) for datos in resultado.data]
        except Exception as e:
            print(f"✘ Error obteniendo consultas: {e}")
            return []

    @staticmethod
    def obtener_por_mascota(id_mascota):
        """Obtiene todas las consultas de una mascota específica"""
        try:
#trae todas las consultas de una mascota, con el nombre del veterinario
            resultado = supabase.table("consulta").select("*, veterinario(nombre)").eq("id_mascota", id_mascota).order("fecha_consulta", desc=True).execute()
            return [Consulta(**datos) for datos in resultado.data]
        except Exception as e:
            print(f"✘ Error obteniendo historial de mascota: {e}")
            return []


def reporte_historial_completo(id_mascota):
    """Generar reporte completo del historial clínico"""
    try:
#busca la mascota que ya incluye al dueño gracias al JOIN en buscar_por_id
        mascota = Mascota.buscar_por_id(id_mascota)
        if not mascota:
            print("Mascota no encontrada")
            return None
        
#el dueño ya viene en el objeto mascota
        dueno = mascota.dueno
        
#busca todas las consultas para esa mascota
        consultas = Consulta.obtener_por_mascota(id_mascota)
        
#devuelve un diccionario con todos los datos recopilados
        return {
            "mascota": mascota,
            "dueno": dueno,
            "consultas": consultas
        }
        
    except Exception as e:
        print(f"✘ Error generando reporte: {e}")
        return None


def estadisticas_veterinaria():
    """Estadísticas generales de la veterinaria"""
    try:
        # Usa los métodos estáticos .obtener_todos() y cuenta los resultados
        dueños_count = len(Dueno.obtener_todos())
        mascotas_count = len(Mascota.obtener_todas())
        veterinarios_count = len(Veterinario.obtener_todos())
        consultas_count = len(Consulta.obtener_todas())
        
        return {
            "total_dueños": dueños_count,
            "total_mascotas": mascotas_count,
            "total_veterinarios": veterinarios_count,
            "total_consultas": consultas_count
        }
        
    except Exception as e:
        print(f"✘ Error obteniendo estadísticas: {e}")
        return {}

#El Método Estático (Dueno.obtener_todos()) 
#este es un método @staticmethod que pertenece a la clase Dueno. 
#Su trabajo es ir a la base de datos de Supabase y devolver una lista con todos los dueños.

class Pago:
#esta clase representa un pago, vinculado a una consulta.
    def __init__(self, id_consulta, monto, metodo_pago, estado='Pagado', id_pago=None, fecha_pago=None):
        self.__id_pago = id_pago
        self.id_consulta = id_consulta #foreign Key a Consulta
        self.monto = monto
        self.metodo_pago = metodo_pago
        self.estado = estado
        self.fecha_pago = fecha_pago #la bd asigna este valor
    
    @property
    def id_pago(self):
        return self.__id_pago

    def guardar(self):
        """Crea un nuevo pago en la BD"""
        try:
            datos = {
                "id_consulta": self.id_consulta,
                "monto": self.monto,
                "metodo_pago": self.metodo_pago,
                "estado": self.estado
            }
            resultado = supabase.table("pago").insert(datos).execute()
            self.__id_pago = resultado.data[0]['id_pago']
            print(f"✅ Pago de ${self.monto} registrado con ID: {self.__id_pago}")
            return True
        except Exception as e:
            print(f"✘ Error registrando pago: {e}")
            return False