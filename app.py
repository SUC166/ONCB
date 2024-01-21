import streamlit as st
from googlesearch import search
import openai

# Set your OpenAI API key
openai.api_key = "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"

# Streamlit app
st.title("Dynamic Chatbot with Google Search and OpenAI")

# Function to get Google search results
def get_google_results(query, num_results=3):
    results = list(search(query, num_results=num_results, stop=num_results))
    return results

# Function to chat using OpenAI
def chat_with_openai(prompt, conversation=[]):
    conversation.append({"role": "user", "content": prompt})
    response = openai.Completion.create(
        engine="davinci",
        messages=conversation,
    )
    return response.choices[0].text.strip()

# Streamlit UI
conversation_history = []
user_input = st.text_input("You: ")

if user_input:
    # Check if the user input requires Google Search
    if "search" in user_input.lower():
        search_query = user_input.replace("search", "").strip()
        st.text("Searching on Google...")
        google_results = get_google_results(search_query)

        # Display Google search results
        for i, result in enumerate(google_results):
            st.write(f"{i + 1}. {result}")

        # Add search results to conversation history
        conversation_history.append({"role": "assistant", "content": f"Here are the search results for '{search_query}': {', '.join(google_results)}"})
    else:
        # Use OpenAI for regular conversations
        st.text("Chatbot is responding...")
        openai_response = chat_with_openai(user_input, conversation_history)
        st.text(f"Chatbot: {openai_response}")

        # Add user input and chatbot response to conversation history
        conversation_history.append({"role": "user", "content": user_input})
        conversation_history.append({"role": "assistant", "content": openai_response})

# Display conversation history as a chat
for chat in conversation_history:
    role = chat["role"]
    content = chat["content"]
    st.text(f"{role.capitalize()}: {content}")
