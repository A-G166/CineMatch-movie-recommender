# 🌌 CineMatch – Movie Recommender System
> *Discover your next favorite movie with Machine Learning.*

CineMatch is a **Machine Learning-powered Content-Based Movie Recommendation System** built using **Python**, **Scikit-Learn**, and **Streamlit**.

Instead of recommending movies based on popularity, CineMatch analyzes a movie's **overview, genres, keywords, cast, and director** to find films with similar content. 
The application features a modern glassmorphism interface, dynamic poster-inspired theming, and real-time movie information fetched from the **TMDB API**.

---

## 🎬 Live Demo

https://cinematch-movie-recommender-jtvotrvpndfgbjpjnmswnw.streamlit.app/

---

## 📸 Preview

<img width="1917" height="870" alt="Screenshot 2026-07-05 205356" src="https://github.com/user-attachments/assets/e82d03f3-5f25-4a30-b468-ca8e5ccfe69f" />

### Home Screen

<img width="1918" height="862" alt="Screenshot 2026-07-05 205518" src="https://github.com/user-attachments/assets/19157943-5958-4d7a-9ebe-3642039533bc" />
<img width="1918" height="867" alt="Screenshot 2026-07-05 205535" src="https://github.com/user-attachments/assets/3db5ac48-ed61-49ae-9ca2-f9dfcee7d08a" />

### Recommendations

<img width="1918" height="862" alt="Screenshot 2026-07-05 205558" src="https://github.com/user-attachments/assets/dae36b5c-72cd-4747-860e-778a2495451d" />

---

# ✨ Features

- 🔍 Search from over **4,800 movies**
- 🎬 Get **5 personalized movie recommendations**
- 🖼️ Live movie posters powered by the **TMDB API**
- ⭐ TMDB movie ratings
- 📅 Release year
- ⏱️ Runtime
- 🎭 Genres
- 🌍 Original language
- 💰 Budget & Revenue information
- 🔥 Popularity score
- 📖 Movie overview
- 🎯 Recommendation Match Percentage
- 🌈 Dynamic poster-inspired background
- 🪟 Modern Glassmorphism UI
- 🌙 Dark Mode support
- ⚡ Fast recommendations using a precomputed similarity matrix

---

# 🧠 How It Works

CineMatch uses a **Content-Based Recommendation System**.

Each movie is represented using information such as:

- Overview
- Genres
- Keywords
- Top Cast
- Director

These features are combined into a single text feature called **tags**.

Example:

```
Avatar

Action Adventure Fantasy
Space
Alien
Sam Worthington
James Cameron
```

The preprocessing pipeline then:

- Cleans and combines movie metadata
- Removes spaces from multi-word names
- Creates a bag-of-words representation using **CountVectorizer**
- Computes similarity between every movie using **Cosine Similarity**

When a movie is selected, CineMatch returns the **five most similar movies** ranked by similarity score.

---

# 🛠️ Tech Stack

## Machine Learning

- Python
- Pandas
- NumPy
- Scikit-Learn
- CountVectorizer
- Cosine Similarity

## Frontend

- Streamlit

## APIs

- TMDB API

## Libraries

- Requests
- Pickle
- ColorThief
- HTML
- AST

---

# 📂 Project Structure

```
CineMatch-movie-recommender
│
├── app.py
├── movieRec.ipynb
├── movies.pkl
├── similarity.pkl
├── tmdb_5000_movies.csv
├── tmdb_5000_credits.csv
├── requirements.txt
├── shrink_similarity.py
├── .gitignore
├── LICENSE
└── README.md
```

---

# 🚀 Installation

Clone the repository

```bash
git clone https://github.com/A-G166/CineMatch-movie-recommender.git
```

Move into the project directory

```bash
cd CineMatch-movie-recommender
```

Install dependencies

```bash
pip install -r requirements.txt
```

Create a `.streamlit` folder and add a `secrets.toml` file.

```toml
TMDB_API_KEY="YOUR_API_KEY"
```

Run the application

```bash
streamlit run app.py
```

---

# 🔑 TMDB API Key

This project uses the **TMDB API** to fetch movie posters.

You can generate a free API key here:

https://www.themoviedb.org/settings/api

Store it inside:

```
.streamlit/secrets.toml
```

```toml
TMDB_API_KEY="YOUR_API_KEY"
```

---

# 📊 Dataset

This project uses the **TMDB 5000 Movie Dataset**, containing:

- 4,800+ Movies
- Genres
- Keywords
- Movie Overviews
- Cast Information
- Crew Information
- Ratings
- Popularity Statistics

---

# 🎨 User Experience

CineMatch was designed to feel more immersive than a traditional recommendation engine.

Features include:

- Poster-inspired dynamic backgrounds
- Smooth glassmorphism cards
- Responsive five-column recommendation layout
- Movie metadata cards
- Loading animations
- Recommendation match badges
- Dark Mode support

---

# 🚀 Future Improvements

- ❤️ Save favourite movies
- 🎥 Watch movie trailers
- 👥 Display full cast information
- 🎭 Search by actor or director
- 🌍 Streaming platform availability
- 🤖 Hybrid recommendation engine
- 🧠 Transformer-based semantic recommendations
- 📱 Mobile-first responsive design
- 🎨 Multiple visual themes
- ☁️ Database-backed user accounts

---

# 📚 What I Learned

This project helped me gain practical experience with:

- Machine Learning fundamentals
- Natural Language Processing (NLP)
- Feature Engineering
- Cosine Similarity
- Recommendation Systems
- API Integration
- Streamlit
- Git & GitHub
- UI/UX Design
- Python Project Structure

---

# 👨‍💻 Author

**Arpitha Ganeshan**

B.Tech Artificial Intelligence

SRM Institute of Science and Technology

GitHub:
https://github.com/A-G166

---

# 🙏 Acknowledgements

- TMDB for providing the movie metadata and poster API.
- The TMDB 5000 Movie Dataset.
- Streamlit for making rapid web application development simple and enjoyable.

---

# 📄 License

This project is licensed under the **MIT License**.
