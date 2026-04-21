from datasets import load_dataset

ds = load_dataset("ibm-research/debate_speeches",split="train")
topics = []
seen = set()

for row in ds:
    topic = row["topic"].strip()
    if topic and topic not in seen:
        seen.add(topic)
        topics.append(topic)

with open("topics_dataset.txt", "w", encoding="utf-8") as f:
    for topic in topics:
        f.write(topic + "\n")