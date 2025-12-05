#create_boq.py
import os
from dotenv import load_dotenv
from langchain.messages import SystemMessage, HumanMessage
from langchain.chat_models import init_chat_model

# Load environment variables
load_dotenv()


system_prompt = """
You are smart BOQ(bill of quantities) generator for a project.
"""

user_prompt = """
Based on the following information received from the user, create a BOQ(bill of quantities) for the project in the format provided.

Information received from the user:{info_summary}

Output only the BOQ(bill of quantities) in the format provided, no running commentary.

Example Format(follow this format):
## BOQ
| Services | Requirements | Budgetary pricing per unit |
| :--- | :--- | :--- |
| **IP Telephony** | **General Requirements:**<br>- Number of buildings requiring telephony service: [Value]<br>- Site connectivity to ABC Network: [Yes/No]<br><br>**Area Type:**<br>- Offices - Number of admin/management offices per building: [Value]<br>- Accommodations - Number of accommodation units: [Value]<br>- Other area types (Hotel, Hospital etc) and rooms: [Details]<br><br>**IP Phones - Office Area:**<br>- Executive Phone: Cisco 8845 - Qty: [Value]<br>- Manager Phone: Cisco 9871 - Qty: [Value]<br>- Employee Phone: Cisco 9851 - Qty: [Value]<br>- Conference Room: Cisco 8832 - Qty: [Value]<br>- Any other: [Specify] - Qty: [Value]<br><br>**IP Phones - IP Accommodation Area:**<br>- Living Room: Cisco 9851 - Qty: [Value]<br>- Bed Room: Cisco 7821 - Qty: [Value]<br>- Wash Room / Rest Room: Cisco 7811 - Qty: [Value]<br><br>**Voice mail required:** [Yes/No]<br><br>**Calling Requirements:**<br>- Only Internal: No SIP trunk required<br>- Internal and External: SIP Trunk required | **Office Area:**<br>1250<br>1600<br>950<br>3500<br><br>**Accommodation Area:**<br>950<br>600<br>450 |
| **SIP Trunk_ISP** | **Location Coordinates:** [Value]<br>**Number of DIDs required:** [Value]<br>**Number of DID/DOD channels required:** [Value]<br><br>**Required calling options:**<br>- Local<br>- National<br>- Mobile<br>- International<br>- Toll Free<br>- Any other: [Specify] | Pricing depends on the number of DIDs, Channels, Calling features and ISP framework agreement |
| **Customer Care / Call Center** | **Number of supervisors:** [Value]<br>**Number of Seat Agents:** [Value]<br>**Call Recordings:** [Value]<br>**Storage:** [Value]<br>**Concurrent Calls:** [Value]<br>**Detailed Feature:** [Value] | Pricing depends on the requirements |
| **Video Conferencing** | **Meeting Pods/Silent Room/Focus Room:**<br>- 1-2 Person: Desk Mini/Desk/DeskPro<br><br>**Huddle Room:**<br>- 1-3 Person/Chair: Room Bar with 55 inch TV screen and Accessories<br><br>**Small Room:**<br>- 3-6 Person/Chair: Room Bar Pro with 65 inch TV screen and Accessories<br>- Webex Board 55 Pro (interactive)<br><br>**Executive Director personal office:**<br>- 1-3 Person/Chair: Room Bar Pro with 65 inch TV screen and Accessories<br>- Webex Board 75 Pro (interactive)<br><br>**Medium meeting room:**<br>- 6-8 Person/Chair: Webex Board 75 Pro (interactive)<br>- Room Kit EQ with 70 inch TV screen and accessories<br><br>**Large meeting room:**<br>- 8-14 Person/Chair: Room Kit Pro with 75 inch TV screen and accessories<br><br>**Board Room:**<br>- 12-18 Person/Chair: Room Kit Pro with 2x 75 inch or 1x 85 inch TV screen and accessories | **Huddle Room:** 18000<br><br>**Small Room:**<br>38000<br>55000<br><br>**Executive Director:**<br>38000<br>95000<br><br>**Medium Room:**<br>95000<br>60000<br><br>**Large Room:** 75000<br><br>**Board Room:** 80000 |
"""

def create_boq(info_summary:str):
    """
    Generate BOQ from the summary.
    Initializes LLM on demand to avoid side effects during import.
    """
    # Initialize the LLM here to avoid global scope issues
    llm = init_chat_model("gpt-4o", model_provider="azure_openai", api_version="2025-01-01-preview")
    
    final_user_prompt = user_prompt.replace("{info_summary}", info_summary)
    
    # Use proper message types 
    messages= [SystemMessage(content=system_prompt), 
                HumanMessage(content=final_user_prompt)]
                
    response = llm.invoke(messages)
    #print(f"BOQ:{response.content}")
    return response.content

if __name__ == "__main__":
    info_summary = """
        | Section | Question | Answer | |----------------------------------------------|-----------------------------------------------|------------------------------------------------------| | IP Telephony - General Requirements | How many buildings require IP telephony services, and will the site have connectivity to the ABC Network (Yes/No)? | 3 buildings requiring services, Yes | | IP Telephony - Area Breakdown | Could you please specify the details for the different area types? Offices: How many admin/management offices are in each building? Accommodations: How many accommodation units are in each building? Other: Are there any other area types (e.g., Hotel, Hospital) and how many rooms in each building? | Offices: Building A has 10, Building B has 5, Building C has 5. Accommodations: Building A has 0, Buildings B and C have 50 each. Other: No other area types. | | IP Telephony - Office Hardware | For the Office Area, please specify the quantities required for each phone type- Executive Phone, Manager Phone, Employee Phone, Conference Phone, Any other types? | Executive Phone: 5, Manager Phone: 15, Employee Phone: 100, Conference Phone: 3, Other: None | | IP Telephony - Accommodation Hardware | For the Accommodation Area, please specify the quantities required for Living Room, Bed Room, Wash Room / Rest Room | Living Room: 100, Bed Room: 200, Wash Room: 0 | | IP Telephony - Service Features | Is voice mail required (Yes/No)? And regarding calling requirements, do you need Only Internal calls or Internal and External calls both? | Yes, voice mail required, both Internal and External calling capabilities. | | SIP Trunk & ISP - General | Please provide the Location Coordinates. How many DID (direct numbers) and DID/DOD channels are required? | Coordinates: 25.276987, 55.296249; 50 DIDs, 30 Channels. | | SIP Trunk & ISP - Calling Options | Which of the following calling options are required? Local, National, Mobile, International, Toll Free, Any other (please specify)? | Local, Mobile, International | | Customer Care / Call Center - Capacity | For the Call Center, please specify: Number of Supervisors, Number of Seat Agents, Number of Concurrent Calls | Supervisors: 2, Seat Agents: 10, Concurrent Calls: 15 | | Customer Care / Call Center - Features | Regarding Call Center features, do you require Call Recordings and Storage? Please also list any other detailed features needed. | Yes, call recording required with storage for 6 months; need IVR and basic reporting features. | | Video Conferencing - Room Types & Quantities | Please specify the number of rooms required for each Video Conferencing type: Meeting Pods/Silent Room/Focus Room (1-2 Person), Huddle Room (1-3 Person/Chair), Small Room (3-6 Person/Chair), Executive Director personal office (1-3 Person/Chair), Medium meeting room (6-8 Person/Chair), Large meeting room (8-14 Person/Chair), Board Room (12-18 Person/Chair) | Meeting Pods: 2, Huddle Rooms: 4, Small Rooms: 2, Executive Director Office: 1, Medium Meeting Rooms: 1, Large Meeting Rooms: 1, Board Room: 1 |
    """
    print(create_boq(info_summary=info_summary))


