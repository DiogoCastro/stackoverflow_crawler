import datetime
import re
import scrapy
from ..items import StackOverflowItem


class BountiesSpider(scrapy.Spider):
    name = 'bounties'
    base_url = 'http://www.stackoverflow.com'
    start_urls = ['http://www.stackoverflow.com/questions?tab=Bounties']

    user_details = {'name': '', 'reputation_score': '', 'badges': ''}
    user_info = {
        'asked_at': '',
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
            asked_at = question.css(
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
                self.user_info['asked_at'],
                self.user_info['gravatar'],
                self.user_info['user_details'],
            ) = (asked_at, gravatar, self.user_details)

            items['crawled_at'] = datetime.datetime.now()
            items['bounty_indicator'] = re.sub(r'[^\w]', '', bounty_indicator)
            items['question'] = question_text
            items['question_hyperlink'] = f'{self.base_url}{question_hyperlink}'
            items['excerpt'] = excerpt.strip()
            items['tags'] = tags
            items['user_info'] = self.user_info

            yield items

        next_page = response.css(
            'div.s-pagination.pager.fl a[rel="next"]::attr(href)',
        ).get()

        if next_page:
            yield response.follow(next_page, callback=self.parse)
