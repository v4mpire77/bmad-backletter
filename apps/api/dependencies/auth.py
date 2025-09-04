from typing import Callable
from fastapi import Depends, Header, HTTPException, status

from ..models.user import Role, User


async def get_current_user(x_user_role: str = Header(...)) -> User:
    """Retrieve the current user from request headers.

    This simplistic implementation expects an ``X-User-Role`` header and
    returns a mock ``User`` instance. In a real application this would validate
    a session or token and fetch the user from a database.
    """
    try:
        role = Role(x_user_role.lower())
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid role") from exc
    return User(id="test-user", email="test@example.com", role=role)


def require_role(required_role: Role) -> Callable[[User], User]:
    """Dependency factory enforcing that the user has ``required_role``."""

    def role_checker(user: User = Depends(get_current_user)) -> User:
        if user.role != required_role:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Operation not permitted")
        return user

    return role_checker
