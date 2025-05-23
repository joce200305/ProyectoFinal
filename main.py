from peliculas import Peliculas
from login import Login
from conexion import ConexionBD
import json
import os

def mostrar_menu_principal() -> str:
    print("\n" + "="*40)
    print(" SISTEMA DE GESTIÓN DE CINE ".center(40))
    print("="*40)
    print("1. Iniciar sesión")
    print("2. Registrarse")
    print("3. Salir")
    print("="*40)
    return input("Seleccione una opción (1-3): ").strip()

def mostrar_menu_usuario() -> str:
    print("\n" + "="*40)
    print(" MENÚ DE USUARIO ".center(40))
    print("="*40)
    print("1. Ver todas las películas")
    print("2. Buscar película por ID")
    print("3. Agregar nueva película")
    print("4. Actualizar película")
    print("5. Eliminar película")
    print("6. Llenar base de datos desde JSON")
    print("7. Generar respaldo de películas")
    print("8. Cerrar sesión")
    print("="*40)
    return input("Seleccione una opción (1-8): ").strip()

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def pausa():
    input("\nPresione Enter para continuar...")

def main():
    sistema_login = Login()
    gestor_peliculas = Peliculas()
    
    while True:
        limpiar_pantalla()
        opcion = mostrar_menu_principal()
        
        if opcion == '1':
            limpiar_pantalla()
            usuario_id = sistema_login.iniciar_sesion()
            
            if usuario_id:
                while True:
                    limpiar_pantalla()
                    opcion_usuario = mostrar_menu_usuario()
                    
                    if opcion_usuario == '1':
                        limpiar_pantalla()
                        gestor_peliculas.mostrar_todas()
                        pausa()
                        
                    elif opcion_usuario == '2':
                        limpiar_pantalla()
                        try:
                            id_pelicula = int(input("ID de la película a buscar: "))
                            pelicula = gestor_peliculas.leer(id_pelicula)
                            
                            if pelicula:
                                print("\n" + "="*40)
                                print(" DETALLES DE LA PELÍCULA ".center(40))
                                print("="*40)
                                print(f"ID: {pelicula['id']}")
                                print(f"Título: {pelicula['titulo']}")
                                print(f"Director: {pelicula['director']}")
                                print(f"Género: {pelicula['genero']}")
                                print(f"Año: {pelicula['año']}")
                                print(f"Duración: {pelicula['duracion']} minutos")
                                print(f"Sinopsis: {pelicula['sinopsis']}")
                                print("="*40)
                            else:
                                print("\nℹ️ Película no encontrada.")
                        except ValueError:
                            print("\n❌ Error: El ID debe ser un número.")
                        pausa()
                        
                    elif opcion_usuario == '3':
                        limpiar_pantalla()
                        print("\n" + "="*40)
                        print(" AGREGAR NUEVA PELÍCULA ".center(40))
                        print("="*40)
                        datos = {
                            'titulo': input("Título: ").strip(),
                            'director': input("Director: ").strip(),
                            'genero': input("Género: ").strip(),
                            'año': input("Año: ").strip(),
                            'duracion': input("Duración (minutos): ").strip(),
                            'sinopsis': input("Sinopsis: ").strip() or None
                        }
                        
                        try:
                            datos['año'] = int(datos['año'])
                            datos['duracion'] = int(datos['duracion'])
                            if gestor_peliculas.crear(datos):
                                print("\n✅ Película agregada exitosamente!")
                            else:
                                print("\n⚠️ No se pudo agregar la película")
                        except ValueError:
                            print("\n❌ Error: El año y la duración deben ser números.")
                        pausa()
                        
                    elif opcion_usuario == '4':
                        limpiar_pantalla()
                        try:
                            id_pelicula = int(input("ID de la película a actualizar: "))
                            pelicula = gestor_peliculas.leer(id_pelicula)
                            
                            if pelicula:
                                print("\n" + "="*40)
                                print(" ACTUALIZAR PELÍCULA ".center(40))
                                print("="*40)
                                print("Deje en blanco los campos que no desea cambiar")
                                print("="*40)
                                
                                datos = {
                                    'titulo': input(f"Título [{pelicula['titulo']}]: ").strip() or pelicula['titulo'],
                                    'director': input(f"Director [{pelicula['director']}]: ").strip() or pelicula['director'],
                                    'genero': input(f"Género [{pelicula['genero']}]: ").strip() or pelicula['genero'],
                                    'año': input(f"Año [{pelicula['año']}]: ").strip() or str(pelicula['año']),
                                    'duracion': input(f"Duración [{pelicula['duracion']}]: ").strip() or str(pelicula['duracion']),
                                    'sinopsis': input(f"Sinopsis [{pelicula['sinopsis'][:20] if pelicula['sinopsis'] else 'None'}...]: ").strip() or pelicula['sinopsis']
                                }
                                
                                try:
                                    datos['año'] = int(datos['año'])
                                    datos['duracion'] = int(datos['duracion'])
                                    if gestor_peliculas.actualizar(id_pelicula, datos):
                                        print("\n✅ Película actualizada correctamente!")
                                    else:
                                        print("\n⚠️ No se actualizó ninguna película")
                                except ValueError:
                                    print("\n❌ Error: El año y la duración deben ser números.")
                            else:
                                print("\nℹ️ Película no encontrada.")
                        except ValueError:
                            print("\n❌ Error: El ID debe ser un número.")
                        pausa()
                        
                    elif opcion_usuario == '5':
                        limpiar_pantalla()
                        try:
                            id_pelicula = int(input("ID de la película a eliminar: "))
                            confirmacion = input(f"\n¿Está seguro de eliminar esta película? (s/n): ").lower()
                            
                            if confirmacion == 's':
                                if gestor_peliculas.eliminar(id_pelicula):
                                    print("\n✅ Película eliminada correctamente!")
                                else:
                                    print("\n⚠️ No se eliminó ninguna película")
                        except ValueError:
                            print("\n❌ Error: El ID debe ser un número.")
                        pausa()
                        
                    elif opcion_usuario == '6':
                        limpiar_pantalla()
                        archivo = input("\nNombre del archivo JSON (dejar vacío para 'peliculas.json'): ").strip() or 'peliculas.json'
                        confirmacion = input(f"\n¿Está seguro de llenar la base de datos desde {archivo}? (s/n): ").lower()
                        
                        if confirmacion == 's':
                            if os.path.exists(archivo):
                                if ConexionBD.llenar_desde_json(archivo):
                                    print("\n✅ Base de datos llenada exitosamente!")
                                else:
                                    print("\n⚠️ Hubo problemas al llenar la base de datos")
                            else:
                                print(f"\n❌ Error: El archivo {archivo} no existe.")
                        pausa()
                        
                    elif opcion_usuario == '7':
                        limpiar_pantalla()
                        archivo = input("\nNombre del archivo de salida (dejar vacío para 'respaldo_peliculas.json'): ").strip() or 'respaldo_peliculas.json'
                        if ConexionBD.generar_respaldo(archivo):
                            print("\n✅ Respaldo generado exitosamente!")
                        else:
                            print("\n⚠️ Hubo problemas al generar el respaldo")
                        pausa()
                        
                    elif opcion_usuario == '8':
                        sistema_login.cerrar_sesion()
                        break
                        
                    else:
                        print("\n❌ Opción no válida.")
                        pausa()
                        
        elif opcion == '2':
            limpiar_pantalla()
            if sistema_login.registrar():
                print("\n✅ ¡Usuario registrado con éxito!")
            else:
                print("\n⚠️ No se completó el registro")
            pausa()
            
        elif opcion == '3':
            limpiar_pantalla()
            print("\n¡Hasta luego!")
            break
            
        else:
            print("\n❌ Opción no válida.")
            pausa()

if __name__ == "__main__":
    main()