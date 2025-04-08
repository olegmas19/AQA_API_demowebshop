import requests
import json
from allure_commons.types import AttachmentType
import logging
import allure
from allure_commons._allure import step
from tests.conftest import BASE_URL


class DemoWebShopApi:
    def api_request(
        endpoint, method, data=None, params=None, allow_redirects=None, cookies=None
    ):
        with step("API Request"):

            result = requests.request(
                method,
                url=BASE_URL + endpoint,
                data=data,
                params=params,
                allow_redirects=allow_redirects,
                cookies=cookies,
            )
            allure.attach(
                body=f"URL: {result.request.url}\nMethod: {result.request.method}\nBody: {result.request.body}",
                name="Request",
                attachment_type=AttachmentType.TEXT,
                extension="txt",
            )
            allure.attach(
                body=str(result.cookies),
                name="Cookies",
                attachment_type=AttachmentType.TEXT,
                extension="text",
            )
            allure.attach(
                body=json.dumps(result.text, indent=4, ensure_ascii=True),
                name="Response",
                attachment_type=AttachmentType.JSON,
                extension="json",
            )
            logging.info(result.request.url)
            logging.info(result.status_code)
            logging.info(result.text)
        return result
