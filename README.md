# PyQuiz

PyQuiz is a terminal-based Python quiz app for running timed, repeatable quiz sets from CSV files. Students can choose a quiz, answer randomized questions, and have their scores saved automatically.

## Features

- Runs fully in the terminal with simple text prompts
- Loads quiz settings from `config.csv`
- Reads quiz banks from the `quiz_sets/` folder
- Supports single-answer and multiple-answer questions
- Randomizes both question order and answer choices
- Limits attempts per student per quiz file
- Stores progress and final results in `scores.csv`
- Supports timed quizzes

## Project Structure

```text
oop-project/
|-- main.py
|-- config.csv
|-- scores.csv
`-- quiz_sets/
    |-- math.csv
    `-- science.csv
```

## Requirements

- Python 3
- A terminal or command prompt
- All project files kept in the same folder structure

## How to Set Up

1. Install Python 3 on your device.
2. Save the source code as `main.py` if you are setting the project up manually.
   - Alternatively, you can clone the project using `git clone https://github.com/aaronfilarca/PyQuiz`
3. Prepare the files and project folders in one main project directory.
4. Make sure the program structure includes these components:

```text
PyQuiz/
|-- main.py
|-- config.csv
|-- scores.csv
|-- quiz_sets/
    |-- math.csv
    `-- science.csv
```

5. Set up the main files correctly:

   - `main.py` contains the main Python program that runs the quiz system.
   - `config.csv` contains the configuration settings, including the maximum attempts allowed, the number of questions per quiz, and the optional timer per quiz in minutes.
   - `scores.csv` stores the quiz results, including the user name, student ID, score, and time taken.
   - `quiz_sets/` contains all quiz question files in CSV format.
   - The `math.csv` and `science.csv` files inside `quiz_sets/` must follow the proper quiz format with the question, correct answer or answers, and answer choices.

6. Open `config.csv` and set the quiz rules you want.
7. Add or edit quiz CSV files inside `quiz_sets/`.
8. Open the project in your Integrated Terminal or Command Prompt.
9. Navigate to the directory where `main.py` is stored.
10. Run the program with `py main.py`.

### Minimum setup checklist

- `main.py` is in the root folder
- `config.csv` exists and has valid settings
- `scores.csv` exists with the score header row
- `quiz_sets/` contains at least one quiz CSV file

### Example `config.csv`

```csv
Option,Value
MaxNumberOfItems,5
MaxAttempts,2
ShowScoreAndCorrectAnswers,TRUE
TimerMinutes,0.5
```

### Example `scores.csv`

```csv
Name,Student ID,Quiz File,Score,Questions Answered,Questions Total,Date Taken,Duration
```

## Getting Started

1. Make sure Python 3 is installed.
2. Open a terminal in the project folder.
3. Run the program:

```bash
python main.py
```

## How The App Works

When the program starts, the user is asked to:

1. Enter their name.
2. Enter a numeric student ID.
3. Select a quiz set from the list.
4. Confirm the quiz start if a timer is enabled.
5. Answer each question using the displayed letter choices.

After the attempt ends, the app shows the final score and gives the option to take another quiz.

## Configuration Setup

The app reads its rules from `config.csv`.

### Required Format

```csv
Option,Value
MaxNumberOfItems,5
MaxAttempts,2
ShowScoreAndCorrectAnswers,TRUE
TimerMinutes,0.5
```

### Config Options

| Option | Description |
|---|---|
| `MaxNumberOfItems` | Maximum number of questions shown in one attempt |
| `MaxAttempts` | Maximum attempts allowed per student for each quiz file |
| `ShowScoreAndCorrectAnswers` | If `TRUE`, the program shows per-question feedback and correct answers |
| `TimerMinutes` | Quiz time limit in minutes |

### Notes

- If `TimerMinutes` is greater than `0`, the quiz is timed.
- A value of `0.5` means 30 seconds.
- The program will only show up to `MaxNumberOfItems`, even if the quiz file contains more questions.
- Attempt limits are tracked separately for each student and each quiz CSV file.

## Quiz File Setup

Quiz files belong in the `quiz_sets/` folder.

Each quiz file must be a CSV with this header:

```csv
Question,Answer,Choice1,Choice2,Choice3,Choice4,Choice5,Choice6,Choice7,Choice8
```

### Field Rules

- `Question`: the question text shown to the user
- `Answer`: the correct answer or answers
- `Choice1` to `Choice8`: possible answer choices
- Unused choice columns can be left blank

### Single-Answer Example

```csv
What is 2 + 2?,4,3,4,5,6,,,,
```

### Multiple-Answer Example

Use `&&` between correct answers in the `Answer` column:

```csv
Which of these are even numbers?,2&&4&&6,1,2,3,4,5,6,,
```

## Usage Guide

### Single-answer questions

Enter one letter:

```text
A
```

### Multiple-answer questions

Enter all correct letters separated by spaces:

```text
A C D
```

### Quiz selection

- Enter the quiz index shown in the menu to start a quiz
- Enter `-1` at the selection screen to quit

## Scoring

- Each question is worth up to `1.0` point.
- Correct answers receive full credit.
- Multiple-answer questions can receive partial credit.
- Missing correct answers or choosing extra wrong answers lowers the score.
- The final result is saved as a percentage.

## Score Saving

Results are written to `scores.csv`.

Each record stores:

- Name
- Student ID
- Quiz file
- Score
- Questions answered
- Total questions
- Date taken
- Duration

The program updates `scores.csv` after each answered question, so partial progress is still saved if the quiz ends early.

## Running The App

From the root folder of the project:

```bash
python main.py
```

If `python` does not work on your machine, try:

```bash
py main.py
```

## Example Workflow

1. Open the project folder.
2. Edit `config.csv` if you want different quiz rules.
3. Add or edit quiz files inside `quiz_sets/`.
4. Run `python main.py`.
5. Enter student details.
6. Pick a quiz and answer the questions.
7. Check `scores.csv` for saved results.

## Important Behavior

- Empty names are rejected.
- Student ID must be numeric.
- Questions and answer options are shuffled every attempt.
- Students cannot exceed the configured number of attempts for the same quiz file.
- If the timer expires, the quiz ends immediately.

## AI Disclosure

Artificial intelligence tools were used to support parts of this project.

- AI was used to help generate sample quiz sets for files such as `math.csv` and `science.csv`.
- AI was used to help generate and refine this `README.md` documentation.
- AI was used to insert comments in `main.py` and improve the grammar and clarity of existing comments.

All generated content was reviewed and adjusted to match the project requirements and current program behavior.

## Troubleshooting

### Python is not recognized

Install Python 3, then check:

```bash
python --version
```

### A quiz file does not appear in the menu

Check that the file:

- is inside `quiz_sets/`
- has a `.csv` extension
- uses the correct header row

### Scores are not saving

Make sure `scores.csv` exists and is not locked by another program such as Excel.

### Colors look wrong in the terminal

The app uses ANSI color codes. If colors do not display properly, try using Windows Terminal or another terminal that supports ANSI colors.
