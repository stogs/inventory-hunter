from scraper.common import ScrapeResult, Scraper, ScraperFactory


class UnifiScrapeResult(ScrapeResult):
    def parse(self):
        alert_subject = 'In Stock'
        alert_content = ''

        # get name of product
        tag = self.soup.body.find('div', class_='comProduct__title--wrapper')
        if tag:
            alert_content += tag.text.strip() + '\n'
        else:
            self.logger.warning(f'missing title: {self.url}')

        # get listed price
        tag = self.soup.body.find('div', class_='comProduct__price add16right')
        price_str = self.set_price(tag)
        if price_str:
            alert_subject = f'In Stock for {price_str}'
        else:
            self.logger.warning(f'missing price: {self.url}')

        # check for in-stock icon
        tag = self.soup.find('span', class_='comProductTile__inStock add8right')
        if tag:
            self.alert_subject = alert_subject
            self.alert_content = f'{alert_content.strip()}\n{self.url}'


@ScraperFactory.register
class UnifiScraper(Scraper):
    @staticmethod
    def get_domain():
        return 'ui'

    @staticmethod
    def get_driver_type():
        return 'requests'

    @staticmethod
    def get_result_type():
        return UnifiScrapeResult