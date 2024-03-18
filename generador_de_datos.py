import random
import string
import csv

cif_generado = set()
direcciones_creadas = set()
emails_generados = set()

def obtener_nombres_empresas():
    nombres_empresas = []
    with open('companies.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            nombres_empresas.append(row[1])  # La segunda columna contiene los nombres de las empresas
    return nombres_empresas

def crear_direccion():
    calle = 'calle'
    numero = random.randint(1,5000000)
    return f"{calle} {numeros}"

def crear_email ():
    direccion_email = ''.join(random.choices(string.ascii_uppercase, k=10))
    gmail = '@hotmail.com'
    return f"{direccion_email}{gmail}"

def crear_cif():
    opciones = ['A','B']
    letras = random.choice(opciones)
    numeros =  ''.join(random.choice(string.digits, k=8))
    return f"{letras}{numeros}"

"""------------------------------------------------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------------------------------------------------"""

# Aquí estan los generadores de EMPRESAS y CONDUCTORES que tienes una PK y una FK
def generar_datos_empresas(num_empresas):
    nombres_empresas = obtener_nombres_empresas()
    nombres_provincias = gen_provincia()
    lista_provincias = [
    "Álava", "Albacete", "Alicante", "Almería", "Asturias", "Ávila", "Badajoz",
    "Barcelona", "Burgos", "Cáceres", "Cádiz", "Cantabria", "Castellón",
    "Ciudad Real", "Córdoba", "Cuenca", "Gerona", "Granada", "Guadalajara",
    "Guipúzcoa", "Huelva", "Huesca", "Islas Baleares", "Jaén", "La Coruña",
    "La Rioja", "Las Palmas", "León", "Lérida", "Lugo", "Madrid", "Málaga",
    "Murcia", "Navarra", "Orense", "Palencia", "Pontevedra", "Salamanca",
    "Santa Cruz de Tenerife", "Segovia", "Sevilla", "Soria", "Tarragona",
    "Teruel", "Toledo", "Valencia", "Valladolid", "Vizcaya", "Zamora", "Zaragoza"
    ]
    with open('empresas.dat', 'w') as data:
        for i in range(num_empresas):
            nombres_provincias = (nombres_provincias)
            nombre_empresa = (nombres_empresas)
            provincia = lista_provincias(random.randint(0,49))
            telefono = random.randint(100000000,999999999)

            cif = crear_cif()
            while cif in crear_cif:
                cif = crear_cif()
            cif_generado.add(cif)

            direccion = crear_direccion
            while direcciones in crear_direccion:
                direccion = crear_direccion
            direcciones_creadas.add(direccion)
            
            email = crear_email
            while email in crear_email:
                email = crear_email
            emails_generados.add(email)
            data.write(f"{cif};{nombre_empresa};{direccion};{provincia};{email};{telefono}\n")
            #data.write(f"{nombre_empresa} \n")


def generar_datos_conductores ():
    


"""-----------------------------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------------------------------"""

#Aquí estan los generadores de CLIENTES y BULTOS que tienen una PK y una FK



def generar_datos_clientes(num_clientes):
    lista_provincias = [
    "Álava", "Albacete", "Alicante", "Almería", "Asturias", "Ávila", "Badajoz",
    "Barcelona", "Burgos", "Cáceres", "Cádiz", "Cantabria", "Castellón",
    "Ciudad Real", "Córdoba", "Cuenca", "Gerona", "Granada", "Guadalajara",
    "Guipúzcoa", "Huelva", "Huesca", "Islas Baleares", "Jaén", "La Coruña",
    "La Rioja", "Las Palmas", "León", "Lérida", "Lugo", "Madrid", "Málaga",
    "Murcia", "Navarra", "Orense", "Palencia", "Pontevedra", "Salamanca",
    "Santa Cruz de Tenerife", "Segovia", "Sevilla", "Soria", "Tarragona",
    "Teruel", "Toledo", "Valencia", "Valladolid", "Vizcaya", "Zamora", "Zaragoza"
    ]
    nombres_predefinidos = [
    "Ana", "Carlos", "Elena", "Diego", "Isabel", "Luis", "María", "Pedro",
    "Sofía", "Tomás", "Valentina", "Xavier", "Yolanda", "Zara", "Alejandro", 
    "Beatriz", "Carmen", "David", "Fernanda", "Gabriel",
    "Helena", "Ignacio", "Julia", "Kevin", "Laura", "Manuel", "Natalia",
    "Óscar", "Paula", "Quim", "Raquel", "Santiago", "Teresa", "Ulises",
    "Violeta", "Walter", "Ximena", "Yago", "Zaida", "Adrián", "Bianca", "César", 
    "Daniela", "Emilio", "Florencia",
    "Gonzalo", "Hilda", "Iván", "Julieta", "Kai", "Lorena", "Mateo",
    "Nora", "Óscar", "Patricia", "Quirino", "Renata", "Sergio",
    "Tatiana", "Uriel", "Valeria", "Waldo", "Xenia", "Yasmin", "Zacarías","Alicia", 
    "Bruno", "Clara", "Dante", "Eva", "Felipe",
    "Gisela", "Hugo", "Inés", "Javier", "Karen", "Lorenzo",
    "Mónica", "Nicolás", "Olivia", "Pablo", "Quinta", "Rafael",
    "Sara", "Tobías", "Úrsula", "Víctor", "Wanda", "Xander",
    "Yara", "Zoe", "Aurora", "Brunilda", "Ciro", "Delfina", "Ezequiel", "Fabiola",
    "Gerardo", "Héctor", "Irene", "Jacinto", "Kassandra", "Leandro",
    "Margarita", "Néstor", "Ofelia", "Pascual", "Quintín", "Ramona",
    "Salvador", "Tatiana", "Ulrico", "Valentín", "Wendy", "Ximeno",
    "Yolanda", "Zafiro", "Zephyr", "Octavia", "Caspian", "Seraphina",
    "Thaddeus", "Isolde", "Lysander", "Persephone", "Caius", "Eulalia",
    "Balthazar", "Aurelia", "Cormac", "Melisande", "Leocadia",
    "Peregrine", "Euphemia", "Cassian", "Ottoline", "Ignatius"]
    with open('clientes.dat', 'w') as data:

        for i in range(num_clientes):
            id_cliente = i + 1
            nombre = random.choice(nombres_predefinidos)
            direccion = crear_direccion
            provincia = random.choice(lista_provincias)
            telefono = random.randint(100000000,999999999)
            while direcciones in crear_direccion:
                direccion = crear_direccion
            direcciones_creadas.add(direccion)
            email = crear_email
            while email in crear_email:
                email = crear_email
            emails_generados.add(email)
            data.write(f"{id_cliente};{nombre};{direccion};{provincia};{email};{telefono}\n")


#generar_datos_fichero(10)
generar_datos_empresas(10000)
generar_datos_clientes(2000000)

