import matplotlib
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import io
import base64
import math
matplotlib.use('Agg')

def build_chart(df, type, name_chart=None, is_grid=False, grid_color='#c2c2c2', is_legend=False, label='',
                fig_color='#ffffff', ax_color='#ffffff', al_color='#000000', column_color='#1f77b4', xlabel='',
                ylabel='', list_colors=[], list_labels=[], is_pct=False, color_pct=None, is_dowloand=False):
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
        if is_legend:
            ax.legend()
    elif type == 'Ленточная':
        list_names = []
        list_x = []
        for i in range(count_column):
            list_names.append(df.columns[i])
            list_x.append(df[df.columns[i]][0])
        ax.barh(list_names, list_x, label=label, color=column_color)
        if is_legend:
            ax.legend()
    elif type == 'Круговая':
        list_labels = []
        list_x = []
        for i in range(count_column):
            list_labels.append(df.columns[i])
            list_x.append(df[df.columns[i]][0])
        if len(list_colors) == count_column:
            if is_pct:
                wedges, texts, autotexts = ax.pie(list_x, labels=list_labels, colors=list_colors, autopct='%1.1f%%')
            else:
                ax.pie(list_x, labels=list_labels, colors=list_colors)
        else:
            if is_pct:
                wedges, texts, autotexts = ax.pie(list_x, labels=list_labels, autopct='%1.1f%%')
            else:
                wedges, texts = ax.pie(list_x, labels=list_labels)
            list_colors = [mcolors.to_hex(wedge.get_facecolor()) for wedge in wedges]
        if is_pct:
            for autotext in autotexts:
                autotext.set_color(color_pct)
        if is_legend:
            ax.legend()
    else:
        ax.set_xlabel(xlabel, color=al_color)
        ax.set_ylabel(ylabel, color=al_color)
        count_line = 0
        for i in range(0, count_column, 2):
            if i + 1 != count_column:
                x_column = df[df.columns[i]]
                y_column = df[df.columns[i + 1]]
                if len(list_colors) == math.ceil(count_column / 2):
                    ax.plot(x_column, y_column, color=list_colors[count_line])
                else:
                    line = ax.plot(x_column, y_column)
                    list_colors.append(line[0].get_color())
                    list_labels.append('')
            else:
                y_column = df[df.columns[i]]
                if len(list_colors) == math.ceil(count_column / 2):
                    ax.plot(y_column, color=list_colors[count_line])
                else:
                    line = ax.plot(y_column)
                    list_colors.append(line[0].get_color())
                    list_labels.append('')
            count_line += 1
            print(list_labels)
            if is_legend:
                ax.legend(labels=list_labels)
    buf = io.BytesIO()
    if is_dowloand:
        fig.savefig(buf, format='png', dpi=300)
    else:
        fig.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    base64_image = base64.b64encode(buf.read()).decode('utf-8')
    if type == 'Линии':
        return {'base64_image': base64_image, 'count_lines': math.ceil(count_column / 2), 'list_colors': list_colors,
                'list_labels': list_labels}
    elif type == 'Круговая':
        return {'base64_image': base64_image, 'list_colors': list_colors, 'count_parts': count_column}
    return {'base64_image': base64_image}