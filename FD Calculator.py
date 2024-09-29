import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QWidget, QGridLayout, QScrollArea, QCheckBox, QComboBox, QSlider
from PyQt5.QtGui import QIcon, QPixmap
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter
import uuid
#from pyqtgraph import PlotWidget, plot
#import pyqtgraph as pg


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Fixed Deposit Calculator")
        self.setGeometry(100, 100, 400, 250)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        window_icon = QIcon("new_icons.png")
        self.setWindowIcon(window_icon)  # Set the window icon

        #self.user_input = ""

        layout = QVBoxLayout()

        self.statuscheck = False
        self.input_layout1 = QHBoxLayout() ##
        self.input_label1 = QLabel("Principal Amount:           ", self)
        self.input_layout1.addWidget(self.input_label1)
        self.input_field1 = QLineEdit(self)
        self.input_layout1.addWidget(self.input_field1)
        layout.addLayout(self.input_layout1)

        self.input_layout2 = QHBoxLayout()
        self.input_label2 = QLabel("Tenure (Months):            ", self)
        self.input_layout2.addWidget(self.input_label2)
        self.input_field2 = QLineEdit(self)
        self.input_layout2.addWidget(self.input_field2)
        layout.addLayout(self.input_layout2)

        self.input_layout3 = QHBoxLayout()
        self.input_label3 = QLabel("Annual Interest Rate (%):   ", self)
        self.input_layout3.addWidget(self.input_label3)
        self.input_field3 = QLineEdit(self)
        self.input_layout3.addWidget(self.input_field3)
        layout.addLayout(self.input_layout3)

        self.checkbox_layout = QHBoxLayout()
        self.checkbox = QCheckBox("Compare Interest Rate", self)
        self.checkbox.stateChanged.connect(self.checkbox_state_changed)
        self.checkbox_layout.addWidget(self.checkbox)
        self.input_label4 = QLabel("Compare Rate (%): ", self)
        self.checkbox_layout.addWidget(self.input_label4)
        self.input_field4 = QLineEdit(self)
        self.input_field4.setEnabled(False)
        self.checkbox_layout.addWidget(self.input_field4)
        layout.addLayout(self.checkbox_layout)

        self.slider_layout = QHBoxLayout()
        self.slidervalue_label = QLabel("FontSize: 5")
        self.slider_layout.addWidget(self.slidervalue_label)
        self.slider = QSlider()
        self.slider.setOrientation(1)  # Set to horizontal orientation
        self.slider.setMinimum(0)       # Set minimum value
        self.slider.setMaximum(15)     # Set maximum value
        self.slider.setValue(5)        # Set initial value
        self.slider.setTickInterval(1) # Set tick interval
        self.slider.setTickPosition(QSlider.TicksBothSides) # Show ticks on both sides
        self.slider.valueChanged.connect(self.selection_changed)
        self.slider_layout.addWidget(self.slider)
        layout.addLayout(self.slider_layout)

        self.button_layout = QHBoxLayout()
        self.button = QPushButton("Calculate !", self)
        self.button.setStyleSheet("background-color: #9caf88; color: white;")
        self.button.clicked.connect(self.process_input)
        self.button_layout.addWidget(self.button)
        layout.addLayout(self.button_layout)

        self.output_label = QLabel("", self)
        layout.addWidget(self.output_label)

        self.image_label = QLabel(self)
        layout.addWidget(self.image_label)

        self.grid_layout = QGridLayout()
        layout.addLayout(self.grid_layout)

        #self.graphWidget = pg.PlotWidget()
        #self.setCentralWidget(self.graphWidget)
        
        self.central_widget.setLayout(layout)

    def clearAll(self):
        #print("Yes!")
        for i in reversed(range(self.scroll_layout.count())):
            layout_item = self.scroll_layout.itemAt(i)
            if layout_item is not None:
                widget = layout_item.widget()
                if widget is not None:
                    widget.deleteLater()

    def selection_changed(self, value):
        self.slidervalue_label.setText(f"FontSize: {value}")
        

    def checkbox_state_changed(self, state):
        if state == 2: #clicked
            self.statuscheck = True
            self.input_field4.setEnabled(True)
        
        else:
            self.statuscheck = False
            self.input_field4.setEnabled(False)

    def plotyy(self,x,y,filename):
        print('GOING2Plot!')
        plt.plot(x, y)
        plt.scatter(x,y)
        print(x,y)
        plt.xlabel('Maturity (Month)')  # naming the x axis 
        plt.ylabel('Maturity Amount')  # naming the y axis
        plt.grid(True)
        numb_fontsize = self.slider.value()
        print (numb_fontsize)
        for idx in range(len(x)):
            plt.text(idx+1, y[idx], round(y[idx],2), ha = 'center', fontsize=numb_fontsize)
            
        
        
        plt.savefig(filename,bbox_inches='tight', dpi=150)
        #self.button.setText("Refresh !")
        print('SAVE!')
        plt.clf()  # Clear the current figure
        plt.close()

    def compare_plotyy(self,x,y,x2,y2,filename):
        plt.plot(x, y)
        plt.scatter(x,y)
        plt.plot(x2, y2)
        plt.scatter(x2,y2)
        plt.xlabel('Maturity (Month)')  # naming the x axis 
        plt.ylabel('Maturity Amount')  # naming the y axis
        plt.grid(True)        
        numb_fontsize = self.slider.value()
        #self.button.setText("Refresh !")
        for idx in range(len(x)):
            plt.text(idx+1, y[idx], round(y[idx],2), ha = 'center', fontsize=numb_fontsize)
            plt.text(idx+1, y2[idx], round(y2[idx],2), ha = 'center', fontsize=numb_fontsize)
            
        
        plt.savefig(filename,bbox_inches='tight', dpi=150)
        plt.clf()  # Clear the current figure
        plt.close()
                
    def fd_cal(self, month, rate, prin_amount):
        month, rate, prin_amount = int(month), float(rate), float(prin_amount)
        filename = "plotdata/" + f"img_{uuid.uuid4()}.png"
        print(month, rate, prin_amount)
        month_idx = []
        money_idx = []
        month_idx = [i for i in range(1,month+1)]
        

        for i in range (month):
            init_rate = (1+(rate/1200))
            init_prin_amount = prin_amount
            init_prin_amount *= (init_rate**(i+1))
            money_idx.append(init_prin_amount)

        
        
        #print( month_idx,  money_idx)
        #self.graphWidget.plot(month_idx, money_idx)
        #plt.bar(month_idx, money_idx)
        #plt.minorticks_off()
        #plt.ylim(min(money_idx)*0.98, max(money_idx)*1.01)
        #plt.yscale('log')
        #plt.ticklabel_format(style='plain')
        #plt.gca().yaxis.set_major_formatter(ScalarFormatter(useMathText=False))    
        #plt.scatter(month_idx, money_idx, marker='o')
        #print(month_idx)
        #print(money_idx)
        
        
        """plt.grid()
        for i in range(len(self.month_idx)):
            plt.text(i+1, money_idx[i], round(money_idx[i],2), ha = 'center', fontsize=7)
            
        plt.xlabel('Maturity (Month)')  # naming the x axis 
        plt.ylabel('Maturity Amount')  # naming the y axis
        #plt.show()
        print("preYes")
        plt.savefig(filename,bbox_inches='tight', dpi=150)
        
        print("Yes!")
        #plt.title('My first graph!') # giving a title to my graph 
        print(filename)
        """
        return init_prin_amount, month_idx, money_idx, filename
         
    def error_input_check(self, sanity_check):
        for i in range(len(sanity_check)):
            if sanity_check[i] == "" or sanity_check[i] == " ":
                sanity_check[i] = str(0)

        return sanity_check
        
    def process_input(self):
        prin_amount = self.input_field1.text()
        month = self.input_field2.text()
        rate = self.input_field3.text()
        compare_rate = self.input_field4.text()
        listofres = []
        sanity_check = [prin_amount, month, rate]
        sanity_check = self.error_input_check(sanity_check)
        
        prin_amount, month, rate = sanity_check[0], sanity_check[1] , sanity_check[2]
        
        if month == '0':
            results = prin_amount
            self.output_label.setText(f"Upon Maturity Date: {results}")
            dummy = "plotdata/" + f"img_{uuid.uuid4()}.png"
            plt.xlabel('Maturity (Month)')  # naming the x axis 
            plt.ylabel('Maturity Amount')  # naming the y axis
            plt.grid(True)
            plt.savefig(dummy,bbox_inches='tight', dpi=150)
            pixmap = QPixmap(dummy)  # Replace with your image file path
            self.image_label.setPixmap(pixmap)

        
        else:
            print("Here3")
            for i in range(len(sanity_check)):
                if sanity_check[i] == "":
                    sanity_check[i] = str(0)
                    
            prin_amount, month, rate = sanity_check[0], sanity_check[1] , sanity_check[2]
            print(sanity_check)
            if self.statuscheck == False:
                
                results,month_idx, money_idx, filename = self.fd_cal(month, rate, prin_amount)
                self.plotyy(month_idx, money_idx, filename)
                results = format(results, ".3f")
                self.output_label.setText(f"Upon Maturity Date: {results}")
                #print(filename)
                pixmap = QPixmap(filename)  # Replace with your image file path
                self.image_label.setPixmap(pixmap)

            else:
                initial_results, month_idx, money_idx, _ = self.fd_cal(month, rate, prin_amount)
                initial_results = format(initial_results, ".3f")
                compare_results, month_idx2, money_idx2, filename = self.fd_cal(month, compare_rate, prin_amount)
                compare_results = format(compare_results, ".3f")
                listofres = [float(initial_results),  float(compare_results)]
                #print(type(listofres[1]))
                self.compare_plotyy(month_idx, money_idx,month_idx2, money_idx2, filename)
                percen = format(((max(listofres)- min(listofres)) / min(listofres))*100, ".3f")
                self.output_label.setText(f"{rate}% : {initial_results}\n{compare_rate}% : {compare_results}\nPercentage of difference: {percen} %")
                pixmap = QPixmap(filename)  # Replace with your image file path
                self.image_label.setPixmap(pixmap)
            

                
            

            

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
