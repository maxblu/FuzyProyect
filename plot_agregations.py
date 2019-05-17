import matplotlib.pyplot as plt
import numpy as np

def plot_agregations(valores,a1,a2,a3,a1_act,a2_act,a3_act):

    tip0 = np.zeros_like(valores)


    fig, ax0 = plt.subplots(figsize=(8, 3))

    ax0.fill_between(valores, tip0, a1_act, facecolor='b', alpha=0.7)
    ax0.plot(valores, a1, 'b', linewidth=0.5, linestyle='--', )
    ax0.fill_between(valores, tip0, a2_act, facecolor='g', alpha=0.7)
    ax0.plot(valores,a2, 'g', linewidth=0.5, linestyle='--')
    ax0.fill_between(valores, tip0, a3_act, facecolor='r', alpha=0.7)
    ax0.plot(valores, a3, 'r', linewidth=0.5, linestyle='--')
    ax0.set_title('Output membership activity')

    # Turn off top/right axes
    for ax in (ax0,):
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.get_xaxis().tick_bottom()
        ax.get_yaxis().tick_left()

    plt.tight_layout()

    plt.show()