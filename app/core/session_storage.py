from collections import defaultdict

class ChatStorage:
    def __init__(self):
        self._storage: dict[str, list[dict[str, str]]] = defaultdict(list)

    def add(self, identifier: str, user: str, assistant: str) -> None:
        """Add a conversation turn."""
        self._storage[identifier].append({
            "user": user,
            "assistant": assistant,
        })

    def get(self, identifier: str) -> list[dict[str, str]]:
        """Return conversation history."""
        return self._storage.get(identifier, [])

    def clear(self, identifier: str) -> None:
        """Clear one conversation."""
        self._storage.pop(identifier, None)

    def remove_last(self, identifier: str) -> None:
        """Remove the most recent conversation turn."""
        if self._storage.get(identifier):
            self._storage[identifier].pop()

    def set(self, identifier: str, history: list[dict[str, str]]) -> None:
        """Replace the entire history."""
        self._storage[identifier] = history

    def all(self) -> dict[str, list[dict[str, str]]]:
        """Return all stored conversations."""
        return self._storage
    

storage=ChatStorage()