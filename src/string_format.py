def format_debate_history(debate_history):
    formated_debate_history = ""
    for entry in debate_history:
        formated_debate_history =  formated_debate_history  + entry['phase'] + " : "+ entry['content'] + "\n"
    return formated_debate_history