import streamlit as st

if not st.session_state.get('authenticated', False):
    st.warning('Debes iniciar sesionb para acceder a esta vista!') #Relampago
    st.switch_page('pages/login.py')
    
st.title('🏠 Bienvenido')
#* mostrar la info del usuario en sesion
nombre = st.session_state.get('user_nombre', 'Usuario')
st.markdown(f'### hola , **{nombre}** 👋🏻')
st.markdown("""
    Esta es tu página principal. Desde aquí puedes:
    - ✏️ **Actualizar tu perfil**
    - 🗑️ **Eliminar tu cuenta**
    - 🚪 **Cerrar sesión**
    Usa el menú de la izquierda o los botones de abajo.
""" 
)

# las 2 columnas de los 2 btn

col1, col2 = st.columns(2)

with col1:
    if st.button('Ver/Editar Perfil'):
        st.switch_page('pages/perfil.py') #TODO
with col2:
    if st.button('Cerrar sesion'):
        st.session_state.authenticated = False
        st.session_state.user_id = None
        st.session_state.user_correo = None
        st.session_state.user_nombre = None
        st.session_state.user_edad = None
        st.rerun()
    