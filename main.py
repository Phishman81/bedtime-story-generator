# Required Imports
import streamlit as st
import openai

# Load GPT-4 API Key
openai.api_key = st.secrets["openai_api_key"]

# Story Settings
story_settings = {
    "The Adventures of Family Mouse": "In a cozy hole in a green meadow, lives a family of mice. The family includes Mama Mouse, Papa Mouse, and their three little mouse children.",
    "Ferdinand, the red racing Car": "In a bustling city, a shiny red racing car named Ferdinand resides. Ferdinand is known for his speed and agility, bringing joy to everyone who sees him race."
}

def get_story_titles(prompt):
    # Generate story titles with GPT-4
    response = openai.Completion.create(engine="text-davinci-002", prompt=prompt, max_tokens=100)
    titles = response.choices[0].text.strip().split('\n')
    return titles

def get_story(prompt):
    # Generate story with GPT-4
    response = openai.Completion.create(engine="text-davinci-002", prompt=prompt, max_tokens=1000)
    return response.choices[0].text.strip()

def main():
    # Title
    st.title("Bedtime-Stories")

    # Password Protection
    password = st.text_input("Enter Password", type='password')
    if password != st.secrets["password"]:
        st.error("Incorrect password. Please try again.")
        st.stop()

    st.subheader("Choose your story")

    # Dropdown for Story Selection
    story = st.selectbox("Select a Story", list(story_settings.keys()))

    # Get Story Titles
    if st.button("Get Story Titles"):
        prompt = story_settings[story] + "\nNow generate 10 titles for a bedtime story."
        titles = get_story_titles(prompt)
        st.session_state.titles = titles

    # Show Titles
    if 'titles' in st.session_state:
        title = st.selectbox("Select a Title", st.session_state.titles)

        # Generate Story
        if st.button("Write this story now"):
            prompt = story_settings[story] + " The title of the story is '" + title + "'. Now write the story."
            story = get_story(prompt)
            st.session_state.story = story

    # Show Story
    if 'story' in st.session_state:
        st.markdown("# " + title)
        st.markdown("## " + story)

# Main function
if __name__ == "__main__":
    main()
