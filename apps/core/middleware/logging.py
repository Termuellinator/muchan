from django.conf import settings
from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin

from apps.core.logging import Logging


logging = Logging(str(settings.BASE_DIR / "logs" / "view_runtime_logs.txt"))


class LogViewExecutionTimeMiddleware(MiddlewareMixin):
    """Calculate the time needed to execute a view and log it."""

    def process_request(self, request):
        request.start_time = timezone.now()

    def process_response(self, request, response):
        runtime = timezone.now() - request.start_time
        http_method = request.method
        url = request.get_full_path()
        host_port = request.get_host()

        msg = f"Execution time: {runtime} >> {http_method} | {host_port}{url}"

        # Log execution time with severity depending on runtime
        if runtime < timezone.timedelta(seconds=0.1):
            logging.info(msg)
        elif runtime < timezone.timedelta(seconds=1):
            logging.warning(msg)
        else:
            logging.critical(msg)

        return response


class LogRequestAndResponseMiddleware(MiddlewareMixin):
    """Log the http method, address, content and UA of requests and responses."""

    def process_request(self, request):
        http_method = request.method
        url = request.get_full_path()
        host_port = request.get_host()
        content = request.headers["Content-Type"]
        user_agent = request.headers["User-Agent"]
        pre_msg = f"{http_method} | {host_port}{url} | {content} | {user_agent}"

        logging.info(pre_msg)

    def process_response(self, request, response):
        status_code = response.status_code
        is_closed = response.closed
        reason_phrase = response.reason_phrase
        post_msg = f"Status code: {status_code} | closed: {is_closed} | reason phrase: {reason_phrase}"
        logging.info(post_msg)

        return response
