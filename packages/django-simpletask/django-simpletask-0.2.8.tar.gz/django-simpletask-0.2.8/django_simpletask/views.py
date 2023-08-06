
import logging

import bizerror
from fastutils import sysutils
from fastutils import randomutils

from django.urls import path
from django.utils import timezone
from django.db.models import Q
from django.conf import settings

from django_apiview.views import apiview
from django_db_lock.client import DjangoDbLock
from django_db_lock.client import get_default_lock_service

logger = logging.getLogger(__name__)

class SimpleTaskViews(object):
    def __init__(self, model, aclkey=None, lock_service=None):
        app_label = model._meta.app_label
        model_name = model._meta.model_name
        self.model = model
        self.worker_name = sysutils.get_worker_id("{0}:{1}".format(app_label, model_name))
        self.lock_service = lock_service or get_default_lock_service()
        self.aclkey = aclkey or getattr(settings, "DJANGO_SIMPLETASK_ACLKEY", None)

    def get_urls(self):
        return [
            path("getReadyTasks", self.get_ready_tasks_view()),
            path("doTask", self.do_task_view()),
            path("getTaskInfo", self.get_task_info_view()),
            path("reportSuccess", self.report_success_view()),
            path("reportError", self.report_error_view()),
        ]

    def get_ready_tasks_view(self):
        @apiview
        def get_ready_tasks(aclkey:str, executorName:str, batchSize:int=5, channel=None):
            if not self.aclkey:
                raise bizerror.MissingConfigItem(item="DJANGO_SIMPLETASK_ACLKEY")
            if aclkey != self.aclkey:
                raise bizerror.AppAuthFailed()
            # get ready tasks
            app_label = self.model._meta.app_label
            model_name = self.model._meta.model_name
            lock_name = self.model.GET_READY_TASKS_LOCK_NAME_TEMPLATE.format(app_label=app_label, model_name=model_name)
            timeout = self.model.GET_READY_TASKS_LOCK_TIMEOUT
            with DjangoDbLock(self.lock_service, lock_name, (randomutils.uuid4()), timeout) as locked:
                if not locked:
                    raise RuntimeError("get lock failed...")
                tasks = []
                queryset = self.get_ready_tasks_queryset(channel)
                for task in queryset[:batchSize]:
                    task.start(executorName, save=True)
                    tasks.append(task)
                    logger.debug("task {} have been fetched and will be handled soon...".format(task))
                return tasks
        return get_ready_tasks

    def get_ready_tasks_queryset(self, channel=None):
        now = timezone.now()
        queryset = self.model.objects
        queryset = queryset.filter(status=self.model.READY)
        queryset = queryset.filter(ready_time__lte=now)
        queryset = queryset.filter(Q(expire_time=None) | Q(expire_time__gte=now))
        queryset = queryset.order_by("mod_time")

        prefetch_related = getattr(self.model, "prefetch_related", None)
        if prefetch_related:
            queryset = queryset.prefetch_related(*prefetch_related)

        channel_field = getattr(self.model, "channel_field", None)
        if channel_field and channel:
            queryset = queryset.filter(**{channel_field: channel})

        return queryset

    def do_task_view(self):
        @apiview
        def do_task(aclkey:str, taskId:int, executorName:str):
            if not self.aclkey:
                raise bizerror.MissingConfigItem(item="DJANGO_SIMPLETASK_ACLKEY")
            if aclkey != self.aclkey:
                raise bizerror.AppAuthFailed()
            task = self.model.objects.get(pk=taskId)
            return task.do_task(executorName)
        return do_task

    def get_task_info_view(self):
        @apiview
        def get_task_info(aclkey:str, taskId:int):
            if not self.aclkey:
                raise bizerror.MissingConfigItem(item="DJANGO_SIMPLETASK_ACLKEY")
            if aclkey != self.aclkey:
                raise bizerror.AppAuthFailed()
            task = self.model.objects.get(pk=taskId)
            return self.get_task_info(task)
        return get_task_info

    def report_success_view(self):
        @apiview
        def report_success(aclkey:str, taskId:int, worker, result_message):
            if not self.aclkey:
                raise bizerror.MissingConfigItem(item="DJANGO_SIMPLETASK_ACLKEY")
            if aclkey != self.aclkey:
                raise bizerror.AppAuthFailed()
            task = self.model.objects.get(pk=taskId)
            task.report_success(worker, result_message, save=True)
            return True
        return report_success

    def report_error_view(self):
        @apiview
        def report_error(aclkey:str, taskId:int, worker, error_code, error_message):
            if not self.aclkey:
                raise bizerror.MissingConfigItem(item="DJANGO_SIMPLETASK_ACLKEY")
            if aclkey != self.aclkey:
                raise bizerror.AppAuthFailed()
            task = self.model.objects.get(pk=taskId)
            task.report_error(worker, error_code, error_message, save=True)
            return True
        return report_error
    
    def get_task_info(self, task):
        return task.get_task_info()
