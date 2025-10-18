from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.core.mail import send_mail
from .models import Task
from .forms import TaskForm

def task_list_create(request):
    """GET: lista tarefas; POST: cria tarefa nova."""
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save()

            # notificação simples por e-mail (fica no locmem nos testes)
            send_mail(
                subject='Nova tarefa criada',
                message=f'Você criou: {task.title}',
                from_email='noreply@example.com',
                recipient_list=['admin@example.com'],
                fail_silently=True
            )
            return redirect('tarefas:lista')
    else:
        form = TaskForm()

    tasks = Task.objects.all()
    return render(request, 'tarefas/lista.html', {'form': form, 'tasks': tasks})

@require_POST
def toggle_done(request, pk: int):
    """Alterna o status de uma tarefa via POST e redireciona para a lista."""
    task = get_object_or_404(Task, pk=pk)
    task.done = not task.done
    task.save(update_fields=['done'])
    return redirect('tarefas:lista')
