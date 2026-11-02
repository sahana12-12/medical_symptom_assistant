# Local Medical Symptom Assistant

A Python learning project for the symptom assistant assignment. It asks for basic patient context and symptoms, sends them to a locally running Ollama model, displays a cautious informational response, and saves it to `outputs/medical_analysis.txt`.

## Important safety note

This program does not diagnose, triage, or provide treatment instructions. A language model can be wrong or miss important details. Do not use it to make healthcare decisions. For serious, worsening, or urgent symptoms, contact a qualified healthcare professional or local emergency service.

## Requirements

- Windows with Ollama installed and a model downloaded (for example, `llama3.2:latest`).
- Python 3.10 or newer.
- VS Code. The Microsoft Python extension is recommended.
- Ollama running locally while the program is in use.

## Run in VS Code

1. Extract the ZIP.
2. In VS Code, choose **File > Open Folder** and open the extracted `medical_symptom_assistant` folder.
3. Open `main.py`. Set `MODEL` near the top to the exact name shown by `ollama list`. The default is `llama3.2:latest`.
4. Choose **Terminal > New Terminal** and run:

   ```powershell
   ollama list
   python main.py
   ```

5. Enter the requested patient context and symptoms. Fields can be left blank if unknown.
6. Review the displayed informational report. A copy is saved to `outputs\medical_analysis.txt`.

If `python` is not recognized, try `py main.py`. If Ollama cannot be reached, launch the Ollama app from the Windows Start menu.

## Data and privacy

This project sends the entered text only to Ollama at `http://localhost:11434` on the local computer and writes the generated report to the local `outputs` folder. Avoid entering real identifying or sensitive health information in a classroom demo. The included sample case is fictional.

## Model limitation

This project uses a local model through Ollama, not GPT-4. If the assignment requires GPT-4 specifically, ask the instructor whether a local model is acceptable for the demonstration.
