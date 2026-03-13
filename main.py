import csv
import random
import os
from datetime import datetime, timedelta

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
    # In-place shuffle by swapping each position with a random index.
    for i in range(0, len(list1)):
        new = random.randint(0, len(list1) - 1)
        temp = list1[new]
        list1[new] = list1[i]
        list1[i] = temp
    return list1

def main():
    # Load runtime configuration once at startup.
    config = {}
    with open ("config.csv", "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            config[row["Option"]] = row["Value"]

    timerMinutes = float(config["TimerMinutes"])
    timerSeconds = timerMinutes * 60

    # Collect required student identity details with validation.
    userName = ""
    while userName == "":
        userName = input(f"{Colors.BLUE}Enter your name: {Colors.RESET}").strip()
        if userName == "":
            print(f"{Colors.RED}Name cannot be empty. Please enter your name.{Colors.RESET}")

    studentID = 0
    while studentID == 0:
        try:
            studentID = str(int(input(f"{Colors.BLUE}Enter your Student ID (numbers only): {Colors.RESET}").strip()))
        except ValueError:
            print(f"{Colors.RED}Please enter a valid Student ID.{Colors.RESET}")
            studentID = 0

    print()

       # Main loop: show available quizzes, run one attempt, then ask whether to continue.
    while True:
        # Refresh scores each cycle so attempts remain accurate.
        scores = []
        with open("scores.csv", "r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                scores.append(row)

        availableSets = os.listdir("./quiz_sets/")
        quizAttempts = []
        maxAttempts = int(config["MaxAttempts"])

        # Build and display per-quiz attempt counters for this student.
        print("Index\tQuiz Set\tAttempts Used/Allowed")
        for i in range(0, len(availableSets)):
            submittedAttempts = 0
            for row in scores:
                if row["Student ID"] == str(studentID) and row["Quiz File"] == availableSets[i]:
                    submittedAttempts += 1
            quizAttempts.append({"Quiz File": availableSets[i], "Attempts": submittedAttempts})
            print(f"[{i}]\t{availableSets[i]}\tAttempts: {submittedAttempts}/{maxAttempts}")

        print()

        # Prompt for a valid quiz selection; -1 exits the app.
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

        print()

        # Parse selected quiz CSV into question objects, then randomize choices and question order.
        quiz = []
        with open(f"./quiz_sets/{availableSets[selectedSet]}", "r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file, delimiter=",")
            next(reader)
            for row in reader:
                # Expected CSV layout per row: question, required_answers, choice1, choice2, ...
                question = row.pop(0)
                # Multiple correct answers are encoded as "answer1&&answer2" in the source CSV.
                requiredAnswers = row.pop(0).split("&&")
                choices = [choice for choice in row if (choice != "")]

                quiz.append({"question": question, "requiredAnswers": requiredAnswers, "choices": shuffle(choices)})

        quiz = shuffle(quiz)

        maxNumberOfItems = int(config["MaxNumberOfItems"])
        quiz = quiz[:maxNumberOfItems]

        # Confirm the timed quiz policy before starting the attempt.
        if timerSeconds > 0:
            timerText = f"{timerMinutes} minute(s)"
            startTimedQuiz = input(f"{Colors.RED}This quiz is timed. You will have {timerText}. Start now? (Y/N): {Colors.RESET}").strip().upper()
            if startTimedQuiz != "Y":
                print(f"{Colors.CYAN}Quiz start cancelled. Returning to quiz selection.{Colors.RESET}")
                print()
                continue

        print()
        print(f"Good luck, {userName}!")
        print()

        # Start timing this attempt for score log duration.
        startTime = datetime.now()
        if timerSeconds > 0:
            endTime = startTime + timedelta(seconds=timerSeconds)

        # Ask each question, validate answer format, and compute per-item score.
        totalScore = 0
        questionsAnswered = 0

        for number in quiz:
            if timerSeconds > 0:
                remainingSeconds = int((endTime - datetime.now()).total_seconds())
                if remainingSeconds < 0:
                    print(f"{Colors.RED}Time is up!{Colors.RESET}")
                    print()
                    break

                minutesLeft = remainingSeconds // 60
                secondsLeft = remainingSeconds % 60
                print(f"{Colors.RED}Time left: {minutesLeft:02d}:{secondsLeft:02d}{Colors.RESET}")

            validResponseLetter = []

            while len(validResponseLetter) == 0:
                print(f"{Colors.MAGENTA}{number['question']}{Colors.RESET}")

                letters = ["A", "B", "C", "D", "E", "F", "G", "H"]
                for i in range(0, len(number["choices"])):
                    print(f"[{letters[i]}] {number['choices'][i]}")

                if len(number["requiredAnswers"]) == 1:
                    responseLetters = input(f"{Colors.BLUE}Enter the letter of the correct answer: {Colors.RESET}").upper().split(" ")
                    if len(responseLetters) != 1:
                        print(f"{Colors.RED}Invalid input. Use a single letter.{Colors.RESET}")
                        continue
                else:
                    responseLetters = input(f"{Colors.BLUE}Enter all letters (separated by space): {Colors.RESET}").upper().split(" ")

                for responseLetter in responseLetters:
                    # Convert letter input (A/B/C...) back to the corresponding choice text.
                    if responseLetter in letters and letters.index(responseLetter) < len(number["choices"]):
                        validResponseLetter.append(number["choices"][letters.index(responseLetter)])
                    else:
                        print(f"{Colors.RED}Invalid letter choice.{Colors.RESET}")
                        # Reset and re-ask the same question if any invalid token is entered.
                        validResponseLetter = []

            # Symmetric difference gives all mismatches: missing correct answers or extra wrong picks.
            missingOrExcess = set(validResponseLetter) ^ set(number["requiredAnswers"])

            # Partial credit: each mismatch subtracts an equal fraction from a perfect score of 1.0.
            score = 1 - len(missingOrExcess) / len(number["requiredAnswers"])
            if score < 0:
                score = 0

            if config["ShowScoreAndCorrectAnswers"].upper() == "TRUE":
                correct_answers = ", ".join(number["requiredAnswers"])

                if score == 1.0:
                    print(f"{Colors.GREEN}Correct!{Colors.RESET} Score: {score:.2f}")
                elif score == 0.0:
                    print(f"{Colors.RED}Incorrect.{Colors.RESET} Score: {score:.2f}. Answer(s): {Colors.GREEN}{correct_answers}{Colors.RESET}")
                else:
                    print(f"{Colors.YELLOW}Partial Credit.{Colors.RESET} Score: {score:.2f}. Answer(s): {Colors.GREEN}{correct_answers}{Colors.RESET}")

            totalScore += score
            questionsAnswered += 1

            # After each question, update the CSV with the current progress so that if the app is closed mid-quiz, the student still has a record of their attempt and partial score.
            attemptDateTaken = str(startTime)
            scores = [row for row in scores if  row["Date Taken"] != attemptDateTaken]

            scores.append({"Name": userName,"Student ID": studentID,"Quiz File": availableSets[selectedSet],"Score": f"{(totalScore / len(quiz)) * 100:.2f}%","Questions Answered": questionsAnswered,"Questions Total": len(quiz),"Date Taken": attemptDateTaken,"Duration": str(datetime.now() - startTime)})

            with open("scores.csv", "w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=["Name", "Student ID", "Quiz File", "Score", "Questions Answered", "Questions Total", "Date Taken", "Duration"])
                writer.writeheader()
                writer.writerows(scores)

        # Summarize result and provide user feedback.
        print()
        scorePercent = totalScore * 100 / len(quiz)
        print(f"{Colors.MAGENTA}Final Score: {scorePercent:.2f}%{Colors.RESET}")

        if scorePercent == 100:
            print(f"{Colors.GREEN}Perfect score! Congratulations {userName}!{Colors.RESET}")
        elif scorePercent >= 70:
            print(f"{Colors.GREEN}Great job {userName}! Almost there.{Colors.RESET}")
        else:
            print(f"{Colors.YELLOW}Good effort {userName}! Keep studying.{Colors.RESET}")

        # Exit or continue another attempt based on user choice.
        print()
        if input(f"{Colors.BLUE}Do you want to take another quiz? (Y/N): {Colors.RESET}").upper() == "N":
            print("Goodbye!")
            break

if __name__ == "__main__":
    main()
