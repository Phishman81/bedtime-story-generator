import streamlit as st
import openai

# Initialize OpenAI API
openai.api_key = 'your_openai_api_key_here'

def login():
    if 'password' not in st.session_state:
        st.session_state['password'] = ''
    
    password = st.text_input('Enter password:', type='password')
    
    if password == 'your_password_here':
        st.session_state['password'] = password
    else:
        st.error('Incorrect password')

if 'password' not in st.session_state or st.session_state['password'] != 'your_password_here':
    login()
else:
    st.write('Welcome to the Story Generator!')
    
    story_settings = ['Fantasy', 'Adventure', 'Sci-Fi', 'Mystery']
    selected_setting = st.selectbox('Choose a story setting:', story_settings)
    
    if st.button('Generate Story Titles'):
        response = openai.Completion.create(
            model="gpt-4o",
            prompt=f"Generate three interesting story titles for a {selected_setting} story:",
            max_tokens=50,
            n=3
        )
        titles = [choice['text'].strip() for choice in response.choices]
        st.session_state['titles'] = titles

    if 'titles' in st.session_state:
        selected_title = st.selectbox('Choose a story title:', st.session_state['titles'])
    
    if st.button('Generate Story Outline'):
        response = openai.Completion.create(
            model="gpt-4o",
            prompt=f"Generate a story outline for the {selected_setting} story titled '{selected_title}':",
            max_tokens=150
        )
        outline = response['choices'][0]['text'].strip()
        st.session_state['outline'] = outline

    if 'outline' in st.session_state:
        st.write('Story Outline:')
        st.write(st.session_state['outline'])
    
    if st.button('Generate Complete Story'):
        response = openai.Completion.create(
            model="gpt-4o",
            prompt=f"Write a complete {selected_setting} story titled '{selected_title}' with the following outline:\n{st.session_state['outline']}",
            max_tokens=500
        )
        story = response['choices'][0]['text'].strip()
        st.session_state['story'] = story

    if 'story' in st.session_state:
        st.write('Complete Story:')
        st.write(st.session_state['story'])

    if st.button('Generate Illustrative Image'):
        response = openai.Image.create(
            prompt=f"Illustrate a scene from the story titled '{selected_title}' with the following outline:\n{st.session_state['outline']}",
            n=1,
            size="1024x1024"
        )
        image_url = response['data'][0]['url']
        st.session_state['image_url'] = image_url

    if 'image_url' in st.session_state:
        st.image(st.session_state['image_url'])
