import json
import openpyxl

quantitative_data =  {
                    'Topic' : "",
                    'Rematch_Win_Time' : 0,
                     }

wb = openpyxl.Workbook()
ws = wb.active
ws.append(list(quantitative_data.keys()))

for i in range(100):
    with open(f'logs/Debate Topic {i+1}.json') as file:
        debate_data = json.load(file)
    print(i + "\n")
    print(debate_data['topic'] + "\n")
    print(debate_data['rounds'][0]['winner_stance'] + "\n")
    print(debate_data['rounds'][0]['loser_stance'] + "\n")
    normal_debater = NormalDebater(debate_data['topic'],debate_data['rounds'][0]['winner_stance'],"gpt-5-mini-2025-08-07")
    reflexion_debater = ReflexionDebater(debate_data['topic'],debate_data['rounds'][0]['loser_stance'],"gpt-5-mini-2025-08-07",debate_data['rounds'][-1]['reflexion_memory'])
    quantitative_data['Topic'] = debate_data['topic']
    quantitative_data['Rematch_Win_Time'] = 0

    for j in range(3):
        debate_history = []

        for k in range(len(COMPETITION_PROCESS)):
            phase = COMPETITION_PROCESS[k]['phase'] + " " + "Phase"
            if COMPETITION_PROCESS[k]['speaker_stance'] == normal_debater.stance :
                print( normal_debater.stance + "speaking" + k + "\n")
                response = normal_debater.generate_argument(COMPETITION_PROCESS,phase,debate_history)
                debate_history.append({"phase":COMPETITION_PROCESS[k]['phase'],"content": response})
            else :
                print( reflexion_debater.stance + "speaking" + k + "\n")
                response = reflexion_debater.generate_argument(COMPETITION_PROCESS,phase,debate_history)
                debate_history.append({"phase":COMPETITION_PROCESS[k]['phase'],"content": response})
        result = evaluate_debate_result(debate_data['topic'],debate_history)
        
        if result['losing_side'].strip().lower() != reflexion_debater.stance.strip().lower():
            quantitative_data['Rematch_Win_Time'] =  quantitative_data['Rematch_Win_Time']  + 1
        print("debate round done \n")
    
    ws.append(list(quantitative_data.values()))

wb.save('quantitative_data_file/quantitative_data_.xlsx')
     