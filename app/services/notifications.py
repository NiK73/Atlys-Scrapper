class NotificationsService:
    """
    This class provides a method to send notifications about the results of the 
    scraping process, such as the total number of products scraped and the number 
    of products that were updated.
    """
    @staticmethod
    def send_notification(total_scraped_products: str, updated_products: str) -> str:
        print("Total Scraped Products - ", total_scraped_products)
        print("Updated Products - ", updated_products)