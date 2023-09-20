import sys
import os
import time


## importa classes
from environment import Env
from explorer import Explorer
from rescuer import Rescuer

def main(data_folder_name):

    # Set the path to config files and data files for the environment
    current_folder = os.path.abspath(os.getcwd())
    data_folder = os.path.abspath(os.path.join(current_folder, data_folder_name))


    # Instantiate the environment
    env = Env(data_folder)

    # config files for the agents
    rescuer_file = os.path.join(data_folder, "rescuer_config.txt")
    explorer_file = []
    explorer_file.append(os.path.join(data_folder, "explorer0_config.txt"))
    explorer_file.append(os.path.join(data_folder, "explorer1_config.txt"))
    explorer_file.append(os.path.join(data_folder, "explorer2_config.txt"))
    explorer_file.append(os.path.join(data_folder, "explorer3_config.txt"))

    # Instantiate agents rescuer and explorer
    resc = Rescuer(env, rescuer_file)

    # Explorer needs to know rescuer to send the map
    # that's why rescuer is instatiated before
    exp0 = Explorer(env, explorer_file[0], resc)
    exp1 = Explorer(env, explorer_file[1], resc)
    exp2 = Explorer(env, explorer_file[2], resc)
    exp3 = Explorer(env, explorer_file[3], resc)

    # Run the environment simulator
    env.run()


if __name__ == '__main__':
    """ To get data from a different folder than the default called data
    pass it by the argument line"""

    if len(sys.argv) > 1:
        data_folder_name = sys.argv[1]
    else:
        data_folder_name = os.path.join("datasets", "data_20x20_42vic")

    main(data_folder_name)
