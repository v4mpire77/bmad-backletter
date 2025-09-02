from __future__ import annotations

from enum import Enum
from typing import Mapping

from fastapi import status
from fastapi.responses import JSONResponse


class ErrorCode(str, Enum):
    """Enumerated application error codes."""

    NOT_FOUND = "not_found"
    EMAIL_ALREADY_REGISTERED = "email_already_registered"
    INCORRECT_CREDENTIALS = "incorrect_credentials"
    NO_ORG_MEMBERSHIP = "no_org_membership"
    UNSUPPORTED_FILE_TYPE = "unsupported_file_type"
    FILE_TOO_LARGE = "file_too_large"
    DISK_IO_ERROR = "disk_io_error"


_STATUS_MAP: dict[ErrorCode, int] = {
    ErrorCode.NOT_FOUND: status.HTTP_404_NOT_FOUND,
    ErrorCode.EMAIL_ALREADY_REGISTERED: status.HTTP_409_CONFLICT,
    ErrorCode.INCORRECT_CREDENTIALS: status.HTTP_401_UNAUTHORIZED,
    ErrorCode.NO_ORG_MEMBERSHIP: status.HTTP_403_FORBIDDEN,
    ErrorCode.UNSUPPORTED_FILE_TYPE: status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
    ErrorCode.FILE_TOO_LARGE: status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
    ErrorCode.DISK_IO_ERROR: status.HTTP_500_INTERNAL_SERVER_ERROR,
}


def error_response(
    code: ErrorCode,
    detail: str,
    *,
    status_code: int | None = None,
    headers: Mapping[str, str] | None = None,
) -> JSONResponse:
    """Return a standardized JSON error response."""
    status_code = status_code or _STATUS_MAP.get(code, status.HTTP_400_BAD_REQUEST)
    return JSONResponse({"code": code.value, "detail": detail}, status_code=status_code, headers=headers)
