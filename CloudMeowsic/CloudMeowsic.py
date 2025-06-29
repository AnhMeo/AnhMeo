import Firestore_Service as fs

def login():
    print("\nLogin to CloudMeowsic")
    user_id = input("Username: ").strip()
    password = input("Password: ").strip()
    if fs.check_user_password(user_id, password):
        print("Logged in successfully.")
        return user_id
    else:
        print("Invalid username or password.")
        return None

def register():
    print("\nRegister for CloudMeowsic")
    user_id = input("Choose a username: ").strip()
    password = input("Choose a password: ").strip()
    success = fs.create_user(user_id, password)
    if success:
        print("Registration successful. You can now log in.")
        return user_id
    else:
        print("Username already exists.")
        return None

def show_menu():
    print("\n🎵 CloudMeowsic Playlist Menu 🎵")
    print("1. Create Playlist")
    print("2. Show Playlists")            
    print("3. View Playlist")             
    print("4. Update Playlist")
    print("5. Delete Playlist")
    print("6. Add Song to Playlist")
    print("7. Remove Song from Playlist")
    print("8. Search Songs")
    print("9. Logout / Exit")


def main():
    user_id = None
    while not user_id:
        print("\nWelcome to CloudMeowsic!")
        print("1. Login")
        print("2. Register")
        print("3. Exit")
        choice = input("Choose an option (1-3): ").strip()
        
        if choice == "1":
            user_id = login()
        elif choice == "2":
            user_id = register()
        elif choice == "3":
            print("Goodbye!")
            return
        else:
            print("Invalid choice. Try again.")

    # Main Playlist Menu
    while True:
        show_menu()
        choice = input("Choose an option (1-8): ").strip()

        if choice == "1":
            name = input("Playlist name: ")
            description = input("Description: ")
            fs.create_playlist(user_id, {"name": name, "description": description, "songs": []})
            print("Playlist created!")

        elif choice == "2":
            print("\nYour Playlists:")
            playlists = fs.get_playlists(user_id)
            for p in playlists:
                data = p.to_dict()
                print(f" {p.id}: {data['name']} - {data['description']} ({len(data.get('songs', []))} songs)")

        elif choice == "3":
            # View playlist: show playlists first, then prompt for ID, then show songs
            print("\nYour Playlists:")
            playlists = fs.get_playlists(user_id)
            playlist_dict = {}
            for p in playlists:
                data = p.to_dict()
                playlist_dict[p.id] = data
                print(f" {p.id}: {data['name']}")

            pid = input("Enter Playlist ID to view songs: ").strip()
            if pid in playlist_dict:
                songs = playlist_dict[pid].get("songs", [])
                if songs:
                    print(f"\nSongs in playlist '{playlist_dict[pid]['name']}':")
                    for idx, song in enumerate(songs, 1):
                        print(f" {idx}. {song['title']} by {song['artist']} [{song['genre']}]")
                else:
                    print("This playlist has no songs.")
            else:
                print("Invalid Playlist ID.")

        elif choice == "4":
            pid = input("Playlist ID to update: ")
            name = input("New name (leave blank to skip): ")
            desc = input("New description (leave blank to skip): ")
            update = {}
            if name:
                update["name"] = name
            if desc:
                update["description"] = desc
            fs.update_playlist(user_id, pid, update)
            print("Playlist updated!")

        elif choice == "5":
            pid = input("Playlist ID to delete: ")
            fs.delete_playlist(user_id, pid)
            print("Playlist deleted.")

        elif choice == "6":
            pid = input("Playlist ID: ")
            title = input("Song Title: ")
            artist = input("Artist: ")
            genre = input("Genre: ")
            fs.add_song_to_playlist(user_id, pid, {"title": title, "artist": artist, "genre": genre})
            print("Song added!")

        elif choice == "7":
            pid = input("Playlist ID: ")
            title = input("Title of song to remove: ")
            fs.remove_song_from_playlist(user_id, pid, title)
            print("Song removed.")

        elif choice == "8":
            keyword = input("Search keyword (title/artist): ")
            results = fs.search_songs(user_id, keyword)
            if results:
                print(f"\nSearch Results for '{keyword}':")
                for r in results:
                    s = r["song"]
                    print(f" {s['title']} by {s['artist']} [{s['genre']}] (Playlist ID: {r['playlist']})")
            else:
                print("No matching songs found.")

        elif choice == "9":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()

