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
