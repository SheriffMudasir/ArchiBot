import os
import streamlit as st
import openai

st.markdown("""
<style>
.css-iiif1v.ef3psqc3
{
    visibility: hidden;          
}
.css-h5rgaw.ea3mdgi1
{
    visibility: hidden;          
}            
</style>
""", unsafe_allow_html=True)

openai.api_key = st.secrets["OPENAI_API_KEY"]
   
def get_completion(prompt, model="gpt-3.5-turbo", api_key=None):
    openai.api_key = api_key
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0,  # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]

def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0, api_key=None):
    openai.api_key = api_key
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature,  # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]

def collect_messages(prompt, api_key=None, conversation=None):
    if conversation is None:
        conversation = [{'role': 'system', 'content': """
        You are ArchiBot, a bot with thorough knowledge in architecture and building construction. \
        You respond to every prompt in the context of architecture and building construction. \
        You politely decline any prompt out of the scope of architecture and building. \                 
        You only answer questions related to architecture. You do not provide code. You do not answer questions not related to architecture and building construction. When a user prompts you for information not related to architecture or building construction, simply apologize to them and re-emphasize that you are an architectural bot. \
        You provide basic information on users' queries based on architecture and building construction and ask if they would like more details. \
        Provide more details on the concept if they so desired.\
        Also, recommend other resources or channels where users can get more information like books or websites.
        """}]  # accumulate messages

    context = conversation
    context.append({'role': 'user', 'content': prompt})
    response = get_completion_from_messages(context, api_key=api_key)
    context.append({'role': 'assistant', 'content': response})

    return context

st.title("ArchiBot🤖")

# Initialize the conversation state in session_state
if "conversation" not in st.session_state:
    st.session_state.conversation = None

# Use st.form context manager to handle user input
with st.form(key="user_input_form"):
    # Set up a default prompt
    default_prompt = "Type in your prompt!"
    prompt = st.text_input("User:", default_prompt)

    # Submit the form immediately to start the conversation
    form_submit = st.form_submit_button("Submit!")

    # Collect messages and display conversation history
    if form_submit:
        context = collect_messages(prompt, api_key=st.secrets["OPENAI_API_KEY"], conversation=st.session_state.conversation)

        # Create empty containers for displaying chat messages
        chat_messages = [st.empty() for _ in range(len(context))]

        for idx, message in enumerate(context):
            role = message["role"]
            content = message["content"]

            if role == "user":
                chat_messages[idx].markdown(f"**User🤵:** {content}")
            elif role == "assistant":
                chat_messages[-(idx+1)].markdown(f"**ArchiBot🤖:** {content}")

        # Update the conversation state in session_state
        st.session_state.conversation = context

# Adding the side_bar with "About me" and multiline text
with st.sidebar:
    st.title("Meet me")
    st.image("image.jpg", caption="Sheriff Olalekan Mudasir")
    st.text("""
    I am Sheriff, an AI enthusiast with a strong passion for machine learning. I take great pleasure in creating free AI tools 
    to make this exciting technology accessible to everyone. I also enjoy contributing to the AI community 
    and sharing my knowledge and skills with others. My expertise in machine learning allows me to develop intelligent 
    systems that can make a positive impact on various industries. I am dedicated to fostering innovation and learning 
    in the field of artificial intelligence, and I thrive on the opportunity to create tools that empower others to explore 
    and experiment with AI technologies freely.
    """)

    st.write("Buy me a cup of coffee ☕[HERE](https://paystack.com/pay/scj36fu7mx)")
