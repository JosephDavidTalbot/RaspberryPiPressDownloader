import requests, bs4, webbrowser, os, datetime, time, string, unicodedata, threading


#def downloadIssues(magazine, startIssue, endIssue):
def downloadIssues(magazine):
    try:
        os.stat(os.path.abspath(destination + magazine))
    except:
        os.mkdir(os.path.abspath(destination + magazine))
    startIssue = 1
    print('http://'+magazine+genericURLPrefix)
    tempres = requests.get('http://'+magazine+genericURLPrefix, headers=headers)
    soup = bs4.BeautifulSoup(tempres.text, "html.parser")
    latest = soup.select('.c-latest-issue__description a')[0]
    endIssue = int((latest.get('href')).replace('/issues/',''))+1
    for issueNumber in range(startIssue, endIssue):
        if not (os.path.exists(destination + magazine + "\\" + magazine + str(issueNumber) + ".pdf")):
            print('Downloading '+magazine+' issue #'+str(issueNumber))
            res = None
            if(magazine == "helloworld"):
                res = requests.get('http://'+magazine+genericURLPrefix+str(issueNumber)+helloworldSuffix, headers=headers)
                #print('http://'+magazine+genericURLPrefix+str(issueNumber)+helloworldSuffix)
            else:
                res = requests.get('http://'+magazine+genericURLPrefix+str(issueNumber)+genericURLSuffix, headers=headers)
                #print('http://'+magazine+genericURLPrefix+str(issueNumber)+genericURLSuffix)
            soup = bs4.BeautifulSoup(res.text, "html.parser")
            found = ""
            for link in soup.find_all('a'):
                current_link = link.get('href')
                if 'pdf' in current_link:
                    issuePath = (destination + magazine + "\\" + magazine + str(issueNumber) + ".pdf")
                    #print(issuePath)
                    issueFile = open(issuePath, 'wb')
                    #print('http://'+magazine+downloadURLPrefix+current_link)
                    if 'http' not in current_link:
                        res = requests.get('http://'+magazine+downloadURLPrefix+current_link)
                    else:
                        res = requests.get(current_link)
                    issueFile.write(res.content)
                    issueFile.close()
                    print(magazine+' issue #'+str(issueNumber)+' downloaded!')
                    found = "true"
            if not found:
                print("Error: "+magazine+" #"+str(issueNumber)+" download link not found.")

#Main

magazines = ["magpi","hackspace","wireframe","helloworld"]


genericURLPrefix='.raspberrypi.org/issues/'
genericURLSuffix='/pdf/download'
helloworldSuffix='/pdf'
downloadURLPrefix='.raspberrypi.org'

headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0", 'Accept-Language': 'en-US, en;q=0.5'}

destination = ".\\"

start = time.time()
startTime = datetime.datetime.now()

print('Starting...\nTime: '+str(startTime.hour)+':'+str(startTime.minute)+'\n\n')

#downloadIssues(magazinePrefixes[0], 1, 2)

"""
for magazine in magazines:
    downloadIssues(magazine)
"""


downloadThreads = []

for magazine in magazines:
    downloadThread = threading.Thread(target=downloadIssues, args=(magazine,))
    downloadThreads.append(downloadThread)
    downloadThread.start()
    time.sleep(0.5)

for downloadThread in downloadThreads:
    downloadThread.join()

print('All done!')
end = time.time()
endTime = datetime.datetime.now()
print('Elapsed time: '+(str(end - start))+'\nStart Time: '+str(startTime.hour)+':'+str(startTime.minute)+'\nEnd Time: '+str(endTime.hour)+':'+str(endTime.minute))
