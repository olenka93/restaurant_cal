Feature: Restaurant checkout system

  Scenario: Group of 4 people orders full meal and gets correct total before 19
    Given the order payload is:
      | item    | quantity |
      | starter | 4        |
      | main    | 4        |
      | drink   | 4        |
    And the order time is "18:00"
    When the order is submitted
    Then the total should be 55.4

  Scenario: Group of 4 people orders full meal and gets correct total
    Given the order payload is:
      | item    | quantity |
      | starter | 4        |
      | main    | 4        |
      | drink   | 4        |
    When the order is submitted
    Then the total should be 58.4

  Scenario: Two people order before 19:00, two more join after 20:00
    Given the order payload is:
      | item    | quantity |
      | starter | 1        |
      | main    | 2        |
      | drink   | 2        |
    And the order time is "18:45"
    When the order is submitted
    Then the total should be 23.3
    When more items are added at "20:00":
      | item  | quantity |
      | main  | 2        |
      | drink | 2        |
    Then the total should be 43.7

  Scenario: A member cancel its order
    Given the order payload is:
      | item    | quantity |
      | starter | 4        |
      | main    | 4        |
      | drink   | 4        |
    And the order time is "19:45"
    When the order is submitted
    Then the total should be 58.4
    When items are canceled:
      | item  | quantity |
      | main  | 2        |
      | drink | 2        |
    Then the total should be 38.0
