import vertexai
import streamlit as st
from vertexai.preview import generative_models
from vertexai.preview.generative_models import GenerativeModel, Part, Content, ChatSession

#initialize Vertex AI
#project = "Gemini Explorer"
project = "platinum-tube-425318-d5"
vertexai.init(project = project)

config = generative_models.GenerationConfig(
    #temperature(in the contaxt of GenAI - control the "creativity" of the genarated content)
    #A lower temperature value (close to 0) will result in more deterministic and conservative outputs, 
    #where the model is more likely to choose high-confidence predictions.

    #On the other hand, a higher temperature value will lead to more diverse and creative outputs, 
    #as it allows the model to take more risks and explore a wider range of possibilities.
    temperature=0.4,

    #top_k controls the diversity of the models predictions by limiting the number of tokens that are considered at each step
    #When the model generates the next token in a sequence, it ranks all the possible tokens based on their likelihood
    #Ex: model will only consider the top 50 most likely tokens for the next step, effectively reducing the number of choices and promoting diversity in the generated text.
    top_k=40
)

model = GenerativeModel(
    "gemini-pro",
    generation_config = config
)

chat = model.start_chat()

# helper function to display and send stramlit messages
def llm_function(chat: ChatSession, query):
    response = chat.send_message(query)
    output = response.candidates[0].content.parts[0].text

    with st.chat_message("model"):
        st.markdown(output)

    #adding the query and respponse to the chat history = chat memory
    st.session_state.messages.append(
        {
            "role" : "user",
            "content" : query
         }
    )

    st.session_state.messages.append(
        {
            "role" : "model",
            "content" : output
        }
    )

#adding the title to the chat
st.title("Gemini Explorer")

#initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

#to ignore the Initial Prompt = system prompt
#if len(st.session_state.messages) > 0:
    # Exclude the first item (system prompt) from the list of messages
    #displayed_messages = st.session_state.messages[1:]

    # Display the messages in the app
    #for message in displayed_messages:
        #st.write(message)

#Capture user's name
#user_name = st.text_input("Please enter your name")

#display and load to chat history
for index, message in enumerate(st.session_state.messages):
    content = Content(
        role = message["role"],
        parts = [Part.from_text(message["content"])]
    )

    #if index != 0:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

    #appending what we talked so far to the gemini chat history - so the model is aware of what we are doing - multi-turn conversation
    chat.history.append(content)

#for initial message startup
if len(st.session_state.messages) == 0:
    #if user_name:
    #    initial_prompt = f"Hey {user_name}! I'm ReX, your Google Gemini-powered assistant. Let's vibe with some emojis and get things done!"
    #else: 
    initial_prompt = "Hey there! I'm ReX, your Google Gemini-powered assistant. Let's vibe with some emojis and get things done!!!"
    with st.chat_message("model"):
        st.markdown(initial_prompt)
    #llm_function(chat, initial_prompt)

#for capture user input
query = st.chat_input("Say something...")

if query:
    with st.chat_message("user"):
        st.markdown(query)
    llm_function(chat, query)

#cd C:\Users\user\RadicalAIWorkspace
#python -m streamlit run gemini_explorer.py
#in gcloud CLI -> default authentication configuration -> gcloud auth application-default login 
