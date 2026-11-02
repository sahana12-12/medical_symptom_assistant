import json
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path

# Change this to the exact model name shown by `ollama list`.
MODEL = "llama3.2:latest"
OLLAMA_URL = "http://localhost:11434/api/generate"
OUTPUT_FILE = Path(__file__).parent / "outputs" / "medical_analysis.txt"
DISCLAIMER = (
    "This AI-generated response is intended for educational and informational purposes only. "
    "It is not a medical diagnosis and does not replace advice from a qualified healthcare "
    "professional. For serious, worsening or urgent symptoms, seek appropriate medical care."
)


def ask(label: str) -> str:
    return input(f"{label}: ").strip()


def collect_information() -> dict[str, str]:
    print("LOCAL MEDICAL SYMPTOM ASSISTANT")
    print("Enter what you know; press Enter to leave an item blank.\n")
    return {
        "Age": ask("Age"),
        "Sex (if relevant)": ask("Sex (if relevant)"),
        "Symptoms": ask("Describe the symptoms in your own words"),
        "Duration": ask("How long have symptoms been present"),
        "Severity": ask("How severe are they (mild, moderate, severe, or unsure)"),
        "Relevant medical history": ask("Relevant medical history (if any)"),
        "Current medications": ask("Current medications (if relevant)"),
        "Allergies": ask("Allergies (if relevant)"),
    }


def make_prompt(info: dict[str, str]) -> str:
    supplied = "\n".join(f"{key}: {value or 'Not provided'}" for key, value in info.items())
    return f"""You are generating a cautious, general health information summary for an educational demonstration. This is not clinical care.

Use only the supplied information. Do not invent details or claim certainty. Do not diagnose, assign probabilities, rank conditions, or say the user is safe. If mentioning possible explanations, give only broad possibilities and say that many causes may fit the same symptoms. Do not recommend medication, dosage, starting/stopping treatment, or home remedies. Do not replace a clinician's judgment.

Use these headings exactly:
1. Reported Symptoms
2. Patient Information
3. Possible Conditions (general possibilities only; state that this is not a diagnosis)
4. Explanation
5. Missing Information
6. Follow-up Questions
7. Medical Attention Guidance
8. Disclaimer

In Missing Information, note relevant blank fields and symptom details that remain unclear. In Follow-up Questions, ask concise questions that could help a qualified healthcare professional understand the situation. In Medical Attention Guidance, do not make a triage decision. Say that serious, worsening, or urgent symptoms need appropriate professional medical care; if there may be immediate danger, contact local emergency services. Do not claim to detect emergencies automatically.

PATIENT INFORMATION AND SYMPTOMS:
{supplied}

Include this disclaimer verbatim under the Disclaimer heading:
{DISCLAIMER}
"""


def generate_analysis(info: dict[str, str]) -> str:
    payload = json.dumps({
        "model": MODEL,
        "prompt": make_prompt(info),
        "stream": False,
    }).encode("utf-8")
    request = urllib.request.Request(
        OLLAMA_URL,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=600) as response:
        result = json.loads(response.read().decode("utf-8"))
    return result["response"].strip()


def main() -> None:
    info = collect_information()
    if not info["Symptoms"]:
        print("Please provide a symptom description to continue.")
        return

    print("\nGenerating an informational response with the local model...\n")
    try:
        analysis = generate_analysis(info)
    except urllib.error.URLError as error:
        print("Could not connect to Ollama. Make sure the Ollama app is running.")
        print(f"Details: {error}")
        return
    except (KeyError, json.JSONDecodeError) as error:
        print(f"Ollama returned an unexpected response: {error}")
        return

    report = (
        "AI-POWERED MEDICAL SYMPTOM ASSISTANT\n"
        f"Generated: {datetime.now().astimezone().strftime('%Y-%m-%d %H:%M %Z')}\n\n"
        f"{analysis}\n\nDISCLAIMER\n{'-' * 40}\n{DISCLAIMER}\n"
    )
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(report, encoding="utf-8")
    print(report)
    print(f"Report saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
