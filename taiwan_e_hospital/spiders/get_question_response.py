from taiwan_e_hospital.items import TaiwanEHospitalItem

from bs4 import BeautifulSoup

import scrapy
import re


class EHospitalCrawler(scrapy.Spider):
    name = 'taiwan_e_hospital'

    # 設定爬取的網址，範圍是 1 到 212715 (2024/10/31 前有問有答的所有資料)
    start_urls = [f'https://sp1.hso.mohw.gov.tw/doctor/All/ShowDetail.php?q_no={number}' for number in range(1, 212716)]
    
    def parse(self, response):
        qa_item = TaiwanEHospitalItem()  # 初始化物件來儲存抓取的資料

        soup = BeautifulSoup(response.body, 'lxml')

        # 抓取發問者的基本資訊及提問內容並解析
        questioner_info_div = soup.select_one('div:nth-of-type(2) > div:nth-of-type(1) > div:nth-of-type(2) > div')
        questioner_question_div = soup.find_all(class_='msg')
        if questioner_info_div is not None and len(questioner_question_div) > 0:
            questioner_info = questioner_info_div.text.strip().replace('\xa0', ' ')
            questioner_question = questioner_question_div[0].text.strip()
        else:
            self.logger.error("無法找到問題者信息或問題文本")
            return

        # 抓取醫生的基本資訊及回答內容並解析
        doctor_info_div = soup.select_one('div:nth-of-type(3) > div:nth-of-type(1) > div:nth-of-type(2) > div')
        if doctor_info_div is not None and len(questioner_question_div) > 1:
            doctor_info = doctor_info_div.text.strip().replace('\xa0', ' ')
            doctor_answer = questioner_question_div[1].text.strip()
        else:
            self.logger.error("無法找到醫生信息或回答文本")
            return

        # 使用正規表達式來解析問題者及醫生的資訊
        questioner_pattern = re.compile(r'([^／]+)／([^／]+)／\(([^)]+)\),(\d{4}/\d{2}/\d{2}) 提問：')
        doctor_pattern = re.compile(r'(?:(.+?)／)?([^／]+)／([^,]+), (\d{4}/\d{2}/\d{2}) 回覆：')

        # 抓取問題的 ID
        question_id_pattern = re.compile(r'#(\d+)')
        question_id = soup.find(class_='w3-bar')

        # 檢查並取得符合的編號、提問者及醫生資訊
        question_id_match = question_id_pattern.search(question_id.get_text()) if question_id else None
        questioner_info_matches = questioner_pattern.match(questioner_info)
        doctor_info_matches = doctor_pattern.match(doctor_info)

        # 驗證資訊並存儲至 qa_item 中
        if question_id_match and questioner_info_matches and doctor_info_matches:
            qa_item['question_id'] = str(question_id_match.group(1))
            
            qa_item['questioner_name'] = questioner_info_matches.group(1)
            qa_item['questioner_gender'] = questioner_info_matches.group(2)
            qa_item['questioner_age_range'] = questioner_info_matches.group(3)
            qa_item['question_date'] = questioner_info_matches.group(4)
            qa_item['question_text'] = str(questioner_question)

            qa_item['doctor_hospital'] = doctor_info_matches.group(1) if doctor_info_matches.group(1) else ""
            qa_item['doctor_department'] = doctor_info_matches.group(2)
            qa_item['doctor_name'] = doctor_info_matches.group(3)
            qa_item['reply_date'] = doctor_info_matches.group(4)
            qa_item['answer_text'] = str(doctor_answer)

            # 將抓取的資料 yield 出去以進行後續處理
            yield qa_item
