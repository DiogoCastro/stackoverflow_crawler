import scrapy


class StackOverflowItem(scrapy.Item):
    bounty_indicator = scrapy.Field()
    question = scrapy.Field()
    question_hyperlink = scrapy.Field()
    excerpt = scrapy.Field()
    tags = scrapy.Field()
    user_info = scrapy.Field()
