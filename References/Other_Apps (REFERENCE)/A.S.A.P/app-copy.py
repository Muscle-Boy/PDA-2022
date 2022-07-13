from cmath import e
import dash
from dash import html, dcc, no_update
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash_extensions import Lottie
from dash import Dash
import plotly.express as px
import pandas as pd
import base64
import numpy as np
import base64
from PIL import Image
import io
import cv2
import pymongo
import flask

import tensorflow as tf
from tensorflow.keras.models import load_model
import os
import sys

from transformers import pipeline

#-----------------------------------------------------------------------------------------------------------
def parse_image(contents):
  content_type, content_string = contents.split(',')
  # Decode the bas64 encoded string
  decoded_data = base64.b64decode(content_string)
  image = Image.open(io.BytesIO(decoded_data))
  # Convert from RGB -> BGR (openCV)
  image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
  return image_cv


def parse_text(contents):
  content_type, content_string = contents.split(',')
  # Decode the bas64 encoded string
  decoded_data = base64.b64decode(content_string)
  text = decoded_data.decode("utf-8")
  return text


def generate_image_card(encoded_image):
  return dbc.Col([
                  dbc.Card(
                    dbc.CardBody([
                            html.Img(src='data:image/png;base64,{}'.format(encoded_image), height="320px", width="260px")
                    ])
                )
          ], className='ms-3 mt-2', width = 3)


def generate_text_card(text, label, score):
    return dbc.Col([
                    dbc.Card(
                        dbc.CardBody([
                            html.P(text, className='fs-4'),
                            html.P("Sentiment: " + label, className='display-6'),
                            html.P("Score: " + score, className='display-6')
                        ])
                    )
    ], className='ms-3 mt-2', width = 3)


def text_processing(text):
    prediction = classifier([text])
    if prediction[0]['label'] == 'LABEL_0':
        label = 'NEGATIVE'
    
    elif prediction[0]['label'] == 'LABEL_1':
        label = 'POSITIVE'

    score = str(round(prediction[0]['score'], 2))

    return label, score


def image_processing(image):
  output = image.copy()
  image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

  input_Tensor = tf.convert_to_tensor(image, dtype=tf.uint8)
  input_Tensor = input_Tensor[tf.newaxis, ...]

  # Feed our tensor image into our saved OD model
  detections = OD_model(input_Tensor)

  bboxs = detections['detection_boxes'][0].numpy()
  classIndexes = detections['detection_classes'][0].numpy().astype(np.int32)
  classScores = detections['detection_scores'][0].numpy()

  # Carry out NON-MAXIMA SUPPRESSION AND THRESHOLDING on the bounding boxes 
  # and give the indexes of bounding boxes kept in the form of a list
  bboxes_indexes = tf.image.non_max_suppression(bboxs, classScores, max_output_size=100, 
                                          iou_threshold = 0.5, score_threshold = 0.5)


  # Important when converting the bounding box coordinates to their original coordinates
  imHeight, imWidth, imChannels = output.shape


  if len(bboxs) > 0:
    for i in bboxes_indexes:

      # Extract one element at a time in the bboxs list and convert it to a tuple "()"" 
      bbox = tuple(bboxs[i].tolist())
      confidence = round(100*classScores[i])

      # [IMPORTANT STEP] Here we extract the STRING class label
      classIndex = classIndexes[i]
      class_name = label_map_dict_number_to_name[classIndex]

      # Here we prepare the text to be drawn ontop of the bounding box
      display = '{}: {}%'.format(class_name, confidence)

      # Unpack the bbox coordinates
      ymin, xmin, ymax, xmax = bbox

      # Convert the coordinates to their original values
      xmin, xmax, ymin, ymax = (int(xmin*imWidth), int(xmax*imWidth), int(ymin*imHeight), int(ymax*imHeight))


      # Draw the rectangle and text (COLOUR IS ACCORDING TO THE CLASS [if - elif statements])
      if class_name == "Soldier":
        #cv2.rectangle(image, start_point, end_point, color, thickness)
        cv2.rectangle(output, (xmin, ymin), (xmax, ymax), (30, 105, 210), 1)
        # cv2.putText(image, text, org, font, fontScale, color[, thickness[, lineType[, bottomLeftOrigin]]])
        cv2.putText(output, display, (xmin, ymin - 10), cv2.FONT_HERSHEY_PLAIN, 1.5, (30, 105, 210), 2)
        # [AESTHETICS] We will add "lines" to our bounding box to make it look more pleasant
        lineWidth = min(int((xmax-xmin)*0.2), int((ymax-ymin)*0.2))

        #----- cv2.line(image, start_point, end_point, color, thickness)----------
        cv2.line(output, (xmin,ymin), (xmin + lineWidth, ymin), (30, 105, 210), 5)
        cv2.line(output, (xmin,ymin), (xmin, ymin + lineWidth), (30, 105, 210), 5)

        cv2.line(output, (xmax,ymin), (xmax - lineWidth, ymin), (30, 105, 210), 5)
        cv2.line(output, (xmax,ymin), (xmax, ymin + lineWidth), (30, 105, 210), 5)

        cv2.line(output, (xmin,ymax), (xmin + lineWidth, ymax), (30, 105, 210), 5)
        cv2.line(output, (xmin,ymax), (xmin, ymax - lineWidth), (30, 105, 210), 5)

        cv2.line(output, (xmax,ymax), (xmax - lineWidth, ymax), (30, 105, 210), 5)
        cv2.line(output, (xmax,ymax), (xmax, ymax - lineWidth), (30, 105, 210), 5)
        #-------------------------------------------------------------------------


      elif class_name == "Civilian":
        cv2.rectangle(output, (xmin, ymin), (xmax, ymax), (255, 255, 224), 1)
        cv2.putText(output, display, (xmin, ymin - 10), cv2.FONT_HERSHEY_PLAIN, 1.5, (255, 255, 224), 2)

        # [AESTHETICS] We will add "lines" to our bounding box to make it look more pleasant
        lineWidth = min(int((xmax-xmin)*0.2), int((ymax-ymin)*0.2))

        #----- cv2.line(image, start_point, end_point, color, thickness)----------
        cv2.line(output, (xmin,ymin), (xmin + lineWidth, ymin), (255, 255, 224), 5)
        cv2.line(output, (xmin,ymin), (xmin, ymin + lineWidth), (255, 255, 224), 5)

        cv2.line(output, (xmax,ymin), (xmax - lineWidth, ymin), (255, 255, 224), 5)
        cv2.line(output, (xmax,ymin), (xmax, ymin + lineWidth), (255, 255, 224), 5)

        cv2.line(output, (xmin,ymax), (xmin + lineWidth, ymax), (255, 255, 224), 5)
        cv2.line(output, (xmin,ymax), (xmin, ymax - lineWidth), (255, 255, 224), 5)

        cv2.line(output, (xmax,ymax), (xmax - lineWidth, ymax), (255, 255, 224), 5)
        cv2.line(output, (xmax,ymax), (xmax, ymax - lineWidth), (255, 255, 224), 5)
        #-------------------------------------------------------------------------


      elif class_name == "Weapon":
        cv2.rectangle(output, (xmin, ymin), (xmax, ymax), (60, 20, 220), 1)
        cv2.putText(output, display, (xmin, ymin - 10), cv2.FONT_HERSHEY_PLAIN, 1.5, (60, 20, 220), 2)

        # [AESTHETICS] We will add "lines" to our bounding box to make it look more pleasant
        lineWidth = min(int((xmax-xmin)*0.2), int((ymax-ymin)*0.2))

        #----- cv2.line(image, start_point, end_point, color, thickness)----------
        cv2.line(output, (xmin,ymin), (xmin + lineWidth, ymin), (60, 20, 220), 5)
        cv2.line(output, (xmin,ymin), (xmin, ymin + lineWidth), (60, 20, 220), 5)

        cv2.line(output, (xmax,ymin), (xmax - lineWidth, ymin), (60, 20, 220), 5)
        cv2.line(output, (xmax,ymin), (xmax, ymin + lineWidth), (60, 20, 220), 5)

        cv2.line(output, (xmin,ymax), (xmin + lineWidth, ymax), (60, 20, 220), 5)
        cv2.line(output, (xmin,ymax), (xmin, ymax - lineWidth), (60, 20, 220), 5)

        cv2.line(output, (xmax,ymax), (xmax - lineWidth, ymax), (60, 20, 220), 5)
        cv2.line(output, (xmax,ymax), (xmax, ymax - lineWidth), (60, 20, 220), 5)
        #-------------------------------------------------------------------------

      elif class_name == "Tank":
        cv2.rectangle(output, (xmin, ymin), (xmax, ymax), (205, 0, 0), 1)
        cv2.putText(output, display, (xmin, ymin - 10), cv2.FONT_HERSHEY_PLAIN, 1.5, (205, 0, 0), 2)

        # [AESTHETICS] We will add "lines" to our bounding box to make it look more pleasant
        lineWidth = min(int((xmax-xmin)*0.2), int((ymax-ymin)*0.2))

        #----- cv2.line(image, start_point, end_point, color, thickness)----------
        cv2.line(output, (xmin,ymin), (xmin + lineWidth, ymin), (205, 0, 0), 5)
        cv2.line(output, (xmin,ymin), (xmin, ymin + lineWidth), (205, 0, 0), 5)

        cv2.line(output, (xmax,ymin), (xmax - lineWidth, ymin), (205, 0, 0), 5)
        cv2.line(output, (xmax,ymin), (xmax, ymin + lineWidth), (205, 0, 0), 5)

        cv2.line(output, (xmin,ymax), (xmin + lineWidth, ymax), (205, 0, 0), 5)
        cv2.line(output, (xmin,ymax), (xmin, ymax - lineWidth), (205, 0, 0), 5)

        cv2.line(output, (xmax,ymax), (xmax - lineWidth, ymax), (205, 0, 0), 5)
        cv2.line(output, (xmax,ymax), (xmax, ymax - lineWidth), (205, 0, 0), 5)
        #-------------------------------------------------------------------------
        

      elif class_name == "Armoured Vehicle":
        cv2.rectangle(output, (xmin, ymin), (xmax, ymax), (0, 215, 255), 1)
        cv2.putText(output, display, (xmin, ymin - 10), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 215, 255), 2)

        # [AESTHETICS] We will add "lines" to our bounding box to make it look more pleasant
        lineWidth = min(int((xmax-xmin)*0.2), int((ymax-ymin)*0.2))

        #----- cv2.line(image, start_point, end_point, color, thickness)----------
        cv2.line(output, (xmin,ymin), (xmin + lineWidth, ymin), (0, 215, 255), 5)
        cv2.line(output, (xmin,ymin), (xmin, ymin + lineWidth), (0, 215, 255), 5)

        cv2.line(output, (xmax,ymin), (xmax - lineWidth, ymin), (0, 215, 255), 5)
        cv2.line(output, (xmax,ymin), (xmax, ymin + lineWidth), (0, 215, 255), 5)

        cv2.line(output, (xmin,ymax), (xmin + lineWidth, ymax), (0, 215, 255), 5)
        cv2.line(output, (xmin,ymax), (xmin, ymax - lineWidth), (0, 215, 255), 5)

        cv2.line(output, (xmax,ymax), (xmax - lineWidth, ymax), (0, 215, 255), 5)
        cv2.line(output, (xmax,ymax), (xmax, ymax - lineWidth), (0, 215, 255), 5)
        #-------------------------------------------------------------------------

      elif class_name == "Helicopter":
        cv2.rectangle(output, (xmin, ymin), (xmax, ymax), (204, 50, 153), 1)
        cv2.putText(output, display, (xmin, ymin - 10), cv2.FONT_HERSHEY_PLAIN, 1.5, (204, 50, 153), 2)

        # [AESTHETICS] We will add "lines" to our bounding box to make it look more pleasant
        lineWidth = min(int((xmax-xmin)*0.2), int((ymax-ymin)*0.2))

        #----- cv2.line(image, start_point, end_point, color, thickness)----------
        cv2.line(output, (xmin,ymin), (xmin + lineWidth, ymin), (204, 50, 153), 5)
        cv2.line(output, (xmin,ymin), (xmin, ymin + lineWidth), (204, 50, 153), 5)

        cv2.line(output, (xmax,ymin), (xmax - lineWidth, ymin), (204, 50, 153), 5)
        cv2.line(output, (xmax,ymin), (xmax, ymin + lineWidth), (204, 50, 153), 5)

        cv2.line(output, (xmin,ymax), (xmin + lineWidth, ymax), (204, 50, 153), 5)
        cv2.line(output, (xmin,ymax), (xmin, ymax - lineWidth), (204, 50, 153), 5)

        cv2.line(output, (xmax,ymax), (xmax - lineWidth, ymax), (204, 50, 153), 5)
        cv2.line(output, (xmax,ymax), (xmax, ymax - lineWidth), (204, 50, 153), 5)
        #-------------------------------------------------------------------------

      else:
        cv2.rectangle(output, (xmin, ymin), (xmax, ymax), (128, 0, 128), 1)
        cv2.putText(output, display, (xmin, ymin - 10), cv2.FONT_HERSHEY_PLAIN, 1.5, (128, 0, 128), 2)

        # [AESTHETICS] We will add "lines" to our bounding box to make it look more pleasant
        lineWidth = min(int((xmax-xmin)*0.2), int((ymax-ymin)*0.2))

        #----- cv2.line(image, start_point, end_point, color, thickness)----------
        cv2.line(output, (xmin,ymin), (xmin + lineWidth, ymin), (128, 0, 128), 5)
        cv2.line(output, (xmin,ymin), (xmin, ymin + lineWidth), (128, 0, 128), 5)

        cv2.line(output, (xmax,ymin), (xmax - lineWidth, ymin), (128, 0, 128), 5)
        cv2.line(output, (xmax,ymin), (xmax, ymin + lineWidth), (128, 0, 128), 5)

        cv2.line(output, (xmin,ymax), (xmin + lineWidth, ymax), (128, 0, 128), 5)
        cv2.line(output, (xmin,ymax), (xmin, ymax - lineWidth), (128, 0, 128), 5)

        cv2.line(output, (xmax,ymax), (xmax - lineWidth, ymax), (128, 0, 128), 5)
        cv2.line(output, (xmax,ymax), (xmax, ymax - lineWidth), (128, 0, 128), 5)

  return output

#--------------------------------------------------------------------------------------------------------------
# ADD ENVIRONMENT PATH:
# os.environ['Path']+='/app/Tensorflow/research'
# sys.path.append('/app/Tensorflow/research')

from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as viz_utils

#--------------------------------------------------------------------------------------------------------------
logo = '/app/Images/icons8-easy-100.png' 
encoded_logo = base64.b64encode(open(logo, 'rb').read())

image_filename1 = '/app/Images/hugging-face-pngrepo-com.png' # replace with your own image
encoded_image1 = base64.b64encode(open(image_filename1, 'rb').read())

image_filename2 = '/app/Images/SA1.png' # replace with your own image
encoded_image2 = base64.b64encode(open(image_filename2, 'rb').read())

image_filename3 = '/app/Images/SA2.png' # replace with your own image
encoded_image3 = base64.b64encode(open(image_filename3, 'rb').read())

image_filename4 = '/app/Images/SA3.png' # replace with your own image
encoded_image4 = base64.b64encode(open(image_filename4, 'rb').read())
#--------------------------------------------------------------------------------------------------------------

# PROVIDE PATH TO LABEL MAP
PATH_TO_LABELS = '/app/OD_files/label_map.pbtxt'

# PROVIDE PATH TO SAVED MODEL FILE (.pb)
PATH_TO_SAVED_MODEL = '/app/OD_files/saved_model'

# Load our labels and IDs
label_map_dict = label_map_util.get_label_map_dict(PATH_TO_LABELS)

# Flip the order of the dictionary (now it will have INTEGERS as its keys and STRINGS(class labels) as its values)
label_map_dict_number_to_name = {v: k for k, v in label_map_dict.items()}

# LOAD OUR TENSORFLOW MODEL
OD_model = tf.saved_model.load(PATH_TO_SAVED_MODEL)

# LOAD OUR NLP MODEL
classifier = pipeline(model='RANG012/SENATOR')
#--------------------------------------------------------------------------------------------------------------
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    #"background": "grey"
}

sidebar = html.Div(
    [
        html.H2("Menu", className="display-4"),
        html.Hr(),
        html.P(
            "Select Any Option Below", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact", className="mt-4"),
                dbc.NavLink("View Results", href="/view-results", active="exact", className="mt-4"),
                dbc.NavLink("Collection", href="/collection", active="exact", className="mt-4"),
                dbc.NavLink("SENATOR", href="/senator", active="exact", className="mt-5"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)
#--------------------------------------------------------------------------------------------------------------
# Connect to MongoDB
client = pymongo.MongoClient('mongodb://0.0.0.0:27017')
db = client['ASAP-Database']
information = db.data_collection

# Define the FLASK app.server => Gunicorn WSGI
server = flask.Flask(__name__)

# Define app
app = Dash(server=server, external_stylesheets=[dbc.themes.MINTY], meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}], suppress_callback_exceptions=True)

app.title = "A.S.A.P"
ENCODED_IMAGE_LIST = []   # list of STRINGS
ENCODED_TEXT_LIST = []  # list of *TUPLES* [(text, label, score)]
FILENAMES = []   # list of STRINGS

#-------------------------------------------------------------------------------
home_page = dbc.Row([
                  dbc.Row([
                           dbc.Col([
                                    html.Img(src='data:image/png;base64,{}'.format(encoded_logo.decode()), height="120px", width="120px", className="mt-4")
                           ], width=1),
                           dbc.Col([
                                    html.P("A.S.A.P", className="fw-bold ms-4 mt-4 text-primary", style={"font-size":"80px"})
                           ], width=4)
                  ], className="justify-content-center"),

                  dbc.Row([
                            html.Div([
                                      html.Span("A", className="fs-3 fw-bold",style={'text-decoration': 'underline'}),
                                      html.Span("  ", className="fs-3"),
                                      html.Span("S", className="fs-3 fw-bold",style={'text-decoration': 'underline'}),
                                      html.Span("imple", className="fs-3"),
                                      html.Span("  ", className="fs-3"),
                                      html.Span("A", className="fs-3 fw-bold",style={'text-decoration': 'underline'}),
                                      html.Span("pplication", className="fs-3"),
                                      html.Span("  ", className="fs-3"),
                                      html.Span("P", className="fs-3 fw-bold",style={'text-decoration': 'underline'}),
                                      html.Span("rogram", className="fs-3"),
                            ])
                  ], className = "text-center"),

                  dbc.Row([
                           dbc.Col([
                              html.P("User Guide", className='fs-3 fw-bold', style={'text-decoration': 'underline'}),
                              html.Div([
                                        html.Span("Users can ", className='fs-4'),
                                        html.Span("UPLOAD", className="fw-bold fs-4", style={"color": "red"}),
                                        html.Span(" document(s) containing either an ", className='fs-4'),
                                        html.Span("IMAGE", className="fw-bold fs-4", style={"color": "red"}),
                                        html.Span(" or a ", className='fs-4'),
                                        html.Span("TEXT", className="fw-bold fs-4", style={"color": "red"}),
                                        html.Span(" below. The document(s) will then be processed and the results can be viewed by clicking the 'View Results' \
                                        option in the menu. Otherwise, they can view ", className='fs-4'),
                                        html.Span("ALL", className="fw-bold fs-4", style={"color": "blue"}),
                                        html.Span(" of the results gathered from previous users of A.S.A.P by clicking the 'Collection' option in the menu.", className='fs-4')
                                    ]),
                                    html.Div(html.P("PLEASE WAIT FOR A MOMENT FOR THE DOCUMENT TO BE PROCESSED UPON UPLOADING IT"), className='fs-6 fw-bold mt-3', 
                                    style={"color": "orangered"})
                           ], className="text-center", width = 9)
                  ], className='justify-content-center mt-4 ms-2'),


                  dbc.Row([
                           dbc.Col([
                            html.Div([
                                  dcc.Upload(
                                      id='file-upload',
                                      children=html.Div([
                                            'Drag and Drop or ',
                                            html.A('Select File', className='fw-bold', style={"text-decoration": "underline", "color": "lightblue"})
                                      ], className='fs-4'),
                                      style={                   
                                        'width': '85%',
                                        'height': '60px',
                                        'lineHeight': '60px',
                                        'borderWidth': '1px',
                                        'borderStyle': 'dashed',
                                        'borderRadius': '5px',
                                        'textAlign': 'center',
                                        'margin': '10px',
                                        'background': 'AliceBlue'
                                      }
                                    )
                              ])
                        ], width = 9)
                  ], className='justify-content-center mt-5 ms-5'),
                 dbc.Row(id='status', className='mt-3 fs-5 text-center')    

]) # End of home_page
#-------------------------------------------------------------------------------

view_results_page = dbc.Row([
                             dbc.Row([
                                  dbc.Col([
                                      html.P("Result of Your Input(s):", className='display-4 fw-bold'),
                                      html.Hr(),
                                      html.Div(html.P("PLEASE WAIT FOR A MOMENT FOR THE RESULT(S) TO BE DISPLAYED"), className='fs-6 fw-bold mt-2', 
                                    style={"color": "orangered"})
                                  ], className='text-center ms-5', width = 8)
                      ], className='justify-content-center mt-3'),

                      dbc.Row(id='pg2-content', className='justify-content-end'),
                      dbc.Row(id='pg2-content-text', className='justify-content-end'),
                      dbc.Row([
                               dbc.Col([
                                        dbc.Button("Store Result(s)", size='lg', id='store-result-button')
                               ], width = 3)
                      ], className='justify-content-end mt-4 ms-5'),
                      dbc.Row(id='status-pg2', className='mt-3 fs-5 text-end') 

]) # End of view_results_page

#-------------------------------------------------------------------------------
database_page = dbc.Row([
            dbc.Row([
                        dbc.Col([
                            html.P("Saved Results in A.S.A.P:", className='display-4 fw-bold'),
                            html.Hr()
                        ], className='text-center ms-5', width = 8)
            ], className='justify-content-center mt-3'),
            dbc.Row(id='pg3-content', className='justify-content-end'),
            dbc.Row(id='pg3-content-text', className='justify-content-end'),
]) # End of Database Page


#--------------------------------------------------------------------------------
senator_page = dbc.Row([
                            dbc.Row([
                                     html.H1('SENATOR', className='text-center fs-1 fst-italic fw-bold', style={'color':"darkgreen"})
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

                            dbc.Row([
                                     html.Div([
                                             dcc.Upload(
                                                  id='upload-file1',
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
                                                dcc.Download(id="download-file1")
                                    ])
                            ], className='mt-2')

])


#--------------------------------------------------------------------------------
app.layout = html.Div([
      sidebar,
      dcc.Store(id="Image_Decodings", storage_type='session'),
      dcc.Store(id="Filenames", storage_type='session'),
      dcc.Store(id="Text_Encodings", storage_type='session'),
      dcc.Location(id='url', refresh=False),
      html.Div(id='page-content')       
])


#------------------------------------ CALLBACKS -------------------------------------------------------------

# Index Callback
@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname'),
)
def display_page(pathname):
    if pathname == '/':
        return home_page
    elif pathname == '/view-results':
        return view_results_page
    elif pathname == '/collection':
        return database_page
    elif pathname == '/senator':
      return senator_page

# Home Page Callback
@app.callback(
    Output('status', 'children'),
    Output('Image_Decodings', 'data'),
    Output('Filenames', 'data'),
    Output('Text_Encodings', 'data'),
    Input('file-upload', 'contents'),
    State('file-upload', 'filename'),
    prevent_initial_call=True,
)

def check_and_process_upload(contents, filename):
  if contents is not None:
    if filename.split('.')[0] not in FILENAMES:     # Check for duplicate uploads
      FILENAMES.append(filename.split('.')[0])
      if ('png' in filename) or ('jpg' in filename):
        image = parse_image(contents)
        if image is None:
          result = "Image '{}' failed to process!".format(filename.split('.')[0])
          return [html.P(result, className="text-warning")], ENCODED_IMAGE_LIST, FILENAMES, ENCODED_TEXT_LIST
        processed_image = image_processing(image)
        encoded_image = cv2.imencode('.png', processed_image)[1]       # imendcode() returns ['true/false', ....]
        data_bytes = base64.b64encode(encoded_image)
        data = data_bytes.decode()
        ENCODED_IMAGE_LIST.append(data)   
        result = "Image '{}' is processed successfully!".format(filename.split('.')[0])
        return [html.P(result, className="text-success")], ENCODED_IMAGE_LIST, FILENAMES, ENCODED_TEXT_LIST

      elif 'txt' in filename:
        text = parse_text(contents)
        if len(text) == 0:
          result = "Text '{}' failed to process!".format(filename.split('.')[0])
          return [html.P(result, className="text-warning")], ENCODED_IMAGE_LIST, FILENAMES, ENCODED_TEXT_LIST
        label, score = text_processing(text)
        ENCODED_TEXT_LIST.append((text, label, score))
        result = "Text '{}' is processed successfully!".format(filename.split('.')[0])
        return [html.P(result, className="text-success")], ENCODED_IMAGE_LIST, FILENAMES, ENCODED_TEXT_LIST

      else:
        result = "Please upload either a TEXT or an IMAGE document only!"
        return [html.P(result, className="text-danger")], ENCODED_IMAGE_LIST, FILENAMES, ENCODED_TEXT_LIST

    else:
      result = "File '{}' has been processed before. Please upload a different file!".format(filename.split('.')[0])
      return [html.P(result, className="text-info")], ENCODED_IMAGE_LIST, FILENAMES, ENCODED_TEXT_LIST
  
  else:
    return '', ENCODED_IMAGE_LIST, FILENAMES, ENCODED_TEXT_LIST
  

# View-Result Callback
@app.callback(
    Output('pg2-content', 'children'),
    Output('pg2-content-text', 'children'),
    Output('status-pg2', 'children'),
    Input('Image_Decodings', 'data'),
    Input('Text_Encodings', 'data'),
    Input('store-result-button', 'n_clicks')
)

def generate_results(image_data, text_data, n):
    if ((image_data is not None) or (text_data is not None)) and (n is None):
        return [generate_image_card(i) for i in image_data], [generate_text_card(text, label, score) for (text, label, score) in text_data], ''
        
    elif ((image_data is not None) or (text_data is not None)) and (n is not None):
        # SAVING LOCAL RESULTS TO DATABASE
        for encoding in image_data:
            duplicate = False
            for data in information.find({"Type":"Image"}):
                if encoding == data['Encoding']:
                    duplicate = True
                    break
            if duplicate:
                continue
            
            else:
                record = [{
                    "Type": "Image",
                    "Encoding": encoding
                }]

                information.insert_many(record)
        #---------------------------------------

        for (text, label, score) in text_data:
            duplicate = False
            for data in information.find({"Type":"Text"}):
                if text == data['Text Content']:
                    duplicate = True
                    break
            if duplicate:
                continue
            
            else:
                record = [{
                    "Type": "Text",
                    "Text Content": text,
                    "Label": label,
                    "Score": score
                }]

                information.insert_many(record)
        result = "Result(s) have been saved successfully!"

        return [generate_image_card(i) for i in image_data], [generate_text_card(text, label, score) for (text, label, score) in text_data], [html.P(result, className='text-success')]

    else:
        return '', ''


# Database Callback
@app.callback(
    Output('pg3-content', 'children'),
    Output('pg3-content-text', 'children'),
    Input('Image_Decodings', 'data'),
    Input('Text_Encodings', 'data')
)

def DB_results(image_data, text_data):
    if (image_data is not None) or (text_data is not None):
        # LOADING IMAGES/TEXTS FROM DATABASE
        db_images = []
        db_texts = []
        for x in information.find({"Type":"Image"}):
            data = x['Encoding']
            db_images.append(data)

        for y in information.find({"Type":"Text"}): 
            text = y['Text Content']
            label = y['Label']
            score = y['Score']
            db_texts.append((text, label, score))
        return [generate_image_card(i) for i in db_images], [generate_text_card(text, label, score) for (text, label, score) in db_texts]


    else:
        # LOADING IMAGES/TEXTS FROM DATABASE
        db_images = []
        db_texts = []
        for x in information.find({"Type":"Image"}):
            data = x['Encoding']
            db_images.append(data)

        for y in information.find({"Type":"Text"}): 
            text = y['Text Content']
            label = y['Label']
            score = y['Score']
            db_texts.append((text, label, score))
        return [generate_image_card(i) for i in db_images], [generate_text_card(text, label, score) for (text, label, score) in db_texts]




# SENATOR Callback
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
    Output('download-file1', 'data'),
    Input('upload-file1', 'contents'),
    State('upload-file1', 'filename'),
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


#-------------------------------------------------------------
if __name__ == '__main__':
    app.run_server(debug=False)
