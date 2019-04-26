import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
from scipy.stats import spearmanr

def plot_runtime (runtime_cdf_data_file):
  r_data = np.loadtxt(runtime_cdf_data_file)
  sorted_r_data = np.sort(r_data)
  yvals=np.arange(len(sorted_r_data))/float(len(sorted_r_data)-1)
  plt.plot(sorted_r_data,yvals, label='Runtime')
  plt.legend()
  plt.xlabel ("Client Runtime (in Seconds)")
  plt.ylabel ("Probability")
  plt.show()
  plt.savefig('runtime_cdf.png')

def plot_disk_idle ():
  r_data = np.loadtxt("disk_thread_idle.data")
  sorted_r_data = np.sort(r_data)
  yvals=np.arange(len(sorted_r_data))/float(len(sorted_r_data)-1)
  plt.plot(sorted_r_data,yvals, label='Disk Thread Idle (Ticks)')
  plt.legend()
  plt.xlabel ("Disk Thread Idle (Ticks)")
  plt.ylabel ("Probability")
  plt.show()
  plt.savefig('disk_thread_idle_cdf.png')

def plot_image_size(image_size_cdf_data_file):
  r_data = np.loadtxt(image_size_cdf_data_file)
  sorted_r_data = np.sort(r_data)
  yvals=np.arange(len(sorted_r_data))/float(len(sorted_r_data)-1)
  plt.plot(sorted_r_data,yvals, label='Image Size (MB)')
  plt.legend()
  plt.xlabel ("Image Size (MB)")
  plt.ylabel ("Probability")
  plt.show()
  plt.savefig('image_size_cdf.png')

def plot_mcast_benefit(mcast_benefit_cdf_data_file):
  plt.clf ()
  r_data = np.loadtxt(mcast_benefit_cdf_data_file)
  sorted_r_data = np.sort(r_data)
  yvals=np.arange(len(sorted_r_data))/float(len(sorted_r_data)-1)
  plt.plot(sorted_r_data,yvals, label='Mcast benefit')
  plt.legend()
  plt.xlabel ("Mcast Benefit")
  plt.ylabel ("Probability")
  plt.show()
  plt.savefig('mcast_benefit_cdf.png')

def plot_num_clients(num_clients_cdf_data_file):
  plt.clf ()
  r_data = np.loadtxt(num_clients_cdf_data_file)
  sorted_r_data = np.sort(r_data)
  yvals=np.arange(len(sorted_r_data))/float(len(sorted_r_data)-1)
  plt.plot(sorted_r_data,yvals, label='Number of Clients')
  plt.legend()
  plt.xlabel ("Number of clients")
  plt.ylabel ("Probability")
  plt.show()
  plt.savefig('number_of_clients_cdf.png')

def plot_mcast_vs_clients ():
  plt.clf ()
  m_data = np.loadtxt ("mcast_benefit.data")
  c_data = np.loadtxt ("num_clients.data")

  sorted_m_data = np.sort (m_data)
  sorted_c_data = np.sort (c_data)

  yvals = np.arange(len(sorted_m_data))/float(len(sorted_m_data)-1)
  plt.plot(sorted_m_data,yvals, label='Mcast Benefit')
  
  yvals = np.arange(len(sorted_c_data))/float(len(sorted_c_data)-1)
  plt.plot(sorted_c_data,yvals, label='Num of Clients')
  plt.legend()
  plt.xlabel("Num of clients/Mcast Benefit")
  plt.ylabel("Probability")
  #plt.show()
  plt.savefig('mcast_vs_clients.png')

def plot_concurrency(client_concurrency_cdf_data_file):
  r_data = np.loadtxt(client_concurrency_cdf_data_file)
  sorted_r_data = np.sort(r_data)
  yvals=np.arange(len(sorted_r_data))/float(len(sorted_r_data)-1)
  plt.plot(sorted_r_data,yvals, label='Concurrency')
  plt.legend()
  plt.xlabel ("% of concurrency")
  plt.ylabel ("Probability")
  plt.show()
  plt.savefig('concurrency_cdf.png')

def plot_concurrency_histogram (client_concurrency_cdf_data_file):
  r_data = np.loadtxt(client_concurrency_cdf_data_file)
  plt.hist (r_data, density=0, bins=10)
  plt.legend()
  plt.xlabel ("% of concurrency")
  plt.show()
  plt.savefig('concurrency_hist.png')
 
def file_read_graph (file_read_time_data_file, file_size_data_file, num_clients_cdf_data_file, file_repeated_read_data_file,
                     p_file_read_time_data_file, p_file_size_data_file, p_file_repeated_read_data_file):
  readtime_data = np.loadtxt (file_read_time_data_file)
  size_in_mb    = np.loadtxt (file_size_data_file)
  no_of_clients = np.loadtxt (num_clients_cdf_data_file)
  repeated_data = np.loadtxt (file_repeated_read_data_file)

  '''
  print ("Size and Read time")
  print ("----------------------------------------")
  corr, _ = pearsonr(size_in_mb, readtime_data)
  print('Pearsons correlation: %.3f' % corr)
  
  corr, _ = spearmanr(size_in_mb, readtime_data)
  print('Spearmans correlation: %.3f' % corr)

  print ("\nNumber of Clients and Repeated reads")
  print ("----------------------------------------")
  corr, _ = pearsonr(no_of_clients, repeated_data)
  print('Pearsons correlation: %.3f' % corr)
  
  corr, _ = spearmanr(no_of_clients, repeated_data)
  print('Spearmans correlation: %.3f' % corr)
  '''

  plt.plot(size_in_mb,readtime_data, 'o', color='blue')
  plt.xlabel ("Size in MB")
  plt.ylabel ("Readtime in Seconds")
  readtime_data = np.loadtxt (p_file_read_time_data_file)
  size_in_mb    = np.loadtxt (p_file_size_data_file)
  plt.plot(size_in_mb,readtime_data, 'o', color='red')
  plt.legend()
  plt.show()
  plt.savefig('file_size_vs_readtime.png')
 
  '''
  plt.plot(no_of_clients, repeated_data, 'o', color='red')
  plt.legend()
  plt.xlabel ("Number of Clients")
  plt.ylabel ("Repeated reads")
  plt.show()
  plt.savefig('no_of_clients_vs_repeated_reads.png')
  '''
 
  '''
  fig, ax1 = plt.subplots ()
  color = 'tab:red'
  ax1.set_xlabel('Size in MB')
  ax1.set_ylabel('File read time (Secs)', color=color)
  ax1.plot(size_in_mb, readtime_data, 'o', color=color)
  ax1.tick_params(axis='y', labelcolor=color)

  ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

  color = 'tab:blue'
  ax2.set_ylabel('Repeated Reads', color=color)  # we already handled the x-label with ax1
  ax2.plot(size_in_mb, repeated_data, color=color)
  ax2.tick_params(axis='y', labelcolor=color)
  
  fig.tight_layout()  # otherwise the right y-label is slightly clipped
  plt.show ()
  '''
def main():
  #plot_runtime ()
  #plot_mcast_benefit ()
  #plot_num_clients ()
  #plot_image_size()
  #plot_disk_idle ()
  #plot_concurrency ()
  file_read_graph ()

#main()
