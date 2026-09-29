import os
import re
import json
import uuid
from typing import Dict, Any, List, Optional
import requests
from agent_tools import LunarisToolRegistry, TOOL_DEFINITIONS

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

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
3. If no tools are required, skip straight to:
Thought: I can answer this directly without tools.
Final Answer: [your response]
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
        try:
            import psycopg2
            return psycopg2.connect(**DB_CONFIG)
        except Exception:
            return None

    def _call_gemini(self, prompt: str, system_prompt: str) -> Optional[str]:
        """Hybrid fallback to Google Gemini API if GEMINI_API_KEY is present."""
        if not GEMINI_API_KEY:
            return None
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
            payload = {
                "contents": [{"parts": [{"text": f"{system_prompt}\n\n{prompt}"}]}],
                "generationConfig": {"temperature": 0.2, "maxOutputTokens": 1024}
            }
            res = requests.post(url, json=payload, timeout=20)
            if res.status_code == 200:
                data = res.json()
                return data["candidates"][0]["content"]["parts"][0]["text"].strip()
        except Exception as e:
            print(f"[Gemini API Error] {e}")
        return None

    def _call_openai_compatible(self, prompt: str, system_prompt: str, api_key: str, base_url: str, model: str) -> Optional[str]:
        """Hybrid fallback to OpenAI / Groq / DeepSeek / OpenRouter API."""
        try:
            headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
            payload = {
                "model": model,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.2,
            }
            res = requests.post(f"{base_url}/chat/completions", headers=headers, json=payload, timeout=20)
            if res.status_code == 200:
                return res.json()["choices"][0]["message"]["content"].strip()
        except Exception as e:
            print(f"[Cloud API Error] {e}")
        return None

    def _rule_based_reasoning(self, query: str) -> str:
        """Intelligent sovereign agent fallback when no external LLM or Ollama is online."""
        q = query.strip()
        lower_q = q.lower()

        # Math / calculation detection
        math_pattern = r"(?:what is|calculate|compute|solve)?\s*([\d\.\s\+\-\*\/\(\)\^\%\s\b(sqrt|pi|pow|sin|cos|abs)\b]+)"
        match = re.search(math_pattern, lower_q)
        if match and any(op in match.group(1) for op in ["+", "-", "*", "/", "sqrt", "pow", "^", "%"]):
            expr = match.group(1).replace("^", "**").strip()
            calc_res = self.tools.calculate_math(expr)
            return (
                f"Thought: The user is asking for a mathematical calculation. I will evaluate '{expr}'.\n"
                f"Action: calculate_math\n"
                f"Action Input: {expr}\n"
                f"Observation: {calc_res}\n"
                f"Thought: I now have the calculated answer.\n"
                f"Final Answer: {calc_res}"
            )

        # Code execution request
        if "python" in lower_q or "run code" in lower_q or "execute" in lower_q:
            code_match = re.search(r"```(?:python)?\s*(.*?)\s*```", q, re.DOTALL)
            code = code_match.group(1) if code_match else "print('Lunaris Sandbox is active and operational.')"
            res = self.tools.execute_python_sandbox(code)
            return (
                f"Thought: I need to execute Python code in the sandbox.\n"
                f"Action: execute_python_sandbox\n"
                f"Action Input: {code}\n"
                f"Observation: {res}\n"
                f"Thought: Code execution completed.\n"
                f"Final Answer: {res}"
            )

        # Knowledge base query
        if "document" in lower_q or "data" in lower_q or "file" in lower_q or "metric" in lower_q or "architecture" in lower_q:
            doc_res = self.tools.search_documents(q)
            return (
                f"Thought: Searching local indexed documents in pgvector for '{q}'.\n"
                f"Action: search_documents\n"
                f"Action Input: {q}\n"
                f"Observation: {doc_res}\n"
                f"Thought: Synthesizing retrieved document information.\n"
                f"Final Answer: {doc_res}"
            )

        # General sovereign greeting & query response
        return (
            f"Thought: I can answer this directly.\n"
            f"Final Answer: 🌕 **Lunaris AI Sovereign Intelligence**\n\n"
            f"I have received your query: *\"{query}\"*\n\n"
            f"### Active Sovereign Capabilities:\n"
            f"- 🧠 **ReAct Multi-Step Tool Reasoning**: Active\n"
            f"- 🔒 **Air-Gapped Code Sandbox**: Active & Ready (`python sandbox.py`)\n"
            f"- 📂 **Multi-Format Vector RAG**: PostgreSQL + pgvector (`documents/` watcher active)\n"
            f"- 🎙️ **Voice Engine**: Offline Whisper STT & TTS ready\n\n"
            f"*(Tip: To connect a full neural model, install [Ollama](https://ollama.com) or add `GEMINI_API_KEY` / `OPENAI_API_KEY` / `GROQ_API_KEY` to your `.env` file)*."
        )

    def generate(self, prompt: str, system_prompt: str = "", stop_sequences: Optional[List[str]] = None) -> str:
        """Generation router: Ollama -> Gemini API -> Groq/OpenAI -> Sovereign Rule Engine."""
        # 1. Try local Ollama instance
        payload = {
            "model": self.llm_model,
            "prompt": prompt,
            "system": system_prompt,
            "stream": False,
            "options": {"temperature": 0.2, "stop": stop_sequences or ["Observation:"]}
        }
        try:
            res = requests.post(f"{OLLAMA_URL}/api/generate", json=payload, timeout=(0.8, 30))
            if res.status_code == 200:
                return res.json().get("response", "").strip()
        except Exception:
            pass

        # 2. Try Gemini API fallback if key is configured
        gemini_res = self._call_gemini(prompt, system_prompt)
        if gemini_res:
            return gemini_res

        # 3. Try Groq API fallback (Ultra-fast & Free)
        if GROQ_API_KEY:
            groq_res = self._call_openai_compatible(
                prompt, system_prompt, GROQ_API_KEY, "https://api.groq.com/openai/v1", "llama-3.3-70b-versatile"
            )
            if groq_res:
                return groq_res

        # 4. Try OpenAI API fallback
        if OPENAI_API_KEY:
            openai_res = self._call_openai_compatible(
                prompt, system_prompt, OPENAI_API_KEY, "https://api.openai.com/v1", "gpt-4o-mini"
            )
            if openai_res:
                return openai_res

        # 5. Extract question and execute intelligent rule reasoning
        q_match = re.search(r"Question:\s*(.*?)(?=\nThought:|\Z)", prompt, re.DOTALL)
        query = q_match.group(1).strip() if q_match else prompt
        return self._rule_based_reasoning(query)

    def execute_tool(self, tool_name: str, tool_input: str) -> str:
        """Dispatches action to the appropriate tool implementation."""
        tool_name = tool_name.strip().lower()
        tool_input = tool_input.strip().strip("'\"`")

        if tool_name == "search_documents":
            return self.tools.search_documents(tool_input)
        elif tool_name == "web_search":
            return self.tools.web_search(tool_input)
        elif tool_name == "execute_python_sandbox":
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
            return f"Error: Tool '{tool_name}' is not recognized."

    def load_session_history(self, session_id: str, limit: int = 6) -> str:
        conn = self.get_db_connection()
        if not conn:
            return ""
        try:
            from psycopg2.extras import RealDictCursor
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
        except Exception:
            return ""

    def save_message(self, session_id: str, role: str, content: str, thought: Optional[str] = None):
        conn = self.get_db_connection()
        if not conn:
            return
        try:
            valid_uuid = uuid.UUID(str(session_id))
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
        except Exception:
            pass

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

        print(f"\n[Lunaris ReAct] Processing Question: {user_query}")

        for i in range(max_iterations):
            prompt = scratchpad + "Thought:"
            llm_output = self.generate(
                prompt=prompt,
                system_prompt=system_prompt,
                stop_sequences=["Observation:"]
            )
            
            full_step = f"Thought: {llm_output}" if not llm_output.startswith("Thought:") else llm_output
            scratchpad += full_step + "\n"

            if "Final Answer:" in full_step:
                final_answer = full_step.split("Final Answer:", 1)[1].strip()
                steps.append({
                    "step": i + 1,
                    "type": "final_answer",
                    "content": full_step
                })
                break

            action_match = re.search(r"Action:\s*([a-zA-Z0-9_\-]+)", full_step)
            input_match = re.search(r"Action Input:\s*(.*?)(?=\nThought:|\nAction:|\Z)", full_step, re.DOTALL)

            if action_match and input_match:
                tool_name = action_match.group(1).strip()
                tool_input = input_match.group(1).strip()

                print(f"[Step {i + 1}] Action: {tool_name} | Input: {tool_input[:60]}...")

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
                final_answer = full_step.replace("Thought:", "").strip()
                break

        if not final_answer:
            final_answer = self.generate(
                prompt=scratchpad + "\nThought: Summarizing final conclusion based on above observations.\nFinal Answer:",
                system_prompt=system_prompt
            )

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
    result = agent.run_react_agent("Calculate 25 * 45")
    print("\n--- Final Result ---")
    print(result["response"])
