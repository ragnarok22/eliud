try:
    import eliud  # noqa: F401
except ImportError as e:
    raise RuntimeError(
        "Eliud module not found, reference tests/README.md for instructions."
    ) from e

if __name__ == "__main__":
    pass
