import dash
# import dash_core_components as dcc
from dash import dcc
import dash_bootstrap_components as dbc
# import dash_html_components as html
from dash import html
from dash.exceptions import PreventUpdate
from dash.dependencies import Input,Output,State
import plotly.graph_objs as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
import json
from numpy import random
from dash_bootstrap_templates import load_figure_template
import dash_daq as daq
from datetime import datetime
load_figure_template(["superhero"])



def blank_fig():
    fig = go.Figure(go.Scatter(x=[], y = []))
    fig.update_layout(template = "superhero")
    fig.update_xaxes(showgrid = False, showticklabels = False, zeroline=False)
    fig.update_yaxes(showgrid = False, showticklabels = False, zeroline=False)
    
    return fig



x = np.random.sample(100)
y = np.random.sample(100)
z = np.random.choice(a = ['a','b','c'], size = 100)


df1x = pd.DataFrame({'x': x, 'y':y, 'z':z}, index = range(100))

# fig1 = px.scatter(df1, x= x, y = y, color = z,template='superhero')
fig1 = px.scatter(df1x, x= x, y = y, color = z)



def logo(app):
    title = html.H5(
        "EDITAIS INOVA EM NÚMEROS",
        style={"marginTop": 5, "marginLeft": "10px"},
    )

    info_about_app = html.H6(
        "Este Dashboard está destinado apresentar resultados e estatísticas dos editais"
        " Os resultados são apresentados interativamente baseado na aplicação de filtros.",
        style={"marginLeft": "10px"},
    )

    logo_image = html.Img(
        src=app.get_asset_url("logo_INOVA2.png"), style={"float": "right", "height": 50,'marginTop':5}
    )
    link = html.A(logo_image, href="https://plotly.com/dash/")

    return dbc.Row(
        [dbc.Col([dbc.Row([title]), dbc.Row([info_about_app])]), dbc.Col(link)]
    )

# ------------------------------- TRANSFORMAÇÃO DE JSON PARA DATAFRAME ----------------------------#
# *************************************************************************************************#
import json
# Natalia
# f = open('D:/Users/arquivos_nathalia/Documents/INOVA_FioCruz/projetos-inova-jan-2023/projetos-inova-jan-2023.json')

#Nayher
# f = open('C:/Users/nacla/Downloads/Innova/projetos-innova-Junho23.json')
# f = open('C:/Users/nacla/Downloads/Innova/projetos-innova-Junho23.json')
# f = open('C:/Users/nacla/Downloads/Innova/projetos-innova-Julho23.json')

# Marcel
# f = open('G:\.shortcut-targets-by-id/17VwseeFoNRQuVF9viXYxvir2WWNhCOGG/Innova/projetos-inova-jan-2023.json')
# f = open('G:\.shortcut-targets-by-id/17VwseeFoNRQuVF9viXYxvir2WWNhCOGG/Innova/projetos-innova-Julho23.json')
f = open('data/projetos-innova-Julho23.json')
data = json.load(f)

li = []
for i in range(len(data['hits']['hits'])):
    li.append(pd.Series(data['hits']['hits'][i]['_source']))

df_completo = pd.DataFrame(li)

# ------------------------------- PRETRATAMENTO ----------------------------#
# **************************************************************************#

print(df_completo['field_rodada_produtos:name'].unique())
df1 = df_completo[df_completo['field_rodada_produtos:name']=='1ª Rodada']
df2 = df_completo[df_completo['field_rodada_produtos:name']=='2ª Rodada']
df3 = df_completo[df_completo['field_rodada_produtos:name']=='3ª Rodada']
df4 = df_completo[df_completo['field_rodada_produtos:name']=='4ª Rodada']
dfn = df_completo[(df_completo['field_rodada_produtos:name'] != '1ª Rodada') & (df_completo['field_rodada_produtos:name'] != '2ª Rodada') & (df_completo['field_rodada_produtos:name'] != '3ª Rodada')& (df_completo['field_rodada_produtos:name'] != '4ª Rodada')]

# ----- Atualizacoes pontuais antes da geral ----
df_completo['field_rodada_produtos:name'] = np.where((df_completo['field_edital_de_referencia:title'].isin(['Geração de Conhecimento (2021)','Novos Talentos (2021)'])),'2ª Rodada',df_completo['field_rodada_produtos:name'])
df_completo['field_edital_de_referencia:title'] = np.where((df_completo['field_edital_de_referencia:title'].isin(['Geração de Conhecimento (2021)'])),'Geração de Conhecimento',df_completo['field_edital_de_referencia:title'])
df_completo['field_edital_de_referencia:title'] = np.where((df_completo['field_edital_de_referencia:title'].isin(['Novos Talentos (2021)'])),'Novos Talentos',df_completo['field_edital_de_referencia:title'])

# Nao precisa, ja vem na base corretamente
df_completo['field_rodada_produtos:name'] = np.where((df_completo['field_edital_de_referencia:title'].isin(['Ideias Inovadoras (2022)'])),'2ª Rodada',df_completo['field_rodada_produtos:name'])
df_completo['field_edital_de_referencia:title'] = np.where((df_completo['field_edital_de_referencia:title'].isin(['Ideias Inovadoras (2022)'])),'Ideias Inovadoras',df_completo['field_edital_de_referencia:title'])

# Rever se 'Produtos Inovadores (2022)' é 4 rodada ou 3 rodada como vem da base.
df_completo['field_rodada_produtos:name'] = np.where((df_completo['field_edital_de_referencia:title'].isin(['Produtos Inovadores (2022)'])),'4ª Rodada',df_completo['field_rodada_produtos:name'])
df_completo['field_edital_de_referencia:title'] = np.where((df_completo['field_edital_de_referencia:title'].isin(['Produtos Inovadores (2022)'])),'Produtos Inovadores',df_completo['field_edital_de_referencia:title'])



df_completo.drop(df_completo[df_completo['field_edital_de_referencia:title'].isin(['Edital Vacinas Sars-CoV-2','Animais Peçonhentos'])].index,inplace=True)

"""
# Subtitute class None por Indefindo
df_completo['field_rodada_produtos:name'] = np.where(
   (df_completo['field_rodada_produtos:name'] != '1ª Rodada') & (df_completo['field_rodada_produtos:name'] != '2ª Rodada') & (df_completo['field_rodada_produtos:name'] != '3ª Rodada'), 'Indefinido', df_completo['field_rodada_produtos:name']
   )
"""

# Subtitute class None por 1 rodada
df_completo['field_rodada_produtos:name'] = np.where(
   (df_completo['field_rodada_produtos:name'] != '1ª Rodada') & (df_completo['field_rodada_produtos:name'] != '2ª Rodada') & (df_completo['field_rodada_produtos:name'] != '3ª Rodada') & (df_completo['field_rodada_produtos:name'] != '4ª Rodada'), 
   '1ª Rodada', df_completo['field_rodada_produtos:name'])

# Subtitute approval situation name
df_completo['field_situacao'] = np.where((df_completo['field_situacao']=='aprovado Recomendado'),'Recomendado',df_completo['field_situacao'])
df_completo['field_situacao'] = np.where((df_completo['field_situacao']=='reprovado Não recomendado'),'Não recomendado',df_completo['field_situacao'])
df_completo['field_situacao'] = np.where((df_completo['field_situacao']=='ajustes Recomendado com ajustes'),'Recomendado com ajustes',df_completo['field_situacao'])
df_completo['field_situacao'] = np.where((df_completo['field_situacao']=='submetido Submetido'),'Submetido',df_completo['field_situacao'])
df_completo['field_situacao'] = np.where((df_completo['field_situacao']=='rascunho Rascunho'),'Rascunho',df_completo['field_situacao'])
df_completo['field_situacao'] = np.where((df_completo['field_situacao']=='desistencia Desistência'),'Desistência',df_completo['field_situacao'])

#Read date format and creating a new column created_year
df_completo['ano_creacao'] = [datetime.fromtimestamp(int(timestamp)).year for timestamp in df_completo['created'] ]

# Pie chart, where the slices will be ordered and plotted counter-clockwise:
labels = list(df_completo['field_rodada_produtos:name'].unique())
sizes=[df_completo[df_completo['field_rodada_produtos:name']==i].shape[0] for i in labels]
min_val = min(sizes)
min_index = sizes.index(min_val)
explode= tuple([0 if i!=min_index else 0.2 for i in range(len(sizes))])

Eixo1 = ['Novos Talentos', 'Geração de Conhecimento', 'Produtos Inovadores', 'Produtos Inovadores (2022)'
       'Ideias Inovadoras','Ideias Inovadoras (2022)', 'Geração de Conhecimento (2021)','Novos Talentos (2021)']
Eixo2 = ['Covid-19', 'Covid-19 (Geração)','Equipamentos Inova','PMA',
         'Territórios Sustentáveis e Saudáveis','Saúde Indígena','Emergências em Saúde Pública','Inova Gestão',
         'Inovação na Amazônia','Inova IOC', 'PROEP IAM', 'COVID-19-longa', 'Pesquisa Clínica', 'Inova Educação' ]
Eixo3 = ['Pós-Doutorado Júnior','Inova Labs']

eixos_nomes = ['1: Institucional e cadeia produtiva', '2: Encomendas especiais',
                '3: Redes e capacitação', '4: Desenvolvimento']




# adicionando coluna de Eixos para cada edital
df_completo['Eixo'] = np.nan
df_completo['Eixo'] = np.where((df_completo['field_edital_de_referencia:title'].isin(Eixo1)),eixos_nomes[0],df_completo['Eixo'])
df_completo['Eixo'] = np.where((df_completo['field_edital_de_referencia:title'].isin(Eixo2)),eixos_nomes[1],df_completo['Eixo'])
df_completo['Eixo'] = np.where((df_completo['field_edital_de_referencia:title'].isin(Eixo3)),eixos_nomes[2],df_completo['Eixo'])
df_completo['Eixo'] = np.where((~df_completo['field_edital_de_referencia:title'].isin(Eixo1+Eixo2+Eixo3)),eixos_nomes[3],df_completo['Eixo'])

df_completo['field_unidade_da_fiocruz:name'] = np.where((df_completo['field_unidade_da_fiocruz:name'].isin([None])),'N/A',df_completo['field_unidade_da_fiocruz:name'])
group_presidencia = ['Vice-Presidência de Ensino, Informação e Comunicação (VPEIC)','Vice-Presidência de Ambiente, Atenção e Promoção da Saúde (VPAAPS)',
                     'Vice-Presidência de Pesquisa e Coleções Biológicas (VPPCB)', 'Vice-Presidência de Gestão e Desenvolvimento Institucional (VPGDI)',
                     'Vice-Presidência de Produção e Inovação em Saúde (VPPIS)','Presidência']
df_completo['field_unidade_da_fiocruz:name'] = np.where((df_completo['field_unidade_da_fiocruz:name'].isin(group_presidencia)),'Presidência', df_completo['field_unidade_da_fiocruz:name'])

unidades_drop = ['Coordenação da Qualidade (CQuali)','Coordenação de Comunicação Social (CCS)',
                 'Coordenação de Gestão Tecnológica (Gestec)','Coordenação de Gestão de Tecnologia de Informação (Cogetic)',
                 'Coordenação-geral de Infraestrutura dos Campi (Cogic)']
df_completo.drop(df_completo[df_completo['field_unidade_da_fiocruz:name'].isin(unidades_drop)].index,inplace=True)



df_completo['field_total_de_recursos'] = df_completo['field_total_de_recursos'].astype(float)
df_completo['field_orcamento_final'] = df_completo['field_orcamento_final'].astype(float)

# ------------------------------- FUNÇÕES PARA CARDS ----------------------------#
# *******************************************************************************#

def pessoas_equipe(df_completo):
    Lg =[]
    for i in range(df_completo.shape[0]):
        li = df_completo.iloc[i]['field_equipe_do_projeto:field_nome_equipe']
        for j in li:
            Lg.append(j)
    return len(Lg)

def coordenadores(df_completo):
    lio = set(df_completo['field_nome_coordenador'].unique())
    return len(lio)

def bolsistas(df_completo):
    Lb =[]
    for i in range(df_completo.shape[0]):
        li = df_completo.iloc[i]['field_equipe_do_projeto:field_vinculo_institucional']
        for j in li:
            if j =='bolsista Bolsista':
                Lb.append([j,i])
    return (len(Lb))


df_completo['id_dummy'] = df_completo['id']
gk5 = df_completo.groupby(['Eixo','field_edital_de_referencia:title','field_rodada_produtos:name'], as_index=False)['id_dummy'].count()

lista_rodadas =list(gk5['field_rodada_produtos:name'].unique())


def figure2():
    fig2 = go.Figure(
    px.bar(gk5, x="id_dummy", y='field_edital_de_referencia:title', color='field_rodada_produtos:name', text_auto=True))
    fig2.update_traces(textfont_size=8, textangle=0, textposition="outside", cliponaxis=False)
    fig2.update_layout(yaxis_title=None,xaxis_title=None)
    fig2.update_layout(
        margin=dict(l=5, r=5, t=5, b=5),
        title='',
        xaxis_tickfont_size=10,
        yaxis=dict(
            showgrid=False,
            showline=False,
            showticklabels=True,
            title='',
            titlefont_size=1,
            tickfont_size=9,
        ),
        xaxis=dict(
            zeroline=False,
            showline=False,
            showticklabels=True,
            showgrid=True
        ),
        legend_title_text='',
        legend=dict(font_size=9,orientation="h",
        yanchor="bottom",
        y=1.01,
        xanchor="right",
        x=1)
        )

    # fig2.update_traces(
    #                  hovertemplate = "Eixo:%{label}: <br>Porcentagem : %{customdata:.2f}% </br>N° Submissões: %{value}"
    # )

    fig2.update_traces(hovertemplate=
                    '<b></b>%{y}' +
                    '<br><b>N° Submissões</b>: %{x}<br>')

    return fig2

df_completo['N° Submissões'] = df_completo['id']
gk3 = df_completo.groupby(['Eixo'], as_index=False)['N° Submissões'].count()
gk3['percentage'] = 100*gk3['N° Submissões']/gk3['N° Submissões'].sum()


# fig3 = go.Figure(
# px.pie(gk3, values='N° Submissões',names='Eixo',title='Editais por Eixo'))
def figure3():
    fig3 = go.Figure(data=[go.Pie(labels=gk3['Eixo'],
                                values=gk3['N° Submissões'],
                                name='',
                                customdata=gk3['percentage'])])
    # fig3.update_traces(hoverinfo='label+percent', textinfo='value')
    fig3.update_traces(textposition='inside', textinfo='value',\
                    hovertemplate = "Eixo:%{label}: <br>Porcentagem : %{customdata:.2f}% </br>N° Submissões: %{value}"
    )

    fig3.update_layout(legend = dict(font = dict(size = 16),
            bgcolor="#20374c",
            bordercolor="White",
            borderwidth=0.5),
                    legend_title = dict(font = dict(size = 15)))


    fig3.update_layout(
        title={
            'text': 'EDITAIS por Eixo',
            # 'y':0.9,
            # 'x':0.5,
            'xanchor': 'left',
            'yanchor': 'top',
            'font': {'size': 16}},
        legend_title_text='Eixos',
        margin= {"t": 2, "r": 2, "b": 2, "l": 2},
        plot_bgcolor= "#20374c",
        paper_bgcolor= "#20374c",
        font= {"color": "white"}
    )
    return fig3
# fig2.update_layout(legend_orientation="h")

# fig2.update_yaxes( # the y-axis is in dollars
#     tickprefix="$", showgrid=True
# )



df1_completo = df_completo[df_completo['field_situacao'].isin(['Recomendado','Não recomendado','Recomendado com ajustes'])]
df2_completo = df_completo[df_completo['field_situacao'].isin(['Submetido','Rascunho','Desistência'])]
gk4_a = df1_completo.groupby(['field_situacao'], as_index=False)['N° Submissões'].count()
gk4_b = df2_completo.groupby(['field_situacao'], as_index=False)['N° Submissões'].count()

gk4_a['percentage'] = 100*gk4_a['N° Submissões']/gk4_a['N° Submissões'].sum()
gk4_b['percentage'] = 100*gk4_b['N° Submissões']/gk4_b['N° Submissões'].sum()
def figure4():
    # Create subplots: use 'domain' type for Pie subplot
    fig4 = make_subplots(rows=1, cols=2, specs=[[{'type':'domain'}, {'type':'domain'}]])
    fig4.add_trace(go.Pie(labels=gk4_a['field_situacao'], values=gk4_a['N° Submissões'],customdata=gk4_a['percentage'],name="Status A"),
                1, 1)
    fig4.add_trace(go.Pie(labels=gk4_b['field_situacao'], values=gk4_b['N° Submissões'],customdata=gk4_b['percentage'], name="Status B"),
                1, 2)

    # Use `hole` to create a donut-like pie chart
    # fig4.update_traces(hole=.4, hoverinfo="label+percent+name")
    # fig4.update_traces(hole=.4, textposition='inside', textinfo='percent',\
    #                     hovertemplate = "Status: %{label} <br>N° Submissões: %{value}"
    #     )
    
    fig4.update_traces(hole=.4,textposition='inside', textinfo='value',\
                    hovertemplate = "Status:%{label}: <br>Porcentagem : %{customdata:.2f}% </br>N° Submissões: %{value}"
    )

    fig4.update_layout(
            title='',
            margin=dict(l=5, r=5, t=5, b=5),
            legend_title_text='Status',
            legend = dict(orientation = 'h', 
                xanchor = "left", 
                x = 0.04, y= 1.11,
                font_size=10,
                # bgcolor="#20374c",
                bordercolor="White",
                borderwidth=0.5)
 
        )
    return fig4

field_situacao_set = ['Recomendado','Recomendado com ajustes']
df_c = df_completo[(df_completo['field_situacao'].isin(field_situacao_set))]
gk6 = df_c.groupby(['field_unidade_da_fiocruz:name']).agg({'field_total_de_recursos': 'sum', 'id': 'count'})
# gk6 = df_c.groupby(['field_unidade_da_fiocruz:name']).agg({'field_orcamento_final': 'sum', 'id': 'count'})

# gk6 = gk6.sort_values(by=['field_total_de_recursos'],ascending=False)
gk6 = gk6.sort_values(by=['id'],ascending=False)
fig=make_subplots(specs=[[{"secondary_y":True}]])

with open('data/ShortNames_FioCruz2.json') as json_file:
    ShortNames_Fiocruz = json.load(json_file)

def figure7():
    fig.add_trace(                           #Add a bar chart to the figure
            go.Bar(
            x=gk6.index,
            y=gk6['id'],
            name="Número de Projetos",
            hoverinfo='none' ,               #Hide the hoverinfo
            marker_color='#ef6790',#'#f0497b',#'#f27097',     
            ),
            secondary_y=False)               #The bar chart uses the primary y-axis 

    fig.add_trace(                           #Add the second chart (line chart) to the figure
        go.Scatter(
        x=gk6.index,
        y=gk6['field_total_de_recursos'],
        name="Total de recursos (BRL)",
        mode='lines+markers',
        text= list(ShortNames_Fiocruz.keys()),
        customdata = gk6['id'],
        hovertemplate=
        "<b>%{text}</b><br><br>" +
        "Total de recursos (BRL): %{y:$,.0f}<br>" +
        "N° de projetos: %{customdata:.0f}<br>" +
        "<extra></extra>",
        # text=df['text'],               
        # hoverinfo='text',                   #Pass the 'text' column to the hoverinfo parameter to customize the tooltip
        line = dict(color='#3ff698', width=3),#Specify the color of the line
        marker=dict(color='LightSkyBlue',
            size=8)
        ),
        secondary_y=True)                   #The line chart uses the secondary y-axis 

    fig.update_layout(hoverlabel_bgcolor='#DAEEED',  #Change the background color of the tooltip to light blue
                # title_text="Housing Market Trends: Raleigh, NC", #Add a chart title
                # title_font_family="Times New Roman",
                # title_font_size = 20,
                # title_font_color="darkblue", #Specify font color of the title
                # title_x=0.46, #Specify the title position
                margin=dict(l=5, r=5, t=5, b=5),
                xaxis=dict(
                        tickfont_size=10,
                        tickangle = 270,
                        showgrid = True,
                        zeroline = True,
                        showline = True,
                        #showticklabels = True,
                        #dtick="M1", #Change the x-axis ticks to be monthly
                        tickformat="%b\n%Y"
                        ),
                legend = dict(orientation = 'h', xanchor = "center", x = 0.45, y= 1.11), #Adjust the legend position
                yaxis_title='Número de Projetos',
                yaxis2_title='Total de recuros (BRL)')
    
    fig.update_layout(
    xaxis=dict(
        tickangle=90,
        # tickfont=dict(family="Rockwell", color="crimson", size=14),
        tickvals=list(ShortNames_Fiocruz.keys()),
        ticktext=list(ShortNames_Fiocruz.values())
    ),
    yaxis2=dict(
        # color='#f70f13',
        color = '#3ff698',

    ),
    yaxis=dict(
        # color='#f0497b',
        color = '#ef6790',

    )

)
    

    # fig.for_each_trace(lambda t: t.update(name = ShortNames_Fiocruz[t.name]))

    return fig

genero = ['field_genero','field_sexo']
generoi = genero[0]
df_completo['N° Submissões'] = df_completo['id']
gk7 = df_completo.groupby([generoi], as_index=False)['N° Submissões'].count()
gk7['percentage'] = 100*gk7['N° Submissões']/gk7['N° Submissões'].sum()


# fig3 = go.Figure(
# px.pie(gk3, values='N° Submissões',names='Eixo',title='Editais por Eixo'))
def figure8():
    fig8 = go.Figure(data=[go.Pie(labels=gk7[generoi],
                                values=gk7['N° Submissões'],
                                name='',
                                customdata=gk7['percentage'])])
    # fig3.update_traces(hoverinfo='label+percent', textinfo='value')
    fig8.update_traces(textposition='inside', textinfo='value',\
                    hovertemplate = "Genero:%{label}: <br>Porcentagem : %{customdata:.2f}% </br>N° Coordenadores: %{value}"
    )

    fig8.update_layout(legend = dict(font = dict(size = 16),
            bgcolor="#20374c",
            bordercolor="White",
            borderwidth=0.5),
                    legend_title = dict(font = dict(size = 15)))


    fig8.update_layout(
        title={
            'text': 'Genero Coordenador',
            # 'y':0.9,
            # 'x':0.5,
            'xanchor': 'left',
            'yanchor': 'top',
            'font': {'size': 16}},
        legend_title_text='Eixos',
        margin= {"t": 2, "r": 2, "b": 2, "l": 2},
        plot_bgcolor= "#20374c",
        paper_bgcolor= "#20374c",
        font= {"color": "white"}
    )
    return fig8

# ------------
df_completot = df_completo.copy()
field_situacao_set = ['Recomendado','Recomendado com ajustes']
df_completot['N° Submissões'] = df_completot['id']
df_d = df_completot[(df_completot['field_situacao'].isin(field_situacao_set))]
gk8 = df_d.groupby(['ano_creacao']).agg({'field_total_de_recursos': 'sum', 'id': 'count'})
# gk6 = gk6.sort_values(by=['field_total_de_recursos'],ascending=False)
# gk8 = gk8.sort_values(by=['id'],ascending=False)
fig9=make_subplots(specs=[[{"secondary_y":True}]])



def figure9():
    fig9.add_trace(                           #Add a bar chart to the figure
            go.Bar(
            x=gk8.index,
            y=gk8['id'],
            name="Número de Projetos",
            hoverinfo='none' ,               #Hide the hoverinfo
            marker_color='#9f89d8',#'#f27097',     
            ),
            secondary_y=False)               #The bar chart uses the primary y-axis 

    fig9.add_trace(                           #Add the second chart (line chart) to the figure
        go.Scatter(
        x=gk8.index,
        y=gk8['field_total_de_recursos'],
        name="Total de recursos (BRL)",
        mode='lines+markers',
        customdata = gk8['id'],
        hovertemplate=
        "<b>%{x}</b><br><br>" +
        "Total de recursos (BRL): %{y:$,.0f}<br>" +
        "N° de projetos: %{customdata:.0f}<br>" +
        "<extra></extra>",

        line = dict(color='#3ff698', width=3),#Specify the color of the line
        marker=dict(color='LightSkyBlue',
            size=8)
        ),
        secondary_y=True)                   #The line chart uses the secondary y-axis 

    fig9.update_layout(hoverlabel_bgcolor='#DAEEED',  #Change the background color of the tooltip to light blue
                # title_text="Housing Market Trends: Raleigh, NC", #Add a chart title
                # title_font_family="Times New Roman",
                # title_font_size = 20,
                # title_font_color="darkblue", #Specify font color of the title
                # title_x=0.46, #Specify the title position
                margin=dict(l=5, r=5, t=5, b=5),
                xaxis=dict(
                        tickfont_size=16,
                        showgrid = True,
                        zeroline = True,
                        showline = True,
                        #showticklabels = True,
                        #dtick="M1", #Change the x-axis ticks to be monthly
                        tickformat="%b\n%Y"
                        ),
                legend = dict(orientation = 'h', xanchor = "center", x = 0.45, y= 1.11), #Adjust the legend position
                yaxis_title='Número de Projetos',
                yaxis2_title='Total de recuros (BRL)')
    
    fig9.update_layout(
    yaxis2=dict(
        # color='#f70f13',
        color = '#3ff698',

    ),
    yaxis=dict(
        color='#9f89d8',
        # color = '#ef6790',

    )

)
    

    # fig.for_each_trace(lambda t: t.update(name = ShortNames_Fiocruz[t.name]))

    return fig9


def figure11_():
    fig = go.Figure(go.Indicator(
    mode = "number+gauge+delta",
    gauge = {'shape': "bullet"},
    delta = {'reference': 300},
    value = 220,
    domain = {'x': [0.1, 1], 'y': [0.2, 0.9]},
    title = {'text': "Avg order size"}))

    fig.update_layout(
    height=55,  # Added parameter
    )

    return fig

def figure11(coor_agra, coor_naoagra):
    fig = go.Figure()
    fig.add_trace(go.Bar(
    y=['Agraciados'],
    x=[coor_agra],
    name='Agraciados',
    text = coor_agra,
    texttemplate='%{text:.0f}',
    textangle=0, textposition="outside",  textfont_color='white',cliponaxis=False,
    orientation='h',
    # marker=dict(
    #     color='rgba(246, 78, 139, 0.6)',
    #     line=dict(color='rgba(246, 78, 139, 1.0)', width=3)
    # )
    ))
    fig.add_trace(go.Bar(
    y=[ 'Não agraciados'],
    x=[ coor_naoagra],
    name='Não agraciados',
    text = coor_naoagra,
    texttemplate='%{text:.0f}',
    textangle=0, textposition="outside",  textfont_color='white',cliponaxis=False,
    orientation='h',

    ))

    fig.update_traces(textposition='inside',\
                        hovertemplate = "Coordenadores %{label} <br> </br>N°: %{value}"
        )

    fig.update_layout(legend = dict(font = dict(size = 11),
                bgcolor="#20374c",
                bordercolor="White",
                borderwidth=0.5),
                        legend_title = dict(font = dict(size = 11)))


    fig.update_layout(
            barmode='group',
            legend=dict(font_size=11),
            margin= {"t": 2, "r": 2, "b": 2, "l": 2},
            plot_bgcolor= "#20374c",
            paper_bgcolor= "#20374c",
            font= {"color": "white"}
        )



    fig.update_layout(height=250)

    return fig


def figure12():
    fig.add_trace(                           #Add a bar chart to the figure
            go.Bar(
            x=gk6.index,
            y=gk6['id'],
            name="Número de Projetos",
            hoverinfo='none' ,               #Hide the hoverinfo
            marker_color='#ef6790',#'#f0497b',#'#f27097',     
            ),
            secondary_y=False)               #The bar chart uses the primary y-axis 

    fig.add_trace(                           #Add the second chart (line chart) to the figure
        go.Scatter(
        x=gk6.index,
        y=gk6['field_total_de_recursos'],
        name="Total de recursos (BRL)",
        mode='lines+markers',
        text= list(ShortNames_Fiocruz.keys()),
        customdata = gk6['id'],
        hovertemplate=
        "<b>%{text}</b><br><br>" +
        "Total de recursos (BRL): %{y:$,.0f}<br>" +
        "N° de projetos: %{customdata:.0f}<br>" +
        "<extra></extra>",
        # text=df['text'],               
        # hoverinfo='text',                   #Pass the 'text' column to the hoverinfo parameter to customize the tooltip
        line = dict(color='#3ff698', width=3),#Specify the color of the line
        marker=dict(color='LightSkyBlue',
            size=8)
        ),
        secondary_y=True)                   #The line chart uses the secondary y-axis 

    fig.update_layout(hoverlabel_bgcolor='#DAEEED',  #Change the background color of the tooltip to light blue
                # title_text="Housing Market Trends: Raleigh, NC", #Add a chart title
                # title_font_family="Times New Roman",
                # title_font_size = 20,
                # title_font_color="darkblue", #Specify font color of the title
                # title_x=0.46, #Specify the title position
                margin=dict(l=5, r=5, t=5, b=5),
                xaxis=dict(
                        tickfont_size=10,
                        tickangle = 270,
                        showgrid = True,
                        zeroline = True,
                        showline = True,
                        #showticklabels = True,
                        #dtick="M1", #Change the x-axis ticks to be monthly
                        tickformat="%b\n%Y"
                        ),
                legend = dict(orientation = 'h', xanchor = "center", x = 0.45, y= 1.11), #Adjust the legend position
                yaxis_title='Número de Projetos',
                yaxis2_title='Total de recuros (BRL)')
    
    fig.update_layout(
    xaxis=dict(
        tickangle=90,
        # tickfont=dict(family="Rockwell", color="crimson", size=14),
        tickvals=list(ShortNames_Fiocruz.keys()),
        ticktext=list(ShortNames_Fiocruz.values())
    ),
    yaxis2=dict(
        # color='#f70f13',
        color = '#3ff698',

    ),
    yaxis=dict(
        # color='#f0497b',
        color = '#ef6790',

    )

)
    

    # fig.for_each_trace(lambda t: t.update(name = ShortNames_Fiocruz[t.name]))

    return fig

df_completo_ = df_completo.copy()

#app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SUPERHERO])
app = dash.Dash(__name__)
# FA = "https://use.fontawesome.com/releases/v6.4.0/css/all.css"
# app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, FA])
# app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME])


predict_button = dbc.Card(
    className="mt-auto",
    children=[
        dbc.CardBody(
            [
                html.Div(
                    [
                        dbc.Button(
                            "Download",
                            id="download-button",
                            color="primary",
                            outline=True,
                            size="lg",
                            style={"color": "#fec036"},
                        ),
                        dcc.Download(id="download-xls")
                    ]
                )
            ],
            style={
                "text-align": "center",
                "backgroundColor": "black",
                "border-radius": "1px",
                "border-width": "5px",
                "border-top": "1px solid rgb(216, 216, 216)",
                "border-left": "1px solid rgb(216, 216, 216)",
                "border-right": "1px solid rgb(216, 216, 216)",
                "border-bottom": "1px solid rgb(216, 216, 216)",
            },
        )
    ],
)

get_new_information_button = dbc.Card(
    className="mt-auto",
    children=[
        dbc.CardBody(
            [
                html.Div(
                    [
                        dbc.Button(
                            "Aplicar",
                            id="get-new-info-button",
                            color="primary",
                            outline=True,
                            size="lg",
                            style={"color": "#fec036"},
                        ),
                    ]
                )
            ],
            style={
                "text-align": "center",
                "backgroundColor": "black",
                "border-radius": "1px",
                "border-width": "5px",
                "border-top": "1px solid rgb(216, 216, 216)",
                "border-left": "1px solid rgb(216, 216, 216)",
                "border-right": "1px solid rgb(216, 216, 216)",
                "border-bottom": "1px solid rgb(216, 216, 216)",
            },
        )
    ],
)

graphs2 = dbc.Card(className='bg-dark',
    children=[
        dbc.CardBody(
            [
                html.Div(
                    [
                        dcc.Graph(
                            id="Main-Graph",
                            figure={
                                "layout": {
                                    "margin": {"t": 30, "r": 35, "b": 40, "l": 50},
                                    "xaxis": {
                                        "dtick": 5,
                                        "gridcolor": "#636363",
                                        "showline": False,
                                    },
                                    "yaxis": {"showgrid": False, "showline": False},
                                    "plot_bgcolor": "black",
                                    "paper_bgcolor": "black",
                                    "font": {"color": "gray"},
                                },
                            },
                            config={"displayModeBar": False},
                        ),
                        html.Pre(id="update-on-click-data"),
                    ],
                    style={"width": "98%", "display": "inline-block"},
                ),
            ],
            style={
                # "backgroundColor": "black",
                "border-radius": "1px",
                "border-width": "5px",
                "border-top": "1px solid rgb(216, 216, 216)",
            },
        )
    ]
)



graphs = dbc.Card(className='bg-dark',
    children=[
        dbc.CardBody(
            [
                html.Div(
                    [
                        dcc.Graph(
                            id="Main-Graph",
                            figure=figure3(),
                            config={"displayModeBar": False},
                        ),
                        html.Pre(id="update-on-click-data"),
                    ],
                    style={"width": "98%", "display": "inline-block"},
                ),
            ],
            style={
                # "backgroundColor": "black",
                "border-radius": "1px",
                "border-width": "5px",
                "border-top": "1px solid rgb(216, 216, 216)",
            },
        )
    ]
)

rul_estimation_indicator = dbc.Card(className='bg-dark',
    children=[
        dbc.CardHeader(
            "Número de projetos submetidos",
            style={
                "text-align": "center",
                "color": "white",
                # "backgroundColor": "black",
                "border-radius": "1px",
                "border-width": "5px",
                "border-top": "1px solid rgb(216, 216, 216)",
            },
        ),
        dbc.CardBody(
            [
                dcc.Graph(id="sub-estimation-indicator-led0", figure=go.Figure(data=[go.Indicator(
                mode = "number",
                value = 400,
                # delta = {'position': "top", 'reference': 320},
                # domain = {'x': [0, 1], 'y': [0, 1]}
                )], layout=go.Layout(height=55)))
            ],
            style={
                "text-align": "center",
                # "backgroundColor": "black",
                "border-radius": "1px",
                "border-width": "5px",
                "border-top": "1px solid rgb(216, 216, 216)",
            },
        ),
    ]
)


rul_estimation_indicator_aprov = dbc.Card(className='bg-dark',
    children=[
        dbc.CardHeader(
            "Número de projetos aprovados",
            style={
                "text-align": "center",
                "color": "white",
                # "backgroundColor": "black",
                "border-radius": "1px",
                "border-width": "5px",
                "border-top": "1px solid rgb(216, 216, 216)",
            },
        ),
        dbc.CardBody(
            [
                dcc.Graph(id="sub-estimation-indicator-led1", figure=go.Figure(data=[go.Indicator(
                mode = "number",
                value = 400,
                # delta = {'position': "top", 'reference': 320},
                # domain = {'x': [0, 1], 'y': [0, 1]}
                )], layout=go.Layout(height=55)))
            ],
            style={
                "text-align": "center",
                # "backgroundColor": "black",
                "border-radius": "1px",
                "border-width": "5px",
                "border-top": "1px solid rgb(216, 216, 216)",
            },
        ),
    ]
)


rul_estimation_indicatorc = dbc.Card(className='bg-dark',
    children=[
        dbc.CardHeader(
            "Recursos Solicitados (BRL)",
            style={
                "text-align": "center",
                "color": "white",
                # "backgroundColor": "black",
                "border-radius": "1px",
                "border-width": "5px",
                "border-top": "1px solid rgb(216, 216, 216)",
            },
        ),
        dbc.CardBody(
            [
                dcc.Graph(id="sub-estimation-indicator-led3", figure=go.Figure(data=[go.Indicator(
                mode = "number",
                value = 400,
                number = {'prefix': "$"},
                # delta = {'position': "top", 'reference': 320},
                # domain = {'x': [0, 1], 'y': [0, 1]}
                )], layout=go.Layout(height=55)))
            ],
            style={
                "text-align": "center",
                # "backgroundColor": "black",
                "border-radius": "1px",
                "border-width": "5px",
                "border-top": "1px solid rgb(216, 216, 216)",
            },
        ),
    ]
)

cost_estimation_indicator = dbc.Card(className='bg-dark',
    children=[
        dbc.CardHeader(
            "Recursos Aprovados (BRL)",
            style={
                "text-align": "center",
                "color": "white",
                # "backgroundColor": "black",
                "border-radius": "1px",
                "border-width": "5px",
                "border-top": "1px solid rgb(216, 216, 216)",
            },
        ),
        dbc.CardBody(
            [
                dcc.Graph(id="sub-estimation-indicator-led2", figure=go.Figure(data=[go.Indicator(
                mode = "number",
                value = 400,
                number = {'prefix': "$"},
                # delta = {'position': "top", 'reference': 320},
                # domain = {'x': [0, 1], 'y': [0, 1]}
                )], layout=go.Layout(height=55)))
            ],
            style={
                "text-align": "center",
                # "backgroundColor": "black",
                "border-radius": "1px",
                "border-width": "5px",
                "border-top": "1px solid rgb(216, 216, 216)",
            },
        ),
    ]
)


info_box2 = dbc.Card(className='bg-dark',
    children=[
    
        dbc.CardHeader(
            "Filtros",
            style={
                "text-align": "center",
                "color": "white",
                # "backgroundColor": "black",
                "border-radius": "1px",
                "border-width": "5px",
                "border-top": "1px solid rgb(216, 216, 216)",
            },
        ),

        dbc.CardBody(
            [
        html.Div(
                id="upper-left",
                # className="six columns",
                children=[
                    html.P(
                        className="section-title",
                        children='Escolha e aplique filtros na busca',
                    ),
                    html.Div(
                        # className="control-row-1",
                        children=[
                            html.Div(
                                id="year-select-outer",
                                children=[
                                    html.Label("Selecione um periodo"),
                                    dcc.RangeSlider(id='year-slider', min=2018, max=2023, step=1, value=[2018, 2023],marks={
                                        str(year): {
                                            "label": str(year),
                                            "style": {"color": "#7fafdf"},
                                        }
                                        for year in list(range(2018,2024,1))
                                    },allowCross=False),
                                ],
                            )
                        ],
                    ),
                    html.Div(
                        # className="control-row-1",
                        children=[
                            html.Div(
                                id="state-select-outer",
                                children=[
                                    html.Label("Selecione um Eixo"),
                                    dcc.Dropdown(
                                        id="eixo-select",
                                        options=[{"label": i, "value": i} for i in list(gk5['Eixo'].unique())],
                                        multi=True,
                                    ),
                                ],
                            )
                        ],
                    ),
                    html.Div(
                        id="region-select-outer",
                        # className="control-row-2",
                        children=[
                            html.Label("Selecione um edital"),
                            html.Div(
                                id="checklist-container",
                                children=dcc.Checklist(
                                    id="edital-select-all",
                                    options=[{"label": "Selecionar todos os editais", "value": "All"}],
                                    value=[],
                                ),
                            ),
                            html.Div(
                                id="region-select-dropdown-outer",
                                children=dcc.Dropdown(
                                    id="edital-select", multi=True, searchable=True,
                                ),
                            ),
                        ],
                    ),
                    
                    html.Div(children=[html.Div(
                                id="select-metric-outer",
                                children=[
                                    html.Label("Selecione rodada"),
                                    dcc.Dropdown(
                                        id="rodada-select",
                                        options=[{"label": i, "value": i} for i in lista_rodadas],
                                        multi= True
                                    ),
                                ],
                            )]),

                    html.Div(children=[html.Div(
                                id="select-status-outer",
                                children=[
                                    html.Label("Selecione Status"),
                                    dcc.Dropdown(
                                        id="status-select",
                                        options=[{"label": i, "value": i} for i in list(df_completo['field_situacao'].unique())],
                                        multi= True,
                                        # style={'width':'100%', 'display':'inline-block','font-size' : '85%'}
                                    ),
                                ],
                            )]),
                    
                    html.Div(children=[html.Div(
                                id="select-unit-outer",
                                children=[
                                    html.Label("Selecione unidade"),
                                    dcc.Dropdown(
                                        id="unidade-select",
                                        options=[{"label": i, "value": i} for i in list(df_completo['field_unidade_da_fiocruz:name'].unique())],
                                        multi= True,
                                        optionHeight=60,
                                        # style={'width':'100%', 'display':'inline-block','font-size' : '85%'}
                                    ),
                                ],
                            )])
                    
                    ])

            ],
            style={
                # "backgroundColor": "black",
                "border-radius": "1px",
                "border-width": "5px",
                "border-top": "1px solid rgb(216, 216, 216)",
            },
        ),
    ],
)

# ----------------------------------------------------------------------------------------------------------------#
# --------------------------------------------------- INFO CARDS -------------------------------------------------#
# ----------------------------------------------------------------------------------------------------------------#

cardteam3 = dbc.Card(
    [
        dbc.Row(
            [
                dbc.Col(
                    dbc.CardBody(
                        [
                            html.H4(children = str(pessoas_equipe(df_completo)), id='card_pessoas_equipe',className="card-title"),
                            html.P(
                                "Número de pessoas nas equipes",
                                className="card-text",
                            ),
                        ]
                    ),
                    className="col-md-8",
                ),
                dbc.Col(
                    dbc.CardImg(
                        # src="/static/images/portrait-placeholder.png",
                        # src=count,
                        src = r'assets/icons/team.png',
                        className="img-fluid rounded-start",
                    ),
                    className="col-md-4",
                )
            ],
            className="g-0 d-flex align-items-center",
        )
    ],
    # className="bg-dark",
    # style={"maxWidth": "540px"},
)


cardteam4 = dbc.Card(
    [
        dbc.Row(
            [
                dbc.Col(
                    dbc.CardBody(
                        [
                            html.H4(children = str(coordenadores(df_completo)),id = 'card_coordenadores', className="card-title"),
                            html.P(
                                "Número de coordenadores",
                                className="card-text",
                            ),
                        ]
                    ),
                    className="col-md-8",
                ),
                dbc.Col(
                    dbc.CardImg(
                        # src="/static/images/portrait-placeholder.png",
                        # src=count,
                        src = r'assets/icons/goal.png',
                        className="img-fluid rounded-start",
                    ),
                    className="col-md-4",
                )
            ],
            className="g-0 d-flex align-items-center",
        )
    ],
    # className="bg-dark",
    # style={"maxWidth": "540px"},
)


cardteam5 = dbc.Card(
    [
        dbc.Row(
            [
                dbc.Col(
                    dbc.CardBody(
                        [
                            html.H4(children=str(bolsistas(df_completo)), id= 'card_bolsistas', className="card-title"),
                            html.P(
                                "Número de bolsistas nas equipes",
                                className="card-text",
                            ),
                        ]
                    ),
                    className="col-md-8",
                ),
                dbc.Col(
                    dbc.CardImg(
                        # src="/static/images/portrait-placeholder.png",
                        # src=count,
                        src = r'assets/icons/trainee.png',
                        className="img-fluid rounded-start",
                    ),
                    className="col-md-4",
                )
            ],
            className="g-0 d-flex align-items-center",
        )
    ],
    # className="bg-dark",
    # style={"maxWidth": "540px"},
)

recursos_ = round(gk6['field_total_de_recursos'].sum(),1)

cardteam6 = dbc.Card(
    [
        dbc.Row(
            [
                dbc.Col(
                    dbc.CardBody(
                        [
                            html.H4(children = str(recursos_), id = 'card_orcamento_solicitado', className="card-title"),
                            html.P([
                                "Orçamento",html.Br(), "solicitado"],
                                className="card-text",
                            )
                            ,
                        ]
                    ),
                    className="col-md-8",
                ),
                dbc.Col(
                    dbc.CardImg(
                        # src="/static/images/portrait-placeholder.png",
                        # src=count,
                        src = r'assets/icons/budgett.png',
                        className="img-fluid rounded-start",
                    ),
                    className="col-md-4",
                )
            ],
            className="g-0 d-flex align-items-center",
        )
    ],
    # className="bg-dark",
    # style={"maxWidth": "540px"},
)


# cardaval1a = dbc.Card(
#     [dbc.Row([
#         dbc.Col([
#             dbc.Row(
#                 dbc.Card([dbc.CardBody(
#                         [
#                             html.H4("Card title", className="card-title"),
#                             html.P(
#                                 "Número de pessoas nas equipes",
#                                 className="card-text",
#                             ),
#                         ]
#                     )])
#             ,justify="start"),
#             dbc.Row(dbc.Card([dbc.CardBody(
#                         [
#                             html.H4("Card title", className="card-title"),
#                             html.P(
#                                 "Número de pessoas nas equipes",
#                                 className="card-text",
#                             ),
#                         ]
#                     )])
    
#             ,justify="start")

#         ],width=8),

#         dbc.Col([
#             dbc.Row(dbc.Card([
#                     dbc.CardImg(
#                         src = r'assets/icons/budgett.png',
#                         className="img-fluid rounded-start",
#                     )])
    
#             ,justify="start")

#         ],width=4)


#     ],
#             className="g-0 d-flex align-items-center",)

#     ]

# )

cardaval1 = dbc.Card(
    [dbc.Row([
        dbc.Col([
            dbc.Row(dbc.Col([
                dbc.Card([dbc.CardBody(
                        [
                            html.H4("Card title", className="card-title"),
                            html.P(
                                "Número de pessoas nas equipes",
                                className="card-text",
                            ),
                        ]
                    )],outline=False)])
            ,justify="start",className = "border-0"),
            dbc.Row(dbc.Col([
                dbc.Card([dbc.CardBody(
                        [
                            html.H4("Card title", className="card-title"),
                            html.P(
                                "Número de pessoas nas equipes",
                                className="card-text",
                            ),
                        ]
                    )],outline=False)])
    
            ,justify="start",className="border-0")

        ],width=8),

        dbc.Col([
            dbc.Row(dbc.Col([
                    dbc.Card([
                    dbc.CardImg(
                        src = r'assets/icons/budgett.png',
                        className="img-fluid rounded-start",
                    )])])
    
            ,justify="start",className="border-0")

        ],width=4)


    ],
            className="g-0 d-flex align-items-center"),
            # className = "border-0")

    ]

)



gauge_size = "auto"
sidebar_size = 12
graph_size = 10
app.layout = dbc.Container(
    fluid=True,
    children=[
        logo(app),

        
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Row(dbc.Col(info_box2,
                                        # xs=sidebar_size,
                                        # md=sidebar_size,
                                        # lg=sidebar_size,
                                        width=sidebar_size),
                                ),
                        dbc.Row(dbc.Col(get_new_information_button,
                                        # xs=sidebar_size,
                                        # md=sidebar_size,
                                        # lg=sidebar_size,
                                        width=sidebar_size)
                                ),
                        dbc.Row(dbc.Col(predict_button,
                                        # xs=sidebar_size,
                                        # md=sidebar_size,
                                        # lg=sidebar_size,
                                        width=sidebar_size)
                                ),
                    ], width=4
                ),

                dbc.Col([
                    dbc.Row([dbc.Col(rul_estimation_indicator, 
                                            # xs=sidebar_size,
                                            # md=sidebar_size,
                                            # lg=sidebar_size,
                                            width=3),
                    dbc.Col(rul_estimation_indicator_aprov, 
                                            # xs=sidebar_size,
                                            # md=sidebar_size,
                                            # lg=sidebar_size,
                                            width=3),
                    dbc.Col(cost_estimation_indicator, 
                                            # xs=sidebar_size,
                                            # md=sidebar_size,
                                            # lg=sidebar_size,
                                            width=3),
                    dbc.Col(rul_estimation_indicatorc, 
                                            # xs=sidebar_size,
                                            # md=sidebar_size,
                                            # lg=sidebar_size,
                                            width=3)],justify='end',
                style={
                    "marginTop": "0%"
                },),

            dbc.Row([dbc.Col([html.H6(
            "EDITAIS por eixo",
            style={"marginTop": 10, "marginLeft": "10px"},
            )])
            
            ], justify='end',
                    style={
                        "marginTop": "3%"
                    },),

            dbc.Row([dbc.Col(graphs,
                        # xs=graph_size,
                        # md=graph_size,
                        # lg=graph_size,
                        width=12)]),

            dbc.Row([dbc.Col([html.H6(
            "",
            style={"marginTop": 0, "marginLeft": "10px"},
        )])
        
        ], justify='end',
                style={
                    "marginTop": "3%"
                },)
            ],width=8)
                ],
                style={
                        "marginTop": "3%"
                    }),



    dbc.Row([dbc.Col([html.H6(
        "EDITAIS por rodada",
        style={"marginTop": 2, "marginLeft": "10px"},
    )]), dbc.Col([html.H6(
        children="EDITAIS por aprovacao",
        style={"marginTop": 2, "marginLeft": "10px"},
    )])
    
    ], justify='end',
            style={
                "marginTop": "3%"
            },),


    dbc.Row([dbc.Col([dcc.Graph(id='bar_chart',figure=figure2())]),
            dbc.Col([dcc.Graph(id='pie_chart2',figure=figure4())])
    
    ], justify='end',
            style={
                "marginTop": "0%"
            },),

    dbc.Row([dbc.Col([html.H6(
        "Editais por unidade",
        style={"marginTop": 2, "marginLeft": "10px"},
    )])
    
    ], justify='end',
            style={
                "marginTop": "3%"
            },),

    dbc.Row([dbc.Col([dcc.Graph(id='bar_chartx',figure=figure7())])], 
            justify='end',
            style={
                "marginTop": "3%"
            },),

    dbc.Row([dbc.Col([html.H6(
        "Editais e recursos",
        style={"marginTop": 2, "marginLeft": "10px"},
    )])
    
    ], justify='end',
            style={
                "marginTop": "3%"
            },),
    dbc.Row([dbc.Col([dcc.Graph(id='bar_chart3',figure=figure7())])], 
            justify='end',
            style={
                "marginTop": "3%"
            },),
    
    dbc.Row([dbc.Col([html.H6(
        "Editais por ano",
        style={"marginTop": 2, "marginLeft": "10px"},
    )])
    
    ], justify='end',
            style={
                "marginTop": "3%"
            },),

    dbc.Row([dbc.Col([dcc.Graph(id='bar_chartx2',figure=figure9())])], 
            justify='end',
            style={
                "marginTop": "3%"
            },),

    dbc.Row([dbc.Col([html.H6(
        "Dados sobre equipes",
        style={"marginTop": 2, "marginLeft": "10px"},
    )])
    
    ], justify='end',
            style={
                "marginTop": "3%"
            },),

    dbc.Row([dbc.Col(cardteam3, 
                                            # xs=sidebar_size,
                                            # md=sidebar_size,
                                            # lg=sidebar_size,
                                            width=3),
                    dbc.Col(cardteam4, 
                                            # xs=sidebar_size,
                                            # md=sidebar_size,
                                            # lg=sidebar_size,
                                            width=3),
                    dbc.Col(cardteam5, 
                                            # xs=sidebar_size,
                                            # md=sidebar_size,
                                            # lg=sidebar_size,
                                            width=3),
                    dbc.Col(cardteam6, 
                                            # xs=sidebar_size,
                                            # md=sidebar_size,
                                            # lg=sidebar_size,
                                            width=3)],justify='end',
                style={
                    "marginTop": "0%"
                },),

    dbc.Row([dbc.Col([html.H6(
        "Dados sobre coordenadores",
        style={"marginTop": 2, "marginLeft": "10px"},
    )]), dbc.Col([html.H6(
        children="Dados sobre bolsistas",
        style={"marginTop": 2, "marginLeft": "10px"},
    )])
    
    ], justify='end',
            style={
                "marginTop": "3%"
            },),

    dbc.Row([dbc.Col([dcc.Graph(id='card_bar1',figure =figure11(0, 0))]),

            dbc.Col([dcc.Graph(id='card_bar2',figure =figure11(0, 0))])
            ], justify='end',
            style={
                "marginTop": "2%"
            },),

    dbc.Row([dbc.Col([dcc.Graph(id='bar_chartz',figure=figure2())]),
            dbc.Col([dcc.Graph(id='pie_chart2z',figure=figure8())])
    
    ], justify='end',
            style={
                "marginTop": "2%"
            },),

    dbc.Row([dbc.Col([dcc.Graph(id='bar_chart_coord-ud',figure=figure7())])], 
            justify='end',
            style={
                "marginTop": "3%"
            },),

    dbc.Row([dbc.Col([html.H6(
        "Dados sobre avaliadores",
        style={"marginTop": 2, "marginLeft": "10px"},
    )]), dbc.Col([html.H6(
        children="Dados sobre parceiros",
        style={"marginTop": 2, "marginLeft": "10px"},
    )])
    
    ], justify='end',
            style={
                "marginTop": "3%"
            },),
    
    dbc.Row([dbc.Col(cardaval1,width=6),dbc.Col(cardaval1,width=6)],justify='end',
                style={
                    "marginTop": "0%"
                }),
    dbc.Row([dbc.Col([html.H6(
        "Next",
        style={"marginTop": 2, "marginLeft": "10px"},
    )])
    
    ], justify='end',
            style={
                "marginTop": "3%"
            },),
        ]
)

# https://observablehq.com/@d3/d3-format
# https://d3-wiki.readthedocs.io/zh_CN/master/Formatting/
def fig1_card(recursos):
    fig = go.Figure(go.Indicator(
                mode = "number",
                value = recursos,
                # number = { 'prefix': "$", 'font': { 'size': 20 },'valueformat':',.0f'}
                number = { 'prefix': "$", 'font': { 'size': 30 },'valueformat':'.4s'}
                # delta = {'position': "top", 'reference': 320},
                # domain = {'x': [0, 1], 'y': [0, 1]}
                ))
    fig.update_layout(
    height=55,  # Added parameter
    )
    return fig

def fig0_card(projetos):
    fig = go.Figure(go.Indicator(
                mode = "number",
                value = projetos,
                number = { 'font': { 'size': 20 },'valueformat':'f'}
                # number = { 'prefix': "$", 'font': { 'size': 30 },'valueformat':'.4s'}
                # delta = {'position': "top", 'reference': 320},
                # domain = {'x': [0, 1], 'y': [0, 1]}
                ))
    fig.update_layout(
    height=55,  # Added parameter
    )
    return fig




def figure3_load(gk3):

    fig3 = go.Figure(data=[go.Pie(labels=gk3['Eixo'],
                                    values=gk3['N° Submissões'],
                                    name='',
                                    customdata=gk3['percentage'])])
    # fig3.update_traces(hoverinfo='label+percent', textinfo='value')
    fig3.update_traces(textposition='inside', textinfo='value',\
                        hovertemplate = "Eixo %{label} <br>Porcentagem : %{customdata:.2f}% </br>N° Submissões: %{value}"
        )

    fig3.update_layout(legend = dict(font = dict(size = 16),
                bgcolor="#20374c",
                bordercolor="White",
                borderwidth=0.5),
                        legend_title = dict(font = dict(size = 15)))


    fig3.update_layout(
            title={
                'text': 'EDITAIS por Eixo',
                # 'y':0.9,
                # 'x':0.5,
                'xanchor': 'left',
                'yanchor': 'top',
                'font': {'size': 16}},
            legend_title_text='Eixos',
            legend=dict(font_size=13),
            margin= {"t": 2, "r": 2, "b": 2, "l": 2},
            plot_bgcolor= "#20374c",
            paper_bgcolor= "#20374c",
            font= {"color": "white"}
        )
    
    return fig3

def figure2_load(gk5):
    fig2 = go.Figure(
        px.bar(gk5, x='N° Submissões', y='field_edital_de_referencia:title', color='field_rodada_produtos:name', text_auto=True))
    fig2.update_traces(textfont_size=8, textangle=0, textposition="outside", cliponaxis=False)
    fig2.update_layout(yaxis_title=None,xaxis_title=None)
    fig2.update_layout(
                    margin=dict(l=5, r=5, t=5, b=5),
                    title='',
                    xaxis_tickfont_size=10,
                    yaxis=dict(
                        showgrid=False,
                        showline=False,
                        showticklabels=True,
                        title='',
                        titlefont_size=1,
                        tickfont_size=9,
                    ),
                    xaxis=dict(
                        zeroline=False,
                        showline=False,
                        showticklabels=True,
                        showgrid=True
                    ),
                    legend_title_text='',
                    legend=dict(font_size=9,orientation="h",
                    yanchor="bottom",
                    y=1.01,
                    xanchor="right",
                    x=1)
                    )



    fig2.update_traces(hovertemplate=
                        '<b></b>%{y}' +
                        '<br><b>N° Submissões</b>: %{x}<br>')
    return fig2

# def figure4_load(gk4):
#     fig4 = go.Figure(data=[go.Pie(labels=gk4['field_situacao'],
#                                             values=gk4['N° Submissões'],
#                                             name='',
#                                             )])
#     # fig4.update_traces(hoverinfo='label+value', textinfo='percent')
#     fig4.update_traces(textposition='inside', textinfo='percent',\
#                         hovertemplate = "Status: %{label} <br>N° Submissões: %{value}"
#                         )

#     fig4.update_layout(
#                         title='',
#                         margin=dict(l=5, r=5, t=5, b=5),
#                         legend_title_text='Status',
#                         legend = dict(
#                         # bgcolor="#20374c",
#                         bordercolor="White",
#                         borderwidth=0.5)
#             )
#     return fig4

def figure4_load(gk4_a,gk4_b):
    # Create subplots: use 'domain' type for Pie subplot
    fig4 = make_subplots(rows=1, cols=2, specs=[[{'type':'domain'}, {'type':'domain'}]])
    fig4.add_trace(go.Pie(labels=gk4_a['field_situacao'], values=gk4_a['N° Submissões'],customdata=gk4_a['percentage'],name="Status A"),
                1, 1)
    fig4.add_trace(go.Pie(labels=gk4_b['field_situacao'], values=gk4_b['N° Submissões'],customdata=gk4_b['percentage'], name="Status B"),
                1, 2)

    # Use `hole` to create a donut-like pie chart
    # fig4.update_traces(hole=.4, hoverinfo="label+percent+name")
    # fig4.update_traces(hole=.4, textposition='inside', textinfo='percent',\
    #                     hovertemplate = "Status: %{label} <br>N° Submissões: %{value}"
    #     )
    
    fig4.update_traces(hole=.4,textposition='inside', textinfo='value',\
                    hovertemplate = "Status:%{label}: <br>Porcentagem : %{customdata:.2f}% </br>N° Submissões: %{value}"
    )

    fig4.update_layout(
            title='',
            margin=dict(l=5, r=5, t=5, b=5),
            legend_title_text='Status',
            legend = dict(orientation = 'h', 
                xanchor = "left", 
                x = 0.04, y= 1.11,
                font_size=10,
                # bgcolor="#20374c",
                bordercolor="White",
                borderwidth=0.5)
 
        )
    return fig4


def figure7_load(gk6):
    fig=make_subplots(specs=[[{"secondary_y":True}]])
    fig.add_trace(                           #Add a bar chart to the figure
            go.Bar(
            x=gk6.index,
            y=gk6['N° Projetos'],
            name="Número de Projetos",
            hoverinfo='none' ,               #Hide the hoverinfo
            marker_color='#ef6790',#'#f0497b',#'#f27097',     
            ),
            secondary_y=False)               #The bar chart uses the primary y-axis 
    
    fig.add_trace(                           #Add the second chart (line chart) to the figure
        go.Scatter(
        x=gk6.index,
        y=gk6['field_total_de_recursos'],
        name="Total de recursos (BRL)",
        mode='lines+markers',
        text= list(gk6.index), # list(ShortNames_Fiocruz.keys()), 
        customdata = gk6['N° Projetos'],
        hovertemplate=
        "<b>%{text}</b><br><br>" +
        "Total de recursos (BRL): %{y:$,.0f}<br>" +
        "N° de projetos: %{customdata:.0f}<br>" +
        "<extra></extra>",
        # text=df['text'],               
        # hoverinfo='text',                   #Pass the 'text' column to the hoverinfo parameter to customize the tooltip
        line = dict(color='#3ff698', width=3),#Specify the color of the line
        marker=dict(color='LightSkyBlue',
            size=8)
        ),
        secondary_y=True)                   #The line chart uses the secondary y-axis 

    fig.update_layout(hoverlabel_bgcolor='#DAEEED',  #Change the background color of the tooltip to light blue
                # title_text="Housing Market Trends: Raleigh, NC", #Add a chart title
                # title_font_family="Times New Roman",
                # title_font_size = 20,
                # title_font_color="darkblue", #Specify font color of the title
                # title_x=0.46, #Specify the title position
                margin=dict(l=5, r=5, t=5, b=5),
                xaxis=dict(
                        tickfont_size=10,
                        tickangle = 270,
                        showgrid = True,
                        zeroline = True,
                        showline = True,
                        #showticklabels = True,
                        #dtick="M1", #Change the x-axis ticks to be monthly
                        tickformat="%b\n%Y"
                        ),
                legend = dict(orientation = 'h', xanchor = "center", x = 0.45, y= 1.11), #Adjust the legend position
                yaxis_title='Número de Projetos',
                yaxis2_title='Total de recuros (BRL)')
    
    fig.update_layout(
    xaxis=dict(
        tickangle=90,
        # tickfont=dict(family="Rockwell", color="crimson", size=14),
        # tickvals=list(ShortNames_Fiocruz.keys()),
        # ticktext=list(ShortNames_Fiocruz.values()),
        tickvals=list(gk6.index),
        ticktext= [ShortNames_Fiocruz[x] for x in list(gk6.index)],
    ),
    yaxis2=dict(
        # color='#f70f13',
        color = '#3ff698',

    ),
    yaxis=dict(
        # color='#f0497b',
        color = '#ef6790',

    )
)

    # fig.for_each_trace(lambda t: t.update(name = ShortNames_Fiocruz[t.name]))

    return fig


def figure7x_load(gk6a,gk6b,gk6x):
    fig=make_subplots(specs=[[{"secondary_y":True}]])
    fig.add_trace(                           #Add a bar chart to the figure
            go.Bar(
            x=gk6a.index,
            y=gk6a['N° Projetos'],
            name="Número de Projetos Aprovados",
            text = gk6a['N° Projetos'].tolist(),
            texttemplate='%{text:.0f}',
            textfont_size=8, textangle=0, textposition="outside",  textfont_color='white',cliponaxis=False,
            hoverinfo='none' ,               #Hide the hoverinfo
            marker_color='#ef6790',#'#f0497b',#'#f27097', 
            marker_pattern_shape="x"    
            ),
            secondary_y=False)               #The bar chart uses the primary y-axis 
    
    
    
    fig.add_trace(                           #Add a bar chart to the figure
            go.Bar(
            x=gk6b.index,
            y=gk6b['N° Projetos'],
            name="Número de Projetos Submetidos",
            text = gk6x['N° Projetos'].tolist(),
            texttemplate='%{text:.0f}',
            textfont_size=8, textangle=0, textposition="outside",  textfont_color='white',cliponaxis=False,
            hoverinfo='none' ,               #Hide the hoverinfo
            marker_color='#f0497b',#'#f27097', 
                
            ),
            secondary_y=False)               #The bar chart uses the primary y-axis 
    
    
    # fig.update_traces(texttemplate =gk6a['N° Projetos'].tolist(),textfont_size=8, textangle=0, textposition="outside",  textfont_color='white',cliponaxis=False)
    # fig.update_traces(texttemplate =gk6b['N° Projetos'].tolist(),textfont_size=8, textangle=0, textposition="outside",  textfont_color='white',cliponaxis=False)
    # fig.update_traces(textfont_size=8, textangle=0, textposition="inside", cliponaxis=False)
    # fig.update_traces(textfont_size=8, textangle=0, textposition="inside", cliponaxis=False)
    
    fig.update_layout(barmode='stack')

    
    


    # --- APROBADOS ---#

    fig.add_trace(                           #Add the second chart (line chart) to the figure
        go.Scatter(
        x=gk6a.index,
        y=gk6a['field_total_de_recursos'],
        name="Total de recursos aprovados(BRL)",
        mode='lines+markers',
        text= list(gk6a.index), # list(ShortNames_Fiocruz.keys()), 
        customdata = gk6a['N° Projetos'],
        hovertemplate=
        "<b>%{text}</b><br><br>" +
        "Total de recursos (BRL): %{y:$,.0f}<br>" +
        "N° de projetos: %{customdata:.0f}<br>" +
        "<extra></extra>",
        # text=df['text'],               
        # hoverinfo='text',                   #Pass the 'text' column to the hoverinfo parameter to customize the tooltip
        line = dict(color='#3ff698', width=3,dash='dashdot'),#Specify the color of the line
        marker=dict(color='LightSkyBlue',
            size=8)
        ),
        secondary_y=True)                   #The line chart uses the secondary y-axis 
    
    # --- NO APROBADOS ---#
    # fig.add_trace(                           #Add the second chart (line chart) to the figure
    #     go.Scatter(
    #     x=gk6a.index,
    #     y=gk6b['field_total_de_recursos'],
    #     name="Total de recursos solicitados (BRL)",
    #     mode='lines+markers',
    #     text= list(gk6b.index), # list(ShortNames_Fiocruz.keys()), 
    #     customdata = gk6b['N° Projetos'],
    #     hovertemplate=
    #     "<b>%{text}</b><br><br>" +
    #     "Total de recursos (BRL): %{y:$,.0f}<br>" +
    #     "N° de projetos: %{customdata:.0f}<br>" +
    #     "<extra></extra>",
    #     # text=df['text'],               
    #     # hoverinfo='text',                   #Pass the 'text' column to the hoverinfo parameter to customize the tooltip
    #     line = dict(color='#3ff543', width=3),#Specify the color of the line
    #     marker=dict(color='LightSkyBlue',
    #         size=8)
    #     ),
    #     secondary_y=True)                   #The line chart uses the secondary y-axis 

    # --- TOTAIS ---#

    fig.add_trace(                           #Add the second chart (line chart) to the figure
        go.Scatter(
        x=gk6x.index,
        y=gk6x['field_total_de_recursos'],
        name="Total de recursos solicitados (BRL)",
        mode='lines+markers',
        text= list(gk6x.index), # list(ShortNames_Fiocruz.keys()), 
        customdata = gk6x['N° Projetos'],
        hovertemplate=
        "<b>%{text}</b><br><br>" +
        "Total de recursos (BRL): %{y:$,.0f}<br>" +
        "N° de projetos: %{customdata:.0f}<br>" +
        "<extra></extra>",
        # text=df['text'],               
        # hoverinfo='text',                   #Pass the 'text' column to the hoverinfo parameter to customize the tooltip
        line = dict(color='#3ff543', width=3),#Specify the color of the line
        marker=dict(color='orangered',
            size=8)
        ),
        secondary_y=True)                   #The line chart uses the secondary y-axis 

    fig.update_layout(hoverlabel_bgcolor='#DAEEED',  #Change the background color of the tooltip to light blue
                # title_text="Housing Market Trends: Raleigh, NC", #Add a chart title
                # title_font_family="Times New Roman",
                # title_font_size = 20,
                # title_font_color="darkblue", #Specify font color of the title
                # title_x=0.46, #Specify the title position
                margin=dict(l=5, r=5, t=5, b=5),
                xaxis=dict(
                        tickfont_size=10,
                        tickangle = 270,
                        showgrid = True,
                        zeroline = True,
                        showline = True,
                        #showticklabels = True,
                        #dtick="M1", #Change the x-axis ticks to be monthly
                        tickformat="%b\n%Y"
                        ),
                legend = dict(orientation = 'h', xanchor = "center", x = 0.45, y= 1.11), #Adjust the legend position
                yaxis_title='Número de Projetos',
                yaxis2_title='Total de recuros (BRL)')
    
    fig.update_layout(
    xaxis=dict(
        tickangle=90,
        # tickfont=dict(family="Rockwell", color="crimson", size=14),
        # tickvals=list(ShortNames_Fiocruz.keys()),
        # ticktext=list(ShortNames_Fiocruz.values()),
        tickvals=list(gk6x.index),
        ticktext= [ShortNames_Fiocruz[x] for x in list(gk6x.index)],
    ),
    yaxis2=dict(
        # color='#f70f13',
        color = '#3ff698',

    ),
    yaxis=dict(
        # color='#f0497b',
        color = '#ef6790',

    )
)

    # fig.for_each_trace(lambda t: t.update(name = ShortNames_Fiocruz[t.name]))

    return fig




def figure9_load(gk8a,gk8b,gk8x):
    fig9=make_subplots(specs=[[{"secondary_y":True}]])
    fig9.add_trace(                           #Add a bar chart to the figure
            go.Bar(
            x=gk8a.index,
            y=gk8a['N° Projetos'],
            name="Número de Projetos Aprovados",
            text = gk8a['N° Projetos'].tolist(),
            texttemplate='%{text:.0f}',
            textangle=0, textposition="outside",  textfont_color='white',cliponaxis=False,
            hoverinfo='none' ,               #Hide the hoverinfo
            marker_color='#9f89d8',#'#f0497b',#'#f27097', 
            marker_pattern_shape="x"    
            ),
            secondary_y=False)               #The bar chart uses the primary y-axis 
    
    fig9.add_trace(                           #Add a bar chart to the figure
            go.Bar(
            x=gk8b.index,
            y=gk8b['N° Projetos'],
            name="Número de Projetos Submetidos",
            text = gk8x['N° Projetos'].tolist(),
            texttemplate='%{text:.0f}',
            textangle=0, textposition="outside",  textfont_color='white',cliponaxis=False,
            hoverinfo='none' ,               #Hide the hoverinfo
            marker_color='#6449a8',#'#f27097', 
                
            ),
            secondary_y=False)               #The bar chart uses the primary y-axis 
    
    fig9.update_layout(barmode='stack')

    fig9.add_trace(                           #Add the second chart (line chart) to the figure
        go.Scatter(
        x=gk8a.index,
        y=gk8a['field_total_de_recursos'],
        name="Total de recursos aprovados(BRL)",
        mode='lines+markers',
        text= list(gk8a.index), # list(ShortNames_Fiocruz.keys()), 
        customdata = gk8a['N° Projetos'],
        hovertemplate=
        "<b>%{text}</b><br><br>" +
        "Total de recursos (BRL): %{y:$,.0f}<br>" +
        "N° de projetos: %{customdata:.0f}<br>" +
        "<extra></extra>",
        # text=df['text'],               
        # hoverinfo='text',                   #Pass the 'text' column to the hoverinfo parameter to customize the tooltip
        line = dict(color='#3ff698', width=3,dash='dashdot'),#Specify the color of the line
        marker=dict(color='LightSkyBlue',
            size=8)
        ),
        secondary_y=True)                   #The line chart uses the secondary y-axis 
    
    fig9.add_trace(                           #Add the second chart (line chart) to the figure
        go.Scatter(
        x=gk8x.index,
        y=gk8x['field_total_de_recursos'],
        name="Total de recursos solicitados (BRL)",
        mode='lines+markers',
        text= list(gk8x.index), # list(ShortNames_Fiocruz.keys()), 
        customdata = gk8x['N° Projetos'],
        hovertemplate=
        "<b>%{text}</b><br><br>" +
        "Total de recursos (BRL): %{y:$,.0f}<br>" +
        "N° de projetos: %{customdata:.0f}<br>" +
        "<extra></extra>",
        # text=df['text'],               
        # hoverinfo='text',                   #Pass the 'text' column to the hoverinfo parameter to customize the tooltip
        line = dict(color='#3ff543', width=3),#Specify the color of the line
        marker=dict(color='orangered',
            size=8)
        ),
        secondary_y=True)                   #The line chart uses the secondary y-axis 



    fig9.update_layout(hoverlabel_bgcolor='#DAEEED',  #Change the background color of the tooltip to light blue
                # title_text="Housing Market Trends: Raleigh, NC", #Add a chart title
                # title_font_family="Times New Roman",
                # title_font_size = 20,
                # title_font_color="darkblue", #Specify font color of the title
                # title_x=0.46, #Specify the title position
                margin=dict(l=5, r=5, t=5, b=5),
                xaxis=dict(
                        tickfont_size=16,
                        showgrid = True,
                        zeroline = True,
                        showline = True,
                        #showticklabels = True,
                        #dtick="M1", #Change the x-axis ticks to be monthly
                        tickformat="%b\n%Y"
                        ),
                legend = dict(orientation = 'h', xanchor = "center", x = 0.45, y= 1.11), #Adjust the legend position
                yaxis_title='Número de Projetos',
                yaxis2_title='Total de recuros (BRL)')
    
    fig9.update_layout(
    yaxis2=dict(
        # color='#f70f13',
        color = '#3ff698',

    ),
    yaxis=dict(
        color='#9f89d8',
        # color = '#ef6790',

    )

)
    

    # fig.for_each_trace(lambda t: t.update(name = ShortNames_Fiocruz[t.name]))

    return fig9

def figure8_load(gk7):
    fig8 = go.Figure(data=[go.Pie(labels=gk7[generoi],
                                values=gk7['N° Submissões'],
                                name='',
                                customdata=gk7['percentage'])])
    # fig3.update_traces(hoverinfo='label+percent', textinfo='value')
    fig8.update_traces(textposition='inside', textinfo='value',\
                    hovertemplate = "Genero:%{label}: <br>Porcentagem : %{customdata:.2f}% </br>N° Coordenadores: %{value}"
    )

    fig8.update_layout(legend = dict(font = dict(size = 16),
            bgcolor="#20374c",
            bordercolor="White",
            borderwidth=0.5),
                    legend_title = dict(font = dict(size = 15)))


    fig8.update_layout(
        title={
            'text': 'Genero Coordenador',
            # 'y':0.9,
            # 'x':0.5,
            'xanchor': 'left',
            'yanchor': 'top',
            'font': {'size': 16}},
        legend_title_text='Eixos',
        margin= {"t": 2, "r": 2, "b": 2, "l": 2},
        plot_bgcolor= "#20374c",
        paper_bgcolor= "#20374c",
        font= {"color": "white"}
    )
    return fig8



def figure10_loadx(gk9a,gk9b,gk9x):
    gk9x = gk9x.sort_values(by=['N° Projetos'],ascending=True)
    gk9a = gk9a.reindex_like(gk9x)
    gk9b = gk9b.reindex_like(gk9x)
    # Creating two subplots
    fig = make_subplots(rows=1, cols=2, specs=[[{}, {}]], shared_xaxes=False,
                        shared_yaxes=True, vertical_spacing=0.001)
    
    fig.add_trace(                           #Add a bar chart to the figure
        go.Bar(
        x=gk9a['N° Projetos'],
        y=gk9a.index,
        name="Número de Projetos Aprovados",
        text = gk9a['N° Projetos'].tolist(),
        texttemplate='%{text:.0f}',
        textfont_size=8, textangle=0, textposition="outside",  textfont_color='white',cliponaxis=False,
        orientation = 'h',
        hoverinfo='none' ,               #Hide the hoverinfo
        marker = dict(color='#eca375',
                    line= dict(color='#eca375',width=1)),
        marker_color='#eca375',#'#f0497b',#'#f27097', 
        marker_pattern_shape="x"    
        ),
        1, 1)               #The bar chart uses the primary y-axis 
    
    fig.add_trace(                           #Add a bar chart to the figure
            go.Bar(
            x=gk9b['N° Projetos'],
            y=gk9b.index,
            name="Número de Projetos Submetidos",
            text = gk9x['N° Projetos'].tolist(),
            texttemplate='%{text:.0f}',
            textfont_size=8, textangle=0, textposition="outside",  textfont_color='white',cliponaxis=False,
            orientation='h',
            hoverinfo='none' ,               #Hide the hoverinfo
            marker_color='#f18e50',#'#f27097', 
            marker = dict(color='#f18e50',
                    line= dict(color='#f18e50',width=1)),
                
            ),
            1,1)               #The bar chart uses the primary y-axis 

    fig.update_layout(barmode='stack')

    # --- APROBADOS ---#
    fig.add_trace(                           #Add the second chart (line chart) to the figure
        go.Scatter(
        x=gk9a['field_total_de_recursos'],
        y=gk9a.index,
        name="Total de recursos aprovados(BRL)",
        mode='lines+markers',
        text= list(gk9a.index), # list(ShortNames_Fiocruz.keys()),
        customdata = gk9a['N° Projetos'],
        hovertemplate=
        "<b>%{text}</b><br><br>" +
        "Total de recursos (BRL): %{x:$,.0f}<br>" +
        "N° de projetos: %{customdata:.0f}<br>" +
        "<extra></extra>",
        # text=df['text'],               
        # hoverinfo='text',                   #Pass the 'text' column to the hoverinfo parameter to customize the tooltip
        line = dict(color='#3ff698', width=3,dash='dashdot'),#Specify the color of the line
        marker=dict(color='LightSkyBlue',
            size=2)
        ),
        1,2)                   #The line chart uses the secondary y-axis 
    

    # formattedList =["%.2s" % i for i in list(gk9a['field_total_de_recursos'].values)]

    for k in list(gk9a.index):
        fig.add_annotation(x=gk9a.loc[k,'field_total_de_recursos'],y=k,text=np.round(1e-6*gk9a.loc[k,'field_total_de_recursos'],2),
                           showarrow=False,font=dict(color='white'),bgcolor="#ff7f0e", opacity=0.8,row=1,col=2)
    
    # --- TOTAIS ---#
    # fig.add_trace(                           #Add the second chart (line chart) to the figure
    #     go.Scatter(
    #     x=gk9x['field_total_de_recursos'],
    #     y=gk9x.index,
    #     name="Total de recursos solicitados (BRL)",
    #     mode='lines+markers',
    #     text= list(gk9x.index), # list(ShortNames_Fiocruz.keys()), 
    #     customdata = gk9x['N° Projetos'],
    #     hovertemplate=
    #     "<b>%{text}</b><br><br>" +
    #     "Total de recursos (BRL): %{x:$,.0f}<br>" +
    #     "N° de projetos: %{customdata:.0f}<br>" +
    #     "<extra></extra>",
    #     # text=df['text'],               
    #     # hoverinfo='text',                   #Pass the 'text' column to the hoverinfo parameter to customize the tooltip
    #     line = dict(color='#3ff543', width=3,dash='dashdot'),#Specify the color of the line
    #     marker=dict(color='orangered',
    #         size=8)
    #     ),
    #     1,2)                   #The line chart uses the secondary y-axis 
    
    
    # for k in list(gk9x.index):
    #     fig.add_annotation(x=gk9x.loc[k,'field_total_de_recursos'],y=k,text=np.round(1e-6*gk9x.loc[k,'field_total_de_recursos'],2),showarrow=False,font=dict(color='white'),row=1,col=2)

    
    fig.update_layout(hoverlabel_bgcolor='#DAEEED',  #Change the background color of the tooltip to light blue
                # title_text="Housing Market Trends: Raleigh, NC", #Add a chart title
                # title_font_family="Times New Roman",
                # title_font_size = 20,
                # title_font_color="darkblue", #Specify font color of the title
                # title_x=0.46, #Specify the title position
                margin=dict(l=5, r=5, t=5, b=5),
                yaxis=dict(
                    showticklabels=True,
                    domain=[0, 1],
                    showgrid = True,
                ),
                yaxis2=dict(
                    showticklabels=True,
                    domain=[0, 1],
                ),
                xaxis=dict(
                        tickangle = 0,
                        showgrid = True,
                        zeroline = True,
                        showline = True,
                        #showticklabels = True,
                        #dtick="M1", #Change the x-axis ticks to be monthly
                        ),
                xaxis2=dict(
                        zeroline=False,
                        showticklabels=True,
                        showgrid=True,
                        domain=[0.47, 1],
                        side='top',
                    ),
                legend = dict(orientation = 'h', xanchor = "center", x = 0.45, y= 1.11), #Adjust the legend position
                xaxis_title='Número de Projetos',
                xaxis2_title='Total de recuros (BRL)')
    
    fig.update_layout(
        # xaxis=dict(
        #     tickangle=90,
        #     # tickfont=dict(family="Rockwell", color="crimson", size=14),
        #     # tickvals=list(ShortNames_Fiocruz.keys()),
        #     # ticktext=list(ShortNames_Fiocruz.values()),
        #     tickvals=list(gk9x.index),
        #     # ticktext= [ShortNames_Fiocruz[x] for x in list(gk9x.index)],
        # ),
        xaxis2 = dict(color='#3ff698'),
        yaxis2=dict(
            # color='#f70f13',
            # color = '#3ff698',
            tickvals = list(gk9x.index)

        ),
        xaxis = dict (color='#f18e50' ),
        yaxis=dict(
            # color='#f0497b',
            # color = '#f18e50',
            tickvals = list(gk9x.index)

        )
        )
    fig.layout.yaxis2.update(showticklabels=False)
    fig.update_layout(height = 1000)
    return fig





def figure10_load(gk9a,gk9b,gk9x):
    fig=make_subplots(specs=[[{"secondary_y":True}]])
    fig.add_trace(                           #Add a bar chart to the figure
            go.Bar(
            x=gk9a.index,
            y=gk9a['N° Projetos'],
            name="Número de Projetos Aprovados",
            hoverinfo='none' ,               #Hide the hoverinfo
            marker_color='#eca375',#'#f0497b',#'#f27097', 
            marker_pattern_shape="x"    
            ),
            secondary_y=False)               #The bar chart uses the primary y-axis 
    
    fig.add_trace(                           #Add a bar chart to the figure
            go.Bar(
            x=gk9b.index,
            y=gk9b['N° Projetos'],
            name="Número de Projetos Submetidos",
            hoverinfo='none' ,               #Hide the hoverinfo
            marker_color='#f18e50',#'#f27097', 
                
            ),
            secondary_y=False)               #The bar chart uses the primary y-axis 
    
    fig.update_layout(barmode='stack')

    # --- APROBADOS ---#

    fig.add_trace(                           #Add the second chart (line chart) to the figure
        go.Scatter(
        x=gk9a.index,
        y=gk9a['field_total_de_recursos'],
        name="Total de recursos aprovados(BRL)",
        mode='lines+markers',
        text= list(gk9a.index), # list(ShortNames_Fiocruz.keys()), 
        customdata = gk9a['N° Projetos'],
        hovertemplate=
        "<b>%{text}</b><br><br>" +
        "Total de recursos (BRL): %{y:$,.0f}<br>" +
        "N° de projetos: %{customdata:.0f}<br>" +
        "<extra></extra>",
        # text=df['text'],               
        # hoverinfo='text',                   #Pass the 'text' column to the hoverinfo parameter to customize the tooltip
        line = dict(color='#3ff698', width=3,dash='dashdot'),#Specify the color of the line
        marker=dict(color='LightSkyBlue',
            size=8)
        ),
        secondary_y=True)                   #The line chart uses the secondary y-axis 
    
    # --- NO APROBADOS ---#
    # fig.add_trace(                           #Add the second chart (line chart) to the figure
    #     go.Scatter(
    #     x=gk6a.index,
    #     y=gk6b['field_total_de_recursos'],
    #     name="Total de recursos solicitados (BRL)",
    #     mode='lines+markers',
    #     text= list(gk6b.index), # list(ShortNames_Fiocruz.keys()), 
    #     customdata = gk6b['N° Projetos'],
    #     hovertemplate=
    #     "<b>%{text}</b><br><br>" +
    #     "Total de recursos (BRL): %{y:$,.0f}<br>" +
    #     "N° de projetos: %{customdata:.0f}<br>" +
    #     "<extra></extra>",
    #     # text=df['text'],               
    #     # hoverinfo='text',                   #Pass the 'text' column to the hoverinfo parameter to customize the tooltip
    #     line = dict(color='#3ff543', width=3),#Specify the color of the line
    #     marker=dict(color='LightSkyBlue',
    #         size=8)
    #     ),
    #     secondary_y=True)                   #The line chart uses the secondary y-axis 

    # --- TOTAIS ---#

    fig.add_trace(                           #Add the second chart (line chart) to the figure
        go.Scatter(
        x=gk9x.index,
        y=gk9x['field_total_de_recursos'],
        name="Total de recursos solicitados (BRL)",
        mode='lines+markers',
        text= list(gk9x.index), # list(ShortNames_Fiocruz.keys()), 
        customdata = gk9x['N° Projetos'],
        hovertemplate=
        "<b>%{text}</b><br><br>" +
        "Total de recursos (BRL): %{y:$,.0f}<br>" +
        "N° de projetos: %{customdata:.0f}<br>" +
        "<extra></extra>",
        # text=df['text'],               
        # hoverinfo='text',                   #Pass the 'text' column to the hoverinfo parameter to customize the tooltip
        line = dict(color='#3ff543', width=3),#Specify the color of the line
        marker=dict(color='orangered',
            size=8)
        ),
        secondary_y=True)                   #The line chart uses the secondary y-axis 

    fig.update_layout(hoverlabel_bgcolor='#DAEEED',  #Change the background color of the tooltip to light blue
                # title_text="Housing Market Trends: Raleigh, NC", #Add a chart title
                # title_font_family="Times New Roman",
                # title_font_size = 20,
                # title_font_color="darkblue", #Specify font color of the title
                # title_x=0.46, #Specify the title position
                margin=dict(l=5, r=5, t=5, b=5),
                xaxis=dict(
                        tickfont_size=10,
                        tickangle = 270,
                        showgrid = True,
                        zeroline = True,
                        showline = True,
                        #showticklabels = True,
                        #dtick="M1", #Change the x-axis ticks to be monthly
                        tickformat="%b\n%Y"
                        ),
                legend = dict(orientation = 'h', xanchor = "center", x = 0.45, y= 1.11), #Adjust the legend position
                yaxis_title='Número de Projetos',
                yaxis2_title='Total de recuros (BRL)')
    
    fig.update_layout(
    xaxis=dict(
        tickangle=90,
        # tickfont=dict(family="Rockwell", color="crimson", size=14),
        # tickvals=list(ShortNames_Fiocruz.keys()),
        # ticktext=list(ShortNames_Fiocruz.values()),
        tickvals=list(gk9x.index),
        # ticktext= [ShortNames_Fiocruz[x] for x in list(gk9x.index)],
    ),
    yaxis2=dict(
        # color='#f70f13',
        color = '#3ff698',

    ),
    yaxis=dict(
        # color='#f0497b',
        color = '#f18e50',

    )
    )

    # fig.for_each_trace(lambda t: t.update(name = ShortNames_Fiocruz[t.name]))

    return fig



def figure12_load(gk10a,gk10b,gk10x):
    fig=make_subplots(specs=[[{"secondary_y":True}]])
    fig.add_trace(                           #Add a bar chart to the figure
            go.Bar(
            x=gk10a.index,
            y=gk10a['N° Coordenadores'],
            name="Número de coordenadores agraciados",
            hoverinfo='none' ,               #Hide the hoverinfo
            marker_color='#72c5e5',#'#f0497b',#'#f27097', 
            marker_pattern_shape="x"    
            ),
            secondary_y=False)               #The bar chart uses the primary y-axis 
    
    fig.add_trace(                           #Add a bar chart to the figure
            go.Bar(
            x=gk10b.index,
            y=gk10b['N° Coordenadores'],
            name="Número de coordenadores não agraciados",
            hoverinfo='none' ,               #Hide the hoverinfo
            marker_color='#49a9cf',#'#f27097', 
                
            ),
            secondary_y=False)               #The bar chart uses the primary y-axis 
    
    fig.update_layout(barmode='stack')

    # --- APROBADOS ---#

    fig.add_trace(                           #Add the second chart (line chart) to the figure
        go.Scatter(
        x=gk10a.index,
        y=gk10a['field_total_de_recursos'],
        name="Total de recursos aprovados(BRL)",
        mode='lines+markers',
        text= list(gk10a.index), # list(ShortNames_Fiocruz.keys()), 
        customdata = gk10a['N° Coordenadores'],
        hovertemplate=
        "<b>%{text}</b><br><br>" +
        "Total de recursos (BRL): %{y:$,.0f}<br>" +
        "N° de coordenadores: %{customdata:.0f}<br>" +
        "<extra></extra>",
        # text=df['text'],               
        # hoverinfo='text',                   #Pass the 'text' column to the hoverinfo parameter to customize the tooltip
        line = dict(color='#3ff698', width=3, dash='dashdot'),#Specify the color of the line
        marker=dict(color='LightSkyBlue',
            size=8)
        ),
        secondary_y=True)                   #The line chart uses the secondary y-axis 
    
    # --- NO APROBADOS ---#
    # fig.add_trace(                           #Add the second chart (line chart) to the figure
    #     go.Scatter(
    #     x=gk6a.index,
    #     y=gk6b['field_total_de_recursos'],
    #     name="Total de recursos solicitados (BRL)",
    #     mode='lines+markers',
    #     text= list(gk6b.index), # list(ShortNames_Fiocruz.keys()), 
    #     customdata = gk6b['N° Projetos'],
    #     hovertemplate=
    #     "<b>%{text}</b><br><br>" +
    #     "Total de recursos (BRL): %{y:$,.0f}<br>" +
    #     "N° de projetos: %{customdata:.0f}<br>" +
    #     "<extra></extra>",
    #     # text=df['text'],               
    #     # hoverinfo='text',                   #Pass the 'text' column to the hoverinfo parameter to customize the tooltip
    #     line = dict(color='#3ff543', width=3),#Specify the color of the line
    #     marker=dict(color='LightSkyBlue',
    #         size=8)
    #     ),
    #     secondary_y=True)                   #The line chart uses the secondary y-axis 

    # --- TOTAIS ---#

    fig.add_trace(                           #Add the second chart (line chart) to the figure
        go.Scatter(
        x=gk10x.index,
        y=gk10x['field_total_de_recursos'],
        name="Total de recursos solicitados (BRL)",
        mode='lines+markers',
        text= list(gk10x.index), # list(ShortNames_Fiocruz.keys()), 
        customdata = gk10x['N° Coordenadores'],
        hovertemplate=
        "<b>%{text}</b><br><br>" +
        "Total de recursos (BRL): %{y:$,.0f}<br>" +
        "N° de coordenadores: %{customdata:.0f}<br>" +
        "<extra></extra>",
        # text=df['text'],               
        # hoverinfo='text',                   #Pass the 'text' column to the hoverinfo parameter to customize the tooltip
        line = dict(color='#3ff543', width=3),#Specify the color of the line
        marker=dict(color='orangered',
            size=8)
        ),
        secondary_y=True)                   #The line chart uses the secondary y-axis 

    fig.update_layout(hoverlabel_bgcolor='#DAEEED',  #Change the background color of the tooltip to light blue
                # title_text="Housing Market Trends: Raleigh, NC", #Add a chart title
                # title_font_family="Times New Roman",
                # title_font_size = 20,
                # title_font_color="darkblue", #Specify font color of the title
                # title_x=0.46, #Specify the title position
                margin=dict(l=5, r=5, t=5, b=5),
                xaxis=dict(
                        tickfont_size=10,
                        tickangle = 270,
                        showgrid = True,
                        zeroline = True,
                        showline = True,
                        #showticklabels = True,
                        #dtick="M1", #Change the x-axis ticks to be monthly
                        tickformat="%b\n%Y"
                        ),
                legend = dict(orientation = 'h', xanchor = "center", x = 0.45, y= 1.11), #Adjust the legend position
                yaxis_title='Número de coordenadores',
                yaxis2_title='Total de recuros (BRL)')
    
    fig.update_layout(
    xaxis=dict(
        tickangle=90,
        # tickfont=dict(family="Rockwell", color="crimson", size=14),
        # tickvals=list(ShortNames_Fiocruz.keys()),
        # ticktext=list(ShortNames_Fiocruz.values()),
        tickvals=list(gk10x.index),
        ticktext= [ShortNames_Fiocruz[x] for x in list(gk10x.index)],
    ),
    yaxis2=dict(
        # color='#f70f13',
        color = '#3ff698',

    ),
    yaxis=dict(
        # color='#f0497b',
        color = '#49a9cf',

    )
)

    # fig.for_each_trace(lambda t: t.update(name = ShortNames_Fiocruz[t.name]))

    return fig




@app.callback(
    [
        Output("eixo-select", "options"),
        Output("edital-select", "options"),
        Output("rodada-select", "options"),
        Output("status-select", "options"),
        Output("unidade-select","options")
        # Output("region-select-dropdown-outer", "children"),
    ],
    [Input("eixo-select", "value"),Input("edital-select", "value"),Input("rodada-select", "value"),Input("status-select", "value"),
    Input("unidade-select", "value"),Input("edital-select-all", "value")],
)
def update_dropdown(eixo_select,edital_select,rodada_select,status_select,unidade_select,select_all):
    value=None

    eixos = []
    eixos = []
    rodadas = []
    statuses = []
    unidades = []
    options_eixs=[]
    options_edit=[]
    options_rod=[]
    options_stats =[]
    options_unid = []


    if eixo_select is None or eixo_select ==[]:
        eixos = list(df_completo['Eixo'].unique())

    else:
        eixos = eixo_select

    ctx = dash.callback_context
    if ctx.triggered_id == "edital-select-all":
        editais = list(df_completo['field_edital_de_referencia:title'].unique())
        options = [{"label": i, "value": i} for i in editais]
        if select_all == ["All"]:
            edital_select = [i["value"] for i in options]
        else:
            edital_select = [i["value"] for i in options]

        
        editais = edital_select

    else:

        if edital_select is None or edital_select ==[]:
            editais = list(df_completo['field_edital_de_referencia:title'].unique())


        else:
            editais =  edital_select

    





    if rodada_select is None or rodada_select ==[]:
        rodadas = list(df_completo['field_rodada_produtos:name'].unique())
        
    else:
        rodadas=rodada_select

    if status_select is None or status_select ==[]:
        statuses = list(df_completo['field_situacao'].unique())
        
    else:
        statuses=status_select


    if unidade_select is None or unidade_select ==[]:
        unidades = list(df_completo['field_unidade_da_fiocruz:name'].unique())
        
    else:
        unidades= unidade_select
    # print(eixos)
    # print(editais)
    # print(rodadas)
    if eixo_select is None or eixo_select ==[]:
        eixos_set= list(df_completo[(df_completo['Eixo'].isin(eixos))&(df_completo['field_edital_de_referencia:title'].isin(editais))&(df_completo['field_rodada_produtos:name'].isin(rodadas))&(df_completo['field_situacao'].isin(statuses))&(df_completo['field_unidade_da_fiocruz:name'].isin(unidades))]['Eixo'].unique())
        options_eixs = [{"label": i, "value": i} for i in eixos_set]
    else:
        opts_eixs = list(df_completo[(df_completo['field_edital_de_referencia:title'].isin(editais))&(df_completo['field_rodada_produtos:name'].isin(rodadas))&(df_completo['field_situacao'].isin(statuses))&(df_completo['field_unidade_da_fiocruz:name'].isin(unidades))]['Eixo'].unique())
        options_eixs = [{"label": i, "value": i} for i in opts_eixs]

    if edital_select is None or edital_select ==[]:
        editais_set= list(df_completo[(df_completo['Eixo'].isin(eixos))&(df_completo['field_edital_de_referencia:title'].isin(editais))&(df_completo['field_rodada_produtos:name'].isin(rodadas))&(df_completo['field_situacao'].isin(statuses))&(df_completo['field_unidade_da_fiocruz:name'].isin(unidades))]['field_edital_de_referencia:title'].unique())
        options_edit = [{"label": i, "value": i} for i in editais_set]
    else:
        opts_edi = list(df_completo[(df_completo['Eixo'].isin(eixos))&(df_completo['field_rodada_produtos:name'].isin(rodadas))&(df_completo['field_situacao'].isin(statuses))&(df_completo['field_unidade_da_fiocruz:name'].isin(unidades))]['field_edital_de_referencia:title'].unique())
        options_edit = [{"label": i, "value": i} for i in opts_edi]


    if rodada_select is None or rodada_select ==[]:
        rodadas_set= list(df_completo[(df_completo['Eixo'].isin(eixos))&(df_completo['field_edital_de_referencia:title'].isin(editais))&(df_completo['field_rodada_produtos:name'].isin(rodadas))&(df_completo['field_situacao'].isin(statuses))&(df_completo['field_unidade_da_fiocruz:name'].isin(unidades))]['field_rodada_produtos:name'].unique())
        options_rod = [{"label": i, "value": i} for i in rodadas_set]

    else:
        opts_rod = list(df_completo[(df_completo['Eixo'].isin(eixos))&(df_completo['field_edital_de_referencia:title'].isin(editais))&(df_completo['field_situacao'].isin(statuses))&(df_completo['field_unidade_da_fiocruz:name'].isin(unidades))]['field_rodada_produtos:name'].unique())
        options_rod = [{"label": i, "value": i} for i in opts_rod]

    if status_select is None or status_select ==[]:
        status_set= list(df_completo[(df_completo['Eixo'].isin(eixos))&(df_completo['field_edital_de_referencia:title'].isin(editais))&(df_completo['field_rodada_produtos:name'].isin(rodadas))&(df_completo['field_situacao'].isin(statuses))&(df_completo['field_unidade_da_fiocruz:name'].isin(unidades))]['field_situacao'].unique())
        options_stats = [{"label": i, "value": i} for i in status_set]

    else:
        opts_stats = list(df_completo[(df_completo['Eixo'].isin(eixos))&(df_completo['field_edital_de_referencia:title'].isin(editais))&(df_completo['field_rodada_produtos:name'].isin(rodadas))&(df_completo['field_unidade_da_fiocruz:name'].isin(unidades))]['field_situacao'].unique())
        options_stats = [{"label": i, "value": i} for i in opts_stats]

    if unidade_select is None or unidade_select ==[]:
        unidades_set= list(df_completo[(df_completo['Eixo'].isin(eixos))&(df_completo['field_edital_de_referencia:title'].isin(editais))&(df_completo['field_rodada_produtos:name'].isin(rodadas))&(df_completo['field_situacao'].isin(statuses))&(df_completo['field_unidade_da_fiocruz:name'].isin(unidades))]['field_unidade_da_fiocruz:name'].unique())
        options_unid = [{"label": i, "value": i} for i in unidades_set]

    else:
        opts_unid = list(df_completo[(df_completo['Eixo'].isin(eixos))&(df_completo['field_edital_de_referencia:title'].isin(editais))&(df_completo['field_rodada_produtos:name'].isin(rodadas))&(df_completo['field_situacao'].isin(statuses))]['field_unidade_da_fiocruz:name'].unique())
        options_unid = [{"label": i, "value": i} for i in opts_unid]


    return (options_eixs,options_edit,options_rod,options_stats,options_unid)

 
@app.callback([Output('Main-Graph','figure'),
              Output('bar_chart','figure'),
              Output('pie_chart2','figure'),
              Output('bar_chartx', 'figure'),
              Output('bar_chartx2', 'figure'),
              Output('bar_chart3', 'figure'),
              Output("sub-estimation-indicator-led0",'figure'),
              Output("sub-estimation-indicator-led1",'figure'),
              Output("sub-estimation-indicator-led2",'figure'),
              Output("sub-estimation-indicator-led3",'figure'),
              Output('card_orcamento_solicitado','children'),
              Output('card_pessoas_equipe','children'),
              Output('card_coordenadores','children'),
              Output('card_bolsistas','children'),
              Output('pie_chart2z', 'figure'),
              Output('card_bar1','figure'),
              Output('card_bar2','figure'),
              Output('bar_chart_coord-ud','figure')],
            [Input('year-slider','value'),Input("eixo-select",'value'),Input("edital-select",'value'), Input('rodada-select','value'),Input('status-select','value'),Input("unidade-select", "value")])

def callback_piecharts(year_select,eixo_select,edital_select,rodada_select,status_select,unidade_select):

    fig2 = figure2()
    fig3 = figure3()
    fig4 = figure4()
    count = 0


    df_completo = df_completo_[(df_completo_['ano_creacao']<=year_select[1]) & (df_completo_['ano_creacao']>=year_select[0])]

    if eixo_select is None or eixo_select ==[]:
        eixo_select= list(df_completo['Eixo'].unique())

    if unidade_select is None or unidade_select ==[]:
        unidade_select= list(df_completo['field_unidade_da_fiocruz:name'].unique())

    if status_select is None or status_select ==[]:
        status_select= list(df_completo['field_situacao'].unique())

    if edital_select is None or edital_select ==[]:
        edital_select =  list(df_completo[df_completo['Eixo'].isin(eixo_select)&(df_completo['field_situacao'].isin(status_select))&(df_completo['field_unidade_da_fiocruz:name'].isin(unidade_select))]['field_edital_de_referencia:title'].unique())

    if rodada_select is None or rodada_select==[]:
        rodada_select= list(df_completo[(df_completo['Eixo'].isin(eixo_select))&(df_completo['field_situacao'].isin(status_select))&(df_completo['field_unidade_da_fiocruz:name'].isin(unidade_select))&(df_completo['field_edital_de_referencia:title'].isin(edital_select))]['field_rodada_produtos:name'].unique())

    # if unidade_select is None or unidade_select==[]:
    #     unidade_select= list(df_completo[(df_completo['Eixo'].isin(eixo_select))&(df_completo['field_edital_de_referencia:title'].isin(edital_select))]['field_rodada_produtos:name'].unique())


    df = df_completo[(df_completo['Eixo'].isin(eixo_select))&(df_completo['field_situacao'].isin(status_select))&(df_completo['field_unidade_da_fiocruz:name'].isin(unidade_select))&(df_completo['field_edital_de_referencia:title'].isin(edital_select))&(df_completo['field_rodada_produtos:name'].isin(rodada_select))].copy()
    df.loc[:,'N° Submissões'] = df['id']
    df.loc[:,'N° Projetos'] = df['id']

    gk3 = df.groupby(['Eixo'], as_index=False)['N° Submissões'].count()
    gk3['percentage'] = 100*gk3['N° Submissões']/gk3['N° Submissões'].sum()
    # gk3.to_csv('editaisxeixo.csv')
    fig3 = figure3_load(gk3)

    gk5 = df.groupby(['Eixo','field_edital_de_referencia:title','field_rodada_produtos:name'], as_index=False)['N° Submissões'].count()
    # gk5.to_csv('editaisxrodada.csv')
    fig2 = figure2_load(gk5)

    df1_c = df[df['field_situacao'].isin(['Recomendado','Não recomendado','Recomendado com ajustes'])]
    df2_c = df[df['field_situacao'].isin(['Submetido','Rascunho','Desistência'])]
    gk4_a = df1_c.groupby(['field_situacao'], as_index=False)['N° Submissões'].count()
    gk4_b = df2_c.groupby(['field_situacao'], as_index=False)['N° Submissões'].count()
    gk4_a['percentage'] = 100*gk4_a['N° Submissões']/gk4_a['N° Submissões'].sum()
    gk4_b['percentage'] = 100*gk4_b['N° Submissões']/gk4_b['N° Submissões'].sum()
    # gk4_a.to_csv('editaisxrecomendado.csv')
    # gk4_b.to_csv('editaisxsubmetido.csv')
    fig4 = figure4_load(gk4_a,gk4_b)
    
    # --
    field_situacao_set = ['Recomendado','Recomendado com ajustes']
    df_c = df[(df['field_situacao'].isin(field_situacao_set))]


    gk6a = df_c.groupby(['field_unidade_da_fiocruz:name']).agg({'field_total_de_recursos': 'sum', 'N° Projetos': 'count'})
    # gk6 = df_c.groupby(['field_unidade_da_fiocruz:name']).agg({'field_orcamento_final': 'sum', 'N° Projetos': 'count'})

    # gk6 = gk6.sort_values(by=['field_total_de_recursos'],ascending=False)
    gk6a = gk6a.sort_values(by=['N° Projetos'],ascending=False)


    df_d = df[~(df['field_situacao'].isin(field_situacao_set))]

    gk6b = df_d.groupby(['field_unidade_da_fiocruz:name']).agg({'field_total_de_recursos': 'sum', 'N° Projetos': 'count'})
    # gk6 = df_c.groupby(['field_unidade_da_fiocruz:name']).agg({'field_orcamento_final': 'sum', 'N° Projetos': 'count'})
    gk6b = gk6b.sort_values(by=['N° Projetos'],ascending=False)

    gk6x = df.groupby(['field_unidade_da_fiocruz:name']).agg({'field_total_de_recursos': 'sum', 'N° Projetos': 'count'})
    # gk6 = df_c.groupby(['field_unidade_da_fiocruz:name']).agg({'field_orcamento_final': 'sum', 'N° Projetos': 'count'})
    gk6x = gk6x.sort_values(by=['N° Projetos'],ascending=False)

    gk6a = gk6a.reindex_like(gk6x)
    gk6b = gk6b.reindex_like(gk6x)

    # gk6a.to_csv('unidadesxrecursosxaprov.csv')
    # gk6b.to_csv('unidadesxrecursosxnaoaprov.csv')


    # gk6a = gk6a.sort_values(by=['field_total_de_recursos'],ascending=False)
    # gk6b = gk6b.sort_values(by=['field_total_de_recursos'],ascending=False)

    
    fig7 = figure7x_load(gk6a,gk6b,gk6x)

    #---

    field_situacao_set = ['Recomendado','Recomendado com ajustes']
    df_e = df[(df['field_situacao'].isin(field_situacao_set))]
    gk8a = df_e.groupby(['ano_creacao']).agg({'field_total_de_recursos': 'sum', 'N° Projetos': 'count'})
    df_f = df[~(df['field_situacao'].isin(field_situacao_set))]
    gk8b = df_f.groupby(['ano_creacao']).agg({'field_total_de_recursos': 'sum', 'N° Projetos': 'count'})
    gk8x = df.groupby(['ano_creacao']).agg({'field_total_de_recursos': 'sum', 'N° Projetos': 'count'})

    # gk8a.to_csv('recomendadosxanocriacao.csv')
    # gk8b.to_csv('naorecomendadosxanocriacao.csv')
    # gk8x.to_csv('totaisxanocriacao.csv')

    fig9 = figure9_load(gk8a,gk8b,gk8x)

    #---
    field_situacao_set = ['Recomendado','Recomendado com ajustes']
    df_g = df[(df['field_situacao'].isin(field_situacao_set))]


    gk9a = df_g.groupby(['field_edital_de_referencia:title']).agg({'field_total_de_recursos': 'sum', 'N° Projetos': 'count'})
    # gk6a = df_g.groupby(['field_edital_de_referencia:title']).agg({'field_orcamento_final': 'sum', 'N° Projetos': 'count'})

    # gk9a = gk9a.sort_values(by=['field_total_de_recursos'],ascending=False)
    gk9a = gk9a.sort_values(by=['N° Projetos'],ascending=False)


    df_h = df[~(df['field_situacao'].isin(field_situacao_set))]

    gk9b = df_h.groupby(['field_edital_de_referencia:title']).agg({'field_total_de_recursos': 'sum', 'N° Projetos': 'count'})
    # gk9b = df_h.groupby(['field_edital_de_referencia:title']).agg({'field_orcamento_final': 'sum', 'N° Projetos': 'count'})
    gk9b = gk9b.sort_values(by=['N° Projetos'],ascending=False)

    gk9x = df.groupby(['field_edital_de_referencia:title']).agg({'field_total_de_recursos': 'sum', 'N° Projetos': 'count'})
    # gk9x = df_c.groupby(['field_edital_de_referencia:title']).agg({'field_orcamento_final': 'sum', 'N° Projetos': 'count'})
    gk9x = gk9x.sort_values(by=['N° Projetos'],ascending=False)

    gk9a = gk9a.reindex_like(gk9x)
    gk9b = gk9b.reindex_like(gk9x)

    # gk9a.to_csv('editalxrecursoaprov.csv')
    # gk9b.to_csv('editalxrecursonaoaprov.csv')


    # gk6a = gk6a.sort_values(by=['field_total_de_recursos'],ascending=False)
    # gk6b = gk6b.sort_values(by=['field_total_de_recursos'],ascending=False)

    # fig10 = figure10_load(gk9a,gk9b,gk9x)
    fig10 = figure10_loadx(gk9a,gk9b,gk9x)

    # ---
    count = gk5['N° Submissões'].sum()
    card1_fig = fig0_card(count)
    card2_fig = fig0_card(df_e.shape[0])
    recursos_aprov = round(gk6a['field_total_de_recursos'].sum(),1)
    card3_fig = fig1_card(recursos_aprov)
    recursos_solic = round(gk6x['field_total_de_recursos'].sum(),1)
    card4_fig = fig1_card(recursos_solic)
    # recursos = round(gk6['field_orcamento_final'].sum(),1)

    # CARDS 
    pessoa_equipe_val = str(pessoas_equipe(df))
    coordenadores_val = str(coordenadores(df))
    bolsistas_val = str(bolsistas(df))

    # bar plots cards
    field_situacao_set = ['Recomendado','Recomendado com ajustes']
    df_agra = df[(df['field_situacao'].isin(field_situacao_set))]
    coor_agra = coordenadores(df_agra)
    coor_naoagra = coordenadores(df) - coor_agra

    bol_agra = bolsistas(df_agra)
    bol_naoagra = bolsistas(df) - bol_agra

    fig11 = figure11(coor_agra, coor_naoagra)
    fig12 = figure11(bol_agra, bol_naoagra)

    #---------- coordenadores vs unidade

    field_situacao_set = ['Recomendado','Recomendado com ajustes']
    df.loc[:,'N° Coordenadores'] = df['id']
    df_i = df[(df['field_situacao'].isin(field_situacao_set))]


    gk10a = df_i.groupby(['field_unidade_da_fiocruz:name']).agg({'field_total_de_recursos': 'sum', 'N° Coordenadores': 'count'})
    df_ix = df_i[~df_i.duplicated(subset=['field_nome_coordenador'])].copy()


    gk10a_mask = df_ix.groupby(['field_unidade_da_fiocruz:name']).agg({'field_total_de_recursos': 'sum', 'N° Coordenadores': 'count'})
    gk10a.loc[:,'N° Coordenadores'] = gk10a_mask['N° Coordenadores']
    # gk6 = df_c.groupby(['field_unidade_da_fiocruz:name']).agg({'field_orcamento_final': 'sum', 'N° Projetos': 'count'})
    # gk6 = gk6.sort_values(by=['field_total_de_recursos'],ascending=False)
    gk10a = gk10a.sort_values(by=['N° Coordenadores'],ascending=False)


    df_j = df[~(df['field_situacao'].isin(field_situacao_set))]
    df_jx = df_j[~df_j.duplicated(subset=['field_nome_coordenador'])].copy()

    gk10b = df_j.groupby(['field_unidade_da_fiocruz:name']).agg({'field_total_de_recursos': 'sum', 'N° Coordenadores': 'count'})
    gk10b_mask = df_jx.groupby(['field_unidade_da_fiocruz:name']).agg({'field_total_de_recursos': 'sum', 'N° Coordenadores': 'count'})
    gk10b.loc[:,'N° Coordenadores'] = gk10b_mask['N° Coordenadores']
    # gk6 = df_c.groupby(['field_unidade_da_fiocruz:name']).agg({'field_orcamento_final': 'sum', 'N° Projetos': 'count'})
    gk10b = gk10b.sort_values(by=['N° Coordenadores'],ascending=False)


    df_sx = df[~df.duplicated(subset=['field_nome_coordenador'])].copy()
    gk10x = df.groupby(['field_unidade_da_fiocruz:name']).agg({'field_total_de_recursos': 'sum', 'N° Coordenadores': 'count'})
    # gk6 = df_c.groupby(['field_unidade_da_fiocruz:name']).agg({'field_orcamento_final': 'sum', 'N° Projetos': 'count'})
    gk10x_mask = df_sx.groupby(['field_unidade_da_fiocruz:name']).agg({'field_total_de_recursos': 'sum', 'N° Coordenadores': 'count'})
    gk10x.loc[:,'N° Coordenadores'] = gk10x_mask['N° Coordenadores']

    gk10x = gk10x.sort_values(by=['N° Coordenadores'],ascending=False)

    gk10a = gk10a.reindex_like(gk10x)
    gk10b = gk10b.reindex_like(gk10x)

    # gk6a.to_csv('unidadesxrecursosxaprov.csv')
    # gk6b.to_csv('unidadesxrecursosxnaoaprov.csv')
    # gk6a = gk6a.sort_values(by=['field_total_de_recursos'],ascending=False)
    # gk6b = gk6b.sort_values(by=['field_total_de_recursos'],ascending=False)

    
    fig13 = figure12_load(gk10a,gk10b,gk10x)





    #--------
    
    genero = ['field_genero','field_sexo']
    generoi = genero[0]
    gk7 = df.groupby([generoi], as_index=False)['N° Submissões'].count()
    gk7['percentage'] = 100*gk7['N° Submissões']/gk7['N° Submissões'].sum()

    fig8 = figure8_load(gk7)
                        
                


    return fig3,fig2,fig4,fig7,fig9,fig10,card1_fig,card2_fig,card3_fig,card4_fig,str(recursos_solic),pessoa_equipe_val,coordenadores_val,bolsistas_val,fig8,fig11,fig12,fig13

    # return fig3,fig2,fig4,fig7,fig9,count,recursos_aprov,recursos_solic,str(recursos_solic),pessoa_equipe_val,coordenadores_val,bolsistas_val,fig8



# @app.callback(
#     Output("download-xls", "data"),
#     [Input("download-button", "n_clicks"),Input('year-slider','value'),Input("eixo-select",'value'),Input("edital-select",'value'), Input('rodada-select','value'),Input('status-select','value'),Input("unidade-select", "value")],
#     prevent_initial_call=True,
# )
@app.callback(
    Output("download-xls", "data"),
    Input("download-button", "n_clicks"),
    State('year-slider','value'),State("eixo-select",'value'),State("edital-select",'value'), State('rodada-select','value'),State('status-select','value'),State("unidade-select", "value"),
    prevent_initial_call=True,
)
def callback_xls(n_clicks, year_select,eixo_select,edital_select,rodada_select,status_select,unidade_select):

    count = 0

    df_completo = df_completo_[(df_completo_['ano_creacao']<=year_select[1]) & (df_completo_['ano_creacao']>=year_select[0])]

    if eixo_select is None or eixo_select ==[]:
        eixo_select= list(df_completo['Eixo'].unique())

    if unidade_select is None or unidade_select ==[]:
        unidade_select= list(df_completo['field_unidade_da_fiocruz:name'].unique())

    if status_select is None or status_select ==[]:
        status_select= list(df_completo['field_situacao'].unique())

    if edital_select is None or edital_select ==[]:
        edital_select =  list(df_completo[df_completo['Eixo'].isin(eixo_select)&(df_completo['field_situacao'].isin(status_select))&(df_completo['field_unidade_da_fiocruz:name'].isin(unidade_select))]['field_edital_de_referencia:title'].unique())

    if rodada_select is None or rodada_select==[]:
        rodada_select= list(df_completo[(df_completo['Eixo'].isin(eixo_select))&(df_completo['field_situacao'].isin(status_select))&(df_completo['field_unidade_da_fiocruz:name'].isin(unidade_select))&(df_completo['field_edital_de_referencia:title'].isin(edital_select))]['field_rodada_produtos:name'].unique())

    # if unidade_select is None or unidade_select==[]:
    #     unidade_select= list(df_completo[(df_completo['Eixo'].isin(eixo_select))&(df_completo['field_edital_de_referencia:title'].isin(edital_select))]['field_rodada_produtos:name'].unique())


    df = df_completo[(df_completo['Eixo'].isin(eixo_select))&(df_completo['field_situacao'].isin(status_select))&(df_completo['field_unidade_da_fiocruz:name'].isin(unidade_select))&(df_completo['field_edital_de_referencia:title'].isin(edital_select))&(df_completo['field_rodada_produtos:name'].isin(rodada_select))].copy()
    df.loc[:,'N° Submissões'] = df['id']
    df.loc[:,'N° Projetos'] = df['id']


    # EDITAIS X EIXO - (FIGURA #1 )
    gk3 = df.groupby(['Eixo'], as_index=False)['N° Submissões'].count()
    gk3['percentage'] = 100*gk3['N° Submissões']/gk3['N° Submissões'].sum()


    # EDITAIS X RODADA - (FIGURA #2)
    gk5 = df.groupby(['Eixo','field_edital_de_referencia:title','field_rodada_produtos:name'], as_index=False)['N° Submissões'].count()
    

    # EDITAIS X APROVACAO
    df1_c = df[df['field_situacao'].isin(['Recomendado','Não recomendado','Recomendado com ajustes'])]
    df2_c = df[df['field_situacao'].isin(['Submetido','Rascunho','Desistência'])]
    gk4_a = df1_c.groupby(['field_situacao'], as_index=False)['N° Submissões'].count()
    gk4_b = df2_c.groupby(['field_situacao'], as_index=False)['N° Submissões'].count()
    gk4_a['percentage'] = 100*gk4_a['N° Submissões']/gk4_a['N° Submissões'].sum()
    gk4_b['percentage'] = 100*gk4_b['N° Submissões']/gk4_b['N° Submissões'].sum()


    
    # EDITAIS X UNIDADE
    field_situacao_set = ['Recomendado','Recomendado com ajustes']
    df_c = df[(df['field_situacao'].isin(field_situacao_set))]


    gk6a = df_c.groupby(['field_unidade_da_fiocruz:name']).agg({'field_total_de_recursos': 'sum', 'N° Projetos': 'count'})
    # gk6 = df_c.groupby(['field_unidade_da_fiocruz:name']).agg({'field_orcamento_final': 'sum', 'N° Projetos': 'count'})

    # gk6 = gk6.sort_values(by=['field_total_de_recursos'],ascending=False)
    gk6a = gk6a.sort_values(by=['N° Projetos'],ascending=False)


    df_d = df[~(df['field_situacao'].isin(field_situacao_set))]

    gk6b = df_d.groupby(['field_unidade_da_fiocruz:name']).agg({'field_total_de_recursos': 'sum', 'N° Projetos': 'count'})
    # gk6 = df_c.groupby(['field_unidade_da_fiocruz:name']).agg({'field_orcamento_final': 'sum', 'N° Projetos': 'count'})
    gk6b = gk6b.sort_values(by=['N° Projetos'],ascending=False)

    gk6x = df.groupby(['field_unidade_da_fiocruz:name']).agg({'field_total_de_recursos': 'sum', 'N° Projetos': 'count'})
    # gk6 = df_c.groupby(['field_unidade_da_fiocruz:name']).agg({'field_orcamento_final': 'sum', 'N° Projetos': 'count'})
    gk6x = gk6x.sort_values(by=['N° Projetos'],ascending=False)

    gk6a = gk6a.reindex_like(gk6x)
    gk6b = gk6b.reindex_like(gk6x)

    # EDITAIS X ANO

    field_situacao_set = ['Recomendado','Recomendado com ajustes']
    df_e = df[(df['field_situacao'].isin(field_situacao_set))]
    gk8a = df_e.groupby(['ano_creacao']).agg({'field_total_de_recursos': 'sum', 'N° Projetos': 'count'})
    df_f = df[~(df['field_situacao'].isin(field_situacao_set))]
    gk8b = df_f.groupby(['ano_creacao']).agg({'field_total_de_recursos': 'sum', 'N° Projetos': 'count'})
    gk8x = df.groupby(['ano_creacao']).agg({'field_total_de_recursos': 'sum', 'N° Projetos': 'count'})

    # EDITAIS X RECURSO
    field_situacao_set = ['Recomendado','Recomendado com ajustes']
    df_g = df[(df['field_situacao'].isin(field_situacao_set))]


    gk9a = df_g.groupby(['field_edital_de_referencia:title']).agg({'field_total_de_recursos': 'sum', 'N° Projetos': 'count'})
    # gk6a = df_g.groupby(['field_edital_de_referencia:title']).agg({'field_orcamento_final': 'sum', 'N° Projetos': 'count'})

    # gk9a = gk9a.sort_values(by=['field_total_de_recursos'],ascending=False)
    gk9a = gk9a.sort_values(by=['N° Projetos'],ascending=False)


    df_h = df[~(df['field_situacao'].isin(field_situacao_set))]

    gk9b = df_h.groupby(['field_edital_de_referencia:title']).agg({'field_total_de_recursos': 'sum', 'N° Projetos': 'count'})
    # gk9b = df_h.groupby(['field_edital_de_referencia:title']).agg({'field_orcamento_final': 'sum', 'N° Projetos': 'count'})
    gk9b = gk9b.sort_values(by=['N° Projetos'],ascending=False)

    gk9x = df.groupby(['field_edital_de_referencia:title']).agg({'field_total_de_recursos': 'sum', 'N° Projetos': 'count'})
    # gk9x = df_c.groupby(['field_edital_de_referencia:title']).agg({'field_orcamento_final': 'sum', 'N° Projetos': 'count'})
    gk9x = gk9x.sort_values(by=['N° Projetos'],ascending=False)

    gk9a = gk9a.reindex_like(gk9x)
    gk9b = gk9b.reindex_like(gk9x)


    #Coordenadores vs unidade

    field_situacao_set = ['Recomendado','Recomendado com ajustes']
    df.loc[:,'N° Coordenadores'] = df['id']
    df_i = df[(df['field_situacao'].isin(field_situacao_set))]


    gk10a = df_i.groupby(['field_unidade_da_fiocruz:name']).agg({'field_total_de_recursos': 'sum', 'N° Coordenadores': 'count'})
    df_ix = df_i[~df_i.duplicated(subset=['field_nome_coordenador'])].copy()


    gk10a_mask = df_ix.groupby(['field_unidade_da_fiocruz:name']).agg({'field_total_de_recursos': 'sum', 'N° Coordenadores': 'count'})
    gk10a.loc[:,'N° Coordenadores'] = gk10a_mask['N° Coordenadores']
    # gk6 = df_c.groupby(['field_unidade_da_fiocruz:name']).agg({'field_orcamento_final': 'sum', 'N° Projetos': 'count'})
    # gk6 = gk6.sort_values(by=['field_total_de_recursos'],ascending=False)
    gk10a = gk10a.sort_values(by=['N° Coordenadores'],ascending=False)


    df_j = df[~(df['field_situacao'].isin(field_situacao_set))]
    df_jx = df_j[~df_j.duplicated(subset=['field_nome_coordenador'])].copy()

    gk10b = df_j.groupby(['field_unidade_da_fiocruz:name']).agg({'field_total_de_recursos': 'sum', 'N° Coordenadores': 'count'})
    gk10b_mask = df_jx.groupby(['field_unidade_da_fiocruz:name']).agg({'field_total_de_recursos': 'sum', 'N° Coordenadores': 'count'})
    gk10b.loc[:,'N° Coordenadores'] = gk10b_mask['N° Coordenadores']
    # gk6 = df_c.groupby(['field_unidade_da_fiocruz:name']).agg({'field_orcamento_final': 'sum', 'N° Projetos': 'count'})
    gk10b = gk10b.sort_values(by=['N° Coordenadores'],ascending=False)


    df_sx = df[~df.duplicated(subset=['field_nome_coordenador'])].copy()
    gk10x = df.groupby(['field_unidade_da_fiocruz:name']).agg({'field_total_de_recursos': 'sum', 'N° Coordenadores': 'count'})
    # gk6 = df_c.groupby(['field_unidade_da_fiocruz:name']).agg({'field_orcamento_final': 'sum', 'N° Projetos': 'count'})
    gk10x_mask = df_sx.groupby(['field_unidade_da_fiocruz:name']).agg({'field_total_de_recursos': 'sum', 'N° Coordenadores': 'count'})
    gk10x.loc[:,'N° Coordenadores'] = gk10x_mask['N° Coordenadores']

    gk10x = gk10x.sort_values(by=['N° Coordenadores'],ascending=False)

    gk10a = gk10a.reindex_like(gk10x)
    gk10b = gk10b.reindex_like(gk10x)

    if not n_clicks:
        raise PreventUpdate
    else:

        # Create a Pandas Excel writer using XlsxWriter as the engine.
        writer = pd.ExcelWriter('Datafile.xlsx', engine='xlsxwriter')
        gk3.to_excel(writer, sheet_name='editaisxeixo.csv')
        gk5.to_excel(writer, sheet_name='editaisxrodada.csv')
        gk4_a.to_excel(writer, sheet_name='editaisxrecomendado.csv')
        gk4_b.to_excel(writer, sheet_name='editaisxsubmetido.csv')
        gk6a.to_excel(writer, sheet_name='unidadesxrecursosxaprov.csv')
        gk6b.to_excel(writer, sheet_name='unidadesxrecursosxnaoaprov.csv')
        gk6x.to_excel(writer, sheet_name='unidadesxrecursosxtotais.csv')
        gk8a.to_excel(writer, sheet_name='recomendadosxanocriacao.csv')
        gk8b.to_excel(writer, sheet_name='naorecomendadosxanocriacao.csv')
        gk8x.to_excel(writer, sheet_name='totaisxanocriacao.csv')
        gk9a.to_excel(writer, sheet_name='editalxrecursoaprov.csv')
        gk9b.to_excel(writer, sheet_name='editalxrecursonaoaprov.csv')
        gk9x.to_excel(writer, sheet_name='editalxrecursototais.csv')
        gk10a.to_excel(writer, sheet_name='coordxunidadexaprov.csv')
        gk10b.to_excel(writer, sheet_name='coordxunidadexnaoaprov.csv')
        gk10x.to_excel(writer, sheet_name='coordxunidadextotais.csv')

        # Close the Pandas Excel writer and output the Excel file.
        writer.save()

    # with pd.ExcelWriter('Datafile.xlsx') as writer:  
    #     gk3.to_excel(writer, sheet_name='editaisxeixo.csv')
    #     gk5.to_excel(writer, sheet_name='editaisxrodada.csv')
    #     gk4_a.to_excel(writer, sheet_name='editaisxrecomendado.csv')
    #     gk4_b.to_excel(writer, sheet_name='editaisxsubmetido.csv')
    #     gk6a.to_excel(writer, sheet_name='unidadesxrecursosxaprov.csv')
    #     gk6b.to_excel(writer, sheet_name='unidadesxrecursosxnaoaprov.csv')
    #     gk6x.to_excel(writer, sheet_name='unidadesxrecursosxtotais.csv')
    #     gk8a.to_excel(writer, sheet_name='recomendadosxanocriacao.csv')
    #     gk8b.to_excel(writer, sheet_name='naorecomendadosxanocriacao.csv')
    #     gk8x.to_excel(writer, sheet_name='totaisxanocriacao.csv')
    #     gk9a.to_excel(writer, sheet_name='editalxrecursoaprov.csv')
    #     gk9b.to_excel(writer, sheet_name='editalxrecursonaoaprov.csv')
    #     gk9x.to_excel(writer, sheet_name='editalxrecursototais.csv')
    #     gk10a.to_excel(writer, sheet_name='coordxunidadexaprov.csv')
    #     gk10b.to_excel(writer, sheet_name='coordxunidadexnaoaprov.csv')
    #     gk10x.to_excel(writer, sheet_name='coordxunidadextotais.csv')

    # dcc.send_data_frame(df.to_excel, "mydf.xlsx", sheet_name="Sheet_name_1")

    return dcc.send_file('Datafile.xlsx')


if __name__ == "__main__":
    app.run_server()

# if __name__ == "__main__":
#     app.run_server(debug=True)

    
