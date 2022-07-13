#!/usr/bin/env python
# coding: utf-8

# ## Import Libraries

# In[2]:


import dash
from dash import html, dcc, no_update
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash_extensions import Lottie
from dash import Dash
import pandas as pd
import base64
import numpy as np
import io
from jupyter_dash import JupyterDash


# ## Encoding Images

# In[3]:


# --- PLEASE CHANGE THE IMAGE FILEPATH TO THE LOCATION ON YOUR LOCAL MACHINE ----
image_filename1 = r"C:\Users\65844\OneDrive\Desktop\SA_Jupyter\images\hugging-face-pngrepo-com.png" 
encoded_image1 = base64.b64encode(open(image_filename1, 'rb').read())

image_filename2 = r"C:\Users\65844\OneDrive\Desktop\SA_Jupyter\images\SA1.png" # replace with your own image
encoded_image2 = base64.b64encode(open(image_filename2, 'rb').read())

image_filename3 = r"C:\Users\65844\OneDrive\Desktop\SA_Jupyter\images\SA2.png" # replace with your own image
encoded_image3 = base64.b64encode(open(image_filename3, 'rb').read())

image_filename4 = r"C:\Users\65844\OneDrive\Desktop\SA_Jupyter\images\SA3.png" # replace with your own image
encoded_image4 = base64.b64encode(open(image_filename4, 'rb').read())


# ## Import our FINE-TUNED Model

# In[4]:


from transformers import pipeline

classifier = pipeline(model='RANG012/SENATOR')


# ## Design of our App

# In[7]:


# Define app
app = JupyterDash(__name__, external_stylesheets=[dbc.themes.QUARTZ])
app.title = "SENATOR - Sentiment Analysis"

app.layout = dbc.Container([
                            dbc.Row([
                                     html.H1('SENATOR', className='text-center fs-1 fst-italic fw-bold', style={'color':"yellow"})
                            ], className='mt-3'),
                            dbc.Row([
                                html.H1('with', className='text-center fs-3 fw-light')
                            ], className='mt-1'),
                            dbc.Row([
                                     html.A(
                                         html.Img(src='data:image/png;base64,{}'.format(encoded_image1.decode()), height="150px", width="150px"),
                                         href = 'https://huggingface.co/',
                                         target="_blank"
                                     )
                            ], className='mt-1 text-center'),
                            dbc.Row([
                                      html.P("What is Hugging Face?", className="fs-4 text-center", style={'text-decoration': 'underline'})      
                            ], className="mt-5"),
                            dbc.Row([
                                     dbc.Col([
                                              html.P(" Hugging Face is a startup in the Natural Language Processing (NLP) domain, offering its library of models for use by some of the A-listers including Apple and Bing.", className="fs-5 text-center", style={'color': 'lightgrey'})
                                     ], width = 7)
                            ], justify = 'center', className=' mt-1'),
                            dbc.Row([
                                      html.Div([
                                              html.Span("For this demo, we will be using a", className="fs-4"), 
                                              html.Span(" FINE-TUNED", className="fs-4 fw-bold", style={'color': 'red'}),
                                              html.Span(" DistilBERT model trained on the IMDB dataset", className="fs-4 fw-bold")   
                                      ], className="text-center") 
                            ], className="mt-3"),
                            dbc.Row([
                                     dbc.Col([
                                              dbc.Row([
                                                     html.P('Data Preprocessing & Models:', className='fs-5', style={'text-decoration': 'underline'})  
                                              ]),
                                              dbc.Row([
                                                       html.Img(src='data:image/png;base64,{}'.format(encoded_image2.decode()), height="350px", width="200px")
                                              ])
                                     ], width = 4),
                                     dbc.Col([
                                              dbc.Row([
                                                     html.P('Defining Training Parameters:', className='fs-5', style={'text-decoration': 'underline'})  
                                              ]),
                                              dbc.Row([
                                                       html.Img(src='data:image/png;base64,{}'.format(encoded_image3.decode()), height="350px", width="200px")
                                              ])
                                     ], width = 4, className='ms-1'),
                                     dbc.Col([
                                              dbc.Row([
                                                     html.P('Model Training:', className='fs-5', style={'text-decoration': 'underline'})  
                                              ]),
                                              dbc.Row([
                                                       html.Img(src='data:image/png;base64,{}'.format(encoded_image4.decode()), height="350px", width="200px")
                                              ])
                                     ], width = 3, className='ms-2')
                            ], className='mt-4'),
                            dbc.Row([
                                     dbc.Col([
                                              dbc.Row([
                                                    dbc.Label("Input Text",  className='fs-3'),
                                                    dbc.Textarea(size="lg", id='text-input', placeholder="Type Any Text You Like Here")
                                              ]),
                                              dbc.Row([
                                                       dbc.Col([
                                                                dbc.Button("Submit", id="submit-button", color="warning")
                                                       ], width=3)
                                              ], justify = 'center', className='mt-2')
                                     ], width = 6),
                                     dbc.Col([
                                              dbc.Row([
                                                       html.H3('Results:')
                                              ], className='text-center'),
                                              dbc.Row([], id ="result-text", className="mt-1 text-center")
                                     ])
                            ], className='mt-4'),
                    #------------------------------ UPLOAD FILE SECTION -----------------------
                            dbc.Row([
                                     html.Div([
                                             dcc.Upload(
                                                  id='upload-file',
                                                  children = html.Div([
                                                          'Drag and Drop or ',
                                                          html.A('Select File', href='#', style={'text-decoration': 'underline', 'color': 'aqua'})
                                                      ]),
                                                  style={
                                                      'width': '100%',
                                                      'height': '60px',
                                                      'lineHeight': '60px',
                                                      'borderWidth': '1px',
                                                      'borderStyle': 'dashed',
                                                      'borderRadius': '5px',
                                                      'textAlign': 'center',
                                                      'margin': '10px'
                                                    }
                                               ),
                                                dcc.Download(id="download-file")
                                    ])
                            ], className='mt-2') 
])

#------------------------ call back ------------------------------------

#------------------------------------------------------------
def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    if 'csv' in filename:
      df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))

    elif 'xlsx' in filename:
      df = pd.read_excel(io.BytesIO(decoded))

    elif 'xls' in filename:
      df = pd.read_excel(io.BytesIO(decoded))

    return df

#---------------------------------------------------

@app.callback(
    Output("result-text", "children"),
    Input("submit-button", "n_clicks"),
    State("text-input", "value"),
    prevent_initial_call=True
)
def submission(n, text):
  if  (n == 0) and (len(text) == 0) :
    return ''

  else:
    result = classifier([text])

    if result[0]['label'] == 'LABEL_0':
      sentiment = "Negative"
      color = 'red'
    else:
      sentiment = "Positive"
      color = 'yellow'

    return html.Div([
                     html.Div([
                            html.Span('Sentiment: ', className='fs-3'),
                            html.Span(sentiment, className='fw-bold fs-2', style={'color':color, 'text-decoration': 'underline'})
                     ]),
                     html.Div([
                            html.Span('Confidence: ', className='fs-3'),
                            html.Span(str(round(result[0]['score'], 2)), className='fw-bold fs-2', style={'text-decoration': 'underline'})
                     ], className='mt-3')
            ])
    

@app.callback(
    Output('download-file', 'data'),
    Input('upload-file', 'contents'),
    State('upload-file', 'filename'),
    #State('upload-file', 'last_modified')
    prevent_initial_call=True
)

def file_upload(content, filename):
  if content is not None:
    dataframe = parse_contents(content, filename)
    number_of_rows = dataframe.shape[0]  # Gives number of rows
    x = dataframe.columns   # returns a string of the name of the 1st column
    column = list(x)[0]
    predictions = []
    scores = []

    for i in range(number_of_rows):
      new_df = dataframe.iloc[i]
      sequence = new_df[column]
      results = classifier([sequence])

      if results[0]['label'] == 'LABEL_0':
        sent = "Negative"
      else:
        sent = "Positive"
      score = str(round(results[0]['score'], 2))
      predictions.append(sent)
      scores.append(score)

    dataframe['Sentiment'] = predictions
    dataframe['Confidence'] = scores
    return dcc.send_data_frame(dataframe.to_excel, "SENATOR_Ouput.xlsx", index=False, sheet_name="Updated_Sheet")


#-------------------------------


# In[8]:


app.run_server(mode='external')


# In[ ]:




