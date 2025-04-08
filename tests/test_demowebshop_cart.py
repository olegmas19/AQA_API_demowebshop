from selene import browser, have
from allure_commons._allure import step
from aqa_api_demowebshop.demowebshop_api import DemoWebShopApi
from tests.conftest import BASE_URL

LOGIN = "dude@mail.ru"
PASSWORD = "qwe123"


def test_adding_goods_to_the_cart():
    url = "/addproducttocart/catalog/31/1/1"
    url2 = "/cart"

    with step("Добавление товара в корзину через API"):
        result = DemoWebShopApi.api_request(url, method="POST")

    with step("Получение куки через API"):
        cookie = result.cookies.get("Nop.customer")

    with step("Переход в корзину с помощью куки полученных через API"):
        browser.open(BASE_URL)
        browser.driver.add_cookie({"name": "Nop.customer", "value": cookie})
        browser.open(BASE_URL + url2)

    with step("Проверка добавленного товара в корзине через WEB"):
        browser.element(".product-name").should(have.text("14.1-inch Laptop"))
        browser.element(".product-price.order-total").should(have.text("1590.00"))


def test_increase_quantity_goods_to_the_cart():
    url = "/addproducttocart/catalog/31/1/1"
    url2 = "/cart"

    with step("Добавление товара в корзину через API"):
        result = DemoWebShopApi.api_request(url, method="POST")

    with step("Получение куки через API"):
        cookie = result.cookies.get("Nop.customer")

    with step("Увеличение количества товара в корзине через API"):
        DemoWebShopApi.api_request(url, method="POST", cookies={"Nop.customer": cookie})

    with step("Переход в корзину с помощью куки полученных через API"):
        browser.open(BASE_URL)
        browser.driver.add_cookie({"name": "Nop.customer", "value": cookie})
        browser.open(BASE_URL + url2)

    with step("Проверка общего количества добавленного товара в корзине через WEB"):
        browser.element(".product-name").should(have.text("14.1-inch Laptop"))
        browser.element(".product-price.order-total").should(have.text("3180.00"))


def test_adding_several_goods_to_the_cart():
    url = "/addproducttocart/catalog/31/1/1"
    url2 = "/cart"
    url3 = "/addproducttocart/details/72/1"

    with step("Добавление товара в корзину через API"):
        result = DemoWebShopApi.api_request(url, method="POST")

    with step("Получение куки через API"):
        cookie = result.cookies.get("Nop.customer")

    with step("Добавление другого товара в корзину через API"):
        DemoWebShopApi.api_request(
            url3,
            method="POST",
            data={
                "product_attribute_72_5_18": 3,
                "product_attribute_72_6_19": 54,
                "product_attribute_72_3_20": 57,
                "addtocart_72.EnteredQuantity": 1,
            },
            cookies={"Nop.customer": cookie},
        )

    with step("Переход в корзину с помощью куки полученных через API"):
        browser.open(BASE_URL)
        browser.driver.add_cookie({"name": "Nop.customer", "value": cookie})
        browser.open(BASE_URL + url2)

    with step("Проверка добавленных товаров в корзине через WEB"):
        browser.element(".product-name").should(have.text("14.1-inch Laptop"))
        browser.all(".attributes").should(
            have.texts("Processor: 2X\nRAM: 2 GB\nHDD: 320 GB")
        )
        browser.element(".product-price.order-total").should(have.text("2390.00"))
