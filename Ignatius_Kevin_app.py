from flask import Flask, render_template 
import pandas as pd
import requests
from bs4 import BeautifulSoup 
from io import BytesIO
import base64
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')


app = Flask(__name__) #don't change this code

def scrap(url):
    url_get = requests.get(url)
    soup = BeautifulSoup(url_get.content,"html.parser")
    
    table = soup.find('table', attrs={'class':'centerText newsTable2'}) 
    tr = table.find_all('tr') 

    place = [] #initiating a tuple

    for i in range(1, len(tr)):
        row = table.find_all('tr')[i]
        tanggal = row.find_all('td')[0].text
        tanggal = tanggal.strip()
        kjual = row.find_all('td')[1].text
        kjual = kjual.strip()
        kbeli = row.find_all('td')[2].text
        kbeli = kbeli.strip()
    
        place.append((tanggal, kjual, kbeli))
    
    place = place[::-1]

    df = pd.DataFrame(place, columns = ('Tanggal','Jual', 'Beli')) 

    df['Jual'] = df['Jual'].str.replace(",",".")
    df['Beli'] = df['Beli'].str.replace(",",".")
    df['Jual'] = df['Jual'].astype('float64')
    df['Beli'] = df['Beli'].astype('float64')
    df.set_index("Tanggal")

    return df

@app.route("/")
def index():
    df = scrap('https://news.mifx.com/kurs-valuta-asing?kurs=JPY') #insert url here

    #This part for rendering matplotlib
    fig = plt.figure(figsize=(5,2),dpi=300)
    df.plot()
    
    #Do not change this part
    plt.savefig('plot1',bbox_inches="tight") 
    figfile = BytesIO()
    plt.savefig(figfile, format='png')
    figfile.seek(0)
    figdata_png = base64.b64encode(figfile.getvalue())
    result = str(figdata_png)[2:-1]
    #This part for rendering matplotlib

    #this is for rendering the table
    df = df.to_html(classes=["table table-bordered table-striped table-dark table-condensed"])

    return render_template("index.html", table=df, result=result)


if __name__ == "__main__": 
    app.run()
