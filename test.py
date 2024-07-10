def test(mesage:str,*format):
    print(format)
    return mesage.format(*format)

print(test("hello"))