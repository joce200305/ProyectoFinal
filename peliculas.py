from conexion import ConexionBD
from typing import Optional, Dict, List, Union

class Peliculas:
    def __init__(self):
        self.__tabla = 'peliculas'

    def __validar_datos(self, datos: Dict) -> bool:
        required = ['titulo', 'director', 'genero', 'año', 'duracion']
        if not all(key in datos and datos[key] for key in required):
            return False
        
        try:
            año = int(datos['año'])
            duracion = int(datos['duracion'])
            return año > 1900 and duracion > 0
        except ValueError:
            return False

    def crear(self, datos: Dict) -> bool:
        if not self.__validar_datos(datos):
            print("Datos incompletos o inválidos. El año debe ser mayor a 1900 y la duración positiva.")
            return False
        
        consulta = f"""
        INSERT INTO {self.__tabla} (titulo, director, genero, año, duracion, sinopsis)
        VALUES (%(titulo)s, %(director)s, %(genero)s, %(año)s, %(duracion)s, %(sinopsis)s)
        """
        
        try:
            resultado = ConexionBD.ejecutar_consulta(consulta, datos)
            if resultado:
                print(" Película agregada exitosamente!")
                return True
            print("No se pudo agregar la película")
            return False
        except Exception as e:
            print(f" Error al crear película: {e}")
            return False

    def leer(self, id_pelicula: Optional[int] = None) -> Optional[Union[Dict, List[Dict]]]:
        try:
            if id_pelicula:
                consulta = f"SELECT * FROM {self.__tabla} WHERE id = %s"
                return ConexionBD.ejecutar_consulta(consulta, (id_pelicula,), fetch='one')
            else:
                consulta = f"SELECT * FROM {self.__tabla} ORDER BY titulo"
                return ConexionBD.ejecutar_consulta(consulta, fetch=True)
        except Exception as e:
            print(f" Error al leer películas: {e}")
            return None

    def actualizar(self, id_pelicula: int, datos: Dict) -> bool:
        if not self.__validar_datos(datos):
            print(" Datos incompletos o inválidos.")
            return False
        
        datos['id'] = id_pelicula
        consulta = f"""
        UPDATE {self.__tabla}
        SET titulo = %(titulo)s, director = %(director)s, 
            genero = %(genero)s, año = %(año)s, 
            duracion = %(duracion)s, sinopsis = %(sinopsis)s
        WHERE id = %(id)s
        """
        
        try:
            resultado = ConexionBD.ejecutar_consulta(consulta, datos)
            if resultado:
                print(" Película actualizada correctamente!")
                return True
            print(" No se actualizó ninguna película (ID no existe o datos iguales)")
            return False
        except Exception as e:
            print(f" Error al actualizar: {e}")
            return False

    def eliminar(self, id_pelicula: int) -> bool:
        consulta = f"DELETE FROM {self.__tabla} WHERE id = %s"
        try:
            resultado = ConexionBD.ejecutar_consulta(consulta, (id_pelicula,))
            if resultado:
                print(" Película eliminada correctamente!")
                return True
            print(" No se eliminó ninguna película (ID no existe)")
            return False
        except Exception as e:
            print(f" Error al eliminar: {e}")
            return False

    def mostrar_todas(self) -> bool:
        try:
            peliculas = self.leer()
            if peliculas:
                print("\n" + "="*120)
                print(" LISTA DE PELÍCULAS ".center(120))
                print("="*120)
                print(f"{'ID':<5} | {'Título':<30} | {'Director':<20} | {'Género':<15} | {'Año':<6} | {'Duración':<8} | {'Sinopsis'}")
                print("-"*120)
                for pelicula in peliculas:
                    print(f"{pelicula['id']:<5} | {pelicula['titulo']:<30} | {pelicula['director']:<20} | {pelicula['genero']:<15} | {pelicula['año']:<6} | {pelicula['duracion']:<8} | {pelicula['sinopsis'][:50]}...")
                print("="*120)
                return True
            else:
                print(" No hay películas registradas.")
                return False
        except Exception as e:
            print(f" Error al mostrar películas: {e}")
            return False