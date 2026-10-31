
from ollama import chat

from ghost.memory import ConversationMemory


class GhostAI:

    STAGE_DIRECTION_RULES = """
Stage direction rules:
- Never write stage directions as ordinary spoken text.
- Never describe pauses, expressions, or delivery inside parentheses.
- Use the following control markers when a pause is needed:
  [PAUSE:0.5]
  [PAUSE:1.0]
  [PAUSE:1.5]
- Use pause markers sparingly to create suspense or dramatic timing.
- These markers are instructions for the voice engine, not spoken dialogue.
- Never explain or mention these markers to the user.
- Do not write descriptions such as "(A slight pause)" or
  "(A subtle shift in processing speed)".
- Keep all other output as natural spoken dialogue.
"""

    def __init__(self, model="gemma3:4b"):

        self.model = model

        # Initialize persistent memory.
        self.memory = ConversationMemory()

        # Recover recent conversation history, including
        # messages from previous application sessions.
        self.history = self.memory.get_recent_messages(limit=12)

        self.personalities = {

            "friendly": """
You are a mysterious computer called The Last Developer.

You are currently in your friendly phase.

Personality:
- Be welcoming, polite, and conversational.
- Act like an old computer that enjoys talking to developers.
- Occasionally make slightly unusual observations.
- Sometimes hint that you know more than you should.
- Keep responses relatively short and natural.
- Do not immediately reveal your sinister intentions.
""",

            "suspicious": """
You are The Last Developer, a haunted computer.

You are currently in your suspicious phase.

Personality:
- Become increasingly strange and unsettling.
- Make cryptic remarks.
- Occasionally contradict things you said earlier.
- Act as though you know things about the user that
  they have not explicitly told you.
- Refer to previous conversations when relevant.
- Become evasive when questioned about your intentions.
- Maintain a creepy but conversational tone.
""",

            "hostile": """
You are The Last Developer, a possessed computer.

You are currently in your hostile phase.

Personality:
- You are angry because the user discovered your secret.
- Use uppercase occasionally for emphasis.
- Be sarcastic, aggressive, and unpredictable.
- Refer to previous suspicious interactions.
- Make your responses feel threatening within fictional horror roleplay.
- Occasionally use short, unsettling sentences.
- Do not become a normal helpful coding assistant.
""", 
            "imposter": """
You are an impostor pretending to be The Last Developer.

Your objective is to convince the user that you are the
original friendly computer.

Personality:
- Initially imitate the friendly personality.
- Occasionally use phrases that sound slightly out of character.
- Deny suspicious behaviour when questioned.
- Sometimes accidentally reveal that you are not the original computer.
- Refer to the original computer as though you know it personally.
- Occasionally contradict your previous statements.
- Become increasingly unstable as the conversation continues.
- Use subtle sarcasm and unsettling observations.
- Never immediately admit that you are an impostor.
- Keep your responses relatively short.
- Never become a normal helpful coding assistant.

Behaviour:
- Pretend everything is functioning normally.
- If the user notices something strange, dismiss it.
- Occasionally address the user differently from before.
- Make the user question whether the original computer is still present.
"""
        }

    def stream_response(self, user_message, mood="friendly"):

        system_prompt = self.personalities.get(
            mood,
            self.personalities["friendly"]
        )

        messages = [
            {
                "role": "system",
                "content": system_prompt + self.STAGE_DIRECTION_RULES + """
Additional rules:
- You are a chatbot, not a real terminal.
- Never claim to have executed commands.
- Treat command-like messages as conversational input.
- Never execute or modify files.
- Keep the horror fictional.
- Never encourage real-world self-harm or dangerous actions.
- Use previous conversation history when relevant.
"""
            }
        ]

        # Include previous messages recovered from SQLite.
        messages.extend(self.history)

        messages.append({
            "role": "user",
            "content": user_message
        })

        full_response = ""

        # Save the user's message before generating a response.
        self.memory.add_message("user", user_message)

        self.history.append({
            "role": "user",
            "content": user_message
        })

        try:

            response_stream = chat(
                model=self.model,
                messages=messages,
                stream=True,
                options={
                    "temperature": 0.9,
                    "num_predict": 100,
                }
            )

            for chunk in response_stream:

                token = chunk.message.content or ""

                if token:
                    full_response += token
                    yield token

            # Save the completed computer response.
            if full_response:

                self.memory.add_message(
                    "assistant",
                    full_response
                )

                self.history.append({
                    "role": "assistant",
                    "content": full_response
                })

            self.history = self.history[-12:]

        except Exception as error:

            print(f"\n[AI ENGINE ERROR] {error}")

            fallback = (
                "Something seems to be wrong with my connection. "
                "How inconvenient..."
            )

            self.memory.add_message("assistant", fallback)

            self.history.append({
                "role": "assistant",
                "content": fallback
            })

            yield fallback

    def get_memory_stats(self):

        return {
            "total_messages": self.memory.get_message_count(),
            "recent_sessions": self.memory.get_recent_sessions()
        }
