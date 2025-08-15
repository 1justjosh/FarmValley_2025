from src.engine.settings import *

import json


DEFAULT_DATA = {
    ""
}

def save_file(path,generator):
    with open(path,"w") as file:
        data = {}

        # ----------- player ------------------
        data["player"] = {
            "pos": generator.player.rect.midtop,
            "selected-tool": generator.player.selected_tool,
            "inventory":generator.player.inventory
        }


        # ------------trees--------------------
        if len(generator.tree_tiles) > 0:
            data["trees"] = {}
            for pos in generator.tree_tiles:
                tree = generator.tree_tiles[pos][1]
                if not tree.tree_type in data["trees"]:
                    data["trees"][tree.tree_type] = {}

                data["trees"][tree.tree_type][pos] = {
                    "num-fruit":tree.num_fruit
                }

        # -----------Dirt-----------------------------
        if len(generator.dirt_tiles) > 0:
            data["dirt"] = {}
            for pos in generator.dirt_tiles:
                print(f"{pos =}")
                dirt = generator.dirt_tiles[pos]

                dirt_type = dirt.plant if dirt.plant is not None else "None"
                if dirt_type not in data["dirt"]:
                    data["dirt"][dirt_type] = {}

                data["dirt"][dirt_type][pos] = {
                    "stage":0
                }

        json.dump(data,file,indent=4)

def load_file(path):
    with open(path, "r") as file:
        return json.load(file)



