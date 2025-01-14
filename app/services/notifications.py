class NotificationsService:
    @staticmethod
    def send_notification(total_scraped_products: str, updated_products: str) -> str:
        print("Total Scraped Products - ", total_scraped_products)
        print("Updated Products - ", updated_products)