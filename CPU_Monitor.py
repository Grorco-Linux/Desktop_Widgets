import Base_Desktop_Dial_Meter as base
import psutil
import sys

class CPU_GUI(base.BaseDial):
    def __init__(self):
        super().__init__(sidelength=100, refreshrate=50, ticklength=10, monitortext='GPU')
        self.cpu_list = []


    def monitor(self):
        if len(self.cpu_list) < 50:
            self.cpu_list.append(psutil.cpu_percent(0))
        else:
            self.cpu_list.pop(0)
            self.cpu_list.append(psutil.cpu_percent(0))

        self.average = 0
        for i in range(len(self.cpu_list)):
            self.average += self.cpu_list[i]

        self.average = self.average / len(self.cpu_list)

        return int(self.average)


if __name__ == '__main__':
    app = base.QApplication(sys.argv)
    ex = CPU_GUI()
    sys.exit(app.exec_())

