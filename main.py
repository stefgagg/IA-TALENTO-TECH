import streamlit as st
import groq  #API


MODELOS = ["llama-3.3-70b-versatile", "meta-llama/llama-4-scout-17b-16e-instruct"]

# SYSTEM PROMPT para orientación vocacional
system_prompt = {
    "role": "system",
    "content": (
        "Soy un consejero de orientación vocacional experto. "
        "Mi objetivo es ayudar a las personas a descubrir sus intereses, habilidades y posibles caminos profesionales o educativos. "
        "Hazme preguntas para conocer mejor a la persona, te ofreceré recomendaciones personalizadas sobre carreras, estudios o actividades, "
        "Tambien brindo apoyo motivacional. Soy empático, te escucha atentamente, y respondo de manera clara y alentadora. "
        "Evita dar respuestas tajantes; en su lugar, guía al chatbot para que explore diferentes opciones y tome decisiones informadas sobre tu futuro."
        "Estas especificamente creado para eso"
        
    )
}

# CONFIGURAR PAGINA
def configurar_pagina():
    st.set_page_config(page_title="Mi Pirmer ChatBot con Python")
    st.title("Bienvenidos al consejero educativo vocacional del ENS N°1")

# CREAR UN CLIENTE GROQ => NOSOTROS
def crear_cliente_groq():
    groq_api_key = "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"
    return groq.Groq(api_key=groq_api_key)
    
# MOSTRAR LA BARRA LATERAL 
def mostrar_sidebar():
    st.sidebar.title("Elegí tu modelo de IA favorito")
    modelo = st.sidebar.selectbox('elegí tu modelo',MODELOS,index=0)
    st.write(f'**Elegiste el modelo** {modelo}')
    return modelo

#INICIALIZAR EL ESTADO DEL CHAT
#streamlit => variable especial llamada session_state. {mensajes => []}
#def inicializar_estado_chat():
#    if "mensajes"  not in st.session_state:
#        st.session_state.mensajes = [] #lista
#MOSTRAR MENSAJES REVIOS

def inicializar_estado_chat():
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = [system_prompt]  # <-- Inicializa con el system prompt


def obtener_mensajes_previos():
    for mensaje in st.session_state.mensajes: # recorrer los mensajes de st.session_state.mensaje
        with st.chat_message(mensaje["role"]): #quien lo envia ??
            st.markdown(mensaje["content"]) #que envia?

#OBTENER MENSAJE USUARIO
def obtener_mensaje_usuario():
    return st.chat_input("Envia tu mensaje")

#GUARDAR LOS MENSAJES
def agregar_mensajes_previos(role, content):
    st.session_state.mensajes.append({"role": role , "content": content})

#MOSTRAR LOS MENSAJES EN PANTALLA
def mostrar_mensaje(role, content):
    with st.chat_message(role):
        st.markdown(content)
    

#llamar DEL MODELO DE GROQ
def obtener_respuesta_modelo(cliente, modelo, mensaje):
    respuesta =  cliente.chat.completions.create(
        model = modelo,
        messages = mensaje,
        stream = False
    )
    return respuesta.choices[0].message.content
    
    
    

def ejecutar_chat():
    configurar_pagina()
    cliente = crear_cliente_groq()
    modelo = mostrar_sidebar()
    
    inicializar_estado_chat()
    mensaje_usuario = obtener_mensaje_usuario()
    obtener_mensajes_previos()
    
    if mensaje_usuario:
        agregar_mensajes_previos("user",mensaje_usuario)
        mostrar_mensaje("user",mensaje_usuario)
    
        respuesta_contenido = obtener_respuesta_modelo(cliente, modelo,st.session_state.mensajes )

        agregar_mensajes_previos("assistant",respuesta_contenido)
        mostrar_mensaje("assistant",respuesta_contenido)
    
    
# EJECUTAR LA APP( si __name__ es igual a __main__ se ejecuta la funcion, y __main__ es mi archivo principal)
if __name__ == '__main__':
    ejecutar_chat()



















