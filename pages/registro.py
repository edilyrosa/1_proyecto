# import streamlit as st
# from werkzeug.security import generate_password_hash
# from supabase import Client

# # verificamos si usuario esta logeado
# if st.session_state.get('authenticated', False):
#     st.switch_page("pages/home.py")

# st.title('🔐 Registro de Usuario')
# # crear el formulario de registro
# with st.form('registro_form'):
#     nombre = st.text_input('Nombre Completooo', placeholder="Ej: Ana Pérez")
#     correo = st.text_input('Correo Electrónico')
#     edad = st.number_input('Edad', min_value=0, max_value=120)
#     contrasena = st.text_input('Contraseña', type='password', help='La contraseña debe tener al menos 6 caracteres')


import streamlit as st
from werkzeug.security import generate_password_hash

supabase = st.session_state.supabase
 
# Verificamos si el usuario ya está logueado para redirigirlo
if st.session_state.get('authenticated', False):
    st.switch_page("pages/home.py")
 
# Título de la página
st.title('🔒Registro de Usuario')
 
# Crear el formulario de registro
with st.form('registro_form'):
    nombre = st.text_input('Nombre Completo')
    correo = st.text_input('Correo Electrónico')
    edad = st.number_input('Edad', min_value=0, max_value=120)
    contrasena = st.text_input('Contraseña', type='password', help='La contraseña debe tener al menos 6 caracteres')
    confirmar_contrasena = st.text_input('Confirmar contraseña', type='password', help='La contraseña debe tener al menos 6 caracteres')

    # El botón de envío es OBLIGATORIO dentro del form
    boton_registrar = st.form_submit_button('Registrarse')

# LÓGICA DE BASE DE DATOS (BACKEND)
# ==============================================================================
# Este bloque se ejecuta cuando el usuario hace clic en el botón
if boton_registrar:

    # Validaciones básicas
    if not nombre or not correo or not contrasena:
        st.error('Por favor, rellena todos los campos obligatorios.')
    elif len(contrasena) < 6:
        st.error('La contraseña es muy corta. Debe tener al menos 6 caracteres.')
    elif confirmar_contrasena != contrasena:
        st.error('Las contraseñas no coinciden')
    else:
        # Mostramos un indicador de carga mientras procesa
        with st.spinner('Creando usuario en la base de datos...'):
            try:
                # Paso A: Hashear la contraseña para máxima seguridad
                contrasena_hash = generate_password_hash(contrasena)
               
                # Paso B: Empaquetar los datos para Supabase
                # Asegúrate de que las claves de la izquierda ("nombre", "correo", etc.)
                # sean exactamente iguales a las columnas de tu tabla
                datos_usuario = {
                    "nombre": nombre,
                    "correo": correo,
                    "edad": edad,
                    "contrasena_hash": contrasena_hash
                }
               
                # Paso C: Insertar los datos en la tabla 'usuarios'
                response = supabase.table('usuarios').insert(datos_usuario).execute()
            
                # Paso D: Confirmar el éxito en pantalla
                st.success('¡Usuario registrado exitosamente!')
                st.balloons()                            #* nuevo
                st.session_state.registro_exitoso = True #* nuevo
            
            except Exception as e:
                # Capturar y mostrar cualquier error que devuelva Supabase (ej. correo duplicado)
                st.error(f'Hubo un problema al registrar el usuario: {e}')


if st.session_state.get('registro_exitoso', False): #* nuevo
    if st.button('Ir a iniciar sesion'):
        st.switch_page('pages/login.py')