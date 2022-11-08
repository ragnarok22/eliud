"""
Invokes eliud when the eliud module is run as a script.

Example: python -m eliud check
"""
from eliud.core import management

if __name__ == "__main__":
    management.execute_from_command_line()
