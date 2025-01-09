# Spotify Stats Tracker and Music Recommendation System

A Flask-based web application that integrates with the Spotify Web API to provide users with a personalized music experience. This app allows users to log in with their Spotify account, view their top tracks and artists, generate music recommendations, and create playlists directly on Spotify.

---

## Features

### 🎵 User Authentication
- Secure Spotify login using OAuth2.
- Access and refresh tokens managed via Flask sessions.

### 🔝 Top Tracks and Artists
- Fetch and display your top 50 tracks and artists based on your Spotify listening habits.

### 🎧 Music Recommendations
- Generate track recommendations based on:
  - Your top tracks.
  - Your top artists.
- View recommended tracks in an organized format.

### 📜 Playlist Creation
- Create a Spotify playlist from the generated recommendations with a single click.

---

## Technologies Used

- **Backend:** Flask, Python
- **Frontend:** HTML, CSS (with `styles.css`), Jinja2 Templates
- **API Integration:** Spotify Web API
- **Authentication:** OAuth2

---

## Prerequisites

To run this application, ensure you have the following:

1. Python 3.7 or higher.
2. A Spotify Developer account.
3. The following Python libraries installed:
   - Flask
   - python-dotenv
   - requests

---

## Application Workflow

1. Navigate to the home page (`/`) to see the login option.
2. Log in with your Spotify account.
3. Explore the following features:
   - View your top tracks and artists.
   - Generate track and artist-based recommendations.
   - Create a Spotify playlist from the recommendations.

---

## Folder Structure

```
spotify-flask-app/
├── app.py                # Main application entry point
├── routes.py             # Defines app routes and logic
├── spotify.py            # Handles Spotify API interactions
├── templates/            # HTML templates (e.g., index.html, main.html)
├── static/
│   ├── styles.css        # Stylesheet for the application
├── .env                  # Environment variables
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation
```

---

## Demo

[Watch the Demo](https://drive.google.com/file/d/1kGYhOA-ontkkjs66-UU2thPLh9pfpitW/view)

---

## Future Improvements

- Add a feature to allow users to filter recommendations by genre.
- Implement unit tests for API interactions and routes.
- Improve UI/UX with additional styling and animations.
