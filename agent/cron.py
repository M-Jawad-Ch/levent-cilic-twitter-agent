from django_cron import CronJobBase, Schedule
from django.utils.timezone import now


class MyCronJob(CronJobBase):
    RUN_EVERY_MINS = 60  # every hour

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = "myapp.my_cron_job"  # a unique code for the job

    def do(self):
        print("Running scheduled task at", now())
        # Place your logic here (e.g., sending emails, cleaning up data, etc.)
