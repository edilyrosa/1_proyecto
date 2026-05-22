import streamlit as st
from werkzeug.security import generate_password_hash
from supabase import Client

# verificamos si usuario esta logeado
if st.session_state.get('authenticated', False):
    st.swtich_page("pages/home.py")

st.title('🔐 Registro de Usuario')
# crear el formulario de registro
with st.form('registro_form'):
    nombre = st.text_input('Nombre Completo')
    correo = st.text_input('Correo Electrónico')
    edad = st.number_input('Edad', min_value=0, max_value=120)
    contrasena = st.text_input('Contraseña', type='password', help='La contraseña debe tener al menos 6 caracteres')