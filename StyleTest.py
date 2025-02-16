import tkinter as tk
from tkinter import ttk

def on_button_click():
    """Change the window background and display an excited message when clicked!"""
    # Change the background color to something exciting!
    root.config(bg='yellow')
    message_label.config(text="WOW! You clicked the button!! 🎉🎉🎉", fg="red", font=("Helvetica", 18, "bold"))
    button.config(state=tk.DISABLED)  # Disable the button once clicked

    # Let's change the window size to make it feel more grand!
    root.geometry("500x500")

    # Show a message box with excitement!
    print("🎉🎉🎉 YOU DID IT! 🎉🎉🎉")

root = tk.Tk()
root.title("Excitement Central 🚀")

# Set the initial size of the window
root.geometry("400x400")

# Create a label that will display the excited message
message_label = ttk.Label(root, text="Welcome to the Excitement Zone!", font=("Helvetica", 16), anchor="center")
message_label.pack(pady=50)

# Create a style object to make the button taller and change its appearance
style = ttk.Style()
style.configure("TButton", font=("Helvetica", 16), padding=(20, 30))  # Adjust padding for height

# Create the button that will trigger excitement! Now taller!
button = ttk.Button(root, text="Click me for fun!", command=on_button_click, style="TButton")
button.pack(pady=20)

# Start the main event loop
root.mainloop()
