# pyramid_task_scheduler

[![Build Status](http://git/api/badges/PLANT/pyramid_task_scheduler/status.svg)](http://git/PLANT/pyramid_task_scheduler)
coming soon

## Install

install packages
`pip install pyramid-task-scheduler`

or require in `setup.py`

add the follwing line to your `Configuratior` section of your pyramid application:
e.g
```python
    config = Configurator(settings=settings)
    config.include('pyramid_task_scheduler')  # Add this Line
```
## Modes

### json crontab

add the following two lines to your .ini file

```{ .ini }
pyramid_task_scheduler_mode = json
pyramid_task_scheduler_path = path_to/crontab.json
```

single cron crontab example:

```json
{
	"cron": [
		{
			"name": "first_cron",
			"import_script": "import_script",
			"exec_func": "function_to_execute",
			"crontab_time": "0 * * * *"
		}
	]
}
```

multiple crons crontab example:

```json
{
    "cron": [
        {
            "name": "first_cron",
            "import_script": "import_script",
            "exec_func": "function_to_execute",
            "crontab_time": "0 * * * *"
        },
        {
            "name": "second_cron",
            "import_script": "import_script",
            "exec_func": "function_to_execute",
            "crontab_time": "0 * * * *"
        }
    ]   
}
```

# NOTE

this package is alpha experimental. It is recommened to NOT use it for productional environments.
