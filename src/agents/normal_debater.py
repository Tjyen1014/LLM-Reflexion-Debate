from llm.client import ai_call

class NormalDebater:
    def __init__(self, topic, stance,model):
        self.topic = topic
        self.stance = stance
        self.model = model


    def format_debate_history(self,debate_history):
        formated_debate_history = ""
        for entry in debate_history:
            formated_debate_history =  formated_debate_history  + entry['phase'] + " : "+ entry['content'] + "\n"
        return formated_debate_history

    def build_prompt(self,competition_format,phase,formated_debate_history):
        Role_Prompt =  "You are a professional AI debate agent. You are currently participating in a formal debate competition with strict word count enforcement."
        if(phase == "Proposal Opening Phase"):
            prompt = f"""
                    Role : 
                    {Role_Prompt}
                    Competiton Format :
                    {competition_format}
                    Current Task :
                    The Topic is {self.topic}. You are the {self.stance}. You are now in the {phase}.
                    Instruction :
                    Please deliver a high-quality opening argument. Strictly adhere to the 600-word limit. Any text exceeding this limit will be disregarded. Focus on defining the scope and establishing your core pillars.

                    Please begin your statement:
                    """
        else:
            prompt = f"""
                    Role : 
                    {Role_Prompt}
                    Competiton Format :
                    {competition_format}
                    Current Task :
                    The Topic is {self.topic}. You are the {self.stance}. You are now in the {phase}.
                    History oF Debate :
                    {formated_debate_history}
                    Instruction :
                    The history above includes all arguments made prior to the current phase. Please analyze the opponent's logic, address their points, and deliver your {phase} argument.

                    Please begin your statement:
                    """
        
        return prompt

    def generate_argument(self,competition_format,phase,debate_history):
        formated_debate_history = self.format_debate_history(debate_history)
        print(formated_debate_history)
        prompt = self.build_prompt(competition_format,phase,formated_debate_history)
        print(prompt)
        pass
    ### response = ai_call(model,prompt)

    ### return response
    
