from enum import Enum
import json

from analyze_prompt import get_keywords

class Types(Enum):
    MCQ = 0
    FRQ = 1
    SAQ = 2

class Level(Enum):
    NOT_ATTEMPTED = 0
    PRACTICED = 1
    NEEDS_PRACTICE = 2
    MASTERED = 3

class Questions:
    def __init__(self, question_type: Types, save_dir: str) -> None:
        self.question_type = question_type
        self.save_dir = save_dir
    
    def add_question(self, q_json):
        try:
            with open(self.save_dir, 'r') as json_file:
                existing_data = json.load(json_file)
        except (FileNotFoundError, json.JSONDecodeError):
            existing_data = {"MCQ": [], "FRQ": [], "SAQ": []}

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
            "answer": answer,
            "num_correct": 0,
            "num_wrong": 0,
            "state": Level.NOT_ATTEMPTED.value
        }

        self.add_question(q_json = q_json)

    
    def FRQ(self, question, answer):
        q_json = {
            "question": question,
            "answer": answer,
            "num_correct": 0,
            "num_wrong": 0,
            "state": Level.NOT_ATTEMPTED.value
        }

        self.add_question(q_json = q_json)

    def SAQ(self, question):
        q_json = {
            "question": question,
            "answer": get_keywords(question),
            "num_correct": 0,
            "num_wrong": 0,
            "state": Level.NOT_ATTEMPTED.value
        }
        self.add_question(q_json = q_json)
    
    def grade_SAQ(self):
        if (self.question_type != Types.SAQ):
            raise QuestionTypeException("wrong type", "add to SAQ object")
        #TODO implement logic for whether response is adequate


    def add_FRQ_questions(self, file):
        if self.question_type != Types.FRQ:
            raise QuestionTypeException("wrong question type", "add to FRQ object")
        
        with open(file, 'r') as file:
            for line in file:
                vals = line.split("  ")
                self.add_question(
                    q_json = {"question":vals[0].strip(), 
                                "answer":vals[1].strip(),
                                "num_correct": 0,
                                "num_wrong": 0,
                                "state": Level.NOT_ATTEMPTED.value})

    def are_similar_words(self, word_one, word_two, thresh):
        map_one = {}
        map_two = {}
        for c in word_one:
            map_one[c] = map_one.get(c, 0) + 1
        for c in word_two:
            map_two[c] = map_two.get(c, 0) + 1

        if abs(len(map_one.keys()) - len(map_two.keys())) > 2:
            return False
        
        num_same_freqs = 0
        for c in map_one.keys():
            if map_two.keys().__contains__(c) and map_one[c] == map_two[c]:
                num_same_freqs += 1
        freq_same_percent = num_same_freqs / max(len(map_one.keys()), len(map_two.keys()))
        num_chars_same = 0
        for i in range(min(len(word_one), len(word_two))):
            if word_one[i] == word_two[i]:
                num_chars_same += 1
        chars_same_percent = num_chars_same / max(len(word_one), len(word_two))

        if freq_same_percent >= thresh and chars_same_percent >= thresh:
            return True
        return False

        
    def grade_FRQ(self, response, answer, word_thresh = 0.8, index_thresh = 1, tot_thresh = 1) -> bool:
        #first sort and check how diff from sorted Q and A are (also track initial indices to see how many are matching)
        resp_words = response.split(" ")
        answer_words = answer.split(" ")
        r_tuple = [(i, resp_words[i]) for i in range(len(resp_words))]
        a_tuple = [(i, answer_words[i]) for i in range(len(answer_words))]
        sort_func = lambda tuple: tuple[0]
        r_tuple.sort(key = sort_func)
        a_tuple.sort(key = sort_func)

        num_words_same = 0
        num_indices_same = 0
        for i in range(min(len(resp_words), len(answer_words))):
            r = r_tuple[i]
            a = a_tuple[i]
            if self.are_similar_words(r[1], a[1], word_thresh):
                num_words_same += 1
                if r[0] == a[0]:
                    num_indices_same += 1

        num_words = max(len(resp_words), len(answer_words))
        words_same_percent = num_words_same / num_words
        indices_same_percent = num_indices_same / num_words
        if words_same_percent >= tot_thresh and indices_same_percent >= index_thresh:
            return True
        return False
            

questions = Questions(Types.FRQ, "")
#print(questions.are_similar_words("mccollouch v maryland", "mccoullock v Maryland", 0.8))
print(questions.grade_FRQ("i like rice", "i like riice"))

class QuestionTypeException(Exception):
        def __init__(self, message, errors):     
            super().__init__(message)
            self.errors = errors
