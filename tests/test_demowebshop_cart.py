import requests
import json
from allure_commons.types import AttachmentType
from selene import browser, have
import logging
import allure
from allure_commons._allure import step


BASE_URL = "https://demowebshop.tricentis.com"
LOGIN = "dude@mail.ru"
PASSWORD = "qwe123"


def api_request(endpoint, method, data=None, params=None, allow_redirects=None):
    with step("API Request"):

        result = requests.request(
            method,
            url=BASE_URL + endpoint,
            data=data,
            params=params,
            allow_redirects=allow_redirects,
        )
        allure.attach(
            body=json.dumps(result.text, indent=4, ensure_ascii=True),
            name="Response",
            attachment_type=AttachmentType.JSON,
            extension="json",
        )
        allure.attach(
            body=str(result.cookies),
            name="Cookies",
            attachment_type=AttachmentType.TEXT,
            extension="text",
        )
        allure.attach(
            body=f"URL: {result.request.url}\nMethod: {result.request.method}\nBody: {result.request.body}",
            name="Request Details",
            attachment_type=AttachmentType.TEXT,
            extension="txt",
        )
        logging.info(result.request.url)
        logging.info(result.status_code)
        logging.info(result.text)
    return result


def test_adding_goods_to_the_cart():

    with step("Авторизация через API"):
        url = "/login"

        resultLogin = api_request(
            url,
            method="POST",
            data={"Email": LOGIN, "Password": PASSWORD, "RememberMe": False},
            allow_redirects=False,
        )

        # resultLogin = requests.post(
        #                        url=BASE_URL + url,
        #                        data={"Email": LOGIN, "Password": PASSWORD, "RememberMe": False},
        #                        allow_redirects=False)
        # allure.attach(body=json.dumps(resultLogin.text, indent=4, ensure_ascii=True), name="Response",
        #               attachment_type=AttachmentType.JSON, extension="json")
        # allure.attach(body=str(resultLogin.cookies), name="Cookies", attachment_type=AttachmentType.TEXT, extension="text")
        # allure.attach(
        #     body=f"URL: {resultLogin.request.url}\nMethod: {resultLogin.request.method}\nBody: {resultLogin.request.body}",
        #     name="Request Details",
        #     attachment_type=AttachmentType.TEXT,
        #     extension="txt"
        # )

    with step("Получение куки через API"):
        cookie = resultLogin.cookies.get("Nop.customer")
        print(cookie)

    with step("Добавление товара в корзину через API"):
        requests.post(
            url=BASE_URL + "/addproducttocart/catalog/31/1/1",
            cookies={"Nop.customer": cookie},
            allow_redirects=False,
        )

    with step("Переход в корзину с помощью куки полученных через API"):
        browser.open(BASE_URL)
        browser.driver.add_cookie({"name": "Nop.customer", "value": cookie})
        browser.open(BASE_URL + "/cart")

    with step("Проверка добавленного товара в корзине через WEB"):
        browser.element(".product-name").should(have.text("14.1-inch Laptop"))
        browser.element(".product-price.order-total").should(have.text("1590.00"))
