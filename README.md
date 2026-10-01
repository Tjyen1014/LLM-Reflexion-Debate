# LLM-Reflexion-Debate
An LLM debate project that uses evaluator feedback and self-reflection to improve argument strategy across rounds.

1. Project Overview

In debate training, the preparation process usually involves simulated debates, post-match review, strategic reflection, and applying revised strategies in the next practice round. Debaters observe the results, continue adjusting their approach, and repeat this process until the actual competition.

This training cycle is similar to the Reflexion framework proposed by Noah Shinn, which improves language agents on multi-step reasoning tasks such as HotPotQA and ALFWorld through self-reflection and verbal feedback. Inspired by this idea, this project aims to apply the logic of Reflexion to AI debate agents and explore whether it can improve their argumentation and reasoning performance.

2. Learning Goals

Practice Python project development

Practice basic Git and GitHub workflows

Practice using APIs and Python libraries

Practice breaking down a research idea into executable modules

Practice recording experiments and organizing results

3. Planned System Modules

Normal Debater AI Agent: an AI debater without a reflection mechanism

Evaluator: an AI debate judge

Reflector: a module that generates reflections based on debate performance and feedback

Reflexion AI Agent: an AI debater with a reflection mechanism

Reflection Memory: a memory component for storing reflections from previous rounds

Experiment Runner: a module for connecting and managing the overall experiment pipeline

4. Current Status

Current status: 
Experiments on 100 debate topics have been completed. Number of initial losers that won after reflection:
- GPT-5 mini vs GPT-5 mini (single judge): 72 / 100
- GPT-5 nano (reflecting side) vs GPT-5 mini: 13 / 100
- GPT-5 mini vs GPT-5 mini (three-judge majority vote): 91 / 100

Ongoing work: developing quantitative methods to evaluate answer quality in open-ended reasoning.

5. Roadmap

Phase 1: Environment setup (Completed)

Phase 2: API call testing  (Completed)

Phase 3: Simple debate prototype  (Completed)

Phase 4: Add human judgment and test the full debate-reflection workflow  (Completed)

Phase 5: Add multiple topics and multi-round experiments  (Completed)

Phase 6: Add AI judging / automated evaluation  (Completed)
