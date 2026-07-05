import ast
import html
import io

import pandas as pd
import pickle
import requests
import streamlit as st

try:
    from colorthief import ColorThief
    COLORTHIEF_AVAILABLE = True
except ModuleNotFoundError:
    COLORTHIEF_AVAILABLE = False

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------
st.set_page_config(
    page_title=" 𝒞𝒾𝓃𝑒𝑀𝒶𝓉𝒸𝒽 Movie Recommender",
    page_icon="🌌",
    layout="wide"
)

# --------------------------------------------------
# Load Data
# --------------------------------------------------
movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

movie_details = pd.read_csv("tmdb_5000_movies.csv")

# --------------------------------------------------
# TMDB API
# --------------------------------------------------
try:
    API_KEY = st.secrets["TMDB_API_KEY"]
except Exception:
    st.error(
        "TMDB API key not found. Add TMDB_API_KEY to your .streamlit/secrets.toml "
        "(locally) or to your app's Secrets settings (on Streamlit Cloud)."
    )
    st.stop()

PLACEHOLDER_POSTER = "https://placehold.co/500x750?text=No+Poster"
DEFAULT_ACCENT = (35, 82, 145)


# --------------------------------------------------
# Data helpers
# --------------------------------------------------
@st.cache_data(show_spinner=False)
def fetch_poster(movie_id):
    """Fetch a poster URL from TMDB, falling back to a placeholder on any failure."""
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}"

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
    except (requests.RequestException, ValueError):
        return PLACEHOLDER_POSTER

    if data.get("poster_path"):
        return "https://image.tmdb.org/t/p/w500/" + data["poster_path"]

    return PLACEHOLDER_POSTER


@st.cache_data(show_spinner=False)
def fetch_selected_poster(movie):
    """Look up the TMDB id for `movie` and fetch its poster. Returns placeholder if not found."""
    matches = movie_details[movie_details['title'] == movie]['id']

    if matches.empty:
        return PLACEHOLDER_POSTER

    return fetch_poster(matches.values[0])


@st.cache_data(show_spinner=False)
def get_dominant_color(poster_url):
    """Download the poster and extract its dominant color for theming."""
    if not COLORTHIEF_AVAILABLE or poster_url == PLACEHOLDER_POSTER:
        return DEFAULT_ACCENT

    try:
        response = requests.get(poster_url, timeout=5)
        response.raise_for_status()
        color_thief = ColorThief(io.BytesIO(response.content))
        return color_thief.get_color(quality=1)
    except Exception:
        return DEFAULT_ACCENT


def get_genres(title):
    """Return a ' • '-joined string of genre names for `title`, or '' if unavailable."""
    matches = movie_details[movie_details['title'] == title]['genres']

    if matches.empty or pd.isna(matches.values[0]):
        return ""

    try:
        genre_list = ast.literal_eval(matches.values[0])
    except (ValueError, SyntaxError):
        return ""

    return " • ".join(g['name'] for g in genre_list)


def format_money(amount):
    """Format a raw dollar figure into something like $165.0M."""
    if not amount or pd.isna(amount) or amount <= 0:
        return "N/A"
    if amount >= 1_000_000_000:
        return f"${amount / 1_000_000_000:.1f}B"
    if amount >= 1_000_000:
        return f"${amount / 1_000_000:.1f}M"
    return f"${amount:,.0f}"


def get_movie_meta(title):
    """Pull the full detail set for a movie title, with safe fallbacks for missing data."""
    row = movie_details[movie_details['title'] == title]

    if row.empty:
        return None

    row = row.iloc[0]

    return {
        'rating': round(row['vote_average'], 1) if pd.notna(row['vote_average']) else None,
        'year': str(row['release_date'])[:4] if pd.notna(row['release_date']) else 'N/A',
        'runtime': int(row['runtime']) if pd.notna(row['runtime']) else None,
        'overview': row['overview'] if pd.notna(row['overview']) else '',
        'genres': get_genres(title),
        'language': str(row['original_language']).upper() if pd.notna(row.get('original_language')) else 'N/A',
        'budget': format_money(row.get('budget')),
        'revenue': format_money(row.get('revenue')),
        'popularity': round(row['popularity'], 1) if pd.notna(row.get('popularity')) else None,
    }


def recommend(title):
    """Return the top 5 similar movies, each enriched with poster + metadata + match %."""
    movie_index = movies[movies['title'] == title].index[0]
    distances = similarity[movie_index]

    ranked = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    results = []
    for idx, score in ranked:
        rec_title = movies.iloc[idx].title
        movie_id = movies.iloc[idx].movie_id
        meta = get_movie_meta(rec_title) or {}

        results.append({
            'title': rec_title,
            'poster': fetch_poster(movie_id),
            'match': round(min(max(score, 0), 1) * 100),
            'rating': meta.get('rating'),
            'year': meta.get('year'),
            'genres': meta.get('genres'),
        })

    return results


# --------------------------------------------------
# Global styling
# --------------------------------------------------
def inject_global_css(accent, dark_mode):
    overlay_top = 0.55 if dark_mode else 0.10
    overlay_bottom = 0.95 if dark_mode else 0.55
    base_bg = "#0e1117" if dark_mode else "#f4f4f6"
    text_color = "#fafafa" if dark_mode else "#1a1a1a"
    card_bg = "rgba(255,255,255,0.05)" if dark_mode else "rgba(255,255,255,0.55)"
    card_border = "rgba(255,255,255,0.12)" if dark_mode else "rgba(0,0,0,0.08)"

    st.markdown(f"""
    <style>
    :root {{
        --accent-r: {accent[0]};
        --accent-g: {accent[1]};
        --accent-b: {accent[2]};
    }}

    html, body {{
        background: {base_bg};
    }}
    [data-testid="stAppViewContainer"],
    .stApp,
    [data-testid="stMain"],
    [data-testid="stHeader"],
    .main,
    .block-container {{
        background: transparent !important;
        color: {text_color};
    }}

    .blurred-poster-bg {{
        position: fixed;
        inset: -40px;
        background-size: cover;
        background-position: center;
        filter: blur(40px) brightness({0.45 if dark_mode else 0.85}) saturate(1.15);
        z-index: -2;
        transition: background-image 0.8s ease-in-out;
    }}
    .bg-overlay {{
        position: fixed;
        inset: 0;
        background: linear-gradient(180deg,
            rgba(14,17,23,{overlay_top}),
            rgba(14,17,23,{overlay_bottom}));
        z-index: -1;
    }}

    .stButton > button {{
        background: linear-gradient(135deg,
            rgba(var(--accent-r),var(--accent-g),var(--accent-b),0.95),
            rgba(var(--accent-r),var(--accent-g),var(--accent-b),0.65));
        color: white;
        border: none;
        border-radius: 10px;
        font-weight: 600;
        padding: 0.6rem 1rem;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }}
    .stButton > button:hover {{
        transform: scale(1.03);
        box-shadow: 0 6px 24px rgba(var(--accent-r),var(--accent-g),var(--accent-b),0.5);
        color: white;
    }}

    .glass-card {{
        background: {card_bg};
        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);
        border-radius: 20px;
        border: 1px solid {card_border};
        padding: 28px 32px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.25);
        color: {text_color};
    }}
    .glass-rating {{
        display: inline-block;
        font-weight: 700;
        font-size: 15px;
        padding: 4px 12px;
        border-radius: 20px;
        background: rgba(var(--accent-r),var(--accent-g),var(--accent-b),0.3);
        margin-bottom: 10px;
    }}
    .facts-grid {{
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 10px;
        margin-top: 18px;
        text-align: center;
    }}
    .facts-grid div {{
        background: rgba(var(--accent-r),var(--accent-g),var(--accent-b),0.12);
        border-radius: 10px;
        padding: 8px 6px;
        font-size: 12.5px;
    }}

    @keyframes fadeInUp {{
        from {{ opacity: 0; transform: translateY(24px); }}
        to   {{ opacity: 1; transform: translateY(0); }}
    }}
    .rec-card {{
        background: {card_bg};
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid {card_border};
        border-radius: 16px;
        padding: 12px;
        text-align: center;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        animation: fadeInUp 0.6s ease both;
        color: {text_color};
    }}
    .rec-card:hover {{
        transform: scale(1.06);
        box-shadow: 0 10px 34px rgba(0,0,0,0.45);
    }}
    .rec-card img {{
        border-radius: 12px;
        width: 100%;
        display: block;
    }}
    .rec-title {{
        margin-top: 10px;
        font-weight: 700;
        font-size: 14.5px;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }}
    .rec-meta {{
        font-size: 12.5px;
        opacity: 0.75;
        margin-top: 2px;
    }}
    .match-badge {{
        display: inline-block;
        margin-top: 8px;
        padding: 3px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 700;
        background: rgba(var(--accent-r),var(--accent-g),var(--accent-b), 0.28);
    }}
    .app-tagline {{
        text-align: center;
        opacity: 0.7;
        margin-top: -8px;
        margin-bottom: 4px;
        font-size: 15px;
    }}
    .app-footer {{
        text-align: center;
        opacity: 0.55;
        font-size: 13px;
        margin-top: 48px;
        padding-top: 18px;
        border-top: 1px solid {card_border};
    }}
    </style>
    """, unsafe_allow_html=True)


def inject_poster_background(poster_url):
    if poster_url and poster_url != PLACEHOLDER_POSTER:
        st.markdown(f"""
        <div class="blurred-poster-bg" style="background-image: url('{poster_url}');"></div>
        <div class="bg-overlay"></div>
        """, unsafe_allow_html=True)


# --------------------------------------------------
# UI
# --------------------------------------------------
top_left, top_right = st.columns([5, 1])

with top_left:
    st.markdown(
        """
        <h1 style='text-align:center; margin-bottom:2px;'>🌌 𝒞𝒾𝓃𝑒𝑀𝒶𝓉𝒸𝒽</h1>
        <h3 style='text-align:center; margin-top:0; opacity:0.85; font-weight:500;'>Movie Recommender System</h3>
        """,
        unsafe_allow_html=True
    )
    st.markdown(
        "<p class='app-tagline'>Find your next favorite movie.</p>",
        unsafe_allow_html=True
    )

with top_right:
    dark_mode = st.toggle("🌙 Dark", value=True)

st.caption(f"🔍 Search among **{len(movies):,} movies**")

selected_movie = st.selectbox(
    "Search a movie",
    sorted(movies['title'].values),
    index=None,
    placeholder="Search any movie..."
)

if selected_movie:
    selected_poster = fetch_selected_poster(selected_movie)
    accent = get_dominant_color(selected_poster)
else:
    selected_poster = None
    accent = DEFAULT_ACCENT

inject_global_css(accent, dark_mode)
if selected_movie:
    inject_poster_background(selected_poster)

if selected_movie:
    meta = get_movie_meta(selected_movie) or {}

    rating_display = meta.get('rating') if meta.get('rating') is not None else "N/A"
    year = meta.get('year', 'N/A')
    runtime_display = f"{meta['runtime']} min" if meta.get('runtime') else "N/A"
    genres = meta.get('genres', '')
    overview_text = meta.get('overview', '')

    left, right = st.columns([1, 3])

    with left:
        st.image(selected_poster, use_container_width=True)

    with right:
        meta_line = f"{year} • {runtime_display}" + (f" • {genres}" if genres else "")

        card_html = f"""
        <div class="glass-card">
            <div class="glass-rating">★ {rating_display}/10</div>
            <h2 style="margin:4px 0 6px 0;">{html.escape(selected_movie)}</h2>
            <div style="opacity:0.85; margin-bottom:12px;">{html.escape(meta_line)}</div>
            <p style="line-height:1.55; margin-bottom:0;">{html.escape(overview_text)}</p>
            <div class="facts-grid">
                <div><b>Language</b><br/>{meta.get('language', 'N/A')}</div>
                <div><b>Popularity</b><br/>{meta.get('popularity', 'N/A')}</div>
                <div><b>Budget</b><br/>{meta.get('budget', 'N/A')}</div>
                <div><b>Revenue</b><br/>{meta.get('revenue', 'N/A')}</div>
            </div>
        </div>
        """
        st.markdown(card_html, unsafe_allow_html=True)

    st.write("")

    c1, c2, c3 = st.columns([2, 1, 2])
    with c2:
        recommend_btn = st.button("✨ Find Similar Movies", use_container_width=True)

    if recommend_btn:
        with st.spinner("🎬 Finding similar movies..."):
            recs = recommend(selected_movie)

        st.success(f"🎬 Because you liked **{selected_movie}**...")
        st.divider()
        st.subheader("✨ You might also like")

        cols = st.columns(5)

        for i, rec in enumerate(recs):
            with cols[i]:
                rating_text = f"⭐ {rec['rating']}" if rec['rating'] is not None else "⭐ N/A"
                meta_text = f"{rating_text} • {rec['year']}"

                card_html = f"""
                <div class="rec-card" style="animation-delay:{i * 0.12}s;">
                    <img src="{rec['poster']}" />
                    <div class="rec-title">{html.escape(rec['title'])}</div>
                    <div class="rec-meta">{html.escape(meta_text)}</div>
                    <div class="rec-meta">{html.escape(rec['genres'] or '')}</div>
                    <span class="match-badge">{rec['match']}% Match</span>
                </div>
                """
                st.markdown(card_html, unsafe_allow_html=True)

else:
    st.info("👆 Search and select a movie above to see details and get recommendations.")

# --------------------------------------------------
# Footer
# --------------------------------------------------
st.markdown("""
<div class="app-footer">
    Made with ❤️ by AG using Python • Streamlit • TMDB API • Scikit-Learn
</div>
""", unsafe_allow_html=True)