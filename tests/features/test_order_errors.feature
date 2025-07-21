Feature: Order submission error handling


  Scenario: Order submission fails when items is not a list
    Given an order payload with non-list items
    When the order invalid is submitted
    Then the response status code should be 400
    And the error message should mention "Items must be a list"
