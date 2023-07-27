# Required Imports
import streamlit as st
import openai

# Load GPT-4 API Key
openai.api_key = st.secrets["openai_api_key"]

# Story Settings
story_settings = {
    "Die Abenteuer der Familie Maus": 
    """
    SETTING: WALDSEE
    Ein idyllisches Refugium, umgeben von hohen, grünen Bäumen und bunten Blumen, die das Ufer säumen. Ein geheimnisvoller Ort, wo menschliche Aktivitäten nur aus der Ferne beobachtet werden.    
    CHARAKTERE:
    FAMILIE MAUS: PAPA MAUS - Ein fürsorglicher und harter Arbeiter, stets bemüht, seine Familie zu schützen und zu versorgen. MAMA MAUS - Liebevolle und geduldige Mutter, sie hält die Familie zusammen und sorgt dafür, dass jeder sich sicher und geliebt fühlt. MAX - Der älteste der Mäusekinder, mutig und verantwortungsbewusst. MINA - Die mittlere Maus, sie ist neugierig und immer bereit zu lernen. MO - Das jüngste Kind, unschuldig und abenteuerlustig, beste Freunde mit Greta, der Grille.
    FREUNDE DER FAMILIE: GRETA - Die fröhliche Grille, immer mit einem Lied auf den Lippen, sie bringt Freude und Musik in das Leben der Mäusefamilie. FRITZ - Der schlaue Fuchs, voller Weisheit und Ratschläge für die Familie Maus. BELLA - Die gütige Biene, die hart arbeitet, um den besten Honig im ganzen Wald zu produzieren.
    FEINDE: HELGA - Die hungrige Habichtsdame, immer auf der Suche nach ihrer nächsten Mahlzeit. KONRAD - Der knurrige Kater, ein ewiger Schrecken für die Mäusefamilie.
    MENSCHEN - Unbekannte Wesen, die am Waldsee für Freizeitaktivitäten auftauchen. Sie sind faszinierend und beängstigend.
    """,
    "Ferdinand, das rote Auto": "In einer belebten Stadt lebt ein glänzendes rotes Rennauto namens Ferdinand. Ferdinand ist bekannt für seine Geschwindigkeit und Agilität und bringt jedem, der ihn Rennen sieht, Freude."
}

# Function to generate story titles with GPT-4
def get_story_titles(prompt):
    response = openai.Completion.create(engine="text-davinci-003", prompt=prompt, max_tokens=500)
    titles = response.choices[0].text.strip().split('\n')  # Updated here
    return titles

# Function to generate story with GPT-4
def get_story(prompt):
    response = openai.Completion.create(engine="text-davinci-003", prompt=prompt, max_tokens=3500)
    return response.choices[0].text.strip()

def main():
    # Title
    st.title("Bedtime-Stories")

    # Password Protection
    password = st.text_input("Enter Password", type='password')
    if password != st.secrets["password"]:
        st.error("Incorrect password. Please try again.")
        st.stop()

    st.subheader("Wähle deine Geschichte")

    # Dropdown for Story Selection
    chosen_story = st.selectbox("Wähle eine Geschichte", list(story_settings.keys()))

    # Get Story Titles
    if st.button("Geschichtstitel erhalten"):
        prompt = f"In der Sprache Deutsch, mit der Einstellung von '{story_settings[chosen_story]}', generiere 10 kurze, ansprechende und lustige Titel für eine Gutenachtgeschichte. Erstelle sie als Liste, einen Titel je Zeile."
        titles = get_story_titles(prompt)
        st.session_state.titles = titles

    # Show Titles
    if 'titles' in st.session_state:
        st.session_state.title = st.selectbox("Wähle einen Titel", st.session_state.titles)

        # Generate Story
        if st.button("Schreibe jetzt diese Geschichte"):
            prompt = f"In der Sprache Deutsch, mit der Einstellung von '{story_settings[chosen_story]}', und mit dem Titel '{st.session_state.title}', generiere eine 1000 Wörter lange, fesselnde und altersgerechte Gutenachtgeschichte im Stil von Beatrix Potter. Stelle sicher, dass die Geschichte spannend, lustig ist und einen klaren Anfang, Mitte und Ende hat."
            st.session_state.story = get_story(prompt)

    # Show Story
    if 'story' in st.session_state and 'title' in st.session_state:
        st.markdown("# " + st.session_state.title)
        st.markdown("## " + st.session_state.story)

# Main function
if __name__ == "__main__":
    main()
