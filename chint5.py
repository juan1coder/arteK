import tkinter as tk
from tkinter import simpledialog
import random
import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime

# List of artists to be randomized and included in the output
artists = [
    "Akira Toriyama", "Alex Grey", "Alphonse Mucha", "Arcane", "Arnold Böcklin", "Artgerm", "Bioshock",
    "Botticelli", "Caravaggio", "Cezanne", "Dariusz Zawadzki", "David Cronenberg", "David Lynch",
    "Dishonored", "Edvard Munch", "Egon Schiele", "Fernanda Suarez", "Franz Marc", "Grant Wood",
    "Gustav Klimt", "Gustavé Doré", "Hermann Stenner", "HR Giger", "Ilya Kuvshinov", "Jakub Rozalski",
    "John Jude Palencar", "Josan Gonzalez", "Katsushika Hokusai", "Liam Wong", "Luis Buñuel", "Luis Royo",
    "Michelangelo", "Nekro", "Odilon Redon", "Pascal Blanche", "Paul Gauguin", "Rembrandt",
    "Roger Ballen", "Simon Stalenhag", "Takashi Miike", "Utagawa Kunisada", "Utagawa Kuniyoshi",
    "Vincent van Gogh", "Wassily Kandinsky", "Wlop", "Pietro Adami", "Yoshitaka Amano",
    "Yousuf Karsh", "Zdzislaw Beksinski"
]

# Function to fetch data from Wikipedia
def fetch_wikipedia_data(topic):
    """Fetch clean data from Wikipedia for a given topic."""
    url = f"https://en.wikipedia.org/wiki/{topic.replace(' ', '_')}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        paragraphs = soup.find_all('p')
        if paragraphs:
            # Clean up text by removing non-printable and escape characters
            content = "\n".join([p.get_text() for p in paragraphs[:2]])
            content = content.replace("\u2060", "").replace("\\", "").replace("\n", " ").strip()
            return content
        else:
            return "No Wikipedia content found."

    except requests.exceptions.RequestException:
        return "Failed to fetch Wikipedia content."

# Generate a JSON-style prompt
def generate_amplified_prompt(base_prompt, resolution, style, theme, elements, wiki_data, artist_list):
    random.shuffle(artist_list)
    selected_artists = artist_list[:5]

    prompt = {
        "base_prompt": base_prompt,
        "style": [style, "surreal", "dream-like", "3D"],
        "resolution": resolution,
        "elements": [
            {"type": "shapes", "variety": ["triangles", "squares", "hexagons", "fractal patterns"], "colors": "neon"},
            {"type": "character", "appearance": "surreal", "features": ["bright eyes", "abstract face", "geometric body", "volumetric lighting"]},
            {"type": "background", "style": "organic", "colors": ["neon", "pastel"], "theme": theme},
            {"type": "guidelines", "anatomical_accuracy": "Renaissance principles of human anatomy", "influence": ["dynamic composition", "cinematic proportions"]}
        ],
        "theme": theme,
        "artists": selected_artists,
        "inspired_by": wiki_data if wiki_data else "General knowledge"
    }
    return prompt

# Save all generated prompts to a single file
def save_prompts_to_file(prompts, filename):
    """Save all prompts to a single file."""
    filepath = os.path.join("/tmp", filename)
    try:
        with open(filepath, "w") as file:
            for idx, prompt in enumerate(prompts, 1):
                file.write(f"Chain of thoughts {idx}:\n{prompt}\n\n")
        print(f"All prompts saved to: {filepath}")
    except IOError as e:
        print(f"Failed to save prompts: {e}")

def main():
    # Create a Tkinter root window and hide it
    root = tk.Tk()
    root.withdraw()

    print("Welcome to the Advanced Prompt Generator!")
    base_prompt = simpledialog.askstring("Base Art Prompt", "Enter your base art prompt:")
    if not base_prompt:
        print("No prompt entered. Exiting...")
        return

    resolution = simpledialog.askstring("Resolution", "Enter the resolution (default: 16K):", initialvalue="16K") or "16K"
    style = simpledialog.askstring("Style", "Enter the style (default: hyper-realistic):", initialvalue="hyper-realistic") or "hyper-realistic"
    theme = simpledialog.askstring("Theme", "Enter a theme (e.g., forest mystery):", initialvalue="forest mystery") or "forest mystery"

    wiki_topic = simpledialog.askstring("Wikipedia Topic", "Enter a Wikipedia topic to fetch data (e.g., Surrealism):")
    print("Fetching Wikipedia data...")
    wiki_data = fetch_wikipedia_data(wiki_topic) if wiki_topic else "No Wikipedia topic entered."

    num_prompts = simpledialog.askinteger("Number of Prompts", "How many prompts would you like to generate?", minvalue=1, initialvalue=3)
    if not num_prompts or num_prompts < 1:
        print("Invalid number of prompts. Exiting...")
        return

    elements = ["shapes", "character", "background", "guidelines"]

    # Generate and save multiple prompts
    all_prompts = []
    for i in range(num_prompts):
        amplified_prompt = generate_amplified_prompt(base_prompt, resolution, style, theme, elements, wiki_data, artists)
        # Add the sanitized prompt string to the list
        all_prompts.append(str(amplified_prompt).replace("'", '"'))  # Use JSON-style double quotes

    # Generate a single unique filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"all_prompts_{timestamp}.txt"

    # Save all prompts to a single file
    save_prompts_to_file(all_prompts, filename)

if __name__ == "__main__":
    main()
