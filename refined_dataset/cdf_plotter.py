import numpy as np
import matplotlib.pyplot as plt

def plot_runtime ():
  r_data = np.loadtxt("runtime.data")
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
  #plt.savefig('image_size_cdf.png')

def plot_image_size():
  r_data = np.loadtxt("image_size.data")
  sorted_r_data = np.sort(r_data)
  yvals=np.arange(len(sorted_r_data))/float(len(sorted_r_data)-1)
  plt.plot(sorted_r_data,yvals, label='Image Size (MB)')
  plt.legend()
  plt.xlabel ("Image Size (MB)")
  plt.ylabel ("Probability")
  plt.show()
  plt.savefig('image_size_cdf.png')

def plot_mcast_benefit():
  plt.clf ()
  r_data = np.loadtxt("mcast_benefit.data")
  sorted_r_data = np.sort(r_data)
  yvals=np.arange(len(sorted_r_data))/float(len(sorted_r_data)-1)
  plt.plot(sorted_r_data,yvals, label='Mcast benefit')
  plt.legend()
  plt.xlabel ("Mcast Benefit")
  plt.ylabel ("Probability")
  plt.show()
  plt.savefig('mcast_benefit_cdf.png')

def plot_num_clients():
  plt.clf ()
  r_data = np.loadtxt("num_clients.data")
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

def plot_concurrency():
  r_data = np.loadtxt("concurrency_cdf.data")
  sorted_r_data = np.sort(r_data)
  yvals=np.arange(len(sorted_r_data))/float(len(sorted_r_data)-1)
  plt.plot(sorted_r_data,yvals, label='Concurrency')
  plt.legend()
  plt.xlabel ("% of concurrency")
  plt.ylabel ("Probability")
  plt.show()
  plt.savefig('concurrency_cdf.png')

def main():
  #plot_runtime ()
  #plot_mcast_benefit ()
  #plot_num_clients ()
  #plot_image_size()
  #plot_disk_idle ()
  #plot_mcast_vs_clients ()
  plot_concurrency ()

main()
