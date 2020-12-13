def test(path):
    with open(path) as file:
        print(file.read(5))
        file.seek(5)
        print(file.read(5))


test("E:\\PJs\\Python\\TestFlask\\upload\\dism.log")