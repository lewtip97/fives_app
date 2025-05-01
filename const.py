from pathlib import Path


APP_DIR = Path.cwd()

STATE_PATH                = APP_DIR / "state"
SESSION_STATE_FILE_PATH   = STATE_PATH / "session_state.json"

RANDOM_SEED = 1337