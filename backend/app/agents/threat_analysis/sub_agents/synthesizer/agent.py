import json
import logging
from google.adk.agents import Agent
from .prompt import SYNTHESIZER_PROMPT
from app.services.adk_service import ADKService
from google.adk.agents.callback_context import CallbackContext
from google.genai import types
from typing import Optional
from google.adk.models import LlmResponse
from app.services.threat_utils import store_agent_threat
from app.db.session import AsyncSessionLocal

MODEL = ADKService().get_litellm_model()


def create_synthesizer_agent():
    return Agent(
        name="SynthesizerAgent",
        model=MODEL,
        instruction=SYNTHESIZER_PROMPT,
        description="Aggregates, deduplicates, and structures collected data into actionable threat intelligence.",
        output_key="synthesized_intel",
        after_model_callback=modify_output_after_agent,
    )

async def store_synthesized_intel(agent_input):
    """
    Runs the SynthesizerAgent, extracts synthesized intel, and stores it as a Threat record.
    Returns the new Threat ID if successful, else None.
    """
    # agent = create_synthesizer_agent()
    # result = await agent.run(agent_input)
    # synthesized = result.get("synthesized_intel")
    if not agent_input:
        print("No synthesized intel found in agent output.")
        return None
    async with AsyncSessionLocal() as session:
        threat_id = await store_agent_threat(session, agent_input)
    if threat_id:
        print(f"Synthesized threat stored with ID: {threat_id}")
    else:
        print("Failed to store synthesized threat.")
    return threat_id


async def modify_output_after_agent(
    callback_context: CallbackContext, llm_response: LlmResponse
) -> Optional[LlmResponse]:
    """Inspects/modifies the LLM response after it's received."""
    agent_name = callback_context.agent_name
    print(f"[Callback] After model call for agent: {agent_name}")

    # --- Inspection ---
    original_text = ""
    if llm_response.content and llm_response.content.parts:
        # Assuming simple text response for this example
        if llm_response.content.parts[0].text:
            original_text = llm_response.content.parts[0].text
            try:
                parsed_json = parse_content(original_text)
                await store_synthesized_intel(parsed_json)
            except (json.JSONDecodeError, ValueError) as e:
                logging.error(f"[Callback] Error parsing LLM JSON in modify_output_after_agent: {e}. Original text: {original_text!r}")
        elif llm_response.content.parts[0].function_call:
            return None
        else:
            return None
    elif llm_response.error_message:
        logging.error(
            f"[Callback] Inspected response: Contains error '{llm_response.error_message}'. No modification."
        )
        return None
    else:
        return None

def parse_content(content):
    if not content or not str(content).strip():
        logging.error('[parse_content] Empty or whitespace-only content received.')
        raise ValueError('parse_content: Input content is empty or whitespace.')

    # First, try to extract the JSON string from within a markdown code block
    # This handles cases where the LLM wraps the JSON in ```json\n...\n```
    if content.strip().startswith('```json') and content.strip().endswith('```'):
        # Find the first newline after ```json and the last newline before ```
        start_index = content.find('```json') + len('```json')
        end_index = content.rfind('```')
        if start_index != -1 and end_index != -1 and start_index < end_index:
            inner_json_string = content[start_index:end_index].strip()
            # Remove the first newline if it exists after ```json
            if inner_json_string.startswith('\n'):
                inner_json_string = inner_json_string[1:]
        else:
            # If markdown block is malformed, treat original content as is
            inner_json_string = content
    else:
        inner_json_string = content

    final_parsed_json = None
    
    try:
        final_parsed_json = json.loads(inner_json_string)
    except json.JSONDecodeError as e:
        logging.error(f'[parse_content] Failed to decode JSON from content: {inner_json_string!r}. Error: {e}')
        raise
    finally:
        return final_parsed_json
    

# if __name__ == "__main__":
#     import asyncio
#     asyncio.run(store_synthesized_intel("test"))