Windows setup for the trainer

Target folder:
C:\Тренажер

1) Copy this entire folder content into C:\Тренажер.
2) Install Python 3 (if needed):
   https://www.python.org/downloads/
   Enable the checkbox: Add python.exe to PATH.

Web version (exam mode):
- Double-click start_web.bat
- Open in browser:
  http://localhost:8000/web_trainer.html
- Choose one of two buttons to start:
  "Основной" or "Олимпиадный".

Exam rules in web version:
- Two modes:
  Основной and Олимпиадный.
- Основной: 30 questions.
- Олимпиадный: 15 questions.
- Основной now uses the current harder task bank from:
  assets/main_variants_bank.json
  Main variants open one by one in a cycle.
  Score is calculated by the actual difficulty saved in each task.
- You can add your own full main variants manually in:
  assets/main_variants_manual.json
  The program loads this file automatically together with the base bank.
  Add new variants only into the "variants" array.
  Each manual variant must contain 30 tasks.
  Use positive integer answers only.
- Олимпиадный: 15 olympiad tasks (selected from the olympiad bank built from supplied files).
- One common timer for all questions: 90 minutes.
- You can switch between questions (Back/Next buttons and question grid).
- Main test answers are natural numbers from the JSON key set.
- Each question has one correct answer.
- Statistics is saved after each completed test:
  test number, start datetime, end datetime, correct, wrong, score.
  For Основной mode, history also stores and shows the source variant number.
  After each completed test, the app also shows a random motivating message for Arlen.
  History also shows mistakes by question number:
  your answer and the correct answer.
  You can open each mistaken question and review:
  full task text, picture (if any), your answer, correct answer.
- Task topic names are hidden in the UI.
- Some tasks in both modes can include pictures (diagram/image-based tasks).
- Score weights:
  easy = 3 points, medium = 5 points, hard = 7 points.
- History safety:
  replacing files in C:\Тренажер does not remove browser localStorage history.
  You can also use buttons "Экспорт истории" and "Импорт истории".

CLI version:
- Double-click start_cli.bat

Included files:
- web_trainer.html  (web app)
- math_trainer.py   (console trainer)
- start_web.bat     (web launcher)
- start_cli.bat     (CLI launcher)
- assets/main_variants_bank.json   (current main variants bank)
- assets/main_variants_manual.json (file for manual variant additions)
