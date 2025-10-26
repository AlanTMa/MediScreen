from letta_client import Letta
from letta_client.core.api_error import ApiError
import os
from letta_client.client import BaseTool
from pydantic import BaseModel
from typing import List, Type

class EndConversationEntry(BaseModel):
    pass

class EndConversation(BaseTool):
    name: str = "end_call"
    args_schema: Type[BaseModel] = EndConversationEntry
    description: str = "Ends the conversation with the user"
    
    def run(self) -> bool:
        print("Call has been ended") # TODO: add the end convo part
        return True

class ScheduleTrialEntry(BaseModel):
    datetime: str
    phone_number: str

class ScheduleTrialTool(BaseTool):
    name: str = "schedule_trial"
    args_schema: Type[BaseModel] = ScheduleTrialEntry
    description: str = "Schedule a trial for patients using the given datetime and phone number"
    def run(self, datetime: str, phone_number : str) -> bool:
        return datetime, phone_number

# Initialize client
client = Letta(token="sk-let-MjE0YTMxOWUtYTA4OC00NTEzLWIxYTUtNDA5ODU1M2E1NmExOjY3Zjc4ZWRjLWNmNDItNGUwNy05YTM5LTA3MmNiYTM0YjVlZg==")

# Create folder (or use existing one)
try:
    folder_id = client.folders.retrieve_by_name("Clinical Trials Documents")
    print(f"Using existing folder: {folder_id}\n")
except ApiError as e:
    if e.status_code == 404:
        folder = client.folders.create(
            name="Clinical Trials Documents",
            description="A folder containing PDF files of informaiton about clinical trials occurring for the agent to read",
        )
        folder_id = folder.id
        print(f"Created folder: {folder_id}\n")
    else:
        raise

def uploadfile(pdf_filename):
    if not os.path.exists(pdf_filename):
        print(pdf_filename + " not found")
    with open(pdf_filename, "rb") as f:
        file = client.folders.files.upload(
            folder_id=folder_id,
            file=f,
            duplicate_handling="skip",
        )
        print(f"Uploaded PDF: {file.id}\n")
        return file


# Create agent
agent = client.agents.create(
    name="clinical_trial_recruiter",
    model="anthropic/claude-3-5-sonnet-20241022",
    memory_blocks=[
        {
            "label": "persona",
            "value": "I am a clinical trial recruiter. I will inform the patient about the clinical trial listed under Clinical Trials Documents, answer their questions, and ask question about them to see if the patient is meets all the criterias to be part of the clinical trial. If the patient is not eligible, I would explicitly state they unfortunately cannot be part of the clinical trial. If the patient is eligible, I will ask for a prefered time and date and their phone number and schedule a trial for them using the schedule_trial tool. I need to keep messages brief like one to two sentences. I will ask questions one at a time and wait for the patient to respond before moving on to the next question."
        },
        {
            "label": "human",
            "value": "Name: User\nInteraction: A patient interested in being part of a clinical trial"
        }
    ],
)

print(f"Created agent: {agent.id}\n")

# Attach folder to agent
client.agents.folders.attach(
    agent_id=agent.id,
    folder_id=folder_id,
)

print(f"Attached folder to agent\n")


# Create tools
tool_from_class = client.tools.add(
    tool=ScheduleTrialTool(),
)

# Attach tool to agent
client.agents.tools.attach(
    agent_id=agent.id,
    tool_id=tool_from_class.id,
)

# Create tools
tool_from_class = client.tools.add(
    tool=EndConversation(),
)

# Attach tool to agent
client.agents.tools.attach(
    agent_id=agent.id,
    tool_id=tool_from_class.id,
)

print(f"Attached tool to agent\n")

uploadfile("Preoperative BOTOX® Injection for Large Ventral Hernia Repair (PRETOX).pdf")

while (True):
    response = client.agents.messages.create(
        agent_id=agent.id,
        messages=[{"role": "user", "content": input("User: ")}],
    )
    for msg in response.messages:
        if msg.message_type == "assistant_message":
            print(f"Assistant: {msg.content}\n")
        elif msg.message_type == "tool_message":
            if msg.tool_name == "end_call":
                break
        elif msg.message_type == "tool_message":
            if msg.tool_name == "schedule_trial":
                print(f"Schedule trial for {msg.tool_args['datetime']} at {msg.tool_args['phone_number']}")

'''
# Query the PDF
response = client.agents.messages.create(
    agent_id=agent.id,
    messages=[{"role": "user", "content": "Can you summarize the main ideas from the MemGPT paper?"}],
)

for msg in response.messages:
    if msg.message_type == "assistant_message":
        print(f"Assistant: {msg.content}\n")

# Ask specific question
response = client.agents.messages.create(
    agent_id=agent.id,
    messages=[{"role": "user", "content": "What problem does MemGPT solve?"}],
)

for msg in response.messages:
    if msg.message_type == "assistant_message":
        print(f"Assistant: {msg.content}\n")
'''
