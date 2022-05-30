import os, requests, sys, time
from random import shuffle
import pyinputplus as pyip
from supabase import create_client, Client

#Database Connection
supabase_url = "https://hqatoyyncrwdojrhwygi.supabase.co"
supabase_key = "SUPABASE_KEY"
client: Client = create_client(supabase_url, supabase_key)

#Get Questions+Answers from Open Trivia Database
def get_questions() -> dict:
    res = requests.get("https://opentdb.com/api.php?amount=10&type=multiple")
    if res.status_code != 200:
        return res.json()
    questions = res.json()
    return questions


answer_keys = ["a", "b", "c", "d"]

#Start a new game (Quiz-logic)
def new_game(score: int) -> int:

    questions = get_questions()
    questions = questions['results']

    # iterate through question-set and append answer-options into single list
    for question in questions:
        now = time.time()
        print("-------------------------")
        print(question["question"])
        answers: list = question['incorrect_answers']
        answers.append(question['correct_answer'])
        
        shuffle(answers)

        answersDict = {
            "a": answers[0],
            "b": answers[1],
            "c": answers[2],
            "d": answers[3],
        }

        # print out answer-options
        for key in answersDict:
            print("{})\t{}".format(key, answersDict[key]))

        guess = pyip.inputMenu(answer_keys).lower()

        answer_given_at = time.time()

        # quiz logic - check if answer is correct and in time
        if question['correct_answer'] == answersDict[guess] and answer_given_at - now <= 20:
            score += 1
        elif question['correct_answer'] == answersDict[guess]:
            print("you answered correct, but exceeded the time limit - you will get no points!")
        else:
            print("you exceeded the time limit - you will get no points!")
    print(f"Score: {score}/10")
    return score

# query to play again --> new game
def play_again() -> bool:

    response = pyip.inputYesNo("Do you want to play again? (yes or no): ")
    response = response.upper()

    return response == "YES"

# logic to enter name
gamertag = pyip.inputStr("Please enter your gamertag:\t")

if len(gamertag) == 0:
    print("enter your gamertag!!!!!")
    sys.exit(1)

total_score = new_game(0)


while play_again():
    total_score = new_game(total_score)

# post highscore and name to database 
client.postgrest.from_("highscores").upsert({
    "name": gamertag,
    "score": total_score
}).execute()

# get highscores to display at the end of the game
res = client.postgrest.from_("highscores").select("*").execute()
highscores: list = res.data
highscores.sort(key=lambda x: x.get("score"), reverse=True)

print("the current highscores are:")
print()

for score in highscores:
    print("{}: {}".format(score["name"], score["score"]))
