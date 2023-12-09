import pickle
import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

CLIENT_ID = "70a9fb89662f4dac8d07321b259eaad7"
CLIENT_SECRET = "4d6710460d764fbbb8d8753dc094d131"

# Initialize the Spotify client
client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_song_album_cover_url(song_name, artist_name):
    search_query = f"track:{song_name} artist:{artist_name}"
    results = sp.search(q=search_query, type="track")

    if results and results["tracks"]["items"]:
        track = results["tracks"]["items"][0]
        album_cover_url = track["album"]["images"][0]["url"]
        print(album_cover_url)
        return album_cover_url
    else:
        return "https://i.postimg.cc/0QNxYz4V/social.png"

def recommend(song):
    index = music[music['song'] == song].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_music_names = []
    recommended_music_posters = []
    recommended_artist_names = []
    for i in distances[1:6]:
        # fetch the movie poster
        artist = music.iloc[i[0]].artist
        print(artist)
        print(music.iloc[i[0]].song)
        recommended_music_posters.append(get_song_album_cover_url(music.iloc[i[0]].song, artist))
        recommended_music_names.append(music.iloc[i[0]].song)
        recommended_artist_names.append(music.iloc[i[0]].artist)
    return recommended_music_names,recommended_music_posters, recommended_artist_names

def getArtist(song):
    index = music[music['song'] == song].index[0]
    artist = music.iloc[index].artist
    return artist

def drop_after_brace(input_string):
    result = ''
    brace_encountered = False

    for char in input_string:
        if char == '{':
            brace_encountered = True
        if not brace_encountered:
            result += char

    return result

st.header('GrooveGalaxy:headphones:')

st.sidebar.markdown(":orange[App made by] :orange[-] :orange[[Pranjal Asthana](https://github.com/PranjalAsthana)]")
st.sidebar.markdown(":orange[[Please Support GrooveGalaxy on Github](https://github.com/PranjalAsthana/GrooveGalaxy)]")


music = pickle.load(open('songsdata.pkl','rb'))
similarity = pickle.load(open('similaritymatrix.pkl','rb'))

music_list = music['song'].values + '{ ' + music['artist'].values + ' }'
selected_song = st.selectbox(
    "Select a song you like from the menu below",
    music_list
) 

selected_song = drop_after_brace(selected_song)

if st.button('Recommend'):
    recommended_music_names,recommended_music_posters, recommended_artist_names = recommend(selected_song)
    artist = getArtist(selected_song)
    st.write(f"Since you like {selected_song} by {artist}, you may also like:")
    col1, col2, col3, col4, col5= st.columns(5)
    with col1:
        st.image(recommended_music_posters[0])
        st.write(recommended_music_names[0],"by",recommended_artist_names[0])
    with col2:
        st.image(recommended_music_posters[1])
        st.write(recommended_music_names[1],"by",recommended_artist_names[1])

    with col3:
        st.image(recommended_music_posters[2])
        st.write(recommended_music_names[2],"by",recommended_artist_names[2])
    with col4:
        st.image(recommended_music_posters[3])
        st.write(recommended_music_names[3],"by",recommended_artist_names[3])
    with col5:
        st.image(recommended_music_posters[4])
        st.write(recommended_music_names[4],"by",recommended_artist_names[4])