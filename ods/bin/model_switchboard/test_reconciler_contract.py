"""Contract tests for the Model Switchboard runtime activation boundary."""

from __future__ import annotations

from datetime import datetime, timezone

from ods.bin.model_switchboard.adapters import ContainerLlamaAdapter
from ods.bin.model_switchboard.reconciler import run_runtime_activation


PROOF = {
    "identity": "/models/test.gguf",
    "contextLength": 4096,
    "contextVerified": True,
    "capabilities": {
        "chat": True,
        "tools": False,
        "vision": False,
        "agentViable": False,
    },
    "verifiedAt": datetime.now(timezone.utc).isoformat(),
}


class PlannedAdapter:
    kind = "test"

    def __init__(self, plan):
        self.plan = plan
        self.calls = []

    def stage(self, env):
        self.calls.append("stage")
        return self.plan.get("stage", {"ok": True})

    def verify_identity(self, env):
        self.calls.append("verify_identity")
        return self.plan.get("verify_identity", {"ok": True, **PROOF})

    def verify_completion(self, env):
        self.calls.append("verify_completion")
        return self.plan.get("verify_completion", {"ok": True, **PROOF})


def test_reconciler_rejects_truthy_non_boolean_ok():
    for invalid_ok in ("false", 1, [], {}):
        adapter = PlannedAdapter({"stage": {"ok": invalid_ok}})
        result = run_runtime_activation(adapter, {})
        assert result["ok"] is False
        assert result["phase"] == "stage"
        assert "boolean ok" in result["detail"]
        assert adapter.calls == ["stage"]


def test_reconciler_accepts_only_boolean_true():
    adapter = PlannedAdapter({})
    result = run_runtime_activation(adapter, {})
    assert result["ok"] is True
    assert adapter.calls == ["stage", "verify_identity", "verify_completion"]


def test_completion_phase_performs_a_fresh_probe():
    calls = []

    def wait_ready(env, gguf_file, context_length, *, lemonade_model_id=""):
        calls.append("probe")
        return {**PROOF, "verifiedAt": datetime.now(timezone.utc).isoformat()}

    adapter = ContainerLlamaAdapter(
        restart=lambda env: None,
        wait_ready=wait_ready,
        expected_gguf="/models/test.gguf",
        context_length=4096,
    )
    identity = adapter.verify_identity({})
    completion = adapter.verify_completion({})

    assert identity["ok"] is True
    assert completion["ok"] is True
    assert len(calls) == 2
    assert completion["detail"] == "fresh runtime completion probe succeeded"


def test_completion_probe_fails_if_runtime_identity_changes():
    calls = 0

    def wait_ready(env, gguf_file, context_length, *, lemonade_model_id=""):
        nonlocal calls
        calls += 1
        identity = "/models/test.gguf" if calls == 1 else "/models/other.gguf"
        return {**PROOF, "identity": identity}

    adapter = ContainerLlamaAdapter(
        restart=lambda env: None,
        wait_ready=wait_ready,
        expected_gguf="/models/test.gguf",
        context_length=4096,
    )
    assert adapter.verify_identity({})["ok"] is True
    result = adapter.verify_completion({})
    assert result["ok"] is False
    assert "identity changed" in result["detail"]
