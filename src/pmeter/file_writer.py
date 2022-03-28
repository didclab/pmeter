from email.policy import default
import multiprocessing
from pathlib import Path
import json
from datetime import date, datetime
import psutil
import platform
from tcp_latency import measure_latency
import os
import time
import requests
from pythonping import ping
from datetime import datetime, timedelta


class ODS_Metrics():

    def __init__(self):
        # kernel metrics
        self.active_core_count = 0
        self.cpu_frequency = []
        self.energy_consumed = 0.0
        self.cpu_arch = ""
        # network metrics
        self.interface = ""
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
        self.nic_speed = 0  # this is in mb=megabits
        self.nic_mtu = 0  # max transmission speed of nic
        # identifying properties
        self.start_time = ""
        self.end_time = ""
        self.count = 0
        self.latency = []

    # def active_core_count(self):
    #     self.active_core_count = multiprocessing.cpu_count()
    def to_file(self, folder_path="/.pmeter", file_name="pmeter_measure.txt"):
        folder_path = str(Path.home())+folder_path
        file_path = folder_path + "/" + file_name
        j = json.dumps(self.__dict__)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        with open(file_path, "a+") as f:
            f.write(j + "\n")

    def length_measure(self, interface='', measure_tcp=True, measure_udp=True, measure_kernel=True, measure_network=True, print_to_std_out=False, interval="00:00:01", latency_host="google.com", length="0s"):
        end_date = datetime.now()
        num = int(length[:-1])
        print("The number of length measure", num)
        if "s" in length:
            end_date = datetime.now() + timedelta(seconds=num)
        if "d" in length:
            end_date = datetime.now() + timedelta(days=num)
        if "w" in length:
            end_date = datetime + timedelta(weeks=num)
        if "h" in length:
            end_date = datetime + timedelta(hours=num)

        current_date = datetime.now()
        while(current_date < end_date):
            self.measure(interface, measure_tcp, measure_udp, measure_kernel,
                         measure_network, print_to_std_out, interval, latency_host)
            current_date = datetime.now()
            print(current_date, end_date)


    def measurements_to_do(self, interface='', measure_tcp=True, measure_udp=True, measure_kernel=True, measure_network=True, print_to_std_out=False, interval="00:00:01", latency_host="google.com", measurement=1):
        for i in range(0, measurement):
            self.measure(interface, measure_tcp, measure_udp, measure_kernel,
                         measure_network, print_to_std_out, interval, latency_host)

    def measure(self, interface='', measure_tcp=True, measure_udp=True, measure_kernel=True, measure_network=True, print_to_std_out=False, interval="00:00:01", latency_host="google.com"):
        self.start_time = datetime.now().__str__()
        self.interface = interface
        if measure_kernel:
            self.active_core_count = multiprocessing.cpu_count()
            self.cpu_frequency = psutil.cpu_freq()
            self.cpu_arch = platform.platform()
        if measure_network:
            print('Getting metrics of: ' + interface)
            # we could take the average of all speeds that every socket experiences and thus get a rough estimate of bandwidth??
            nic_counter_dic = psutil.net_io_counters(pernic=True)
            interface_counter_tuple = nic_counter_dic[interface]
            self.bytes_sent = interface_counter_tuple[0]
            self.bytes_recv = interface_counter_tuple[1]
            self.packets_sent = interface_counter_tuple[2]
            self.packets_recv = interface_counter_tuple[3]
            self.errin = interface_counter_tuple[4]
            self.errout = interface_counter_tuple[5]
            self.dropin = interface_counter_tuple[6]
            self.dropout = interface_counter_tuple[7]
            sys_interfaces = psutil.net_if_stats()
            interface_stats = sys_interfaces[self.interface]
            self.nic_mtu = interface_stats[3]
            self.nic_speed = interface_stats[2]
            self.latency = measure_latency(host=latency_host)
            self.rtt = self.find_rtt()
            print(self.latency)
        if measure_tcp:
            print('Measuring tcp')
            psutil.net_connections(kind="tcp")
        if measure_udp:
            print('Measuring udp')
            psutil.net_connections(kind="udp")
        self.end_time = datetime.now().__str__()
        if(print_to_std_out):
            print(json.dumps(self.__dict__))
        self.to_file()
        time.sleep(interval)

    def find_rtt(self, url=None):
        default_rtt = 0
        new_rtt = -1
        try:
            response_list = ping(('8.8.8.8'))
            new_rtt = response_list.rtt_avg_ms
        except:
            try:
                if not url:
                    url = "http://www.google.com"
                t1 = time.time()
                r = requests.get(url)
                t2 = time.time()
                new_rtt = t2-t1
            except:
                new_rtt = default_rtt
        finally:
            return new_rtt if new_rtt != -1 else default_rtt
