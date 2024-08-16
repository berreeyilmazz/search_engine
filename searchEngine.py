def getPage(url):
  try:
    import urllib.request
    page = urllib.request.urlopen(url).read()
    page = page.decode("utf-8")
    return page
  except:
    return ""

def get_next_target(page):
    start_link = page.find('<a href=')
    if start_link == -1:
        return None, 0
    start_quote = page.find('"', start_link)
    end_quote = page.find('"', start_quote+1)
    url = page[start_quote + 1:end_quote]
    return url, end_quote

def get_all_links(page):
    links = []
    while True:
      url, endpos = get_next_target(page)
      if url:
        links.append(url)
        page = page[endpos:]
      else:
        break
    return links

def union(p,q):
    for e in q:
        if e not in p:
            p.append(e)
                 
def getNextTarget(page):
  startLink=page.find('<a href')
  startQuote = page.find('"', startLink+1)
  endQuote= page.find('"', startQuote+1 )
  url= page[startQuote+1: endQuote]
  return url, endQuote

def getAllLinks(page):
  urlList=[]
  myUrl, lastQuote = getNextTarget(page)
  page=page[lastQuote:]
  urlList.append(myUrl)
  
  while myUrl:
    myUrl, lastQuote = getNextTarget(page)
    page=page[lastQuote:]
    urlList.append(myUrl)
  return urlList

def lookUp(index, keyword):
    for item in index:
        if keyword == item: 
            return item
    return None

def addToIndex(index, keyword, url):
  key = lookUp(index,keyword)
  if key is None:
        index[keyword] = {
            "links": [],  # 1-b I created a dictionary in my "index" dictionary.
            "count": 0    
        }
  index[keyword]["links"].append(url)
  index[keyword]["count"] += 1
  

def addPageToIndex(index, url, c):
    content = c.split()
    for item in content:
        addToIndex(index,item,url)

def crawlWeb (seed) :
  tocrawl = [seed]
  crawled = []
  index = {}
  graph = {}
  while tocrawl :
    page = tocrawl.pop()
    if (page not in crawled) :
      content = getPage (page)
      addPageToIndex(index ,page ,content)
      outlinks = getAllLinks (content) 
      graph[page]=outlinks

      union ( tocrawl , getAllLinks ( content ) )
      crawled.append ( page )
  return index , graph 

#1-a  rest of the ranking algorithm

def questionB(key):  #1-b   an example input and output would be nice for us. thank you ::::::)
    for element in index:
            if element == key:
                print("Keyword: ", key)
                print(index[key]["count"], " result found.")   # 1.b
                print("Urls:")
                for url in index[key]["links"]:
                    print(url)

def lookUpLink(givenUrl):  # 1-c
    countKeys = 0
    
    for key in index:
        value = index[key]["links"]
        for item in value:
            if item == givenUrl:
                countKeys += 1
                break

    if (countKeys == 0):
        print("0 keyword found")
        return

    print(countKeys, " keyword found")

def countUrls(graph):
    urlList = []
    for urls in graph.values():
        for url in urls:
            if url not in urlList:
                urlList.append(url)
    return len(urlList)

def computeRanks(graph):
    d = 0.8  # damping factor
            
    N = countUrls(graph)
    numloops = 10 
    ranks = {}
    for key in graph:
        urls = graph[key]
        for url in urls:
            if url not in ranks:
                ranks[url] = 1 / N

    for i in range(numloops):
        newranks = {}
        for page in ranks:
            newrank = (1 - d) / N
            for keyword in graph:
                if page in graph[keyword]:
                    num_links = len(graph[keyword])
                    for link in graph[keyword]:
                        if link in ranks:
                            newrank += d * (ranks[link] / num_links)
                        else:
                            newrank += d * (0 / num_links)
            newranks[page] = newrank
        ranks = newranks

    return ranks

index, graph = crawlWeb("https://searchengineplaces.com.tr/")

ranks = computeRanks(graph)

total_rank = 0 
for key in ranks:
    total_rank += ranks[key]
    
for url in ranks:
    ranks[url] /= total_rank  # I wanted my rank to be between 0 and 1


lookUpLink("http://www.searchengineplaces.com.tr/oktayrecommends.html") #1-c
