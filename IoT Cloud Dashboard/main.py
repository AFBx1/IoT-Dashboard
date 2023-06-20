import sys
import os
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.uic import *
from PyQt5.Qt import QApplication
from PyQt5.QtWidgets import QMainWindow, QGraphicsScene, QMessageBox
import boto3
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.dates as mdates
import matplotlib.pyplot as plt


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("arayuz.ui", self)
        self.setWindowTitle('IoT Cloud Dashboard')

        self.button_show_csv.clicked.connect(self.show_csv)
        self.button_open_csv.clicked.connect(self.open_csv)
        self.button_update_csv.clicked.connect(self.update_csv)
        self.button_update_dataset.clicked.connect(self.start_query)
        self.button_clear_dataset.clicked.connect(self.clear_dataset)
        self.button_show_lastgraphic.clicked.connect(self.show_graphic)
        self.button_update_graphics.clicked.connect(self.show_updated_graphic)
        self.button_clearConsole.clicked.connect(self.clear_console)
        self.url = self.connect_aws()

        self.rbutton_num.setChecked(True)

    def show_graphic(self):
        if self.rbutton_time.isChecked():
            self.show_lastgraphic()
        else:
            self.show_lastgraphicNum()

    def show_updated_graphic(self):
        if self.rbutton_num.isChecked():
            self.update_graphicsNum()
        else:
            self.update_graphics()

    def show_on_ui(self):

        scene = QGraphicsScene()
        image_path = "figure.png"
        pixmap = QPixmap(image_path)
        scene.addPixmap(pixmap)
        self.grafik1.setScene(scene)
        self.grafik1.show()

    def connect_aws(self):
        try:
            self.client = boto3.client('iotanalytics')
            self.response = self.client.get_dataset_content(
                datasetName='clusterdataset'
            )
            self.client.close()
            url = self.response['entries'][0]['dataURI']
            return url
        except:
            self.console_output.appendPlainText("Cannot Found any Dataset !")

    def show_csv(self):
        timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S] ")
        self.console_output.appendPlainText(timestamp + "Printing dataset...\n")
        dataframe = pd.read_csv('dataset_aws.csv')
        if dataframe.empty:
            timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S] ")
            self.console_output.appendPlainText(timestamp + "EMPTY DATASET !")
            return
        self.console_output.appendPlainText(dataframe.to_string() + "\n")

    def update_csv(self):
        timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S] ")
        self.console_output.appendPlainText(timestamp + "Updating CSV.")
        try:
            self.url = self.connect_aws()
            dataframe = pd.read_csv(self.url)
            dataframe.drop(['__dt'], axis='columns', inplace=True)
            dataframe.to_csv('dataset_aws.csv', encoding='utf-8', index=False)
            timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S] ")
            self.console_output.appendPlainText(timestamp +
                                                "Successfully updated the CSV.")
        except:
            timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S] ")
            self.console_output.appendPlainText(timestamp +
                                                'Error while updating CSV.')

    def open_csv(self):
        timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S] ")
        self.console_output.appendPlainText(timestamp + "Opening CSV...")
        try:
            project_directory = os.getcwd()
            csv_file_path = os.path.join(project_directory, 'dataset_aws.csv')
            if os.path.isfile(csv_file_path):
                if sys.platform.startswith('win'):
                    os.startfile(csv_file_path)
            else:
                timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S] ")
                self.console_output.appendPlainText(timestamp +
                                                    'CSV file not found.')
        except:
            timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S] ")
            self.console_output.appendPlainText(timestamp +
                                                "Error while opening the CSV.")
        else:
            timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S] ")
            self.console_output.appendPlainText(timestamp +
                                                "Successfully opened the CSV.")

    def show_lastgraphicNum(self):

        dataframe = pd.read_csv('dataset_aws.csv')
        if dataframe.empty:
            timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S] ")
            self.console_output.appendPlainText(timestamp + "EMPTY DATASET !")
            return
        else:
            timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S] ")
            self.console_output.appendPlainText(timestamp +
                                                "Showing Last Created "
                                                "Graphic (Number Indexed)...")

        plt.close()
        plt.figure(figsize=(8, 6))
        plt.plot(dataframe['y_axis'])
        plt.xticks(range(len(dataframe['y_axis'])))
        plt.yticks([dataframe['y_axis'].min(), 0, dataframe['y_axis'].max()])

        plt.xlabel('')
        plt.ylabel('(g) (m/s^2)')
        plt.title('Vibration')
        plt.tight_layout()
        plt.grid()

        plt.savefig('figure.png')
        self.show_on_ui()

        timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S] ")
        self.console_output.appendPlainText(timestamp + "Last Graphic shown."
                                                        "(Number Indexed)")

    def show_lastgraphic(self):
        dataframe = pd.read_csv('dataset_aws.csv')
        if dataframe.empty:
            timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S] ")
            self.console_output.appendPlainText(timestamp + "EMPTY DATASET !")
            return
        else:
            timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S] ")
            self.console_output.appendPlainText(timestamp + "Showing Last "
                                                            "Created Graphic "
                                                            "(Time Indexed)...")

        dataframe['datetime'] = pd.to_datetime(dataframe['datetime'])
        plt.close()
        fig, ax = plt.subplots(figsize=(10, 6))
        scatter = ax.scatter(dataframe['datetime'], dataframe['y_axis'], s=25, color='orange')
        scatter = ax.plot(dataframe['datetime'], dataframe['y_axis'])

        ax.xaxis.set_major_locator(mdates.SecondLocator(interval=1))
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))

        plt.xticks(rotation=90)
        plt.yticks([dataframe['y_axis'].min(), 0, dataframe['y_axis'].max()])
        plt.xlabel('Time')
        plt.ylabel('(g) (m/s^2)')
        plt.title('Vibration')
        plt.tight_layout()
        plt.grid()

        plt.savefig('figure.png')
        self.show_on_ui()

        timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S] ")
        self.console_output.appendPlainText(timestamp + "Last Graphic "
                                                        "shown.(Time Indexed)")

    def update_graphics(self):
        self.url = self.connect_aws()

        dataframe = pd.read_csv(self.url)
        if dataframe.empty:
            timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S] ")
            self.console_output.appendPlainText(timestamp + "EMPTY DATASET !")
            return
        else:
            timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S] ")
            self.console_output.appendPlainText(timestamp + "Updating Graphic "
                                                            "(Time Indexed)...")

        dataframe.drop(['__dt'], axis='columns', inplace=True)
        dataframe.to_csv('dataset_aws.csv', encoding='utf-8', index=False)
        dataframe['datetime'] = pd.to_datetime(dataframe['datetime'])

        plt.close()

        fig, ax = plt.subplots(figsize=(10, 6))
        scatter = ax.scatter(dataframe['datetime'], dataframe['y_axis'], s=25, color='orange')
        scatter = ax.plot(dataframe['datetime'], dataframe['y_axis'])

        ax.xaxis.set_major_locator(mdates.SecondLocator(interval=1))
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))

        plt.xticks(rotation=90)
        plt.yticks([dataframe['y_axis'].min(), 0, dataframe['y_axis'].max()])
        plt.xlabel('Time')
        plt.ylabel('(g) (m/s^2)')
        plt.title('Vibration')
        plt.tight_layout()
        plt.grid()

        plt.savefig('figure.png')
        self.show_on_ui()

        timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S] ")
        self.console_output.appendPlainText(timestamp + "Graphic updated.")

    def update_graphicsNum(self):
        self.url = self.connect_aws()

        dataframe = pd.read_csv(self.url)
        if dataframe.empty:
            timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S] ")
            self.console_output.appendPlainText(timestamp + "EMPTY DATASET !")
            return
        else:
            timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S] ")
            self.console_output.appendPlainText(timestamp + "Updating Graphic "
                                                            "(Number Indexed)...")
        dataframe.drop(['__dt'], axis='columns', inplace=True)
        dataframe.to_csv('dataset_aws.csv', encoding='utf-8', index=False)

        plt.close()
        plt.figure(figsize=(8, 6))
        plt.plot(dataframe['y_axis'])
        plt.xticks(range(len(dataframe['y_axis'])))
        plt.yticks([0, max(dataframe['y_axis'])])
        plt.xlabel('')
        plt.ylabel('(g) (m/s^2)')
        plt.title('Vibration')
        plt.tight_layout()
        plt.grid()

        plt.savefig('figure.png')
        self.show_on_ui()

        timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S] ")
        self.console_output.appendPlainText(timestamp + "Graphic updated.")

    def clear_console(self):
        self.console_output.clear()

    def start_query(self):
        try:
            self.queryClient = boto3.client('iotanalytics')

            # Create a dataset content without scheduling
            self.queryResponse = self.queryClient.create_dataset_content(
                datasetName='clusterdataset'
            )
            self.queryClient.close()
            timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S] ")
            self.console_output.appendPlainText(timestamp + " Query Finished.")
        except:
            timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S] ")
            self.console_output.appendPlainText(timestamp + " Query FAILED !")

    def clear_dataset(self):
        result = QMessageBox.question(self, 'Cleanup Dataset',
                                      "Are you sure you want to clear the dataset?",
                                      QMessageBox.Yes | QMessageBox.No)
        if result == QMessageBox.Yes:
            try:
                self.clearClient = boto3.client('iotanalytics')
                self.clearResponse = self.clearClient.delete_dataset_content(
                    datasetName='clusterdataset'
                )
                self.clearClient.close()
                timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S] ")
                self.console_output.appendPlainText(timestamp + " Cleanup Finished.")
            except:
                timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S] ")
                self.console_output.appendPlainText(timestamp + " Cleanup FAILED !")
        else:
            timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S] ")
            self.console_output.appendPlainText(timestamp + " Cleanup Canceled.")


if __name__ == "__main__":
    app = QApplication(sys.argv)

    icon_path = 'icon.ico'
    app_icon = QIcon(icon_path)
    app.setWindowIcon(app_icon)

    MainWindow = MainWindow()
    MainWindow.setFixedSize(1413, 847)
    MainWindow.show()

    sys.exit(app.exec())
