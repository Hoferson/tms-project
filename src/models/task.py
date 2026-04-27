from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4

class TaskStatus(Enum):
    """Перелік можливих статусів завдання."""
    TODO = 'todo'
    IN_PROGRESS = 'in_progress'
    IN_REVIEW = 'in_review'
    DONE = 'done'
    BLOCKED = 'blocked'

# Словник, що визначає логіку переходів між статусами
ALLOWED_TRANSITIONS = {
    TaskStatus.TODO: [TaskStatus.IN_PROGRESS],
    TaskStatus.IN_PROGRESS: [TaskStatus.IN_REVIEW, TaskStatus.BLOCKED],
    TaskStatus.IN_REVIEW: [TaskStatus.DONE, TaskStatus.IN_PROGRESS],
    TaskStatus.BLOCKED: [TaskStatus.IN_PROGRESS],
    TaskStatus.DONE: []
}

@dataclass
class Task:
    """Модель завдання системи керування задачами (TMS)."""
    title: str
    description: str = ""
    id: UUID = field(default_factory=uuid4)
    status: TaskStatus = TaskStatus.TODO
    assignee_id: UUID | None = None
    created_at: datetime = field(default_factory=datetime.utcnow)

    def change_status(self, new_status: TaskStatus) -> None:
        """
        Змінює статус завдання з перевіркою на допустимість переходу.
        Включає перевірку на None (Hotfix).
        """
        # Перевірка на None (реалізовано в межах Hotfix)
        if new_status is None:
            raise ValueError('Status cannot be None')

        # Перевірка, чи дозволений перехід із поточного стану до нового
        if new_status not in ALLOWED_TRANSITIONS[self.status]:
            raise ValueError(
                f'Cannot transition from {self.status} to {new_status}'
            )

        self.status = new_status