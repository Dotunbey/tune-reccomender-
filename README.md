
# 🎵 Tune reccomender: AI-Powered Audio Fingerprint Recommender

**TuneTexture** is a full-stack music discovery engine that helps users find "hidden gems" based on sonic texture rather than popularity.

Unlike traditional recommenders (like Spotify's "Fans Also Like") which rely on collaborative filtering (user behavior), TuneTexture analyzes the **mathematical audio fingerprint** of a song—metrics like *danceability*, *valence*, *energy*, and *acousticness*. It uses a **K-Nearest Neighbors (KNN)** machine learning algorithm to find songs that are geometrically closest to your input track in high-dimensional vector space.

## 🚀 Key Engineering Features

* **Local-First Architecture:** Runs entirely on a local **PostgreSQL** instance, bypassing cloud costs and latency.
* **Automated Data Pipeline:** Includes a custom ETL (Extract, Transform, Load) script that programmatically authenticates with the **Kaggle API**, downloads the dataset, cleans it, and seeds the local database automatically.
* **Real-Time Feature Extraction:** Integrates with the **Spotify Web API** to fetch audio features for new songs on-the-fly.
* **In-Memory Machine Learning:** Trains a Scikit-Learn KNN model on server startup for sub-millisecond recommendation latency.

---

## 🛠️ Tech Stack

| Component | Technology | Purpose |
| :--- | :--- | :--- |
| **Frontend** | **Next.js 14 (React)** | Modern, responsive UI with server-side rendering. |
| **Backend** | **FastAPI (Python)** | High-performance asynchronous API. |
| **Database** | **PostgreSQL** | Relational database for storing track metadata. |
| **ORM** | **SQLModel** | Type-safe SQL interaction in Python. |
| **ML Engine** | **Scikit-Learn** | K-Nearest Neighbors implementation. |
| **Data Pipeline**| **Kaggle API + Pandas** | Automated data fetching and cleaning. |

---

## ⚙️ Prerequisites

Before running the project, ensure you have the following installed/set up:

1.  **PostgreSQL:** Installed and running locally. ([Download Here](https://www.postgresql.org/download/))
2.  **Node.js & npm:** For the frontend.
3.  **Python 3.8+:** For the backend and data loader.
4.  **Spotify Developer Account:** You need a Client ID and Secret. ([Dashboard](https://developer.spotify.com/dashboard))
5.  **Kaggle API Token:**
    * Go to Kaggle Settings -> "Create New Token".
    * Place the downloaded `kaggle.json` file in your home directory:
        * **Windows:** `C:\Users\<YourUser>\.kaggle\kaggle.json`
        * **Mac/Linux:** `~/.kaggle/kaggle.json`

---

## 🏁 Installation & Setup

### 1. Clone the Repository
```bash
git clone [https://github.com/YOUR-USERNAME/tune-texture.git](https://github.com/YOUR-USERNAME/tune-texture.git)
cd tune-texture
````

### 2\. Database Setup

1.  Open your terminal or SQL shell (psql).
2.  Create the database:
    ```sql
    CREATE DATABASE tunetexture;
    ```

### 3\. Configure Environment Variables

Create a `.env` file in the **root** directory (or separate ones for backend/loader) with the following credentials:

```env
# Database (Format: postgresql://user:password@localhost:5432/dbname)
DATABASE_URL="postgresql://postgres:password@localhost:5432/tunetexture"

# Spotify Credentials
SPOTIFY_CLIENT_ID="your_spotify_client_id"
SPOTIFY_CLIENT_SECRET="your_spotify_client_secret"
```

### 4\. Run the Automated Data Loader

This script bypasses manual downloads. It uses your Kaggle API token to fetch the 1.2M+ songs dataset, cleans it, samples 50,000 tracks, and bulk-loads them into your local PostgreSQL database.

```bash
cd data_loader
pip install -r requirements.txt
python load_data.py
```

*Wait for the message: "✅ Success\! Local database populated."*

### 5\. Start the Backend Server

The FastAPI server will load the data from SQL and train the KNN model in memory upon startup.

```bash
cd ../backend
pip install -r requirements.txt
uvicorn main:app --reload
```

*Server will run at `http://127.0.0.1:8000`*

### 6\. Start the Frontend

```bash
cd ../frontend
npm install
npm run dev
```

*Open your browser to `http://localhost:3000`*

-----

## 🧠 How the AI Works

1.  **Vectorization:** Every song in the database is represented as a vector $V = [d, e, v, t, a, i]$ where each variable represents a normalized audio feature (0.0 to 1.0).
2.  **Input Processing:** When you search for a song, we fetch its raw features from Spotify and normalize them using the same scaler fitted on our dataset.
3.  **Nearest Neighbors Search:** We use the **Euclidean Distance** metric to find vectors in our database that minimize the distance $D$ to the input vector:
    $$D(x, y) = \sqrt{\sum_{i=1}^{n} (x_i - y_i)^2}$$
4.  **Result:** The system returns the tracks with the smallest $D$ value, guaranteeing they share the same "texture" regardless of genre or popularity.

-----

## 🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## 📜 License

[MIT](https://choosealicense.com/licenses/mit/)

```
```
