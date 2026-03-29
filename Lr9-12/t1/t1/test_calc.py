from calc import Calculator

calculator = Calculator();

def test_add():
    if calculator.makeOperation(calculator._add,1,2) == 3:
        print("Test add(a,b) is OK")
    else:
        print("Test add(a,b) is FAIL")
         
def test_sub():
    if calculator.makeOperation(calculator._sub ,4,2) == 2:
          print("Test sub(a,b) is OK")
    else:
        print("Test sub(a,b) is FAIL")

def test_mul():
    if calculator.makeOperation(calculator._mul,2,5) == 10:
          print("Test mul(a,b) is OK")
    else:
        print("Test mul(a,b) is FAIL")

def test_div():
    if calculator.makeOperation(calculator._div,8,4) == 2:
          print("Test div(a,b) is OK")
    else:
        print("Test div(a,b) is FAIL")



test_add()
test_sub()
test_mul()
test_div()