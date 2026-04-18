from tts_app.core.speaker import State

ICON_FOR_STATE: dict[State, str] = {
    State.LOADING: "⋯",
    State.IDLE: "🔈",
    State.CAPTURING: "📋",
    State.GENERATING: "✨",
    State.SPEAKING: "🔊",
    State.INTERRUPTING: "✕",
}

DEFAULT_ICON = ICON_FOR_STATE[State.LOADING]
