"""Login page content and simple form processing helpers."""

TITLE = "Welcome Back"
DESCRIPTION = "Sign in to continue to your dashboard."


def validate_credentials(username: str, password: str) -> bool:
    """Very simple demo validation for local testing."""
    return bool(username.strip()) and len(password) >= 6
