from conexion import ConexionBD
import getpass
from typing import Optional, Dict

class Login:
    def __init__(self):
        self.__tabla = 'usuarios'
        self.__usuario_actual = None

    def __validar_credenciales(self, email: str, password: str) -> Optional[Dict]:
        try:
            consulta = f"""
            SELECT id, nombre, email, password 
            FROM {self.__tabla} 
            WHERE email = %s
            """
            usuario = ConexionBD.ejecutar_consulta(consulta, (email,), fetch='one')
            
            if usuario and ConexionBD.verificar_password(password, usuario['password']):
                return {
                    'id': usuario['id'],
                    'nombre': usuario['nombre'],
                    'email': usuario['email']
                }
            return None
        except Exception as e:
            print(f"❌ Error al validar credenciales: {e}")
            return None

    def iniciar_sesion(self) -> Optional[int]:
        print("\n" + "="*40)
        print(" INICIO DE SESIÓN ".center(40))
        print("="*40)
        
        try:
            email = input("Email: ").strip()
            password = getpass.getpass("Contraseña: ").strip()
            
            if not email or not password:
                print("\n❌ Email y contraseña son obligatorios.")
                return None
            
            usuario = self.__validar_credenciales(email, password)
            
            if usuario:
                print(f"\n✅ ¡Bienvenido, {usuario['nombre']}!")
                self.__usuario_actual = usuario
                return usuario['id']
            else:
                print("\n❌ Email o contraseña incorrectos.")
                return None
        except Exception as e:
            print(f"\n❌ Error durante el inicio de sesión: {e}")
            return None

    def registrar(self) -> Optional[int]:
        print("\n" + "="*40)
        print(" REGISTRO DE NUEVO USUARIO ".center(40))
        print("="*40)
        
        try:
            nombre = input("Nombre: ").strip()
            email = input("Email: ").strip()
            password = getpass.getpass("Contraseña: ").strip()
            confirm_password = getpass.getpass("Confirmar contraseña: ").strip()
            
            if not all([nombre, email, password, confirm_password]):
                print("\n❌ Todos los campos son obligatorios.")
                return None
                
            if password != confirm_password:
                print("\n❌ Las contraseñas no coinciden.")
                return None
                
            if len(password) < 5:
                print("\n❌ La contraseña debe tener al menos 5 caracteres.")
                return None
            
            consulta_verificar = f"""
            SELECT id FROM {self.__tabla} 
            WHERE email = %s
            """
            existe = ConexionBD.ejecutar_consulta(
                consulta_verificar, 
                (email,), 
                fetch='one'
            )
            
            if existe:
                print("\n❌ Este email ya está registrado.")
                return None
            
            hashed_password = ConexionBD.encriptar_password(password)
            
            datos = {
                'nombre': nombre,
                'email': email,
                'password': hashed_password
            }
            
            consulta = f"""
            INSERT INTO {self.__tabla} 
            (nombre, email, password)
            VALUES (%(nombre)s, %(email)s, %(password)s)
            """
            
            resultado = ConexionBD.ejecutar_consulta(consulta, datos)
            if resultado:
                # Obtener el ID del usuario recién insertado
                consulta_id = "SELECT LAST_INSERT_ID() as id"
                usuario_id = ConexionBD.ejecutar_consulta(consulta_id, fetch='one')['id']
                print("\n✅ ¡Registro exitoso! Ahora puedes iniciar sesión.")
                return usuario_id
            else:
                print("\n⚠️ El registro no se completó (pero no hubo error en la consulta)")
                return None
                
        except Exception as e:
            print(f"\n❌ Error real durante el registro: {e}")
            return None

    def get_usuario_actual(self) -> Optional[Dict]:
        return self.__usuario_actual

    def cerrar_sesion(self) -> None:
        if self.__usuario_actual:
            print(f"\nℹ️ Sesión cerrada. Hasta luego, {self.__usuario_actual['nombre']}!")
        self.__usuario_actual = None