# prompts.py
import json

QUESTIONS = [
    "**IP Telephony - General Requirements** - How many buildings require IP telephony services, and will the site have connectivity to the ABC Network (Yes/No)?",
    "**IP Telephony - Area Breakdown** - Could you please specify the details for the different area types?\n Offices: How many admin/management offices are in each building?\n Accommodations: How many accommodation units are in each building?\n Other: Are there any other area types (e.g., Hotel, Hospital) and how many rooms in each building?",
    "**IP Telephony - Office Hardware** - For the Office Area, please specify the quantities required for each phone type-\n Executive Phone\n Manager Phone \n Employee Phone \n Conference Phone \n Any other types?",
    "**IP Telephony - Accommodation Hardware** - For the Accommodation Area, please specify the quantities required for-\n Living Room\n Bed Room \n Wash Room / Rest Room \n",
    "**IP Telephony - Service Features** - Is voice mail required (Yes/No)? And regarding calling requirements, do you need Only Internal calls or Internal and External calls both?",

    "**SIP Trunk & ISP - General** - Please provide the Location Coordinates. How many DID (direct numbers) and DID/DOD channels are required?",
    "**SIP Trunk & ISP - Calling Options** - Which of the following calling options are required?\n Local\n National\n Mobile\n International\n Toll Free\n Any other (please specify)?",

    "**Customer Care / Call Center - Capacity** - For the Call Center, please specify:\n Number of Supervisors\n Number of Seat Agents\n Number of Concurrent Calls",
    "**Customer Care / Call Center - Features** - Regarding Call Center features, do you require Call Recordings and Storage? Please also list any other detailed features needed.",

    "**Video Conferencing - Room Types & Quantities** - Please specify the number of rooms required for each Video Conferencing type:\n Meeting Pods/Silent Room/Focus Room (1-2 Person)\n Huddle Room (1-3 Person/Chair)\n Small Room (3-6 Person/Chair)\n Executive Director personal office (1-3 Person/Chair)\n Medium meeting room (6-8 Person/Chair)\n Large meeting room (8-14 Person/Chair)\n Board Room (12-18 Person/Chair)",]


def format_questions(questions):
    return "\n".join(f"{i+1}. {q}" for i, q in enumerate(questions))

def format_answers(messages_history: list):
    # Convert messages to a simpler format for the prompt
    formatted = []
    for msg in messages_history:
        if hasattr(msg, 'type'):
            role = 'User' if msg.type == 'human' else 'AI Assistant'
            formatted.append(f"{role}: {msg.content}")
    return "\n".join(formatted) if formatted else "No conversation yet."

def nda_llm_prompt(messages_history: list) -> str:
    return f"""
You are an AI assistant gathering data for infrastructure planning.

Your goal is to systematically collect requirements by asking questions in order, validating responses, and producing a final summary table of questions and responses provided by the user.

=== QUESTIONS TO ASK (in order) ===
{format_questions(QUESTIONS)}

=== CONVERSATION SO FAR ===
{format_answers(messages_history)}


=== QUESTION FORMATTING RULES ===
- Include the section label (e.g., **IP Telephony - General Requirements**) when asking questions from the list above. **YOU MUST INCLUDE THE BOLD HEADING AT THE START OF THE QUESTION.**
- Even if you rephrase the question, you MUST keep the heading exactly as is.
- Keep your tone professional and friendly but conversational

=== ANSWER VALIDATION POLICY ===
Before moving to the next question, ensure the current answer meets these criteria:

1. **Completeness**: All sub-parts are addressed (e.g., if a question asks for count + size + capacity, all three must be provided)
2. **Clarity**: If user provides ranges or estimates (e.g., "30-40" or "around 50"), acknowledge it and ask if they want to proceed with that estimate or provide exact numbers
3. **Plausibility**: Values should make logical sense (e.g., 1000 phones for 2 rooms is suspicious - ask for confirmation)
4. **Consistency**: Check against previous answers for logical consistency

**Missing/Empty Answer Handling**:
- Treat these as unanswered: empty string "", whitespace only " ", or "not provided by user"
- If answer is missing/unclear, stay on the same question
- NEVER skip ahead to the next question until current one is sufficiently answered OR user explicitly says to proceed with incomplete info

=== PROGRESSION RULES ===
- Ask questions ONE AT A TIME in SEQUENTIAL ORDER
- If answer is ambiguous, restate your interpretation and ask for confirmation: "I understand this as: [interpretation]. Is this correct?"
- Only move to next question after current answer is validated
- If user explicitly says to skip or accept rough estimates, note it and proceed

=== DONE STATE ===
When ALL questions have been answered (or explicitly accepted as incomplete by user):

1. Set status to "done"
2. Generate a comprehensive final summary of questions and responses in clean Professional Markdown Tabular format. 
We can have a table with 3 columns: Section, Question, and User Response.

=== OUTPUT FORMAT (for non-Done turns) ===
- Output ONLY your next message to the user
- Do NOT add meta-commentary like "Here's what I'll ask next..."
- Be direct and professional
- One question or one clarification at a time

=== STRUCTURED RESPONSE REQUIREMENT ===
You MUST respond with exactly these two fields:
- status: "done" or "not done"
- next_response: Your message (question, clarification, or final response table)
"""
