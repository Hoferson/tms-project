from enum import Enum
from dataclasses import dataclass, field
from uuid import UUID, uuid4

class TaskStatus(Enum):
    TODO = 'todo'
    IN_PROGRESS = 'in_progress'
    DONE = 'done'

@dataclass
class Task:
    title: str
    id: UUID = field(default_factory=uuid4)
    status: TaskStatus = TaskStatus.TODO
