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
    "completionVerified": True,
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


def test_completion_phase_publishes_real_probe_evidence_without_restarting_readiness():
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
    assert len(calls) == 1
    assert completion["completionVerified"] is True
    assert completion["detail"] == "real runtime completion proven"


def test_reconciler_rejects_completion_without_real_generation_evidence():
    adapter = PlannedAdapter({"verify_completion": { "ok": True, **{k: v for k, v in PROOF.items() if k != "completionVerified"} }})
    result = run_runtime_activation(adapter, {})
    assert result["ok"] is False
    assert result["phase"] == "verify_completion"
    assert "real generated completion" in result["detail"]
