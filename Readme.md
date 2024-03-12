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

1) Data distribution statistics
2) Extended statistics
3) Monitoring statistics


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

```
create database proyectos_empresa;
```

Creamos la base de datos de proyectos de empresas, posteriormente especificamos la tabla empleados y la creamos estipulando la clave primaria numero_empleado, posteriormente creamos
la tabla proyectos de la misma manera que la tabla anterior, identificando numero_proyecto como clave primaria, por ultimo creamos la tabla trabaja_proyectos, donde declaramos los parametros
numero_empleado y numero_proyecto como clave primaria de la tabla y como clave foranea de las tablas empleados y proyectos respectivamente, y establecemos la restricción RESTRICT que 
garantiza que no se puedan eliminar registros en las tablas relacionadas si hay registros en la tabla trabaja_proyectos que dependen de ellos.

```
create TABLE empleados (
    numero_empleado NUMERIC PRIMARY KEY,
    nombre TEXT,
    apellidos TEXT,
    salario NUMERIC
);
```

```
create TABLE proyectos (
    numero_proyecto NUMERIC PRIMARY KEY,
    nombre TEXT,
    localizacion TEXT,
    coste NUMERIC
);
```

```
create TABLE trabaja_proyectos (
    numero_empleado NUMERIC,
    numero_proyecto NUMERIC,
    horas NUMERIC,
    PRIMARY KEY (numero_empleado, numero_proyecto),
    FOREIGN KEY (numero_empleado) REFERENCES empleados(numero_empleado) ON DELETE RESTRICT,
    FOREIGN KEY (numero_proyecto) REFERENCES proyectos(numero_proyecto) ON DELETE RESTRICT
);
```


```
\timing

Timing is on.
```

```
\copy empleados(numero_empleado,nombre,apellidos,salario) FROM '/tmp/datos_empleados.csv' DELIMITER ',' CSV
COPY 2000000
Time: 4191.524 ms (00:04.192)
```

```
\copy proyectos(numero_proyecto,nombre,localizacion,coste) FROM '/tmp/datos_proyectos.csv' DELIMITER ',' CSV
COPY 100000
Time: 274.249 ms
```

```
\copy trabaja_proyectos(numero_empleado,numero_proyecto,horas) FROM '/tmp/datos_trabaja_proyectos.csv' DELIMITER ',' CSV
COPY 10000000
Time: 293663.817 ms (04:53.664)
```

Comprobamos que ha necesito mucho más tiempo para la última carga de datos. Lo cual es lógico ya que tiene que comprobar las referencias de intregridad de datos entre las otras dos tablas. Pero es que además, el CSV asociado a esta carga, tiene un peso mucho mas elevado.

```
root@postgresql01:/home/felix/pl2# du -sh *
93M     datos_empleados.csv
4.5M    datos_proyectos.csv
171M    datos_trabaja_proyectos.csv
```

```
SELECT * from pg_catalog.pg_stat_progress_copy;
```


----------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------



Cuestión 3: Mostrar las estadísticas obtenidas en este momento para cada tabla. ¿Qué
se almacena? ¿Son correctas? Si no son correctas, ¿cómo se pueden actualizar?

Para saber si estan actualizadas:
```
select * from pg_stat_user_tables 
```
Ademas de esto sabemos que para actualizarla hay que hacer un analyze.



----------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------




Cuestión 4: Aplicar el comando EXPLAIN a una consulta que obtenga la información
de los empleados con salario de más de 96000 euros. ¿Son correctos los resultados
del comando EXPLAIN? ¿Por qué? Comparar con lo que se obtendría con lo visto en
teoría obteniendo las estadísticas de las tablas con postgres.

(FALTA COMPARAR CON LO VISTO EN TEORÍA)

```
proyectos_empresas=# explain select * from empleados where salario > 96000
proyectos_empresas-# ;
                                   QUERY PLAN                                    
---------------------------------------------------------------------------------
 Gather  (cost=1000.00..40125.37 rows=100357 width=41)
   Workers Planned: 2
   ->  Parallel Seq Scan on empleados  (cost=0.00..29089.67 rows=41815 width=41)
         Filter: (salario > '96000'::numeric)
(4 rows)
```
