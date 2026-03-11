from agents.normal_debater import NormalDebater

debate_history = [
    {"phase":"Proponent Opening Phase","content": "abc"},
    {"phase":"Opponent Opening Phase","content": "cde"}
]
competition_format =  f"""
                Aphase
                Bphase
                """
topic = "ABC"
phase = "Bphase"
stance = "Proponent"
model = "gpt-5"

debater = NormalDebater(topic,stance,model)
debater.generate_argument(competition_format,phase,debate_history)
pass