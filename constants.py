from enum import IntEnum, unique

@unique
class TaskStatus(IntEnum):
    """
    Types of Task Status (NOT_STARTED/IN_PROGRESS/COMPLETED)
    """

    NOT_STARTED = 0
    IN_PROGRESS = 1
    COMPLETED = 2

RESPONSE_STATUS_KWD = "status"
RESPONSE_MSG_KWD = "msg"
DEFAULT_API_RESPONSE_OBJ = {
    RESPONSE_STATUS_KWD: False,
    RESPONSE_MSG_KWD: "TODO",
}