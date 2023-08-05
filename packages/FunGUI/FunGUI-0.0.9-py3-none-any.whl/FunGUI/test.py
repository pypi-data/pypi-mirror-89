from math import *
def plot_sin(t=[*range(1000)],frequency1 = 10,phase1=2.05,offset1=30,amplify1=10,
                            frequency2 = 20,phase2=2.01,offset2=3,amplify2=10):

    error = ''#@
    try:
        x,y1,y2 =[],[],[]
        for t_i in t:
            t_i+=1
            t_i = t_i/1.0
            y1.append(amplify1*sin((t_i+phase1)*frequency1*2*pi)+offset1)
            y2.append((amplify2*sin((t_i+phase2)*frequency2*2*pi)+offset2)*log(t_i))

            # y3.append()
        plot = [t,y1,y2] #@
    except Exception as e:
        error = e #@

    return plot
if __name__ == "__main__":
    plot = plot_sin()
    import matplotlib.pyplot as plt
    plt.plot(plot[0],plot[2])
    # plt.ylabel('some numbers')
    plt.show()
# print(log(0))
