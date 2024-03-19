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


----------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------



Cuestión 3: Mostrar las estadísticas obtenidas en este momento para cada tabla. ¿Qué se almacena? ¿Son correctas? Si no son correctas, ¿cómo se pueden actualizar?


Activamos la vista display ON:
```
postgres=# \x
Expanded display is on.
```

 1: Data distribution statistics
    Se almacenan en  pg_statistic system catalog, y son visibles mediante la vista  pg_stats. Ahora bien, de entrada no estan disponibles o no actualizadas, debemos lanzar ANALYZE o un proceso de autovacuum para que se actualicen.
    Lo que vamos a visualizar es una estadísitaca para cada columna, 4 records, 4 columnas. Podemos ver los siguientes campos:


    ```
    schemaname: El esquema al que pertenece la tabla.
    tablename: El nombre de la tabla.
    attname: El nombre de la columna.
    inherited: Indica si esta columna es heredada de una tabla padre.
    null_frac: La fracción de valores nulos en la columna.
    avg_width: El ancho promedio de los valores en la columna en bytes.
    n_distinct: El número estimado de valores distintos en la columna. En este caso, -1 indica que no se han calculado las estadísticas para los valores distintos.
    most_common_vals: Los valores más comunes en la columna.
    most_common_freqs: La frecuencia de los valores más comunes en la columna.
    histogram_bounds: Los límites del histograma para la columna, que ayudan a PostgreSQL a estimar la distribución de los valores. Aquí, parece que hay muchos valores diferentes, por lo que se proporcionan límites para ayudar a estimar la distribución.
    correlation: La correlación entre los valores de esta columna y los valores de otras columnas en la misma tabla. Un valor negativo indica una correlación inversa, mientras que un valor positivo indica una correlación directa. Cuando el valor está cerca de -1 o +1, se estima que un escaneo de índice en la columna será más económico que cuando está cerca de 0, debido a la reducción del acceso aleatorio al disco. 
    most_common_elems: Elementos más comunes en una columna de tipo de datos de arreglo.
    most_common_elem_freqs: Frecuencia de los elementos más comunes en una columna de tipo de datos de arreglo.
    elem_count_histogram: Histograma de recuento de elementos para una columna de tipo de datos de arreglo.

    ```

    La actualización se realiza mediante ANALYZE <nombre_de_tabla>


    empleados:
        ```
            ANALYZE VERBOSE empleados ;
            INFO:  analyzing "public.empleados"
            INFO:  "empleados": scanned 18696 of 18696 pages, containing 2000000 live rows and 0 dead rows; 30000 rows in sample, 2000000 estimated total rows
            ANALYZE
        ```

        ```
        SELECT * FROM pg_stats WHERE tablename ='empleados';
        ``` 

        ```
                -[ RECORD 1 ]----------
                schemaname             | public
                tablename              | empleados
                attname                | nombre
                inherited              | f
                null_frac              | 0
                avg_width              | 13
                n_distinct             | -1
                most_common_vals       | 
                most_common_freqs      | 
                histogram_bounds       | {nombre1000066,nombre1018454,nombre1037631,nombre1055675,nombre1073630,nombre1091927,nombre1109521,nombre112747,nombre114640,nombre116400,nombre1181465,nombre1200894,nombre1219311,nombre1237101,nombre1254316,nombre1273941,nombre1294242,nombre1312266,nombre1331354,nombre1350426,nombre1369512,nombre1387822,nombre1406347,nombre1424492,nombre1442968,nombre1459513,nombre1478770,nombre1497874,nombre151612,nombre153475,nombre1552535,nombre1570805,nombre1588240,nombre1606995,nombre16224,nombre1641266,nombre1659037,nombre1678689,nombre1697696,nombre1716340,nombre1735288,nombre1752330,nombre1769440,nombre1785941,nombre1806041,nombre1824583,nombre184109,nombre1859854,nombre1876366,nombre1896129,nombre1913492,nombre1931581,nombre1950535,nombre1969781,nombre1988167,nombre206826,nombre226569,nombre241982,nombre26112,nombre279943,nombre297097,nombre31510,nombre335485,nombre353309,nombre370296,nombre388273,nombre405181,nombre421883,nombre440150,nombre458350,nombre477212,nombre494389,nombre511249,nombre52823,nombre547532,nombre565557,nombre582889,nombre599614,nombre615596,nombre631886,nombre649954,nombre667743,nombre685375,nombre703419,nombre718645,nombre736107,nombre754335,nombre774373,nombre789689,nombre809729,nombre827834,nombre844457,nombre861070,nombre879008,nombre896694,nombre914584,nombre929999,nombre94704,nombre964660,nombre982375,nombre999978}
                correlation            | -0.4015029
                most_common_elems      | 
                most_common_elem_freqs | 
                elem_count_histogram   | 
                -[ RECORD 2 ]----------
                schemaname             | public
                tablename              | empleados
                attname                | numero_empleado
                inherited              | f
                null_frac              | 0
                avg_width              | 6
                n_distinct             | -1
                most_common_vals       | 
                most_common_freqs      | 
                histogram_bounds       | {95,20153,39643,59259,78704,97763,119847,141033,160476,180249,203982,225725,243187,264853,285262,304109,325338,346411,365416,385560,404479,423592,444192,464516,484217,502716,521558,541872,562065,582430,600781,618937,636014,656638,676025,695850,714045,732004,752193,775153,794227,814871,834414,853635,872455,891973,911954,929229,948241,968798,988026,1008334,1027210,1047998,1068216,1088277,1107277,1126795,1148563,1168060,1187826,1208823,1228902,1248112,1268614,1292068,1312012,1332384,1354230,1374867,1395270,1416194,1435498,1455170,1476464,1497819,1517727,1537274,1558556,1578745,1598745,1617906,1637301,1658069,1679074,1699905,1721404,1740852,1760450,1779011,1799212,1821058,1838710,1859725,1878667,1899725,1918424,1939042,1958968,1979646,1999950}
                correlation            | 1
                most_common_elems      | 
                most_common_elem_freqs | 
                elem_count_histogram   | 
                -[ RECORD 3 ]----------
                schemaname             | public
                tablename              | empleados
                attname                | apellidos
                inherited              | f
                null_frac              | 0
                avg_width              | 16
                n_distinct             | -1
                most_common_vals       | 
                most_common_freqs      | 
                histogram_bounds       | {apellidos1000066,apellidos1018454,apellidos1037631,apellidos1055675,apellidos1073630,apellidos1091927,apellidos1109521,apellidos112747,apellidos114640,apellidos116400,apellidos1181465,apellidos1200894,apellidos1219311,apellidos1237101,apellidos1254316,apellidos1273941,apellidos1294242,apellidos1312266,apellidos1331354,apellidos1350426,apellidos1369512,apellidos1387822,apellidos1406347,apellidos1424492,apellidos1442968,apellidos1459513,apellidos1478770,apellidos1497874,apellidos151612,apellidos153475,apellidos1552535,apellidos1570805,apellidos1588240,apellidos1606995,apellidos16224,apellidos1641266,apellidos1659037,apellidos1678689,apellidos1697696,apellidos1716340,apellidos1735288,apellidos1752330,apellidos1769440,apellidos1785941,apellidos1806041,apellidos1824583,apellidos184109,apellidos1859854,apellidos1876366,apellidos1896129,apellidos1913492,apellidos1931581,apellidos1950535,apellidos1969781,apellidos1988167,apellidos206826,apellidos226569,apellidos241982,apellidos26112,apellidos279943,apellidos297097,apellidos31510,apellidos335485,apellidos353309,apellidos370296,apellidos388273,apellidos405181,apellidos421883,apellidos440150,apellidos458350,apellidos477212,apellidos494389,apellidos511249,apellidos52823,apellidos547532,apellidos565557,apellidos582889,apellidos599614,apellidos615596,apellidos631886,apellidos649954,apellidos667743,apellidos685375,apellidos703419,apellidos718645,apellidos736107,apellidos754335,apellidos774373,apellidos789689,apellidos809729,apellidos827834,apellidos844457,apellidos861070,apellidos879008,apellidos896694,apellidos914584,apellidos929999,apellidos94704,apellidos964660,apellidos982375,apellidos999978}
                correlation            | -0.4015029
                most_common_elems      | 
                most_common_elem_freqs | 
                elem_count_histogram   | 
                -[ RECORD 4 ]----------
                schemaname             | public
                tablename              | empleados
                attname                | salario
                inherited              | f
                null_frac              | 0
                avg_width              | 6
                n_distinct             | 94095
                most_common_vals       | 
                most_common_freqs      | 
                histogram_bounds       | {1000.000,1970.000,2926.000,3939.000,4906.000,5982.000,7003.000,7953.000,8866.000,9873.000,10860.00,11831.00,12812.00,13791.00,14726.00,15710.00,16844.00,17815.00,18776.00,19768.00,20655.00,21696.00,22775.00,23844.00,24843.00,25971.00,27019.00,27977.00,28928.00,29856.00,30779.00,31752.00,32692.00,33784.00,34808.00,35797.00,36836.00,37787.00,38814.00,39902.00,40963.00,41880.00,42877.00,43820.00,44835.00,45785.00,46763.00,47774.00,48718.00,49725.00,50689.00,51645.00,52657.00,53618.00,54577.00,55592.00,56552.00,57619.00,58684.00,59807.00,60754.00,61727.00,62639.00,63520.00,64478.00,65428.00,66355.00,67362.00,68362.00,69391.00,70317.00,71241.00,72268.00,73207.00,74244.00,75194.00,76296.00,77334.00,78319.00,79316.00,80292.00,81374.00,82369.00,83328.00,84420.00,85552.00,86510.00,87626.00,88564.00,89531.00,90455.00,91560.00,92636.00,93686.00,94780.00,95784.00,96756.00,97885.00,98935.00,99965.00,100994.0}
                correlation            | -0.00281962
                most_common_elems      | 
                most_common_elem_freqs | 
                elem_count_histogram   | 
        ```

proyectos
  
  ```
    ANALYZE VERBOSE proyectos ;
        INFO:  analyzing "public.proyectos"
        INFO:  "proyectos": scanned 968 of 968 pages, containing 100000 live rows and 0 dead rows; 30000 rows in sample, 100000 estimated total rows
        ANALYZE
        Time: 282.382 ms
  ```

  ```
    SELECT * FROM pg_stats WHERE tablename ='proyectos';
  ```
  
    
  ```
    -[ RECORD 1 ]----------
        schemaname             | public
        tablename              | proyectos
        attname                | numero_proyecto
        inherited              | f
        null_frac              | 0
        avg_width              | 6
        n_distinct             | -1
        most_common_vals       | 
        most_common_freqs      | 
        histogram_bounds       | {1,1012,1986,2947,3941,4972,5945,6978,7944,8896,9979,10986,12021,13064,14115,15127,16130,17158,18208,19207,20144,21205,22205,23154,24137,25130,26139,27105,28071,29044,29996,30906,31908,32862,33824,34936,35875,36822,37805,38725,39690,40566,41545,42621,43639,44605,45569,46572,47524,48576,49564,50555,51548,52565,53531,54591,55610,56615,57600,58650,59708,60737,61774,62792,63833,64869,65875,66940,67940,69002,69942,70880,71885,72868,73842,74845,75855,76889,77936,78924,79901,80929,81904,82926,83907,84894,85882,86886,87962,89018,89979,91002,91971,93025,94091,95071,96074,97009,97960,98990,100000}
        correlation            | 1
        most_common_elems      | 
        most_common_elem_freqs | 
        elem_count_histogram   | 
        -[ RECORD 2 ]----------
        schemaname             | public
        tablename              | proyectos
        attname                | nombre
        inherited              | f
        null_frac              | 0
        avg_width              | 11
        n_distinct             | -1
        most_common_vals       | 
        most_common_freqs      | 
        histogram_bounds       | {nombre1,nombre10867,nombre11811,nombre12747,nombre13666,nombre14634,nombre15494,nombre16436,nombre17371,nombre18274,nombre1917,nombre20016,nombre20924,nombre21861,nombre22734,nombre23632,nombre24504,nombre25409,nombre26299,nombre27156,nombre28025,nombre28900,nombre29745,nombre30602,nombre31430,nombre3234,nombre33219,nombre34109,nombre35128,nombre35930,nombre368,nombre37677,nombre38526,nombre39402,nombre40166,nombre41018,nombre41906,nombre42931,nombre4380,nombre44680,nombre45564,nombre46470,nombre47365,nombre48288,nombre49168,nombre50081,nombre50947,nombre51858,nombre5272,nombre53606,nombre54558,nombre55488,nombre56381,nombre57288,nombre5824,nombre59112,nombre60132,nombre610,nombre61949,nombre62872,nombre63815,nombre64776,nombre6565,nombre66600,nombre67545,nombre68470,nombre69370,nombre70186,nombre71095,nombre71989,nombre72867,nombre73764,nombre74644,nombre75574,nombre76453,nombre77331,nombre78299,nombre79179,nombre80077,nombre81020,nombre81903,nombre82841,nombre83686,nombre84577,nombre8543,nombre86373,nombre87239,nombre88236,nombre89130,nombre90032,nombre90947,nombre91806,nombre92722,nombre93671,nombre94591,nombre95455,nombre96399,nombre97243,nombre98174,nombre99062,nombre99998}
        correlation            | 0.8193038
        most_common_elems      | 
        most_common_elem_freqs | 
        elem_count_histogram   | 
        -[ RECORD 3 ]----------
        schemaname             | public
        tablename              | proyectos
        attname                | localizacion
        inherited              | f
        null_frac              | 0
        avg_width              | 17
        n_distinct             | -1
        most_common_vals       | 
        most_common_freqs      | 
        histogram_bounds       | {localizacion1,localizacion10867,localizacion11811,localizacion12747,localizacion13666,localizacion14634,localizacion15494,localizacion16436,localizacion17371,localizacion18274,localizacion1917,localizacion20016,localizacion20924,localizacion21861,localizacion22734,localizacion23632,localizacion24504,localizacion25409,localizacion26299,localizacion27156,localizacion28025,localizacion28900,localizacion29745,localizacion30602,localizacion31430,localizacion3234,localizacion33219,localizacion34109,localizacion35128,localizacion35930,localizacion368,localizacion37677,localizacion38526,localizacion39402,localizacion40166,localizacion41018,localizacion41906,localizacion42931,localizacion4380,localizacion44680,localizacion45564,localizacion46470,localizacion47365,localizacion48288,localizacion49168,localizacion50081,localizacion50947,localizacion51858,localizacion5272,localizacion53606,localizacion54558,localizacion55488,localizacion56381,localizacion57288,localizacion5824,localizacion59112,localizacion60132,localizacion610,localizacion61949,localizacion62872,localizacion63815,localizacion64776,localizacion6565,localizacion66600,localizacion67545,localizacion68470,localizacion69370,localizacion70186,localizacion71095,localizacion71989,localizacion72867,localizacion73764,localizacion74644,localizacion75574,localizacion76453,localizacion77331,localizacion78299,localizacion79179,localizacion80077,localizacion81020,localizacion81903,localizacion82841,localizacion83686,localizacion84577,localizacion8543,localizacion86373,localizacion87239,localizacion88236,localizacion89130,localizacion90032,localizacion90947,localizacion91806,localizacion92722,localizacion93671,localizacion94591,localizacion95455,localizacion96399,localizacion97243,localizacion98174,localizacion99062,localizacion99998}
        correlation            | 0.8193038
        most_common_elems      | 
        most_common_elem_freqs | 
        elem_count_histogram   | 
        -[ RECORD 4 ]----------
        schemaname             | public
        tablename              | proyectos
        attname                | coste
        inherited              | f
        null_frac              | 0
        avg_width              | 6
        n_distinct             | 9810
        most_common_vals       | {11598.00,13157.00,16179.00,19488.00,10918.00,11299.00,11858.00,15725.00,15942.00,16495.00,17944.00,18748.00,19574.00,10391.00,11111.00,11155.00,11300.00,12371.00,12555.00,12624.00,12674.00,12865.00,12886.00,12939.00,13237.00,13744.00,13878.00,15084.00,15302.00,16583.00,17044.00,17213.00,17259.00,18933.00,19837.00}
        most_common_freqs      | {0.00036666667,0.00036666667,0.00036666667,0.00036666667,0.00033333333,0.00033333333,0.00033333333,0.00033333333,0.00033333333,0.00033333333,0.00033333333,0.00033333333,0.00033333333,0.0003,0.0003,0.0003,0.0003,0.0003,0.0003,0.0003,0.0003,0.0003,0.0003,0.0003,0.0003,0.0003,0.0003,0.0003,0.0003,0.0003,0.0003,0.0003,0.0003,0.0003,0.0003}
        histogram_bounds       | {10000.00,10090.00,10195.00,10296.00,10396.00,10495.00,10589.00,10699.00,10799.00,10894.00,10989.00,11100.00,11194.00,11291.00,11399.00,11510.00,11600.00,11689.00,11787.00,11888.00,11988.00,12088.00,12181.00,12284.00,12384.00,12479.00,12572.00,12672.00,12783.00,12883.00,12984.00,13082.00,13178.00,13278.00,13375.00,13470.00,13574.00,13679.00,13785.00,13894.00,13994.00,14099.00,14192.00,14290.00,14396.00,14500.00,14590.00,14692.00,14789.00,14884.00,14979.00,15080.00,15177.00,15274.00,15379.00,15476.00,15578.00,15692.00,15794.00,15895.00,15998.00,16092.00,16193.00,16300.00,16398.00,16500.00,16599.00,16702.00,16795.00,16893.00,17003.00,17097.00,17187.00,17287.00,17388.00,17479.00,17573.00,17668.00,17761.00,17854.00,17959.00,18062.00,18163.00,18258.00,18365.00,18475.00,18574.00,18672.00,18778.00,18882.00,18985.00,19094.00,19195.00,19296.00,19399.00,19501.00,19600.00,19697.00,19804.00,19905.00,19999.00}
        correlation            | -0.0056740893
        most_common_elems      | 
        most_common_elem_freqs | 
        elem_count_histogram   | 

  ```

trabaja_proyectos:
    
    ```
    ANALYZE VERBOSE trabaja_proyectos ;
        INFO:  analyzing "public.trabaja_proyectos"
        INFO:  "trabaja_proyectos": scanned 30000 of 63728 pages, containing 4707804 live rows and 0 dead rows; 30000 rows in sample, 10000631 estimated total rows
        ANALYZE
    ```
    
    ```
    SELECT * FROM pg_stats WHERE tablename ='trabaja_proyectos';
    ```


    ```
    -[ RECORD 1 ]----------
    schemaname             | public
    tablename              | trabaja_proyectos
    attname                | numero_empleado
    inherited              | f
    null_frac              | 0
    avg_width              | 6
    n_distinct             | -0.149868
    most_common_vals       | 
    most_common_freqs      | 
    histogram_bounds       | {15,20659,38843,57493,76903,96343,115952,135315,157105,179196,198787,217371,236001,256971,276149,294876,314180,334632,352933,370987,390964,410736,430257,449877,470443,493496,513641,534424,553922,573791,594093,614867,635973,658935,681755,702028,720575,740584,759479,780128,800412,820616,841421,861164,880757,901042,921395,942077,962797,982624,1003352,1023705,1043788,1062657,1084216,1101821,1121506,1143228,1164595,1185429,1205120,1225708,1245335,1265141,1284991,1304521,1325156,1345726,1365383,1387011,1406715,1426170,1443750,1463446,1483223,1503706,1523525,1544620,1564177,1584585,1602851,1623669,1642895,1661292,1679425,1701758,1720165,1741080,1761139,1780556,1798187,1818486,1837316,1859492,1880810,1897867,1918264,1938677,1958365,1978949,1999950}
    correlation            | -0.0086555295
    most_common_elems      | 
    most_common_elem_freqs | 
    elem_count_histogram   | 
    -[ RECORD 2 ]----------
    schemaname             | public
    tablename              | trabaja_proyectos
    attname                | numero_proyecto
    inherited              | f
    null_frac              | 0
    avg_width              | 6
    n_distinct             | 98496
    most_common_vals       | 
    most_common_freqs      | 
    histogram_bounds       | {1,925,1932,2863,3838,4903,5973,7099,8183,9248,10215,11129,11966,13073,14108,15100,16117,17119,18147,19244,20215,21227,22265,23345,24277,25273,26229,27220,28173,29135,30079,31047,32121,33160,34173,35181,36245,37204,38181,39204,40121,41062,42090,43121,44156,45255,46165,47210,48173,49175,50148,51054,52115,53069,54032,55188,56235,57255,58202,59164,60160,61227,62229,63073,64074,65126,66098,67057,68155,69097,70219,71174,72201,73167,74156,75188,76251,77212,78258,79087,80097,81166,82260,83253,84240,85218,86150,87157,88210,89167,90095,91089,92113,93108,94070,95205,96074,97043,97990,98959,99996}
    correlation            | -0.004180803
    most_common_elems      | 
    most_common_elem_freqs | 
    elem_count_histogram   | 
    -[ RECORD 3 ]----------
    schemaname             | public
    tablename              | trabaja_proyectos
    attname                | horas
    inherited              | f
    null_frac              | 0
    avg_width              | 4
    n_distinct             | 24
    most_common_vals       | {7,11,8,20,22,15,12,5,4,18,21,19,14,2,13,1,9,0,3,6,10,17,16,23}
    most_common_freqs      | {0.042966668,0.042933334,0.0428,0.0428,0.0426,0.04256667,0.0424,0.0423,0.042233333,0.042066667,0.042033333,0.041633334,0.0413,0.041233335,0.041233335,0.041033335,0.041033335,0.040966667,0.040966667,0.04083333,0.04083333,0.0408,0.0407,0.03973333}
    histogram_bounds       | 
    correlation            | 0.043831687
    most_common_elems      | 
    most_common_elem_freqs | 
    elem_count_histogram   | 
    ```


2: Extended statistics

Las estadísticas de ANALYZE se almacenan en una base de datos por columna y tabla, y por lo tanto no pueden capturar ningún conocimiento sobre la correlación entre columnas. Es común ver consultas lentas ejecutando malos planes de ejecución porque múltiples columnas utilizadas en las cláusulas de consulta están correlacionadas. Sin embargo, con el comando CREATE STATISTICS, puedes crear estadísticas extendidas para columnas correlacionadas.

Podemos hacerlo de la siguiente forma:
    CREATE TABLE ext_stats(numero_empleado NUMERIC, salario NUMERIC);


3: Monitoring statistics

Estas estadísticas recopilan información sobre el número de accesos a tablas e índices, tanto en términos de bloques de disco como de filas individuales. También realizan un seguimiento del número total de filas en cada tabla, así como información sobre las acciones de vacío y análisis para cada tabla (cuándo se ejecutaron por última vez en la tabla).



 ``` 
SELECT * FROM pg_stat_user_tables WHERE relname='empleados';
-[ RECORD 1 ]-------+------------------------------
relid               | 18454
schemaname          | public
relname             | empleados
seq_scan            | 3
last_seq_scan       | 2024-03-12 00:06:20.885991+00
seq_tup_read        | 4000000
idx_scan            | 10000000
last_idx_scan       | 2024-03-12 00:15:05.890623+00
idx_tup_fetch       | 10000000
n_tup_ins           | 6000000
n_tup_upd           | 0
n_tup_del           | 4000000
n_tup_hot_upd       | 0
n_tup_newpage_upd   | 0
n_live_tup          | 2000000
n_dead_tup          | 0
n_mod_since_analyze | 0
n_ins_since_vacuum  | 0
last_vacuum         | 
last_autovacuum     | 2024-03-12 00:07:34.171257+00
last_analyze        | 
last_autoanalyze    | 2024-03-12 00:07:34.999046+00
vacuum_count        | 0
autovacuum_count    | 4
analyze_count       | 0
autoanalyze_count   | 4
 ```

 ```
SELECT * FROM pg_stat_user_tables WHERE relname='proyectos';
-[ RECORD 1 ]-------+------------------------------
relid               | 18461
schemaname          | public
relname             | proyectos
seq_scan            | 1
last_seq_scan       | 2024-03-11 23:57:05.800873+00
seq_tup_read        | 0
idx_scan            | 10000000
last_idx_scan       | 2024-03-12 00:15:05.890623+00
idx_tup_fetch       | 10000000
n_tup_ins           | 100000
n_tup_upd           | 0
n_tup_del           | 0
n_tup_hot_upd       | 0
n_tup_newpage_upd   | 0
n_live_tup          | 100000
n_dead_tup          | 0
n_mod_since_analyze | 0
n_ins_since_vacuum  | 0
last_vacuum         | 
last_autovacuum     | 2024-03-12 00:08:28.550644+00
last_analyze        | 
last_autoanalyze    | 2024-03-12 00:08:28.88351+00
vacuum_count        | 0
autovacuum_count    | 1
analyze_count       | 0
autoanalyze_count   | 1
 ```

```
 SELECT * FROM pg_stat_user_tables WHERE relname='trabaja_proyectos';
-[ RECORD 1 ]-------+------------------------------
relid               | 18468
schemaname          | public
relname             | trabaja_proyectos
seq_scan            | 1
last_seq_scan       | 2024-03-11 23:57:11.237232+00
seq_tup_read        | 0
idx_scan            | 4000000
last_idx_scan       | 2024-03-12 00:06:20.885991+00
idx_tup_fetch       | 0
n_tup_ins           | 10000000
n_tup_upd           | 0
n_tup_del           | 0
n_tup_hot_upd       | 0
n_tup_newpage_upd   | 0
n_live_tup          | 9999306
n_dead_tup          | 0
n_mod_since_analyze | 0
n_ins_since_vacuum  | 0
last_vacuum         | 
last_autovacuum     | 2024-03-12 00:15:54.839373+00
last_analyze        | 
last_autoanalyze    | 2024-03-12 00:15:55.744766+00
vacuum_count        | 0
autovacuum_count    | 1
analyze_count       | 0
autoanalyze_count   | 1
```


----------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------


Cuestión 4: Aplicar el comando EXPLAIN a una consulta que obtenga la información de los empleados con salario de más de 96000 euros. ¿Son correctos los resultados del comando EXPLAIN? ¿Por qué? Comparar con lo que se obtendría con lo visto en
teoría obteniendo las estadísticas de las tablas con postgres.

(FALTA COMPARAR CON LO VISTO EN TEORÍA)


```
    explain select * from empleados where salario > 96000;
                                QUERY PLAN                            
    ------------------------------------------------------------------
    Seq Scan on empleados  (cost=0.00..43696.00 rows=99438 width=41)
    Filter: (salario > '96000'::numeric)
    (2 rows)

    Time: 0.358 ms
```

----------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------

Cuestión 5: Aplicar el comando EXPLAIN a una consulta que obtenga la información de los proyectos en los cuales el empleado trabaja 8 horas. ¿Son correctos los
resultados del comando EXPLAIN? ¿Por qué? Comparar con lo que se obtendría con lo visto en teoría obteniendo las estadísticas de las tablas con postgres.

 (FALTA COMPARAR CON LO VISTO EN TEORÍA)

EXPLAIN SELECT p.* FROM proyectos p JOIN trabaja_proyectos tp ON p.numero_proyecto = tp.numero_proyecto WHERE tp.horas = 8;

----------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------


Cuestión 6: Aplicar el comando EXPLAIN a una consulta que obtenga la información
de los proyectos que tienen un coste mayor de 10000, y tienen empleados de salario
de 24000 euros y trabajan menos de 3 horas en ellos. ¿Son correctos los resultados
del comando EXPLAIN? ¿Por qué? Comparar con lo que se obtendría con lo visto en
teoría obteniendo las estadísticas de las tablas con postgres.



----------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------



Cuestión 7: Generar los datos solicitados al comienzo de la práctica para la base de
datos Logística creando un programa para tal fin que deberá de estar en un único
fichero y comentado. Pegar el código del fichero en el cuadro de texto que se adjunta
a continuación.

1º Generar las bases de datos:

createDBpl2.sql :

```
-- Database generated with pgModeler (PostgreSQL Database Modeler).
-- pgModeler version: 0.9.4
-- PostgreSQL version: 13.0
-- Project Site: pgmodeler.io
-- Model Author: ---

-- Database creation must be performed outside a multi lined SQL file. 
-- These commands were put in this file only as a convenience.
-- 
-- object: new_database | type: DATABASE --
-- DROP DATABASE IF EXISTS new_database;
-- CREATE DATABASE logistica;
-- ddl-end --


-- object: public.bultos | type: TABLE --
-- DROP TABLE IF EXISTS public.bultos CASCADE;
CREATE TABLE public.bultos (
        id_bulto integer NOT NULL,
        direccion_origen text NOT NULL,
        direccion_destino text NOT NULL,
        provincia_origen text NOT NULL,
        provincia_destino text NOT NULL,
        peso real NOT NULL,
        fecha_salida date NOT NULL,
        fecha_llegada date NOT NULL,
        matricula_vehiculos char(7),
        id_cliente_clientes integer,
        CONSTRAINT bultos_pk PRIMARY KEY (id_bulto)
);
-- ddl-end --
ALTER TABLE public.bultos OWNER TO postgres;
-- ddl-end --

-- object: public.vehiculos | type: TABLE --
-- DROP TABLE IF EXISTS public.vehiculos CASCADE;
CREATE TABLE public.vehiculos (
        matricula char(7) NOT NULL,
        marca text NOT NULL,
        modelo text NOT NULL,
        kilometros integer NOT NULL,
        fecha_matricula date NOT NULL,
        "DNI_conductores" char(9),
        CONSTRAINT vehiculos_pk PRIMARY KEY (matricula)
);
-- ddl-end --
ALTER TABLE public.vehiculos OWNER TO postgres;
-- ddl-end --

-- object: public.empresas | type: TABLE --
-- DROP TABLE IF EXISTS public.empresas CASCADE;
CREATE TABLE public.empresas (
        "CIF" char(9) NOT NULL,
        nombre text NOT NULL,
        direccion text NOT NULL,
        "Provincia" text NOT NULL,
        email text NOT NULL,
        telefono integer NOT NULL,
        CONSTRAINT email_unique UNIQUE (email),
        CONSTRAINT telefono_unique UNIQUE (telefono),
        CONSTRAINT emresas_pk PRIMARY KEY ("CIF")
);
-- ddl-end --
ALTER TABLE public.empresas OWNER TO postgres;
-- ddl-end --

-- object: public.conductores | type: TABLE --
-- DROP TABLE IF EXISTS public.conductores CASCADE;
CREATE TABLE public.conductores (
        "DNI" char(9) NOT NULL,
        nombre text NOT NULL,
        fecha_contrato date NOT NULL,
        telefono integer NOT NULL,
        salario real NOT NULL,
        "CIF_empresas" char(9),
        CONSTRAINT conductores_pk PRIMARY KEY ("DNI")
);
-- ddl-end --
ALTER TABLE public.conductores OWNER TO postgres;
-- ddl-end --

-- object: public.clientes | type: TABLE --
-- DROP TABLE IF EXISTS public.clientes CASCADE;
CREATE TABLE public.clientes (
        id_cliente integer NOT NULL,
        nombre text NOT NULL,
        direccion text NOT NULL,
        provincia text NOT NULL,
        email text NOT NULL,
        telefono integer NOT NULL,
        CONSTRAINT telefono_cliente_unique UNIQUE (email),
        CONSTRAINT email_cliente_unique UNIQUE (email),
        CONSTRAINT clientes_pk PRIMARY KEY (id_cliente)
);
-- ddl-end --
ALTER TABLE public.clientes OWNER TO postgres;
-- ddl-end --

-- object: vehiculos_fk | type: CONSTRAINT --
-- ALTER TABLE public.bultos DROP CONSTRAINT IF EXISTS vehiculos_fk CASCADE;
ALTER TABLE public.bultos ADD CONSTRAINT vehiculos_fk FOREIGN KEY (matricula_vehiculos)
REFERENCES public.vehiculos (matricula) MATCH FULL
ON DELETE RESTRICT ON UPDATE RESTRICT;
-- ddl-end --

-- object: clientes_fk | type: CONSTRAINT --
-- ALTER TABLE public.bultos DROP CONSTRAINT IF EXISTS clientes_fk CASCADE;
ALTER TABLE public.bultos ADD CONSTRAINT clientes_fk FOREIGN KEY (id_cliente_clientes)
REFERENCES public.clientes (id_cliente) MATCH FULL
ON DELETE RESTRICT ON UPDATE RESTRICT;
-- ddl-end --

-- object: empresas_fk | type: CONSTRAINT --
-- ALTER TABLE public.conductores DROP CONSTRAINT IF EXISTS empresas_fk CASCADE;
ALTER TABLE public.conductores ADD CONSTRAINT empresas_fk FOREIGN KEY ("CIF_empresas")
REFERENCES public.empresas ("CIF") MATCH FULL
ON DELETE RESTRICT ON UPDATE RESTRICT;
-- ddl-end --

-- object: conductores_fk | type: CONSTRAINT --
-- ALTER TABLE public.vehiculos DROP CONSTRAINT IF EXISTS conductores_fk CASCADE;
ALTER TABLE public.vehiculos ADD CONSTRAINT conductores_fk FOREIGN KEY ("DNI_conductores")
REFERENCES public.conductores ("DNI") MATCH FULL
ON DELETE RESTRICT ON UPDATE RESTRICT;
-- ddl-end --
```

```
sudo -u postgres psql -d logistica -f createDBpl2.sql 
```

```
CREATE TABLE
ALTER TABLE
CREATE TABLE
ALTER TABLE
CREATE TABLE
ALTER TABLE
CREATE TABLE
ALTER TABLE
CREATE TABLE
ALTER TABLE
ALTER TABLE
ALTER TABLE
ALTER TABLE
ALTER TABLE
```

```
\l
                                                           List of databases
       Name        |  Owner   | Encoding | Locale Provider |   Collate   |    Ctype    | ICU Locale | ICU Rules |   Access privileges   
-------------------+----------+----------+-----------------+-------------+-------------+------------+-----------+-----------------------
 logistica         | postgres | UTF8     | libc            | en_US.UTF-8 | en_US.UTF-8 |            |           | 
```

```
\c logistica
You are now connected to database "logistica" as user "postgres".
```

```
logistica=# \dt
            List of relations
 Schema |    Name     | Type  |  Owner   
--------+-------------+-------+----------
 public | bultos      | table | postgres
 public | clientes    | table | postgres
 public | conductores | table | postgres
 public | empresas    | table | postgres
 public | vehiculos   | table | postgres
(5 rows)
```

La generacíon de datos debe seguir el siguiente orden:

```
EMPRESAS ----> CONDUCTORES ---->  CLIENTES ----> VEHICULOS ---->  BULTOS
```

Basado en ese orden para respetar la integridad de datos, se generaran los registros mediantes funciones. Un csv por cada tabla.
En el siguiente apartado se hará la carga. Es importante que la carga se realice respetando el orden.


generateRandomDat.py: 
```
from datetime import datetime, timedelta
import random
import string
import csv

##########################################################################################

# GENERADOR DE CIFs

        
# GENERADOR DE NOMBRES DE EMPRESA       
def obtener_nombres_empresas():
    nombres_empresas = []
    with open('companies.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            nombres_empresas.append(row[1])  
    return nombres_empresas


def generar_cif(cifs_generados, Provincia):
    while True:
        # Selecciona aleatoriamente un tipo de CIF (persona jurídica o persona física)
        tipo_cif = random.choice(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'P', 'Q', 'R', 'S', 'U', 'V', 'N', 'W'])
        codigoProvincia= Provincia[0]
        # Genera los 7 dígitos aleatorios para el CIF
        numeros = ''.join(random.choices(string.digits, k=6))

        # Calcula la letra de control
        letras_cif = 'JABCDEFGHI'
        suma = sum(int(n) if i % 2 else int(n)*2//10 + int(n)*2%10 for i, n in enumerate(numeros))
        if (10 - suma % 10) == 10:
            letra_control = 'J'  # Como el residuo es 0, la letra de control sería 'J'
        else:
            letra_control = letras_cif[10 - suma % 10]

        # Concatena todos los componentes para formar el CIF completo
        cif = tipo_cif + codigoProvincia + numeros + letra_control
        if cif not in cifs_generados:
                cifs_generados.add(cif)
                return cif


# GENERADOR DE NOMBRES DE CALLE    
def obtener_nombres_calles():
    nombres_calles = []
    with open('calles.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            nombres_calles.append(row[3])  
    return nombres_calles

def obtener_provincia_aleatoria():
    provincias_espanolas = [
        "Alava", "Albacete", "Alicante", "Almeria", "Asturias", "Avila", "Badajoz", "Barcelona", 
        "Burgos", "Caceres", "Cádiz", "Cantabria", "Castellon", "Ceuta", "Ciudad Real", "Cordoba", 
        "Cuenca", "Girona", "Las Palmas", "Granada", "Guadalajara", "Guipuzcoa", "Huelva", "Huesca", 
        "Illes Balears", "Jaen", "La Coruna", "La Rioja", "Leon", "Lleida", "Lugo", "Madrid", "Malaga", 
        "Melilla", "Murcia", "Navarra", "Ourense", "Palencia", "Pontevedra", "Salamanca", "Santa Cruz de Tenerife", 
        "Segovia", "Sevilla", "Soria", "Tarragona", "Teruel", "Toledo", "Valencia", "Valladolid", "Vizcaya", 
        "Zamora", "Zaragoza"
    ]
    return random.choice(provincias_espanolas)


def generar_email_aleatorio():
    dominios = ["gmail.com", "hotmail.com", "yahoo.com", "outlook.com", "uah.com"]
    nombre_usuario = ''.join(random.choices(string.ascii_lowercase + string.digits, k=random.randint(5, 10)))
    dominio = random.choice(dominios)
    return f"{nombre_usuario}@{dominio}"

def generar_telefono_aleatorio(conjunto_telefonos):
    while True:
        prefijo = random.choice(['6', '7', '8', '9'])
        numero = ''.join(random.choices('0123456789', k=8))
        telefono = f"{prefijo}{numero}"
        if telefono not in conjunto_telefonos:
            conjunto_telefonos.add(telefono)
            return telefono

def generar_datos_empresa(num_empresas):
   nombres_empresas = obtener_nombres_empresas()
   nombres_calles = obtener_nombres_calles()
   with open('dataRandom/empresas.dat', 'w') as data: 
    for i in range(num_empresas):
        nombre = nombres_empresas[i]
        direccion = random.choice(nombres_calles)
        Provincia = obtener_provincia_aleatoria()
        CIF =  generar_cif(cifs_generados, Provincia)
        email = str(i) + generar_email_aleatorio()
        telefono = generar_telefono_aleatorio(conjunto_telefonos)
        data.write(f"{CIF};{nombre};{direccion};{Provincia};{email};{telefono}\n")

##########################################################################################

# GENERADOR DNI
def generar_dni(dnis_generados):
    while True:
        numeros = ''.join(random.choices('0123456789', k=8))
        letra = 'TRWAGMYFPDXBNJZSQVHLCKE'[int(numeros) % 23]
        dni = numeros + letra
        if dni not in dnis_generados:
            dnis_generados.add(dni)
            return dni
        

# GENERAR NOMBRES         
def generar_nombre():
    nombres = [
        "Antonio", "María", "Manuel", "Jose", "Ana", "Francisco", "Isabel", "Luis", "Carmen", "Javier",
        "Pilar", "David", "Laura", "Pedro", "Marta", "Juan", "Sara", "Miguel", "Elena", "Carlos",
        "Raquel", "Josefa", "Ángel", "Sonia", "Fernando", "Nuria", "Diego", "Eva", "Jorge", "Beatriz",
        "Adrián", "Cristina", "Rubén", "Patricia", "Rafael", "Silvia", "Daniel", "Monica", "Alejandro", "Teresa",
        "Jordi", "Noelia", "Álvaro", "Natalia", "Roberto", "Lorena", "Ángela", "Rosa", "Sergio", "Lucía",
        "Jesús", "Marina", "Víctor", "Julia", "Alberto", "Inés", "Raul", "Miriam", "Fernando", "Esther",
        "Ivan", "Olga", "Óscar", "Celia", "Guillermo", "Gemma", "Joaquín", "Paula", "Alfonso", "Irene",
        "Emilio", "Nerea", "Jordi", "Alicia", "Roberto", "Elsa", "José Manuel", "Adela", "Álex", "Clara",
        "Felipe", "Sofía", "Vicente", "Marisol", "Nicolás", "Cristina", "Ignacio", "Verónica", "Ramón", "Estefanía",
        "Xavier", "Celia", "Pablo", "Elisa", "Víctor Manuel", "Judith", "Luis Miguel", "Lucía", "Juan José", "Mónica"
        # Puedes agregar más nombres según sea necesario
    ]
    apellidos = [
        "García", "Fernández", "González", "Rodríguez", "López", "Martínez", "Sánchez", "Pérez", "Martín", "Gómez",
        "Ruiz", "Hernández", "Díaz", "Moreno", "Álvarez", "Romero", "Alonso", "Gutiérrez", "Navarro", "Torres",
        "Domínguez", "Vázquez", "Ramos", "Gil", "Ramírez", "Serrano", "Blanco", "Suárez", "Molina", "Morales"
        # Puedes agregar más apellidos según sea necesario
    ]
    nombre = random.choice(nombres)
    apellido = random.choice(apellidos)  
    # Devolvemos el nombre completo
    return f"{nombre} {apellido}"

def generar_fecha_contrato_aleatoria():
    # Seleccionar un año aleatorio entre 1980 y 2020
    año = random.randint(1980, 2020)
    # Seleccionar un mes y un día aleatorio dentro del año seleccionado
    mes = random.randint(1, 12)
     # Si el mes es febrero (2), generamos el día aleatoriamente entre 1 y 28
    if mes == 2:
        dia = random.randint(1, 28)
    # Si el mes tiene 30 días, generamos el día aleatoriamente entre 1 y 30
    elif mes in [4, 6, 9, 11]:
        dia = random.randint(1, 30)
    # Si el mes tiene 31 días, generamos el día aleatoriamente entre 1 y 31
    else:
        dia = random.randint(1, 31)    
    # Devolver la fecha de contrato generada
    return datetime(año, mes, dia)

def generar_sueldo_aleatorio():
    return random.randrange(20000, 30000)


def seleccionar_cif_aleatorio(cifs_generados):
    # Verifica si hay CIFs en el conjunto
    if cifs_generados:
        # Elige un CIF aleatorio del conjunto y lo devuelve
        return random.choice(list(cifs_generados))
    else:
        # Devuelve None si el conjunto está vacío
        return None
    
def generar_datos_conductores(num_conductores):
   with open('dataRandom/conductores.dat', 'w') as data: 
    for i in range(num_conductores):
        DNI =  generar_dni(dnis_generados)
        nombre = generar_nombre()
        fechaContrato= generar_fecha_contrato_aleatoria().strftime('%Y-%m-%d')
        telefono= generar_telefono_aleatorio(conjunto_telefonos)
        salario = generar_sueldo_aleatorio()
        CIF_empresa = seleccionar_cif_aleatorio(cifs_generados)
        data.write(f"{DNI};{nombre};{fechaContrato};{telefono};{salario};{CIF_empresa}\n")

##########################################################################################



def generar_datos_clientes(num_clientes):
    nombres_calles = obtener_nombres_calles()
    with open('dataRandom/clientes.dat', 'w') as data: 
        for i in range(num_clientes):
            id_cliente  = i
            clientes_id_generados.add(id_cliente)
            nombre = generar_nombre()
            direccion = random.choice(nombres_calles)
            provincia = obtener_provincia_aleatoria()
            email = str(i) +  str(id_cliente) + generar_email_aleatorio() 
            telefono = generar_telefono_aleatorio(conjunto_telefonos)
            data.write(f"{id_cliente};{nombre};{direccion};{provincia};{email};{telefono}\n")

##########################################################################################
def generar_matricula(matriculas_generadas):
    while True:
        matricula = ''.join(random.choices(string.ascii_uppercase, k=3)) + \
                    ''.join(random.choices(string.digits, k=4))
        if matricula not in matriculas_generadas:
            matriculas_generadas.add(matricula)
            return matricula

def marca_modelo_aleatorio():
    marcas_modelos = {
        'Toyota': ['Corolla', 'Camry', 'RAV4', 'Prius', 'Highlander'],
        'Honda': ['Civic', 'Accord', 'CR-V', 'Pilot', 'Odyssey'],
        'Ford': ['F-150', 'Escape', 'Explorer', 'Focus', 'Mustang'],
        'Chevrolet': ['Silverado', 'Equinox', 'Tahoe', 'Malibu', 'Traverse'],
        'Volkswagen': ['Jetta', 'Passat', 'Tiguan', 'Atlas', 'Golf'],
        # Agrega más marcas y modelos según sea necesario
    }
    marca = random.choice(list(marcas_modelos.keys()))
    modelo = random.choice(marcas_modelos[marca])
    return marca, modelo

def generar_kilometros_aleatorios():
    return random.randint(50000, 100000)

def generar_año_matriculacion_aleatorio():
    # Seleccionar un año aleatorio entre 2000 y 2020
    año = random.randint(2000, 2020)
    # Seleccionar un mes y un día aleatorio dentro del año seleccionado
    mes = random.randint(1, 12)
     # Si el mes es febrero (2), generamos el día aleatoriamente entre 1 y 28
    if mes == 2:
        dia = random.randint(1, 28)
    # Si el mes tiene 30 días, generamos el día aleatoriamente entre 1 y 30
    elif mes in [4, 6, 9, 11]:
        dia = random.randint(1, 30)
    # Si el mes tiene 31 días, generamos el día aleatoriamente entre 1 y 31
    else:
        dia = random.randint(1, 31)    
    # Devolver la fecha de contrato generada
    return datetime(año, mes, dia)


def seleccionar_dni_aleatorio(dnis_generados):
    # Verifica si hay CIFs en el conjunto
    if dnis_generados:
        # Elige un CIF aleatorio del conjunto y lo devuelve
        return random.choice(list(dnis_generados))
    else:
        # Devuelve None si el conjunto está vacío
        return None


def generar_datos_vehiculos(num_vehiculos):
    with open('dataRandom/vehiculos.dat', 'w') as data: 
        for i in range(num_vehiculos):
            matricula  = generar_matricula(matriculas_generadas)
            marca, modelo = marca_modelo_aleatorio()
            kilometros = generar_kilometros_aleatorios()
            fecha_matricula = generar_año_matriculacion_aleatorio().strftime('%Y-%m-%d')
            DNI_conductores = seleccionar_dni_aleatorio(dnis_generados)
            data.write(f"{matricula};{marca};{modelo};{kilometros};{fecha_matricula};{DNI_conductores}\n")           

##########################################################################################

def generar_peso_aleatorio():
    # Generar un peso aleatorio entre 100 gramos y 10000 kilogramos
    peso = random.randrange(1, 10000)
    return peso

def generar_fecha_salida_aleatoria():
    # Seleccionar un día aleatorio dentro del año 2023
    fecha_salida = datetime(2023, random.randint(1, 12), random.randint(1, 28))
    return fecha_salida

def generar_fecha_llegada(fecha_salida):
    # Generar un número aleatorio de días entre 1 y 10
    dias = random.randint(1, 10)
    # Calcular la fecha de llegada sumándole el número de días aleatorios a la fecha de salida
    fecha_llegada = fecha_salida + timedelta(days=dias)
    return fecha_llegada


def seleccionar_matricula_aleatorio(matriculas_generadas):
    # Verifica si hay CIFs en el conjunto
    if matriculas_generadas:
        # Elige un CIF aleatorio del conjunto y lo devuelve
        return random.choice(list(matriculas_generadas))
    else:
        # Devuelve None si el conjunto está vacío
        return None
    
def seleccionar_id_cliente_aleatorio(clientes_id_generados):
    # Verifica si hay CIFs en el conjunto
    if clientes_id_generados:
        # Elige un CIF aleatorio del conjunto y lo devuelve
        return random.choice(list(clientes_id_generados))
    else:
        # Devuelve None si el conjunto está vacío
        return None

#fechaContrato= generar_fecha_contrato_aleatoria().strftime('%Y-%m-%d')


def generar_datos_bultos(num_bultos):
    nombres_calles = obtener_nombres_calles()
    listaClientes=list(clientes_id_generados)
    listaMatriculas=list(matriculas_generadas)
    with open('dataRandom/bultos.dat', 'w') as data: 
        for i in range(num_bultos):
            id_bulto  = i
            direccion_origen =  str(random.randint(1, 200)) + random.choice(nombres_calles)
            direccion_destino = str(random.randint(1, 200))  + random.choice(nombres_calles)
            provincia_origen = obtener_provincia_aleatoria()
            provincia_destino = obtener_provincia_aleatoria()
            peso = generar_peso_aleatorio()
            fecha_salida = generar_fecha_salida_aleatoria()
            fecha_llegada = generar_fecha_llegada(fecha_salida)
            fecha_salida = fecha_salida.strftime('%Y-%m-%d')
            fecha_llegada = fecha_llegada.strftime('%Y-%m-%d')
            matricula_vehiculos = random.choice(listaMatriculas)
            id_cliente_clientes = random.choice(listaClientes)
            data.write(f"{id_bulto};{direccion_origen};{direccion_destino};{provincia_origen};{provincia_destino};{peso};{fecha_salida};{fecha_llegada};{matricula_vehiculos};{id_cliente_clientes}\n")            

##########################################################################################
matriculas_generadas = set()
dnis_generados = set()
cifs_generados = set()
clientes_id_generados = set()
conjunto_telefonos = set()

generar_datos_empresa(10000)
generar_datos_conductores(200000)
generar_datos_clientes(2000000)
generar_datos_vehiculos(1000000)
generar_datos_bultos(20000000)
```




```
python3 generateRandomDat.py
```

```
sftp> ls
bultos.dat            clientes.dat          conductores.dat
empresas.dat          vehiculos.dat
sftp> put *
```

```
felix@postgresql01:~/pl2/dbLogistica/data$ pwd
/home/felix/pl2/dbLogistica/data
felix@postgresql01:~/pl2/dbLogistica/data$ cp * /tmp/
```

----------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------


Cuestión 8: Realizar la carga masiva de los datos generados en la cuestión 7 en la base
de datos Logística. Indicar el proceso seguido y el orden de carga de las tablas,
explicando el porqué de dicho orden; y asegurando la consistencia e integridad de los
datos cargados. Comparar los tiempos en las tablas implicadas y explicar a qué es
debida la diferencia. ¿Existe diferencia entre los tiempos que ha obtenido y los que
aparecen en el LOG de operaciones de postgreSQL? ¿Por qué?



EJEMPLOS de insercción single row:

```
EMPRESA OK:
INSERT INTO public.empresas ("CIF", nombre, direccion, "Provincia", email, telefono)
VALUES ('123456789', 'Empresa Ejemplo', 'Calle Ejemplo 123', 'Ejemplo', 'ejemplo@empresa.com', 123456789);

CONDUCTOR OK: DEBE EXISTIR EL CIF EN EMPRESA:
INSERT INTO public.conductores ("DNI", nombre, fecha_contrato, telefono, salario, "CIF_empresas")
VALUES ('123456789', 'Juan Perez', '2024-03-17', 123456789, 1500.00, '123456789');


CLIENTES OK:
INSERT INTO public.clientes (id_cliente, nombre, direccion, provincia, email, telefono)
VALUES (1, 'Cliente Ejemplo', 'Calle Ejemplo 123', 'Ejemplo', 'cliente@example.com', 123456789);


VEHICULOS: DNI CONDUCTOR 
INSERT INTO public.vehiculos (matricula, marca, modelo, kilometros, fecha_matricula, "DNI_conductores")
VALUES ('ABC1234', 'Marca Ejemplo', 'Modelo Ejemplo', 10000, '2022-01-01', '123456789');

BULTOS: ID DE CLIENTES, MATRICULA DE VEHICULOS
INSERT INTO public.bultos (id_bulto, direccion_origen, direccion_destino, provincia_origen, provincia_destino, peso, fecha_salida, fecha_llegada, matricula_vehiculos, id_cliente_clientes)
VALUES (1, 'Calle Origen 123', 'Calle Destino 456', 'Provincia Origen', 'Provincia Destino', 10.5, '2024-03-17', '2024-03-18', 'ABC1231', 1);
```

```
\copy empresas("CIF", nombre, direccion, "Provincia", email, telefono) FROM '/tmp/empresas.dat' DELIMITER ';' CSV
\copy conductores("DNI", nombre, fecha_contrato, telefono, salario, "CIF_empresas") FROM '/tmp/conductores.dat' DELIMITER ';' CSV
\copy clientes(id_cliente, nombre, direccion, provincia, email, telefono) FROM '/tmp/clientes.dat' DELIMITER ';' CSV
\copy vehiculos(matricula, marca, modelo, kilometros, fecha_matricula, "DNI_conductores") FROM '/tmp/vehiculos.dat' DELIMITER ';' CSV
\copy bultos(id_bulto, direccion_origen, direccion_destino, provincia_origen, provincia_destino, peso, fecha_salida, fecha_llegada, matricula_vehiculos, id_cliente_clientes) FROM '/tmp/bultos.dat' DELIMITER ';' CSV
```


Volcado de datos:
```
\copy empresas("CIF", nombre, direccion, "Provincia", email, telefono) FROM '/tmp/empresas.dat' DELIMITER ';' CSV
COPY 10000
Time: 74.102 ms
```

```
select count(*) from  empresas;
 count 
-------
 10000
(1 row)
```

```
\copy conductores("DNI", nombre, fecha_contrato, telefono, salario, "CIF_empresas") FROM '/tmp/conductores.dat' DELIMITER ';' CSV
COPY 200000
Time: 2250.494 ms (00:02.250)
```

```
select count(*) from  conductores;
 count  
--------
 200000
```


```
\copy clientes(id_cliente, nombre, direccion, provincia, email, telefono) FROM '/tmp/clientes.dat' DELIMITER ';' CSV
COPY 2000000
Time: 12409.685 ms (00:12.410)
```

```
select count(*) from  clientes;
  count  
---------
 2000000
(1 row)
```


```
\copy vehiculos(matricula, marca, modelo, kilometros, fecha_matricula, "DNI_conductores") FROM '/tmp/vehiculos.dat' DELIMITER ';' CSV
COPY 1000000
Time: 15919.455 ms (00:15.919)
```

```
select count(*) from  vehiculos;
  count  
---------
 1000000
(1 row)
```


```
 \copy bultos(id_bulto, direccion_origen, direccion_destino, provincia_origen, provincia_destino, peso, fecha_salida, fecha_llegada, matricula_vehiculos, id_cliente_clientes) FROM '/tmp/bultos.dat' DELIMITER ';' CSV
COPY 20000000
Time: 612474.243 ms (10:12.474)
```

```
select count(*) from  bultos;
  count   
----------
 20000000
(1 row)
```

LOGS DE COPY:

```
 UTC [2092]LOG:  statement: COPY  empresas ( "CIF" , nombre, direccion, "Provincia" , email, telefono ) FROM STDIN DELIMITER ';' CSV
[DNI: XXXX & XXXX] [host: [local]] 2024-03-18 23:50:50.530 UTC [2092]LOG:  statement: COPY  conductores ( "DNI" , nombre, fecha_contrato, telefono, salario, "CIF_empresas" ) FROM STDIN DELIMITER ';' CSV
[DNI: XXXX & XXXX] [host: [local]] 2024-03-18 23:51:08.328 UTC [2092]LOG:  statement: COPY  clientes ( id_cliente, nombre, direccion, provincia, email, telefono ) FROM STDIN DELIMITER ';' CSV
[DNI: XXXX & XXXX] [host: ] 2024-03-18 23:51:19.537 UTC [773]LOG:  checkpoint starting: wal
[DNI: XXXX & XXXX] [host: [local]] 2024-03-18 23:51:42.334 UTC [2092]LOG:  statement: COPY  vehiculos ( matricula, marca, modelo, kilometros, fecha_matricula, "DNI_conductores" ) FROM STDIN DELIMITER ';' CSV
```

LOGS de COPY LLENADO DE VM:

```
PANIC:  could not write to file "pg_wal/xlogtemp.2092": No space left on device
```

Segunda copia de tabla bultos:

```
[DNI: XXXX & XXXX] [host: [local]] 2024-03-18 23:57:46.309 UTC [14804]LOG:  statement: COPY  bultos ( id_bulto, direccion_origen, direccion_destino, provincia_origen, provincia_destino, peso, fecha_salida, fecha_llegada, matricula_vehiculos, id_cliente_clientes ) FROM STDIN DELIMITER ';' CSV
[DNI: XXXX & XXXX] [host: ] 2024-03-18 23:57:50.415 UTC [14776]LOG:  checkpoint complete: wrote 4245 buffers (25.9%); 0 WAL file(s) added, 0 removed, 33 recycled; write=95.488 s, sync=0.266 s, total=96.291 s; sync files=15, longest=0.116 s, average=0.018 s; distance=540945 kB, estimate=900893 kB; lsn=43/67729820, redo lsn=43/49044D28
```