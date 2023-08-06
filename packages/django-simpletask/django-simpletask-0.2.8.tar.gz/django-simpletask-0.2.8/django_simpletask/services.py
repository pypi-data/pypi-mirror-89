import logging
import json
import time
from urllib import parse as urlparse
import bizerror
from django.http import response

import requests
from fastutils import sysutils
from fastutils import threadutils
from fastutils import threadutils


logger = logging.getLogger(__name__)


class SimpleTaskService(threadutils.SimpleProducerConsumerServerBase):
    default_produce_loop_interval = 1
    default_queue_size = 10

    def __init__(self, server, aclkey, channel=None, task_id_field_name="pk", batch_size=5, api_url_get_ready_tasks=None, api_url_do_task=None, **kwargs):
        self.server = server
        self.aclkey = aclkey
        self.batch_size = batch_size
        self.channel = channel
        self.task_id_field_name = task_id_field_name
        self.executorName = sysutils.get_worker_id("SimpleTaskService")
        self.api_url_get_ready_tasks = api_url_get_ready_tasks or urlparse.urljoin(self.server, "./getReadyTasks")
        self.api_url_do_task = api_url_do_task or urlparse.urljoin(self.server, "./doTask")
        super().__init__(**kwargs)

    def produce(self):
        params = {
            "aclkey": self.aclkey,
            "executorName": self.executorName,
            "batchSize": self.batch_size,
            "channel": self.channel,
            "ts": time.time(),
        }
        logger.info("calling get_ready_tasks api: url={}, params={}".format(self.api_url_get_ready_tasks, params))
        response = requests.get(self.api_url_get_ready_tasks, params)
        logger.info("calling get_ready_tasks api got response: content={}".format(response.content))
        response_package = json.loads(response.content)
        tasks = response_package["result"]
        return tasks

    def consume(self, task):
        params = {
            "taskId": task[self.task_id_field_name],
            "aclkey": self.aclkey,
            "executorName": self.executorName,
            "ts": time.time(),
        }
        logger.info("calling do_task api: url={}, params={}".format(self.api_url_do_task, params))
        response = requests.get(self.api_url_do_task, params)
        logger.info("calling do_task api got response: content={}".format(response.content))
        response_package = json.loads(response.content)
        tasks = response_package["result"]
        return tasks

    @classmethod
    def serve(cls, **kwargs):
        service = cls(**kwargs)
        service.start()
        return service

class SimpleTaskServiceProxy(SimpleTaskService):

    def __init__(self, server, aclkey, api_url_get_task_info=None, api_url_report_success=None, api_url_report_error=None, **kwargs):
        super().__init__(server, aclkey, **kwargs)
        self.api_url_get_task_info = api_url_get_task_info or urlparse.urljoin(self.server, "./getTaskInfo")
        self.api_url_report_success = api_url_report_success or urlparse.urljoin(self.server, "./reportSuccess")
        self.api_url_report_error = api_url_report_error or urlparse.urljoin(self.server, "./reportError")

    def consume(self, task):
        info = self.get_task_info(task)
        try:
            result = self.do_task_main(task, info)
            self.report_success(task, result)
        except Exception as error:
            logger.exception("do_task_main failed")
            error = bizerror.BizError(error)
            self.report_error(task, error.code, error.message)

    def get_task_info(self, task):
        params = {
            "taskId": task[self.task_id_field_name],
            "aclkey": self.aclkey,
            "ts": time.time(),
        }
        logger.info("calling get_task_info api: url={}, params={}".format(self.api_url_get_task_info, params))
        response = requests.get(self.api_url_get_task_info, params)
        logger.info("calling get_task_info api got response: content={}".format(response.content))
        response_package = json.loads(response.content)
        info = response_package["result"]
        return info

    def do_task_main(self, task, info):
        raise NotImplementedError()

    def report_success(self, task, result_message):
        params = {
            "taskId": task[self.task_id_field_name],
            "aclkey": self.aclkey,
        }
        data = {
            "worker": self.executorName,
            "result_message": result_message,
        }
        logger.info("calling report_success api: url={}, params={}, data={}".format(self.api_url_report_success, params, data))
        response = requests.post(self.api_url_report_success, params=params, json=data)
        logger.info("calling report_success api got response: content={}".format(response.content))
        response_package = json.loads(response.content)
        result = response_package["result"]
        return result

    def report_error(self, task, error_code, error_message):
        params = {
            "taskId": task[self.task_id_field_name],
            "aclkey": self.aclkey,
        }
        data = {
            "worker": self.executorName,
            "error_code": error_code,
            "error_message": error_message,
        }
        logger.info("calling report_error api: url={}, params={}, data={}".format(self.api_url_report_error, params, data))
        response = requests.post(self.api_url_report_error, params=params, json=data)
        logger.info("calling report_error api got response: content={}".format(response.content))
        response_package = json.loads(response.content)
        result = response_package["result"]
        return result
