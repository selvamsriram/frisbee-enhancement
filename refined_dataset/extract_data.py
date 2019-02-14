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

def begin_extracting (filename):
  server_list = {}
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

      elif (len (words) > 1) and (words[1] == "1k"):
        s = server_list [words[0]]
        s.totalblocks_sent = int(words[4])
        
  return server_list 

#Main function
server_list = begin_extracting ("messages.log") 

for k, s in server_list.items ():
  no_of_clients = len (s.client_list)
  no_of_blocks_unicast = no_of_clients * s.imageblocks
  print ("\nServer Id               : ", s.serverid)
  print ("Serving Image             : ", s.image_name)
  print ("Total clients served      : ", no_of_clients)
  print ("Total blocks on image     : ", s.imageblocks)
  print ("Total blocks on multicast : ", s.totalblocks_sent)
  print ("Total blocks on unicast   : ", no_of_blocks_unicast)
  print ("Saving using multicast    : ", (no_of_blocks_unicast - s.totalblocks_sent))

  '''
  for c in s.client_list:
    print ("    Client ID       : ", c.clientid)
    print ("    Runtime         : ", c.runtime)
    '''
