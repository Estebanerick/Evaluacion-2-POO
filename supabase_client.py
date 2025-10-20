import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

class ConexionBD:
    def __init__(self):
        self.url = os.getenv("SUPABASE_URL")
        self.key = os.getenv("SUPABASE_KEY")
        self.client: Client = None
        self.conectar()
    
    def conectar(self):
        """Establecer conexión con Supabase"""
        try:
            if not self.url or not self.key:
                raise ValueError("❌ Faltan variables de entorno en .env")
            
            print("🔗 Conectando a Supabase...")
            self.client = create_client(self.url, self.key)
            print("✅ Cliente Supabase creado exitosamente")
            
        except Exception as e:
            print(f"❌ Error en conexión: {e}")
            self.client = None
    
    def probar_tablas(self):
        """Probar acceso a las tablas"""
        if not self.client:
            print("❌ No hay conexión disponible")
            return False
        
        tablas = ["dueno", "mascota", "veterinario", "consulta"]
        print("\n🔍 Probando acceso a tablas...")
        
        tablas_conectadas = 0
        for tabla in tablas:
            try:
                self.client.table(tabla).select("*").limit(1).execute()
                print(f"   ✅ {tabla}: CONECTADA")
                tablas_conectadas += 1
            except Exception as e:
                if "relation" in str(e) and "does not exist" in str(e):
                    print(f"   ❌ {tabla}: TABLA NO EXISTE")
                else:
                    print(f"   ❌ {tabla}: Error - {str(e)[:80]}...")
        
        return tablas_conectadas == len(tablas)

#instancia global
#esta instancia se importará en otros archivos
try:
    conexion_db = ConexionBD()
    supabase = conexion_db.client
except Exception as e:
    print(f"❌ Error fatal al inicializar conexión: {e}")
    supabase = None

def test_conexion():
    """Función para probar la conexión - compatible con main.py"""
    if not supabase:
        print("❌ No se pudo inicializar Supabase")
        return False
    
    print("\n" + "="*50)
    print("🔍 VERIFICACIÓN DE CONEXIÓN A SUPABASE")
    print("="*50)
    
    if conexion_db.probar_tablas():
        print(f"\n¡CONEXIÓN EXITOSA! Todas las tablas accesibles.")
        return True
    else:
        print("\n❌ FALLO EN LA CONEXIÓN O TABLAS FALTANTES")
        print("💡 SOLUCIÓN: Verifica tus credenciales en .env y que las 4 tablas existan en Supabase.")
        return False