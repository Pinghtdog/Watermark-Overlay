# gui_app.py

import customtkinter as ctk
from tkinter import filedialog, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
from PIL import Image
import os

# Import the image processing function from our other file
from image_processor import add_overlay

class App(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        self.title("Image Overlay App")
        self.geometry("800x600")

        self.overlay_image = None
        self.overlay_filepath = ""

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.settings_frame = ctk.CTkFrame(self)
        self.settings_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        
        self.file_list_frame = ctk.CTkFrame(self)
        self.file_list_frame.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nsew")

        self.action_frame = ctk.CTkFrame(self)
        self.action_frame.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        self.setup_settings_widgets()
        self.setup_file_list_widgets()
        self.setup_action_widgets()

        self.drop_target_register(DND_FILES)
        self.dnd_bind('<<Drop>>', self.handle_drop)

    def setup_settings_widgets(self):
        self.settings_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)
        self.overlay_button = ctk.CTkButton(self.settings_frame, text="Select Overlay Image", command=self.select_overlay)
        self.overlay_button.grid(row=0, column=0, padx=10, pady=10)
        self.overlay_label = ctk.CTkLabel(self.settings_frame, text="No overlay selected", wraplength=150)
        self.overlay_label.grid(row=0, column=1, padx=10, pady=10)
        ctk.CTkLabel(self.settings_frame, text="Position:").grid(row=0, column=2, padx=(20, 5), pady=10, sticky="e")
        self.position_var = ctk.StringVar(value="bottom-right")
        self.position_menu = ctk.CTkOptionMenu(self.settings_frame, values=["bottom-right", "bottom-left", "top-right", "top-left", "center"], variable=self.position_var)
        self.position_menu.grid(row=0, column=3, padx=(0, 10), pady=10, sticky="w")
        ctk.CTkLabel(self.settings_frame, text="Scale:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.scale_slider = ctk.CTkSlider(self.settings_frame, from_=0.05, to=1.0, command=lambda v: self.scale_label.configure(text=f"{int(v*100)}%"))
        self.scale_slider.set(0.25)
        self.scale_slider.grid(row=1, column=1, columnspan=2, padx=10, pady=10, sticky="ew")
        self.scale_label = ctk.CTkLabel(self.settings_frame, text="25%")
        self.scale_label.grid(row=1, column=3, padx=10, pady=10, sticky="w")
        ctk.CTkLabel(self.settings_frame, text="Padding:").grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.padding_slider = ctk.CTkSlider(self.settings_frame, from_=0.0, to=0.2, command=lambda v: self.padding_label.configure(text=f"{int(v*100)}%"))
        self.padding_slider.set(0.02)
        self.padding_slider.grid(row=2, column=1, columnspan=2, padx=10, pady=10, sticky="ew")
        self.padding_label = ctk.CTkLabel(self.settings_frame, text="2%")
        self.padding_label.grid(row=2, column=3, padx=10, pady=10, sticky="w")

    def setup_file_list_widgets(self):
        self.file_list_frame.grid_rowconfigure(0, weight=1)
        self.file_list_frame.grid_columnconfigure(0, weight=1)
        self.scrollable_list = ctk.CTkScrollableFrame(self.file_list_frame, label_text="Images to Process")
        self.scrollable_list.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.file_labels = []

        self.drop_label = ctk.CTkLabel(self.scrollable_list, text="Drag & Drop Images Here\nor\nClick 'Select Images' below", font=("", 20))
        self.drop_label.pack(expand=True, padx=20, pady=50)

    def setup_action_widgets(self):
        self.action_frame.grid_columnconfigure((0, 1, 2), weight=1)
        self.select_files_button = ctk.CTkButton(self.action_frame, text="Select Images", command=self.select_files)
        self.select_files_button.grid(row=0, column=0, padx=10, pady=10)
        self.clear_button = ctk.CTkButton(self.action_frame, text="Clear List", command=self.clear_list)
        self.clear_button.grid(row=0, column=1, padx=10, pady=10)
        self.process_button = ctk.CTkButton(self.action_frame, text="Apply Overlays", command=self.start_processing, fg_color="green", hover_color="dark green")
        self.process_button.grid(row=0, column=2, padx=10, pady=10)
        self.progress_bar = ctk.CTkProgressBar(self.action_frame)
        self.progress_bar.set(0)
        self.progress_bar.grid(row=1, column=0, columnspan=3, padx=10, pady=(0, 10), sticky="ew")
        self.status_label = ctk.CTkLabel(self.action_frame, text="Ready")
        self.status_label.grid(row=2, column=0, columnspan=3, padx=10, pady=(0, 10))

    def _add_files_to_list(self, filepaths):
        self.drop_label.pack_forget()
        current_files = [label.cget("text") for label in self.file_labels]
        for f in filepaths:
            if f not in current_files:
                label = ctk.CTkLabel(self.scrollable_list, text=f)
                label.pack(anchor="w", padx=5)
                self.file_labels.append(label)

    def select_overlay(self):
        filepath = filedialog.askopenfilename(title="Select an Overlay Image", filetypes=[("Image Files", "*.png *.jpg *.jpeg *.bmp *.gif")])
        if filepath:
            try:
                self.overlay_image = Image.open(filepath).convert("RGBA")
                self.overlay_filepath = filepath
                self.overlay_label.configure(text=os.path.basename(filepath))
            except Exception as e:
                messagebox.showerror("Error", f"Could not open overlay image:\n{e}")

    def select_files(self):
        filepaths = filedialog.askopenfilenames(title="Select Base Images", filetypes=[("Image Files", "*.png *.jpg *.jpeg")])
        if filepaths:
            self._add_files_to_list(filepaths)

    def handle_drop(self, event):
        filepaths = self.tk.splitlist(event.data)
        if filepaths:
            self._add_files_to_list(filepaths)
    
    def clear_list(self):
        for label in self.file_labels:
            label.destroy()
        self.file_labels.clear()
        self.drop_label.pack(expand=True, padx=20, pady=50)
        self.status_label.configure(text="Ready")
        self.progress_bar.set(0)

    def start_processing(self):
        if not self.overlay_image:
            messagebox.showerror("Error", "Please select an overlay image first.")
            return
        image_paths = [label.cget("text") for label in self.file_labels]
        if not image_paths:
            messagebox.showerror("Error", "Please add some images to process.")
            return
        output_dir = filedialog.askdirectory(title="Select a Folder to Save the Output")
        if not output_dir:
            return

        position = self.position_var.get()
        scale = self.scale_slider.get()
        padding = self.padding_slider.get()
        total_images = len(image_paths)
        
        self.progress_bar.set(0)
        for i, path in enumerate(image_paths):
            self.status_label.configure(text=f"Processing {i+1}/{total_images}: {os.path.basename(path)}")
            self.update_idletasks()

            filename, ext = os.path.splitext(os.path.basename(path))
            output_filename = f"{filename}_with_overlay.png"
            output_path = os.path.join(output_dir, output_filename)
            
            # Here we call the imported function
            success, error_msg = add_overlay(path, self.overlay_image, output_path, position, scale, padding)
            
            if not success:
                print(f"Failed to process {path}: {error_msg}")
            self.progress_bar.set((i + 1) / total_images)

        self.status_label.configure(text=f"Done! {total_images} images saved to {output_dir}")
        messagebox.showinfo("Success", f"All {total_images} images have been processed successfully!")