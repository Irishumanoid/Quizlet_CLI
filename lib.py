from question_types import Questions, Types
import emoji
import json
from random import randint
import os

def generate_question(data: list, test_mode: str):
    random_index = randint(0, len(data)-1)
    print("question is: " + data[random_index]["question"])
    answer = ""

    if test_mode == "MCQ":
        for (key, value) in data[random_index]["choices"].items():
            print(str(key) + " -- " + value)
    answer = input("answer: \n")

    if answer == data[random_index]["answer"]:
        print("correct! \n")
    elif answer == "q":
        return
    else:
        print("wrong, the correct answer is: " + data[random_index]["answer"] + "\n")
    
    return generate_question(data, test_mode)


def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')


def main():
    print("Welcome to your new favorite Quizlet rip off! " + emoji.emojize(":winking_face_with_tongue:"))
    set_name = input("Please enter a name for your set (and press q to quit at any time, c to change test mode): ")

    q_test_frq = Questions(Types.FRQ, "sessions/" + set_name + ".json")
    q_test_frq.FRQ("je vous prie d'accepter l'expression de mes salutations", "I beg you to accept my goodbyes")
    q_test_frq.add_FRQ_questions("frq_sets/frq.txt")

    q_test_mcq = Questions(Types.MCQ,  "sessions/" + set_name + ".json")
    q_test_mcq.MCQ("what is my name?", ["Iris", "Other"], 0)
    q_test_mcq.MCQ("where do I go to school?", ["Ballard", "Lincoln", "Lakeside"], 1)
    

    with open("sessions/" + set_name + ".json", "r") as file:
        test_mode = input("choose a test mode: MCQ or FRQ -- ").strip()
        try:
            data = json.load(file)[test_mode]
            generate_question(data = data, test_mode = test_mode)        
        except ValueError:
            print("invalid question type")



if __name__ == "__main__":
    main()