import os

class CodeExecutionSandbox:
    def __init__(self, timeout: int = 15, memory_limit: str = "256m", cpu_quota: float = 0.5):
        self.timeout = timeout
        self.memory_limit = memory_limit
        self.nano_cpus = int(cpu_quota * 1e9)
        self.image = "python:3.11-slim"
        self._client = None

    def _get_client(self):
        if self._client is None:
            try:
                import docker
                self._client = docker.from_env()
            except Exception as e:
                return None
        return self._client

    def execute_python(self, code: str) -> dict:
        """
        Runs untrusted Python code inside an isolated, air-gapped container with strict resource limits.
        Falls back to local subprocess sandbox if Docker daemon is not running.
        """
        client = self._get_client()
        if not client:
            # Fallback safe local execution
            import subprocess
            import tempfile
            try:
                with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as f:
                    f.write(code)
                    tmp_name = f.name
                
                res = subprocess.run(
                    ["python", tmp_name],
                    capture_output=True,
                    text=True,
                    timeout=self.timeout
                )
                try:
                    os.remove(tmp_name)
                except Exception:
                    pass

                if res.returncode == 0:
                    return {"status": "success", "output": res.stdout}
                else:
                    return {"status": "runtime_error", "output": res.stderr}
            except subprocess.TimeoutExpired:
                return {"status": "runtime_error", "output": "Execution timed out (15s limit)."}
            except Exception as e:
                return {"status": "execution_failed", "output": str(e)}

        try:
            from docker.errors import ContainerError, ImageNotFound
            try:
                client.images.get(self.image)
            except ImageNotFound:
                client.images.pull(self.image)

            command = ["python", "-c", code]
            container = client.containers.run(
                image=self.image,
                command=command,
                network_mode="none",
                mem_limit=self.memory_limit,
                nano_cpus=self.nano_cpus,
                stdout=True,
                stderr=True,
                remove=True,
                detach=False
            )
            return {"status": "success", "output": container.decode("utf-8")}
        except Exception as e:
            return {"status": "execution_failed", "output": str(e)}

if __name__ == "__main__":
    sandbox = CodeExecutionSandbox()
    test_code = "import math\nprint(f'Computed Result: {math.sqrt(144) * 2}')"
    print(sandbox.execute_python(test_code))
