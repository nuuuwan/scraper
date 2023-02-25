from scraper import Spider

if __name__ == '__main__':
    spider = Spider(
        'https://www.sltda.gov.lk/en/monthly-tourist-arrivals-reports-2023'
    )
    table_paths = spider.spider_tables(limit=200)
    for table_path in table_paths:
        print(table_path)
