Export:
Working
1.Enter first view (criteria view)
    1.1.Import json
2.Window appear with success message

Result:
State was changed to updated value at:
Criteria view
Solution view
Calculation view

Import = success

----------------------------------------------------

Not Working
1.Enter criteria view
    1.1.Add third row
2.Enter calculation view
    2.1.Third criteria row was added
3.Enter criteria view
    3.1.Delete row
4.Enter calculation view
    4.1.Third criteria row was removed but space remain
5.Enter solution view
    5.1.Add third row
6.Enter calculation view
    6.1.Third solution row was added
    6.2.Space from deleted third criteria row was removed
7.Enter solution view
    7.1.Delete row
8.Enter calculation view
    8.1.Third solution row was removed
    8.2.Space from deleted third solution row was removed

----------------------------------------------------

Working
1.Enter solution view
    1.1.Add third row
2.Enter calculation view
    2.1.Third solution row was added
3.Enter solution view
    3.1.Delete row
4.Enter calculation view
    4.1.Third solution row was removed
    4.2.Space from deleted third solution row was removed