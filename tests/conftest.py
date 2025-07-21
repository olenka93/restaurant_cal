import logging
import os

import pytest
import responses

from app.logger_config import setup_logging


def pytest_configure(config):
    logs_dir = "logs/tests"
    os.makedirs(logs_dir, exist_ok=True)
    worker_id = getattr(config, "workerinput", {}).get("workerid", "master")
    setup_logging(
        level=logging.INFO,
        log_to_file=True,
        log_file_path=f"logs/tests/test_log_{worker_id}.log",
        logger_name="bdd-tests",
    )


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
def mock_responses():
    with responses.RequestsMock() as rsps:
        yield rsps


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
        if not (
            isinstance(table_data, list)
            and table_data
            and all(isinstance(row, list) for row in table_data)
        ):
            return []

        headers = [h.strip() for h in table_data[0]]

        try:
            return [
                {
                    k: int(v.strip()) if k == "quantity" else v.strip()
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
