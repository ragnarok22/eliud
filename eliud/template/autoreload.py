from pathlib import Path

from eliud.dispatch import receiver
from eliud.template import engines
from eliud.template.backends.eliud import EliudTemplates
from eliud.utils._os import to_path
from eliud.utils.autoreload import autoreload_started, file_changed, is_eliud_path


def get_template_directories():
    # Iterate through each template backend and find
    # any template_loader that has a 'get_dirs' method.
    # Collect the directories, filtering out Eliud templates.
    cwd = Path.cwd()
    items = set()
    for backend in engines.all():
        if not isinstance(backend, EliudTemplates):
            continue

        items.update(cwd / to_path(dir) for dir in backend.engine.dirs if dir)

        for loader in backend.engine.template_loaders:
            if not hasattr(loader, "get_dirs"):
                continue
            items.update(
                cwd / to_path(directory)
                for directory in loader.get_dirs()
                if directory and not is_eliud_path(directory)
            )
    return items


def reset_loaders():
    for backend in engines.all():
        if not isinstance(backend, EliudTemplates):
            continue
        for loader in backend.engine.template_loaders:
            loader.reset()


@receiver(autoreload_started, dispatch_uid="template_loaders_watch_changes")
def watch_for_template_changes(sender, **kwargs):
    for directory in get_template_directories():
        sender.watch_dir(directory, "**/*")


@receiver(file_changed, dispatch_uid="template_loaders_file_changed")
def template_changed(sender, file_path, **kwargs):
    if file_path.suffix == ".py":
        return
    for template_dir in get_template_directories():
        if template_dir in file_path.parents:
            reset_loaders()
            return True
