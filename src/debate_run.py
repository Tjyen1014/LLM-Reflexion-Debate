from agents.debater_agent import NormalDebater,ReflexionDebater
from agents.reflexion_agent import generate_debate_reflexion
from pathlib import Path
from string_format import format_list_of_dictionary_to_string
from setting import COMPETITION_PROCESS,NORMAL_DEBATER_MODEL,REFLEXION_DEBATER_MODEL,TOPIC,REFLEXION_MEMORY_LENGTH

def update_reflexion_memory(debate_history,reflexion_debater):
    new_reflexion_memory = generate_debate_reflexion(format_list_of_dictionary_to_string(debate_history),reflexion_debater)
    reflexion_debater.reflexion_memory.append(f"{len(reflexion_debater.reflexion_memory)+1}. {new_reflexion_memory}")
    return

def save_debate_results(debate_history,reflexion_memory):
    output_file = Path("logs/output.txt")
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open("logs/output.txt", "a") as f:
        f.write("Next debate\n")
        f.write(format_list_of_dictionary_to_string(debate_history))
        f.close()
    pass

normal_debater= NormalDebater(TOPIC,"Proponent",NORMAL_DEBATER_MODEL)
reflexion_debater = ReflexionDebater(TOPIC,"Opponent",REFLEXION_DEBATER_MODEL)
number_of_rounds = REFLEXION_MEMORY_LENGTH + 1

for i in range(number_of_rounds):
    debate_history = []
    for j in range(len(COMPETITION_PROCESS)):
        phase = COMPETITION_PROCESS[j]['phase'] + " " + "Phase"
        if COMPETITION_PROCESS[j]['stance'] == normal_debater.stance :
            response = normal_debater.generate_argument(COMPETITION_PROCESS,phase,debate_history)
            debate_history.append({"phase":COMPETITION_PROCESS[j]['phase'],"content": response})
        else :
            response = reflexion_debater.generate_argument(COMPETITION_PROCESS,phase,debate_history,reflexion_debater.reflexion_memory)
            debate_history.append({"phase":COMPETITION_PROCESS[j]['phase'],"content": response})
    save_debate_results(debate_history,reflexion_debater.reflexion_memory)
    update_reflexion_memory(debate_history,reflexion_debater)
pass