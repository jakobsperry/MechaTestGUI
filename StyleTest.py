import tkinter as tk

class PageManager(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Partial Page Switching")
        self.geometry("500x300")

        # Main container frame
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill="both", expand=True)

        # Left side (Dynamic)
        self.left_frame = tk.Frame(self.main_frame, width=250, height=300, bg="lightgray")
        self.left_frame.pack(side="left", fill="both", expand=True)

        # Right side (Static)
        self.right_frame = tk.Frame(self.main_frame, width=250, height=300, bg="white")
        self.right_frame.pack(side="right", fill="both")

        # Static content in right frame
        tk.Label(self.right_frame, text="Static Right Panel", font=("Arial", 14)).pack(pady=20)

        # Navigation buttons
        btn_frame = tk.Frame(self)
        btn_frame.pack(side="bottom", fill="x")
        tk.Button(btn_frame, text="Settings", command=lambda: self.show_page("Settings")).pack(side="left")
        tk.Button(btn_frame, text="Test", command=lambda: self.show_page("Test")).pack(side="left")
        tk.Button(btn_frame, text="About", command=lambda: self.show_page("About")).pack(side="left")

        # Dictionary to hold dynamic pages
        self.pages = {
            "Settings": SettingsPage(self.left_frame),
            "Test": TestPage(self.left_frame),
            "About": AboutPage(self.left_frame)
        }

        # Show default page
        self.show_page("Settings")

    def show_page(self, page_name):
        """Swap the left-side content with the selected page."""
        for page in self.pages.values():
            page.pack_forget()  # Hide all pages
        self.pages[page_name].pack(fill="both", expand=True)  # Show selected page

# Page Definitions
class SettingsPage():
    def __init__(self, frame, parent):
        
        super().__init__(parent, bg="lightblue")
        tk.Label(self, text="Settings Page", font=("Arial", 14), bg="lightblue").pack(pady=20)

class TestPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="lightgreen")
        tk.Label(self, text="Test Page", font=("Arial", 14), bg="lightgreen").pack(pady=20)

class AboutPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="lightcoral")
        tk.Label(self, text="About Page", font=("Arial", 14), bg="lightcoral").pack(pady=20)

# Run Application
if __name__ == "__main__":
    app = PageManager()
    app.mainloop()
