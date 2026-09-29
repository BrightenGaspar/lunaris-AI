import docker
from docker.errors import ContainerError, ImageNotFound

class CodeExecutionSandbox:
    def __init__(self, timeout: int = 15, memory_limit: str = "256m", cpu_quota: float = 0.5):
        self.client = docker.from_env()
        self.timeout = timeout
        self.memory_limit = memory_limit
        self.nano_cpus = int(cpu_quota * 1e9)
        self.image = "python:3.11-slim"

    def execute_python(self, code: str) -> dict:
        """
        Runs untrusted Python code inside an isolated, air-gapped container with strict resource limits.
        """
        try:
            self.client.images.get(self.image)
        except ImageNotFound:
            self.client.images.pull(self.image)

        command = ["python", "-c", code]
        try:
            container = self.client.containers.run(
                image=self.image,
                command=command,
                network_mode="none",         # Air-gapped, zero external network
                mem_limit=self.memory_limit,     # Memory cap
                nano_cpus=self.nano_cpus,        # CPU cap
                stdout=True,
                stderr=True,
                remove=True,                     # Clean up container immediately after execution
                detach=False
            )
            return {"status": "success", "output": container.decode("utf-8")}
        except ContainerError as e:
            return {"status": "runtime_error", "output": e.stderr.decode("utf-8")}
        except Exception as e:
            return {"status": "execution_failed", "output": str(e)}

if __name__ == "__main__":
    sandbox = CodeExecutionSandbox()
    test_code = "import math\nprint(f'Computed Result: {math.sqrt(144) * 2}')"
    print(sandbox.execute_python(test_code))
