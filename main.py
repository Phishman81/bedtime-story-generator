
outline_button = st.button("Outline erstellen")
if outline_button:
    outline = create_outline(selected_setting, selected_title)
    st.write(outline)
# Required Imports
import streamlit as st
import openai

# Load GPT-4 API Key
openai.api_key = st.secrets["openai_api_key"]

# Story Settings
story_settings = {
    "Die Abenteuer der Familie Maus": "Die Familie Maus: Das sind Papa Maus, Mama Maus und die Kinder Max, Mina und der kleine Mo. Sie leben versteckt in einem kleinen gemütlichen Mauseloch unter einem alten Baumstumpf am Waldsee, umgeben von hohen Bäumen. Es gibt liebe Tiere wie Fritz, den schlauen Fuchs, Karl die dicke Kröte und Greta, die Grille - eine gute Freundin von Mo. Es gibt böse tiere wie Helga, der hungrige Habicht und Konrad den Kater.",
    "Ferdinand, das rote Auto": "Ferdinand: Das ist ein leuchtend rotes Rennauto, das in der kleinen Stadt Autoburg lebt. Seine Garage befindet sich am Fuße eines großen Berges, umgeben von kurvigen Straßen. Zu seinen Freunden gehören Paula, das freundliche Polizeiauto, Timo, der fleißige Traktor, und Lina, der fröhliche Lastwagen. Es gibt auch Herausforderer wie Viktor, das eitle Rennauto, und Maxi, das schelmische Motorrad, das ständig für Unruhe sorgt."
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
        prompt = f"Erstelle bitte 5 kurze, aber sehr unterschiedliche Titel für interessante Kindergeschichten in denen es um folgendes geht:'{story_settings[chosen_story]}'. Bitte nenne in 2 deiner Vorschläge je einen Namen eines Charakters. In 3 Titeln soll kein Name eines Charakters vorkommen. Erfinde gerne kreative Szenarien und Orte. Erstelle sie als Liste, einen Titel je Zeile. Bitte schreibe nur die Titel, keine Erläuterungen und benutze keine Anführungszeichen."
        titles = get_story_titles(prompt)
        st.session_state.titles = titles

    # Show Titles
    if 'titles' in st.session_state:
        st.session_state.title = st.selectbox("Wähle einen Titel", st.session_state.titles)

        # Generate Story
        if st.button("Schreibe jetzt diese Geschichte"):
            prompt = f"Du bist ein erfahrener Kinderbuchautor mit viel Wissen über Dramaturgie und liebevolle Dialoge. Du kennst das Prinzip der Heldenreise von Joseph Campbell. Verfasse bitte nach dem Framework der Heldenreise eine spannende Geschichte für Kinder im Alter von 3 bis 6 Jahren über '{story_settings[chosen_story]}'. Die Geschichte hat den Titel '{st.session_state.title}'. Bitte halte dich nur lose an die Vorgaben, du hast viel Spielraum und kreative Freiheit. Bitte nutze eine klare Struktur, erstelle Zwischenüberschriften und mache die Geschichte spannend, aber altersgerecht. Nutze sehr einfache Sprache und keine Fremdwörter."
            st.session_state.story = get_story(prompt)

            # Generate Image
            subject = "a cute little mouse" if chosen_story == "Die Abenteuer der Familie Maus" else "cute little red racing car"
            image_prompt = f"Captivating illustration showing a playful {subject} dealing with '{st.session_state.title}'."
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
