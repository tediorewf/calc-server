# calc-server

Сервер для протокола CALC 1.1, представляющий из себя по сути CALC 1.0, но поддерживающий возможность создания глобальных переменных общих для всех клиентов.

## Формат сообщения

               CALC <OPERATION> <OPERAND1> <OPERAND2>

где OPERATION может быть одним из символов +, -, *, /, =

OPERAND1, OPERAND2 могут быть целыми так и вещественными числами

Если OPERATION является =, то OPERAND1 обязан быть правильным названием переменной

## Примеры запросов

### Пример 1
               Request: CALC + 2 3
               Response: OK 5

### Пример 2
               Request: CALC - 5 1
               Response: OK 4

### Пример 3
               Request: CALC / 6 3
               Response: OK 2

### Пример 4
               Request: CALC * 2 3
               Response: OK 6

### Пример 5
               Request: CALC = x 5
               Response: OK 5
