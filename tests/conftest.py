import logging

import pytest

from logger_config import setup_logging


def pytest_configure(config):
    setup_logging(level=logging.INFO)
    worker_id = getattr(config, "workerinput", {}).get("workerid", "master")

    # Create a unique log file for each worker
    log_file = f"test_log_{worker_id}.txt"
    log_file_handler = logging.FileHandler(log_file, mode="w")
    log_file_handler.setFormatter(
        logging.Formatter("[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s")
    )
    logging.getLogger().addHandler(log_file_handler)


logger = logging.getLogger("bdd-tests")


@pytest.fixture(scope="session", autouse=True)
def log_test_start_and_end():
    logger.info("Starting pytest-bdd test session")
    yield
    logger.info("Finished pytest-bdd test session")


@pytest.fixture
def context():
    return {}


@pytest.fixture
def parse_gherkin_table():
    def _parse(table_data):
        """
        Parses a table represented as a list of lists of strings.

        Args:
            table_data (list[list[str]]): The raw table data from pytest-bdd.

        Returns:
            list[dict]: A list of dictionaries, with headers as keys and values from rows.
                       'quantity' fields are converted to integers.
        """
        if not (isinstance(table_data, list) and table_data and all(isinstance(row, list) for row in table_data)):
            return []

        headers = [h.strip() for h in table_data[0]]

        try:
            return [
                {
                    k: int(v.strip()) if k == 'quantity' else v.strip()
                    for k, v in zip(headers, row)
                }
                for row in table_data[1:]
            ]
        except ValueError as e:
            pytest.fail(
                f"Invalid data in table: {str(e)}. "
                f"Ensure 'quantity' values are valid integers."
            )

    return _parse
