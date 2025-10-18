from django.db import models
from django.core.validators import MinLengthValidator

class Task(models.Model):
    title = models.CharField(
        'título',
        max_length=120,
        validators=[MinLengthValidator(3, 'Título muito curto.')]
    )
    done = models.BooleanField('concluída', default=False)
    created_at = models.DateTimeField(
        'criada em',
        auto_now_add=True
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'tarefa'
        verbose_name_plural = 'tarefas'

    def __str__(self) -> str:
        status = '✔' if self.done else '✗'
        return f'[{status}] {self.title}'

    def mark_done(self) -> None:
        """Regra de negócio: marca como feita apenas se ainda não estiver."""
        if not self.done:
            self.done = True
            self.save(update_fields=['done'])
