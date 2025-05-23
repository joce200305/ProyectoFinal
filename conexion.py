import mysql.connector as db
import json
import bcrypt
import getpass
from typing import Optional, Union, List, Dict, Tuple

class ConexionBD:
    __config = {
        "user": "root",
        "password": "",
        "host": "localhost",
        "port": "3306",
        "database": "cinedb",
        "raise_on_warnings": True
    }

    @classmethod
    def conectar(cls) -> Optional[db.connection.MySQLConnection]:
        try:
            return db.connect(**cls.__config)
        except Exception as error:
            print(f"Error al conectar a la base de datos: {error}")
            return None

    @classmethod
    def ejecutar_consulta(cls, consulta: str, parametros=None, fetch=False):
        conexion = cls.conectar()
        if conexion:
            try:
                cursor = conexion.cursor(dictionary=True)
                cursor.execute(consulta, parametros or ())
                
                if not fetch:
                    filas_afectadas = cursor.rowcount
                    conexion.commit()
                    return filas_afectadas > 0  
                
                if fetch == 'one':
                    return cursor.fetchone()
                else:
                    return cursor.fetchall()
                    
            except Exception as error:
                conexion.rollback()
                print(f"Error en la consulta: {error}")
                return False
            finally:
                if conexion.is_connected():
                    cursor.close()
                    conexion.close()
        return False

    @staticmethod
    def encriptar_password(password: str) -> str:
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')

    @staticmethod
    def verificar_password(password: str, hashed: str) -> bool:
        if not hashed:
            return False
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

    @classmethod
    def llenar_desde_json(cls, archivo_json='peliculas.json'):
        try:
            with open(archivo_json, 'r', encoding='utf-8') as f:
                datos = json.load(f)
                
            for pelicula in datos:
                consulta = """
                INSERT INTO peliculas (titulo, director, genero, año, duracion, sinopsis)
                VALUES (%(titulo)s, %(director)s, %(genero)s, %(año)s, %(duracion)s, %(sinopsis)s)
                """
                if not cls.ejecutar_consulta(consulta, pelicula):
                    print(f"Error al insertar película {pelicula['titulo']}")
                    return False
            
            print("Base de datos llenada exitosamente desde el archivo JSON.")
            return True
        except Exception as error:
            print(f"Error al llenar la base de datos: {error}")
            return False

    @classmethod
    def generar_respaldo(cls, archivo_salida='respaldo_peliculas.json'):
        try:
            consulta = "SELECT * FROM peliculas"
            peliculas = cls.ejecutar_consulta(consulta, fetch=True)
            
            if peliculas:
                with open(archivo_salida, 'w', encoding='utf-8') as f:
                    json.dump(peliculas, f, indent=4, ensure_ascii=False)
                
                print(f"Respaldo generado exitosamente en {archivo_salida}")
                return True
            return False
        except Exception as error:
            print(f"Error al generar respaldo: {error}")
            return False