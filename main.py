from clases import (TareaRecurrente, TareaSimple, Gestion)
from datetime import(date, timedelta)
import os
import platform


def limpiar_pantalla():
    print(platform.system())
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')


def menu_para_mostrar():
    print("1. Tareas del dia")
    print("2. Tareas de la semana")
    print("3. Tareas del mes")
    print("4. Todas las tareas")
    return input("Elija una opcion(1-4): ").strip()


def menu_actualizacion(tarea):
    print("========( Actualizacion )==========")
    print("1. Titulo - 2. Descripcion - 3. Fecha de vencimiento - 4. Estado", end="")
    if tarea.get('importancia'):
        print(" - 5. Importancia")
    else: 
        print(" - 5. Recurrencia") 
    return input("Elija una opción (1-5): ").strip()


def cambiar_tarea(archivo, tarea, atributo):

    try:
        nuevo_atributo = input(f"Escriba el nuevo valor de '{atributo}': ").strip()
        if atributo == 'titulo':
            if nuevo_atributo == "":
                raise Exception("El titulo no puede estar vacio")
            elif len(nuevo_atributo) > 30:
                raise Exception("El titulo es muy largo")
            else:
                archivo.actualizar_tarea(atributo, nuevo_atributo, tarea)
        elif atributo == 'descripcion':
            if len(nuevo_atributo) > 255:
                raise Exception("La descripción es muy larga")
            else:
                archivo.actualizar_tarea(atributo, nuevo_atributo, tarea)
        elif atributo == 'f_vencimiento':
            if nuevo_atributo == "":
                raise Exception("La fecha de vencimiento no puede estar vacio")
            else:
                nuevo_atributo = date.fromisoformat(nuevo_atributo)
                if nuevo_atributo < date.today():
                    raise Exception("La fecha no es válida. Debe ser mayor a la fecha actual")
                else:
                    archivo.actualizar_tarea(atributo, nuevo_atributo, tarea)
        elif atributo == 'estado':
            if nuevo_atributo == "":
                raise Exception("El estado no puede estar vacio")
            elif nuevo_atributo not in ["pendiente", "en progreso", "completada"]:
                raise Exception("Valor inválido de estado.")
            else:
                archivo.actualizar_tarea(atributo, nuevo_atributo, tarea)
        elif atributo == 'recurrencia':
            if int(nuevo_atributo) <= 0:
                raise Exception("La recurrencia no puede ser un número negativo o cero.")
            else:
                archivo.actualizar_tarea(atributo, nuevo_atributo, tarea)
        elif atributo == 'importancia':
            if nuevo_atributo == "":
                raise Exception("La importancia no puede estar vacia")
            elif nuevo_atributo not in ["alta", "media", "baja"]:
                raise Exception("Valor inválido de importancia")
            else:
                archivo.actualizar_tarea(atributo, nuevo_atributo, tarea)
    except ValueError:
        print("El formato de fecha no es correcto.")
    except Exception as e:
        print(f"{e}")


def menu():
    print("========( Bienvenidx )=========")
    print("1. Crear una tarea simple")
    print("2. Crear una tarea recurrente")
    print("3. Leer una tarea")
    print("4. Actualizar una tarea")
    print("5. Eliminar una tarea")
    print("6. Ver todas las tareas")
    print("7. Salir")
    print("===========================")


def crear_tarea(archivo, tipo_tarea):
    try:
        print("===========================")
        print("Creando una tarea...")
        titulo = input("Titulo: ").strip()
        descripcion = input("Descripcion: ").strip()
        f_vencimiento = input("Fecha de vencimiento(AAAA-MM-DD): ").strip()
        estado = input("Estado(pendiente, en progreso, completada): ").strip()

        if tipo_tarea == '1':
            importancia = input("Importancia(baja, media, alta): ").strip()
            tarea = TareaSimple(titulo, descripcion, f_vencimiento, estado, importancia) 
        else:
            recurrencia = input("Recurrencia en dias: ").strip()
            tarea = TareaRecurrente(titulo, descripcion, f_vencimiento, estado, recurrencia)

        archivo.crear_tarea(tarea)
    except Exception as e:
        print(f"{e}")
        
    print("===========================")
    input("Presiona enter para continuar...") 


def actualizar_tarea(archivo):
    try:
        tarea = archivo.leer_una_tarea(input("Escriba el titulo de la tarea a actualizar: ").strip())
        opt = menu_actualizacion(tarea)

        if opt == '1':
            cambiar_tarea(archivo, tarea, 'titulo')
        elif opt == '2':
            cambiar_tarea(archivo, tarea, 'descripcion')
        elif opt == '3':
            cambiar_tarea(archivo, tarea, 'f_vencimiento')
        elif opt == '4':
            cambiar_tarea(archivo, tarea, 'estado')
        elif opt == '5':
            if tarea.get("importancia"):
                cambiar_tarea(archivo, tarea, 'importancia')
            else:
                cambiar_tarea(archivo, tarea, 'recurrencia')
        else:
            print("Opcion inválida.")
    except Exception as e:
        print(f"{e}")

    input("Presiona enter para continuar...") 


def leer_una_tarea(archivo):
    titulo = input("Escriba un titulo: ").strip()
    tarea = archivo.leer_una_tarea(titulo)

    if tarea:
        print("===========================")
        print(f"Tarea: {tarea['titulo']}")
        print(f"Descripcion: {tarea['descripcion']}")
        print(f"Fecha vencimiento: {tarea['f_vencimiento']}")
        print(f"Estado: {tarea['estado']}")
        if tarea.get('importancia'):
            print(f"Importancia: {tarea['importancia']}")
        else:
            print(f"Recurrencia: {tarea['recurrencia']}")
        print("===========================")
        
    else:
        print(f"No se encontró ninguna tarea con el titulo '{titulo}'")

    input("Presiona enter para continuar...") 


def eliminar_tarea(archivo):
    print("===========================")

    titulo = input("Escriba el titulo de la tarea: ")
    archivo.eliminar_tarea(titulo)

    print("===========================")
    input("Presiona enter para continuar...") 

#
def mostrar_tareas(archivo):
    opt = menu_para_mostrar()
    if opt == '4':
        datos = archivo.leer_datos() # va a tirar error
    else:
        datos = archivo.leer_segun_fecha(opt)
    cont = 1

    print("=======( Mostrando tareas )======")
    print("Tarea | Fecha de vencimiento | Estado | Importancia/Recurrencia")
    for tarea in datos:
        if tarea.get('importancia'):
            print(f"-------------({cont})-----------------")
            print(f"{tarea['titulo']} | {tarea['f_vencimiento']} | {tarea['estado']} | {tarea['importancia']}")
            cont += 1
        else:
            if opt == '1': days = 1
            elif opt == '2': days = 7
            elif opt == '3': days = 30
            else: 
                days = date.fromisoformat(tarea['f_vencimiento']) - date.today()
                days = days.days

            f_vencimiento = date.fromisoformat(tarea['f_vencimiento'])
            f_limite = date.today() + timedelta(days=days)
            cont_int = 1

            while (f_vencimiento <= f_limite) and (cont_int != 5):
                print(f"-------------({cont})-------------")
                print(f"{tarea['titulo']} | {f_vencimiento} | {tarea['estado']} | {tarea['recurrencia']}")
                cont += 1
                cont_int += 1
                f_vencimiento += timedelta(days=int(tarea['recurrencia']))
    
    print("=============================")
    input("Presiona enter para continuar...") 


if __name__ == '__main__':
    gestion = Gestion()

    while True:
        limpiar_pantalla()
        menu()
        opcion = input("Elija una opcion: ").strip()

        if opcion == '1' or opcion == '2':
            crear_tarea(gestion, opcion)
        elif opcion == '3':
            leer_una_tarea(gestion)
        elif opcion == '4':
            actualizar_tarea(gestion)
        elif opcion == '5': 
            eliminar_tarea(gestion)
        elif opcion == '6':
            mostrar_tareas(gestion)
        elif opcion == '7':
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida. Por favor elija una opción válida.")

