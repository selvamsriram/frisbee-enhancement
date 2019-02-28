class server:
  def __init__(self, serverid):
    self.serverid = serverid
    self.imageblocks = 0
    self.totalblocks_sent = 0
    self.image_name = ""
    self.client_list = {}
    self.last_client = 0

class client:
  def __init__(self, clientid):
    self.clientid = clientid
    self.runtime = 0

class run_stats:
  def __init__(self, key):
    self.image_size_start = (key * 100) + 1
    self.image_size_end   = ((key+1)*100)
    self.min_time         = float("inf")
    self.max_time         = 0

#----------------------------------------------------------------------------------------------------------------
def begin_extracting (filename):
  server_list = {}
  run_statistics = {}

  with open (filename) as file:
    for line in file:
      words = line.split ()
      #New server being opened
      if (len (words) > 1) and (words[1] == "Opened"):
        s = server (words[0])
        s.imageblocks = int (words[3])
        s.image_name = words[2]
        server_list[words[0]] = s
      
      elif (len(words) > 3) and (words[1] == "Client") and (words[3] == "Performance:"):
        s = server_list [words[0]]
        c = client(words[2])
        s.client_list[words[2]] = c
        s.last_client = words[2]

      elif (len(words) > 1) and (words[1] == "runtime:"):
        s = server_list [words[0]]
        c = s.client_list[s.last_client]
        c.runtime = float(words[2])
        key = int(((s.imageblocks/1024)-1)/100)
        if key not in run_statistics:
          rs = run_stats (key)
          run_statistics[key] = rs
          rs.min_time = c.runtime
          rs.max_time = c.runtime 
        else:
          rs = run_statistics[key]
          if (c.runtime < rs.min_time):
            rs.min_time = c.runtime
          elif (c.runtime > rs.max_time):
            rs.max_time = c.runtime 
      elif (len (words) > 1) and (words[1] == "1k"):
        s = server_list [words[0]]
        s.totalblocks_sent = int(words[4])
        
  return server_list, run_statistics 

#----------------------------------------------------------------------------------------------------------------
def print_runtime_statistics (run_statistics):
  print ("Image Size Range : Minimum time taken : Maximum time taken")
  for kkk, stat in run_statistics.items ():
    print (stat.image_size_start,"-",stat.image_size_end, ",", stat.min_time, ",", stat.max_time)


#----------------------------------------------------------------------------------------------------------------
def print_client_server_stats (server_list):
  servers_with_no_clients = []
  for k, s in server_list.items ():
    no_of_clients = len (s.client_list)

    if (no_of_clients == 0):
      servers_with_no_clients.append (s.serverid)
      continue

    no_of_blocks_unicast = no_of_clients * s.imageblocks
    multicast_savings = (no_of_blocks_unicast - s.totalblocks_sent)
    #print ((no_of_blocks_unicast/s.totalblocks_sent)-1)
    print (no_of_clients)
    #print (no_of_clients,",",(no_of_blocks_unicast/s.totalblocks_sent)-1)
    #print (s.imageblocks/1024,"MB")
    '''
    for kk, c in s.client_list.items ():
      print (s.imageblocks/1024, ",", c.runtime)
      print ("\nServer Id               : ", s.serverid)
      print ("Serving Image             : ", s.image_name)
      print ("Total clients served      : ", no_of_clients)
      print ("Total blocks on image     : ", s.imageblocks)
      print ("Total blocks on multicast : ", s.totalblocks_sent)
      print ("Total blocks on unicast   : ", no_of_blocks_unicast)
      print ("Saving using multicast    : ", multicast_savings)
      print ("Ucast/Mcast ratio         : ", no_of_blocks_unicast/s.totalblocks_sent)
      for kk, c in s.client_list.items ():
        print ("    Client ID       : ", c.clientid)
        print ("    Runtime         : ", c.runtime)
    '''
  print ("\nNumber of servers with 0 clients : ", len(servers_with_no_clients))
  print ("List of them                     : ", servers_with_no_clients)

#----------------------------------------------------------------------------------------------------------------
def print_only_runtime (server_list):
  for k, s in server_list.items ():
    no_of_clients = len (s.client_list)

    for kk1, c in s.client_list.items ():
      for kk2, c in s.client_list.items ():
        print (c.runtime)

#----------------------------------------------------------------------------------------------------------------
#Main function
def main_function ():
  server_list, run_statistics = begin_extracting ("messages.log") 
  
  #Print time taken analysis statistics
  #print_runtime_statistics (run_statistics)

  #Print client server stats
  print_client_server_stats (server_list)

  #Print only runtime
  #print_only_runtime (server_list)
#----------------------------------------------------------------------------------------------------------------
main_function ()
