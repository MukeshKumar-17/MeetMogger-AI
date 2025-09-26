import re
from collections import defaultdict
from typing import List

def generate_mock_transcript(seed_brief: str) -> str:
    """Generate a simple mock transcript (10–14 lines) from a seed brief.
    Keeps logic lightweight for hackathon use without external LLM calls.
    """
    if not isinstance(seed_brief, str) or not seed_brief.strip():
        return (
            "Distributor: We're evaluating your solution but have unclear pricing and limited enablement.\n"
            "Vendor: Thanks for sharing—let's clarify pricing and propose training options.\n"
            "Distributor: Our team needs a technical workshop and sales playbook.\n"
            "Vendor: We can schedule a workshop next week and send the playbook today.\n"
            "Distributor: Support SLAs worried a customer last quarter.\n"
            "Vendor: We'll review SLAs and share the premium support tier.\n"
            "Distributor: If we get enablement and a discount, we can push Q4 deals.\n"
            "Vendor: We'll draft action items and owners after this call.\n"
        )

    brief = seed_brief.strip()
    # Extract cues
    wants_workshop = bool(re.search(r"workshop|enablement|training", brief, re.I))
    pricing_concern = bool(re.search(r"price|pricing|discount", brief, re.I))
    sla_concern = bool(re.search(r"sla|support|response", brief, re.I))
    timeline = "this month" if re.search(r"q\d|quarter|month", brief, re.I) else "next few weeks"

    lines: List[str] = []
    lines.append("Distributor: We reviewed your solution and have a few concerns and opportunities.")
    if pricing_concern:
        lines.append("Distributor: Pricing isn't clear and we may need a partner discount for a pilot.")
    if wants_workshop:
        lines.append("Distributor: Our team needs enablement—ideally a hands-on technical workshop.")
    if sla_concern:
        lines.append("Distributor: A previous customer escalated due to slow support response times.")
    lines.append("Vendor: Thanks for the context; let's map problems to concrete next steps.")
    if pricing_concern:
        lines.append("Vendor: We'll clarify SKUs and propose a tiered discount for the pilot phase.")
    if wants_workshop:
        lines.append("Vendor: We can deliver a 2-hour workshop and share a sales playbook.")
    if sla_concern:
        lines.append("Vendor: We'll review SLAs and add a premium support option with faster response.")
    lines.append(f"Distributor: Can we align on owners and dates within {timeline}?")
    lines.append("Vendor: Yes—I'll summarize action items, owners, and deadlines right after the call.")
    lines.append("Distributor: If we close these gaps, we can co-sell in two target accounts.")
    lines.append("Vendor: Great—let's keep momentum and schedule a follow-up to confirm progress.")

    # Cap to ~12 lines
    return "\n".join(lines[:12])

def extract_insights(text):
    """Extract problems, solutions, and action items from text"""
    # Convert to lowercase for case-insensitive matching
    lower_text = text.lower()
    
    # Extract problems (sentences with problem indicators)
    problem_pattern = r'(?:problem|issue|challenge|concern|difficult|trouble)[\s\w\',-]*[.!?]'
    problems = re.findall(problem_pattern, text, re.IGNORECASE)
    
    # Extract solutions (sentences with solution indicators)
    solution_pattern = r'(?:solution|resolve|fix|address|recommend|suggest)[\s\w\',-]*[.!?]'
    solutions = re.findall(solution_pattern, text, re.IGNORECASE)
    
    # Extract action items (sentences with action indicators)
    action_pattern = r'(?:action item|next step|todo|task|follow up)[\s\w\',-]*[.!?]'
    action_items = re.findall(action_pattern, text, re.IGNORECASE)
    
    # Clean and deduplicate
    def clean_list(items):
        return list(dict.fromkeys([item.strip() for item in items if len(item.split()) > 3]))
    
    return {
        "problems": clean_list(problems)[:5],  # Top 5 problems
        "solutions": clean_list(solutions)[:5],  # Top 5 solutions
        "action_items": clean_list(action_items)  # All action items
    }