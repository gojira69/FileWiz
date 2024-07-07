import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout

def main():
    app = QApplication(sys.argv)
    window = QWidget()
    window.setWindowTitle('PyQt5 Layout')
    
    # Create layout
    layout = QVBoxLayout()
    
    # Create a label and a button
    label = QLabel('Hello, PyQt5!')
    button = QPushButton('Click Me')
    
    # Add label and button to layout
    layout.addWidget(label)
    layout.addWidget(button)
    
    # Set layout for the window
    window.setLayout(layout)
    
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
