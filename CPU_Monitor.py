
#!/usr/bin/python3.5
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#
# Base_Desktop_Dial_Meter and CPU_Monitor created by Grorco <Grorco.Linux@gmail.com> 2018
# Main trunk at https://github.com/Grorco-Linux/Desktop_Widgets
import Base_Desktop_Dial_Meter as base
import psutil
import sys


class CPU_GUI(base.BaseDial):

    def __init__(self):
        super().__init__(sidelength=100, refreshrate=50, ticklength=10, monitortext='CPU')
        self.cpu_list = []



    def monitor(self):
        try:
            type(self.cpu_list)
        except AttributeError:
            self.cpu_list = []
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