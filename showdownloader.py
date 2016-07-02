try:
    import re
    import requests
    from bs4 import BeautifulSoup
    import datetime
    import subprocess
    import os
    import sys
    import time
    import pyautogui
    from collections import OrderedDict
except ImportError:
    print "!!Modules aren't properly installed!!"
    print "Please go through the Readme file and follow the steps"
    print "Exiting..."
    sys.exit()
od=OrderedDict()

def torr_download(url,minSize):
    headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0' }
    proxies={"https":"http://52.53.207.221:8083"}
    try:        
        response=requests.get(url)
        if response.raise_for_status():
            print "======================================================="
            print "Some error occured while connecting to website!"
            print "Please check your internet connection and your proxy connection!"
            print "Make sure 'https://kat.cr' is accessible"
            print "Downloading terminated!\nExiting...."
    except:
        print "======================================================="
        print "Couldn't connect to the website!"
        print "Please check your internet connection and your proxy connection!"
        print "Make sure 'https://kat.cr' is accessible"
        print "Exiting..."
        sys.exit()
        
    soup=BeautifulSoup(response.text,"html.parser")

    ##finding links and size
    rows=soup.find_all('tr',class_=["even","odd"])
    for row in rows:
        
        link=row.find_all('a',href=re.compile(r"^//torcache.net/torrent/"))
        #print link[0].get('href')          #type unicode
        size=row.find_all('td',class_="nobr center")
        #print size[0].text              #type unicode
        od[ link[0].get('href') ]= size[0].text

    ##finding and downloading the right file
    size,type_=minSize.split()
    size=float(size)
    type_=type_.upper()
        
    for lnks in od:        
        print "Fetching appropriate file.Please wait..."
        temp2=od[lnks].split()        
        if float(temp2[0]) >=size:
            try:
                r=requests.get("https:"+str(lnks),headers=headers)
                fname="seasondownload.torrent"
                with open(fname,'wb') as f:
                    print "======================================================="
                    print "Success!Downloading..."
                    for chunk in r.iter_content(chunk_size=100000):
                        if chunk:
                            f.write(chunk)
                            f.flush()
                break
            except requests.exception.RequestException as e:
                print "======================================================="
                print "Error occured:",e
                print "Downloading another file!"
                continue
    print ">>>>>>>>> Torrent downloaded at "+os.getcwd()+"\fname"

    fpath=os.path.abspath(fname)

    ##opening the torrent using default torrent application
    ##for now works only on windows

    try:
        print "======================================================="
        print "Opening default application to download the file..."
        if subprocess.Popen(['start',fpath],shell=True):
            time.sleep(15)
            pyautogui.press('enter')
            print "======================================================="
            print "Successfully launched the application."
            print "Kudos!Your downloading has started."
            
    except:
        print "======================================================="
        print "Error occured while opening the application"
        print "Make sure some application to download torrent files is available on system!"
        print "Exiting..."
        sys.exit()
        
def main():
    print "======================================================="
    print "Make sure all the modules are properly installed"
    name=raw_input("Enter the tv series name [Eg- Suits,Sherlock]: ")
    season=raw_input("Enter the season number: ")
    ep=raw_input("Enter the episode number: ")
    if not ep.isdigit() or not season.isdigit():
        print "Invalid Input!!"
        print "Enter numeric values only [1,2,3,...]"
        print "Exiting...."
        sys.exit()
    sea=name.lower()
    
    keywords=name.split()
    temp=str("%20".join(keywords))
    baseurl="https://kat.cr/usearch/"
    url=baseurl+ temp + "%20category:tv%20season:"+season+"%20episode:"+ep+"/?field=size&sorder=asc"
    #print url
    ##size
    minSize=raw_input("Enter the minimum size of file you want to download\n[Eg-123 MB,3 GB] : ")
    
    try:
        temp=minSize.split()
        if  not temp[0].isdigit() or temp[1].upper() not in ["MB","GB"]:
            print "======================================================="
            print "Invalid input size!"
            print "Please enter the file size in right format.Eg-[352 MB]"
            print "Exiting..."
            sys.exit()
    except IndexError:
        print "Invalid input!\nCheck the example for correct size format.\nExiting.."
        sys.exit()
    ##time
    print "======================================================="
    print "Enter the time you want to start downloading the torrent"
    print "Please enter the date in specified format (dd-mm-yyyy-hh-mm) !!"
    print "Wrong format may cause error/failure in downloading."
    print "For example if you wish to download on 3rd June 2016 at 7:30 PM,enter the date and time as 03-06-2016-19-30 "
    
    down_time=raw_input("Enter the date and time : ")
    try:
        down_timeObj=datetime.datetime.strptime(down_time,"%d-%m-%Y-%H-%M")
        crossCheck=datetime.datetime.strftime(down_timeObj,"%d-%m-%Y-%H-%M")
    except :
        print "Invalid time input\nPlease enter corrent date and time in format specified\nExiting..."
        sys.exit()

    if down_timeObj<datetime.datetime.now():
        print "Invalid time input.Please re-run and enter correct time."
        print "Exiting..."
        sys.exit()
    print "======================================================="
    print "All good!"
    print "Sit back and relax,your downloading will start at specified time"
    print "Time left : "+ str(down_timeObj-datetime.datetime.now())
    while datetime.datetime.now()<down_timeObj:
        time.sleep(1)

    print "It's downloading time already!! "
    #downloading function call
    torr_download(url,minSize)

if __name__ =='__main__':main()
