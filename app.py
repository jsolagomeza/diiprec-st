import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="DiipRec")
st.title("DiipRec")
st.header("Pregunta sobre la presentación :books: ")

api_key = st.secrets["OPENAI_API_KEY"]

endpoint = "https://api.openai.com/v1/chat/completions"
client = OpenAI(api_key=api_key)

# Check if the messages are in session state, if not initialize them
if "messages" not in st.session_state:
    st.session_state.messages = []

system_message = st.secrets["system_message"]
training_message = st.secrets["training_message"]

if system_message and "system_message_set" not in st.session_state:
    st.session_state.chat = []
    st.session_state.messages.append({"role": "system", "content": system_message})
    st.session_state.messages.append({"role": "user", "content": training_message})

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=st.session_state.messages,
        temperature=0.2,
    )

    st.session_state["system_message_set"] = True

# Display the chat messages
for message in st.session_state.chat:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if prompt := st.chat_input("Escribe un mensaje"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.chat.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Assistant response

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("Escribiendo...")
        
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=st.session_state.messages,
            temperature=0.2,
            stream=True
        )

        try:
            model_answer = ""
            for chunk in completion:
                model_answer += (chunk.choices[0].delta.content or "")
                message_placeholder.markdown(model_answer + "▌")
                
        except KeyError:
            model_answer = "Error, compruebe su conexión a internet o intente de nuevo"
        
        message_placeholder.markdown(model_answer)
    
    st.session_state.messages.append({"role": "assistant", "content": model_answer})
    st.session_state.chat.append({"role": "assistant", "content": model_answer})


