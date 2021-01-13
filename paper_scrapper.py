class Fbise(object):
    
    def __init__(self, homePage):
        self.homePage = homePage

    def getHomePage(self):
        return self.homePage
    
    def scrapPastPaperSite(self, site):
        'Parses a fbise old paper site'
        
        from urllib.request import urlopen
        scrappedSite = urlopen(site)
        '''
        with open('fbise.html','wb') as f:
            f.write(data.read())
        ''' 
        from bs4 import BeautifulSoup as BS
        soupedSite = BS(scrappedSite, 'html.parser')
        return soupedSite

    def extractClassDetails(self, scrappedSite):
        'Return Details that papers of which class are being extracted'
        heading = scrappedSite.find('th')
        heading = heading.find('b')
        heading = heading.text.split()
        return '%s_%s' % (heading[2], heading[5][:-1])


    def extractDownloadLinks(self, scrappedSite, subjects):
        import os
        subjects = [subjects[i].lower() for i in range(len(subjects))]
        classDetail = self.extractClassDetails(scrappedSite)
        f = open('%s.txt' % (classDetail), 'a')
        for tableData in scrappedSite.find_all('td'):
            linkTag = tableData.find('a')
            if(linkTag != None):
                subjectName = tableData.text.strip()                
                if(subjectName.lower() in subjects):
                    print(subjectName)
                    tempLink = linkTag.get('href')
                    tempLink = tempLink.replace(' ','%20')
                    subjectName = subjectName.replace(' ','_')
                    f.write('%s/%s %s_%s.pdf\n'%(self.getHomePage(),tempLink,
                        subjectName,classDetail))
        f.close()


    def listAllPapersYearsOfClass(self, siteLink, theClass):
        from urllib.request import urlopen
        tempSite = urlopen(siteLink)
        from bs4 import BeautifulSoup as BS
        soupedSite = BS(tempSite,'html.parser')
        tempLinks = list()
        for tableData in soupedSite.find_all('td'):
            linkTag = tableData.find('a')
            if (linkTag != None):
                className = linkTag.text.strip()
                className = className.lower()
                theClass = theClass.lower()
                if(className.startswith(theClass) and 'annual' in className):
                    tempLinks.append('%s/%s' %(self.getHomePage(),linkTag.get('href')))
                    

        return [tempLinks[i] for i in range(len(tempLinks)) if i%2==0]

def downloadPapers():
    import os
    files = list()
    for i in os.listdir(os.getcwd()):
        if(i.endswith('.txt')):
            files.append(i)
            
    for f in files:              
        dwnldCmnd = 'FOR /F "tokens=1,2* delims= " %%i in (%s) do "%%IDM_PATH%%" /d %%i /f %%j /a' % (f)
        os.system(dwnldCmnd)
        


if __name__ == "__main__":

    from bs4 import BeautifulSoup as BS    
    myFbise = Fbise('https://www.fbise.edu.pk')
    
    subjects = ['Biology', 'Physics', 'Chemistry',
                'English (Compulsory)', 'Urdu (Compulsory)', 'Islamic Education (Compulsory)']

    t = myFbise.listAllPapersYearsOfClass('https://www.fbise.edu.pk/Old%20Question%20Paper.php',
                                   'HSSC-I')

    del t[-3]
    del t[0]
    for i in t:     
        print('Scrapping : ',i)
        tempSite = myFbise.scrapPastPaperSite(i)
        myFbise.extractDownloadLinks(tempSite, subjects)
    

    downloadPapers()
