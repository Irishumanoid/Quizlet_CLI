from question_types import Questions, Types, Level
from analyze_prompt import sufficient_answer_criteria
import emoji
import json
from random import randint
import os

def generate_question(data: list, test_mode: str, file_name: str, correct, wrong, random_index):
    print("question is: " + data[test_mode][random_index]["question"])
    answer = ""

    if test_mode == "MCQ":
        for (key, value) in data[test_mode][random_index]["choices"].items():
            print(str(key) + " -- " + value)
    answer = input("answer: \n")

    correct_answer = data[test_mode][random_index]["answer"]
    if answer == correct_answer or (test_mode == "SAQ" and sufficient_answer_criteria(answer, correct_answer)):
        correct += 1
    elif answer == "q":
        return
    else:
        print("wrong, the correct answer is: " + str(correct_answer) + "\n")
        wrong += 1
        
    if correct + wrong > 0:
        with open(file_name, 'r+') as f:
            d = json.load(f)
            d[test_mode][random_index]["num_wrong"] = wrong
            d[test_mode][random_index]["num_correct"] = correct

            percent_correct = correct/(correct + wrong)
            if percent_correct < 0.5:
                d[test_mode][random_index]["state"] = Level.NEEDS_PRACTICE.value
            elif percent_correct < 0.8:
                d[test_mode][random_index]["state"] = Level.PRACTICED.value
            elif correct >= 3:
                d[test_mode][random_index]["state"] = Level.MASTERED.value

            f.seek(0)
            json.dump(d, f, indent=4)
            f.truncate()
    
    return generate_question(data, test_mode, file_name, correct, wrong, randint(0, len(data[test_mode])-1))


def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')


def main():
    print("Welcome to your new favorite Quizlet rip off! " + emoji.emojize(":winking_face_with_tongue:"))
    set_name = input("Please enter a name for your set (and press q to quit at any time, c to change test mode): ")

    q_test_frq = Questions(Types.FRQ, "sessions/" + set_name + ".json")
    q_test_frq.FRQ("je vous prie d'accepter l'expression de mes salutations", "I beg you to accept my goodbyes")
    q_test_frq.add_FRQ_questions("frq_sets/frq.txt")

    q_test_mcq = Questions(Types.MCQ,  "sessions/" + set_name + ".json")
    q_test_mcq.MCQ("who are you?", ["me", "them", "they"], 0)

    q_test_saq = Questions(Types.SAQ,  "sessions/" + set_name + ".json")
    q_test_saq.SAQ("what is the meawning of life")

    with open("sessions/" + set_name + ".json", "r") as file:
        test_mode = input("choose a test mode: MCQ or FRQ -- ").strip()
        try:
            data = json.load(file)
            random_index = randint(0, len(data[test_mode])-1)
            generate_question(
                data = data, 
                test_mode = test_mode, 
                file_name = "sessions/" + set_name + ".json", 
                correct=data[test_mode][random_index]["num_correct"], 
                wrong=data[test_mode][random_index]["num_wrong"], 
                random_index=random_index)        
        except ValueError:
            print("invalid question type")



if __name__ == "__main__":
    main()
    clear_console()


#ideas
'''
-SAQ section that uses AI to get the gist of the response to see if it's correct
-keeping track of answers correct vs wrong
-weighting on questions showed (mastered not showed, needs practice showed the most)
'''