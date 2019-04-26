import numpy as np
import matplotlib.pyplot as plt
import statistics
import datetime

class server:
  def __init__(self, serverid):
    self.serverid = serverid
    self.imageblocks      = 0
    self.totalblocks_sent = 0
    self.image_name       = ""
    self.client_list      = {}
    self.last_client      = 0
    self.active_clients   = 0
    self.file_size_in_mb  = 0
    self.file_read_time   = 0
    self.file_reread      = 0
    self.something_wrong  = False

class client:
  def __init__(self, clientid):
    self.clientid = clientid
    self.runtime                       = 0
    self.total_concurrent_overlap_time = 0
    self.concurrency_percentage        = 0
    self.concurrent_start              = None
    self.active                        = True 

class run_stats:
  def __init__(self, key):
    self.image_size_start = (key * 100) + 1
    self.image_size_end   = ((key+1)*100)
    self.min_time         = float("inf")
    self.max_time         = 0
    self.timelist         = []

class image_based_run_stats:
  def __init__ (self, key):
    self.image_name   = key
    self.timelist     = []

#----------------------------------------------------------------------------------------------------------------
def remove_prefix_in_loglien (line):
  words = line.split ()
  time_str = words[0] + " " + words[1] + " 2019 " + words[2]
  w4_1 = words[4].split('[')
  w4_2 = w4_1[1].split(']')

  ret_words = []
  ret_words.append (w4_2[0])
  for i in range (5, len(words)):
    ret_words.append (words[i])

  time = datetime.datetime.strptime(time_str, '%b %d %Y %H:%M:%S')
  return time, ret_words 

#----------------------------------------------------------------------------------------------------------------
def add_concurrency_to_existing_client (server, time):
  for kk, c in server.client_list.items ():
    if (c.active == True) and (c.concurrent_start == None):
      c.concurrent_start = time

#----------------------------------------------------------------------------------------------------------------
def remove_concurrency_from_existing_client (server, time):
  for kk, c in server.client_list.items ():
    if (c.active == True) and (c.concurrent_start != None):
      diff = time - c.concurrent_start
      c.total_concurrent_overlap_time += diff.total_seconds ()
      c.concurrent_start = None 

#----------------------------------------------------------------------------------------------------------------
def begin_extracting (filename):
  server_list = {}
  run_statistics = {}

  with open (filename) as file:
    for line in file:
      time, words = remove_prefix_in_loglien (line)
      #New server being opened
      if (len (words) > 1) and (words[1] == "Opened"):
        s = server (words[0])
        s.imageblocks = int (words[3])
        s.image_name = words[2]
        server_list[words[0]] = s

      elif (len(words) > 6) and (words[6] == "joins") and (words[2] == "(id"):
        if (words[0] not in server_list):
          s = server (words[0])
          server_list[words[0]] = s
        s = server_list [words[0]]

        words[3] = words[3][0:len(words[3])-1]
        #If client is not there already create it
        if words[3] not in s.client_list: 
          c = client(words[3])
          s.client_list[words[3]] = c
          c = s.client_list[words[3]]
          #There is already a client in the server, so this client is concurrent with that one.
          if (s.active_clients > 0):      
            c.concurrent_start = time 
            if (s.active_clients == 1):
              #The existing client will now have concurrency update that
              add_concurrency_to_existing_client (s, time)

          #Increment the active client count
          s.active_clients += 1 

      elif (len(words) > 3) and (words[1] == "Client") and (words[3] == "Performance:"):
        if (words[0] not in server_list):
          s = server (words[0])
          server_list[words[0]] = s
        s = server_list [words[0]]

        if words[2] not in s.client_list: #If client is not there already create it
          c = client(words[2])
          s.client_list[words[2]] = c
        c = s.client_list[words[2]]
        
        #Consider the end of concurrent time and account it
        if (c.concurrent_start != None):
          diff = time - c.concurrent_start
          c.total_concurrent_overlap_time += diff.total_seconds ()
          c.concurrent_start = None 

        #Set the client as inactive
        c.active = False

        #Decrement the active client count 
        s.active_clients -= 1 
        if (s.active_clients == 1):
          #The last concurrent client is gone, so remove the concurrency now for other dependent clients
          remove_concurrency_from_existing_client (s, time)

        s.last_client = words[2]
       
      elif (len(words) > 1) and (words[1] == "runtime:"):
        if (words[0] not in server_list):
          s = server (words[0])
          server_list[words[0]] = s
        s = server_list [words[0]]
        c = s.client_list[s.last_client]
        c.runtime = float(words[2])

        #Account the total concurrency percentage
        c.concurrency_percentage = (c.total_concurrent_overlap_time/c.runtime) * 100
        if (c.concurrency_percentage > 100):
          c.concurrency_percentage = 100

        key = int(((s.imageblocks/1024)-1)/100)
        if key not in run_statistics:
          rs = run_stats (key)
          run_statistics[key] = rs
          rs.min_time = c.runtime
          rs.max_time = c.runtime 
          rs.timelist.append (c.runtime)
        else:
          rs = run_statistics[key]
          rs.timelist.append (c.runtime)
          if (c.runtime < rs.min_time):
            rs.min_time = c.runtime
          elif (c.runtime > rs.max_time):
            rs.max_time = c.runtime 
      elif (len (words) > 1) and (words[1] == "1k"):
        if (words[0] not in server_list):
          s = server (words[0])
          server_list[words[0]] = s
        s = server_list [words[0]]
        s.totalblocks_sent = int(words[4])
      elif (len(words) == 8) and (words[7] == "repeated)"):
        if (words[0] not in server_list):
          s = server (words[0])
          server_list[words[0]] = s
        s = server_list [words[0]]
        s.file_reread = int (words[6])
      elif (len(words) == 11) and (words[1] == "file") and (words[2] == "read")  and (words[3] == "time:"):
        if (words[0] not in server_list):
          s = server (words[0])
          server_list[words[0]] = s
        s = server_list [words[0]]
        s.file_read_time = float (words[4])
        s.file_size_in_mb = s.imageblocks/ (1024)

  return server_list, run_statistics 

#----------------------------------------------------------------------------------------------------------------
def print_runtime_statistics (run_statistics):
  print ("Image Size Range : Minimum time taken : Maximum time taken")
  for kkk, stat in run_statistics.items ():
    print (stat.image_size_start,"-",stat.image_size_end, ",", stat.min_time, ",", stat.max_time)
    #print ("Image Range       : ", stat.image_size_start,"-",stat.image_size_end)
    #print ("Completion Times  : ", stat.timelist)
#----------------------------------------------------------------------------------------------------------------
def print_client_server_stats (server_list):
  servers_with_no_clients = []
  for k, s in server_list.items ():
    if (s.imageblocks == 0):
      continue

    no_of_clients = len (s.client_list)
    if (no_of_clients == 0):
      servers_with_no_clients.append (s.serverid)
      continue

    no_of_blocks_unicast = no_of_clients * s.imageblocks
    multicast_savings = (no_of_blocks_unicast - s.totalblocks_sent)

    print ("\nServer Id               : ", s.serverid)
    print ("Serving Image             : ", s.image_name)
    print ("Total clients served      : ", no_of_clients)
    print ("File read time            : ", s.file_read_time)
    print ("File size in MB           : ", s.file_size_in_mb)
    print ("File repeated reads       : ", s.file_reread)
    print ("Total blocks on image     : ", s.imageblocks)
    print ("Total blocks on multicast : ", s.totalblocks_sent)
    print ("Total blocks on unicast   : ", no_of_blocks_unicast)
    print ("Saving using multicast    : ", multicast_savings)
    if (s.totalblocks_sent != 0):
      print ("Ucast/Mcast ratio         : ", no_of_blocks_unicast/s.totalblocks_sent)
      print ("Something wrong           : False")
    else:
      s.something_wrong = True
      print ("Something wrong           : True")

    for kk, c in s.client_list.items ():
      #print (s.imageblocks/1024, ",", c.runtime)
      print ("    Client ID       : ", c.clientid)
      print ("    Runtime         : ", c.runtime)
      print ("    Concurrent time : ", c.total_concurrent_overlap_time)
      print ("    Concurrency     : ", c.concurrency_percentage, "%")
      print ("    Concurrent Start: ", c.concurrent_start)

  print ("\nNumber of servers with 0 clients : ", len(servers_with_no_clients))
  print ("List of them                     : ", servers_with_no_clients)

#----------------------------------------------------------------------------------------------------------------
def write_client_server_stats (server_list, op_filename):

  if (op_filename == None):
    print ("Output filename is not present")
    return
  
  fhandle = open (op_filename, "w+")

  servers_with_no_clients = []
  for k, s in server_list.items ():
    if (s.imageblocks == 0):
      continue

    no_of_clients = len (s.client_list)
    if (no_of_clients == 0):
      servers_with_no_clients.append (s.serverid)
      continue

    no_of_blocks_unicast = no_of_clients * s.imageblocks
    multicast_savings = (no_of_blocks_unicast - s.totalblocks_sent)

    fhandle.write ("\nServer Id               : " + str(s.serverid))
    fhandle.write ("\n")
    fhandle.write ("Serving Image             : " + s.image_name)
    fhandle.write ("\n")
    fhandle.write ("Total clients served      : " + str(no_of_clients))
    fhandle.write ("\n")
    fhandle.write ("File read time            : " + str(s.file_read_time))
    fhandle.write ("\n")
    fhandle.write ("File size in MB           : " + str(s.file_size_in_mb))
    fhandle.write ("\n")
    fhandle.write ("File repeated reads       : " + str(s.file_reread))
    fhandle.write ("\n")
    fhandle.write ("Total blocks on image     : " + str(s.imageblocks))
    fhandle.write ("\n")
    fhandle.write ("Total blocks on multicast : " + str(s.totalblocks_sent))
    fhandle.write ("\n")
    fhandle.write ("Total blocks on unicast   : " + str(no_of_blocks_unicast))
    fhandle.write ("\n")
    fhandle.write ("Saving using multicast    : " + str(multicast_savings))
    fhandle.write ("\n")
    if (s.totalblocks_sent != 0):
      fhandle.write ("Ucast/Mcast ratio         : " + str(no_of_blocks_unicast/s.totalblocks_sent))
      fhandle.write ("\n")
      fhandle.write ("Something wrong           : False")
      fhandle.write ("\n")
    else:
      s.something_wrong = True
      fhandle.write ("Something wrong           : True")
      fhandle.write ("\n")

    for kk, c in s.client_list.items ():
      fhandle.write ("    Client ID       : "+ str(c.clientid))
      fhandle.write ("\n")
      fhandle.write ("    Runtime         : "+ str(c.runtime))
      fhandle.write ("\n")
      fhandle.write ("    Concurrent time : "+ str(c.total_concurrent_overlap_time))
      fhandle.write ("\n")
      fhandle.write ("    Concurrency     : "+ str(c.concurrency_percentage) + "%")
      fhandle.write ("\n")
      fhandle.write ("    Concurrent Start: "+ str(c.concurrent_start))
      fhandle.write ("\n")

  fhandle.write ("\nNumber of servers with 0 clients : " + str(len(servers_with_no_clients)))
  fhandle.write ("\n")
  fhandle.write ("List of them                     : " + str(servers_with_no_clients))
  fhandle.write ("\n")

#----------------------------------------------------------------------------------------------------------------
def get_image_based_stats (server_list):
  image_based_stats = {}

  for k, s in server_list.items ():
    if (s.imageblocks == 0):
      continue

    no_of_clients = len (s.client_list)
    if (no_of_clients == 0):
      continue

    if s.image_name not in image_based_stats:
      i_stats = image_based_run_stats (s.image_name)
      image_based_stats[s.image_name] = i_stats
    else:
      i_stats = image_based_stats[s.image_name]

    for kk, c in s.client_list.items ():
      i_stats.timelist.append (c.runtime)

  return image_based_stats
#----------------------------------------------------------------------------------------------------------------
def print_only_runtime (server_list):
  for k, s in server_list.items ():
    for kk1, c in s.client_list.items ():
      #print ("time :", c.runtime, "size : ", s.imageblocks/1024,"MB")
      print (c.runtime)
      #print (s.imageblocks/1024,"MB")

#----------------------------------------------------------------------------------------------------------------
def plot_box_whisker (run_statistics):
  list_of_times = []
  list_of_sizes = []
  keylist = sorted (run_statistics)
  keylist.sort ()
  for kkk in keylist: 
    stat = run_statistics[kkk]
    size_str = str (stat.image_size_start) + "-" + str(stat.image_size_end)
    list_of_sizes.append (size_str)
    list_of_times.append (stat.timelist)

  fig = plt.figure(1, figsize=(20, 20))
  ax = fig.add_subplot(111)
  bp = ax.boxplot(list_of_times)
  ax.set_xticklabels(list_of_sizes, rotation=40, ha="right")
  plt.title ("Image size vs Time taken")
  plt.xlabel ("Image size (MB)")
  plt.ylabel ("Time taken (Seconds)")
  plt.savefig('boxplot.png')
  plt.show ()

def extract_image_name_from_line (line):
  words = line.split ("/")
  return (words[len(words)-1])

def image_based_box_whisker (run_stats):
  list_of_times = []
  list_of_names = []
  keylist = sorted (run_stats)

  for kkk in keylist:
    i_stat = run_stats[kkk]
    list_of_names.append (extract_image_name_from_line (i_stat.image_name))
    list_of_times.append (i_stat.timelist)

  fig = plt.figure(1, figsize=(30, 30))
  ax = fig.add_subplot(111)
  bp = ax.boxplot(list_of_times)
  print (len(list_of_names))

  ax.set_xticklabels(list_of_names, rotation=40, ha="right")
  plt.title ("Image vs Time taken")
  plt.xlabel ("Image")
  plt.ylabel ("Time taken (Seconds)")
  plt.savefig('boxplot.png')
  plt.show ()

#----------------------------------------------------------------------------------------------------------------
def print_image_based_stats (i_run_stats):
  list_of_times = []
  list_of_names = []
  keylist = sorted (i_run_stats)

  for kkk in keylist:
    i_stat = i_run_stats[kkk]
    print ("Image Name         : ", extract_image_name_from_line (i_stat.image_name))
    i_stat.timelist.sort ()
    print ("Min time taken     : ", i_stat.timelist[0])
    print ("Max time taken     : ", i_stat.timelist[len(i_stat.timelist)-1])
    print ("Median time taken  : ", statistics.median (i_stat.timelist))
    print ("Best to worst diff : ", i_stat.timelist[len(i_stat.timelist)-1] - i_stat.timelist[0])
    print ("\n")
 
#----------------------------------------------------------------------------------------------------------------
#Create all data files needed for CDF and other outputs
def create_all_data_files (server_list,
                           eliminated_server_list,
                           runtime_cdf_data_file, 
                           mcast_benefit_cdf_data_file,
                           num_clients_cdf_data_file,
                           image_size_cdf_data_file,
                           disk_thread_idle_cdf_data_file,
                           client_concurrency_cdf_data_file,
                           file_read_time_data_file,
                           file_size_data_file,
                           file_repeated_read_data_file,
                           p_file_read_time_data_file,
                           p_file_size_data_file,
                           p_file_repeated_read_data_file):

  #Open all files for writting
  runtime_f    = open (runtime_cdf_data_file, "w+")
  mcast_f      = open (mcast_benefit_cdf_data_file, "w+")
  num_client_f = open (num_clients_cdf_data_file ,"w+")
  img_size_f   = open (image_size_cdf_data_file ,"w+")
  disk_idle_f  = open (disk_thread_idle_cdf_data_file ,"w+") 
  concur_f     = open (client_concurrency_cdf_data_file ,"w+")
  fread_f      = open (file_read_time_data_file ,"w+")
  fsize_f      = open (file_size_data_file ,"w+")
  frepeated_f  = open (file_repeated_read_data_file ,"w+")
  p_fread_f    = open (p_file_read_time_data_file ,"w+")
  p_fsize_f    = open (p_file_size_data_file ,"w+")
  p_frepeated_f= open (p_file_repeated_read_data_file ,"w+")

  #Begin Looping and we are gonna print in all files parallely
  for k, s in server_list.items ():
    if (int(s.serverid) in eliminated_server_list):
      continue

    if (s.imageblocks == 0):
      continue

    no_of_clients = len (s.client_list)
    if (no_of_clients == 0):
      continue

    if (s.totalblocks_sent == 0):
      continue

    no_of_blocks_unicast = no_of_clients * s.imageblocks
    mcast_f.write (str((no_of_blocks_unicast/s.totalblocks_sent) - 1) + "\n")
    num_client_f.write (str(no_of_clients) + "\n")
    img_size_f.write (str(s.imageblocks) + "\n")
    if ("/proj" not in s.image_name):
      fread_f.write (str(s.file_read_time) + "\n")
      fsize_f.write (str(s.file_size_in_mb) + "\n")
      frepeated_f.write (str(s.file_reread) + "\n")
    else:
      p_fread_f.write (str(s.file_read_time) + "\n")
      p_fsize_f.write (str(s.file_size_in_mb) + "\n")
      p_frepeated_f.write (str(s.file_reread) + "\n")
    
    for kk, c in s.client_list.items ():
      runtime_f.write (str(c.runtime) + "\n")
      concur_f.write (str(c.concurrency_percentage) + "\n")

#----------------------------------------------------------------------------------------------------------------
#Main function
#NOT ACTIVE ANYMORE
def main_function ():
  server_list, run_statistics = begin_extracting ("messages.log") 
  
  #Print time taken analysis statistics
  #print_runtime_statistics (run_statistics)

  #Print client server stats
  print_client_server_stats (server_list)

  #Print only runtime
  #print_only_runtime (server_list)

  #Plot the box and whisker
  #plot_box_whisker (run_statistics)

  #Image based boxplot and whisker
  #i_run_stats = get_image_based_stats (server_list)
  #image_based_box_whisker (i_run_stats)
  #print_image_based_stats (i_run_stats)

#----------------------------------------------------------------------------------------------------------------
#main_function ()
