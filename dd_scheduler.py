import threading
import time
import schedule


class DailyDigestScheduler(threading.Thread):

    def __init__(self):
        super().__init__()
        self.__stop_running = threading.Event()

    # Schedule a task to repeat at the same time every day.

    def schedule_daily(self, hour, minute, job):
        schedule.clear()  # clear any existing scheduled tasks
        schedule.every().day.at(f"{hour:02d}:{minute:02d}").do(job)

    # Start the scheduler as a background thread.

    def run(self):
        self.__stop_running.clear()
        while not self.__stop_running.is_set():
            schedule.run_pending()
            time.sleep(1)

    # Stop the scheduler thread.

    def stop(self):
        self.__stop_running.set()


if __name__ == "__main__":
    # test DailyDigestScheduler
    import dd_email

    email = dd_email.DailyDigestEmail()

    scheduler = DailyDigestScheduler()
    scheduler.start()

    hour = time.localtime().tm_hour
    minute = time.localtime().tm_min + 1  # schedule for next minute
    print(f"Scheduling test email for {hour:02d}:{minute:02d}")
    scheduler.schedule_daily(hour, minute, email.send_email)

    time.sleep(60)  # keep program alive long enough to ensure send
    scheduler.stop()
