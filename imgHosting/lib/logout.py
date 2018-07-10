import datetime
from colorama import Fore

class LogOutPut(object):
    
    def checkstring(func):
        def wrappers(self, strings=''):
            if isinstance(strings, (int, str, float, bool, list, dict, tuple, set)):
                print(Fore.GREEN, "[time]:"+datetime.datetime.now().strftime("%Y--%m--%d %H:%M:%S"))
                return func(self, strings)
            else:
                print(Fore.RED, "[Error]:"+"检查输入参数，确保其为字符串或数字。")
                return
            
        return wrappers

    @checkstring
    def success(self, strings):
        print(Fore.GREEN, "[Succ]:", end='')
        print(Fore.GREEN, strings)
    @checkstring
    def error(self, strings):
        print(Fore.RED, "[Error]:", end='')
        print(Fore.RED, strings)
    @checkstring
    def warning(self, strings):
        print(Fore.YELLOW, "[Warning]:", end='')
        print(Fore.YELLOW, strings)
    @checkstring
    def info(self, strings):
        print("[Info]:", end='')
        print("[Info]:"+strings)

def test():
    a = LogOutPut()
    a.success('123')

if __name__ == '__main__':
    test()