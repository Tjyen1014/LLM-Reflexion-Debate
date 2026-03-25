from src.llm.client import ai_call
from src.string_format import format_list_of_dictionary_to_string
from src.settings.prompts import NORMAL_DEBATER_PROMPT,REFLEXION_DEBATER_PROMPT

class NormalDebater:
    def __init__(self, topic,stance,model):
        self.topic = topic
        self.stance = stance
        self.model = model

    def build_prompt(self,COMPETITION_PROCESS,phase,debate_history):
        Role_Prompt =  "You are a professional AI debate agent. You are currently participating in a formal debate competition with strict word count enforcement."
        prompt = NORMAL_DEBATER_PROMPT.format(competition_process = format_list_of_dictionary_to_string(COMPETITION_PROCESS),
                                              topic = self.topic,stance = self.stance, phase = phase,
                                              debate_history = format_list_of_dictionary_to_string(debate_history))
        return prompt

    def generate_argument(self,COMPETITION_PROCESS,phase,debate_history):
        prompt = self.build_prompt(COMPETITION_PROCESS,phase,debate_history)
        print(f"Waiting ai generate {phase} arguement.\n")
        response = ai_call(self.model,prompt)
        print(f"{phase} arguement generate done.\n")
        return response
        
class ReflexionDebater(NormalDebater):
        def __init__(self,topic,stance,model):
            super().__init__(topic,stance,model)
            self.reflexion_memory = []

        def build_prompt(self,COMPETITION_PROCESS,phase,debate_history,reflexion_memory):
            if len(reflexion_memory) == 0 :
                raise ValueError("Reflexion memory doest not exist")
            prompt = REFLEXION_DEBATER_PROMPT.format(competition_process = format_list_of_dictionary_to_string(COMPETITION_PROCESS), 
                                                     topic = self.topic,stance = self.stance,phase = phase, 
                                                     debate_history = format_list_of_dictionary_to_string(debate_history),
                                                     reflexion_memory = "\n".join(reflexion_memory))
            return prompt
        
        def generate_argument(self,COMPETITION_PROCESS,phase,debate_history,reflexion_memory):
            prompt = self.build_prompt(COMPETITION_PROCESS,phase,debate_history,reflexion_memory)
            print(f"Waiting ai generate {phase} arguement.(Reflexion)\n")
            response = ai_call(self.model,prompt)
            print(f"{phase} arguement generate done.\n")
            return response