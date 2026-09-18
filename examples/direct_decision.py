from hermes_jev.engine import DecisionEngine

engine = DecisionEngine()
result = engine.decide(
    state={"task": "run unit tests", "changed_files": 4},
    instructions="Choose where this job should run.",
    choices=["LOCAL", "GPU_WORKER", "CLOUD"],
    criteria={
        "LOCAL": "Normal CPU-bound development work.",
        "GPU_WORKER": "Requires CUDA or substantial GPU compute.",
        "CLOUD": "Requires isolated or elastic remote compute.",
    },
    contract="example/worker-route/v1",
)
print(result.as_dict())
