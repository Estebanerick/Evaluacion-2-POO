# test_veterinaria.py
import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Agregar el directorio actual al path para importar los módulos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from modelos import Dueno, Mascota, Veterinario, Consulta, Pago, reporte_historial_completo, estadisticas_veterinaria
from supabase_client import test_conexion

class TestConexionBD(unittest.TestCase):
    
    @patch('supabase_client.ConexionBD')
    def test_conexion_exitosa(self, MockConexionBD):
        """Test para verificar conexión exitosa a la base de datos"""
        mock_instance = MockConexionBD.return_value
        mock_instance.client = MagicMock()
        mock_instance.probar_tablas.return_value = True
        
        resultado = test_conexion()
        self.assertTrue(resultado)

class TestClaseDueno(unittest.TestCase):
    
    def setUp(self):
        """Configuración inicial para las pruebas"""
        self.datos_dueno = {
            'id_dueno': 1,
            'nombre': 'Juan Pérez',
            'direccion': 'Calle 123',
            'telefono': '123456789',
            'email': 'juan@email.com'
        }
    
    def test_creacion_dueno(self):
        """Test para crear instancia de Dueño"""
        dueno = Dueno(
            nombre='Juan Pérez',
            direccion='Calle 123',
            telefono='123456789',
            email='juan@email.com'
        )
        
        self.assertEqual(dueno.nombre, 'Juan Pérez')
        self.assertEqual(dueno.direccion, 'Calle 123')
        self.assertEqual(dueno.telefono, '123456789')
        self.assertEqual(dueno.email, 'juan@email.com')
    
    def test_get_descripcion_dueno(self):
        """Test para el método get_descripcion de Dueño"""
        dueno = Dueno('Juan Pérez', 'Calle 123')
        descripcion = dueno.get_descripcion()
        self.assertIn('Juan Pérez', descripcion)
        self.assertIn('Calle 123', descripcion)
    
    @patch('modelos.supabase')
    def test_guardar_dueno_nuevo(self, mock_supabase):
        """Test para guardar un nuevo dueño"""
        mock_response = MagicMock()
        mock_response.data = [{'id_dueno': 1}]
        mock_supabase.table.return_value.insert.return_value.execute.return_value = mock_response
        
        dueno = Dueno('Juan Pérez')
        resultado = dueno.guardar()
        
        self.assertTrue(resultado)
        mock_supabase.table.return_value.insert.assert_called_once()
    
    @patch('modelos.supabase')
    def test_eliminar_dueno(self, mock_supabase):
        """Test para eliminar un dueño"""
        mock_supabase.table.return_value.delete.return_value.eq.return_value.execute.return_value = MagicMock()
        
        resultado = Dueno.eliminar(1)
        
        self.assertTrue(resultado)
        mock_supabase.table.return_value.delete.return_value.eq.assert_called_once_with('id_dueno', 1)

class TestClaseMascota(unittest.TestCase):
    
    def test_creacion_mascota(self):
        """Test para crear instancia de Mascota"""
        mascota = Mascota(
            nombre='Firulais',
            id_dueno=1,
            especie='Perro',
            raza='Labrador',
            fecha_nacimiento='2020-01-01'
        )
        
        self.assertEqual(mascota.nombre, 'Firulais')
        self.assertEqual(mascota.especie, 'Perro')
        self.assertEqual(mascota.raza, 'Labrador')
        self.assertEqual(mascota.id_dueno, 1)
    
    @patch('modelos.supabase')
    def test_guardar_mascota(self, mock_supabase):
        """Test para guardar una mascota"""
        mock_response = MagicMock()
        mock_response.data = [{'id_mascota': 1}]
        mock_supabase.table.return_value.insert.return_value.execute.return_value = mock_response
        
        mascota = Mascota('Firulais', 1)
        resultado = mascota.guardar()
        
        self.assertTrue(resultado)
        mock_supabase.table.return_value.insert.assert_called_once()

class TestClaseVeterinario(unittest.TestCase):
    
    def test_creacion_veterinario(self):
        """Test para crear instancia de Veterinario"""
        vet = Veterinario(
            nombre='Dra. María López',
            especialidad='Cirugía',
            telefono='987654321',
            email='maria@vet.com'
        )
        
        self.assertEqual(vet.nombre, 'Dra. María López')
        self.assertEqual(vet.especialidad, 'Cirugía')
        self.assertEqual(vet.telefono, '987654321')
        self.assertEqual(vet.email, 'maria@vet.com')
    
    def test_get_descripcion_veterinario(self):
        """Test para el método get_descripcion de Veterinario"""
        vet = Veterinario('Dra. María López', 'Cirugía')
        descripcion = vet.get_descripcion()
        self.assertIn('Dra. María López', descripcion)
        self.assertIn('Cirugía', descripcion)

class TestClaseConsulta(unittest.TestCase):
    
    def test_creacion_consulta(self):
        """Test para crear instancia de Consulta"""
        consulta = Consulta(
            id_mascota=1,
            motivo='Control anual',
            diagnostico='Saludable',
            tratamiento='Vacunación',
            observaciones='Mascota en buen estado',
            id_veterinario=1,
            costo=15000.0
        )
        
        self.assertEqual(consulta.id_mascota, 1)
        self.assertEqual(consulta.motivo, 'Control anual')
        self.assertEqual(consulta.diagnostico, 'Saludable')
        self.assertEqual(consulta.costo, 15000.0)
    
    @patch('modelos.supabase')
    def test_guardar_consulta(self, mock_supabase):
        """Test para guardar una consulta"""
        mock_response = MagicMock()
        mock_response.data = [{'id_consulta': 1}]
        mock_supabase.table.return_value.insert.return_value.execute.return_value = mock_response
        
        consulta = Consulta(1, 'Control anual')
        resultado = consulta.guardar()
        
        self.assertTrue(resultado)
        mock_supabase.table.return_value.insert.assert_called_once()

class TestClasePago(unittest.TestCase):
    
    def test_creacion_pago(self):
        """Test para crear instancia de Pago"""
        pago = Pago(
            id_consulta=1,
            monto=15000.0,
            metodo_pago='Efectivo',
            estado='Pagado'
        )
        
        self.assertEqual(pago.id_consulta, 1)
        self.assertEqual(pago.monto, 15000.0)
        self.assertEqual(pago.metodo_pago, 'Efectivo')
        self.assertEqual(pago.estado, 'Pagado')
    
    @patch('modelos.supabase')
    def test_guardar_pago(self, mock_supabase):
        """Test para guardar un pago"""
        mock_response = MagicMock()
        mock_response.data = [{'id_pago': 1}]
        mock_supabase.table.return_value.insert.return_value.execute.return_value = mock_response
        
        pago = Pago(1, 15000.0, 'Efectivo')
        resultado = pago.guardar()
        
        self.assertTrue(resultado)
        mock_supabase.table.return_value.insert.assert_called_once()

class TestFuncionesReportes(unittest.TestCase):
    
    @patch('modelos.Mascota.buscar_por_id')
    @patch('modelos.Consulta.obtener_por_mascota')
    def test_reporte_historial_completo(self, mock_obtener_consultas, mock_buscar_mascota):
        """Test para generar reporte de historial completo"""
        # Mock de mascota
        mock_mascota = MagicMock()
        mock_mascota.dueno = MagicMock()
        mock_buscar_mascota.return_value = mock_mascota
        
        # Mock de consultas
        mock_consultas = [MagicMock(), MagicMock()]
        mock_obtener_consultas.return_value = mock_consultas
        
        reporte = reporte_historial_completo(1)
        
        self.assertIsNotNone(reporte)
        self.assertEqual(reporte['mascota'], mock_mascota)
        self.assertEqual(reporte['consultas'], mock_consultas)
        mock_buscar_mascota.assert_called_once_with(1)
        mock_obtener_consultas.assert_called_once_with(1)
    
    @patch('modelos.Dueno.obtener_todos')
    @patch('modelos.Mascota.obtener_todas')
    @patch('modelos.Veterinario.obtener_todos')
    @patch('modelos.Consulta.obtener_todas')
    def test_estadisticas_veterinaria(self, mock_consultas, mock_veterinarios, mock_mascotas, mock_duenos):
        """Test para obtener estadísticas de la veterinaria"""
        mock_duenos.return_value = [MagicMock()] * 5  # 5 dueños
        mock_mascotas.return_value = [MagicMock()] * 8  # 8 mascotas
        mock_veterinarios.return_value = [MagicMock()] * 3  # 3 veterinarios
        mock_consultas.return_value = [MagicMock()] * 12  # 12 consultas
        
        stats = estadisticas_veterinaria()
        
        self.assertEqual(stats['total_dueños'], 5)
        self.assertEqual(stats['total_mascotas'], 8)
        self.assertEqual(stats['total_veterinarios'], 3)
        self.assertEqual(stats['total_consultas'], 12)

class TestBusquedas(unittest.TestCase):
    
    @patch('modelos.Dueno.buscar_por_nombre')
    def test_buscar_dueno_por_nombre(self, mock_buscar):
        """Test para búsqueda de dueños por nombre"""
        mock_duenos = [
            MagicMock(id_dueno=1, nombre='Juan Pérez', telefono='123456789', email='juan@email.com'),
            MagicMock(id_dueno=2, nombre='Juan Carlos', telefono='987654321', email='juanc@email.com')
        ]
        mock_buscar.return_value = mock_duenos
        
        duenos = Dueno.buscar_por_nombre('Juan')
        
        self.assertEqual(len(duenos), 2)
        self.assertEqual(duenos[0].nombre, 'Juan Pérez')
        self.assertEqual(duenos[1].nombre, 'Juan Carlos')
    
    @patch('modelos.Mascota.buscar_por_nombre')
    def test_buscar_mascota_por_nombre(self, mock_buscar):
        """Test para búsqueda de mascotas por nombre"""
        mock_mascotas = [
            MagicMock(id_mascota=1, nombre='Firulais', especie='Perro', dueno={'nombre': 'Juan Pérez'}),
            MagicMock(id_mascota=2, nombre='Firulais Jr', especie='Perro', dueno={'nombre': 'Ana García'})
        ]
        mock_buscar.return_value = mock_mascotas
        
        mascotas = Mascota.buscar_por_nombre('Firulais')
        
        self.assertEqual(len(mascotas), 2)
        self.assertEqual(mascotas[0].nombre, 'Firulais')
        self.assertEqual(mascotas[1].nombre, 'Firulais Jr')

class TestValidaciones(unittest.TestCase):
    
    def test_dueno_nombre_obligatorio(self):
        """Test que verifica que el nombre del dueño sea obligatorio"""
        with self.assertRaises(TypeError):
            Dueno()  # Debería fallar sin nombre
    
    def test_mascota_nombre_obligatorio(self):
        """Test que verifica que el nombre de la mascota sea obligatorio"""
        with self.assertRaises(TypeError):
            Mascota()  # Debería fallar sin nombre e id_dueno
    
    def test_consulta_motivo_obligatorio(self):
        """Test que verifica que el motivo de consulta sea obligatorio"""
        with self.assertRaises(TypeError):
            Consulta()  # Debería fallar sin id_mascota y motivo

if __name__ == '__main__':
    # Ejecutar todas las pruebas
    unittest.main(verbosity=2)