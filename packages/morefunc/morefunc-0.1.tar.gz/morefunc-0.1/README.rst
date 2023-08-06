usage
=====

run more function at same time!

install
===========
``pip install morefunc``

how to use
===============

.. code:: python

    from morefunc import moreFunc

    def func1():
        print("func1!")

    def func2(a):
        print("func2 says:"+a)

    def func3(a,b):
        print("func3 says:"+a+"and b^2 is"+str(b*b))

    moreFunc(func1=(), func2=("Hello,World!"), func3=("Hello,python!",3))
