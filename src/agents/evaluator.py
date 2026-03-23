from src.settings.prompts import EVALUATOR_ROLE_PROMPT,JUDGE_PARADIGM,EVALUATOR_INSTRUCTION_PROMPT
from src.settings.configs import EVALUATOR_MODEL
from src.llm.client import ai_call
from src.string_format import  format_list_of_dictionary_to_string
import re
def build_evaluator_prompt(topic,debate_history):
    prompt_list = [
            EVALUATOR_ROLE_PROMPT,
            JUDGE_PARADIGM,
            f"Task: The topic of this debate is: '{topic}'. Based on the actual clash in the debate regarding this specific topic—including argumentation, rebuttal, weighing, comparison, and extension—determine the winner and loser of the round.",### task
            EVALUATOR_INSTRUCTION_PROMPT,
            format_list_of_dictionary_to_string(debate_history),
            ]
    prompt = "\n".join(prompt_list)
    print(prompt)
    return prompt

def parse_evaluate_result(evaluate_result):
    pattern = re.compile(
                r"winning side:(.*?)\n"
                r"losing side:(.*?)\n"
                r"reason for decision:(.*)",
                re.DOTALL
                )
    format_evalute_result = evaluate_result.lower()
    match = pattern.search(format_evalute_result)
    if not match:
        raise ValueError("Invalid judgment format")
    return {
    "winning_side": match.group(1).strip().lower(),
    "losing_side": match.group(2).strip().lower(),
    "reason_for_decision": match.group(3).strip().lower(),  
    }

def evaluate_debate_result(topic,debate_history):
    evaluator_prompt = build_evaluator_prompt(topic,debate_history)
    for attempt in range(3):
        print("evaluating")
        evaluate_result = ai_call(EVALUATOR_MODEL,evaluator_prompt)
        try:
            evaluate_result_dic = parse_evaluate_result(evaluate_result)
            return  evaluate_result_dic
        except ValueError:
            print(f"parse failed, retry {attempt + 1}/{str(3)}")
    raise ValueError("Failed to generate valid evaluation after retries")