from llm.client import ai_call
from string_format import format_list_of_dictionary_to_string

class NormalDebater:
    def __init__(self, topic,stance,model):
        self.topic = topic
        self.stance = stance
        self.model = model

    def build_prompt(self,COMPETITION_PROCESS,phase,debate_history):
        Role_Prompt =  "You are a professional AI debate agent. You are currently participating in a formal debate competition with strict word count enforcement."
        sections = [
                "Role :", 
                Role_Prompt,
                "Competiton Format :",
                format_list_of_dictionary_to_string(COMPETITION_PROCESS),
                "Current Task :",
                f"The Topic is {self.topic}. You are the {self.stance}. You are now in the {phase}.",
                "History Of Debate :",
                format_list_of_dictionary_to_string(debate_history),
                "Instruction :",
                "Please deliver a high-quality argument. Strictly adhere to the 600-word limit. Any text exceeding this limit will be disregarded.",
                f"The history above includes all arguments made prior to the current phase. Please analyze the opponent's logic, address their points, and deliver your {phase} argument.",
                "",
                "Please begin your statement:"
                ]
        prompt = "\n".join(sections)
        return prompt

    def generate_argument(self,COMPETITION_PROCESS,phase,debate_history):
        prompt = self.build_prompt(COMPETITION_PROCESS,phase,debate_history)
        print(f"Waiting ai generate {phase} arguement.\n")
        ##response = ai_call(self.model,prompt)
        print(f"{phase} arguement generate done.\n")
        return "a"
        
class ReflexionDebater(NormalDebater):
        def __init__(self,topic,stance,model):
            super().__init__(topic,stance,model)
            self.reflexion_memory = []

        def build_prompt(self,COMPETITION_PROCESS,phase,debate_history,reflexion_memory):
            if len(reflexion_memory) == 0 :
                reflexion_prompt = ""
            else :
                reflexion_prompt = "Self-Reflection & Feedback (Reflexion):\n"
                reflexion_prompt = reflexion_prompt + "\n".join(reflexion_memory) + "\n"
                reflexion_prompt = reflexion_prompt + "Before delivering your statement, please review the history of reflections and refine your debate strategy accordingly.\n"

            Role_Prompt =  "You are a professional AI debate agent. You are currently participating in a formal debate competition with strict word count enforcement."
            sections = [
                    "Role :", 
                    Role_Prompt,
                    "Competiton Format :",
                    format_list_of_dictionary_to_string(COMPETITION_PROCESS),
                    "Current Task :",
                    f"The Topic is {self.topic}. You are the {self.stance}. You are now in the {phase}.",
                    "History Of Debate :",
                    format_list_of_dictionary_to_string(debate_history),
                    "Instruction :",
                    "Please deliver a high-quality argument. Strictly adhere to the 600-word limit. Any text exceeding this limit will be disregarded.",
                    f"The history above includes all arguments made prior to the current phase. Please analyze the opponent's logic, address their points, and deliver your {phase} argument.",
                    reflexion_prompt,
                    "Please begin your statement:"
                    ]
            prompt = "\n".join(sections)
            return prompt

        def generate_argument(self,COMPETITION_PROCESS,phase,debate_history,reflexion_memory):
            prompt = self.build_prompt(COMPETITION_PROCESS,phase,debate_history,reflexion_memory)
            print(f"Waiting ai generate {phase} arguement.d\n")
            print(prompt)
            ##response = ai_call(self.model,prompt)
            print(f"{phase} arguement generate done.\n")
            ##return response
            return "b"