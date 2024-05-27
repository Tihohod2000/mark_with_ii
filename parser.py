from yandex_reviews_parser.utils import YandexParser
# id_ya = "197064256254"#ID Компании Yandex
# parser = YandexParser(id_ya)
# #reviews
# #company
# company = parser.parse(type_parse='reviews') #Получаем список отзывов
# print(company)


def parse_company_reviews(company_id):
    parser = YandexParser(company_id)
    company_reviews = parser.parse(type_parse='reviews')
    return company_reviews