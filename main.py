import csv
import random
import os
from datetime import datetime

# ANSI escape codes for coloring terminal text
class Colors:
    GREEN = "\033[92m"
    RED = "\033[91m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"
    YELLOW = "\033[93m"
    MAGENTA = "\033[95m"
    DIM_WHITE = "\033[2;37m"
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
    config = {}
    with open ("config.csv", "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            config[row["Option"]] = row["Value"]

        # Ensure the user enters a non-empty name
    userName = ""
    while userName == "":
        userName = input(f"{Colors.BLUE}Enter your name: {Colors.RESET}").strip()
        if userName == "":
            print(f"{Colors.RED}Name cannot be empty. Please enter your name.{Colors.RESET}")

    # Ensure the user enters a Student ID
    studentID = 0
    while studentID == 0:
        try:
            studentID = str(int(input(f"{Colors.BLUE}Enter your Student ID (numbers only): {Colors.RESET}").strip()))
        except ValueError:
            print(f"{Colors.RED}Please enter a valid Student ID.{Colors.RESET}")
            studentID = 0

    print()
    
    while True:
        # Read configuration settings from config.csv into a dictionary

        scores = []
        with open("scores.csv", "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                scores.append(row)
        
        # List all files in the quiz directory
        availableSets = os.listdir("./quiz_sets/")


        quizAttempts = []
        maxAttempts = int(config["MaxAttempts"])
        print("Index\tQuiz Set\tAttempts Used/Allowed")
        for i in range(0, len(availableSets)):
            submittedAttempts = 0
            for row in scores:
                if row["Student ID"] == str(studentID) and row["Quiz File"] == availableSets[i]:
                    submittedAttempts += 1
            
            # append to list
            quizAttempts.append({"Quiz File": availableSets[i], "Attempts": submittedAttempts})
            print(f"[{i}]\t{availableSets[i]}\tAttempts: {submittedAttempts}/{maxAttempts}")

        # Ask the user which quiz set they want to take
        selectedSet = -2
        while selectedSet == -2:
            try:
                selectedSet = int(input(f"{Colors.BLUE}Enter the index of the quiz set you want to take (enter -1 to quit): {Colors.RESET}").strip())
            except ValueError:
                print(f"{Colors.RED}Invalid input. Please enter a number.{Colors.RESET}")
                selectedSet = -2
                continue

            if selectedSet < 0:
                break
            elif selectedSet >= len(availableSets):
                print(f"{Colors.RED}You must enter a value less than {len(availableSets)}.{Colors.RESET}")
                selectedSet = -2
                continue
            elif quizAttempts[selectedSet]["Attempts"] >= maxAttempts:
                print(f"{Colors.RED}You have used all {maxAttempts} attempts for this quiz set. Please select a different one.{Colors.RESET}")
                selectedSet = -2
                continue

        if selectedSet < 0:
            print("Goodbye!")
            break

        print(f"\nGood luck, {userName}!")

        startTime = datetime.now()  # Start the timer

        quiz = []
        totalScore = 0

        with open(f"./quiz_sets/{availableSets[selectedSet]}", "r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file, delimiter=",")
            next(reader)
            for row in reader:
                question = row.pop(0)  # First column is the question
                requiredAnswers = row.pop(0).split("&&")  # Second column contains correct answers, separated by &&
                choices = [choice for choice in row if (choice != "")]

                # Store the question data and shuffle the choice order
                quiz.append({"question": question, "requiredAnswers": requiredAnswers, "choices": shuffle(choices)})

        # Shuffle the order of the questions themselves
        quiz = shuffle(quiz)

        maxNumberOfItems = int(config["MaxNumberOfItems"])
        quiz = quiz[:maxNumberOfItems]

        for number in quiz:
            validResponseLetter = []

            while len(validResponseLetter) == 0:
                print(f"\n{Colors.MAGENTA}{number['question']}{Colors.RESET}")

                # Assign letters A-H to the available choices
                letters = ["A", "B", "C", "D", "E", "F", "G", "H"]
                for i in range(0, len(number["choices"])):
                    print(f"[{letters[i]}] {number['choices'][i]}")

                # Handle single vs. multiple answer inputs
                if len(number["requiredAnswers"]) == 1:
                    responseLetters = input(f"{Colors.BLUE}Enter the letter of the correct answer: {Colors.RESET}").upper().split(" ")
                    if len(responseLetters) != 1:
                        print(f"{Colors.RED}Invalid input. Use a single letter.{Colors.RESET}")
                        continue
                else:
                    responseLetters = input(f"{Colors.BLUE}Enter all letters (separated by space): {Colors.RESET}").upper().split(" ")

                # Convert letter input back into the actual choice text
                for responseLetter in responseLetters:
                    if responseLetter in letters and letters.index(responseLetter) < len(number["choices"]):
                        validResponseLetter.append(number["choices"][letters.index(responseLetter)])
                    else:
                        print(f"{Colors.RED}Invalid letter choice.{Colors.RESET}")
                        validResponseLetter = []

            # Compare sets to find items missing from user's answer or extra items they included
            missingOrExcess = set(validResponseLetter) ^ set(number["requiredAnswers"])

            # Calculate partial credit: 1 point minus a penalty for every error
            score = 1 - len(missingOrExcess) / len(number["requiredAnswers"])
            if score < 0:
                score = 0

            if config["ShowScoreAndCorrectAnswers"].upper() == "TRUE":
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
        print(f"{Colors.MAGENTA}Final Score: {scorePercent:.2f}%{Colors.RESET}")

        # Final words of encouragement
        if scorePercent == 100:
            print(f"{Colors.GREEN}Perfect score! Congratulations {userName}!{Colors.RESET}")
        elif scorePercent >= 70:
            print(f"{Colors.GREEN}Great job {userName}! Almost there.{Colors.RESET}")
        else:
            print(f"{Colors.YELLOW}Good effort {userName}! Keep studying.{Colors.RESET}")

        # Log the result: Name, Score, Quiz File, Timestamp, and Time Taken
        with open("scores.csv", "a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file, delimiter=",")
            writer.writerow([userName, studentID, availableSets[selectedSet], f"{scorePercent:.2f}%", datetime.now(), datetime.now() - startTime])

        if input(f"{Colors.BLUE}Do you want to take another quiz? (Y/N): {Colors.RESET}").upper() == "N":
            print("Goodbye!")
            break


if __name__ == "__main__":
    main()
