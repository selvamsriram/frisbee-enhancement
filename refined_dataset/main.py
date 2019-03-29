import sys
import argparse
import extract_data as ed
import cdf_plotter as cp

#-----------------------------------------------------------------------------------
#Global Constants
runtime_cdf_data_file = "runtime_cdf_input.data"
mcast_benefit_cdf_data_file = "mcast_benefit_cdf_input.data"
num_clients_cdf_data_file = "num_clients_cdf_input.data"
image_size_cdf_data_file = "image_size_cdf_input.data"
disk_thread_idle_cdf_data_file = "disk_thread_idle_cdf_input.data"
client_concurrency_cdf_data_file = "client_concurrency_cdf_input.data"
file_read_time_data_file = "file_read_time.data"
file_size_data_file = "file_size.data"
file_repeated_read_data_file = "file_read_repeated.data"
eliminated_server_list = [97749, 10800]

#-----------------------------------------------------------------------------------
#CLI Commands
parser = argparse.ArgumentParser()
parser.add_argument ("-i", "--ifile", help="Input file containing log messages")
parser.add_argument ("-o", "--ofile", help="Output file printing stats")
parser.add_argument ("-bp", "--boxplot", help="Boxplot of Image Size vs Time Taken", action="store_true")
parser.add_argument ("-rcdf", "--runtime-cdf", help="CDF of client runtime", action="store_true")
parser.add_argument ("-mcdf", "--mcast-cdf", help="CDF of multicast benefit", action="store_true")
parser.add_argument ("-ncdf", "--nclients-cdf", help="CDF of number of clients", action="store_true")
parser.add_argument ("-iscdf", "--image-size-cdf", help="CDF of image sizes served by various frisbee instances", action="store_true")
parser.add_argument ("-ccdf", "--concurrency-cdf", help="CDF of client concurrency", action="store_true")
parser.add_argument ("-dicdf", "--disk-idle-cdf", help="CDF of disk idle thread stats", action="store_true")
parser.add_argument ("-frscatter", "--file-read-scatter-plot", help="Scatter plot of file read stats", action="store_true")
#parser.add_argument ("-cache", "--cache-enabled", help="Use saved data from prev run to make CDFs and charts", action="store_true")
#parser.add_argument ("-ucache", "--update-cache", help="Update cache in this run", action="store_true")

args = parser.parse_args()
#Main processing condition
if (args.ifile != None):
  try:
    fhandle = open(args.ifile, 'r')
  except filenotfounderror:
    print ("input file doesn't exist")
    sys.exit ()
  server_list, run_statistics = ed.begin_extracting (args.ifile)

  #Print or Write the output to the file
  if (args.ofile == None):
    ed.print_client_server_stats (server_list)
  else:
    ed.write_client_server_stats (server_list, args.ofile)
  #Update cache file
  ed.create_all_data_files (server_list,
                            eliminated_server_list,
                            runtime_cdf_data_file,
                            mcast_benefit_cdf_data_file,
                            num_clients_cdf_data_file,
                            image_size_cdf_data_file,
                            disk_thread_idle_cdf_data_file,
                            client_concurrency_cdf_data_file,
                            file_read_time_data_file,
                            file_size_data_file,
                            file_repeated_read_data_file)
#-----------------------------------------------------------------------------------
#Box-Whisker Plot Image size vs Time taken
if (args.boxplot == True):
  if (args.ifile == None):
    print ("Box plot can't be drawn from cache, needs input file")
    sys.exit ()
  ed.plot_box_whisker (run_statistics)

#-----------------------------------------------------------------------------------
#Runtime CDF
if (args.runtime_cdf == True):
  try:
    fhandle = open(runtime_cdf_data_file, 'r')
  except filenotfounderror:
    print (runtime_cdf_data_file, "file doesn't exist")
    sys.exit ()

  cp.plot_runtime (runtime_cdf_data_file)
  print ("Client runtime CDF saved in runtime_cdf.png")

#-----------------------------------------------------------------------------------
#MCAST benefit CDF
if (args.mcast_cdf == True):
  try:
    fhandle = open(mcast_benefit_cdf_data_file, 'r')
  except filenotfounderror:
    print (mcast_benefit_cdf_data_file, "file doesn't exist")
    sys.exit ()

  cp.plot_mcast_benefit (mcast_benefit_cdf_data_file)
  print ("Mcast benefit CDF saved in mcast_benefit_cdf.png")

#-----------------------------------------------------------------------------------
#Number of Clients CDF
if (args.nclients_cdf == True):
  try:
    fhandle = open(num_clients_cdf_data_file, 'r')
  except filenotfounderror:
    print (num_clients_cdf_data_file, "file doesn't exist")
    sys.exit ()

  cp.plot_num_clients (num_clients_cdf_data_file)
  print ("Number of clients served CDF saved in number_of_clients_cdf.png")

#-----------------------------------------------------------------------------------
#Image Size CDF
if (args.image_size_cdf == True):
  try:
    fhandle = open(image_size_cdf_data_file, 'r')
  except filenotfounderror:
    print (image_size_cdf_data_file, "file doesn't exist")
    sys.exit ()

  cp.plot_image_size (image_size_cdf_data_file)
  print ("Image Size CDF saved in image_size_cdf.png")

#-----------------------------------------------------------------------------------
#Disk Thread Idle CDF
if (args.disk_idle_cdf == True):
  try:
    fhandle = open(disk_thread_idle_cdf_data_file, 'r')
  except filenotfounderror:
    print (disk_thread_idle_cdf_data_file, "file doesn't exist")
    sys.exit ()

  cp.plot_disk_idle (disk_thread_idle_cdf_data_file)
  print ("Disk thread idle time CDF saved in disk_thread_idle_cdf")

#-----------------------------------------------------------------------------------
#Client Concurrency CDF
if (args.concurrency_cdf == True):
  try:
    fhandle = open(client_concurrency_cdf_data_file, 'r')
  except filenotfounderror:
    print (client_concurrency_cdf_data_file, "file doesn't exist")
    sys.exit ()

  cp.plot_concurrency (client_concurrency_cdf_data_file)
  print ("Client Concurrency CDF saved in concurrency_cdf.png")

#-----------------------------------------------------------------------------------
#File Read Scatter Plot
if (args.file_read_scatter_plot == True):
  try:
    fhandle = open(file_read_time_data_file, 'r')
  except filenotfounderror:
    print (file_read_time_data_file, "file doesn't exist")
    sys.exit ()
  try:
    fhandle = open(file_size_data_file, 'r')
  except filenotfounderror:
    print (file_size_data_file, "file doesn't exist")
    sys.exit ()
  try:
    fhandle = open(file_repeated_read_data_file, 'r')
  except filenotfounderror:
    print (file_repeated_read_data_file, "file doesn't exist")
    sys.exit ()

  cp.file_read_graph (file_read_time_data_file, file_size_data_file, file_repeated_read_data_file)
#-----------------------------------------------------------------------------------
