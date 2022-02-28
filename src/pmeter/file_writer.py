from email.policy import default
import multiprocessing
import json
from datetime import date, datetime
import psutil
import platform


class ODS_Metrics():

    def __init__(self):
        #kernel metrics 
        self.active_core_count = 0
        self.cpu_frequency = 0.0
        self.energy_consumed = 0.0
        self.cpu_arch = ""
        #network metrics
        self.rtt = 0.0
        self.bandwidth = 0.0
        self.bandwidth_delay_product = 0.0
        self.packet_loss_rate = 0.0
        self.link_capacity = 0.0
        self.bytes_sent = 0.0
        self.bytes_recv = 0.0
        self.packets_sent = 0
        self.packets_recv = 0
        self.dropin = 0
        self.dropout = 0
        #identifying properties
        self.start_time=""
        self.end_time=""
        self.count = 0

    # def active_core_count(self):
    #     self.active_core_count = multiprocessing.cpu_count()

    def to_file(self, file_name):
        j = json.dumps(self.__dict__)
        with open(file_name, "a+") as f:
            f.write(j + "\n")
    
    def measure(self, measure_tcp=True, measure_udp=True, measure_kernel=True, measure_network=True, print_to_std_out=False):
        self.start_time = datetime.now().__str__()

        if measure_kernel:
            self.active_core_count = multiprocessing.cpu_count()
            self.cpu_frequency = psutil.cpu_freq()
            self.cpu_arch = platform.platform()
        if measure_network:
            print('Measuring your network')
            print(psutil.net_if_stats())
        if measure_tcp:
            print('Measuring tcp')
            psutil.net_connections(kind="tcp")
        if measure_udp:
            print('Measuring udp')
            psutil.net_connections(kind="udp")

        self.end_time=datetime.now().__str__()
        if(print_to_std_out):
            print(json.dumps(self.__dict__))
        
        self.to_file("pmeter_measure.txt")

    def defaultconverter(o):
        if isinstance(o, datetime.datetime):
            return o.__str__()

