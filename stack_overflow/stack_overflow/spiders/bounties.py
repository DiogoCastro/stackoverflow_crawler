import scrapy
from ..items import StackOverflowItem


class BountiesSpider(scrapy.Spider):
    name = 'bounties'
    start_urls = ['http://www.stackoverflow.com/questions?tab=Bounties/']

    user_details = {'name': '', 'reputation_score': '', 'badges': ''}
    user_info = {
        'action_time': '',
        'gravatar': '',
        'user_details': user_details,
    }

    def parse(self, response):
        items = StackOverflowItem()

        all_questions = response.xpath('//*[@class="question-summary"]')

        for question in all_questions:
            bounty_indicator = question.css(
                '.bounty-indicator::text',
            ).extract_first()
            question_text = question.css(
                '.summary h3 a.question-hyperlink::text'
            ).extract_first()
            question_hyperlink = question.css(
                '.summary h3 a.question-hyperlink::attr(href)'
            ).get()
            excerpt = question.css('.excerpt::text').extract_first()
            tags = question.css('.post-tag::text').extract()

            # USER INFO
            action_time = question.css(
                'div.started .user-info .user-action-time span.relativetime::text'
            ).extract_first()
            gravatar = question.css(
                'div.started .user-info .user-gravatar32 a div.gravatar-wrapper-32 img::attr(src)'
            ).extract_first()

            # USER DETAILS
            user_name = question.css(
                'div.user-details a::text',
            ).extract_first()
            reputation_score = question.css(
                'div.-flair span.reputation-score::text',
            ).extract_first()
            badges = question.css(
                'div.-flair span span.badgecount::text'
            ).extract_first()

            (
                self.user_details['name'],
                self.user_details['reputation_score'],
                self.user_details['badges'],
            ) = (user_name, reputation_score, badges or '0')

            (
                self.user_info['action_time'],
                self.user_info['gravatar'],
                self.user_info['user_details'],
            ) = (action_time, gravatar, self.user_details)

            items['bounty_indicator'] = bounty_indicator
            items['question'] = question_text
            items['question_hyperlink'] = question_hyperlink
            items['excerpt'] = excerpt
            items['tags'] = tags
            items['user_info'] = self.user_info

            yield items
