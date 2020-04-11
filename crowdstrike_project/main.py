from get_breaches import write_breaches_to_file, check_domain_breach, check_user_breach
import schedule
import time
import multiprocessing
from functools import partial


def main():
    """

    Main function that handles updating the breaches and checks for domain/user breachers. 
    Scheduler will call on this function to run daily at midnight.

    """

    API_KEY = "API_KEY"
    DOMAINS = {"000webhost.com", "126.com"}
    USER_EMAIL = "davidppham1996@gmail.com"

    write_breaches_to_file()
    check_domain_breach("breaches.json", DOMAINS)
    check_user_breach(USER_EMAIL, API_KEY)

if __name__ == "__main__":
    main()
    # schedule.every().day.at("00:00").do(main)
    schedule.every(1).minutes.do(main)

    while True:
        schedule.run_pending()
        time.sleep(1)
