import queue
from threading import Lock

request_queue = queue.Queue()
active_tasks = False
task_lock = Lock()

# A list to mirror request_queue items for inspection
queue_inspector = []


def add_to_queue(ix, callback, success_callback):
    task = [ix, callback, success_callback]
    request_queue.put(task)
    queue_inspector.append(task)  # Add task to inspector list
    print('[QUEUE]: task was added to the queue', ix)


def process_queue(app):
    global active_tasks
    with app.app_context():
        while True:
            task = request_queue.get()
            if task in queue_inspector:
                queue_inspector.remove(task)  # Remove from inspector list

            [ix, callback,  success_callback] = task
            with task_lock:
                active_tasks = True

            try:
                print('[QUEUE]: task just started execution', ix)
                callback()
                success_callback()
            finally:
                with task_lock:
                    active_tasks = False
                request_queue.task_done()


def get_last_queued_task_index():
    """Returns the last task in the queue without removing it."""
    if queue_inspector:
        return queue_inspector[-1][0]

    if active_tasks:
        # for now I expect to have only one task in progress
        return 1

    return None
