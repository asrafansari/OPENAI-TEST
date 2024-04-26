import os
from openai import OpenAI

client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))

# UNCOMMENT BELOW CODE TO MAKE VECTOR STORAGE FROM FILES
# vector_store = client.beta.vector_stores.create(name="Coffee Maching using OOP")
 
# # Ready the files for upload to OpenAI 
# directory = "python-test-processed"
# file_paths = [os.path.join(directory, filename) for filename in os.listdir(directory)]
# file_streams = [open(path, "rb") for path in file_paths]

 
# # Use the upload and poll SDK helper to upload the files, add them to the vector store,
# # and poll the status of the file batch for completion.
# file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
#   vector_store_id=vector_store.id, files=file_streams
# )
 
# # You can print the status and the file counts of the batch to see the result of this operation. 
# print(file_batch.status)
# print(file_batch.file_counts)
# print(vector_store.id)

assistant = client.beta.assistants.create(
  name="Code Error Solver",
  instructions="You are an expert programmer. Use you knowledge base to trace out the errors from stack trace and by looking at the files provided to you solve the issue.",
  model="gpt-4-turbo",
  tools=[{"type": "file_search"}],
  tool_resources={"file_search": {"vector_store_ids": ["vs_V4aqDs1gGvcdbnpfA3DneQAK"]}}, # CHANGE STORE ID to vector_store.id
  temperature=0
)


stack_trace = """ File "/home/hub/Desktop/asraf/assistant_api/python-test/main.py", line 26, in <module>
    menu = MenuItem()
TypeError: MenuItem.__init__() missing 5 required positional arguments: 'name', 'water', 'milk', 'coffee', and 'cost'"""
# Create a thread and attach the file to the message
thread = client.beta.threads.create(
  messages=[
    {
      "role": "user",
      "content": f"Please fix the code as I am getting following error stack trace:\n {stack_trace}. File path is provided in each file first line. Give me output in json. I need two keys, one should have code before changes and another should have code after changes. Before changes and after changes should also include the line no and filepath with filename. strictly follow this output json format",   
    }
  ]
)
 
# The thread now has a vector store with that file in its tool resources.
print(thread.tool_resources.file_search)

from typing_extensions import override
from openai import AssistantEventHandler
 
class EventHandler(AssistantEventHandler):
    @override
    def on_text_created(self, text) -> None:
        print(f"\nassistant > ", end="", flush=True)

    @override
    def on_tool_call_created(self, tool_call):
        print(f"\nassistant > {tool_call.type}\n", flush=True)

    @override
    def on_message_done(self, message) -> None:
        # print a citation to the file searched
        message_content = message.content[0].text
        annotations = message_content.annotations
        citations = []
        for index, annotation in enumerate(annotations):
            message_content.value = message_content.value.replace(
                annotation.text, f"[{index}]"
            )
            if file_citation := getattr(annotation, "file_citation", None):
                cited_file = client.files.retrieve(file_citation.file_id)
                citations.append(f"[{index}] {cited_file.filename}")

        print(message_content.value)
        print("\n".join(citations))


# Then, we use the stream SDK helper
# with the EventHandler class to create the Run
# and stream the response.

with client.beta.threads.runs.stream(
    thread_id=thread.id,
    assistant_id=assistant.id,
    event_handler=EventHandler(),
) as stream:
    print(stream.get_final_run())
    