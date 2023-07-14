# Required Imports
import streamlit as st
import openai

# Load GPT-4 API Key
openai.api_key = st.secrets["openai_api_key"]

# Story Settings
story_settings = {
    "The Adventures of Family Mouse": '''Tief inmitten der grünen Wiesen, versteckt unter dem schützenden Schatten eines uralten Baumstumpfes, 
    liegt das gemütliche Heim der liebenswerten Mäusefamilie Körnchen. Mama und Papa Körnchen teilen ihr Zuhause 
    mit ihren drei entzückenden Kindern: der neugierigen Emma, dem abenteuerlustigen Max und dem jüngsten, 
    dem sanften kleinen Tim. Tim hat eine besondere Freundin namens Greta, eine Grille mit bemerkenswerten 
    Fähigkeiten. Sie kann in der Dunkelheit leuchten, vor nahenden Unwettern warnen, die Sprache aller Insekten 
    verstehen und sprechen, ein beruhigendes Lied spielen, das jedes Tier in Schlaf versetzt, und den Weg nach 
    Hause finden, egal wie weit sie sich von ihrem Heimatbaumstumpf entfernt hat. Nicht weit entfernt vom großen 
    Waldsee, leben sie in einer Welt voller bezaubernder und geheimnisvoller Geschöpfe, darunter der weise Frosch 
    Quako, die gutmütige Eule Frau Federblick und der stets gut gelaunte, aber etwas tollpatschige Biber Benny.

    Doch das Leben in dieser idyllischen Welt ist nicht immer unbeschwert. Gefahren lauern in Gestalt der 
    schlauen Katze Felina und des scharfäugigen Milans Raptor, die die Mäusefamilie stets auf Trab halten. Menschen 
    tauchen ab und zu in ihren Abenteuern auf, große Gestalten, die seltsame Dinge tun, und deren Anwesenheit stets 
    für eine gewisse Aufregung sorgt. Sie sind friedlich und die Mäuse schauen ihnen gerne heimlich bei ihrem Tun zu.

    Die Geschichten aus dem Leben der Mäusefamilie Körnchen sind geprägt von liebevoll gezeichneten Details, die 
    an Beatrix Potters charakteristischen Stil erinnern. Sie sind voll von bildhaften Beschreibungen der 
    wunderschönen Natur und lebhaften Dialogen zwischen den Tieren, die oft humorvoll sind und die Persönlichkeiten 
    der Figuren widerspiegeln. Aktiv erzählt, fühlen sich die jungen Zuhörer direkt in die Geschichte hineinversetzt. 
    So sind die Abenteuer der Mäusefamilie Körnchen ein friedvoller Abschluss eines jeden Tages, voller kleiner 
    Weisheiten und lehrreicher Momente, die die Kinder sanft in den Schlaf begleiten.''',
    "Ferdinand, the red racing Car": "In a bustling city, a shiny red racing car named Ferdinand resides. Ferdinand is known for his speed and agility, bringing joy to everyone who sees him race."
}

story_options = {
    "deutsch": ["Eine Mäusegeschichte", "Ferdinand, das rote Auto"],
    "english": ["The Adventures of Family Mouse", "Ferdinand, the red racing Car"],
    "espanol": ["Las Aventuras de la Familia Ratón", "Ferdinand, el coche rojo"]
}

# This dictionary maps the displayed names to the actual keys in `story_settings`.
story_mapping = {
    "Eine Mäusegeschichte": "The Adventures of Family Mouse",
    "Ferdinand, das rote Auto": "Ferdinand, the red racing Car",
    "The Adventures of Family Mouse": "The Adventures of Family Mouse",
    "Ferdinand, the red racing Car": "Ferdinand, the red racing Car",
    "Las Aventuras de la Familia Ratón": "The Adventures of Family Mouse",
    "Ferdinand, el coche rojo": "Ferdinand, the red racing Car"
}

def get_story_titles(prompt):
    # Generate story titles with GPT-4
    response = openai.Completion.create(engine="text-davinci-003", prompt=prompt, max_tokens=500)
    titles = response.choices[0].text.strip().split('. ')
    return titles

def get_story(prompt):
    # Generate story with GPT-4
    response = openai.Completion.create(engine="text-davinci-003", prompt=prompt, max_tokens=2500)
    return response.choices[0].text.strip()

def main():
    # Title
    st.title("Bedtime-Stories")

    # Password Protection
    password = st.text_input("Enter Password", type='password')
    if password != st.secrets["password"]:
        st.error("Incorrect password. Please try again.")
        st.stop()

    # Dropdown for Language Selection
    language = st.selectbox("Language of the story", ["deutsch", "english", "espanol"], index=0)

    st.subheader("Choose your story")

    # Dropdown for Story Selection
    story = st.selectbox("Select a Story", story_options[language])

    # Get Story Titles
    if st.button("Get Story Titles"):
        prompt = f"In the language of {language}, using the setting of '{story_settings[story_mapping[story]]}', generate 10 engaging and fun titles for a bedtime story."
        titles = get_story_titles(prompt)
        st.session_state.titles = titles

    # Show Titles
    if 'titles' in st.session_state:
        st.session_state.title = st.selectbox("Select a Title", st.session_state.titles)

        # Generate Story
        if st.button("Write this story now"):
            prompt = f"In the language of {language}, using the setting of '{story_settings[story_mapping[story]]}', and with the title '{st.session_state.title}', generate a captivating and age-appropriate bedtime story. Make sure the story is engaging, fun, and has a clear beginning, middle, and end."
            st.session_state
