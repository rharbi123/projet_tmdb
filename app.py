import streamlit as st
from tmdb_api import get_movie_details, search_movie_by_name, get_movies_by_genre

# Configuration de la page
st.set_page_config(page_title="TMDB Explorer", page_icon="🎬", layout="wide")

# -----------------------------------------
# INJECTION DE CSS POUR LE STYLE
# -----------------------------------------
st.markdown("""
<style>
    /* Polices et fond */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');
    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }
    .stApp {
        background: linear-gradient(135deg, #0f0f1a 0%, #1a1a2e 100%);
        color: #ffffff;
    }
    
    /* En-tête */
    .main-title {
        text-align: center;
        font-size: 3rem;
        font-weight: 600;
        background: -webkit-linear-gradient(45deg, #FF4B4B, #FF9A9E);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
    }
    .sub-title {
        text-align: center;
        color: #a0a0b0;
        margin-bottom: 30px;
    }
    
    /* Boutons */
    .stButton>button {
        border-radius: 30px;
        background: linear-gradient(90deg, #FF4B4B, #FF7676);
        color: white;
        border: none;
        padding: 10px 30px;
        font-weight: 600;
        transition: 0.3s;
        width: 100%;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 4px 15px rgba(255, 75, 75, 0.4);
    }
    
    /* Cartes (containers) */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 10px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
        backdrop-filter: blur(10px);
        transition: transform 0.3s ease;
    }
    div[data-testid="stVerticalBlockBorderWrapper"]:hover {
        transform: translateY(-5px);
        border: 1px solid rgba(255, 75, 75, 0.5);
    }
    
    /* Onglets */
    .stTabs [data-baseweb="tab-list"] {
        gap: 20px;
        background-color: transparent;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: transparent;
        border-radius: 10px 10px 0 0;
        color: #a0a0b0;
        font-weight: 600;
    }
    .stTabs [aria-selected="true"] {
        color: #FF4B4B !important;
        border-bottom: 3px solid #FF4B4B !important;
    }
</style>
""", unsafe_allow_html=True)

# En-tête
st.markdown('<p class="main-title">🎬 TMDB Explorer</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Découvrez vos films par ID, nom ou genre</p>', unsafe_allow_html=True)

IMG_URL = "https://image.tmdb.org/t/p/w500"

GENRES = {
    "Action": 28, "Aventure": 12, "Animation": 16, "Comédie": 35,
    "Crime": 80, "Documentaire": 99, "Drame": 18, "Familial": 10751,
    "Fantastique": 14, "Horreur": 27, "Mystère": 9648, "Romance": 10749,
    "Science-Fiction": 878, "Thriller": 53, "Guerre": 10752, "Western": 37
}

tab1, tab2, tab3 = st.tabs(["🔍 Par ID", "📝 Par Nom", "🎭 Par Genre"])

# -----------------------------------------
# ONGLET 1
# -----------------------------------------
with tab1:
    st.markdown("<br>", unsafe_allow_html=True)
    col_search, _ = st.columns([1, 2])
    with col_search:
        movie_id = st.number_input("Entrez l'ID du film", min_value=1, value=550, step=1)
        if st.button("Rechercher par ID", type="primary"):
            st.session_state.search_id = True

    if st.session_state.get("search_id", False):
        with st.spinner("Recherche en cours..."):
            film = get_movie_details(movie_id)
            if film and film.get("titre"):
                st.markdown("<br>", unsafe_allow_html=True)
                with st.container(border=True):
                    col1, col2 = st.columns([1, 3])
                    with col1:
                        if film.get("poster"):
                            st.image(f"{IMG_URL}{film['poster']}", use_container_width=True)
                    with col2:
                        st.title(film["titre"])
                        st.write(f"📅 **Date de sortie :** {film.get('date_sortie', 'Inconnue')}")
                        st.write(f"🎭 **Genres :** {', '.join(film['genres'])}")
                        st.markdown("---")
                        m1, m2 = st.columns(2)
                        m1.metric("⭐ Note moyenne", f"{film['note_moyenne']} / 10")
                        m2.metric("🔥 Popularité", f"{film['popularite']}")
            else:
                st.error("Film introuvable.")

# -----------------------------------------
# ONGLET 2
# -----------------------------------------
with tab2:
    st.markdown("<br>", unsafe_allow_html=True)
    col_search, _ = st.columns([1, 2])
    with col_search:
        nom_film = st.text_input("Entrez le nom du film", "Fight Club")
        if st.button("Rechercher par Nom", type="primary"):
            st.session_state.search_nom = True
            
    if st.session_state.get("search_nom", False):
        with st.spinner("Recherche en cours..."):
            resultats = search_movie_by_name(nom_film)
            if resultats:
                st.markdown(f"### Top {len(resultats)} résultats pour *'{nom_film}'*")
                cols = st.columns(len(resultats))
                for i, film in enumerate(resultats):
                    with cols[i]:
                        with st.container(border=True):
                            if film.get("poster"):
                                st.image(f"{IMG_URL}{film['poster']}", use_container_width=True)
                            st.markdown(f"**{film['titre']}**")
                            st.caption(f"⭐ {film['note_moyenne']} | 📅 {film['date_sortie']}")
            else:
                st.warning("Aucun résultat.")

# -----------------------------------------
# ONGLET 3
# -----------------------------------------
with tab3:
    st.markdown("<br>", unsafe_allow_html=True)
    col_search, _ = st.columns([1, 2])
    with col_search:
        genre_choisi = st.selectbox("Choisissez un genre", list(GENRES.keys()))
        if st.button("Rechercher par Genre", type="primary"):
            st.session_state.search_genre = True
            
    if st.session_state.get("search_genre", False):
        with st.spinner("Recherche en cours..."):
            resultats = get_movies_by_genre(GENRES[genre_choisi])
            if resultats:
                st.markdown(f"### Films populaires : *'{genre_choisi}'*")
                # On affiche en 5 colonnes, 2 lignes
                cols = st.columns(5)
                for i, film in enumerate(resultats):
                    with cols[i % 5]:
                        with st.container(border=True):
                            if film.get("poster"):
                                st.image(f"{IMG_URL}{film['poster']}", use_container_width=True)
                            st.markdown(f"**{film['titre']}**")
                            st.caption(f"⭐ {film['note_moyenne']} | 📅 {film['date_sortie']}")
            else:
                st.warning("Aucun résultat.")