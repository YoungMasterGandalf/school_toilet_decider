import random
import json

from configurator import colors

###
# A simple program for decision making --> can a student go to a loo or not?
# With every iteration the probability of success decreases.
###

welcome_message = """
 __          __  _                            _           _____ ________      ______      .----------------.
 \ \        / / | |                          | |         / ____|  ____\ \    / / __ \     ;----------------;
  \ \  /\  / /__| | ___ ___  _ __ ___   ___  | |_ ___   | |  __| |__   \ \  / / |  | |    | ~~ .------.    |
   \ \/  \/ / _ \ |/ __/ _ \| '_ ` _ \ / _ \ | __/ _ \  | | |_ |  __|   \ \/ /| |  | |    |   /        \   |
    \  /\  /  __/ | (_| (_) | | | | | |  __/ | || (_) | | |__| | |____   \  / | |__| |    |  /          \  |
     \/  \/ \___|_|\___\___/|_| |_| |_|\___|  \__\___/   \_____|______|   \/   \____/     |  |          |  |  ,----. 
                                                                                          |   \ ,    , /   | =|____|= 
                                                                                          '---,########,---'  (---(
  _____            _     _                                                                   /##'    '##\      )---)
 |  __ \          (_)   | |                                                                  |##,    ,##|     (---(
 | |  | | ___  ___ _  __| | ___ _ __                                                          \\'######'/       '---`
 | |  | |/ _ \/ __| |/ _` |/ _ \ '__|                                                          \`\"\"\"\"`/
 | |__| |  __/ (__| | (_| |  __/ |                                                              |`\"\"`|
 |_____/ \___|\___|_|\__,_|\___|_|                                                            .-|    |-.
                                                                                         jgs /  '    '  \\
                                                                                             '----------'

"""

help_message = """

Instructions: 

In order to run a toilet lottery for a class, type "run <class name>" and hit return (enter).
    Example: run 5.B

In order to show current probabilities for a class, type "show <class name>" and hit return (enter).
    Example: show 2.C

To show the whole configuration (all classes and their probabilities), type "showall" and hit return (enter).

When you are finished, type "end" and hit return (enter).

To show this help message again (any time), type "help".

-----------------------------------------------------------------------------------------------------------------------

"""

def run_a_round(class_name, init_conf:dict):

    true_weight = init_conf[class_name]["true_weight"]
    false_weight = init_conf[class_name]["false_weight"]
    
    can_go_to_toilet = random.choices([True, False], weights=[true_weight, false_weight])[0]
    
    false_weight = random.uniform(false_weight, false_weight + true_weight*0.2)
    true_weight = 1 - false_weight
    init_conf[class_name]["true_weight"] = true_weight
    init_conf[class_name]["false_weight"] = false_weight

    student_name = input("Enter student's name: ")
    
    if can_go_to_toilet:
        print(f'{colors["green"]}{student_name} can go, hooray :){colors["end"]}\n')
    else:
        print(f'{colors["red"]}{student_name} can\'t go, too bad :({colors["end"]}\n')

def show_class_conf(class_name, init_conf:dict):
    percentage_conf = f'"Positive chance" = {init_conf[class_name]["true_weight"]*100} %, "Negative chance" = {init_conf[class_name]["false_weight"]*100}'
    print(f'{colors["green"]}{class_name}{colors["end"]}: {percentage_conf}\n')

def show_help(*args):
    print(help_message)

    return False

funcs = {
    "run": run_a_round,
    "show": show_class_conf,
    "showall": lambda _, init_conf: print(init_conf, '\n'),
    "end": lambda x,y: True,
    "help": show_help
}


if __name__ == "__main__":

    with open("./probability_weights.json", "r") as file:
        conf = json.load(file)

    print(welcome_message, '\n', help_message)

    finished = False

    class_names = list(conf.keys())

    if not class_names:
        print("No class configured, please run the 'Configurator' file to create a new configuration.")
        finished = True
    else:
        print(f"Current conf:\n{conf}")

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
        except KeyError:
            print(colors["red"] + 'Wrong command entered! Try again.' + colors["end"])

        # Writes out in every iteration because the program could be killed before writing the new conf
        with open("./probability_weights.json", "w") as file:
            weights_json = json.dumps(conf, indent=4)
            file.write(weights_json)
