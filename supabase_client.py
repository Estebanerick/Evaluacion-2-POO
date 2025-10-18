import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

class DatabaseConnection:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        """Inicializar conexión con Supabase"""
        self.url = os.getenv("SUPABASE_URL")
        self.key = os.getenv("SUPABASE_KEY")
        self.client: Client = None
        self.connect()
    
    def connect(self):
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
    
    def get_client(self):
        """Obtener cliente de Supabase"""
        return self.client

    def probar_tablas(self):
        """Probar acceso a las tablas"""
        if not self.client:
            print("❌ No hay conexión disponible")
            return False
        
        tablas = ["dueno", "mascota", "veterinario", "consulta"]
        resultados = {}
        
        print("\n🔍 Probando acceso a tablas...")
        print("-" * 40)
        
        for tabla in tablas:
            try:
                # Intentar consulta simple
                response = self.client.table(tabla).select("*").limit(1).execute()
                resultados[tabla] = {
                    "conectada": True,
                    "registros": len(response.data),
                    "data": response.data
                }
                print(f"   ✅ {tabla}: CONECTADA ({len(response.data)} registros)")
                
            except Exception as e:
                resultados[tabla] = {
                    "conectada": False, 
                    "error": str(e),
                    "data": []
                }
                error_msg = str(e)
                if "Invalid API key" in error_msg:
                    print(f"   ❌ {tabla}: API KEY INVÁLIDA")
                elif "JWT" in error_msg:
                    print(f"   ❌ {tabla}: TOKEN EXPIRADO")
                elif "relation" in error_msg and "does not exist" in error_msg:
                    print(f"   ❌ {tabla}: TABLA NO EXISTE")
                else:
                    print(f"   ❌ {tabla}: Error - {str(e)[:80]}...")
        
        return resultados

# Crear instancia global - ESTA ES LA LÍNEA IMPORTANTE
db_connection = DatabaseConnection()

# Alias para compatibilidad
supabase = db_connection.get_client()

def test_conexion():
    """Función para probar la conexión - compatible con tu main.py"""
    client = db_connection.get_client()
    if not client:
        print("❌ No se pudo inicializar Supabase")
        return False
    
    print("\n" + "="*50)
    print("🔍 VERIFICACIÓN DE CONEXIÓN A SUPABASE")
    print("="*50)
    
    resultados = db_connection.probar_tablas()
    
    # Verificar si al menos una tabla funciona
    tablas_conectadas = sum(1 for r in resultados.values() if r.get("conectada"))
    
    if tablas_conectadas > 0:
        print(f"\n🎉 ¡CONEXIÓN EXITOSA! {tablas_conectadas}/4 tablas accesibles")
        return True
    else:
        print("\n❌ NO SE PUDO ACCEDER A NINGUNA TABLA")
        print("\n💡 SOLUCIÓN DE PROBLEMAS:")
        print("   1. ✅ Verifica que tu proyecto esté ACTIVO en Supabase")
        print("   2. 🔑 Obtén una nueva API Key en Settings > API")
        print("   3. 📋 Asegúrate de que las tablas existan en Table Editor")
        print("   4. 🌐 Verifica tu conexión a internet")
        print("\n🔧 Verifica en: https://supabase.com/dashboard")
        return False

if __name__ == "__main__":
    test_conexion()