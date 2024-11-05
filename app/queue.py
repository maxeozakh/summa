import queue
request_queue = queue.Queue()


def add_to_queue(callback):
    print('[QUEUE]: task was added to the queue', request_queue.qsize())
    request_queue.put(callback)


def process_queue(app):
    with app.app_context():
        while True:
            callback = request_queue.get()

            try:
                print('[QUEUE]: task just started execution',
                      request_queue.qsize())
                callback()

            finally:
                print('[QUEUE]: task is DONE')
                request_queue.task_done()
