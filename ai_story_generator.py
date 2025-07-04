import os
from dotenv import load_dotenv
import google.generativeai as genai
import streamlit as st
load_dotenv()
def configure_ai():
    """
    Configures the generative AI model with the API key from environment variables.
    Returns the GenerativeModel object if successful, None otherwise.
    """
    api_key =os.getenv("GOOGLE_API_KEY")
    if not api_key:
        st.error("Error: GOOGLE_API_KEY environment variable not found.")
        st.warning("Please get an API key from https://aistudio.google.com/app/apikey and set it.")
        st.info("On Windows, run: `setx GOOGLE_API_KEY \"YOUR_API_KEY\"` in your terminal (and restart it).")
        st.info("On macOS/Linux, add to your .bashrc/.zshrc: `export GOOGLE_API_KEY=\"YOUR_API_KEY\"` (and source it or restart terminal).")
        return None
    
    genai.configure(api_key=api_key)
    try:
        # It's good practice to try a simple operation to check API key validity
        model = genai.GenerativeModel('gemini-1.5-flash')
        return model
    except Exception as e:
        st.error(f"Failed to configure AI model. Check your API key and internet connection. Error: {e}")
        return None

def generate_story(model, prompt):
    """
    Generates a story using the provided model and prompt.
    Returns the generated text or an error message.
    """
    if not prompt:
        return "Please enter a valid prompt to generate a story."

    try:
        # Create a more detailed prompt for the AI
        full_prompt = f"Write a short, creative, and engaging story based on the following prompt: '{prompt}'"
        
        with st.spinner("Generating your story... Please wait."):
            response = model.generate_content(full_prompt)
            return response.text
    except Exception as e:
        return f"An error occurred while generating the story: {e}"

def main():
    """
    Main function to run the AI Story Generator Streamlit application.
    """
    st.set_page_config(page_title="AI Story Generator", page_icon="✍️")

    st.title("Welcome to the AI Story Generator ✍️")
    st.markdown("---")

    # Configure the AI model once
    # Use st.session_state to avoid re-initializing the model on every rerun
    if 'model' not in st.session_state:
        st.session_state.model = configure_ai()

    model = st.session_state.model

    if model:
        st.write("Enter a prompt below and let the AI craft a unique story for you!")
        
        # Get user input for the story prompt
        user_prompt = st.text_area("Your Story Prompt:", height=100, placeholder="E.g., A detective cat solving a mystery in a magical library.")
        
        # Button to trigger story generation
        if st.button("Generate Story"):
            if user_prompt:
                story = generate_story(model, user_prompt)
                st.markdown("---")
                st.subheader("Your AI-Generated Story:")
                st.write(story)
                st.markdown("---")
            else:
                st.warning("Please enter a prompt to generate a story.")
    else:
        st.error("AI model could not be configured. Please resolve the API key issue to proceed.")
        st.markdown("---")
        st.info("Once you set your `GOOGLE_API_KEY` environment variable, restart this Streamlit application.")

if __name__ == "__main__":
    main()