import logging
from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin


logger = logging.getLogger(name="view_performance")

class LogViewExecutionTimeMiddleware(MiddlewareMixin):
    """Calculate the time needed to execute a view and log it."""

    def process_request(self, request):
        request.start_time = timezone.now()

    def process_response(self, request, response):
        runtime = timezone.now() - request.start_time
        http_method = request.method
        url = request.get_full_path()
        host_port = request.get_host()
        status_code = response.status_code

        msg = f"Execution time: {runtime} >> {http_method} -> {status_code} | {host_port}{url}"

        # Log execution time with severity depending on runtime
        if runtime < timezone.timedelta(seconds=0.1):
            logger.info(msg)
        elif runtime < timezone.timedelta(seconds=1):
            logger.warning(msg)
        else:
            logger.critical(msg)

        return response