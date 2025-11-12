# Movie Recommendation System

A Streamlit app that recommends movies based on similarity.

## 🌐 Live Demo

Try the app live: [https://moviereccmenace.streamlit.app/](https://moviereccmenace.streamlit.app/)

## Local Development

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Create a `.env` file with your TMDB API key:
   ```
   API_KEY=your_tmdb_api_key_here
   ```

3. Run the app:
   ```bash
   streamlit run main.py
   ```

## Streamlit Cloud Deployment

1. **Set up API Key in Secrets:**
   - Go to your Streamlit Cloud app dashboard
   - Click on "Manage app" (bottom right)
   - Go to "Secrets" section
   - Add your TMDB API key:
     ```
     API_KEY = "your_tmdb_api_key_here"
     ```

2. **Get TMDB API Key:**
   - Visit https://www.themoviedb.org/
   - Create an account
   - Go to Settings > API
   - Create a new API key
   - Use the "API Read Access Token (v4 auth)"

## Troubleshooting

- If you see "API Key Missing" placeholders, check your secrets configuration
- Make sure your TMDB API key is valid and has read access
- The app uses Git LFS for large model files