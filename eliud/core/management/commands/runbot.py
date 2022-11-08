import errno
import os
import sys
from datetime import datetime
from typing import Dict

from eliud.conf import settings
from eliud.core.management import BaseCommand
from eliud.core.servers import run
from eliud.utils import autoreload


class Command(BaseCommand):
    help = "Starts a bot polling for development."

    def add_arguments(self, parser):
        parser.add_argument(
            "--noreload",
            action="store_false",
            dest="use_reloader",
            help="Tells Django to NOT use the auto-reloader.",
        )
        parser.add_argument(
            "--skip-checks",
            action="store_true",
            help="Skip system checks.",
        )

    def execute(self, *args, **options):
        if options["no_color"]:
            # We rely on the environment because it's currently the only
            # way to reach WSGIRequestHandler. This seems an acceptable
            # compromise considering `runserver` runs indefinitely.
            os.environ["ELIUD_COLORS"] = "nocolor"
        super().execute(*args, **options)

    def handle(self, *args, **options):
        # TODO: Check the variables
        self.run(**options)

    def get_handler(self, *args, **options):
        """Return the default handler for the runner."""
        return None

    def run(self, **options):
        """Run the bot, using the autoreloader if needed."""
        use_reloader = options["use_reloader"]

        if use_reloader:
            autoreload.run_with_reloader(self.inner_run, **options)
        else:
            self.inner_run(None, **options)

    def inner_run(self, *args, **options):
        # If an exception was silenced in ManagementUtility.execute in order
        # to be raised in the child process, raise it now.
        autoreload.raise_last_exception()

        threading = options["use_threading"]
        # 'shutdown_message' is a stealth option.
        shutdown_message = options.get("shutdown_message", "")
        quit_command = "CTRL-BREAK" if sys.platform == "win32" else "CONTROL-C"

        if not options["skip_checks"]:
            self.stdout.write("Performing system checks...\n\n")
            self.check(display_num_errors=True)
        # Need to check migrations here, so can't use the
        # requires_migrations_check attribute.
        self.check_migrations()
        now = datetime.now().strftime("%B %d, %Y - %X")
        self.stdout.write(now)
        self.stdout.write(
            (
                "Eliud version %(version)s, using settings %(settings)r\n"
                "Starting development bot\n"
                "Shutdown the bot with %(quit_command)s."
            )
            % {
                "version": self.get_version(),
                "settings": settings.SETTINGS_MODULE,
                "quit_command": quit_command,
            }
        )

        try:
            handler = self.get_handler(*args, **options)
            run(
                handler,
                threading=threading,
            )
        except OSError as e:
            # Use helpful error messages instead of ugly tracebacks.
            ERRORS: dict[int, str] = {
                errno.EACCES: "You don't have permission to access that port.",
                errno.EADDRINUSE: "That port is already in use.",
                errno.EADDRNOTAVAIL: "That IP address can't be assigned to.",
            }
            try:
                error_text = ERRORS[e.errno]
            except KeyError:
                error_text = e
            self.stderr.write(f"Error: {error_text}")
            # Need to use an OS exit because sys.exit doesn't work in a thread
            os._exit(1)
        except KeyboardInterrupt:
            if shutdown_message:
                self.stdout.write(shutdown_message)
            sys.exit(0)
