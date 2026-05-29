
# venv\Scripts\activate
# Ve a share.streamlit.io e inicia sesión con tu cuenta de GitHub.
# https://github.com/edilyrosa/proyecto_1_Py_automatizaciones/blob/main/app.py

import streamlit as st
from supabase import create_client, Client

# la pestana de la page
st.set_page_config(
    page_title="Sistema CRUD de Registro", 
    page_icon=":rocket:", 
    layout="wide")


if 'supabase' not in st.session_state:
    try:
        # Conexión a Supabase
        url = st.secrets["SUPABASE_URL"]
        key = st.secrets['SUPABASE_KEY']
        # creamos al cliente supabase
        st.session_state.supabase = create_client(url, key) #aqui la estamos creando
        st.success("Conexión a Supabase exitosa")
        supabase: Client  = st.session_state.supabase
        response = supabase.table('usuarios').select('*').execute()
        print(response.data)
    except Exception as e:
        st.error(f"Error al conectar a Supabase: {e}")
        st.stop()
        

#* Contenido de la página principal
st.title("🔐 Bienvenido a la aplicación") #<h1>

st.markdown("""
Esta aplicación permite gestionar usuarios de manera segura:

- Registro de nuevos usuarios (con contraseña cifrada)
- Inicio de sesión
- Visualización y edición del perfil
- Eliminación de cuenta

**Para comenzar, utiliza el menú de la izquierda.**
""")

# mostrar el estado de autenticacion en un abarra lateral, del usuario que este sesionando.
# loa st.session_state son diccionarios con key : value, entonce spueden usar el metodo get('key', False)
if st.session_state.get('authenticated', False):
    st.sidebar.success(f"Usuario autenticado: {st.session_state.get('user_email', 'usuario')}")
    if st.sidebar.button('Cerrar Sesion'):
        st.session_state['authenticated'] = False
        st.session_state['user_email'] = None
        st.success("Has cerrado sesión exitosamente.")
        st.rerun()
else:
    st.sidebar.info('No estas autorizado')