"""
    MOCK TESTS
"""
from http import client
from fastapi.testclient import TestClient
from main import app
client = TestClient(app)

# Test 1
def test_pokemon_battle_win(mocker):
    """
        Check the pokemon/battle endpoint : winner
    """
    mocker.patch(
        "app.utils.pokeapi.battle_compare_stats",
        return_value = 1
    )
    first_poke_api_id=1
    second_poke_api_id=4
    response = client.get(
        "/pokemons/battle?first_poke_api_id="+first_poke_api_id+
        "&second_poke_api_id="+second_poke_api_id
        )
    assert response.status_code == 200
    assert response.json() == {"winner": "bulbasaur"}

# Test 2
def test_pokemon_battle_draw(mocker):
    """
        Check the pokemon/battle endpoint : draw
    """
    mocker.patch(
        "app.utils.pokeapi.battle_compare_stats",
        return_value = 0
    )
    first_poke_api_id=1
    second_poke_api_id=1
    response = client.get(
        "/pokemons/battle?first_poke_api_id="+first_poke_api_id+
        "&second_poke_api_id="+second_poke_api_id)
    assert response.status_code == 200
    assert response.json() == {'winner': 'draw'}

# Test 3
def test_get_three_random_pokemon(mocker):
    """
        Check if the get_three_random_pokemon endpoint return 3 pokemons with the right format
    """
    mocker.patch(
        "app.utils.pokeapi.get_pokemon_name",
        return_value = {"name": "cottonee"}
    )
    mocker.patch(
        "app.utils.pokeapi.get_pokemon_stats",
        return_value = {"hp": 40,
                        "attack": 27,
                        "defense": 60,
                        "special-attack": 37,
                        "special-defense": 50,
                        "speed": 66}
    )
    response = client.get("/pokemons/random")
    assert len(response.json()) > 0
    for poke in response.json():
        assert poke['name'] == {"name": "cottonee"}
        assert poke['stats'] == {"hp": 40, "attack": 27, "defense": 60,
        "special-attack": 37, "special-defense": 50, "speed": 66}
    assert response.status_code == 200

# Test 4
def test_pokemon_for_trainer(mocker):
    """
        Creation d'un pokemon
    """
    mocker.patch(
        "app.utils.pokeapi.get_pokemon_name",
        return_value={"name" : "pikachu"}
        )
    response = client.post("/trainers/1/pokemon/", json={"api_id": 25,"custom_name": "tchutchu"})
    assert response.status_code == 200
    assert response.json() == {"api_id": 25,"custom_name":
        "tchutchu","id": 2,"name": "pikachu","trainer_id": 1}

# Test 5
# Create a pokemon for a trainer
def test_create_pokemon_for_trainer(mocker):
    """
        Creation d'un pokemon pour un trainer
    """
    mocker.patch(
        "app.utils.pokeapi.get_pokemon_data",
        return_value={"name": "charizard", "id": 6}
        )

    nbpokemon = len(client.get("/pokemons").json())
    response = client.post("/trainers/3/pokemon/",
        json={"api_id": 6, "custom_name": "Dracofeu"})
    assert response.status_code == 200
    assert response.json() == {"api_id": 6, "custom_name": "Dracofeu",
        "id": nbpokemon+1, "name": "charizard", "trainer_id": 3}
