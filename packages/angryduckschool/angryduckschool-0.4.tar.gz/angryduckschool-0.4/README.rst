นี่คือตัวอย่างโปรแกรมสำหรับการเรียน OOP
=======================================

วิธีติดตั้ง
~~~~~~~~~~~

เปิด CMD / Terminal

.. code:: python

    pip install uncleschool

วิธีเล่น
~~~~~~~~

เปิด IDLE ขึ้นมาแล้วพิมพ์...

.. code:: python

    from angryduckschool import Student, SpecialStudent

    print('========1 Jan========')
    student0 = SpecialStudent('Mark Zuckerberg','Bill Gates')
    student0.AskEXP()
    student0.ShowEXP()
    student1 = Student('Albert')
    print(student1.name)
    student1.Hello()

    print('------------')
    student2 = Student('Steve')
    print(student2.name)
    student2.Hello()
    print('========2 Jan========')
    print('------angryduck: Who want to learn coding?---(give 10 exp)----')
    student1.AddEXP(10)

    print('========3 Jan========')
    student1.name = 'Albert Einstein'
    print('exp of each student')

    print(student1.name, student1.exp)
    print(student2.name, student2.exp)
    print('========4 Jan========')

    for i in range(5):
        student2.Coding()

    student1.ShowEXP()
    student2.ShowEXP()

พัฒนาโดย: Angryduck888