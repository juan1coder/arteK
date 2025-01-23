import tkinter as tk
from tkinter import simpledialog
import random
import requests
from bs4 import BeautifulSoup

def fetch_wikipedia_data(topic):
    """Fetch data from Wikipedia for a given topic."""
    url = f"https://en.wikipedia.org/wiki/{topic.replace(' ', '_')}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        paragraphs = soup.find_all('p')
        if paragraphs:
            content = ' '.join([p.get_text() for p in paragraphs[:2]])
            return content.strip()
        else:
            return "No Wikipedia content found."
    
    except requests.exceptions.Timeout:
        return "Request to Wikipedia timed out."
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return "No Wikipedia content found."
    except Exception as e:
        print(f"Error fetching Wikipedia data: {e}")
        return "No Wikipedia content found."

def extract_director_name(director_data):
    if isinstance(director_data, list) and len(director_data) > 0:
        return director_data[0].get('name', 'Unknown Director')
    return 'Unknown Director'

def fetch_json_data(url):
    """Fetch movie data from a given JSON URL and select 3 random movies."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        if len(data) < 3:
            selected_movies = data
        else:
            selected_movies = random.sample(data, 3)
        
        movie_list = []
        for movie in selected_movies:
            director = extract_director_name(movie.get("director"))
            title = movie.get('name', 'N/A')
            description = movie.get('trailer', {}).get('description', 'N/A')
            genres = ', '.join(movie.get('genre', []))
            keywords = movie.get('keywords', 'N/A')
            image = movie.get('image', 'N/A')
            
            movie_info = f"Director: {director}\nTitle: {title}\nDescription: {description}\nGenres: {genres}\nKeywords: {keywords}\nImage: {image}"
            movie_list.append(movie_info)
        
        return movie_list
    
    except requests.exceptions.Timeout:
        print("Request to JSON URL timed out.")
        return []
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return []
    except Exception as e:
        print(f"Error fetching JSON data: {e}")
        return []

def generate_amplified_prompt(base_prompt, resolution, style, wiki_data, movie_data):
    amplified_prompt = f"""
Welcome to the Advanced Prompt Amplifier!
Enter your base art prompt: {base_prompt}
Enter the resolution (default: {resolution}): 
Enter the style (default: {style}): 

Generated Amplified Prompt:
<persona>
You are an advanced AI art prompt engineer with expertise in creating detailed and structured prompts for generating highly specific visual and narrative descriptions.
</persona>

<task>
This builds upon the theme of: {base_prompt.split()[0:5]}.
</task>

<details>
1. Art Image prompt: {base_prompt} with {resolution} resolution and {style} style.
2. Includes cinematic, hyper-detailed, surreal, dream-like atmosphere, volumetric lighting, dynamic composition, neon accents.
3. Inspired by {wiki_data if wiki_data else "No Wikipedia data available"} and {", ".join(movie_data) if movie_data else "No IMDb data available."}.
4. The scene evokes surrealism, tension, and a hypnotic atmosphere.
</details>
"""
    return amplified_prompt.strip()

def main():
    # Create a Tkinter root window and hide it
    root = tk.Tk()
    root.withdraw()
    
    print("Welcome to the Advanced Prompt Amplifier!")
    base_prompt = simpledialog.askstring("Base Art Prompt", "Enter your base art prompt:")
    if not base_prompt:
        print("No prompt entered. Exiting...")
        return
    
    resolution = simpledialog.askstring("Resolution", "Enter the resolution (default: 16K):", initialvalue="16K") or "16K"
    style = simpledialog.askstring("Style", "Enter the style (default: hyper-realistic):", initialvalue="hyper-realistic") or "hyper-realistic"
    
    wiki_topic = simpledialog.askstring("Wikipedia Topic", "Enter a Wikipedia topic to fetch data (e.g., Surrealism):")
    print("\nFetching Wikipedia data...")
    wiki_data = fetch_wikipedia_data(wiki_topic) if wiki_topic else "No Wikipedia topic entered."
    
    json_url = "https://raw.githubusercontent.com/movie-monk-b0t/top250/master/top250.json"
    print("\nFetching IMDb data...")
    movie_data = fetch_json_data(json_url)
    
    amplified_prompt = generate_amplified_prompt(base_prompt, resolution, style, wiki_data, movie_data)
    print("\n" + amplified_prompt)

if __name__ == "__main__":
    main()
