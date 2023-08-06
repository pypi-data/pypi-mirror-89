from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import json

# logging.basicConfig(filename='/tmp/log', level=logging.DEBUG,
#                    format='[%(asctime)s]: %(levelname)s : %(message)s')


def parse_config(config):
    settings = config.get_settings()
    pyramid_task_scheduler_path = settings['pyramid_task_scheduler_path']

    return {'pyramid_task_scheduler_path': pyramid_task_scheduler_path}


def parse_crontab(config):
    path = parse_config(config)['pyramid_task_scheduler_path']
    with open(path) as json_file:
        data = json.load(json_file)
        for cron in data['cron']:
            cronname = cron['name']
            import_script = cron['import_script']
            exec_func = cron['exec_func']
            crontab_time = cron['crontab_time']

            yield {'cronname': cronname, 'import_script': import_script,
                   'exec_func': exec_func, 'crontab_time': crontab_time}


def includeme(config):
    main(config)


def main(config):
    cron_entry = parse_crontab(config)
    scheduler = BackgroundScheduler(daemon=True)
    scheduler.start()
    for cron in cron_entry:
        import importlib
        module = getattr(importlib.import_module(cron['import_script']),
                         cron['exec_func'])
        scheduler.add_job(module,
                          CronTrigger.from_crontab(cron['crontab_time'],
                                                   timezone='UTC'),
                          id=cron['cronname'])

    # for job in scheduler.get_jobs():
    #     print("name: %s, trigger: %s, next run: %s, handler: %s" % (
    #           job.name, job.trigger, job.next_run_time, job.func))

    # jobs = scheduler.print_jobs()
    # print(jobs)

    # try:
    #     # This is here to simulate application activity
    #       (which keeps the main thread alive).
    #     while True:
    #         time.sleep(30)
    #         jobs=scheduler.print_jobs()
    #         print(jobs)
    # except (KeyboardInterrupt, SystemExit):
    #     scheduler.shutdown()


if __name__ == '__main__':
    main()
