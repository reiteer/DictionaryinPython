import tkinter as tk
from tkinter import messagebox
import requests
from tkinter import ttk

def get_word_definition(word):
    api_url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    response = requests.get(api_url)

    if response.status_code == 200:
        data = response.json()
        verb_definitions = []
        noun_definitions = []
        for entry in data:
            word = entry["word"]
            for meaning in entry["meanings"]:
                part_of_speech = meaning["partOfSpeech"]
                definition = meaning["definitions"][0]["definition"]
                if part_of_speech.lower() == "verb":
                    verb_definitions.append(definition)
                elif part_of_speech.lower() == "noun":
                    noun_definitions.append(definition)
        return {
            "Verbs": verb_definitions if verb_definitions else ["No verbs found"],
            "Nouns": noun_definitions if noun_definitions else ["No nouns found"]
        }
    elif response.status_code == 404:
        return "Word not found"
    else:
        return f"Error fetching data for '{word}'"

def display_definition(event=None):
    word = entry.get().strip()
    if word:
        results = get_word_definition(word)
        if isinstance(results, str):
            output_label.config(text=results, font=("Arial", 14), wraplength=700, justify="left", bg="#F0F0F0", padx=10, pady=10, borderwidth=2, relief="flat")
        else:
            verb_text = "\n".join(results["Verbs"])
            noun_text = "\n".join(results["Nouns"])
            output_label.config(text=f"Verbs:\n{verb_text}\n\nNouns:\n{noun_text}", font=("Arial", 14), wraplength=700, justify="left", bg="#F0F0F0", padx=10, pady=10)
    else:
        messagebox.showwarning("Empty field", "Please enter a word.")

window = tk.Tk()
window.title("English Dictionary")
window.geometry("800x600")
window.resizable(False, False)
window.configure(bg="#F0F0F0")

title_label = tk.Label(window, text="English Dictionary", font=("Arial", 36, "bold"), bg="#F0F0F0", fg="#333")
title_label.pack(fill=tk.X, pady=20)

search_text_label = tk.Label(window, text="Search for a word", font=("Arial", 14), bg="#F0F0F0", fg="#333")
search_text_label.pack(fill=tk.X, pady=(0, 5))

input_button_frame = tk.Frame(window, bg="#F0F0F0")
input_button_frame.pack(pady=20)

entry = ttk.Entry(input_button_frame, font=("Arial", 18), width=40)
entry.pack(side=tk.LEFT, pady=10, padx=10, ipady=8, fill=tk.BOTH, expand=True)

search_button = ttk.Button(input_button_frame, text="Search", style="Custom.TButton", command=display_definition)
search_button.pack(side=tk.LEFT, pady=10, padx=10, ipady=8, fill=tk.BOTH, expand=True)

output_frame = tk.Frame(window, bg="#F0F0F0")
output_frame.pack(pady=20)

output_label = tk.Label(output_frame, font=("Arial", 14), wraplength=700, justify="left", bg="#F0F0F0", padx=10, pady=10, borderwidth=2, relief="flat")
output_label.pack()

entry.bind("<Return>", display_definition)

footer_label = tk.Label(window, text="All Rights Reserved.", font=("Arial", 10), bg="#F0F0F0", fg="#333")
footer_label.pack(side=tk.BOTTOM, fill=tk.X, pady=10)

window.tk_setPalette(background="#F0F0F0")
window.style = ttk.Style()
window.style.configure("Custom.TButton", foreground="#2E8B57", background="#F0F0F0", font=("Arial", 14, "bold"))

window.mainloop()
