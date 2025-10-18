# prueba-2 Caso 5 – Clínica Veterinaria

# ----------------------------------------------------------------
Se comenzo por la base de datos debido a que se tuvieron complicaciones con la aplicacion de base de datos al vincularla con el visual asi que decidimos empezar a avanza con la base de datos por que empezar por el codigo pensamos que iba a ser algo enrredado debido a que no pudimos conectarlo a la base de datos.

se agrego el archivo conexion_estudiante.py el cual se utilizara como base para empezar la conexion con la base de datos de la veterinaria.

# ----------------------------------------------------------------

se modifico el archivo conexion_estudiante.py paso a ser el archivo veterinaria.py se hizo un renombramiento y Adaptación de Funciones para que sean acordes al tema y a la base de datos se creo una nueva interfaz de usuario y Menú para que sea acorde de el tema que se solicito, las consutas sql fueron modificadas para que se ingresen los datos acorde de la base de datos creada.
se comento dentro del codigo el que hace cada cosa

# ----------------------------------------------------------------

se logro entablar una buena conexion con una base de datos pero se tubo que cambiar de aplicacion de base de datos se paso a utilizar la aplicacion oracle sql se tiene que mejorar mucho el codigo por que devido a que se cambio de base de datos se tiene que modificar vastante el codigo y poner verificaciones pero se va por buen camino

# ----------------------------------------------------------------

volvimos a tener problemas con las base de datos lo que nos llevo a modificar el trabajo entero, realizamos un cambio de base de datos pasamos a utilizar la base de datos supabase la cual nos facilito el trabajo con el codigo, modificamos el codigo y nos cambiamos de repositorio para estar mas comodos.

los cambios en el codigo fueron muy grandes cambiamos los nombres y creamos archivos nuevos que eran necesarios para la conecion y implementamos archivos exclusivos para siertas funciones como el archivo supabase_cliente.py que es el archivo encargado de la conexion con la base de datos, el archivo modelos.py el que es encargado de contener las clases con sus herencias y algunas funciones. el archivo main.py que antes era veterinaria.py es el que mas cambios sufrio paso de contener todo a ser algo mas estructurado para que trabaje con los demas archivos y no este todo centralizado y desordenado 

## Librerías necesarias

```bash
pip install supabase
pip install dotenv

```

## Archivos del proyecto

- `.env`: Archivo de configuración que almacena las credenciales secretas (URL y KEY) para conectarse a la base de datos de Supabase.
- `main.py`: Es el punto de entrada de la aplicación. Contiene el menú interactivo (la interfaz de      usuario en consola) y coordina las llamadas a las funciones y clases definidas en modelos.py.
- `modelos.py`: Es el corazón de la lógica de negocio (POO). Define las clases (Dueno, Mascota, Veterinario, Consulta) y todos los métodos para interactuar con la base de datos (CRUD: Crear, Leer, Actualizar, Eliminar).
- `supabase_client.py`: Gestiona y verifica la conexión inicial con Supabase. Carga las credenciales del archivo .env y crea el cliente global supabase que usan los otros módulos.
- `README`:Archivo de documentación (este mismo archivo) que explica el propósito del proyecto y las librerías necesarias para ejecutarlo.
