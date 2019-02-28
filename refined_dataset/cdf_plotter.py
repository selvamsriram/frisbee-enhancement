import numpy as np
import matplotlib.pyplot as plt

def plot_runtime ():
  r_data = np.loadtxt("runtime.data")
  sorted_r_data = np.sort(r_data)
  yvals=np.arange(len(sorted_r_data))/float(len(sorted_r_data)-1)
  plt.plot(sorted_r_data,yvals)
  plt.show()

def plot_mcast_vs_clients ():
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
  plt.show()

def main():
  #plot_runtime ()
  plot_mcast_vs_clients ()

main()
