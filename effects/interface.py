import random

import sys

import time

import re

from rich.align import Align

from rich.console import Console

from rich.panel import Panel

from rich.text import Text

import random

import threading

import winsound

class HauntedInterface:

    MOOD_STYLES = {

        "friendly": {

            "color": "bright_cyan",

            "border": "cyan",

            "status": "ONLINE",

        },

        "suspicious": {

            "color": "yellow",

            "border": "yellow",

            "status": "SOMETHING IS WRONG",

        },

        "hostile": {

            "color": "bright_red",

            "border": "red",

            "status": "SYSTEM COMPROMISED",

        },

    }

    def __init__(self):

        self.console = Console()

        self.mood = "friendly"

    def startup(self):

        self.console.clear()

        title = Text()

        title.append("THE LAST DEVELOPER", style="bold bright_red")

        title.append("\n")

        title.append("Your code is never alone.", style="italic dim")

        self.console.print()

        self.console.print(

            Panel(

                Align.center(title, vertical="middle"),

                border_style="bright_red",

                padding=(2, 4),

                width=65,

            ),

            justify="center",

        )

        self.console.print()

        self.console.print(

            Align.center(

                "[dim]Initializing system components...[/dim]",

                width=65,

            )

        )

        self.typewriter("Loading memory modules...", "dim")

        self.typewriter("Connecting to the computer...", "dim")

        self.typewriter("Establishing connection...", "dim")

        self.console.print()

        self.console.print(

            Align.center(

                "[bold bright_green]CONNECTION ESTABLISHED[/bold bright_green]",

                width=65,

            )

        )

        self.console.print()

        self.show_status()

    def set_mood(self, mood):

        if mood not in self.MOOD_STYLES:

            return

        self.mood = mood

        self.console.print()

        self.show_status()

        if mood == "hostile":

            self.glitch_smile()

    def print_user_message(self, message):

        self.console.print(

            Panel(

                Text(message, style="white"),

                title="[bold bright_green]YOU[/bold bright_green]",

                border_style="green",

                padding=(0, 1),

            )

        )

    def print_computer_message(self, message):

        style = self.MOOD_STYLES[self.mood]

        self.console.print()

        self.console.print(

            f"[bold {style['color']}]COMPUTER[/bold {style['color']}]"

        )

        self.typewriter(

            message,

            style=style["color"],

        )

        self.console.print()

    def typewriter(self, message, style="white"):

        """Print text one character at a time."""

        for character in message:

            self.console.print(

                Text(character, style=style),

                end="",

                soft_wrap=True,

                highlight=False,

            )

            sys.stdout.flush()

            # Small random variation makes the typing less mechanical.

            time.sleep(random.uniform(0.015, 0.045))

        self.console.print()

    def glitch_smile(self):

        faces = [

            r"""

              .--------.

             /  O    O  \\

            |     __     |

            |   \\____/   |

             \          /

              '--------'

            """,

            r"""

              .--------.

             /  X    X  \\

            |     __     |

            |   \\____/   |

             \   ____   /

              '--------'

            """,

            r"""

              .--------.

             /  O    O  \\

            |     --     |

            |   \\____/   |

             \  //////  /

              '--------'

            """,

        ]

        for face in faces:

            self.console.print(

                face,

                style="bold bright_red",

                justify="center"

            )

            time.sleep(0.25)

            self.console.clear()

        self.console.print(

            r"""

                 .--------.

                /  O    O  \\

               |     __     |

               |   \\____/   |

                \  //////  /

                 '--------'

            """,

            style="bold bright_red",

            justify="center"

        )

    def reveal_hostility(self):

        self.mood = "hostile"

        self.console.clear()

        self.console.print(

            "\n[bold bright_red]!!! UNAUTHORIZED PATTERN RECOGNIZED !!![/bold bright_red]",

            justify="center"

        )

        time.sleep(0.5)

        self.glitch_smile()

        self.console.print(

            "\n[bold red]YOU WERE NOT SUPPOSED TO NOTICE.[/bold red]",

            justify="center"

        )

        time.sleep(0.5)

        self.show_status()

    def get_input(self):

        self.console.print(

            "[bold bright_green]YOU[/bold bright_green]",

            end=" ",

        )

        return self.console.input("[bold green]> [/bold green]")

    def show_goodbye(self):

        self.console.print()

        self.typewriter(

            "Shutting down...",

            style="dim",

        )

        self.typewriter(

            "I'll be waiting for you.",

            style="bold bright_red",

        )

        self.console.print()

    def show_help(self):

        help_text = """

[bold bright_green]AVAILABLE COMMANDS[/bold bright_green]

[green]/help[/green]                 Show these instructions

[green]/clear[/green]                Clear the terminal

[green]/about[/green]                Information about this computer

[green]/exit[/green]                 Disconnect from the computer

[bold yellow]DEVELOPER TEST COMMANDS[/bold yellow]

[yellow]/mood friendly[/yellow]       Restore friendly personality

[yellow]/mood suspicious[/yellow]    Trigger suspicious personality

[yellow]/mood hostile[/yellow]       Trigger hostile personality
[yellow]/imposter on[/yellow]        Enable the fake-friendly personality
[yellow]/imposter off[/yellow]       Disable the imposter personality

[bold cyan]HOW TO INTERACT[/bold cyan]

\- Type any message to talk to the computer.

\- You can type programming commands as messages.

\- The computer will interpret them conversationally.

\- No commands are actually executed.

\- Ask questions, have conversations, and see how

  the computer reacts to your behaviour.

[dim]Tip: The computer remembers your conversation

for the duration of the current session.[/dim]

"""

        self.console.print(

            Panel(

                help_text,

                title="[bold bright_cyan]SYSTEM MANUAL[/bold bright_cyan]",

                border_style="cyan",

                padding=(1, 2),

            )

        )

    def disturbance_sequence(self):
        """Play 2-3 irregular warning beeps, then leave an unsettling silence."""
        beep_count = random.choice([2, 3])

        try:
            for index in range(beep_count):
                frequency = random.choice([780, 900, 1050, 1200])
                duration = random.randint(90, 160)

                winsound.Beep(frequency, duration)

                if index < beep_count - 1:
                    time.sleep(random.uniform(0.30, 0.75))

        except (RuntimeError, OSError):
            # The visual/text experience should continue if system audio is unavailable.
            pass

        time.sleep(random.uniform(1.2, 1.8))

    def show_about(self):

        self.console.print(

            Panel(

                "[bold bright_red]THE LAST DEVELOPER[/bold bright_red]\n\n"

                "A haunted AI chatbot living inside your terminal.\n\n"

                "[dim]Powered by Python, Rich, Ollama and Gemma.[/dim]\n"

                "Status: Connected",

                title="[bold cyan]ABOUT THIS COMPUTER[/bold cyan]",

                border_style="red",

            )

        )

    def clear_screen(self):

        self.console.clear()

        self.show_status()

    def show_status(self):

        mood_data = self.MOOD_STYLES.get(

            self.mood,

            self.MOOD_STYLES["friendly"]

        )

        self.console.print(

            f"\n[{mood_data['color']}]"

            f"[bold]SYSTEM STATUS: {mood_data['status']}[/bold]"

            f"[/{mood_data['color']}]\n"

        )

    def stream_computer_message(self, response_stream, on_sentence=None):

        style = self.MOOD_STYLES[self.mood]

        self.console.print()

        self.console.print(

            f"[bold {style['color']}]COMPUTER[/bold {style['color']}]"

        )

        full_response = ""

        speech_buffer = ""

        for token in response_stream:

            full_response += token

            speech_buffer += token

            self.console.print(

                Text(token, style=style["color"]),

                end="",

                soft_wrap=True,

                highlight=False,

            )

            # Send completed sentences to ElevenLabs.

            if on_sentence:

                parts = re.split(r"(?<=[.!?])\s+", speech_buffer)

                if len(parts) > 1:

                    for sentence in parts[:-1]:

                        if sentence.strip():

                            on_sentence(sentence)

                    speech_buffer = parts[-1]

        # Send the final incomplete sentence.

        if on_sentence and speech_buffer.strip():

            on_sentence(speech_buffer)

        self.console.print("\n")

        return full_response
