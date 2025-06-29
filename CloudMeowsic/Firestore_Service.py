# Firestore_Service.py

import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firestore
def initialize_firestore():
    try:
        # Only initialize once
        if not firebase_admin._apps:
            cred = credentials.Certificate(r"C:\Users\Ndcat\OneDrive\Desktop\School\SPRING 25\APPLIED_PROGRAMMING_CSE310\CloudMeowsic\cloudmeowsic-firebase-adminsdk-fbsvc-a10b51a338.json")
            firebase_admin.initialize_app(cred)
        return firestore.client()
    except Exception as e:
        print(f"Error initializing Firestore: {e}")
        return None

db = initialize_firestore()

# User functions
def create_user(user_id, password):
    user_ref = db.collection("users").document(user_id)
    if user_ref.get().exists:
        print("User already exists.")
        return False
    else:
        user_ref.set({
            "password": password,
            "created": firestore.SERVER_TIMESTAMP
        })
        print(f"User '{user_id}' created successfully.")
        return True


def check_user_password(user_id, password):
    user_ref = db.collection("users").document(user_id)
    doc = user_ref.get()
    if doc.exists:
        stored_password = doc.to_dict().get("password")
        return stored_password == password
    return False


# Playlist CRUD
def create_playlist(user_id, playlist_data):
    playlists_ref = db.collection('users').document(user_id).collection('playlists')
    playlists = playlists_ref.stream()
    
    max_id = 0
    for playlist in playlists:
        try:
            pid = int(playlist.id)
            if pid > max_id:
                max_id = pid
        except ValueError:
            continue

    new_id = str(max_id + 1)
    
    # Use playlist_data keys directly
    playlists_ref.document(new_id).set({
        'name': playlist_data.get('name'),
        'description': playlist_data.get('description'),
        'songs': playlist_data.get('songs', [])
    })

    print(f"Created playlist '{playlist_data.get('name')}' with ID: {new_id}")


def get_playlists(user_id):
    return db.collection("users").document(user_id).collection("playlists").stream()

def update_playlist(user_id, playlist_id, new_data):
    db.collection("users").document(user_id).collection("playlists").document(playlist_id).update(new_data)

def delete_playlist(user_id, playlist_id):
    db.collection("users").document(user_id).collection("playlists").document(playlist_id).delete()

# Song operations
def add_song_to_playlist(user_id, playlist_id, song_data):
    playlist_ref = db.collection("users").document(user_id).collection("playlists").document(playlist_id)
    playlist = playlist_ref.get()
    if playlist.exists:
        songs = playlist.to_dict().get("songs", [])
        songs.append(song_data)
        playlist_ref.update({"songs": songs})
    else:
        print("Playlist not found.")

def remove_song_from_playlist(user_id, playlist_id, song_title):
    playlist_ref = db.collection("users").document(user_id).collection("playlists").document(playlist_id)
    playlist = playlist_ref.get()
    if playlist.exists:
        songs = playlist.to_dict().get("songs", [])
        songs = [s for s in songs if s.get("title") != song_title]
        playlist_ref.update({"songs": songs})
    else:
        print("Playlist not found.")

# Search
def search_songs(user_id, keyword):
    results = []
    playlists = db.collection("users").document(user_id).collection("playlists").stream()
    for playlist in playlists:
        data = playlist.to_dict()
        for song in data.get("songs", []):
            if keyword.lower() in song["title"].lower() or keyword.lower() in song["artist"].lower():
                results.append({"playlist": playlist.id, "song": song})
    return results
