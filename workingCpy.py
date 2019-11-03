from django.shortcuts import render,redirect
from django.http import HttpResponse, StreamingHttpResponse
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import cv2
import pygame
checkmark = pygame.image.scale(pygame.image.load("checkmark.png"), (50, 50))
redo = pygame.image.scale(pygame.image.load("redo.png"), (50, 50))
import time
from PIL import Image
import cv2
import pygame
from PIL import Image
import requests
# If you are using a Jupyter notebook, uncomment the following line.
# %matplotlib inline
import matplotlib.pyplot as plt
from PIL import Image
from io import BytesIO
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import TextOperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import TextRecognitionMode
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials
import os
import sys
import time
import requests
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from io import BytesIO
import cv2
import pygame
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
from django.template.loader import render_to_string

def information(request):
    data = analyze()
    headers = data[0]
    print(headers)
    paragraphs = data[1]
    print(paragraphs)
    return render(request, 'myapp/info.html',context={'headers':headers,'paragraphs':paragraphs})
def home(request):
    return render(request,'myapp/home.html')
def upload(request):
    if(request.GET.get('mybtn')):
        capture()
    return render(request,'myapp/upload.html')
def capture():
    cap = cv2.VideoCapture(0)
    def draw_win():
        window.fill((255, 255, 255))
        window.blit(image, (0, 0))
        pygame.display.update()

    while True:
        ret, frame = cap.read()
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('c'):
            cv2.imwrite('image.png', frame)
            print("img captured")
            break
    cv2.waitKey(1)
    cv2.destroyAllWindows()
    for i in range (1,5):
        cv2.waitKey(1)
    cap.release()
    img = cv2.imread('image.png', cv2.IMREAD_UNCHANGED)
    height = img.shape[0]
    width = img.shape[1]
    pygame.init()
    window = pygame.display.set_mode((width,height))
    image = pygame.image.load('image.png')
    window.blit(image,(0,0))
    pygame.display.update()
    draw_win()
    done = False
    while not done:
        point_count = 2
        points = []
        while point_count > 0:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    coord = pygame.mouse.get_pos()
                    points.append(coord)
                    point_count -= 1
                draw_win()
            print(points)
            window.blit(checkmark, (width-50, 0))
            window.blit(redo, (width-50, 50))
            pygame.display.update()
            confirmed = False
            while not confirmed:
                pygame.draw.line(window, (255, 0, 0), (points[0][0], points[0][1]), (points[1][0], points[0][1]))
                pygame.draw.line(window, (255, 0, 0), (points[1][0], points[0][1]), (points[1][0], points[1][1]))
                pygame.draw.line(window, (255, 0, 0), (points[1][0], points[1][1]), (points[0][0], points[1][1]))
                pygame.draw.line(window, (255, 0, 0), (points[0][0], points[1][1]), (points[0][0], points[0][1]))
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if width-50 <= pygame.mouse.get_pos()[0] <= width and 100 <= pygame.mouse.get_pos[1] <= 150:
                            confirmed = True
                            done = True
                        if width-50 <= pygame.mouse.get_pos()[0] <= width and 150 <= pygame.mouse.get_pos[1] <= 200:
                            confirmed = True
    image = Image.open('image.png')
    left = points[0][0]
    right = points[1][0]
    top = points[0][1]
    bottom = points[1][1]
    cropped = image.crop((left, top, right, bottom))
    cropped.save("cropped.png")
def analyze():
        # Add your Computer Vision subscription key and endpoint to your environment variables.
    if 'COMPUTER_VISION_SUBSCRIPTION_KEY' in os.environ:
        subscription_key = os.environ['COMPUTER_VISION_SUBSCRIPTION_KEY']
    else:
        print("\nSet the COMPUTER_VISION_SUBSCRIPTION_KEY environment variable.\n**Restart your shell or IDE for changes to take effect.**")
        sys.exit()

    if 'COMPUTER_VISION_ENDPOINT' in os.environ:
        endpoint = os.environ['COMPUTER_VISION_ENDPOINT']

    ocr_url = endpoint + "vision/v2.1/ocr"
    params = {'language': 'unk', 'detectOrientation': 'true'}
    image_path = "cropped.png"
    # Read the image into a byte array
    image_data = open(image_path, "rb").read()
    # Set Content-Type to octet-stream
    headers = {'Ocp-Apim-Subscription-Key': subscription_key, 'Content-Type': 'application/octet-stream'}
    # put the byte array into your post request
    response = requests.post(ocr_url, headers=headers, params=params, data = image_data)

    analysis = response.json()

    # Extract the word bounding boxes and text.
    line_infos = [region["lines"] for region in analysis["regions"]]
    word_infos = []
    for line in line_infos:
        for word_metadata in line:
            for word_info in word_metadata["words"]:
                word_infos.append(word_info)
    string_list = []
    for dictn in word_infos:
    	string_list.append(dictn['text'])
    print(string_list)
    conc = ""
    for i in string_list:
    	conc+=i+" "
    formatted_list = conc.split(", ")
    stringsList = ["VEGETABLE_OIL","VEGETABLE OIL","Vegetable_Oil","Vegetable_oil","Vegetable oil","Vegetable Oil"]
    print(formatted_list)
    completeDataSet = return_info(formatted_list)
    print("\n\n\n\n\n\n\n****************")
    print("**RUNNING CODE**")
    print("***PROCESSING***")
    print("****************")

    print(cv2.__version__)
    return completeDataSet

def return_info(ingredients):
    fDH = []
    fDP = []
    source1 = True
    not_found = "Ingredient Not Found in Database"
    for indivString in ingredients:
        url = "https://www.bbc.co.uk/food/zest"
        uClient = uReq(url)
        try:
            try:
                form = indivString.split(" ")
                initFormatted = ""
                for i in range(0,len(form)):
                    initFormatted+=form[i]
                    if i!=len(form)-1:
                        initFormatted+="_"
                try:
                    url = "https://www.bbc.co.uk/food/"+initFormatted
                    print(url)
                    uClient = uReq(url)
                    print("got client")
                    source1 = True
                except:
                    url = "https://en.wikipedia.org/wiki/"+initFormatted
                    uClient = uReq(url)
                    source1 = False
            except:
                try:
                    url = "https://www.bbc.co.uk/food/"+indivString
                    uClient = uReq(url)
                    source1 = True
                except:
                    url = "https://en.wikipedia.org/wiki/"+indivString
                    uClient = uReq(url)
                    source1 = False
            html_page = uClient.read()
            uClient.close()
            page_soup = soup(html_page, "html.parser")
            #print("got to 148")
            if(source1 == True):
                formattedSoup = page_soup.find("div",{"class":"page-header__description"}).getText()
                #print("formatted soup bbc: " + str(formattedSoup))
            else:
                formatted_soup = page_soup.find("p")
                formattedSoup = formatted_soup.find_next_sibling("p").getText()
                #print("formatted soup wiki: " + str(formattedSoup))
            fin = format_string(str(formattedSoup))
            #print("Fin: "+fin)
            #print("got to 158")
            if(fin.isspace()==True):
            #	print("Data Not Attainable...")
                fDH.append(indivString)
                print("did first")
                fDP.append(not_found)
                print("did second")
                not_found+=" "
			#	finishedData.append(((indivString)+": "+"Ingredient Not Found in Database"))
            else:
                fDH.append(indivString)
                print("did first")
                fDP.append(fin)
                print("did second")
			#	finishedData.append(((indivString)+": "+fin))
			#	print("Data found, Appended")
        except:
            fDH.append(indivString)
            print("did first")
            fDP.append(not_found)
            print("did second")
            not_found+=" "
            #	finishedData.append(((indivString)+": "+"Ingredient Not Found in Database"))
    headers = {}
    paragraphs = {}
    print("fDH: "+"***".join(fDH))
    print("fDP: "+"***".join(fDP))
    for i in range(len(fDH)):
        headers[fDH[i]] = i
        paragraphs[fDP[i]] = i
        print(i)
        print(fDH[i])
        print(fDP[i])
    print(headers)
    print(paragraphs)
    dictArr = [headers,paragraphs]
    return dictArr

def format_string(unformatted):
	formatted = ""
	if("<" in unformatted):
		unfArr = unformatted.split("<")
		for i in unfArr:
			try:
				lhs, rhs = i.split(">")
				formatted+=rhs
			except:
				continue
		if("[" in formatted):
			unfArr1 = formatted.split("[")
			formatted1 = ""
			for j in unfArr1:
				try:
					lhs, rhs = j.split("]")
					formatted1+=rhs
				except:
					continue
			return formatted1
		return formatted
	else:
		return unformatted




# Create your views here.
