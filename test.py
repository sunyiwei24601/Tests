name='lzl'

def global_test():
    name="Eric"
    def sub_test():
        global name
        name="Snor"
        print(name)
    sub_test()
    print(name)

global_test()
print(name)
