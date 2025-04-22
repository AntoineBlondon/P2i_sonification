import tkinter as tk 
from tkinter import filedialog
from PIL import Image, ImageTk


class Fenetre(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("450x300")
        self.title("Sonification")
        self.image_pil =  None 
        self.photo_image = None 
        
        self.bouton_charger = tk.Button(self,text="Charger une image", command=self.charger_image)
        self.bouton_charger.pack(pady=10)
        
        self.label_image = tk.Label(self)
        self.label_image.pack()

        # Bouton pour lancer la sonification
        # self.bouton_sonifier = tk.Button(self, text=" ( Sonifier", command=self.sonifier_image, state=tk.DISABLED)
        # self.bouton_sonifier.pack(pady=10)

    def charger_image(self):
        filepath = filedialog.askopenfilename(filetypes=[("Images", "*.png *.jpg *.jpeg *.bmp")])
        if filepath:
            self.image_pil = Image.open(filepath).convert("L")  # Convertir en niveaux de gris
            image_redim = self.image_pil.resize((300, 300))
            self.photo_image = ImageTk.PhotoImage(image_redim)
            self.label_image.config(image=self.photo_image)
            self.bouton_sonifier.config(state=tk.NORMAL)

if __name__=="__main__":

    app = Fenetre()
    app.mainloop()
