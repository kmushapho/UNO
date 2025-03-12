import tkinter as tk

def close_popup():
    popup.destroy()  # Close the popup window

# Create the main window
root = tk.Tk()
root.withdraw()  # Hide the main window (optional, if you only want the pop-up)

# Create a pop-up window
popup = tk.Toplevel(root)
popup.title("Auto-close Pop-up")

# Add a label or other widgets to the pop-up
label = tk.Label(popup, text="This window will close in 3 seconds")
label.pack(padx=20, pady=20)

# Call the close_popup function after 3000 milliseconds (3 seconds)
popup.after(3000, close_popup)

# Start the Tkinter event loop
root.mainloop()
