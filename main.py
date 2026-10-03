import os
import json
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
import pypdf

load_dotenv()
ROOT = Path(__file__).parent
DATA = ROOT / "data"
MODEL = "openai/gpt-oss-120b"

def extract_text(file_path):
    path = Path(file_path)
    if path.suffix.lower() == ".pdf":
        text = ""
        with open(path, "rb") as f:
            reader = pypdf.PdfReader(f)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text
    return path.read_text(encoding="utf-8", errors="ignore")

files = sorted(f for f in DATA.iterdir() if f.suffix.lower() in (".pdf", ".txt"))
cache = {}

def list_documents():
    if not files:
        return "No documents found."
    return "\n".join(f"{i + 1}. {f.stem}" for i, f in enumerate(files))

def read_document(number):
    try:
        n = int(number)
    except (TypeError, ValueError):
        return "Invalid document number."
    if n < 1 or n > len(files):
        return "Invalid document number."
    f = files[n - 1]
    if f not in cache:
        cache[f] = extract_text(f)
    return f"DOCUMENT {n}: {f.stem}\n\n{cache[f]}"

TOOLS = [
    {"type": "function", "function": {
        "name": "list_documents",
        "description": "List the available documents with their numbers.",
        "parameters": {"type": "object", "properties": {}}}},
    {"type": "function", "function": {
        "name": "read_document",
        "description": "Read the full text of one document by its number from list_documents.",
        "parameters": {"type": "object",
                       "properties": {"number": {"type": "integer"}},
                       "required": ["number"]}}},
]

def run_tool(name, args):
    if name == "list_documents":
        return list_documents()
    if name == "read_document":
        return read_document(args.get("number"))
    return "Unknown tool."

def main():
    groq_api_key = os.environ.get("GROQ_API_KEY")
    if not groq_api_key:
        groq_api_key = input("Enter your GROQ_API_KEY: ").strip()
        if not groq_api_key:
            print("GROQ_API_KEY is required.")
            return

    client = OpenAI(api_key=groq_api_key, base_url="https://api.groq.com/openai/v1")

    agents_md = (ROOT / "agent" / "AGENTS.md").read_text(encoding="utf-8", errors="ignore")
    skill_md = (ROOT / "agent" / "skills" / "extract" / "SKILL.md").read_text(encoding="utf-8", errors="ignore")
    system_instruction = (
        "You help the user understand RBI circulars.\n\n"
        f"--- AGENTS.md ---\n{agents_md}\n\n"
        f"--- SKILL.md ---\n{skill_md}\n"
    )
    messages = [{"role": "system", "content": system_instruction}]

    print(f"({len(files)} documents available. Type 'exit' to quit.)")
    while True:
        try:
            user_msg = input("\nYou: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nEnding chat session.")
            break
        if user_msg.lower() in ("quit", "exit"):
            print("Ending chat session.")
            break
        if not user_msg:
            continue

        messages.append({"role": "user", "content": user_msg})
        try:
            while True:
                completion = client.chat.completions.create(
                    model=MODEL, messages=messages, tools=TOOLS, temperature=0.2,
                )
                msg = completion.choices[0].message
                if not msg.tool_calls:
                    reply = msg.content or ""
                    messages.append({"role": "assistant", "content": reply})
                    print(f"\nAgent: {reply}")
                    break
                messages.append({
                    "role": "assistant",
                    "content": msg.content or "",
                    "tool_calls": [{"id": tc.id, "type": "function",
                                    "function": {"name": tc.function.name,
                                                 "arguments": tc.function.arguments}}
                                   for tc in msg.tool_calls],
                })
                for tc in msg.tool_calls:
                    args = json.loads(tc.function.arguments or "{}")
                    messages.append({"role": "tool", "tool_call_id": tc.id,
                                     "content": run_tool(tc.function.name, args)})
        except Exception as e:
            print(f"\nError: {e}")

if __name__ == "__main__":
    main()