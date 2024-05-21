import tkinter as tk
import customtkinter as ctk
from tkinter import filedialog, ttk
import assistant_ai
import cv2
from PIL import Image, ImageTk

def select_video(left_frame):
    
    file_path = filedialog.askopenfilename(filetypes=[("Vidéos", "*.mp4;*.avi;*.mkv")])

    if file_path:
        # Ceci permet de Lire la vidéo sélectionnée avec OpenCV
        cap = cv2.VideoCapture(file_path)

   
        canvas = tk.Canvas(master=left_frame, width=640, height=480)
        canvas.pack(padx=10, pady=10)

        def update_frame():
            ret, frame = cap.read()

            if ret:
                
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame_image = Image.fromarray(frame)

                # Redimensionner l'image pour s'adapter au canvas tout en conservant les proportions
                canvas_width = 640
                canvas_height = 480
                frame_image.thumbnail((canvas_width, canvas_height), Image.Resampling.LANCZOS)
                frame_photo = ImageTk.PhotoImage(frame_image)

                # Centrer l'image dans le canvas
                canvas.create_image(canvas_width/2, canvas_height/2, image=frame_photo, anchor="center")
                canvas.image = frame_photo  # Sauvegarde de la référence

                # Appeler la fonction update_frame() à nouveau après 30 ms
                left_frame.after(30, update_frame)
            else:
                # Libérer la mémoire occupée par la vidéo
                cap.release()

        # Appeler la fonction update_frame() pour la première fois
        update_frame()

def create_new_project():
    # Supprimer tous les widgets actuels dans main_frame
    for widget in main_frame.winfo_children():
        widget.destroy()

    top_frame = ctk.CTkFrame(master=main_frame, fg_color="#9eb9f2", border_width=10, border_color="black")
    bottom_frame = ctk.CTkFrame(master=main_frame, fg_color="#9eb9f2")

    separator = ttk.Separator(master=main_frame, orient="horizontal")

    top_frame.pack(side="top", fill="both", expand=True, padx=10, pady=10)
    separator.pack(side="top", fill="x", padx=10)
    bottom_frame.pack(side="bottom", fill="both", expand=True, padx=10, pady=10)


    top_frame.grid_columnconfigure(0, weight=1)
    top_frame.grid_columnconfigure(1, weight=1)
    top_frame.grid_rowconfigure(0, weight=1)


    left_frame = ctk.CTkFrame(master=top_frame, fg_color="#9eb9f2", width=300, height=250)
    right_frame = ctk.CTkFrame(master=top_frame, fg_color="green", width=300, height=250)


    select_button = ctk.CTkButton(master=left_frame, text="Sélectionner une vidéo", command=lambda: select_video(left_frame))
    select_button.pack(side="top", padx=10, pady=10)


    left_frame.grid(row=0, column=0, padx=5, pady=5)
    right_frame.grid(row=0, column=1, padx=5, pady=5)

    toggle_button = ctk.CTkButton(master=left_frame, text="X", command=lambda: toggle_right_frame(right_frame))
    toggle_button.pack(side="bottom", padx=3, pady=5)

    label = ctk.CTkLabel(master=bottom_frame, text="Rendu final", font=("TkDefaultFont", 10, "bold"), fg_color="#d9d9d9")
    label.place(x=0, y=0)


    assistant_ai.set_right_frame(right_frame)

def toggle_right_frame(right_frame):
    # Masquer le right_frame s'il est affiché, ou l'afficher s'il est masqué
    if right_frame.winfo_ismapped():
        right_frame.grid_forget()
    else:
        right_frame.grid(row=0, column=1, padx=5, pady=5)

app = ctk.CTk()
app.geometry("1300x700")
app.title("VideAi")
app.resizable(width=True, height=True)

main_frame = ctk.CTkFrame(master=app, fg_color="#9eb9f2")
main_frame.pack(fill="both", expand=True)


# Charger l'image du logo
logo_image = Image.open("images/logo.png")  # Remplacer par le chemin de votre image
logo_image = logo_image.resize((200, 200), Image.Resampling.LANCZOS)  # Redimensionner si nécessaire
logo_photo = ImageTk.PhotoImage(logo_image)

# Créer un label pour afficher l'image du logo
logo_label = tk.Label(main_frame, image=logo_photo, bg="#9eb9f2")
logo_label.image = logo_photo  # Sauvegarder une référence à l'image pour éviter le garbage collection
logo_label.place(relx=0.5, rely=0.5, anchor="center")

# ça,  c'est pour le menu qu'on l'a.
menu_bar = tk.Menu(app)

# Création du menu "Fichier"
menu_fichier = tk.Menu(menu_bar, tearoff=0)
menu_fichier.add_command(label="Enregistrer")
menu_fichier.add_command(label="Nouveau projet", command=create_new_project)
menu_fichier.add_separator()
menu_fichier.add_command(label="Quitter", command=app.quit)
menu_bar.add_cascade(label="Fichier", menu=menu_fichier)

# Création du menu "Assistant IA"
menu_assistant_ia = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Assistant IA", menu=menu_assistant_ia)

# Ajout des sous-menus de l'assistant IA
assistant_ai.add_submenus(menu_assistant_ia)

# Création du menu "A propos"
menu_a_propos = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="A propos", menu=menu_a_propos)

# Affectation du menu bar à l'application
app.config(menu=menu_bar)

app.mainloop()
