import time
import logging
import sys

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
file_handler = logging.StreamHandler()
# formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')
formatter = logging.Formatter('%(asctime)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

class ProgressText:

    def __init__(self, iterable=None, every_percent=10, task_name="unnamed"):
        assert iterable is not None
        assert every_percent > 0 and every_percent < 100
        self.iterable = iterable
        self.every_percent = every_percent
        self.task_name = task_name
        self.now_iter = -1
        self.max_iter = len(iterable)
        self.iterator = None
        self.time_start = None
        self.milestones = [self.max_iter * i * self.every_percent / 100 for i in range(int(100 / every_percent))]
        self.next_milestone_offset = -1

    def __iter__(self):
        self.now_iter = 0
        self.next_milestone_offset = 0
        self.iterator = iter(self.iterable)
        self.time_start = time.time()
        logger.info("Task [{}] starts.".format(self.task_name))
        sys.stdout.write("[Time Elapsed < Time Remain]    [Percentage]\n")
        return self

    def __next__(self):
        if self.now_iter < self.max_iter:
            self.print_progress()
            self.now_iter += 1
            return next(self.iterator)
        else:
            self.print_progress()
            sys.stdout.write("\n")
            sys.stdout.flush()
            logger.info("Task [{}] finished.".format(self.task_name))
            raise StopIteration

    def print_progress(self):
        if self.now_iter >= self.milestones[self.next_milestone_offset]:
            time_elapsed = time.time() - self.time_start
            time_elapsed_str = time.strftime("%H:%M:%S", time.gmtime(time_elapsed))
            if self.now_iter == 0:
                eta = "??:??:??"
            else:
                eta = time.strftime("%H:%M:%S",
                                    time.gmtime(time_elapsed * (self.max_iter - self.now_iter) / self.now_iter))
            now_percent = self.next_milestone_offset * self.every_percent
            if now_percent > 100:
                now_percent = 100
            sys.stdout.write("\r    [{} < {}]       [{}%] ({}/{})"\
                            .format(time_elapsed_str,
                                    eta,
                                    now_percent,
                                    self.now_iter,
                                    self.max_iter))
            sys.stdout.flush()
            self.next_milestone_offset += 1
