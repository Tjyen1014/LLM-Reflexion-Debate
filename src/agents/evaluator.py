from src.settings.prompts import EVALUATOR_PROMPT
from src.settings.configs import EVALUATOR_MODEL
from src.llm.client import ai_call
from src.string_format import  format_list_of_dictionary_to_string
from openai import OpenAI
from dotenv import load_dotenv
import os
import cohere
import re
from google import genai

load_dotenv(override=True)
openai_client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
gemini_client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
cohere_client = cohere.ClientV2(api_key=os.environ["COHERE_API_KEY"])
OPENAI_EVALUATOR_MODEL = "gpt-5-mini-2025-08-07"
GEMINI_EVALUATOR_MODEL = "gemini-2.5-flash"
COHERE_EVALUATOR_MODEL = "command-r-08-2024"

def build_evaluator_prompt(topic,debate_history):
    prompt = EVALUATOR_PROMPT.format(topic = topic,debate_trajectory=format_list_of_dictionary_to_string(debate_history))
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

def gpt_call(ai_model, prompt):
    response = openai_client.responses.create(
        model=ai_model,
        input=prompt
    )
    return response.output_text

def gemini_call(ai_model, prompt):
    response = gemini_client.models.generate_content(
        model=ai_model,
        contents=prompt
    )
    return response.text

def cohere_call(ai_model, prompt):
    response = cohere_client.chat(
        model=ai_model,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.message.content[0].text

def three_ai_judge_evaluate(evaluator_prompt):
    evaluate_result_list = []
    print("waiting gpt judge\n")
    evaluate_result_list.append(gpt_call(OPENAI_EVALUATOR_MODEL, evaluator_prompt))
    print("waiting gemini judge\n")
    evaluate_result_list.append(gemini_call(GEMINI_EVALUATOR_MODEL, evaluator_prompt))
    print("waiting cohere judge\n")
    evaluate_result_list.append(cohere_call(COHERE_EVALUATOR_MODEL, evaluator_prompt))

    three_ai_judge_evaluate_result_dic = {}
    evaluate_result_number = 0
    evaluate_result_verdict = ""
    try:
        for i in range(3):
            evaluate_result_dic = parse_evaluate_result(evaluate_result_list[i])
            if evaluate_result_dic['winning_side'].lower().strip() == "proponent":
                evaluate_result_number = evaluate_result_number + 1
            elif evaluate_result_dic['winning_side'].lower().strip() == "opponent":
                evaluate_result_number = evaluate_result_number - 1  
            else:
                raise ValueError("Invalid winning_side")
            evaluate_result_verdict = evaluate_result_verdict + f"Judge {i+1}. \nWinner:{evaluate_result_dic['winning_side']}\nLoser:{evaluate_result_dic['losing_side']} \nReason for decision:  {evaluate_result_dic['reason_for_decision']}\n\n"

        if evaluate_result_number > 0:
            three_ai_judge_evaluate_result_dic["winning_side"] = "proponent"
            three_ai_judge_evaluate_result_dic["losing_side"] = "opponent"
        elif evaluate_result_number < 0:
            three_ai_judge_evaluate_result_dic["winning_side"] = "opponent"
            three_ai_judge_evaluate_result_dic["losing_side"] = "proponent"
        elif evaluate_result_number == 0:
            raise ValueError("Tie vote")

        three_ai_judge_evaluate_result_dic["reason_for_decision"] = evaluate_result_verdict
        return three_ai_judge_evaluate_result_dic
    except ValueError as e:
        raise ValueError(f"Judge evaluation failed: {e}")


def evaluate_debate_result(topic,debate_history):
    evaluator_prompt = build_evaluator_prompt(topic,debate_history)
    evaluate_result_dic = three_ai_judge_evaluate(evaluator_prompt)
    print("winning_side:", evaluate_result_dic["winning_side"])
    print("losing_side:", evaluate_result_dic["losing_side"])
    print("reason_for_decision:")
    print(evaluate_result_dic["reason_for_decision"])
    return evaluate_result_dic

# def evaluate_debate_result(topic,debate_history):
#     evaluator_prompt = build_evaluator_prompt(topic,debate_history)
#     for attempt in range(3):
#         print("evaluating")
#         evaluate_result = ai_call(EVALUATOR_MODEL,evaluator_prompt)
#         try:
#             evaluate_result_dic = parse_evaluate_result(evaluate_result)
#             print(evaluate_result_dic['losing_side'] + "\n")
#             return  evaluate_result_dic
#         except ValueError:
#             print(f"parse failed, retry {attempt + 1}/{str(3)}")
#     raise ValueError("Failed to generate valid evaluation after retries")