import tkinter as tk

def on_button_click():
    label.config(text="Hello, Tkinter!")

# Create the main application window
root = tk.Tk()
root.title("Basic Tkinter App")
root.geometry("300x200")

# Create a label
label = tk.Label(root, text="Welcome", font=("Arial", 12))
label.pack(pady=20)

# Create a button
button = tk.Button(root, text="Click Me", command=on_button_click)
button.pack()

# Start the Tkinter event loop
root.mainloop()
