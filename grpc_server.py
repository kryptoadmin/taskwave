import os
import django
import grpc
from concurrent import futures
import time

# Set up Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'taskwave.settings')
django.setup()

from tasks.models import Task as DjangoTask
import tasks_pb2
import tasks_pb2_grpc

class TaskService(tasks_pb2_grpc.TaskServiceServicer):
    def GetTasks(self, request, context):
        try:
            tasks = DjangoTask.objects.all()
        except Exception as e:
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INTERNAL)
            return tasks_pb2.TaskList()
        
        task_list = tasks_pb2.TaskList()
        for task in tasks:
            task_list.tasks.add(
                id=task.id,
                title=task.title,
                description=task.description,
                priority=task.priority,
                status=task.status,
                created_at=task.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                updated_at=task.updated_at.strftime('%Y-%m-%d %H:%M:%S')
            )
        return task_list

    def CreateTask(self, request, context):
        try:
            task = DjangoTask(
                title=request.title,
                description=request.description,
                priority=request.priority,
                status=request.status
            )
            task.save()
        except Exception as e:
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INTERNAL)
            return tasks_pb2.Task()

        return tasks_pb2.Task(
            id=task.id,
            title=task.title,
            description=task.description,
            priority=task.priority,
            status=task.status,
            created_at=task.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            updated_at=task.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    tasks_pb2_grpc.add_TaskServiceServicer_to_server(TaskService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()
