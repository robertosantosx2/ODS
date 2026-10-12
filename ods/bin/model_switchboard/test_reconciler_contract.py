"""Contract tests for the Model Switchboard runtime activation boundary."""

from __future__ import annotations

from datetime import datetime, timezone

from ods.bin.model_switchboard.adapters import CafeLlamaAdapter, ContainerLlamaAdapter
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

def test_cafe_llama_route_is_accepted_by_model_state(tmp_path):
    from ods.bin.model_switchboard.state import read_state, record_verified_route

    state_path = tmp_path / "model-state.json"
    record_verified_route(
        state_path,
        catalog_id="test-model",
        runtime_model_id="/models/test.gguf",
        backend_kind="cafe-llama",
        endpoint_id="cafe-llama-default",
        context_length=4096,
        capabilities={"chat": True, "tools": False, "vision": False, "agentViable": False},
        proof_identity="/models/test.gguf",
        proof_completion=True,
    )
    state, errors = read_state(state_path)
    assert errors == []
    assert state["active"]["backend"] == {
        "kind": "cafe-llama",
        "endpointId": "cafe-llama-default",
        "nativeRoute": None,
    }


def test_cafe_llama_adapter_is_explicitly_identified_and_requires_real_completion():
    def wait_ready(env, gguf_file, context_length, *, lemonade_model_id=""):
        return {**PROOF, "verifiedAt": datetime.now(timezone.utc).isoformat()}

    adapter = CafeLlamaAdapter(
        restart=lambda env: None,
        wait_ready=wait_ready,
        expected_gguf="/models/test.gguf",
        context_length=4096,
    )
    identity = adapter.verify_identity({})
    completion = adapter.verify_completion({})

    assert adapter.kind == "cafe-llama"
    assert identity["ok"] is True
    assert completion["ok"] is True
    assert completion["runtimeKind"] == "cafe-llama"
    assert completion["completionVerified"] is True

