# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TaiwanEHospitalItem(scrapy.Item):
    question_id = scrapy.Field()

    # 發問者資訊
    questioner_name = scrapy.Field()
    questioner_gender = scrapy.Field()
    questioner_age_range = scrapy.Field()
    question_date = scrapy.Field()
    question_text = scrapy.Field()
    
    # 醫生資訊
    doctor_hospital = scrapy.Field()
    doctor_department = scrapy.Field()
    doctor_name = scrapy.Field()
    reply_date = scrapy.Field()
    answer_text = scrapy.Field()
