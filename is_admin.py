import ctypes, sys
import change_mac_csdn
def is_admin():
    res = 0
    try:
        res = ctypes.windll.shell32.IsUserAnAdmin()
    except:
        # Re-run the program with admin rights
        print("shit")
    finally:
        print("cao")
        print(res)
        if res == 0 :
            print("1")
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)

            print("2")
            sys.exit(0)
        return res
if __name__ == '__main__':
    print(is_admin())

