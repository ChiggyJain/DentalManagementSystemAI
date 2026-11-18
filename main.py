
"""
Dental Appointment System — powered by LangGraph + Groq
"""

from dotenv import load_dotenv
load_dotenv()
from langchain_core.messages import AIMessage, HumanMessage
from workflows.graph import dental_graph

BANNER = """
╔══════════════════════════════════════════════════════════╗
║         Dental Appointment Management System             ║
║         Powered by LangGraph + Groq                       ║
╚══════════════════════════════════════════════════════════╝
Examples:
  • Show available slots for an orthodontist
  • Book patient 1000082 with Emily Johnson on 5/10/2026 9:00
  • Cancel appointment for patient 1000082 at 5/10/2026 9:00
  • Reschedule patient 1000082 from 5/10/2026 9:00 to 5/12/2026 10:00
  • What appointments does patient 1000048 have?

Type 'quit' to exit.
"""


def run():
    print(BANNER)

    # Keep the state returned by LangGraph so later turns have the full
    # conversation history. The graph has no checkpointer, so history must be
    # supplied again on each call to invoke().
    conversation = {"messages": []}

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not user_input:
            continue
        if user_input.lower() in {"quit", "exit"}:
            print("Goodbye!")
            break

        previous_message_count = len(conversation["messages"])
        try:
            result = dental_graph.invoke(
                {
                    "messages": conversation["messages"]
                    + [HumanMessage(content=user_input)]
                }
            )
        except Exception as exc:
            print(f"Assistant: Sorry, the request failed: {exc}")
            continue

        conversation = result
        # A completed graph run ends with the agent's final AI message.
        answer = next(
            (
                message.content
                for message in reversed(
                    result.get("messages", [])[previous_message_count:]
                )
                if isinstance(message, AIMessage)
                and not message.tool_calls
                and message.content
            ),
            None,
        )
        if answer:
            print(f"Assistant: {answer}")


if __name__ == "__main__":
    run()
