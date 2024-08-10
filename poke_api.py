import requests
import os

POKE_API_URL = 'https://pokeapi.co/api/v2/pokemon/'

def get_pokemon_info(pokemon):
    """Gets information about a specified Pokemon from the PokeAPI.

    Args:
        pokemon (str): Pokemon name (or Pokedex number)

    Returns:
        dict: Dictionary of Pokemon information, if successful. Otherwise None.
    """
    pokemon = str(pokemon).strip().lower()

    if pokemon == '':
        print('Error: No Pokemon name specified.')
        return None

    print(f'Getting information for {pokemon.capitalize()}...', end='')
    url = POKE_API_URL + pokemon
    resp_msg = requests.get(url)

    if resp_msg.status_code == requests.codes.ok:
        print('success')
        return resp_msg.json()
    else:
        print('failure')
        print(f'Response code: {resp_msg.status_code} ({resp_msg.reason})')
        return None

def get_pokemon_names():
    """Fetches a list of all Pokémon names from the PokéAPI.

    Returns:
        list: List of Pokémon names if successful, otherwise None.
    """
    url = f"{POKE_API_URL}?limit=10000"
    print('Getting list of Pokémon names...', end='')
    resp_msg = requests.get(url)

    if resp_msg.status_code == requests.codes.ok:
        print('success')
        pokemon_list = resp_msg.json()['results']
        return [pokemon['name'] for pokemon in pokemon_list]
    else:
        print('failure')
        print(f'Response code: {resp_msg.status_code} ({resp_msg.reason})')
        return None

def download_pokemon_artwork(pokemon_name, save_dir):
    """Downloads the official artwork of a specified Pokémon and saves it to disk.

    Args:
        pokemon_name (str): The name of the Pokémon.
        save_dir (str): The directory where the image should be saved.

    Returns:
        str: Path to the saved image file if successful, otherwise None.
    """
    pokemon_name = pokemon_name.strip().lower()
    if pokemon_name == '':
        print('Error: No Pokémon name specified.')
        return None

    print(f'Downloading artwork for {pokemon_name.capitalize()}...', end='')
    
    # Fetch Pokémon info to get artwork URL
    pokemon_info = get_pokemon_info(pokemon_name)
    if pokemon_info is None:
        print('Could not retrieve Pokémon info.')
        return None
    
    artwork_url = pokemon_info['sprites']['other']['official-artwork']['front_default']
    resp_msg = requests.get(artwork_url)

    if resp_msg.status_code == requests.codes.ok:
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        
        image_path = os.path.join(save_dir, f"{pokemon_name}.png")
        with open(image_path, 'wb') as file:
            file.write(resp_msg.content)
        print('success')
        return image_path
    else:
        print('failure')
        print(f'Response code: {resp_msg.status_code} ({resp_msg.reason})')
        return None
