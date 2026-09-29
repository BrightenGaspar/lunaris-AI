import os
import re
import json
import uuid
from typing import Dict, Any, List, Optional
import requests
import psycopg2
from psycopg2.extras import RealDictCursor
from agent_tools import LunarisToolRegistry, TOOL_DEFINITIONS

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
DB_CONFIG = {
    "dbname": os.getenv("DB_NAME", "lunaris_ai"),
    "user": os.getenv("DB_USER", "lunaris"),
    "password": os.getenv("DB_PASSWORD", "lunaris_secure_password"),
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", 5432)),
}

REACT_SYSTEM_PROMPT = """You are Lunaris AI, an advanced sovereign reasoning intelligence with access to local tools.
Solve the user's request step-by-step using the ReAct (Reasoning + Acting) loop.

You have access to the following tools:
{tool_descriptions}

Use the following format strictly:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action (e.g., query, code, or expression)
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat up to 5 times)
Thought: I now know the final answer
Final Answer: the comprehensive final answer to the original question

Rules:
1. Always state a Thought before choosing an Action.
2. Only output ONE Action and Action Input at a time. Wait for the Observation before continuing.
3. If no tools are required (e.g., greetings, general knowledge, or direct reasoning), skip straight to:
Thought: I can answer this directly without tools.
Final Answer: [your response]
4. When writing Python code for execute_python_sandbox, always print the output to standard out.
"""

class LunarisEngine:
    def __init__(
        self,
        llm_model: str = os.getenv("LLM_MODEL", "llama3.3"),
        embed_model: str = os.getenv("EMBED_MODEL", "nomic-embed-text")
    ):
        self.llm_model = llm_model
        self.embed_model = embed_model
        self.tools = LunarisToolRegistry()

    def get_db_connection(self):
        return psycopg2.connect(**DB_CONFIG)

    def generate(self, prompt: str, system_prompt: str = "", stop_sequences: Optional[List[str]] = None) -> str:
        """Raw generation call to local Ollama instance."""
        payload = {
            "model": self.llm_model,
            "prompt": prompt,
            "system": system_prompt,
            "stream": False,
            "options": {
                "temperature": 0.2,
                "stop": stop_sequences or ["Observation:"]
            }
        }
        res = requests.post(f"{OLLAMA_URL}/api/generate", json=payload, timeout=120)
        res.raise_for_status()
        return res.json().get("response", "").strip()

    def execute_tool(self, tool_name: str, tool_input: str) -> str:
        """Dispatches action to the appropriate tool implementation."""
        tool_name = tool_name.strip().lower()
        tool_input = tool_input.strip().strip("'\"`")

        if tool_name == "search_documents":
            return self.tools.search_documents(tool_input)
        elif tool_name == "web_search":
            return self.tools.web_search(tool_input)
        elif tool_name == "execute_python_sandbox":
            # Extract clean code block if wrapped in markdown
            clean_code = tool_input
            if "```" in tool_input:
                match = re.search(r"```(?:python)?\s*(.*?)\s*```", tool_input, re.DOTALL)
                if match:
                    clean_code = match.group(1)
            return self.tools.execute_python_sandbox(clean_code)
        elif tool_name == "calculate_math":
            return self.tools.calculate_math(tool_input)
        elif tool_name == "list_knowledge_base":
            return self.tools.list_knowledge_base()
        else:
            return f"Error: Tool '{tool_name}' is not recognized. Valid tools: {[t['name'] for t in TOOL_DEFINITIONS]}"

    def load_session_history(self, session_id: str, limit: int = 6) -> str:
        """Retrieves recent conversation history from PostgreSQL."""
        try:
            conn = self.get_db_connection()
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(
                    """
                    SELECT role, content FROM lunaris_conversations 
                    WHERE session_id = %s 
                    ORDER BY created_at DESC 
                    LIMIT %s;
                    """,
                    (session_id, limit)
                )
                rows = cur.fetchall()
            conn.close()

            if not rows:
                return ""

            history = []
            for r in reversed(rows):
                history.append(f"{r['role'].capitalize()}: {r['content']}")
            return "\nConversation History:\n" + "\n".join(history) + "\n\n"
        except Exception as e:
            print(f"[Memory Warning] {e}")
            return ""

    def save_message(self, session_id: str, role: str, content: str, thought: Optional[str] = None):
        """Persists a message to conversational memory."""
        try:
            valid_uuid = uuid.UUID(str(session_id))
            conn = self.get_db_connection()
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO lunaris_conversations (session_id, role, content, thought)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (str(valid_uuid), role, content, thought)
                )
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"[Memory Save Warning] {e}")

    def run_react_agent(
        self,
        user_query: str,
        session_id: Optional[str] = None,
        max_iterations: int = 5
    ) -> Dict[str, Any]:
        """
        Full autonomous ReAct reasoning loop.
        Executes Thought -> Action -> Observation cycles until reaching a Final Answer.
        """
        actual_session_id = session_id or str(uuid.uuid4())
        
        # Format tools into system prompt
        tool_desc = "\n".join([f"- {t['name']}: {t['description']}" for t in TOOL_DEFINITIONS])
        tool_names = ", ".join([t['name'] for t in TOOL_DEFINITIONS])
        system_prompt = REACT_SYSTEM_PROMPT.format(
            tool_descriptions=tool_desc,
            tool_names=tool_names
        )

        history_context = self.load_session_history(actual_session_id)
        scratchpad = f"{history_context}Question: {user_query}\n"
        
        steps = []
        final_answer = ""

        print(f"\n🧠 [Lunaris ReAct] Processing Question: {user_query}")

        for i in range(max_iterations):
            prompt = scratchpad + "Thought:"
            llm_output = self.generate(
                prompt=prompt,
                system_prompt=system_prompt,
                stop_sequences=["Observation:"]
            )
            
            # Prepend 'Thought:' if omitted by LLM
            full_step = f"Thought: {llm_output}" if not llm_output.startswith("Thought:") else llm_output
            scratchpad += full_step + "\n"

            # Check for Final Answer
            if "Final Answer:" in full_step:
                final_answer = full_step.split("Final Answer:", 1)[1].strip()
                steps.append({
                    "step": i + 1,
                    "type": "final_answer",
                    "content": full_step
                })
                break

            # Parse Action and Action Input
            action_match = re.search(r"Action:\s*([a-zA-Z0-9_\-]+)", full_step)
            input_match = re.search(r"Action Input:\s*(.*?)(?=\nThought:|\nAction:|\Z)", full_step, re.DOTALL)

            if action_match and input_match:
                tool_name = action_match.group(1).strip()
                tool_input = input_match.group(1).strip()

                print(f"👉 Step {i + 1} | Action: {tool_name} | Input: {tool_input[:60]}...")

                observation = self.execute_tool(tool_name, tool_input)
                obs_text = f"Observation: {observation}\n"
                scratchpad += obs_text

                steps.append({
                    "step": i + 1,
                    "thought": full_step,
                    "action": tool_name,
                    "action_input": tool_input,
                    "observation": observation
                })
            else:
                # If no clear action format, treat whatever generated as answer
                final_answer = full_step.replace("Thought:", "").strip()
                break

        if not final_answer:
            final_answer = self.generate(
                prompt=scratchpad + "\nThought: Summarizing final conclusion based on above observations.\nFinal Answer:",
                system_prompt=system_prompt
            )

        # Persist conversation
        self.save_message(actual_session_id, "user", user_query)
        self.save_message(actual_session_id, "assistant", final_answer, thought=json.dumps(steps))

        return {
            "session_id": actual_session_id,
            "query": user_query,
            "response": final_answer,
            "reasoning_steps": steps,
            "total_steps": len(steps)
        }

if __name__ == "__main__":
    agent = LunarisEngine()
    print("Testing Lunaris ReAct Agent...")
    result = agent.run_react_agent("What is the square root of 256 multiplied by 14?")
    print("\n--- Final Result ---")
    print(result["response"])
