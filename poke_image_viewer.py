import tkinter as tk
from tkinter import ttk
import poke_api
import image_lib

def main():
    global img_label, set_button  # Make these global to access them in other functions

    root = tk.Tk()
    root.title('Pokémon Image Viewer')

    # Frame for the Combobox and button
    frame = ttk.Frame(root, padding="10")
    frame.grid(row=0, column=0, sticky=(tk.W, tk.E))

    # Combobox for Pokémon selection
    pokemon_names = poke_api.get_pokemon_names()
    pokemon_combobox = ttk.Combobox(frame, values=pokemon_names, state='readonly')
    pokemon_combobox.grid(row=0, column=0, sticky=(tk.W, tk.E))
    pokemon_combobox.bind("<<ComboboxSelected>>", on_pokemon_selected)

    # Button to set the desktop image
    set_button = ttk.Button(frame, text="Set as Desktop Image", command=set_as_desktop_image, state=tk.DISABLED)
    set_button.grid(row=1, column=0, sticky=(tk.W, tk.E))

    # Label to display the image
    img_label = tk.Label(root)
    img_label.grid(row=1, column=0, padx=10, pady=10)

    root.mainloop()

def on_pokemon_selected(event):
    global img_label, set_button  # Access global variables

    pokemon_name = event.widget.get()
    img_path = poke_api.download_pokemon_artwork(pokemon_name, 'images')
    if img_path:
        img = tk.PhotoImage(file=img_path)
        img_label.config(image=img)
        img_label.image = img  # Prevent garbage collection
        img_label.image_path = img_path  # Store the path for setting as wallpaper
        set_button.config(state=tk.NORMAL)

def set_as_desktop_image():
    if hasattr(img_label, 'image_path'):
        image_lib.set_desktop_background_image(img_label.image_path)
        return 

if __name__ == '__main__':
    main()
