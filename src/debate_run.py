from agents.normal_debater import NormalDebater
from pathlib import Path
from string_format import format_list_of_dictionary_to_string
from setting import COMPETITION_PROCESS,PROPONENT_MODEL,OPPONENT_MODEL,TOPIC

debate_history = [
]

proponent_debater = NormalDebater(TOPIC,"Proponent",PROPONENT_MODEL)
opponent_debater = ReflexionDebater(TOPIC,"Opponent",OPPONENT_MODEL)

for i in range(len(COMPETITION_PROCESS)):
    phase = COMPETITION_PROCESS[i]['phase'] + " " + "Phase"
    if "Proponent" in phase:
        response = proponent_debater.generate_argument(COMPETITION_PROCESS,phase,debate_history)
        debate_history.append({"phase":COMPETITION_PROCESS[i]['phase'],"content": response})
    else:
        response = opponent_debater.generate_argument(COMPETITION_PROCESS,phase,debate_history)
        debate_history.append({"phase":COMPETITION_PROCESS[i]['phase'],"content": response})

output_file = Path("logs/output.txt")
output_file.parent.mkdir(parents=True, exist_ok=True)
with open("logs/output.txt", "w") as f:
    f.write(format_list_of_dictionary_to_string(debate_history))
    f.close()
pass