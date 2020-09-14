from celery import shared_task
from celery.decorators import task


@task(name="addition")
def addition(x, y):
    return x + y