import customtkinter
from PIL import Image
import os
import webbrowser

class ProductCard(customtkinter.CTkFrame):
    def __init__(self, master, content, image_cache=None, **kwargs):
        super().__init__(master, **kwargs)
        self.content = content
        self.image_cache = image_cache
        
        # Style configuration
        self.configure(fg_color=("white", "#2b2b2b"), corner_radius=10, border_width=1, border_color=("gray80", "gray40"))
        
        # Layout
        self.grid_columnconfigure(1, weight=1) # Title column expands
        
        # Data extraction
        self.title_text = str(content.get('title', 'N/A'))
        
        # Price & Currency
        price_val = content.get('price', 'N/A')
        currency = content.get('currency_code', '€') # Default to Euro if missing
        # If price is a number, format it. If string, just use it.
        # Wallapop often sends price as number.
        if isinstance(price_val, (int, float)):
             self.price_text = f"{price_val['amount']} {currency}"
        else:
             self.price_text = f"{price_val['amount']} {currency}"

        self.web_slug = content.get('web_slug', '')
        
        # Reserved Status
        # Check various possible keys for reservation
        self.is_reserved = content.get('reserved', False)["flag"] 
        if self.is_reserved:         
            self.is_reserved = True

        # Ideally, we pass the full image path or handle the construction outside. 
        # But for now, I'll stick to what was there or improve it. 
        # The previous code used: os.path.join(Constants.Temp_folder, item_content['web_slug'] + ".jpg")
        # I will let the caller handle the full path logic or pass it in 'content' if I modify the caller.
        # Actually, let's keep it simple: caller passes the full image path in a new key or I calculate it if I have Constants.
        
        # Let's assume the caller will pass the calculated image_path in 'content' or I import Constants.
        # Importing Constants here is safer.
        from constants import Constants
        self.full_image_path = os.path.join(Constants.Temp_folder, self.web_slug + ".jpg")

        # --- Image ---
        self.image_label = customtkinter.CTkLabel(self, text="", width=100, height=100)
        self.image_label.grid(row=0, column=0, rowspan=4, padx=10, pady=10) # Increased rowspan for badge
        
        self._load_image()

        # --- Title ---
        self.title_label = customtkinter.CTkLabel(
            self, 
            text=self.title_text, 
            font=customtkinter.CTkFont(size=14, weight="bold"),
            anchor="w",
            wraplength=300 
        )
        self.title_label.grid(row=0, column=1, sticky="nw", padx=(0, 10), pady=(10, 0))

        # --- Price ---
        self.price_label = customtkinter.CTkLabel(
            self, 
            text=self.price_text, 
            font=customtkinter.CTkFont(size=16, weight="bold"),
            text_color=("green", "#2cc985"), 
            anchor="w"
        )
        self.price_label.grid(row=1, column=1, sticky="w", padx=(0, 10), pady=(0, 0))

        # --- Reserved Badge ---
        if self.is_reserved:
            self.reserved_label = customtkinter.CTkLabel(
                self,
                text="RESERVED",
                font=customtkinter.CTkFont(size=12, weight="bold"),
                text_color="white",
                fg_color="#e04f5f", # Reddish color
                corner_radius=5,
                width=80
            )
            self.reserved_label.grid(row=2, column=1, sticky="w", padx=(0, 10), pady=(2, 2))
            
            # Action button moves down
            button_row = 3
        else:
            button_row = 2

        # --- Action Button ---
        self.open_button = customtkinter.CTkButton(
            self, 
            text="Open", 
            width=80, 
            height=30,
            command=self._open_url
        )
        self.open_button.grid(row=button_row, column=1, sticky="se", padx=10, pady=10)

        # Make the whole card clickable (optional)
        # self.bind("<Button-1>", lambda e: self._open_url())
        # self.title_label.bind("<Button-1>", lambda e: self._open_url())
        
    def _load_image(self):
        if self.image_cache is not None and self.web_slug in self.image_cache:
            self.image_label.configure(image=self.image_cache[self.web_slug])
            return

        if os.path.exists(self.full_image_path):
            try:
                pil_image = Image.open(self.full_image_path)
                ctk_image = customtkinter.CTkImage(pil_image, size=(100, 100))
                self.image_label.configure(image=ctk_image)
                
                if self.image_cache is not None:
                    self.image_cache[self.web_slug] = ctk_image
            except Exception as e:
                print(f"Error loading image {self.full_image_path}: {e}")
                self.image_label.configure(text="No Image")
        else:
            self.image_label.configure(text="No Image")

    def _open_url(self):
        url = "https://es.wallapop.com/item/" + self.web_slug
        webbrowser.open_new(url)
