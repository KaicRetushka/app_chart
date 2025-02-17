import flet as ft
from flet_contrib.color_picker import ColorPicker
import pandas as pd

from to_df import mysql_to_df, postgres_to_df, file_to_df, sqlite_to_df
from build_chart import build_chart

df = pd.DataFrame()

def main(page: ft.Page):
    page.title = 'Графики'

    def clear_settings_chart():
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
            row_column.visible = False
        else:
            row_column.visible = True

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

    def change_settings_chart(df, type):
        response_build = build_chart(df=df, type=type, name_chart=input_name_chart.value,
                                             is_grid=checkbox_grid.value, grid_color=brush_grid.color,
                                             is_legend=checkbox_legend.value, label=input_legend.value,
                                             fig_color=brush_fig.color, ax_color=brush_ax.color,
                                             al_color=brush_al.color, column_color=brush_column.color,
                                             xlabel=input_a_axis.value, ylabel=input_o_axis.value)
        image_chart.src_base64 = response_build['base64_image']
        if dd_charts.value == 'Линии':
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
                    global df
                    if e.files:
                        clear_settings_chart()
                        df = file_to_df(e.files[0].path)
                        btn_add_file.text = e.files[0].name
                        response_build = build_chart(df=df, type=dd_charts.value)
                        if dd_charts.value == 'Линии':
                            dd_lines.visible = True
                            for i in range(1, response_build['count_lines'] + 1, 1):
                                dd_lines.options.append(ft.dropdown.Option(f'{i}'))
                        else:
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
                    if e.files:
                        btn_execute_sql.visible = True
                        btn_add_file.text = e.files[0].name
                        page.update()
                        def click_btn_execute_sql(path):
                            global df
                            input_name_chart.value = ''
                            execute = input_execute.value
                            response = sqlite_to_df(path, execute)
                            if response['is_can']:
                                clear_settings_chart()
                                btn_add_file.text = e.files[0].name
                                df = response['df']
                                response_build = build_chart(df=response['df'], type=dd_charts.value)
                                if dd_charts.value == 'Линии':
                                    dd_lines.visible = True
                                    for i in range(1, response_build['count_lines'] + 1, 1):
                                        dd_lines.options.append(ft.dropdown.Option(f'{i}'))
                                else:
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

    btn_add_file = ft.OutlinedButton('Добавить файл', visible=False)
    fp_add_file = ft.FilePicker()

    input_host = ft.TextField(label='host', width=200)
    input_port = ft.TextField(label='port', width=200)
    input_user = ft.TextField(label='user', width=200)
    input_password = ft.TextField(label='password', width=200)
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
            response_build = build_chart(df=response['df'], type=dd_charts.value)
            if dd_charts.value == 'Линии':
                dd_lines.visible = True
                for i in range(1, response_build['count_lines'] + 1, 1):
                    dd_lines.options.append(ft.dropdown.Option(f'{i}'))
            else:
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
    cp = ColorPicker()
    ok_cp_alert = ft.TextButton(text='ок')
    cp_alert = ft.AlertDialog(
        content=cp,
        actions=[
            ok_cp_alert,
            ft.TextButton(text='отмена', on_click=lambda e: page.close(cp_alert))
        ]
    )

    column_image = ft.Column([image_chart])
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
    input_a_axis.on_change = lambda e: change_settings_chart(df, dd_charts)
    input_o_axis = ft.TextField(label='Ось ординат', width=250, visible=False)
    input_o_axis.on_change = lambda e: change_settings_chart(df, dd_charts)
    column_left = ft.Column([input_name_chart, checkbox_grid, row_grid, checkbox_legend, input_legend, input_a_axis,
                             input_o_axis])

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

    column_right = ft.Column([row_fig, row_ax, row_al, row_column, dd_lines])
    column_settings_chart = ft.Column([ft.Row([column_left, column_image, column_right], alignment=ft.MainAxisAlignment.CENTER)],
                                      alignment=ft.MainAxisAlignment.CENTER,
                                      expand=True, visible=False
                                )
    page.add(alert, cp_alert, container_off_on_df, column_settings_df,
             column_settings_chart
             )

if __name__ == '__main__':
    ft.app(target=main)