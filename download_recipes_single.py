import urllib2
import bs4
from os import path, makedirs
    
base_url = 'http://code.activestate.com'
recipe_base_url = 'http://code.activestate.com/recipes/langs/python/?page='
recpie_suffix_url = '/download/1/'
folder = 'tmp'
total_page = 10 # keep it up-to-date 
cnt = 0

def store_recipe(url):
    try:
        url = url.split('?')[0]
        fn = folder + '/' + url[9:-1]+'.py'
        #if path.exists(fn): return

        html = urllib2.urlopen(base_url + url + recpie_suffix_url).read()
        fout = open(fn, 'w')
        fout.write(html)
        global cnt
    except:
        print " RE-TRYING ",
        cnt = cnt - 1
        store_recipe(url)
    finally:
        cnt = cnt + 1
        #print str(cnt)+"(" + str(threading.active_count())+")", url
        print str(cnt), url
        fout.close()

def handle_page(page):
    print 'Start downloading page ' + str(page) + '.'

    # get recpies list on current page
    html = urllib2.urlopen(recipe_base_url + str(page)).read()
    soup = bs4.BeautifulSoup(html)
    recipes = [content.a['href'] 
            for content in soup.findAll(attrs={'class':'recipe-title'})]
    
    #print recipes
    for url in recipes:
        store_recipe(url)

    print 'Done page ' + str(page) + '.'
    print

if __name__=='__main__':
    if not path.exists(folder): 
        makedirs(folder)
    for i in range(1, total_page+1):
        handle_page(i)
