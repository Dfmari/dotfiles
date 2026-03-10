#!/usr/bin/env python3
import os
import sys
import argparse
import mimetypes
import re
import base64
from openai import OpenAI  # Groq uses the OpenAI SDK format
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

# --- CONFIGURATION ---
# Groq model for fast text analysis
TEXT_MODEL = "llama3-70b-8192"
# Groq model for vision
VISION_MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"

# --- AGENT ROSTERS (Unchanged) ---
AGENTS = {
    "webber": """
    ROLE: Elite Web Security & Anomaly Analyst.
    OBJECTIVE: Audit source code for Technical Vulnerabilities AND Logic Anomalies.
    DIRECTIVE: Distinguish between 'Vulnerability' and 'Anomaly'. Do not hallucinate flags.
    PRIORITIES:
    1. ATTACK VECTORS: $_GET/POST, exec(), system(), SQL concatenation, XSS sinks.
    2. PATTERN ANOMALIES: Hidden elements (display:none), breaks in naming conventions, odd comments.
    3. LEAKS: Hardcoded keys/tokens.
    OUTPUT FORMAT: Markdown.
    """,
    "crypter": """ROLE: CTF Cryptanalyst. OBJECTIVE: Break encryption, provide Python solver. OUTPUT FORMAT: Markdown.""",
    "sherlock": """ROLE: Digital Forensics Investigator. OBJECTIVE: Analyze files/metadata. OUTPUT FORMAT: Markdown.""",
    "coder": """ROLE: Competitive Programmer. OBJECTIVE: Write high-performance Python scripts. OUTPUT FORMAT: Python code block.""",
    "geo": """ROLE: IMINT Specialist. OBJECTIVE: Analyze image for geolocation clues. OUTPUT FORMAT: Markdown.""",
}

console = Console()


def extract_code_block(text):
    pattern = r"```(?:python)?\n(.*?)```"
    match = re.search(pattern, text, re.DOTALL)
    return match.group(1) if match else None


# Function to encode image for Groq Vision
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def analyze(agent_name, filepath, save_path=None):
    # 1. Authenticate with Groq
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        console.print("[bold red]MISSING GROQ_API_KEY[/bold red].")
        sys.exit(1)

    # Initialize the client pointing to Groq's base URL
    client = OpenAI(api_key=api_key, base_url="https://api.groq.com/openai/v1")

    if not os.path.exists(filepath):
        console.print(f"[bold red]File not found: {filepath}[/bold red]")
        sys.exit(1)

    mime_type, _ = mimetypes.guess_type(filepath)
    filename = os.path.basename(filepath)

    console.print(
        f"[bold green]Deploying {agent_name.upper()} on {filename}...[/bold green]"
    )

    try:
        messages = [{"role": "system", "content": AGENTS[agent_name]}]

        # 2. Vision Logic (Base64)
        if mime_type and mime_type.startswith("image"):
            console.print("[yellow]Image Detected. Loading Vision Module...[/yellow]")
            base64_image = encode_image(filepath)
            target_model = VISION_MODEL
            messages.append({
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Analyze this image based on your system directives.",
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:{mime_type};base64,{base64_image}"},
                    },
                ],
            })

        # 3. Text Logic
        else:
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                text_data = f.read()
            target_model = TEXT_MODEL
            messages.append({
                "role": "user",
                "content": f"FILENAME: {filename}\nCONTENT:\n\n{text_data}",
            })

        # 4. Execute via Groq
        with console.status(
            f"[bold green]Analyzing via Groq ({target_model})...[/bold green]",
            spinner="dots",
        ):
            response = client.chat.completions.create(
                model=target_model, messages=messages, temperature=0.2
            )
            output_text = response.choices[0].message.content

        # 5. Render Output
        console.print(
            Panel(
                Markdown(output_text),
                title=f"{agent_name.upper()} REPORT",
                border_style="cyan",
            )
        )

        # 6. Save Logic (Unchanged)
        if save_path:
            code = extract_code_block(output_text)
            if code:
                with open(save_path, "w") as f:
                    f.write(code)
                console.print(
                    f"\n[bold green][+] Code saved to: {save_path}[/bold green]"
                )
                os.chmod(save_path, 0o755)
            else:
                console.print(
                    f"\n[bold red][!] No code block found to save.[/bold red]"
                )

    except Exception as e:
        console.print(f"[bold red]MISSION FAILURE:[/bold red] {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("agent", choices=AGENTS.keys(), help="Specialist")
    parser.add_argument("file", help="Target file")
    parser.add_argument("--save", "-s", help="Extract code block to file")
    args = parser.parse_args()

    analyze(args.agent, args.file, args.save)
