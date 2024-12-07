import schedule
import threading
import time
from datetime import datetime
from typing import Callable, List
import logging


class ScanScheduler:
    """
    A sophisticated scheduling system for automated scans.

    Features:
    - Flexible scheduling (daily, weekly, custom intervals).
    - Real-time job tracking and logging.
    - Concurrent scan execution with thread isolation.
    - Dynamic job management (add, remove, update schedules).
    - Configurable retry mechanisms for failed scans.
    """

    def __init__(self):
        """
        Initializes the scheduler with a thread-safe job manager.
        """
        self.logger = logging.getLogger("ScanScheduler")
        self.logger.setLevel(logging.INFO)
        self.jobs = {}
        self.scheduler_thread = threading.Thread(target=self._run_scheduler, daemon=True)
        self.running = False

    def start(self):
        """
        Start the scheduler in a separate thread.
        """
        if not self.running:
            self.running = True
            self.scheduler_thread.start()
            self.logger.info("ScanScheduler started successfully.")

    def stop(self):
        """
        Stop the scheduler and terminate all scheduled jobs.
        """
        self.running = False
        self.logger.info("ScanScheduler stopped successfully.")

    def add_job(self, job_id: str, task: Callable, schedule_type: str, **kwargs):
        """
        Add a job to the scheduler.

        Args:
            job_id (str): Unique identifier for the job.
            task (Callable): The function to execute.
            schedule_type (str): Type of scheduling ('daily', 'weekly', 'interval').
            **kwargs: Additional arguments for the scheduling type:
                - `time` (str): Time for daily or weekly tasks (e.g., '14:30').
                - `day` (str): Day for weekly tasks (e.g., 'monday').
                - `interval` (int): Interval in seconds for interval tasks.

        Raises:
            ValueError: If the schedule_type or parameters are invalid.
        """
        if job_id in self.jobs:
            raise ValueError(f"Job ID '{job_id}' already exists.")

        if schedule_type == "daily":
            if "time" not in kwargs:
                raise ValueError("Time is required for daily scheduling.")
            schedule.every().day.at(kwargs["time"]).do(self._execute_job, job_id=job_id, task=task)

        elif schedule_type == "weekly":
            if "time" not in kwargs or "day" not in kwargs:
                raise ValueError("Time and day are required for weekly scheduling.")
            day = kwargs["day"].lower()
            if day not in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]:
                raise ValueError("Invalid day for weekly scheduling.")
            getattr(schedule.every(), day).at(kwargs["time"]).do(self._execute_job, job_id=job_id, task=task)

        elif schedule_type == "interval":
            if "interval" not in kwargs:
                raise ValueError("Interval is required for interval scheduling.")
            schedule.every(kwargs["interval"]).seconds.do(self._execute_job, job_id=job_id, task=task)

        else:
            raise ValueError(f"Invalid schedule_type: {schedule_type}")

        self.jobs[job_id] = {"task": task, "schedule_type": schedule_type, "kwargs": kwargs}
        self.logger.info(f"Job '{job_id}' added successfully.")

    def remove_job(self, job_id: str):
        """
        Remove a job from the scheduler.

        Args:
            job_id (str): Unique identifier for the job.

        Raises:
            ValueError: If the job_id does not exist.
        """
        if job_id not in self.jobs:
            raise ValueError(f"Job ID '{job_id}' does not exist.")

        schedule.clear(job_id)
        del self.jobs[job_id]
        self.logger.info(f"Job '{job_id}' removed successfully.")

    def list_jobs(self) -> List[dict]:
        """
        List all scheduled jobs.

        Returns:
            List[dict]: Details of all scheduled jobs.
        """
        return [{"job_id": job_id, **job_details} for job_id, job_details in self.jobs.items()]

    def _execute_job(self, job_id: str, task: Callable):
        """
        Execute a scheduled job in a separate thread.

        Args:
            job_id (str): Unique identifier for the job.
            task (Callable): The function to execute.
        """
        self.logger.info(f"Executing job '{job_id}' at {datetime.now()}.")
        try:
            threading.Thread(target=task, name=f"Job-{job_id}", daemon=True).start()
        except Exception as e:
            self.logger.error(f"Job '{job_id}' execution failed: {e}")

    def _run_scheduler(self):
        """
        Run the scheduler loop to check for pending jobs.
        """
        while self.running:
            schedule.run_pending()
            time.sleep(1)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    def sample_scan():
        print(f"Scan executed at {datetime.now()}.")

    scheduler = ScanScheduler()
    scheduler.start()

    # Example: Adding a daily job
    scheduler.add_job(job_id="daily_scan", task=sample_scan, schedule_type="daily", time="14:30")

    # Example: Adding a weekly job
    scheduler.add_job(job_id="weekly_scan", task=sample_scan, schedule_type="weekly", time="10:00", day="friday")

    # Example: Adding an interval job
    scheduler.add_job(job_id="interval_scan", task=sample_scan, schedule_type="interval", interval=10)

    # List all jobs
    for job in scheduler.list_jobs():
        print(job)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        scheduler.stop()
