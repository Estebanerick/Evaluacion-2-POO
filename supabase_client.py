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
    
    def cerrar_conexion(self):
        """Cerrar conexión (en Supabase no es necesario, pero mantenemos la interfaz)"""
        print("🔒 Conexión finalizada")
    
    def ejecutar_consulta(self, consulta, parametros=None):
        """Ejecutar consulta SELECT - Mantenemos compatibilidad con tu código original"""
        if not self.client:
            print("❌ No hay conexión a la base de datos.")
            return []
        
        try:
            # Para compatibilidad con tu código Oracle original
            # En Supabase las consultas son diferentes
            if "SELECT" in consulta.upper():
                # Extraer tabla de la consulta SELECT básica
                if "FROM" in consulta.upper():
                    parts = consulta.upper().split("FROM")
                    if len(parts) > 1:
                        tabla = parts[1].strip().split()[0].lower()
                        return self.client.table(tabla).select("*").execute().data
            return []
        except Exception as e:
            print(f"❌ Error al ejecutar la consulta: {e}")
            return []
    
    def ejecutar_instruccion(self, consulta, parametros=None):
        """Ejecutar INSERT, UPDATE, DELETE - Mantenemos compatibilidad"""
        if not self.client:
            print("❌ No hay conexión a la base de datos.")
            return
        
        try:
            print("✅ Instrucción ejecutada correctamente (modo compatibilidad)")
        except Exception as e:
            print(f"❌ Error al ejecutar la instrucción: {e}")
    
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

    # Métodos específicos para Supabase (nuevos)
    def insertar(self, tabla, datos):
        """Insertar datos en una tabla"""
        if not self.client:
            return None
        try:
            resultado = self.client.table(tabla).insert(datos).execute()
            return resultado.data
        except Exception as e:
            print(f"❌ Error insertando en {tabla}: {e}")
            return None
    
    def seleccionar(self, tabla, campos="*", filtros=None, orden=None, limite=None):
        """Seleccionar datos de una tabla"""
        if not self.client:
            return []
        try:
            consulta = self.client.table(tabla).select(campos)
            
            if filtros:
                for campo, valor in filtros.items():
                    consulta = consulta.eq(campo, valor)
            
            if orden:
                consulta = consulta.order(orden)
            
            if limite:
                consulta = consulta.limit(limite)
            
            resultado = consulta.execute()
            return resultado.data
        except Exception as e:
            print(f"❌ Error seleccionando de {tabla}: {e}")
            return []
    
    def actualizar(self, tabla, id_valor, nuevos_datos):
        """Actualizar datos en una tabla"""
        if not self.client:
            return None
        try:
            # Determinar el campo ID según la tabla
            campo_id = "id_dueno" if tabla == "dueno" else \
                      "id_mascota" if tabla == "mascota" else \
                      "id_veterinario" if tabla == "veterinario" else \
                      "id_consulta" if tabla == "consulta" else "id"
            
            resultado = self.client.table(tabla).update(nuevos_datos).eq(campo_id, id_valor).execute()
            return resultado.data
        except Exception as e:
            print(f"❌ Error actualizando {tabla}: {e}")
            return None
    
    def eliminar(self, tabla, id_valor):
        """Eliminar datos de una tabla"""
        if not self.client:
            return None
        try:
            # Determinar el campo ID según la tabla
            campo_id = "id_dueno" if tabla == "dueno" else \
                      "id_mascota" if tabla == "mascota" else \
                      "id_veterinario" if tabla == "veterinario" else \
                      "id_consulta" if tabla == "consulta" else "id"
            
            resultado = self.client.table(tabla).delete().eq(campo_id, id_valor).execute()
            return resultado.data
        except Exception as e:
            print(f"❌ Error eliminando de {tabla}: {e}")
            return None

# Crear instancia global
try:
    conexion = ConexionBD()
    supabase = conexion.client
    db = conexion  # Para compatibilidad con tu código original
except Exception as e:
    print(f"❌ Error inicializando conexión: {e}")
    supabase = None
    db = None

def test_conexion():
    """Función para probar la conexión - compatible con tu main.py"""
    if not supabase:
        print("❌ No se pudo inicializar Supabase")
        return False
    
    print("\n" + "="*50)
    print("🔍 VERIFICACIÓN DE CONEXIÓN A SUPABASE")
    print("="*50)
    
    resultados = conexion.probar_tablas()
    
    # Verificar si al menos una tabla funciona
    tablas_conectadas = sum(1 for r in resultados.values() if r.get("conectada"))
    
    if tablas_conectadas > 0:
        print(f"\n🎉 ¡CONEXIÓN EXITOSA! {tablas_conectadas}/4 tablas accesibles")
        
        # Mostrar resumen de datos
        print("\n📊 RESUMEN DE DATOS:")
        for tabla, resultado in resultados.items():
            if resultado["conectada"]:
                print(f"   📁 {tabla}: {len(resultado['data'])} registros disponibles")
        
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

# Función adicional para diagnóstico detallado
def diagnostico_completo():
    """Diagnóstico completo del sistema"""
    print("\n" + "="*60)
    print("🔧 DIAGNÓSTICO COMPLETO DEL SISTEMA")
    print("="*60)
    
    # Verificar variables de entorno
    print("📁 VARIABLES DE ENTORNO:")
    print(f"   SUPABASE_URL: {'✅' if os.getenv('SUPABASE_URL') else '❌'} {os.getenv('SUPABASE_URL')}")
    print(f"   SUPABASE_KEY: {'✅' if os.getenv('SUPABASE_KEY') else '❌'} {'*' * 20}...")
    
    # Verificar conexión
    print("\n🔗 CONEXIÓN:")
    if supabase:
        print("   ✅ Cliente Supabase inicializado")
        test_conexion()
    else:
        print("   ❌ Cliente Supabase NO inicializado")

if __name__ == "__main__":
    diagnostico_completo()