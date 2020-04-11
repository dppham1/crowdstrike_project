from flask import Flask, request
import logging
import time


def create_log(directory: str, level: str=logging.INFO) -> None:
    """
    
    Function that sets up the logger, and writes data to the log in the given directory.

    Args:
        directory (str): The directory for where log files should be stored.
        level (str): The logging level to set for the logger.
    
    """

    log_date_time = time.strftime("%Y-%b-%d %H %M")

    formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")

    handler = logging.FileHandler("{}/{}.log".format(directory, log_date_time), mode="w+")
    handler.setFormatter(formatter)

    logger = logging.getLogger()
    logger.setLevel(level)
    logger.addHandler(handler)

    data = request.get_json()
    logger.info("{}\n".format(data))

    logger.removeHandler(handler)

server = Flask(__name__)

@server.route("/logDomainBreach", methods=["POST"])
def log_domain_breach():
    if request.method == "POST":
        create_log("domain_logs")
        return "Successfully logged the domain breach data."
    else:
        return "The logDomainBreach endpoint expected a POST request, but received something else instead.\n"

@server.route("/logUserBreach", methods=["POST"])
def log_user_breach():
    if request.method == "POST":
        create_log("user_logs")
        return "Successfully logged the user breach data."
    else:
        return "The logUserBreach endpoint expected a POST request, but received something else instead.\n"

if __name__ == "__main__":
    server.run(port=5000)