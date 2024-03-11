<h1> Actividades y Cuestiones </h1>


----------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------

Cuestión 0: Configurar el fichero de Error Reporting and Logging de PostgreSQL
para que aparezcan recogidas las sentencias SQL DDL (Lenguaje de Definición de
Datos) + DML (Lenguaje de Manipulación de Datos) generadas en dicho fichero. No
se pide activar todas las sentencias. No activar la duración de la consulta. También se
debe de configurar el log para que en el comienzo de la línea de registro de la
información del log (“line prefix”) aparezca el DNI de los alumnos que realizan la
práctica (ambos), el nombre del host con su puerto, y la fecha y hora de la operación
que se ha realizado. Se ha de configurar también el servidor para que no use el
procesamiento paralelo de consultas.


Editar el finchero:
```
vi /etc/postgresql/16/main/postgresql.conf
```

Parametros de configuración para PL2:
```
log_destination = 'stderr'
log_statement= 'mod'
log_line_prefix = '[DNI: 47224020Y & 44444394E] [host: %r] %m [%p]'
log_directory = 'pl2logs' 
```

Configurar también el servidor para que no use el procesamiento paralelo de consultas.
```
max_parallel_workers = 0
max_parallel_workers_per_gather = 0
```

Comprobar logs:
```
tail -f /var/lib/postgresql/16/main/pl2logs/postgresql-2024-03-11_231524.log 
```
----------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------

Cuestión 1: ¿Tiene el servidor postgres un recolector de estadísticas sobre el
contenido de cada capo de las tablas de datos? Si es así, ¿Qué tipos de estadísticas se
recolectan y dónde se guardan?

```
El sistema de estadísticas acumulativas de PostgreSQL admite la recopilación e informe de información sobre la actividad del servidor. Se cuentan los accesos a tablas e índices tanto en términos de bloques de disco como de filas individuales. También se cuenta el número total de filas en cada tabla, así como información sobre las acciones de vacío(vacuum) y análisis para cada tabla. Si está habilitado, también se cuentan las llamadas a funciones definidas por el usuario y el tiempo total empleado en cada una.

PostgreSQL también admite informar sobre información dinámica sobre lo que está sucediendo exactamente en el sistema en este momento, como el comando exacto que se está ejecutando actualmente por otros procesos del servidor y qué otras conexiones existen en el sistema. Esta facilidad es independiente del sistema de estadísticas acumulativas.

Hay tres tipos de estadística:

Data distribution statistics
Extended statistics
Monitoring statistics


Data distribution statistics:
    Estas estadísticas están relacionadas con la distribución de datos para cada relación. Proporcionan información sobre los valores más comunes en cada columna de una relación, el ancho promedio de la columna, el número de valores distintos en la columna y más. Se recopilan cuando ejecutamos ANALYZE o cuando el análisis es activado por autovacuum, y se almacenan en el catálogo del sistema pg_statistic (cuya vista legible pública es pg_stats).

Extended statistics:
    Por defecto, las estadísticas de ANALYZE se almacenan en una base de datos por columna y tabla, y por lo tanto no pueden capturar ningún conocimiento sobre la correlación entre columnas. Es común ver consultas lentas ejecutando malos planes de ejecución porque múltiples columnas utilizadas en las cláusulas de consulta están correlacionadas. Sin embargo, con el comando CREATE STATISTICS, puedes crear estadísticas extendidas para columnas correlacionadas.

Monitoring statistics:
    Estas estadísticas recopilan información sobre el número de accesos a tablas e índices, tanto en términos de bloques de disco como de filas individuales. También rastrea el número total de filas en cada tabla, así como información sobre las acciones de vacío y análisis para cada tabla (cuándo se ejecutaron por última vez en la tabla).
```

----------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------

Cuestión 2: Crear una nueva base de datos llamada proyectos_empresa y que tenga las siguientes tablas con los siguientes campos y características:

• empleados(numero_empleado tipo numeric PRIMARY KEY, nombre tipo text, apellidos tipo text, salario tipo numeric)

• proyectos(numero_proyecto tipo numeric PRIMARY KEY, nombre tipo text, localización tipo text, coste tipo numeric)

• trabaja_proyectos(numero_empleado tipo numeric que sea FOREIGN KEY del campo numero_empleado de la tabla empleados con restricciones de tipo RESTRICT en sus operaciones, numero_proyecto tipo numeric que sea FOREIGN KEY del campo numero_proyecto de la tabla proyectos con restricciones de tipo RESTRICT en sus operaciones, horas de tipo numeric. La PRIMARY KEY debe ser compuesta de numero_empleado y numero_proyecto.

Se pide:

• Indicar el proceso seguido para generar esta base de datos.

• Cargar la información del fichero datos_empleados.csv, datos_proyectos.csv y datos_trabaja_proyectos.csv en dichas tablas de tal manera que sea lo más eficiente posible.

• Indicar los tiempos de carga.