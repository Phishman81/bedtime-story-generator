# Required Imports
import streamlit as st
import openai

# Load GPT-4 API Key
openai.api_key = st.secrets["openai_api_key"]

# Story Settings
story_settings = {
    "Die Abenteuer der Familie Maus": 'SETTING:Waldsee,idyllisch,umgeben von hohen Bäumen und bunten Blumen.Menschenaktivitäten nur aus Ferne.CHARAKTERE:FAMILIE MAUS:Papa:Ein Arbeiter,Mama:liebevoll,Max:mutig,Mina:neugierig,Mo:abenteuerlustig,Greta:fröhliche Grille,FREUNDE:Fritz:schlauer Fuchs,Bella:gütige Biene.FEINDE:Helga:hungriger Habicht,Konrad:knurriger Kater.',
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

# Function to generate image with DALL-E
def get_image(prompt):
    response = openai.Image.create(prompt=prompt, model="image-alpha-001", size="512x512")
    try:
        return response['data'][0]['url']
    except IndexError:
        print("No image was generated.")
        return None

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
        prompt = f"Erstelle 10 kurze, ansprechende und lustige Titel für Gutenachtgeschichten für sehr kleine Kinder im Alter von 1 bis 4 Jahren. Hier sind die Charaktere und das Setting für diese Geschichten '{story_settings[chosen_story]}'. Es müssen nicht alle Charaktere in den Geschichten auftauchen. % Titel bitte ohne einen Namen eines Charakters. Wichtig ist, das die Titel magisch und phantasievoll sind. Erstelle sie als Liste, einen Titel je Zeile."
        titles = get_story_titles(prompt)
        st.session_state.titles = titles

    # Show Titles
    if 'titles' in st.session_state:
        st.session_state.title = st.selectbox("Wähle einen Titel", st.session_state.titles)

        # Generate Story
        if st.button("Schreibe jetzt diese Geschichte"):
            prompt = f"In der Sprache Deutsch, mit der Einstellung von '{story_settings[chosen_story]}', und mit dem Titel '{st.session_state.title}', generiere eine 1000 Wörter lange, fesselnde und altersgerechte Gutenachtgeschichte im Stil von Beatrix Potter. Stelle sicher, dass die Geschichte spannend, lustig ist und einen klaren Anfang, Mitte und Ende hat."
            st.session_state.story = get_story(prompt)

            # Generate Image
            subject = "Maus" if chosen_story == "Die Abenteuer der Familie Maus" else "rotes Rennauto"
            image_prompt = f"Eine fesselnde Illustration, die eine verspielte {subject} im Stil von Beatrix Potter darstellt. Die Illustration bezieht sich auf den Titel '{st.session_state.title}'."
            st.session_state.image_url = get_image(image_prompt)

    # Show Image and Story
    if 'image_url' in st.session_state and st.session_state.image_url is not None:
        st.image(st.session_state.image_url)
    
    if 'story' in st.session_state and 'title' in st.session_state:
        st.markdown("# " + st.session_state.title)
        st.markdown("## " + st.session_state.story)

# Main function
if __name__ == "__main__":
    main()
