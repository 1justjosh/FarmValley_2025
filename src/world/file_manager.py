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

            for pos, (pos_key, tree) in generator.tree_tiles.items():

                # Ensure tree_type exists
                if tree.tree_type not in data["trees"]:
                    data["trees"][tree.tree_type] = {}

                # Ensure num_fruit bucket exists
                if tree.num_fruit not in data["trees"][tree.tree_type]:
                    data["trees"][tree.tree_type][tree.num_fruit] = {}

                # Now you can safely store the tree
                data["trees"][tree.tree_type][tree.num_fruit][pos] = {
                }

        # -----------Dirt-----------------------------
        if len(generator.dirt_tiles) > 0:
            data["dirt"] = {}
            for pos in generator.dirt_tiles:
                dirt = generator.dirt_tiles[pos]

                dirt_type = dirt.plant_type if dirt.plant_type is not None else "dirt"
                if dirt_type not in data["dirt"]:
                    data["dirt"][dirt_type] = {}

                if not dirt.plant_stage in data["dirt"][dirt_type]:
                    data["dirt"][dirt_type][dirt.plant_stage] = {}

                data["dirt"][dirt_type][dirt.plant_stage][pos] = {}

        json.dump(data,file,indent=4)

def load_file(path):
    with open(path, "r") as file:
        return json.load(file)



