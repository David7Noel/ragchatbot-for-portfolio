try:
    import fastapi
    print("FastAPI ist installiert.")
except ImportError:
    print("FastAPI ist nicht installiert.")

try:
    from dotenv import load_dotenv
    print("python-dotenv ist installiert.")
except ImportError:
    print("python-dotenv ist nicht installiert.")
