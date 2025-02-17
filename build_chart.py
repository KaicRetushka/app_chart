import matplotlib
import matplotlib.pyplot as plt
import io
import base64
import math
matplotlib.use('Agg')

def build_chart(df, type, name_chart=None, is_grid=False, grid_color='#c2c2c2', is_legend=False, label='',
                fig_color='#ffffff', ax_color='#ffffff', al_color='#000000', column_color='#1f77b4', xlabel='',
                ylabel=''):
    count_column = df.shape[1]
    fig, ax = plt.subplots()
    fig.set_facecolor(color=fig_color)
    ax.set_facecolor(color=ax_color)
    ax.set_title(name_chart, color=al_color)
    ax.tick_params(axis='x', colors=al_color)
    ax.tick_params(axis='y', colors=al_color)
    ax.spines['bottom'].set_color(al_color)
    ax.spines['left'].set_color(al_color)
    ax.spines['top'].set_color(al_color)
    ax.spines['right'].set_color(al_color)
    if is_grid:
        ax.grid(color=grid_color)
    if type == 'Столбчатая':
        list_names = []
        list_x = []
        for i in range(count_column):
            list_names.append(df.columns[i])
            list_x.append(df[df.columns[i]][0])
        ax.bar(list_names, list_x, label=label, color=column_color)
    elif type == 'Ленточная':
        list_names = []
        list_x = []
        for i in range(count_column):
            list_names.append(df.columns[i])
            list_x.append(df[df.columns[i]][0])
        ax.barh(list_names, list_x, label=label, color=column_color)
    elif type == 'Круговая':
        list_labels = []
        list_x = []
        for i in range(count_column):
            list_labels.append(df.columns[i])
            list_x.append(df[df.columns[i]][0])
        ax.pie(list_x, labels=list_labels)
    else:
        ax.set_xlabel(xlabel, color=al_color)
        ax.set_ylabel(ylabel, color=al_color)
        for i in range(0, count_column, 2):
            if i + 1 != count_column:
                x_column = df[df.columns[i]]
                y_column = df[df.columns[i + 1]]
                ax.plot(x_column, y_column)
            else:
                y_column = df[df.columns[i]]
                ax.plot(y_column)
    if is_legend:
        ax.legend()
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    base64_image = base64.b64encode(buf.read()).decode('utf-8')
    if type == 'Линии':
        return {'base64_image': base64_image, 'count_lines': math.ceil(count_column / 2)}
    return {'base64_image': base64_image}