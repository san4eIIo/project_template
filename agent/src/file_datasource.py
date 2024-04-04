from csv import reader
from datetime import datetime
from domain.accelerometer import Accelerometer
from domain.gps import Gps
from domain.parking import Parking
from domain.aggregated_data import AggregatedData
import config


class FileDatasource:
    def __init__(
        self,
        accelerometer_filename: str,
        gps_filename: str,
        parking_filename: str,
    ) -> None:
        self.accelerometer_filename = accelerometer_filename
        self.gps_filename = gps_filename
        self.parking_filename = parking_filename
        with open(self.accelerometer_filename) as file:
            lines = [line.rstrip() for line in file]
            lines = lines[1:]
            self.accelerometer_filelines = lines
        
        with open(self.gps_filename) as file:
            lines = [line.rstrip() for line in file]
            lines = lines[1:]
            self.gps_filelines = lines
        
        with open(self.parking_filename) as file:
            lines = [line.rstrip() for line in file]
            lines = lines[1:]
            self.parking_filelines = lines

    def read(self) -> AggregatedData:
        """Метод повертає дані отримані з датчиків"""
        data = AggregatedData(
            Accelerometer(1, 2, 3),
            Gps(4, 5),
            Parking(1, Gps(1, 1)),
            datetime.now(),
            config.USER_ID,
        )
        if self.is_reading == True:
            if (self.accelerometer_read_line > len(self.accelerometer_filelines) - 1):
                self.accelerometer_read_line = 0
            
            if (self.gps_read_line > len(self.gps_filelines) - 1   ):
                self.gps_read_line = 0 
            
            if (self.parking_read_line > len(self.parking_filelines) - 1):
                self.parking_read_line = 0

            acceleration = self.accelerometer_filelines[self.accelerometer_read_line].split(',')
            gps = self.gps_filelines[self.gps_read_line].split(',')
            parking = self.parking_filelines[self.parking_read_line].split(',')
            
            x, y, z = acceleration
            data.accelerometer = Accelerometer(x, y, z)
            
            latitude, longitude = gps
            data.gps = Gps(longitude, latitude)
            
            longitude, latitude, empty_count = parking
            data.parking = Parking(empty_count, Gps(longitude, latitude))
            
            self.parking_read_line +=1
            self.gps_read_line += 1
            self.accelerometer_read_line += 1
        
        return data

    def startReading(self, *args, **kwargs):
        """Метод повинен викликатись перед початком читання даних"""
        self.parking_read_line = 0
        self.gps_read_line = 0
        self.accelerometer_read_line = 0
        self.is_reading = True

    def stopReading(self, *args, **kwargs):
        """Метод повинен викликатись для закінчення читання даних"""
        self.is_reading = False