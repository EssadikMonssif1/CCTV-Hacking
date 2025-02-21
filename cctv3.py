# Copyright (c) 2025 Monssif Essadik
# Tous droits réservés.
# Ce code est protégé contre la modification non autorisée.
# Toute tentative de modification peut altérer son fonctionnement.

import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import cv2
import threading
import webbrowser


# Dictionnaire des pays et de leurs codes
countries = {
    "United States": "US", "Japan": "JP", "Italy": "IT", "Germany": "DE", 
    "Russian Federation": "RU", "France": "FR", "Austria": "AT", "Norway": "NO", 
    "Czech Republic": "CZ", "United Kingdom": "GB", "Switzerland": "CH", 
    "Korea, Republic Of": "KR", "Taiwan, Province Of": "TW", "Canada": "CA", 
    "Poland": "PL", "Spain": "ES", "Romania": "RO", "Sweden": "SE", "Netherlands": "NL", 
    "Bulgaria": "BG", "Viet Nam": "VN", "Denmark": "DK", "Belgium": "BE", "Serbia": "RS", 
    "Brazil": "BR", "Finland": "FI", "Hungary": "HU", "India": "IN", "Indonesia": "ID", 
    "South Africa": "ZA", "Greece": "GR", "Slovakia": "SK", "Ukraine": "UA", 
    "Ireland": "IE", "Turkey": "TR", "Mexico": "MX", "Bosnia And Herzegovina": "BA", 
    "Iran, Islamic Republic": "IR", "Israel": "IL", "Chile": "CL", "Hong Kong": "HK", 
    "Argentina": "AR", "Syria": "SY", "Thailand": "TH", "Slovenia": "SI", "Lithuania": "LT", 
    "Australia": "AU", "Moldova, Republic Of": "MD", "Ecuador": "EC", "Estonia": "EE", 
    "New Zealand": "NZ", "Belarus": "BY", "Croatia": "HR", "China": "CN", "Malaysia": "MY", 
    "Tanzania": "TZ", "Kazakhstan": "KZ", "Faroe Islands": "FO", "Honduras": "HN", 
    "Colombia": "CO", "Peru": "PE", "Armenia": "AM", "Nicaragua": "NI", "Portugal": "PT", 
    "Montenegro": "ME", "Guernsey": "GG", "Lebanon": "LB", "Trinidad And Tobago": "TT", 
    "New Caledonia": "NC", "Bangladesh": "BD", "Nigeria": "NG", "Latvia": "LV", 
    "Luxembourg": "LU", "Georgia": "GE", "Philippines": "PH", "Iceland": "IS", "Angola": "AO", 
    "Laos": "LA", "Tunisia": "TN"
}


favorites = []  # Liste pour stocker les caméras préférées

def fetch_data():
    country_name = country_combobox.get()
    if country_name not in countries:
        messagebox.showerror("Erreur", "Veuillez sélectionner un pays valide.")
        return
    
    country_code = countries[country_name]
    url = f"http://www.insecam.org/en/bycountry/{country_code}/"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        messagebox.showerror("Erreur", f"Impossible de récupérer les données. Code: {response.status_code}")
        return
    
    soup = BeautifulSoup(response.text, "lxml")
    cameras = soup.find_all('img', {'class': 'thumbnail-item__img img-responsive'})
    
    results_text.delete(1.0, tk.END)  
    for camera in cameras:
        src = camera.get('src')
        title = camera.get('title')
        results_text.insert(tk.END, f"📌 {title}\n🔗 {src}\n")
        results_text.insert(tk.END, "⭐ Ajouter aux favoris\n", "favorite")
        results_text.tag_bind("favorite", "<Button-1>", lambda e, url=src: add_to_favorites(url))
        results_text.insert(tk.END, "\n")

def add_to_favorites(url):
    if url not in favorites:
        favorites.append(url)
        messagebox.showinfo("Favoris", "Caméra ajoutée aux favoris!")

def open_favorites():
    if not favorites:
        messagebox.showinfo("Favoris", "Aucune caméra enregistrée.")
        return
    results_text.delete(1.0, tk.END)
    results_text.insert(tk.END, "📌 Caméras Favorites:\n\n")
    for url in favorites:
        results_text.insert(tk.END, f"🔗 {url}\n")

import threading
import cv2
from tkinter import messagebox

# Variable globale pour contrôler le thread
camera_running = False

def open_camera():
    try:
        url = results_text.get(tk.SEL_FIRST, tk.SEL_LAST).strip()  # Get selected text
        if url.startswith("http"):
            global camera_running
            camera_running = True  # Démarre la caméra
            threading.Thread(target=stream_camera, args=(url,), daemon=True).start()
        else:
            messagebox.showerror("Erreur", "Sélectionnez un lien valide.")
    except tk.TclError:  # Handle case where no text is selected
        messagebox.showerror("Erreur", "Veuillez sélectionner un lien valide.")



def stream_camera(url):
    global camera_running
    cap = cv2.VideoCapture(url)

    if not cap.isOpened():
        messagebox.showerror("Erreur", "Impossible d'ouvrir le flux vidéo.")
        return

    cv2.namedWindow("Live Camera", cv2.WINDOW_NORMAL)
    
    while camera_running:
        ret, frame = cap.read()
        if not ret:
            messagebox.showerror("Erreur", "Impossible de lire le flux vidéo.")
            break
        
        cv2.imshow("Live Camera", frame)
        
        # Vérifie si 'q' est pressé pour fermer
        if cv2.waitKey(1) & 0xFF == ord('q'):
            close_camera()
            break

    cap.release()
    cv2.destroyAllWindows()

def close_camera():
    global camera_running
    camera_running = False  # Stop the loop
    cv2.destroyAllWindows()  # Ensure OpenCV window closes

def open_map():
    latitude = 40.748817  # Exemple de latitude (ici, pour l'Empire State Building à New York)
    longitude = -73.985428  # Exemple de longitude
    url = f"https://www.google.com/maps?q={latitude},{longitude}"
    webbrowser.open(url)




root = tk.Tk()
root.title("Camera Surveillance by Country")
root.geometry("800x600")

style = ttk.Style()
style.configure("TButton", font=("Helvetica", 12), padding=5)


try:
    header_image = Image.open("cctv.png").resize((250, 150))
    header_image = ImageTk.PhotoImage(header_image)
    header_label = tk.Label(root, image=header_image, bg="#f7f7f7")
    header_label.pack(pady=5)
except:
    header_label = tk.Label(root, text="📡 Sélectionnez un pays", font=("Helvetica", 18), fg="black", bg="#f7f7f7")
    header_label.pack(pady=5)

country_combobox = ttk.Combobox(root, values=list(countries.keys()), width=30, font=("Helvetica", 12))
country_combobox.pack(pady=5)
country_combobox.set("Select Country")

search_button = ttk.Button(root, text="🔍 Rechercher", command=fetch_data)
search_button.pack(pady=5)



results_text = tk.Text(root, height=15, width=80, font=("Helvetica", 10))
results_text.pack(pady=10)

view_button = ttk.Button(root, text="📺 Voir Caméra", command=open_camera)
view_button.pack(pady=5)

favorite_button = ttk.Button(root, text="⭐ Voir Favoris", command=open_favorites)
favorite_button.pack(pady=5)

map_button = ttk.Button(root, text="📍 Localiser sur Carte", command=open_map)
map_button.pack(pady=5)

root = tk.Tk()
root.withdraw()  # Cache la fenêtre principale
messagebox.showinfo(
    "Copyright",
    "© 2025 Monssif Essadik\n"
)


root.mainloop()



