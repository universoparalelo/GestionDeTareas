'''
Desafío 3: Sistema de Gestión de Tareas
Objetivo: Desarrollar un sistema para organizar y administrar tareas personales o de equipo.

Requisitos:

Crear una clase base Tarea con atributos como descripción, fecha de vencimiento, estado (pendiente, en progreso, completada), etc.
Definir al menos 2 clases derivadas para diferentes tipos de tareas (por ejemplo, TareaSimple, TareaRecurrente) con atributos y métodos específicos.
Implementar operaciones CRUD para gestionar las tareas.
Manejar errores con bloques try-except para validar entradas y gestionar excepciones.
Persistir los datos en archivo JSON.
##############################'''

import mysql.connector
import json
from mysql.connector import Error
from decouple import config
from datetime import (date, timedelta)

config.encoding = 'cp1251'

class Tarea:
    def __init__(self, titulo, descripcion, f_vencimiento, estado):
        self.__titulo = self.validarTitulo(titulo)
        self.__descripcion = self.validardescripcion(descripcion)
        self.__f_vencimiento = self.validarf_vencimiento(f_vencimiento)
        self.__estado = self.validarEstado(estado)
    
    @property
    def titulo(self):
        return self.__titulo

    @property
    def descripcion(self):
        return self.__descripcion
    
    @property
    def f_vencimiento(self):
        return self.__f_vencimiento
    
    @property
    def estado(self):
        return self.__estado
    
    @titulo.setter
    def titulo(self, nuevoTitulo):
        self.__titulo = self.validarTitulo(nuevoTitulo)
    
    def validarTitulo(self, nuevoTitulo):
        try:
            if len(nuevoTitulo) > 30:
                raise Exception("El titulo es muy largo.")
            elif len(nuevoTitulo) == 0:
                raise Exception("El titulo no puede estar vacio")
            else:
                return nuevoTitulo
        except Exception as e:
            raise Exception(f"{e}")
        

    @descripcion.setter
    def descripcion(self, nuevaDescripcion):
        self.__descripcion = self.validardescripcion(nuevaDescripcion)
    
    def validardescripcion(self, nuevaDescripcion):
        try:
            if len(nuevaDescripcion) > 255:
                raise Exception('La descripcion es muy larga.')
            else:
                return nuevaDescripcion
        except Exception as e:
            raise Exception(f"{e}")
            

    @f_vencimiento.setter
    def f_vencimiento(self, nuevaF_vencimiento):
        self.__f_vencimiento = self.validarf_vencimiento(nuevaF_vencimiento)
    
    def validarf_vencimiento(self, nuevaF_vencimiento):
        try:
            if nuevaF_vencimiento == "":
                raise Exception("La tarea debe tener una fecha de vencimiento")
            else:
                nuevaF_vencimiento = date.fromisoformat(nuevaF_vencimiento)
                if nuevaF_vencimiento < date.today():
                    raise Exception("La fecha no es válida. Debe ser mayor a la fecha actual")
                else:
                    return str(nuevaF_vencimiento)
        except ValueError as e:
            raise Exception(f'El formato de fecha es incorrecto. {e}')
        except Exception as e:
            raise Exception(f"{e}")     
            
    @estado.setter
    def estado(self, nuevoEstado):
        self.__estado = self.validarEstado(nuevoEstado)

    def validarEstado(self, nuevoEstado):
        try:
            if nuevoEstado not in ['pendiente', 'en progreso', 'completada']:
                raise Exception("El estado no se corresponde con ninguna de las opciones válidas.")
            else:
                return nuevoEstado
        except Exception as e: 
            raise Exception(f"{e}")

    def to_dict(self):
        return {
            "titulo": self.titulo,
            "descripcion": self.descripcion,
            "f_vencimiento": self.f_vencimiento,
            "estado": self.estado,
        }


class TareaRecurrente(Tarea):
    def __init__(self, titulo, descripcion, f_vencimiento, estado, recurrencia):
        super().__init__(titulo, descripcion, f_vencimiento, estado)
        self.__recurrencia = self.validarRecurrencia(recurrencia)

    @property
    def recurrencia(self):
        return self.__recurrencia

    @recurrencia.setter
    def recurrencia(self, nuevoRecurrencia):
        self.__recurrencia = self.validarRecurrencia(nuevoRecurrencia)

    def validarRecurrencia(self, nuevoRecurrencia):
        try: 
            if nuevoRecurrencia == '':
                raise Exception("El atributo recurrencia no puede estar vacio.")
            elif int(nuevoRecurrencia) <= 0:
                raise Exception("La recurrencia no puede ser un número negativo.")
            else: 
                return int(nuevoRecurrencia)
        except Exception as e:
            raise Exception(f"{e}")

    def to_dict(self):
        datos = super().to_dict()
        datos['recurrencia'] = self.recurrencia
        return datos


class TareaSimple(Tarea):
    def __init__(self, titulo, descripcion, f_vencimiento, estado, importancia):
        super().__init__(titulo, descripcion, f_vencimiento, estado)
        self.__importancia = self.validarimportancia(importancia)

    @property
    def importancia(self):
        return self.__importancia
    
    @importancia.setter
    def importancia(self, nuevaImportancia):
        self.__importancia = self.validarimportancia(nuevaImportancia)

    def validarimportancia(self, nuevaImportancia):
        try:
            if nuevaImportancia not in ['baja', 'media', 'alta']:
                raise Exception("La importancia no se corresponde con ninguna de las opciones válidas.")
            else:
                return nuevaImportancia
        except Exception as e:
            raise Exception(f"{e}")


    def to_dict(self):
        datos = super().to_dict()
        datos['importancia'] = self.importancia
        return datos


class Gestion():
    def __init__(self):
        self.host = config('DB_HOST')
        self.name = config('DB_NAME')
        self.user = config('DB_USER')
        self.password = config('DB_PASSWORD')
        self.port = config('DB_PORT')


    def connect(self):
        try:
            connection = mysql.connector.connect(
                user=self.user, password=self.password, host=self.host,
                                   database=self.name, port=self.port
            )
            if connection.is_connected():
                return connection
            
        except Error as e:
            print(f"Ocurrio un error en la conexion: {e}")

    def leer_datos(self):
        try:
            connection = self.connect()
            if connection:
                with connection.cursor(dictionary=True) as cursor:
                    cursor.execute('''
                        select * from tarea natural join tareasimple union
                        select * from tarea natural join tarearecurrente''')
                    tareas = cursor.fetchall()

                    return tareas
            
        except Error as e:
            raise Exception(f"Ocurrió un error en la eliminacion: {e}")
        
        finally:
            if connection.is_connected():
                connection.close()

    def crear_tarea(self, tarea):
        try:
            connection = self.connect()
            if connection:
                with connection.cursor() as cursor:
                    cursor.execute('select titulo from tarea where titulo = %s', (tarea.titulo,))
                    if cursor.fetchone():
                        print("Ya existe una tarea con el mismo titulo")
                        return
                    
                    query = '''
                    insert into tarea (titulo, descripcion, f_vencimiento, estado) values (%s, %s, %s, %s)
                    '''
                    cursor.execute(query, (tarea.titulo, tarea.descripcion, tarea.f_vencimiento, tarea.estado))

                    if isinstance(tarea, TareaSimple):

                        query = '''
                        insert into tareasimple (titulo, importancia) values (%s, %s)
                        '''
                        cursor.execute(query, (tarea.titulo, tarea.importancia))
                    elif isinstance(tarea, TareaRecurrente):
                        query = '''
                        insert into tarearecurrente (titulo, recurrencia) values (%s, %s)
                        '''
                        cursor.execute(query, (tarea.titulo, tarea.recurrencia))
                    
                    connection.commit()
                    print(f"La tarea '{tarea.titulo}' se creó correctamente.")

        except Exception as e:
            raise Exception(f"{e}.")

        finally:
            if connection.is_connected:
                connection.close()        

    def leer_una_tarea(self, titulo):
        try:
            connection = self.connect()
            if connection:
                with connection.cursor(dictionary=True) as cursor:
                    cursor.execute('''
                    select * from tarea t natural join tareasimple ts
                    where titulo=%s;
                    ''', (titulo,))
                    tarea = cursor.fetchone()
                    if tarea:
                        return tarea
                    else:
                        cursor.execute('''
                        select * from tarea t natural join tarearecurrente ts
                        where titulo=%s;
                        ''', (titulo,)) 
                        tarea = cursor.fetchone()
                    
                    return tarea


        except Error as e:
            raise Exception(f"Surgió un error en la lectura: {e}")
        
        finally:
            if connection.is_connected:
                connection.close()

    def actualizar_tarea(self, atributo, nuevo_valor, tarea):
        try:
            connection = self.connect()
            if connection.is_connected():
                with connection.cursor() as cursor:

                    if atributo == 'importancia':
                        cursor.execute('''
                            UPDATE tareasimple SET importancia = %s
                            WHERE titulo = %s
                        ''', (nuevo_valor, tarea['titulo']))
                        verificacion = cursor.rowcount
                    elif atributo == 'recurrencia':
                        cursor.execute('''
                        UPDATE tarearecurrente SET recurrencia = %s
                        WHERE titulo = %s
                        ''', (nuevo_valor, tarea['titulo']))
                        verificacion = cursor.rowcount
                    else:
                        sql = f"UPDATE tarea SET {atributo} = %s WHERE titulo = %s"
                        cursor.execute(sql, (nuevo_valor, tarea['titulo']))
                        verificacion = cursor.rowcount


                    connection.commit()

                    if verificacion == 0:
                        print("No se encontró la tarea")
                    else:
                        print(f"Tarea '{tarea['titulo']}' actualizada correctamente")

        except Error as e:
            raise Exception(f"Ocurrió un error en la actualización: {e}")
        
        finally:
            if connection.is_connected():
                connection.close()

    def eliminar_tarea(self, tarea):
        try:
            connection = self.connect()
            if connection:
                with connection.cursor() as cursor:
                    cursor.execute('''select * from tarea where titulo=%s''', (tarea,))
                    if cursor.fetchone():
                        cursor.execute('''delete from tarea where titulo=%s''', (tarea,))
                        if cursor.rowcount == 1:
                            connection.commit()
                            print(f"Tarea '{tarea}' eliminada correctamente")
                    else:
                        print(f"No se encontro la tarea '{tarea}'")
            
        except Error as e:
            raise Exception(f"Ocurrió un error en la eliminacion: {e}")
        
        finally:
            if connection.is_connected():
                connection.close()

    def leer_segun_fecha(self, f_limite):
        try:
            connection = self.connect()
            if connection:
                with connection.cursor(dictionary=True) as cursor:
                    if f_limite == '1':
                        days = 0
                    elif f_limite == '2':
                        days = 7
                    elif f_limite == '3':
                        days = 30
                    else:
                        print("Opción inválida.")

                    cursor.execute('''
                    select * from tarea natural join tareasimple
                    where f_vencimiento >= DATE(NOW()) 
	                    and f_vencimiento <= DATE_ADD( DATE(NOW()), INTERVAL %s DAY )
                                   union
                    select * from tarea natural join tarearecurrente 
                    where f_vencimiento >= DATE(NOW()) 
                        and f_vencimiento <= DATE_ADD( DATE(NOW()), INTERVAL %s DAY );
                    ''', (days,days))

                    datos = cursor.fetchall()
                    print(datos)
                    return datos
            
        except Error as e:
            raise Exception(f"{e}")
        
        finally:
            if connection.is_connected():
                connection.close()
