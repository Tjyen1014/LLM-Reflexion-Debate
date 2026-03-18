from agents.debater_agent import NormalDebater,ReflexionDebater
from agents.reflexion_agent import generate_debate_reflexion
from agents.evaluator import evaluate_losing_stance
from pathlib import Path
from string_format import format_list_of_dictionary_to_string
from setting import COMPETITION_PROCESS,NORMAL_DEBATER_MODEL,REFLEXION_DEBATER_MODEL,TOPIC,REFLEXION_MEMORY_LENGTH

def update_reflexion_debater_reflexion_memory(debate_history,reflexion_debater):
    new_reflexion_memory = generate_debate_reflexion(format_list_of_dictionary_to_string(debate_history),reflexion_debater)
    reflexion_debater.reflexion_memory.append(f"{len(reflexion_debater.reflexion_memory)+1}. {new_reflexion_memory}")
    return

def save_debate_results(debate_history,loser_stance,reflexion_memory):
    output_file = Path("logs/output.txt")
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open("logs/output.txt", "a") as f:
        f.write("==debate==\n")
        f.write(loser_stance + "\n")
        f.write("\n".join(reflexion_memory) + "\n")
        f.write(format_list_of_dictionary_to_string(debate_history))
        f.close()
    return

def run_first_debate():
    first_debate_history = []
    normal_proponent_debater = NormalDebater(TOPIC,"proponent",NORMAL_DEBATER_MODEL)
    normal_opponent_debater = NormalDebater(TOPIC,"opponent",NORMAL_DEBATER_MODEL)
    for i in range(len(COMPETITION_PROCESS)):
        phase = COMPETITION_PROCESS[i]['phase'] + " " + "Phase"
        if COMPETITION_PROCESS[i]['speaker_stance'] == normal_proponent_debater.stance :
            response = normal_proponent_debater.generate_argument(COMPETITION_PROCESS,phase,first_debate_history)
            first_debate_history.append({"phase":COMPETITION_PROCESS[i]['phase'],"content": response})
        else :
            response = normal_opponent_debater.generate_argument(COMPETITION_PROCESS,phase,first_debate_history)
            first_debate_history.append({"phase":COMPETITION_PROCESS[i]['phase'],"content": response})
    return first_debate_history

def run_followup_debate(normal_debater,reflexion_debater):
    followup_debate_history = []
    for i in range(len(COMPETITION_PROCESS)):
        phase = COMPETITION_PROCESS[i]['phase'] + " " + "Phase"

        print(normal_debater.stance)
        print(reflexion_debater.stance)
        print(COMPETITION_PROCESS[i]['speaker_stance'])
        print("\n\n\n\n")
        if COMPETITION_PROCESS[i]['speaker_stance'] == normal_debater.stance :
            response = normal_debater.generate_argument(COMPETITION_PROCESS,phase,followup_debate_history)
            followup_debate_history.append({"phase":COMPETITION_PROCESS[i]['phase'],"content": response})
        else :
            response = reflexion_debater.generate_argument(COMPETITION_PROCESS,phase,followup_debate_history,reflexion_debater.reflexion_memory)
            followup_debate_history.append({"phase":COMPETITION_PROCESS[i]['phase'],"content": response})
    return followup_debate_history


def reflexion_experiment(first_debate_history,loser_stance):
    last_debate_history = first_debate_history
    reflexion_debater = ReflexionDebater(TOPIC,loser_stance,REFLEXION_DEBATER_MODEL)
    if loser_stance == "proponent":
        normal_debater = NormalDebater(TOPIC,"opponent",NORMAL_DEBATER_MODEL)
    else:
        normal_debater = NormalDebater(TOPIC,"proponent",NORMAL_DEBATER_MODEL)

    for i in range(REFLEXION_MEMORY_LENGTH):
        update_reflexion_debater_reflexion_memory(last_debate_history,reflexion_debater)
        last_debate_history = run_followup_debate(normal_debater,reflexion_debater)
        save_debate_results( last_debate_history,loser_stance,reflexion_debater.reflexion_memory)
        if evaluate_losing_stance(last_debate_history) !=  reflexion_debater.stance :
            break
    return
         
first_debate_history = run_first_debate()
save_debate_results(first_debate_history,"","")
loser_stance = evaluate_losing_stance(first_debate_history)
reflexion_experiment(first_debate_history,loser_stance)