import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from contours_vers_son import sonifier, to_piano_wav
from couleurs_vers_son import histogramme_couleur, colors_to_wav_file
import os

class Fenetre(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("450x450")
        self.title("Sonification")
        self.image_pil =  None 
        self.photo_image = None 
        self.midi_output = 'image_musique.mid'
        self.color_midi = print('nommanquant')
        self.color_wav = 'chord.wav'
        self.wav_output = 'ouput.wav'
        self.var_plot = tk.BooleanVar()
        
        # Bouton pour charger une image
        self.bouton_charger = tk.Button(self,text="Charger une image", command=self.charger_image, width=13)
        self.bouton_charger.place(x=0, y=0)

        # Bouton pour lancer la sonification
        self.bouton_sonifier = tk.Button(self, text="Sonifier Contours", command=self.sonifier_image, state=tk.DISABLED, width=13)
        self.bouton_sonifier.place(x=0,y=30)

        

        # Bouton pour jouer le son
        self.bouton_jouer = tk.Button(self, text="Jouer Contours", command=self.play, state=tk.DISABLED, width=13)
        self.bouton_jouer.place(x=0,y=60)

        # Bouton pour ajouter couleur
        self.bouton_couleur = tk.Button(self, text="Sonifier Couleurs", command=self.couleur, state=tk.DISABLED, width=13)
        self.bouton_couleur.place(x=0, y=90)

        #Bouton pour jouer couleurs
        self.bouton_jouer_couleur = tk.Button(self, text="Jouer Couleurs", command=self.playcolor, state=tk.DISABLED, width=13)
        self.bouton_jouer_couleur.place(x=0, y=120)

        # Checkbox pour afficher ou non les graphes
        self.plot_box = tk.Checkbutton(self, text="Afficher graphes", variable=self.var_plot, onvalue=True, offvalue=False)
        self.plot_box.place(x=0, y=150)

        
        self.label_image = tk.Label(self)
        self.label_image.place(x=150,y=0)



    def charger_image(self):
        filepath = filedialog.askopenfilename(filetypes=[("Images", "*.png *.jpg *.jpeg *.bmp")])
        if filepath:
            self.image_pil = Image.open(filepath).convert("RGB") 
            image_redim = self.image_pil.resize((300, 300))
            self.photo_image = ImageTk.PhotoImage(image_redim)
            self.label_image.config(image=self.photo_image)
            self.bouton_sonifier.config(state=tk.NORMAL)
            self.bouton_couleur.config(state=tk.NORMAL)
    
    def sonifier_image(self):
        sonifier(self.image_pil.convert('L'), self.var_plot.get())
        to_piano_wav(self.midi_output, self.wav_output)
        self.bouton_jouer.config(state=tk.NORMAL)

    def couleur(self): 
        histo = histogramme_couleur(self.image_pil, self.var_plot.get())
        colors_to_wav_file(histo, self.color_wav)
        self.bouton_jouer_couleur.config(state=tk.NORMAL)

    def playcolor(self):
        os.system(f"aplay -q {self.color_wav}")

    def play(self):
        os.system(f"aplay -q {self.wav_output}")
        

if __name__=="__main__":

    app = Fenetre()
    app.mainloop()
