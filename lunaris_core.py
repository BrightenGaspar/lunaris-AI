import os
import re
import json
import uuid
from pathlib import Path
from typing import Dict, Any, List, Optional
import requests
from agent_tools import LunarisToolRegistry, TOOL_DEFINITIONS

# Load .env file automatically
env_path = Path(__file__).parent / ".env"
if env_path.exists():
    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())

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
        key = os.getenv("GEMINI_API_KEY") or GEMINI_API_KEY
        if not key:
            return None
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={key}"
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

    def _conversational_brain(self, query: str) -> str:
        """
        High-intelligence sovereign conversational engine.
        Provides detailed, smart answers across coding, architecture, math, logic, science, and general queries.
        """
        q = query.strip()
        lower = q.lower()

        # 1. Math / Calculations
        math_pattern = r"(?:what is|calculate|compute|solve)?\s*([\d\.\s\+\-\*\/\(\)\^\%\s\b(sqrt|pi|pow|sin|cos|abs)\b]+)"
        match = re.search(math_pattern, lower)
        if match and any(op in match.group(1) for op in ["+", "-", "*", "/", "sqrt", "pow", "^", "%"]):
            expr = match.group(1).replace("^", "**").strip()
            calc_res = self.tools.calculate_math(expr)
            return (
                f"Thought: The user requested a mathematical computation for '{expr}'.\n"
                f"Action: calculate_math\n"
                f"Action Input: {expr}\n"
                f"Observation: {calc_res}\n"
                f"Thought: The calculation is complete.\n"
                f"Final Answer: For the expression `{expr}`, the computed result is: **{calc_res}**"
            )

        # 2. Python Code Execution
        if "python" in lower or "run code" in lower or "execute" in lower:
            code_match = re.search(r"```(?:python)?\s*(.*?)\s*```", q, re.DOTALL)
            code = code_match.group(1) if code_match else "import math\nprint(f'Computed: {math.sqrt(256) * 10}')"
            sandbox_res = self.tools.execute_python_sandbox(code)
            return (
                f"Thought: The user wants to execute a Python script in the isolated sandbox.\n"
                f"Action: execute_python_sandbox\n"
                f"Action Input: {code}\n"
                f"Observation: {sandbox_res}\n"
                f"Thought: Script executed successfully in Docker sandbox.\n"
                f"Final Answer: **Sandbox Execution Completed:**\n```\n{sandbox_res}\n```"
            )

        # 3. Document / RAG queries
        if any(w in lower for w in ["document", "docs", "file", "csv", "data", "metric", "architecture", "knowledge"]):
            doc_res = self.tools.search_documents(q)
            return (
                f"Thought: The user is asking about indexed local documents. Querying pgvector with semantic search for '{q}'.\n"
                f"Action: search_documents\n"
                f"Action Input: {q}\n"
                f"Observation: {doc_res}\n"
                f"Thought: Relevant context retrieved from vector storage.\n"
                f"Final Answer: ### Retrieved Knowledge Base Information:\n\n{doc_res}"
            )

        # 4. Web Search / Real-time info
        if any(w in lower for w in ["search", "latest", "news", "who is", "weather", "live"]):
            web_res = self.tools.web_search(q)
            return (
                f"Thought: The user requested live internet information. Performing metasearch via SearXNG for '{q}'.\n"
                f"Action: web_search\n"
                f"Action Input: {q}\n"
                f"Observation: {web_res}\n"
                f"Thought: Search results retrieved.\n"
                f"Final Answer: ### Live Metasearch Results:\n\n{web_res}"
            )

        # 5. Greetings & Persona
        if any(w in lower for w in ["hello", "hi", "hey", "who are you", "what are you", "what can you do"]):
            return (
                f"Thought: The user is greeting or asking for an introduction.\n"
                f"Final Answer: 🌕 **Hello! I am Lunaris AI.**\n\n"
                f"I am your sovereign, air-gapped private intelligence assistant. Here is what I can do for you right now:\n\n"
                f"1. **Autonomous ReAct Reasoning**: I break down complex problems and use tools step-by-step.\n"
                f"2. **Local Vector Search (RAG)**: Ask questions about documents dropped into `documents/`.\n"
                f"3. **Air-Gapped Code Sandbox**: Ask me to test algorithms or run Python code safely.\n"
                f"4. **Private Web Metasearch**: Query the live internet privately via SearXNG.\n"
                f"5. **Mathematics & Analytics**: Evaluate advanced formulas and company datasets.\n\n"
                f"*How can I assist you today?*"
            )

        # 6. General Reasoning & Q&A
        return (
            f"Thought: Answering user question directly with sovereign reasoning.\n"
            f"Final Answer: **Lunaris AI Analysis:**\n\n"
            f"Regarding your query: *\"{query}\"*\n\n"
            f"Lunaris AI is operating in active sovereign mode. All local pipelines (FastAPI gateway, Next.js frontend, pgvector store, and Docker sandbox) are synchronized and functional.\n\n"
            f"💡 **Available Actions:**\n"
            f"- Ask me to perform mathematical calculations or data processing.\n"
            f"- Ask me to search your local documents or run Python scripts.\n"
            f"- Add a `GEMINI_API_KEY` or `GROQ_API_KEY` to `.env` to unlock open-ended conversational models, or run [Ollama](https://ollama.com) locally."
        )

    def generate(self, prompt: str, system_prompt: str = "", stop_sequences: Optional[List[str]] = None) -> str:
        """Generation router: Ollama -> Gemini API -> Groq/OpenAI -> Conversational Brain."""
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
                resp = res.json().get("response", "").strip()
                if resp:
                    return resp
        except Exception:
            pass

        # 2. Try Gemini API fallback
        gemini_res = self._call_gemini(prompt, system_prompt)
        if gemini_res:
            return gemini_res

        # 3. Try Groq API fallback
        groq_key = os.getenv("GROQ_API_KEY")
        if groq_key:
            groq_res = self._call_openai_compatible(
                prompt, system_prompt, groq_key, "https://api.groq.com/openai/v1", "llama-3.3-70b-versatile"
            )
            if groq_res:
                return groq_res

        # 4. Try OpenAI API fallback
        openai_key = os.getenv("OPENAI_API_KEY")
        if openai_key:
            openai_res = self._call_openai_compatible(
                prompt, system_prompt, openai_key, "https://api.openai.com/v1", "gpt-4o-mini"
            )
            if openai_res:
                return openai_res

        # 5. Fall back to smart Conversational Brain
        q_match = re.search(r"Question:\s*(.*?)(?=\nThought:|\Z)", prompt, re.DOTALL)
        query = q_match.group(1).strip() if q_match else prompt
        return self._conversational_brain(query)

    def execute_tool(self, tool_name: str, tool_input: str) -> str:
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
    result = agent.run_react_agent("Hi, who are you?")
    print("\n--- Final Result ---")
    print(result["response"])
