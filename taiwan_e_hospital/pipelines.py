# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import sqlite3


class TaiwanEHospitalPipeline:
    # process_item 之前做的事
    def open_spider(self, spider):
        self.conn = sqlite3.connect('tw_e_hospital.sqlite')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS qanda (
    question_id TEXT NOT NULL,
    questioner_name TEXT NOT NULL,
    questioner_gender TEXT,
    questioner_age_range TEXT,
    question_date TEXT,
    question_text TEXT NOT NULL,
    doctor_hospital TEXT,
    doctor_department TEXT NOT NULL,
    doctor_name TEXT NOT NULL,
    reply_date TEXT,
    answer_text TEXT NOT NULL);''')

    # process_item 做完後做的事
    def close_spider(self, spider):
        self.conn.commit()
        self.conn.close()

    def process_item(self, item, spider):
        col = ','.join(item.keys())
        placeholders = ','.join(len(item) * '?')
        sql = 'INSERT INTO qanda({}) VALUES ({})'

        self.cursor.execute(sql.format(col, placeholders), list(item.values()))
        return item
