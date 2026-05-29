import streamlit as st
from werkzeug.security import check_password_hash
from supabase import Client 

# si estoy autenticada por hacer login, no puedo estar aca, deben redirigirme a home/
#*1. Redirigi si ya estoy loggeada
if st.session_state.get('authenticated', False): #'authenticated' == True cuando usuario que szesiona esta exit logeado
    st.switch_page('pages/home.py')
# personaje = {k:v, }
# personaje['nacionalidad'] #! si no exits ERROR!
# personaje.get('nacionalidad', 'No existe esta key') #*

#* 2. como no esta loggado pintamos la page de login, para q lo haga.
st.title('🔑 Inicio de sesión')
with st.form('login_form'):
    #* 3. inputs del form
    correo = st.text_input('Correo electrónico') #🏳️ para comprar y traerne al usuario que intenta log, si es q existe
    contrasena = st.text_input('Contraseña', type='password')
    submitted = st.form_submit_button('Iniciar Sesion')
    
     #* 3. Clic sobre el btn de envio del form
    if submitted:
        if not correo or not contrasena:
            st.error('Complete todos los campos del formulario.')
        else:
            supabase: Client  = st.session_state.supabase #aqui la estoy usando
            # respuesta = supabase.table('usuarios').select('*').eq('correo', correo).execute() #* → [{el_usuario}, {}, {}...] → {}
            respuesta = supabase.table('usuarios').select('*').eq('correo', correo).single().execute() # → {}  #& otra opcio
            
            if respuesta.data: #✅, pero si tienes un 400 0o 500 → respuesta.error
                # ususario = respuesta.data[0] #* hay q desestructurarlo
                ususario = respuesta.data #& otra opcio
                print('**'*20)
                print(ususario)
                print(respuesta)
                # if check_password_hash( contrasena_hasada, contrasena_en_text_plano)
                # if check_password_hash( 'kjshcoiahscviohsdv hsldkfvl', '123456')
                if check_password_hash(ususario['contrasena_hash'], contrasena): #* hay match entre la bbdd y data usuario
                    #*guademos en sesion todos los datos del usuario que preciam se registro y esta en la BBDD
                    st.session_state.authenticated = True
                    st.session_state.user_id = ususario['id']
                    st.session_state.user_correo = ususario['correo']
                    st.session_state.user_nombre = ususario['nombre']
                    st.session_state.user_edad = ususario['edad']
                    st.success('✅Sesion Iniciada correctamente !! ')
                    st.rerun()
                    #volvera a ejecutar este script, perooo mantendra el valor de las variables de session!
                else: ##* hay match entre la bbdd y data usuario
                    st.error('❌Contrasena incorrecta')
            else:
                st.error('❌Usuario no encontrado, registrese')

# enlace para ir a registro
st.markdown('---')
if st.button('No tienes cienta? Registrate aqui?'):
    st.switch_page('pages/registro.py')