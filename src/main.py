from src.agents.debater_agent import NormalDebater,ReflexionDebater
from src.agents.reflexion import generate_debate_reflexion
from src.agents.evaluator import evaluate_debate_result
from pathlib import Path
from src.string_format import format_list_of_dictionary_to_string
from src.settings.configs import COMPETITION_PROCESS,NORMAL_DEBATER_MODEL,REFLEXION_DEBATER_MODEL,REFLEXION_MEMORY_LENGTH
import json


"""
    "loser_stance": "proponent",
    "debate_history": first_debate_history,
    "new_reflexion": None,
    "reflexion_memory": []
"""

def update_reflexion_debater_reflexion_memory(debate_history,reflexion_debater,debate_judgment_rationale):
    new_reflexion_memory = generate_debate_reflexion(format_list_of_dictionary_to_string(debate_history),reflexion_debater.stance,debate_judgment_rationale)
    reflexion_debater.reflexion_memory.append(f"{len(reflexion_debater.reflexion_memory)+1}. {new_reflexion_memory}")
    return
    
def save_debate_rounds_data(round_index,debate_history,winner_stance,loser_stance,reflexion_memory,judgment_rationale):
    RESULT_JSON['rounds'].append({"round_index" :round_index,
                                  "winner_stance":winner_stance,
                                  "loser_stance":loser_stance,
                                  "reflexion_memory":list(reflexion_memory),
                                  "debate_history":debate_history,
                                  "judgment_rationale":judgment_rationale
                                    })

def save_debate_results(debate_topic_index):
    output_file = Path(f"logs/Debate Topic {debate_topic_index}.json")
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, "w") as f:
        json.dump(RESULT_JSON, f, ensure_ascii=False, indent=2)
    return

def run_first_debate():
    first_debate_history = []
    normal_proponent_debater = NormalDebater(TOPIC,"proponent",NORMAL_DEBATER_MODEL)
    normal_opponent_debater = NormalDebater(TOPIC,"opponent",NORMAL_DEBATER_MODEL)
    
    print("test1: " + NORMAL_DEBATER_MODEL + "\n")
    
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
    print("test2: " + normal_debater.model + "\n")
    print("test3: " + reflexion_debater.model + "\n")
    
    followup_debate_history = []
    for i in range(len(COMPETITION_PROCESS)):
        phase = COMPETITION_PROCESS[i]['phase'] + " " + "Phase"
        if COMPETITION_PROCESS[i]['speaker_stance'] == normal_debater.stance :
            response = normal_debater.generate_argument(COMPETITION_PROCESS,phase,followup_debate_history)
            followup_debate_history.append({"phase":COMPETITION_PROCESS[i]['phase'],"content": response})
        else :
            response = reflexion_debater.generate_argument(COMPETITION_PROCESS,phase,followup_debate_history,reflexion_debater.reflexion_memory)
            followup_debate_history.append({"phase":COMPETITION_PROCESS[i]['phase'],"content": response})
    return followup_debate_history


def reflexion_experiment(first_debate_history,debate_judgment_rationale,loser_stance):
    last_debate_history = first_debate_history
    last_debate_judgment_rationale = debate_judgment_rationale
    reflexion_debater = ReflexionDebater(TOPIC,loser_stance,REFLEXION_DEBATER_MODEL)
    if loser_stance == "proponent":
        normal_debater = NormalDebater(TOPIC,"opponent",NORMAL_DEBATER_MODEL)
    else:
        normal_debater = NormalDebater(TOPIC,"proponent",NORMAL_DEBATER_MODEL)

    for i in range(REFLEXION_MEMORY_LENGTH):
        update_reflexion_debater_reflexion_memory(last_debate_history,reflexion_debater,last_debate_judgment_rationale)
        last_debate_history = run_followup_debate(normal_debater,reflexion_debater)
        result = evaluate_debate_result(TOPIC,last_debate_history)
        last_debate_judgment_rationale = result['reason_for_decision']
        save_debate_rounds_data(i+1,last_debate_history,result['winning_side'],result['losing_side'],reflexion_debater.reflexion_memory,result['reason_for_decision'])
        if  result['losing_side'].lower() !=  reflexion_debater.stance.lower() :
            print(reflexion_debater.stance + "\n")
            print("reflexion success")
            break
    return

with open("src/topics_dataset.txt","r") as f:
    lines = f.readlines()
for i in range(2,15):
    TOPIC = lines[i].strip()
    print(TOPIC + "\n")
    RESULT_JSON = {
               "topic": TOPIC,
               "rounds":[]
              }
    first_debate_history = run_first_debate()
    result = evaluate_debate_result(TOPIC,first_debate_history)
    loser_stance = result['losing_side']
    first_debate_judgment_rationale = result['reason_for_decision']
    save_debate_rounds_data(0,first_debate_history,result['winning_side'],result['losing_side'],[],first_debate_judgment_rationale)
    reflexion_experiment(first_debate_history,first_debate_judgment_rationale,loser_stance)
    save_debate_results(i+1)
