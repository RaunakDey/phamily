import matplotlib.pyplot as plt

def plot_node_time_series_euler(solution,Node,time,semilog = True, singlewindow = True):
    number_of_nodes = len(solution[:,0])
    #to be used for labels.
    node_names = [node.name for node in Node.instances]

    if singlewindow == True:
        fig, ax = plt.subplots()
        for count in range(number_of_nodes):
            ax.plot(time,solution[count,:],label=node_names[count])
            if semilog == True:
                plt.yscale('log')
            else:
                plt.yscale('linear')
        ax.legend(loc='upper left', frameon=False)
        plt.xlabel('Time (hour)')
        plt.ylabel('population')
        fig
        plt.show()
        

    else: 
        raise NotImplementedError
    


