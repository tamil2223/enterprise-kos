from __future__ import annotations

import time
import uuid

from app.playground.models import RunState


class PlaygroundStore:
    def __init__(self) -> None:
        self._runs: dict[str, RunState] = {}

    def create_run(self) -> RunState:
        run_id = str(uuid.uuid4())
        run = RunState(run_id=run_id, created_at=time.time())
        self._runs[run_id] = run
        return run

    def get_run(self, run_id: str) -> RunState:
        return self._runs[run_id]


store = PlaygroundStore()

