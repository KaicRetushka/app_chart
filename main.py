import flet as ft
from flet_contrib.color_picker import ColorPicker
import pandas as pd
import base64

from to_df import mysql_to_df, postgres_to_df, file_to_df, sqlite_to_df
from build_chart import build_chart

df = pd.DataFrame()

list_colors = []
list_labels = []

def main(page: ft.Page):
    global list_colors
    page.title = 'Графики'

    def clear_settings_chart():
        global list_colors
        global list_labels
        input_o_axis.value = ''
        input_o_axis.visible = False
        input_a_axis.value = ''
        input_a_axis.visible = False
        brush_al.color = '#000000'
        brush_ax.color = '#ffffff'
        brush_fig.color = '#ffffff'
        brush_column.color = '#1f77b4'
        brush_grid.color = '#c2c2c2'
        input_name_chart.value = ''
        input_legend.value = ''
        checkbox_grid.value = False
        checkbox_legend.value = False
        row_grid.visible = False
        input_legend.visible = False
        column_settings_chart.visible = True
        if dd_charts.value != 'Круговая':
            checkbox_grid.visible = True
        else:
            checkbox_grid.visible = False
        if dd_charts.value == 'Ленточная':
            btn_brush_column.text = 'цвет лент'
        elif dd_charts.value == 'Столбчатая':
            btn_brush_column.text = 'цвет столбцов'
        if dd_charts.value == 'Линии':
            input_a_axis.visible = True
            input_o_axis.visible = True
        if dd_charts.value == 'Столбчатая' or dd_charts.value == 'Ленточная':
            row_column.visible = True
        else:
            row_column.visible = False
        dd_lines.value = None
        row_lines.visible = False
        input_lines.visible = False
        dd_parts.value = None
        if dd_charts.value == 'Круговая':
            checkbox_pct.visible = True
        else:
            checkbox_pct.visible = False
        list_colors.clear()
        checkbox_pct.value = False
        row_pct.visible = False
        brush_pct.color = '#000000'


    def change_dd_charts():
        dd_loading_type.value = None
        dd_loading_type.visible = True
        column_settings_chart.visible = False
        btn_add_file.visible = False
        row_settings_db.visible = False
        row_execute_sql.visible = False
        page.update()

    dd_charts = ft.Dropdown(
        label='Диаграмма',
        hint_text='Выберите диаграмму',
        options=[
            ft.dropdown.Option('Столбчатая'),
            ft.dropdown.Option('Ленточная'),
            ft.dropdown.Option('Круговая'),
            ft.dropdown.Option('Линии')
        ],
        on_change= lambda e: change_dd_charts()
    )

    input_name_chart = ft.TextField(label='Название графика', width=250)

    def change_settings_chart(df, type, is_dowloand=False):
        global list_labels
        global list_colors
        if is_dowloand:
            response_build = build_chart(df=df, type=type, name_chart=input_name_chart.value,is_grid=checkbox_grid.value,
                                         grid_color=brush_grid.color, is_legend=checkbox_legend.value,
                                         label=input_legend.value, fig_color=brush_fig.color, ax_color=brush_ax.color,
                                         al_color=brush_al.color, column_color=brush_column.color,
                                         xlabel=input_a_axis.value, ylabel=input_o_axis.value, list_colors=list_colors,
                                         list_labels=list_labels, is_pct=checkbox_pct.value, color_pct=brush_pct.color,
                                         is_dowloand=True)
            return response_build['base64_image']
        else:
            response_build = build_chart(df=df, type=type, name_chart=input_name_chart.value,is_grid=checkbox_grid.value,
                                         grid_color=brush_grid.color, is_legend=checkbox_legend.value,
                                         label=input_legend.value, fig_color=brush_fig.color, ax_color=brush_ax.color,
                                         al_color=brush_al.color, column_color=brush_column.color,
                                         xlabel=input_a_axis.value, ylabel=input_o_axis.value, list_colors=list_colors,
                                         list_labels=list_labels, is_pct=checkbox_pct.value, color_pct=brush_pct.color)
        image_chart.src_base64 = response_build['base64_image']
        if not(checkbox_legend.value):
            input_lines.visible = False
        print(checkbox_legend.value and dd_lines.value is not None)
        if checkbox_legend.value and dd_lines.value is not None and dd_lines.value != '':
            # list_labels = response_build['list_labels']
            print(dd_lines.value)
            input_lines.visible = True
            print(list_labels)
            input_lines.value = list_labels[int(dd_lines.value) - 1]
        if dd_charts.value == 'Линии': # pip install odfpy
            input_a_axis.visible = True
            input_o_axis.visible = True
        else:
            input_a_axis.visible = False
            input_o_axis.visible = False
        if type != 'Круговая':
            checkbox_grid.visible = True
        else:
            checkbox_grid.visible = False
        if checkbox_grid.value:
            row_grid.visible = True
        else:
            row_grid.visible = False
        if checkbox_legend.value:
            if dd_charts.value == 'Столбчатая' or dd_charts.value == 'Ленточная':
                input_legend.visible = True
        else:
            input_legend.visible = False
            for i in range(len(list_labels)):
                list_labels[i] = ''
            input_legend.value = ''
        if checkbox_pct.value:
            print('row_pct')
            row_pct.visible = True
        else:
            row_pct.visible = False
        page.update()

    def change_dd_loading_type(value):
        input_host.value = ''
        input_port.value = ''
        input_user.value = ''
        input_password.value = ''
        input_database.value = ''
        input_execute.value = ''
        btn_add_file.text = 'Добавить файл'
        column_settings_chart.visible = False
        if value != 'файл':
            if value == 'MySQL' or value == 'postgres':
                row_settings_db.visible = True
                btn_execute_sql.visible = True
                btn_execute_sql.on_click = lambda e: click_btn_execute_sql()
            else:
                row_settings_db.visible = False
                btn_execute_sql.visible = False
            row_execute_sql.visible = True
        else:
            row_settings_db.visible = False
            row_execute_sql.visible = False
        if value == 'файл' or value == 'sqlite':
            btn_add_file.visible = True
            if value == 'файл':
                def result_fp_add_file(e):
                    global list_colors
                    global list_labels
                    global df
                    if e.files:
                        clear_settings_chart()
                        df = file_to_df(e.files[0].path)
                        btn_add_file.text = e.files[0].name
                        response_build = build_chart(df=df, type=dd_charts.value, list_labels=[])
                        if dd_charts.value == 'Линии':
                            dd_lines.visible = True
                            dd_lines.options.clear()
                            for i in range(1, response_build['count_lines'] + 1, 1):
                                dd_lines.options.append(ft.dropdown.Option(f'{i}'))
                            list_colors = response_build['list_colors']
                            list_labels = response_build['list_labels']
                            dd_parts.visible = False
                            row_parts.visible = False
                        elif dd_charts.value == 'Круговая':
                            print('a')
                            dd_parts.visible = True
                            dd_parts.options.clear()
                            for i in range(1, response_build['count_parts'] + 1, 1):
                                dd_parts.options.append(ft.dropdown.Option(f'{i}'))
                            list_colors = response_build['list_colors']
                        else:
                            row_parts.visible = False
                            dd_parts.visible = False
                            dd_lines.visible = False
                            dd_lines.options.clear()
                        image_chart.src_base64 = response_build['base64_image']
                        input_name_chart.on_change = lambda e: change_settings_chart(df, dd_charts.value)
                        checkbox_grid.on_change = lambda e: change_settings_chart(df, dd_charts.value)
                        page.update()
                fp_add_file.on_result = result_fp_add_file
                btn_add_file.on_click = lambda e: fp_add_file.pick_files(
                    allowed_extensions=['csv', 'ods', 'ots', 'sxc', 'xlsx', 'xltm', 'xltx']
                )
            else:
                def result_fp_add_file(e):
                    global list_colors
                    if e.files:
                        btn_execute_sql.visible = True
                        btn_add_file.text = e.files[0].name
                        page.update()
                        def click_btn_execute_sql(path):
                            global list_colors
                            global list_labels
                            global df
                            input_name_chart.value = ''
                            execute = input_execute.value
                            response = sqlite_to_df(path, execute)
                            if response['is_can']:
                                clear_settings_chart()
                                btn_add_file.text = e.files[0].name
                                df = response['df']
                                response_build = build_chart(df=response['df'], type=dd_charts.value, list_labels=[])
                                if dd_charts.value == 'Линии':
                                    dd_lines.visible = True
                                    dd_lines.options.clear()
                                    for i in range(1, response_build['count_lines'] + 1, 1):
                                        dd_lines.options.append(ft.dropdown.Option(f'{i}'))
                                    list_colors = response_build['list_colors']
                                    list_labels = response_build['list_labels']
                                    dd_parts.visible = False
                                    row_parts.visible = False
                                elif dd_charts.value == 'Круговая':
                                    dd_parts.visible = True
                                    dd_parts.options.clear()
                                    for i in range(1, response_build['count_parts'] + 1, 1):
                                        dd_parts.options.append(ft.dropdown.Option(f'{i}'))
                                    list_colors = response_build['list_colors']
                                else:
                                    row_parts.visible = False
                                    dd_parts.visible = False
                                    dd_lines.visible = False
                                    dd_lines.options.clear()
                                image_chart.src_base64 = response_build['base64_image']
                                input_name_chart.on_change = lambda e: change_settings_chart(response['df'],
                                                                                             dd_charts.value)
                                checkbox_grid.on_change = lambda e: change_settings_chart(response['df'],
                                                                                          type=dd_charts.value)
                            else:
                                alert.content = ft.Text(response['detail'])
                                alert.open = True
                            page.update()
                        path = e.files[0].path
                        btn_execute_sql.on_click = lambda e: click_btn_execute_sql(path)
                fp_add_file.on_result = result_fp_add_file
                btn_add_file.on_click = lambda e: fp_add_file.pick_files(
                    allowed_extensions=['db']
                )
        else:
            btn_add_file.visible = False
        page.update()

    dd_loading_type = ft.Dropdown(
        visible=False,
        label='Тип загрузки',
        hint_text='Выберите тип загрузки',
        options=[
            ft.dropdown.Option('postgres'),
            ft.dropdown.Option('MySQL'),
            ft.dropdown.Option('sqlite'),
            ft.dropdown.Option('файл')
        ],
        on_change= lambda e: change_dd_loading_type(e.control.value)
    )

    dd_lines = ft.Dropdown(
        visible=False,
        label='Линия',
        hint_text='Выберите линию'
    )
    def change_dd_lines():
        global list_colors
        global list_labels
        row_lines.visible = True
        brush_lines.color = list_colors[int(dd_lines.value) - 1]
        if checkbox_legend.value:
            input_lines.visible = True
            input_lines.value = list_labels[int(dd_lines.value) - 1]
        page.update()
    dd_lines.on_change = lambda e: change_dd_lines()
    brush_lines = ft.Icon(ft.Icons.BRUSH)
    btn_brush_lines = ft.TextButton('цвет линии')

    def click_btn_brush_lines():
        cp_alert.title = ft.Text('Выберите цвет линии')
        page.update()
        cp.color = brush_lines.color
        page.open(cp_alert)

        def click_ok_cp_alert():
            global list_colors
            global df
            brush_lines.color = cp.color
            list_colors[int(dd_lines.value) - 1] = cp.color
            page.close(cp_alert)
            change_settings_chart(df=df, type=dd_charts.value)
            page.update()

        ok_cp_alert.on_click = lambda e: click_ok_cp_alert()
        page.update()

    btn_brush_lines.on_click = lambda e: click_btn_brush_lines()
    row_lines = ft.Row([brush_lines, btn_brush_lines], visible=False)

    def change_input_lines():
        global list_labels
        list_labels[int(dd_lines.value) - 1] = input_lines.value
        change_settings_chart(df=df, type=dd_charts.value)

    input_lines = ft.TextField(visible=False, label='Подпись к легенде')
    input_lines.on_change = lambda e: change_input_lines()

    dd_parts = ft.Dropdown(
        visible=False,
        label='Часть',
        hint_text='Выберите часть'
    )

    def change_dd_parts():
        global list_colors
        row_parts.visible = True
        brush_parts.color = list_colors[int(dd_parts.value) - 1]
        page.update()

    dd_parts.on_change = lambda e: change_dd_parts()
    brush_parts = ft.Icon(ft.Icons.BRUSH)
    btn_brush_parts = ft.TextButton('цвет части')

    def click_btn_brush_parts():
        cp_alert.title = ft.Text('Выберите цвет части')
        page.update()
        cp.color = brush_parts.color
        page.open(cp_alert)

        def click_ok_cp_alert():
            global list_colors
            global df
            brush_parts.color = cp.color
            list_colors[int(dd_parts.value) - 1] = cp.color
            page.close(cp_alert)
            change_settings_chart(df=df, type=dd_charts.value)
            page.update()

        ok_cp_alert.on_click = lambda e: click_ok_cp_alert()
        page.update()

    btn_brush_parts.on_click = lambda e: click_btn_brush_parts()
    row_parts = ft.Row([brush_parts, btn_brush_parts], visible=False)

    btn_add_file = ft.OutlinedButton('Добавить файл', visible=False)
    fp_add_file = ft.FilePicker()

    input_host = ft.TextField(label='host', width=200)
    input_port = ft.TextField(label='port', width=200)
    input_user = ft.TextField(label='user', width=200)
    input_password = ft.TextField(label='password', width=200, password=True, can_reveal_password=True)
    input_database = ft.TextField(label='database', width=200)
    row_settings_db = ft.Row([
        input_host,
        input_port,
        input_user,
        input_password,
        input_database
    ], visible=False)
    input_execute = ft.TextField(label='Запрос sql', width=830)

    def close_alert():
        alert.open = False
        page.update()

    alert = ft.AlertDialog(
        actions=[
            ft.TextButton('ok', on_click=lambda e: close_alert())
        ]
    )

    def click_btn_execute_sql():
        global list_colors
        global list_labels
        global base64_image
        global df
        input_name_chart.value = ''
        if dd_loading_type.value != 'файл' and dd_loading_type.value != 'sqlite':
            execute = input_execute.value
            host = input_host.value
            port = input_port.value
            user = input_user.value
            password = input_password.value
            database = input_database.value
        if dd_loading_type.value == 'MySQL':
            response = mysql_to_df(execute, host, port, user, password, database)
        elif dd_loading_type.value == 'postgres':
            response = postgres_to_df(execute, host, port, user, password, database)
        if response['is_can'] == False:
            alert.content = ft.Text(response['detail'])
            alert.open = True
        else:
            clear_settings_chart()
            df = response['df']
            response_build = build_chart(df=response['df'], type=dd_charts.value, list_labels=[])
            if dd_charts.value == 'Линии':
                dd_lines.visible = True
                dd_lines.options.clear()
                for i in range(1, response_build['count_lines'] + 1, 1):
                    dd_lines.options.append(ft.dropdown.Option(f'{i}'))
                list_colors = response_build['list_colors']
                list_labels = response_build['list_labels']
                dd_parts.visible = False
                row_parts.visible = False
            elif dd_charts.value == 'Круговая':
                dd_parts.visible = True
                dd_parts.options.clear()
                for i in range(1, response_build['count_parts'] + 1, 1):
                    dd_parts.options.append(ft.dropdown.Option(f'{i}'))
                list_colors = response_build['list_colors']
            else:
                row_parts.visible = False
                dd_parts.visible = False
                dd_lines.visible = False
                dd_lines.options.clear()
            image_chart.src_base64 = response_build['base64_image']
            input_name_chart.on_change = lambda e: change_settings_chart(response['df'], type=dd_charts.value)
            checkbox_grid.on_change = lambda e: change_settings_chart(response['df'], type=dd_charts.value)

        page.update()

    btn_execute_sql = ft.OutlinedButton(text='Отправить', on_click=lambda e: click_btn_execute_sql(), visible=False)
    row_execute_sql = ft.Row([
        input_execute,
        btn_execute_sql
    ], visible=False)
    column_settings_df = ft.Column([
        ft.Row([dd_charts, dd_loading_type, btn_add_file, fp_add_file]),
        row_settings_db,
        row_execute_sql
    ])
    btn_off_on_df = ft.IconButton(icon=ft.Icons.ARROW_DROP_DOWN)
    container_off_on_df = ft.Container(
        content=ft.Row(
            [ft.Text('Выбор данных', weight=ft.FontWeight.BOLD), btn_off_on_df],
            width=1040,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        ),
        border = ft.Border(bottom=ft.BorderSide(2))
    )

    def click_btn_off_on_df():
        if column_settings_df.visible:
            column_settings_df.visible = False
            btn_off_on_df.icon = ft.Icons.ARROW_DROP_UP
        else:
            column_settings_df.visible = True
            btn_off_on_df.icon = ft.Icons.ARROW_DROP_DOWN
        page.update()

    image_chart = ft.Image()
    image_chart_container = ft.Container(
        content=image_chart,
        border=ft.border.all(5)
    )
    cp = ColorPicker()
    ok_cp_alert = ft.TextButton(text='ок')
    cp_alert = ft.AlertDialog(
        content=cp,
        actions=[
            ok_cp_alert,
            ft.TextButton(text='отмена', on_click=lambda e: page.close(cp_alert))
        ]
    )
    btn_dowloand = ft.IconButton(ft.Icons.DOWNLOAD)
    fp_dowloand = ft.FilePicker()

    def save_image(path_file, base64_image):
        if path_file != None:
            with open(path_file, 'wb') as file:
                file.write(base64.b64decode(base64_image))

    def click_btn_dowloand(e):
        fp_dowloand.on_result = lambda e: save_image(e.path, change_settings_chart(df, dd_charts.value, True))
        fp_dowloand.save_file(file_name='graf.png')

    btn_dowloand.on_click = click_btn_dowloand

    column_image = ft.Column([image_chart_container, fp_dowloand, btn_dowloand])
    btn_off_on_df.on_click = lambda e: click_btn_off_on_df()

    checkbox_grid = ft.Checkbox('Сетка')
    brush_grid = ft.Icon(ft.Icons.BRUSH, color='#c2c2c2')
    btn_brush_grid = ft.TextButton('цвет сетки')
    def click_btn_brush_grid():
        cp_alert.title = ft.Text('Выберите цвет сетки')
        page.update()
        cp.color = brush_grid.color
        page.open(cp_alert)

        def click_ok_cp_alert():
            global df
            brush_grid.color = cp.color
            page.close(cp_alert)
            change_settings_chart(df=df, type=dd_charts.value)
            page.update()

        ok_cp_alert.on_click = lambda e: click_ok_cp_alert()
        page.update()
    btn_brush_grid.on_click = lambda e: click_btn_brush_grid()
    row_grid = ft.Row([brush_grid, btn_brush_grid], visible=False)

    checkbox_legend = ft.Checkbox('Легенда')
    input_legend = ft.TextField(label='Текст легенды', visible=False, width=250)
    checkbox_legend.on_change = lambda e: change_settings_chart(df, dd_charts.value)
    input_legend.on_change = lambda e: change_settings_chart(df, dd_charts.value)
    input_a_axis = ft.TextField(label='Ось абцисс', width=250, visible=False)
    input_a_axis.on_change = lambda e: change_settings_chart(df, dd_charts.value)
    input_o_axis = ft.TextField(label='Ось ординат', width=250, visible=False)
    input_o_axis.on_change = lambda e: change_settings_chart(df, dd_charts.value)

    checkbox_pct = ft.Checkbox('Проценты', visible=False)
    checkbox_pct.on_change = lambda e: change_settings_chart(df, dd_charts.value)
    brush_pct = ft.Icon(ft.Icons.BRUSH, color='#000000')
    btn_brush_pct = ft.TextButton('цвет процентов')

    def click_btn_brush_pct():
        cp_alert.title = ft.Text('Выберите цвет процентов')
        page.update()
        cp.color = brush_pct.color
        page.open(cp_alert)

        def click_ok_cp_alert():
            global df
            brush_pct.color = cp.color
            page.close(cp_alert)
            change_settings_chart(df=df, type=dd_charts.value)
            page.update()

        ok_cp_alert.on_click = lambda e: click_ok_cp_alert()
        page.update()

    btn_brush_pct.on_click = lambda e: click_btn_brush_pct()
    row_pct = ft.Row([brush_pct, btn_brush_pct], visible=False)

    column_left = ft.Column([input_name_chart, checkbox_grid, row_grid, checkbox_legend, input_legend, input_a_axis,
                             input_o_axis, row_pct, checkbox_pct, row_pct])

    brush_fig = ft.Icon(ft.Icons.BRUSH, color='#ffffff')
    btn_brush_fig = ft.TextButton('цвет внешнего фона')
    def click_btn_brush_fig():
        cp_alert.title = ft.Text('Выберите цвет внешнего фона')
        page.update()
        cp.color = brush_fig.color
        page.open(cp_alert)

        def click_ok_cp_alert():
            global df
            brush_fig.color = cp.color
            page.close(cp_alert)
            change_settings_chart(df=df, type=dd_charts.value)
            page.update()

        ok_cp_alert.on_click = lambda e: click_ok_cp_alert()
        page.update()
    btn_brush_fig.on_click = lambda e: click_btn_brush_fig()
    row_fig = ft.Row([brush_fig, btn_brush_fig])

    brush_ax = ft.Icon(ft.Icons.BRUSH, color='#ffffff')
    btn_brush_ax = ft.TextButton('цвет внутреннего фона')
    def click_btn_brush_ax():
        cp_alert.title = ft.Text('Выберите цвет внутреннего фона')
        page.update()
        cp.color = brush_ax.color
        page.open(cp_alert)

        def click_ok_cp_alert():
            global df
            brush_ax.color = cp.color
            page.close(cp_alert)
            change_settings_chart(df=df, type=dd_charts.value)
            page.update()

        ok_cp_alert.on_click = lambda e: click_ok_cp_alert()
        page.update()
    btn_brush_ax.on_click = lambda e: click_btn_brush_ax()
    row_ax = ft.Row([brush_ax, btn_brush_ax])

    brush_al = ft.Icon(ft.Icons.BRUSH, color='#000000')
    btn_brush_al = ft.TextButton('цвет осей и подписей')
    def click_btn_brush_al():
        cp_alert.title = ft.Text('Выберите цвет осей и подписей')
        page.update()
        cp.color = brush_al.color
        page.open(cp_alert)

        def click_ok_cp_alert():
            global df
            brush_al.color = cp.color
            page.close(cp_alert)
            change_settings_chart(df=df, type=dd_charts.value)
            page.update()

        ok_cp_alert.on_click = lambda e: click_ok_cp_alert()
        page.update()
    btn_brush_al.on_click = lambda e: click_btn_brush_al()
    row_al = ft.Row([brush_al, btn_brush_al])

    brush_column = ft.Icon(ft.Icons.BRUSH, color='#1f77b4')
    btn_brush_column = ft.TextButton('цвет столбцов')
    def click_btn_brush_column():
        cp_alert.title = ft.Text(f'Выберите {btn_brush_column.text}')
        page.update()
        cp.color = brush_column.color
        page.open(cp_alert)

        def click_ok_cp_alert():
            global df
            brush_column.color = cp.color
            page.close(cp_alert)
            change_settings_chart(df=df, type=dd_charts.value)
            page.update()

        ok_cp_alert.on_click = lambda e: click_ok_cp_alert()
        page.update()
    btn_brush_column.on_click = lambda e: click_btn_brush_column()
    row_column = ft.Row([brush_column, btn_brush_column])

    column_right = ft.Column([row_fig, row_ax, row_al, row_column, dd_lines, row_lines, input_lines, dd_parts, row_parts])
    column_settings_chart = ft.Column([ft.Row([column_left, column_image, column_right], alignment=ft.MainAxisAlignment.CENTER)],
                                      alignment=ft.MainAxisAlignment.CENTER,
                                      expand=True, visible=False
                                      )
    page.add(alert, cp_alert, container_off_on_df, column_settings_df,
             column_settings_chart
             )

if __name__ == '__main__':
    ft.app(target=main)