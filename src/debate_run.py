from agents.normal_debater import NormalDebater
from pathlib import Path
from string_format import format_debate_history

debate_history = [
]
competition_format ="\n".join([
                        "Proponent Opening: 600 words",
                        "Opponent Opening: 600 words",
                        "Proponent Rebuttal: 600 words",
                        "Opponent Rebuttal: 600 words",
                        "Proponent Closing: 600 words",
                        "Opponent Closing: 600 words"
                    ]) 
topic = "This House Would force all news organizations to be non profit(i.e. NHK, BBC, PBS)"
model =  "gpt-5-mini"

Competition_Process = [
                "Proponent Opening",
                "Opponent Opening",
                "Proponent Rebuttal",
                "Opponent Rebuttal",
                "Proponent Closing",
                "Opponent Closing"
                ]

proponent_debater = NormalDebater(topic,"Proponent",model)
opponent_debater = NormalDebater(topic,"Opponent",model)

for i in range(len(Competition_Process)):
    phase = Competition_Process[i] + " " + "Phase"
    print(Competition_Process[i] + "\n")
    if "Proponent" in Competition_Process[i]:
        response = proponent_debater.generate_argument(competition_format,phase,debate_history)
        debate_history.append({"phase":Competition_Process[i],"content": response})
    else:
        response = opponent_debater.generate_argument(competition_format,phase,debate_history)
        debate_history.append({"phase":Competition_Process[i],"content": response})

output_file = Path("logs/output.txt")
output_file.parent.mkdir(parents=True, exist_ok=True)
with open("logs/output.txt", "w") as f:
    f.write(format_debate_history(debate_history))
    f.close()
pass