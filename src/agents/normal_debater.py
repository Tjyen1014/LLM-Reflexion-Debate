from llm.client import ai_call
from string_format import format_debate_history

class NormalDebater:
    def __init__(self, topic, stance,model):
        self.topic = topic
        self.stance = stance
        self.model = model

    def build_prompt(self,competition_format,phase,formated_debate_history):
        Role_Prompt =  "You are a professional AI debate agent. You are currently participating in a formal debate competition with strict word count enforcement."
        if(phase == "Proponent Opening Phase"):
            sections = [
                    "Role :", 
                    Role_Prompt,
                    "Competiton Format :",
                    competition_format,
                    "Current Task :",
                    f"The Topic is {self.topic}. You are the {self.stance}. You are now in the {phase}.",
                    "Instruction :",
                    "Please deliver a high-quality opening argument. Strictly adhere to the 600-word limit. Any text exceeding this limit will be disregarded. Focus on defining the scope and establishing your core pillars.",
                    "",
                    "Please begin your statement:"
                    ]
        else:
            sections = [
                    "Role :", 
                    Role_Prompt,
                    "Competiton Format :",
                    competition_format,
                    "Current Task :",
                    f"The Topic is {self.topic}. You are the {self.stance}. You are now in the {phase}.",
                    "History oF Debate :",
                    formated_debate_history,
                    "Instruction :",
                    f"The history above includes all arguments made prior to the current phase. Please analyze the opponent's logic, address their points, and deliver your {phase} argument.",
                    "",
                    "Please begin your statement:"
                    ]
        prompt = "\n".join(sections)
        return prompt

    def generate_argument(self,competition_format,phase,debate_history):
        formated_debate_history = format_debate_history(debate_history)
        prompt = self.build_prompt(competition_format,phase,formated_debate_history)
        print("Wait For ai_call\n")
        response = ai_call(self.model,prompt)
        print("ai_call_done\n")
        return response
    
