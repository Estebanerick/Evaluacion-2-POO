prueba-2 Caso 5 – Clínica Veterinaria

Se comenzó por la base de datos debido a que se tuvieron complicaciones con la aplicación de base de datos al vincularla con el visual, así que decidimos empezar a avanzar con la base de datos porque empezar por el código pensamos que iba a ser algo enredado debido a que no pudimos conectarlo a la base de datos.

Se agregó el archivo conexion_estudiante.py, el cual se utilizará como base para empezar la conexión con la base de datos de la veterinaria.

Se modificó el archivo conexion_estudiante.py, pasó a ser el archivo veterinaria.py, se hizo un renombramiento y adaptación de funciones para que sean acordes al tema y a la base de datos. Se creó una nueva interfaz de usuario y menú para que sea acorde al tema que se solicitó. Las consultas SQL fueron modificadas para que se ingresen los datos acorde a la base de datos creada. Se comentó dentro del código qué hace cada cosa.

Se logró entablar una buena conexión con una base de datos, pero se tuvo que cambiar de aplicación de base de datos. Se pasó a utilizar la aplicación Oracle SQL. Se tiene que mejorar mucho el código porque debido a que se cambió de base de datos, se tiene que modificar bastante el código y poner verificaciones, pero se va por buen camino.

Volvimos a tener problemas con la base de datos, lo que nos llevó a modificar el trabajo entero. Realizamos un cambio de base de datos, pasamos a utilizar la base de datos Supabase, la cual nos facilitó el trabajo con el código. Modificamos el código y nos cambiamos de repositorio para estar más cómodos.

Los cambios en el código fueron muy grandes. Cambiamos los nombres y creamos archivos nuevos que eran necesarios para la conexión, e implementamos archivos exclusivos para ciertas funciones, como el archivo supabase_cliente.py, que es el archivo encargado de la conexión con la base de datos; el archivo modelos.py, que es encargado de contener las clases con sus herencias y algunas funciones; y el archivo main.py, que antes era veterinaria.py, es el que más cambios sufrió: pasó de contener todo a ser algo más estructurado para que trabaje con los demás archivos y no esté todo centralizado y desordenado.

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
