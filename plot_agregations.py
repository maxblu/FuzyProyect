import matplotlib.pyplot as plt
import numpy as np

def plot_agregations(valores,a1,a2,a3,a1_act,a2_act,a3_act,variable):

    tip0 = np.zeros_like(valores)


    fig, ax0 = plt.subplots(figsize=(8, 3))

    ax0.fill_between(valores, tip0, a1_act, facecolor='b', alpha=0.7)
    ax0.plot(valores, a1, 'b', linewidth=0.5, linestyle='--', )
    ax0.fill_between(valores, tip0, a2_act, facecolor='g', alpha=0.7)
    ax0.plot(valores,a2, 'g', linewidth=0.5, linestyle='--')
    ax0.fill_between(valores, tip0, a3_act, facecolor='r', alpha=0.7)
    ax0.plot(valores, a3, 'r', linewidth=0.5, linestyle='--')
    ax0.set_title('Resultado de la agregacion para '+ variable)

    # Turn off top/right axes
    for ax in (ax0,):
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.get_xaxis().tick_bottom()
        ax.get_yaxis().tick_left()

    plt.tight_layout()

    plt.savefig('graficas/Resultado de la agregacion para '+ variable+'.png')

def plot_results(valores,agregated,defuzz1,defuzz2,defuzz3,defuzz4,defuzz5,grade1,grade2,grade3,grade4,grade5,variable):

    tip0 = np.zeros_like(valores)

    fig, ax0 = plt.subplots(figsize=(8, 3))

    ax0.fill_between(valores, tip0,agregated, facecolor='Orange', alpha=0.7)
    ax0.plot([defuzz1, defuzz1], [0,grade1],'b', linewidth=1.5, alpha=0.9 ,label='centroid' )
    ax0.plot([defuzz2, defuzz2], [0,grade2], 'g', linewidth=1.5, alpha=0.9,label='biseccion' )
    ax0.plot([defuzz3, defuzz3], [0,grade3], 'r', linewidth=1.5, alpha=0.9,label='max a la izq' )
    ax0.plot([defuzz4, defuzz4], [0,grade4], 'Black', linewidth=1.5, alpha=0.9,label='max a la der' )
    ax0.plot([defuzz5, defuzz5], [0,grade4], 'Purple', linewidth=1.5, alpha=0.9,label='promedio de max' )

    ax0.set_title('Resultados de la  desdifuzyficacion para '+ variable)
    ax0.legend()

    # Turn off top/right axes
    for ax in (ax0,):
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.get_xaxis().tick_bottom()
        ax.get_yaxis().tick_left()

    plt.tight_layout()
    plt.savefig('Resultados de la  desdifuzyficacion para '+ variable+'.png')
