import logging
from django.utils.deprecation import MiddlewareMixin


logger = logging.getLogger(name="logging_mw")


class LogRequestAndResponseMiddleware(MiddlewareMixin):
    """Log the http method, address, content and UA of requests and responses."""

    def process_request(self, request):
        http_method = request.method
        url = request.get_full_path()
        host_port = request.get_host()
        content = request.headers["Content-Type"]
        user_agent = request.headers["User-Agent"]
        pre_msg = f"{http_method} | {host_port}{url} | {content} | {user_agent}"

        logger.info(pre_msg)

    def process_response(self, request, response):
        status_code = response.status_code
        is_closed = response.closed
        reason_phrase = response.reason_phrase
        post_msg = f"Status code: {status_code} | closed: {is_closed} | reason phrase: {reason_phrase}"
        logger.info(post_msg)

        return response