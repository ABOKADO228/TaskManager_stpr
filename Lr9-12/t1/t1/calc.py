class Calculator:
    def makeOperation(self, execution_func, *args):
            return execution_func(*args)
 
    def _add(self,a,b):
        return a+b

    def  _sub(self,a,b):
        return a-b

    def  _mul(self,a,b):
        return a*b

    def  _div(self,a,b):
        return a/b 



