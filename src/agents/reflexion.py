from src.settings.prompts import DEBATE_REFLEXTION_PROMPT_TEMPLATE
from src.settings.configs import REFLEXION_MODEL
from src.llm.client import ai_call
def generate_debate_reflexion(debate_trajectory,reflexion_debater_stance,debate_judgment_rationale):
        reflexion_prompt = DEBATE_REFLEXTION_PROMPT_TEMPLATE.format(debate_trajectory = debate_trajectory,reflexion_debater_stance = reflexion_debater_stance,debate_judgment_rationale = debate_judgment_rationale)
        reflexion_content = ai_call(REFLEXION_MODEL,reflexion_prompt)
        return reflexion_content

