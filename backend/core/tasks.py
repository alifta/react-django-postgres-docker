from celery import shared_task


@shared_task
def add(x, y):
    return x + y


@shared_task
def hello_task(name):
    print(f"Hello {name}! You have {len(name)} characters in your name.")
