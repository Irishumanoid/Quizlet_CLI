from enum import Enum
import json

class Types(Enum):
    MCQ = 0
    FRQ = 1

class Questions:
    def __init__(self, question_type: Types, save_dir: str) -> None:
        self.question_type = question_type
        self.save_dir = save_dir
    
    def add_question(self, q_json):
        try:
            with open(self.save_dir, 'r') as json_file:
                existing_data = json.load(json_file)
        except (FileNotFoundError, json.JSONDecodeError):
            existing_data = {"MCQ": [], "FRQ": []}

        # append the new question to entries if it doesn't already exist
        if not existing_data[str(self.question_type.name)].__contains__(q_json):
            existing_data[str(self.question_type.name)].append(q_json)

        # save the updated data back to the file
        with open(self.save_dir, 'w') as json_file:
            json.dump(existing_data, json_file, indent=2)


    def MCQ(self, question, choices: list, answer_index: int):
        formatted_choices = {chr(i + 65): choice for i, choice in enumerate(choices)}
        answer = chr(answer_index + 65)

        q_json = {
            "question": question,
            "choices": formatted_choices,
            "answer": answer
        }

        self.add_question(q_json = q_json)

    
    def FRQ(self, question, answer):
        q_json = {
            "question": question,
            "answer": answer
        }

        self.add_question(q_json = q_json)

    def add_FRQ_questions(self, file):
        with open(file, 'r') as file:
            for line in file:
                vals = line.split("  ")
                self.add_question(q_json = {"question":vals[0].strip(), "answer":vals[1].strip()})

