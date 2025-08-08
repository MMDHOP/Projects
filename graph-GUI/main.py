import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("final project")
window.setGeometry(200, 200, 800, 330)
window.setFixedSize(800,330)


label1 = QLabel('Input :', parent=window)
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("final project")
window.setGeometry(200, 200, 800, 330)
window.setFixedSize(800,330)


label1 = QLabel('Input :', parent=window)
label1.move(190, 100)
font = QFont("Tahoma", 12)
label1.setFont(font)

box = QWidget(window)
box.setGeometry(250,100,250,200)
box.setStyleSheet("background-color: lightblue")

textbox = QTextEdit(parent=box)
textbox.setGeometry(1,1,250,200)


question_title = QLabel('The least number of stations',parent=window)
question_title.move(250,75)
question_title.resize(400,25)
# question_title.setFont(font)

group_buttons = QGroupBox('Buttons',parent=window)
group_buttons.setGeometry(547,100,200,200)

button1 = QPushButton("Q1", parent=group_buttons)
button1.move(100, 50)

output_box = QWidget(window)
output_box.setGeometry(250, 350, 250, 200)
output_box.setStyleSheet("background-color: lightyellow;")

label2 = QLabel('Output :', parent=window)
label2.move(176, 350)
font = QFont("Tahoma", 12)
label2.setFont(font)

output_text = QTextEdit(parent=output_box)
output_text.setGeometry(1, 1, 250, 200)
output_text.setReadOnly(True)

def on_click_q1():
    question_title.setText('The least number of stations')
    # question_title.show()
button1.clicked.connect(on_click_q1)
button1.setStyleSheet("background-color: green; color: white;")

button2 = QPushButton("Q2", parent=group_buttons)
button2.move(100, 85)
def on_click_q2():
    question_title.setText('The shortest path to destination station')
    # question_title.show()
button2.clicked.connect(on_click_q2)
button2.setStyleSheet("background-color: purple; color: white;")

button_theme = QPushButton('Theme🌗',parent=window)
button_theme.move(120,185)
button_theme.setStyleSheet("background-color: #808000; color: black;")
theme_menu = QMenu()

light_action = QAction("Ligth☀️", window)
def set_light_theme():
    window.setStyleSheet("background-color:  #f2f2f2; color: black;")
    label1.setStyleSheet("background-color: #f2f2f2; color: black;")
    label2.setStyleSheet("background-color: #f2f2f2; color: black;")
    question_title.setStyleSheet("background-color: #f2f2f2; color: black;")
    group_buttons.setStyleSheet("background-color: #f2f2f2; color: black;")

light_action.triggered.connect(set_light_theme)

dark_action = QAction("Dark🌙", parent=window)
def set_dark_theme():
    window.setStyleSheet("background-color: #2c3e50; color: black;")
    label1.setStyleSheet("background-color: #2c3e50; color: white;")
    label2.setStyleSheet("background-color: #2c3e50; color: white;")
    question_title.setStyleSheet("background-color: #2c3e50; color: white;")
    group_buttons.setStyleSheet("background-color: #2c3e50; color: white;")

dark_action.triggered.connect(set_dark_theme)

theme_menu.addAction(light_action)
theme_menu.addAction(dark_action)
button_theme.setMenu(theme_menu)

exit_button = QPushButton('Close',parent=group_buttons)
exit_button.move(1,30)
def close_window():
    QApplication.quit()
exit_button.clicked.connect(close_window)
exit_button.setStyleSheet(("background-color: orange; color: white;"))
    
def check_textbox() :
    if textbox.toPlainText() != '' :
        clear_button.setStyleSheet("background-color: orange; color: white;")
        submit_button.setStyleSheet("background-color: orange; color: white;")
    else :
        clear_button.setStyleSheet("background-color: gray; color: white;")
        submit_button.setStyleSheet("background-color: gray; color: white;")
textbox.textChanged.connect(check_textbox)

clear_button = QPushButton('Clear',parent=group_buttons)
clear_button.setStyleSheet("background-color: gray; color: white;")
clear_button.move(1,90)


def clear_textbox():
    if textbox.toPlainText() != '' :
        textbox.clear()
        output_text.clear()
        textbox.textChanged.connect(check_textbox)
clear_button.clicked.connect(clear_textbox)


reset_button = QPushButton("Reset", parent=group_buttons)
reset_button.move(1, 60)
reset_button.setStyleSheet("background-color: orange; color: white;")
def reset_everything():
    textbox.clear()
    output_text.clear()
    question_title.setText("The least number of stations")
    window.setGeometry(200, 200, 800, 330)
    window.setFixedSize(800, 330)
    set_light_theme()
reset_button.clicked.connect(reset_everything)


submit_button = QPushButton('Submit',parent=group_buttons)
submit_button.setStyleSheet("background-color: gray; color: white;")
submit_button.move(1,120)
def submit_answer():
    if textbox.toPlainText() != '' :
        textbox.textChanged.connect(check_textbox)
        window.setFixedSize(800,570)
    if question_title.text() == "The least number of stations" :
        test = textbox.toPlainText().split('\n')
        ch_test = []
        for i in test :
            ch_test.append(i.strip().split())
        result = []
        try:
            n = int(ch_test[0][0])
            m = int(ch_test[0][1])
            names = ch_test[1:n+1]
            connections = ch_test[n+1:n+m+1]
            origin = ch_test[-1][0]
            dict_of_conn = {}
            # print(connections)
            for i in names :
                dict_of_conn[i[0]] = [0]*n
            # print(dict_of_conn)
            for i in names :
                for j in connections :
                    if i[0] in j :
                        other = j[0] if i[0] != j[0] else j[1]
                        indx = [name[0] for name in names].index(other)
                        indx_i = [name[0] for name in names].index(i[0])
                        dict_of_conn[i[0]][indx] = 1
                        dict_of_conn[other][indx_i] = 1
            # print(dict_of_conn)
            for k ,  v  in dict_of_conn.items() :
                indx = [name[0] for name  in names].index(k)
                if dict_of_conn[origin][indx] == 1 :
                    result.append(f"{k} 1")
                elif k == origin :
                    result.append(f"{k} 0")
                else :
                    def found_des(current, target_index, dict_of, visited=None, depth=0):
                        if visited is None:
                            visited = set()
                        if current in visited:
                            return False
                        visited.add(current)

                        if dict_of[current][target_index] == 1:
                            return depth + 1

                        min_depth = float('inf')
                        for next_station, connected in enumerate(dict_of[current]):
                            if connected == 1:
                                next_name = names[next_station][0]
                                result = found_des(next_name, target_index, dict_of, visited.copy(), depth + 1)
                                if result:
                                    min_depth = min(min_depth, result)

                        return min_depth if min_depth != float('inf') else False

                    func = found_des(origin, indx, dict_of_conn)
                    if func == False :
                        result.append(f"{k} -1")
                    else :
                        result.append(f"{k} {func}")
            # print(dict_of_conn)
        except:
            result.append("Invalid Input Format\n")
        for i in range(len(result)) :
            result[i] = result[i]+'\n'

    else :
        test = textbox.toPlainText().split('\n')
        ch_test = []
        for i in test :
            ch_test.append(i.strip().split())
        result = []
        try:
            n = int(ch_test[0][0])
            m = int(ch_test[0][1])
            names = ch_test[1:n+1]
            connections = ch_test[n+1:n+m+1]
            # print(connections)
            origin = ch_test[n+m+1][0]
            destinantion = ch_test[-1][0]
            dict_of_conn = {}
            for i in names:
                dict_of_conn[i[0]] = [0]*n

            for j in connections:
                a = j[0]
                b = j[1]
                distance = float(j[2])
                indx_a = [name[0] for name in names].index(a)
                indx_b = [name[0] for name in names].index(b)
                dict_of_conn[a][indx_b] = distance
                dict_of_conn[b][indx_a] = distance
            # print(dict_of_conn)
            def found_des(current, target, dict_of, visited=None, total=0, path=None):
                if visited is None:
                    visited = set()
                if path is None:
                    path = []

                if current in visited:
                    return None

                visited.add(current)
                path = path + [current]

                if current == target:
                    return (total, path)

                min_result = None
                for next_station_index, distance in enumerate(dict_of[current]):
                    if distance != 0:
                        next_name = names[next_station_index][0]
                        result_rec = found_des(next_name, target, dict_of, visited.copy(), total + distance, path)
                        if result_rec:
                            if (min_result is None) or (result_rec[0] < min_result[0]):
                                min_result = result_rec

                return min_result

            res = found_des(origin, destinantion, dict_of_conn)
            if res:
                distance, path = res
                result.append(f"{round(distance, 2)}\n")
                result.append(f'{" ".join(path)}\n')
            else:
                result.append("No path found.")

            # for r in result:
            #     print(r)
        except:
            result.append("Invalid Input Format")
            # print(dict_of_conn)

    str_result = ''.join(result)
    output_text.setText(str_result)
submit_button.clicked.connect(submit_answer)

                    
paste_button = QPushButton('Paste TestCase',parent=window)
paste_button.move(335,300)
def paste_testcase():
    if question_title.text() == "The least number of stations" :
        textbox.setText("""4 2
Shiraz
Tehran
Isfahan
Mashhad
Shiraz Tehran
Mashhad Isfahan
Mashhad""")
    else :
        textbox.setText("""5 6
A
B
C
D
E
E C 136.81
D B 12.74
C B 14.63
B A 60.48
A D 45.63
A E 514.74
A
C""")
    submit_answer()
paste_button.clicked.connect(paste_testcase)
paste_button.setStyleSheet("background-color: lightpink; color: black;")


window.show()
sys.exit(app.exec_())
