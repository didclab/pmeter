"""PMeter a tool to measure the TCP/UDP network conditions that the running host experiences

Usage:
  pmeter_cli.py measure <INTERFACE> [-K=KER_BOOL -N=NET_BOOL -F=FILE_NAME -S=STD_OUT_BOOL --interval=INTERVAL --measure=MEASUREMENTS]

Commands:
    measure     The command to start measuring the computers network activity on the specified network devices. This command accepts a list of interfaces that you wish to monitor

Options:
  -h --help                Show this screen
  --version                Show version
  -F --file_name           Set the file name used to measure [default: network_results.txt]
  -N --measure_network     Set if we monitor only the network interface [default: True]
  -K --measure_kernel      Set if we monitor only the kernel [default: True]
  -U --measure_udp         Set UDP monitoring only [default: True]
  -T --measure_tcp         Set TCP monitoring only [default: True]
  -S --enable_std_out      Disable printing the results to standard output [default: False]
  --interval=INTERVAL      Set the time to run the measurement in the format HH:MM:SS [default: 00:00:04]
  --measure=MEASUREMENTS   The number of times to run the measurement [default: 1]
"""
from docopt import docopt
import multiprocessing
import constants

from file_writer import ODS_Metrics


if __name__ == '__main__':
    arguments = docopt(__doc__, version='Naval Fate 2.0')
    print(arguments)
    if arguments['measure']:
        interface = arguments['<INTERFACE>']
        file_name = arguments['--file_name']
        network_only = arguments['--measure_network']
        kernel_only = arguments['--measure_kernel']
        udp_only = arguments['--measure_udp']
        tcp_only = arguments['--measure_tcp']
        std_out_print = arguments['--enable_std_out']
        interval = arguments['--interval']
        pause_between_measure = constants.get_sec(interval)
        times_to_measure = arguments['--measure']
        metrics = ODS_Metrics()
        metrics.measure(interface=interface,measure_tcp=tcp_only, measure_kernel=kernel_only, measure_network=network_only, measure_udp=udp_only, print_to_std_out=std_out_print, interval=pause_between_measure, measurement=int(times_to_measure))
        print('In Measure')
