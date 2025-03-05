# What we expect?
The solution must fulfil the following criteria:
- Unit test coverage
- Clean code
- README with instructions on how to run the code

There’s no requirement to build a full-fledged UI, and the solution must not require any kind of database to run.
A console application is sufficient.
Submission can be in any programming language that they are comfortable with.

Submissions without any form of automated testing will not be considered.

# Problem (Bank Account)

You're designing a simple banking system that handles operations on bank accounts. The system should be capable of the following features:
- input banking transactions
- calculate interest
- printing account statement

All the example below assumes console input/output is used. 


When launching the application, it prompts user for actions:
```
Welcome to AwesomeGIC Bank! What would you like to do?
[T] Input transactions 
[I] Define interest rules
[P] Print statement
[Q] Quit
>
```

User should be able to enter `T` or `t` to select input transactions menu. Similarly, initial character is used for other options.

## Input transactions
Upon selecting Input transactions option, application prompts user for transaction details.
```
Please enter transaction details in <Date> <Account> <Type> <Amount> format 
(or enter blank to go back to main menu):
>
```

User is then able to enter something like the following:
```
20230626 AC001 W 100.00
```
The system should automatically create the account when the first transaction for the account is created.

Some constraints to note:
* Date should be in YYYYMMdd format
* Account is a string, free format
* Type is D for deposit, W for withdrawal, case insensitive
* Amount must be greater than zero, decimals are allowed up to 2 decimal places
* An account's balance should not be less than 0. Therefore, the first transaction on an account should not be a withdrawal, and any transactions thereafter should not make balance go below 0
* Each transaction should be given a unique id in YYYMMdd-xx format, where xx is a running number (see example below)

Then system responds by displaying the statement of the account:
(assuming there are already some transactions in the account)
```
Account: AC001
| Date     | Txn Id      | Type | Amount |
| 20230505 | 20230505-01 | D    | 100.00 |
| 20230601 | 20230601-01 | D    | 150.00 |
| 20230626 | 20230626-01 | W    |  20.00 |
| 20230626 | 20230626-02 | W    | 100.00 |

Is there anything else you'd like to do?
[T] Input transactions 
[I] Define interest rules
[P] Print statement
[Q] Quit
>
```

## Define interest rule
Upon selecting Define interest rule option, application prompts user to define interest rules:

```
Please enter interest rules details in <Date> <RuleId> <Rate in %> format 
(or enter blank to go back to main menu):
>
```

User is then able to enter something like the following:
```
20230615 RULE03 2.20
```
Some constraints to note:
* Date should be in YYYYMMdd format
* RuleId is string, free format
* Interest rate should be greater than 0 and less than 100
* If there's any existing rules on the same day, the latest one is kept

Then system responds by listing all interest rules orderd by date:
(assuming there are already RULE01 and RULE02 in the system) 
```
Interest rules:
| Date     | RuleId | Rate (%) |
| 20230101 | RULE01 |     1.95 |
| 20230520 | RULE02 |     1.90 |
| 20230615 | RULE03 |     2.20 |

Is there anything else you'd like to do?
[T] Input transactions 
[I] Define interest rules
[P] Print statement
[Q] Quit
>
```

## Print Statement
Upon selecting Print statement option, application prompts user to select which account to print the statement for:

```
Please enter account and month to generate the statement <Account> <Year><Month>
(or enter blank to go back to main menu):
>
```

When user enters the account
```
AC001 202306
```

System then responds with the following account statement, which shows all the transactions and interest for that month (transaction type for interest is I):
```
Account: AC001
| Date     | Txn Id      | Type | Amount | Balance |
| 20230601 | 20230601-01 | D    | 150.00 |  250.00 |
| 20230626 | 20230626-01 | W    |  20.00 |  230.00 |
| 20230626 | 20230626-02 | W    | 100.00 |  130.00 |
| 20230630 |             | I    |   0.39 |  130.39 |
```

How to apply the interest rule:
* Interest is applied on end of day balance
```
| Period              | Num of days | EOD Balance | Rate Id | Rate | Annualized Interest      |
| 20230601 - 20230614 | 14          | 250         | RULE02  | 1.90 | 250 * 1.90% * 14 = 66.50 |
| 20230615 - 20230625 | 11          | 250         | RULE03  | 2.20 | 250 * 2.20% * 11 = 60.50 |
| 20230626 - 20230630 |  5          | 130         | RULE03  | 2.20 | 130 * 2.20% *  5 = 14.30 |
(this table is provided to help you get an idea how the calculation is done, it should not be displayed in the output)
```
* Therefore total interest is: (66.50 + 60.50 + 14.30) / 365 = 0.3871 => 0.39
* The interest is credited at the last day of the month

## Quit
When user chooses to quit, user enters:
```
q
```

System responds with:
```
Thank you for banking with AwesomeGIC Bank.
Have a nice day!
```