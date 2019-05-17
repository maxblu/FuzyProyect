import matplotlib.pyplot as plt


def plot_funtions(xp,p1,p2,p3,xph,ph1,ph2,ph3,xd,d1,d2,d3,xa,a1,a2,a3):

    # Visualize these universes and membership functions
    fig, (ax0, ax1, ax2,ax3) = plt.subplots(nrows=4, figsize=(8, 9))

    ax0.plot(xp, p1, 'b', linewidth=1.5, label='Ligera')
    ax0.plot(xp, p2, 'g', linewidth=1.5, label='Media')
    ax0.plot(xp, p3, 'r', linewidth=1.5, label='Pesada')
    ax0.set_title('Peso de la Ropa')
    ax0.legend()

    ax1.plot(xph, ph1, 'b', linewidth=1.5, label='Acido')
    ax1.plot(xph, ph2, 'g', linewidth=1.5, label='Neutro')
    ax1.plot(xph, ph3, 'r', linewidth=1.5, label='Basico')
    ax1.set_title('Nivel de pH')
    ax1.legend()

    ax2.plot(xd, d1, 'b', linewidth=1.5, label='Poco')
    ax2.plot(xd, d2, 'g', linewidth=1.5, label='Medio')
    ax2.plot(xd, d3, 'r', linewidth=1.5, label='Mucho')
    ax2.set_title('Cantidad de Detergente')
    ax2.legend()

    ax3.plot(xa, a1, 'b', linewidth=1.5, label='Poca')
    ax3.plot(xa, a2, 'g', linewidth=1.5, label='Media')
    ax3.plot(xa, a3, 'r', linewidth=1.5, label='Mucha')
    ax3.set_title('Cantidad de Agua')
    ax3.legend()

    # Turn off top/right axes
    for ax in (ax0, ax1, ax2,ax3):
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.get_xaxis().tick_bottom()
        ax.get_yaxis().tick_left()

    plt.tight_layout()
    plt.savefig('graficas/funciones de membrecia.png')
  