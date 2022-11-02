import pandas as pd
import matplotlib.pyplot as plt
import datetime
import numpy as np
import panel as pn
pn.extension('tabulator')
import hvplot.pandas

df = pd.read_csv("forFBpost.csv",sep=';')
df['Относительный прирост %']=(df['Модель'].pct_change()*100).round(decimals = 2)
df.loc[df.Город.shift(1)!=df.Город, 'Относительный прирост %']=np.nan
df.loc[ df['Город'] == 1, 'Относительный прирост %'] = np.nan

help_df = df[df['fact'] > 1]
help_df = help_df[help_df['Модель'] > 100000]
help_df['Погрешность модели %']=(help_df['Модель']-help_df['fact']).abs()/help_df['Модель']*100

idf = df.interactive()
year_slider = pn.widgets.IntSlider(name='Слайдер по годам', start=df['year'].min(), end=df['year'].max(), step=1, value=datetime.date.today().year)

yaxis_pop = pn.widgets.RadioButtonGroup(
    name='Y axis',
    options=['Модель', 'fact',],
    button_type='success'
)

pop_pipeline = (
    idf[
        (idf.year <= year_slider) &
        (idf.Модель >=600000)
    ]
    .groupby(['Город','year'])[yaxis_pop].mean()
    .to_frame()
    .reset_index()
    .sort_values(by='year')
    .reset_index(drop=True)
)

pop_plot = pop_pipeline.hvplot(x='year',by='Город', y=yaxis_pop, line_width=2, title='Население по годам')

pop_table = pop_pipeline.pipe(pn.widgets.Tabulator, pagination='remote', page_size = 10, sizing_mode='stretch_width')

help_of_help_df = help_df[help_df['Погрешность модели %'] > 5]
help_of_help_df_plot = help_of_help_df.hvplot.heatmap(y='year', x='Город', C='Погрешность модели %',
                  height=300, width=1000, colorbar=True, title='Погрешность модели %')

rslt_df = df[df['Относительный прирост %'] > 3]
rslt_df = rslt_df[rslt_df['Относительный прирост %'] < 100]
rslt_df = rslt_df[rslt_df['Модель'] > 100000]
pop_heat = rslt_df.hvplot.heatmap(y='year', x='Город', C='Относительный прирост %',
                  height=300, width=1000, colorbar=True, title='Относительный прирост% > 100 тыс.')

template = pn.template.FastListTemplate(
    title='Количество населения российских городов',
    sidebar = [pn.pane.Markdown('####Население российских городов и социально-экономические выводы'),
               pn.pane.Markdown('''Динамика численности населения характеризует экономическую привлекательность города, и его социальные перспективы. Как мы видим из нашей инфографики модель вполне адекватно описывает численность населения городов в прошлом, и ближайшем будующем. В более отдаленное время модель едва ли способна адекватно предсказать численность населения, в виду самых разных неучтенных факторов, которые могут критически изменять численность населения в отдельных городах.
Мы можем видеть, что в крупных городах все так же продолжается рост населения, на фоне убыли населения в целом, хоть и снижается со временем. В некоторых городах юга происходит более активный рост населения, что позволяет предположить уверенный рост цен на недвижимость и сопутствующие услуги'''),
               pn.pane.Markdown('## Настройки'),
               year_slider],
    main=[pn.Row(pn.Column(yaxis_pop, pop_plot.panel(width=700), margin=(0,25)), pop_table.panel(width=500)),
          pn.Row(pn.Column(help_of_help_df_plot, pop_heat))],
    accent_base_color='88d8b0',
    header_background='88d8b0',
)
template.servable();

