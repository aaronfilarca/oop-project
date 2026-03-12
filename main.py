import csv
import random
import os
from datetime import datetime

# ANSI escape codes for coloring terminal text
class Colors:
    GREEN = "\033[92m"
    RED = "\033[91m"
    CYAN = "\033[96m"
    YELLOW = "\033[93m"
    MAGENTA = "\033[95m"
    WHITE = "\033[97m"
    RESET = "\033[0m"
    BOLD = "\033[1m"


def shuffle(list1):
    # Iterate through the list and swap each element with another at a random index
    for i in range(0, len(list1)):
        new = random.randint(0, len(list1) - 1)
        temp = list1[new]
        list1[new] = list1[i]
        list1[i] = temp
    return list1


def main():
    # List all files in the quiz directory
    availableSets = os.listdir("./quiz_sets/")
    selectedSet = -1

    # Loop until the user provides a valid integer index for a quiz set
    while selectedSet == -1:
        try:
            for i in range(0, len(availableSets)):
                print(f"[{i}] {availableSets[i]}")
            selectedSet = int(input("Enter the index of the quiz set you want to take: "))
        except ValueError:
            print("Input must be index integer.")
            selectedSet = -1
            continue

        if selectedSet >= len(availableSets):
            print(f"You must enter a value less than {len(availableSets)}")
            selectedSet = -1
            continue

    # Ensure the user enters a non-empty name
    userName = ""
    while userName == "":
        userName = input("Enter your name: ").strip()
        if userName == "":
            print("Please enter your name.")

    print(f"\n{Colors.CYAN}Good luck, {userName}!{Colors.RESET}")

    startTime = datetime.now()  # Start the timer

    quiz = []
    totalScore = 0

    with open(f"./quiz_sets/{availableSets[selectedSet]}", "r", newline="") as file:
        reader = csv.reader(file, delimiter=",")
        next(reader)
        for row in reader:
            question = row.pop(0)  # First column is the question
            requiredAnswers = row.pop(0).split("&&")  # Second column contains correct answers, separated by &&
            choices = row  # Remaining columns are the multiple-choice options

            # Store the question data and shuffle the choice order
            quiz.append({"question": question, "requiredAnswers": requiredAnswers, "choices": shuffle(choices)})

        # Shuffle the order of the questions themselves
        quiz = shuffle(quiz)

    for number in quiz:
        validResponseLetter = []

        while len(validResponseLetter) == 0:
            print(f"\n{Colors.WHITE}{Colors.BOLD}{number['question']}{Colors.RESET}")

            # Assign letters A-H to the available choices
            letters = ["A", "B", "C", "D", "E", "F", "G", "H"]
            for i in range(0, len(number["choices"])):
                print(f"{letters[i]}. {number['choices'][i]}")

            # Handle single vs. multiple answer inputs
            if len(number["requiredAnswers"]) == 1:
                responseLetters = input("Enter the letter of the correct answer: ").upper().split(" ")
                if len(responseLetters) != 1:
                    print(f"{Colors.YELLOW}Invalid input. Use a single letter.{Colors.RESET}")
                    continue
            else:
                responseLetters = input("Enter all letters (separated by space): ").upper().split(" ")

            # Convert letter input back into the actual choice text
            for responseLetter in responseLetters:
                if responseLetter in letters and letters.index(responseLetter) < len(number["choices"]):
                    validResponseLetter.append(number["choices"][letters.index(responseLetter)])
                else:
                    print(f"{Colors.YELLOW}Invalid letter choice.{Colors.RESET}")
                    validResponseLetter = []

        # Compare sets to find items missing from user's answer or extra items they included
        missingOrExcess = set(validResponseLetter) ^ set(number["requiredAnswers"])

        # Calculate partial credit: 1 point minus a penalty for every error
        score = 1 - len(missingOrExcess) / len(number["requiredAnswers"])
        if score < 0:
            score = 0

        correct_answers = ", ".join(number["requiredAnswers"])

        # Visual feedback based on how correct the user was
        if score == 1.0:
            print(f"{Colors.GREEN}Correct!{Colors.RESET} Score: {score:.2f}\n")
        elif score == 0.0:
            print(f"{Colors.RED}Incorrect.{Colors.RESET} Answer(s): {Colors.GREEN}{correct_answers}{Colors.RESET}\n")
        else:
            print(f"{Colors.YELLOW}Partial Credit.{Colors.RESET} Answer(s): {Colors.GREEN}{correct_answers}{Colors.RESET}\n")

        totalScore += score

    scorePercent = totalScore * 100 / len(quiz)
    print(f"Final Score: {Colors.BOLD}{scorePercent:.2f}%{Colors.RESET}")

    # Final words of encouragement
    if scorePercent == 100:
        print(f"{Colors.GREEN}Perfect score! Congratulations {Colors.MAGENTA}{userName}!{Colors.RESET}")
    elif scorePercent >= 70:
        print(f"{Colors.CYAN}Great job {Colors.MAGENTA}{userName}! Almost there.{Colors.RESET}")
    else:
        print(f"{Colors.YELLOW}Good effort {Colors.MAGENTA}{userName}! Keep studying.{Colors.RESET}")

    # Log the result: Name, Score, Quiz File, Timestamp, and Time Taken
    with open("scores.csv", "a", newline="") as file:
        writer = csv.writer(file, delimiter=",")
        writer.writerow([userName, f"{scorePercent:.2f}%", availableSets[selectedSet], datetime.now(), datetime.now() - startTime])


if __name__ == "__main__":
    main()
