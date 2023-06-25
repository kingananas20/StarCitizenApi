import requests
import json
import typer
from enum import Enum
from dotenv import load_dotenv
import os
import colorama
from colorama import Fore, init
init(autoreset=True)

load_dotenv()
api_key = os.getenv("API_KEY")

url = f"https://api.starcitizen-api.com/{api_key}/v1/"
try:
    response = requests.get(url)
except:
    print(f"{Fore.YELLOW}No connection to API.")
    quit(10)

if response.status_code == 200:
    data = json.loads(response.text)

    if data["message"] == "Apikey is not correct.":
        print(f"{Fore.RED}Your Apikey is not correct.")
        print(f"{Fore.RED}Create a .env file in the same folder as this file and add this to it: 'API_KEY=<your apikey>'")
        quit(10)

app = typer.Typer()
starmap_app = typer.Typer()
app.add_typer(starmap_app, name="starmap",
              help="Get informations about the starmap.")


@app.command(help="Display information about an user.")
def user(handle: str):
    response = requests.get(url + f"live/user/{handle}")
    if response.status_code == 200:
        data = json.loads(response.text)
        if data["data"] != None:
            if data["data"]["organization"]["stars"] == 0:
                print(f"""
                  handle: {data["data"]["profile"]["handle"]}
                   badge: {data["data"]["profile"]["badge"]}
                location: {data["data"]["profile"]["location"]["country"]}
            organization: None
                    rank: None
                     sid: None
            """)
            else:
                print(f"""
                  handle: {data["data"]["profile"]["handle"]}
                   badge: {data["data"]["profile"]["badge"]}
                location: {data["data"]["profile"]["location"]["country"]}
            organization: {data["data"]["organization"]["name"]}
                    rank: {data["data"]["organization"]["rank"]}
                     sid: {data["data"]["organization"]["sid"]}
            """)

        else:
            print(f"{Fore.YELLOW}User (HANDLE): {handle} not existing!")

    else:
        print(f"{Fore.RED}API Error: {response.status_code}")


@app.command(help="Display information about an organization.")
def org(sid: str):
    response = requests.get(url + f"live/organization/{sid}")
    if response.status_code == 200:
        data = json.loads(response.text)
        if data["data"] != None:
            print(f"""
                  name: {data["data"]["name"]}
                   sid: {data["data"]["sid"]}
            recruiting: {data["data"]["recruiting"]}
                   url: {data["data"]["url"]}
              language: {data["data"]["lang"]}
               members: {data["data"]["members"]}
                  type: {data["data"]["archetype"]}
            commitment: {data["data"]["commitment"]}
                 focus:
                      primary: {data["data"]["focus"]["primary"]["name"]}
                    secondary: {data["data"]["focus"]["secondary"]["name"]}
            """)
        else:
            print(f"{Fore.YELLOW}Organization (SID): {sid} not existing!")

    else:
        print(f"{Fore.RED}API Error: {response.status_code}")


@app.command(help="Display the members of an organization.")
def org_members(sid: str):
    response = requests.get(url + f"live/organization_members/{sid}")
    if response.status_code == 200:
        data = json.loads(response.text)
        if data["data"] != None:
            i = 0
            for x in data["data"]:
                print(f"""
              name: {data["data"][i]["display"]}
            handle: {data["data"][i]["handle"]}
              rank: {data["data"][i]["rank"]}
                      """)
                i = i + 1
        else:
            print(f"{Fore.YELLOW}Organization (SID): {sid} not existing!")

    else:
        print(f"{Fore.RED}API Error: {response.status_code}")


@app.command(help="Display information about a ship.")
def ships(ship: str):
    response = requests.get(url + f"cache/ships?name={ship}")
    if response.status_code == 200:
        data = json.loads(response.text)
        if data["data"] != None:
            i = 0
            for x in data["data"]:
                print(f"""
                     name: {data["data"][i]["name"]}
             manufacturer: {data["data"][i]["manufacturer"]["name"]}
                   status: {data["data"][i]["production_status"]}
                    price: {data["data"][i]["price"]}
                     size: {data["data"][i]["size"]}
                     mass: {data["data"][i]["mass"]}
            cargocapacity: {data["data"][i]["cargocapacity"]}
                    focus: {data["data"][i]["focus"]}
              description:
                    {data["data"][i]["description"]}
                      url: {"https://robertsspaceindustries.com" + data["data"][i]["url"]}
            
                      """)

                i = i + 1
        else:
            print(f"{Fore.YELLOW}Ship (NAME): {ship} not existing!")

    else:
        print(f"{Fore.RED}API Error: {response.status_code}")


class Game(Enum):
    starcitizen = "starcitizen"
    squadron42 = "squadron42"


@app.command(help="Display the roadmap for a version.")
def roadmap(game: Game, version: str):
    response = requests.get(url + f"live/roadmap/{game}?version={version}")
    if response.status_code == 200:
        data = json.loads(response.text)
        if data["data"] != None:
            print(data)
        else:
            print(f"{Fore.YELLOW}Version (VERSION): {version} not existing!")

    else:
        print(f"{Fore.RED}API Error: {response.status_code}")


class Stats(Enum):
    live = "live"
    ptu = "ptu"
    players = "fans"
    funds = "funds"


@app.command(help="Display general stats.")
def stats():
    response = requests.get(url + f"live/stats")
    if response.status_code == 200:
        data = json.loads(response.text)
        if data["data"] != None:
            print(f"""
                live: {data["data"]["current_live"]}
                 ptu: {data["data"]["current_ptu"]}
            citizens: {data["data"]["fans"]}
               funds: {data["data"]["funds"]}      
                  """)

        else:
            print(f"{Fore.YELLOW}Something went wrong!")

    else:
        print(f"{Fore.RED}API Error: {response.status_code}")


@starmap_app.command(help="Display informations about a star system.")
def systems(system: str):
    response = requests.get(url + f"cache/starmap/systems?name={system}")
    if response.status_code == 200:
        data = json.loads(response.text)
        if data["data"] != None:
            print(f"""
            name: {data["data"]["name"]}
            code: {data["data"]["code"]}
            type: {data["data"]["type"]}
            affiliation: {data["data"]["affiliation"][0]["name"]}
            description:
                {data["data"]["description"]}
            x: {data["data"]["position_x"]}
            y: {data["data"]["position_y"]}      
            z: {data["data"]["position_z"]}
                  """)
        else:
            print(f"{Fore.YELLOW}Star system {system} does not exist.")

    else:
        print(f"{Fore.RED}API Error: {response.status_code}")


@starmap_app.command(help="Search for an object in the Starmap.")
def search(query):
    response = requests.get(url + f"live/starmap/search?name={query}")
    if response.status_code == 200:
        data = json.loads(response.text)
        if data["data"] != None:
            i = 0
            for x in data["data"]["objects"]:
                print(f"""
                   name: {data["data"]["objects"][i]["name"]}
                   code: {data["data"]["objects"][i]["code"]}
            designation: {data["data"]["objects"][i]["designation"]}
                   type: {data["data"]["objects"][i]["type"]}
            star_system:
                name: {data["data"]["objects"][i]["star_system"]["name"]}
                code: {data["data"]["objects"][i]["star_system"]["code"]}          
                    """)

                i = i + 1

        else:
            print(f"{Fore.YELLOW}Query {query} is not an object.")

    else:
        print(f"{Fore.RED}API Error: {response.status_code}")


if __name__ == "__main__":
    app()
