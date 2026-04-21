import json
import openpyxl

quantitative_data =  {
                    'Topic' : "",
                    'Reflex_Succeed' : 0,
                    'Reflex_Times' : 1
                     }

wb = openpyxl.Workbook()
ws = wb.active
ws.append(list(quantitative_data.keys()))

for i in range(100):
    with open(f'logs/Debate Topic {i+1}.json') as file:
        debate_data = json.load(file)
    quantitative_data['Topic'] = debate_data['topic']
    quantitative_data['Reflex_Succeed'] = 0
    quantitative_data['Reflex_Times'] = 1
    for i in range(3):
        if i == 0:
            start_winner = debate_data['rounds'][i]['winner_stance']
        else:
            if start_winner != debate_data['rounds'][i]['winner_stance']:
                quantitative_data['Reflex_Succeed'] = 1
                break
            else :
                quantitative_data['Reflex_Times'] =  quantitative_data['Reflex_Times'] + 1
    ws.append(list(quantitative_data.values()))

wb.save('quantitative_data_file/quantitative_data_.xlsx')
     