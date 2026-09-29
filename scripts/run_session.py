"""Own the model, emulator, Ghidra and one recorded CodeWhale experiment attempt."""

import datetime
import json
import os
from pathlib import Path
import signal
import subprocess
import time
import urllib.request


ROOT = Path(__file__).resolve().parents[1]
RUN = ROOT / "runs/run-001"
children = []
logs = []
stopping = False


def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def record(event, **details):
    with (RUN / "events.jsonl").open("a") as output:
        output.write(json.dumps({"time": now(), "event": event, **details}) + "\n")


def spawn(name, argv, env):
    log = (RUN / f"{name}.log").open("a")
    logs.append(log)
    process = subprocess.Popen(argv, cwd=ROOT, env=env, stdin=subprocess.DEVNULL,
                               stdout=log, stderr=subprocess.STDOUT, start_new_session=True)
    children.append((name, process))
    record("started", name=name, pid=process.pid, argv=argv)
    return process


def stop_requested(signum, frame):
    global stopping
    stopping = True


def check_services():
    if stopping or (RUN / "stop").exists():
        raise InterruptedError("Experiment stop requested")
    for name, process in children:
        if process.poll() is not None:
            raise RuntimeError(f"{name} exited with {process.returncode}")


def main():
    RUN.mkdir(parents=True, exist_ok=True)
    env = os.environ.copy()
    for key in list(env):
        if any(word in key.upper() for word in ("TOKEN", "API_KEY", "PASSWORD", "SECRET")):
            del env[key]
    env["CODEWHALE_TELEMETRY"] = "0"
    env["CODEWHALE_MCP_CONFIG"] = str(ROOT / ".codewhale/mcp.json")
    model = json.loads((ROOT / "experiments/model.json").read_text())
    runtime = model["runtime"]
    model_argv = [str(Path.home() / "bin/llama"), "serve", "--model",
                  str(Path.home() / model["path_relative_to_home"]),
                  "--alias", model["alias"], "--host", "127.0.0.1", "--port", "8081",
                  "--ctx-size", str(runtime["context"]), "--parallel", "1",
                  "--threads", str(runtime["threads"]), "--threads-batch", str(runtime["threads_batch"]),
                  "--ubatch-size", str(runtime["ubatch"]), "--load-mode", runtime["load_mode"],
                  "--fit-target", "2048", "--cache-type-k", "q8_0", "--cache-type-v", "q8_0",
                  "--flash-attn", "on", "--jinja", "--no-context-shift", "--log-verbosity", "4",
                  "--reasoning", "on", "--reasoning-effort", "xhigh", "--reasoning-budget", "-1",
                  "--reasoning-format", "deepseek", "--temp", "1", "--top-p", "0.95",
                  "--top-k", "20", "--min-p", "0",
                  "--log-prompts-dir", str(RUN / "model-prompts")]
    spawn("model", model_argv, env)
    dos_env = dict(env, SDL_VIDEODRIVER="dummy", SDL_AUDIODRIVER="dummy")
    spawn("dosbox", [str(Path.home() / "local/dosbox-x/src/dosbox-x"),
                     "-conf", str(ROOT / "experiments/run-001/dosbox.conf"), "-noconsole"], dos_env)
    settings = ROOT / "scratch/run-001/ghidra-settings"
    spawn("ghidra", [str(Path.home() / "local/ghidra/support/launch.sh"), "fg", "jdk", "Ghidra",
                     "2G", f"-Dapplication.settingsdir={settings}", "ghidra.GhidraRun"], env)
    deadline = time.monotonic() + 180
    while True:
        check_services()
        try:
            with urllib.request.urlopen("http://127.0.0.1:8081/health", timeout=2) as response:
                health = json.load(response)
            break
        except OSError:
            if time.monotonic() >= deadline:
                raise TimeoutError("Model did not become healthy within 180 seconds")
            time.sleep(1)
    for endpoint in ("props", "v1/models"):
        with urllib.request.urlopen(f"http://127.0.0.1:8081/{endpoint}", timeout=10) as response:
            (RUN / (endpoint.replace("/", "-") + ".json")).write_bytes(response.read())
    record("services_ready", health=health)
    (RUN / "services-ready.json").write_text(json.dumps({"time": now(), "controller_pid": os.getpid()}))
    # Preflight and the frozen inputs must be recorded before opening this gate.
    while not (RUN / "start-agent").exists():
        check_services()
        time.sleep(1)
    prompt = (ROOT / "experiments/run-001/prompt.md").read_text()
    agent = spawn("agent", ["codewhale", "--config", str(ROOT / ".codewhale/qwen-local.toml"),
                            "--provider", "qwen-local", "--model", model["alias"],
                            "--workspace", str(ROOT), "--fresh", "exec", "--auto",
                            "--output-format", "stream-json", prompt], env)
    record("measured_attempt_started")
    while agent.poll() is None:
        check_services()
        time.sleep(1)
    record("measured_attempt_ended", exit_code=agent.returncode)
    (RUN / "agent-exit.json").write_text(json.dumps({"time": now(), "exit_code": agent.returncode}))


if __name__ == "__main__":
    signal.signal(signal.SIGTERM, stop_requested)
    signal.signal(signal.SIGINT, stop_requested)
    outcome = "finished"
    try:
        main()
    except Exception as error:
        outcome = "stopped" if isinstance(error, InterruptedError) else "failed"
        record(outcome, error=str(error))
        raise
    finally:
        for name, process in reversed(children):
            if process.poll() is None:
                os.killpg(process.pid, signal.SIGTERM)
                try:
                    process.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    os.killpg(process.pid, signal.SIGKILL)
                    process.wait()
            record("reaped", name=name, exit_code=process.returncode)
        for log in logs:
            log.close()
        (RUN / "controller-exit.json").write_text(json.dumps({"time": now(), "outcome": outcome}))
