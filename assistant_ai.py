import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog
from PIL import Image, ImageTk

right_frame = None

def set_right_frame(frame):
    global right_frame
    right_frame = frame

def add_submenus(menu):
    # Création du sous-menu "Traitement fond d'écran"
    menu_traitement_fond_ecran = tk.Menu(menu, tearoff=0)
    menu_traitement_fond_ecran.add_command(label="Traitement par mon propre fond", command=select_image)
    menu_traitement_fond_ecran.add_command(label="Traitement par fond généré", command=open_dialog)
    menu.add_cascade(label="Traitement fond d'écran", menu=menu_traitement_fond_ecran)

    # Création du sous-menu "Traitement couleur vidéo"
    menu_traitement_couleur_video = tk.Menu(menu, tearoff=0)
    menu_traitement_couleur_video.add_command(label="Traitement automatique", command=traitement_automatique)
    menu_traitement_couleur_video.add_command(label="Traitement par thème", command=theme_video)
    menu.add_cascade(label="Traitement couleur vidéo", menu=menu_traitement_couleur_video)

def select_image():
    global right_frame
    # Ouvrir une boîte de dialogue de sélection de fichiers
    file_path = filedialog.askopenfilename(filetypes=[("Images", "*.png;*.jpg;*.jpeg")])

    if file_path:
        # Ouvrir l'image avec Pillow
        img = Image.open(file_path)

        # Redimensionner l'image si nécessaire
        max_size = (300, 300)
        img.thumbnail(max_size, Image.Resampling.LANCZOS)

        img_tk = ImageTk.PhotoImage(img)

        canvas = ctk.CTkCanvas(master=right_frame, width=640, height=480)
        canvas.pack(padx=10, pady=10)


        canvas.create_image(280, 240, image=img_tk, anchor="center")
        canvas.image = img_tk

def open_dialog():
    # Création d'une boîte de dialogue personnalisée avec customtkinter
    dialog = ctk.CTkToplevel()
    dialog.geometry("200x200")
    dialog.title("Fond à générer")

    label = ctk.CTkLabel(dialog, text="Entrez le type de fond désiré")
    label.pack(pady=10)
    entry = ctk.CTkEntry(dialog)
    entry.pack(pady=10)

    button = ctk.CTkButton(dialog, text="OK", command=lambda: dialog.destroy())
    button.pack(pady=10)

    dialog.mainloop()

def traitement_automatique():
    pass

def theme_video():
    dialog = ctk.CTkToplevel()
    dialog.geometry("200x200")
    dialog.title("Thème à générer")

    label = ctk.CTkLabel(dialog, text="Entrez le thème souhaité")
    label.pack(pady=10)
    entry = ctk.CTkEntry(dialog)
    entry.pack(pady=10)

    button = ctk.CTkButton(dialog, text="OK", command=lambda: dialog.destroy())
    button.pack(pady=10)

    dialog.mainloop()
