import requests
import json
from allure_commons.types import AttachmentType
import logging
import allure
from allure_commons._allure import step

from tests.conftest import BASE_URL


class DemoWebShopApi:

    @staticmethod
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
            try:
                response_json = result.json()
                allure.attach(
                    body=json.dumps(response_json, indent=4, ensure_ascii=False),
                    name="Response",
                    attachment_type=AttachmentType.JSON,
                    extension="json",
                )
            except ValueError:
                allure.attach(
                    body=result.text,
                    name="Response",
                    attachment_type=AttachmentType.TEXT,
                    extension="txt",
                )
            logging.info(result.request.url)
            logging.info(result.status_code)
            logging.info(
                f'{json.dumps(json.loads(result.text), indent=4, ensure_ascii=False) if result.text else "None"}'
            )
        return result
