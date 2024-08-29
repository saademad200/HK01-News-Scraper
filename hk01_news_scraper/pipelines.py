import json

class Hk01NewsScraperPipeline:
    def open_spider(self, spider):
        self.file = open('items.json', 'w')
        self.file.write('[\n')

    def close_spider(self, spider):
        self.file.write('\n]')
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + ",\n"
        self.file.write(line)
        return item