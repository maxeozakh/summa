import queue
request_queue = queue.Queue()


def add_to_queue(callback, ix, success_callback):
    request_queue.put([callback, ix, success_callback])
    print('[QUEUE]: task was added to the queue', request_queue.qsize())


def process_queue(app):
    with app.app_context():
        while True:
            [callback, ix, success_callback] = request_queue.get()

            try:
                print('[QUEUE]: task just started execution', ix)
                callback()

            finally:
                success_callback()
                request_queue.task_done()


def get_queue_size():
    return request_queue.qsize()
