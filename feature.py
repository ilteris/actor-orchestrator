def get_greeting(name="Swarm Actor-Orchestrator"):
    """Returns a greeting string."""
    return f"Hello from the {name}!"

def hello_world():
    """Prints the greeting to stdout."""
    print(get_greeting())

if __name__ == "__main__":
    hello_world()