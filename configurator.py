import json

colors = {
        'green': '\033[92m',
        'red': '\033[91m',
        'end': '\033[0m'
    }

welcome_message = """
 __          __  _                            _           _____             __ _                       _             
 \ \        / / | |                          | |         / ____|           / _(_)                     | |            
  \ \  /\  / /__| | ___ ___  _ __ ___   ___  | |_ ___   | |     ___  _ __ | |_ _  __ _ _   _ _ __ __ _| |_ ___  _ __ 
   \ \/  \/ / _ \ |/ __/ _ \| '_ ` _ \ / _ \ | __/ _ \  | |    / _ \| '_ \|  _| |/ _` | | | | '__/ _` | __/ _ \| '__|
    \  /\  /  __/ | (_| (_) | | | | | |  __/ | || (_) | | |___| (_) | | | | | | | (_| | |_| | | | (_| | || (_) | |   
     \/  \/ \___|_|\___\___/|_| |_| |_|\___|  \__\___/   \_____\___/|_| |_|_| |_|\__, |\__,_|_|  \__,_|\__\___/|_|   
                                                                                  __/ |                              
                                                                                 |___/  

"""

help_message = """
Instructions:

In order to add a new class configuration, type "add <class name>" and hit return (enter).
    Example: add 4.A

In order to delete a class configuration, type "delete <class name>" and hit return (enter).
    Example: delete 1.C

In order to reload default probability setting (50/50 chance) of a class, type "reload <class name>" and hit return (enter).
    Example: reload 3.B

When you are finished with the configuration, type "end".

To show this help message again (any time), type "help".

-----------------------------------------------------------------------------------------------------------------------------

"""

def add_class(class_name, init_conf:dict):
    init_conf[class_name] = {"true_weight": 0.5, "false_weight": 0.5}

    return False

def delete_class(class_name, init_conf:dict):
    if class_name in init_conf:
        init_conf.pop(class_name)
    else:
        print(colors['red'] + "Class not found!" + colors['end'])

    return False

def reload_class_settings(class_name, init_conf:dict):
    if class_name in init_conf:
        add_class(class_name, init_conf)
    else:
        print(colors["red"] + "Class not found!" + colors["end"])

    return False

def show_help(*args):
    print(help_message)

    return False

funcs = {
    "add": add_class,
    "delete": delete_class,
    "reload": reload_class_settings,
    "end": lambda x,y: True,
    "help": show_help
}

messages = {
    "add": lambda class_name: f'Succesfully added class "{class_name}".',
    "delete": lambda class_name: f'Succesfully delete configuration of class "{class_name}".',
    "reload": lambda class_name: f'Succesfully reloaded configuration of class "{class_name}".',
    "end": lambda class_name: "Saving configuration and terminating program...",
    "help": lambda class_name: ""
}

if __name__ == "__main__":
    with open("./probability_weights2.json", "r") as file:
        conf = json.load(file)

    print(welcome_message, '\n', help_message)

    finished = False

    while not finished:
        user_input = input("Enter a command (for help type 'help'): ")
        split_input = [x.strip() for x in user_input.split()]

        command = split_input[0]
        try:
            class_name = split_input[1]
        except IndexError:
            class_name = None

        try:
            finished = funcs[command](class_name, conf)
            print(colors["green"] + messages[command](class_name) + colors["end"])
        except KeyError:
            print(colors["red"] + 'Wrong command entered! Try again.' + colors["end"])

    with open("./probability_weights2.json", "w") as file:
        weights_json = json.dumps(conf, indent=4)
        file.write(weights_json)