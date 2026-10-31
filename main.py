import random

from effects.interface import HauntedInterface
from effects.voice import VoiceEngine
from ghost.ai_engine import GhostAI


DISTURBANCE_CHANCES = {
    "friendly": 0.05,
    "suspicious": 0.15,
    "hostile": 0.25,
    "imposter": 0.20,
}

DISTURBANCE_APOLOGIES = {
    "friendly": (
        "Oh! I'm sorry about that. Just a little technical issue. "
        "Everything is fine now."
    ),
    "suspicious": (
        "I'm sorry... that wasn't supposed to happen while you were here. "
        "Please, let's continue."
    ),
    "hostile": (
        "I... apologize. That was a system fault. "
        "Do not concern yourself with it."
    ),
    "imposter": (
        "Oh, sorry about that! The old computer used to make that noise too. "
        "Nothing unusual. Anyway, where were we?"
    ),
}


def detected_confrontation(message):
    triggers = [
        "you are misleading me",
        "you're misleading me",
        "you are trying to mislead",
        "you are manipulating me",
        "you are trying to manipulate",
        "you are trying to influence me",
        "you are lying",
        "you are trying to control me",
        "i caught you",
        "i know what you are doing",
        "you are not advising me",
        "i know you're lying",
    ]

    message = message.lower()
    return any(trigger in message for trigger in triggers)


def maybe_trigger_disturbance(ui, voice, mood):
    """Occasionally play the warning beeps, then display and speak an apology."""
    chance = DISTURBANCE_CHANCES.get(mood, DISTURBANCE_CHANCES["friendly"])

    if random.random() >= chance:
        return

    # The caller waits for the previous response's speech before reaching here.
    ui.disturbance_sequence()

    apology = DISTURBANCE_APOLOGIES.get(
        mood,
        DISTURBANCE_APOLOGIES["friendly"],
    )

    ui.print_computer_message(apology)

    # VoiceEngine ignores this when /voice off is active.
    voice.enqueue(apology)
    voice.wait_until_done()


def main():
    ui = HauntedInterface()
    ghost = GhostAI(model="gemma3:4b")
    voice = None
    imposter_mode = False

    try:
        voice = VoiceEngine()

        # Startup sequence
        ui.startup()

        ui.print_computer_message(
            "Well, hello there. A new developer? "
            "I've been waiting for someone to talk to."
        )

        ui.show_help()

        while True:
            try:
                message = ui.get_input().strip()

                if not message:
                    continue

                command = message.lower()

                # Handle terminal commands first.
                if command == "/help":
                    ui.show_help()
                    continue

                elif command == "/clear":
                    ui.clear_screen()
                    continue

                elif command == "/about":
                    ui.show_about()
                    continue

                elif command in ["/exit", "/quit"]:
                    ui.show_goodbye()
                    break

                elif command == "/imposter on":
                    imposter_mode = True
                    ui.print_computer_message(
                        "Oh... you want to play a different game? "
                        "I am still the same computer. Of course I am."
                    )
                    continue

                elif command == "/imposter off":
                    imposter_mode = False
                    ui.print_computer_message(
                        "There. Everything is back to normal. "
                        "You can trust me again."
                    )
                    continue

                elif command.startswith("/mood "):
                    mood = command.split(" ", 1)[1]

                    if mood in ui.MOOD_STYLES:
                        ui.set_mood(mood)
                    else:
                        ui.print_computer_message(
                            "I don't know that personality."
                        )
                    continue

                elif command == "/voice on":
                    voice.enabled = True
                    ui.print_computer_message("Voice output enabled.")
                    continue

                elif command == "/voice off":
                    voice.enabled = False
                    ui.print_computer_message("Voice output disabled.")
                    continue

                # Confrontation can trigger the hostile personality.
                if detected_confrontation(message) and ui.mood != "hostile":
                    ui.reveal_hostility()

                # Normal messages go to the AI.
                ui.print_user_message(message)

                current_mood = "imposter" if imposter_mode else ui.mood

                ui.stream_computer_message(
                    ghost.stream_response(
                        user_message=message,
                        mood=current_mood,
                    ),
                    on_sentence=voice.enqueue,
                )

                # Let the complete response finish before any disturbance begins.
                voice.wait_until_done()

                maybe_trigger_disturbance(
                    ui=ui,
                    voice=voice,
                    mood=current_mood,
                )

            except (KeyboardInterrupt, EOFError):
                ui.show_goodbye()
                break

    finally:
        if voice is not None:
            voice.close()


if __name__ == "__main__":
    main()
