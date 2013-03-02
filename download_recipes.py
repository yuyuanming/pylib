import urllib2
import bs4
from os import path, makedirs

import threading
import Queue
import time
    
base_url = 'http://code.activestate.com'
recipe_base_url = 'http://code.activestate.com/recipes/langs/python/?page='
recpie_suffix_url = '/download/1/'
folder = 'recipes'
total_page = 3 # keep it up-to-date 
cnt = 0
minitask = 5

class store_recipe(threading.Thread):
    def __init__(self, q):
        threading.Thread.__init__(self)
        self.q = q 

    def run(self):
        try:
            url = self.q.get()
            url = url.split('?')[0]

            fn = folder + '/' + url[9:-1]+'.py'
            is_open = False
            if path.exists(fn): return
            is_open = True

            html = urllib2.urlopen(base_url + url + recpie_suffix_url).read()
            fout = open(fn, 'w')
            fout.write(html)
            global cnt
        except:
            print " RE-TRYING ",
            cnt = cnt - 1
            self.q.put(url)
            self.run()
        finally:
            cnt = cnt + 1
            print str(cnt)+"(" + str(threading.active_count())+")", url
            if is_open: fout.close()
            self.q.task_done()

def handle_page(page):
    print 'Start downloading page ' + str(page) + '.'

    # get recpies list on current page
    html = urllib2.urlopen(recipe_base_url + str(page)).read()
    soup = bs4.BeautifulSoup(html)
    recipes = [content.a['href'] 
            for content in soup.findAll(attrs={'class':'recipe-title'})]
    
    q = Queue.Queue()
    for k in xrange(0, len(recipes), minitask):
        for i in range(minitask):
            t = store_recipe(q)
            t.setDaemon(True)
            t.start()
        for i in range(minitask):
            q.put(recipes[k+i])
        q.join()
        q.queue.clear()
        del t
    del q

    #print recipes
    '''
    for url in recipes:
        store_recipe(url)
        t = threading.Thread(target=store_recipe, args=(url))
        t.daemon = True
        t.start()
        '''

    print 'Done page ' + str(page) + '.'
    print

if __name__=='__main__':
    if not path.exists('recipes'): 
        makedirs('recipes')
    for i in range(1, total_page+1):
        handle_page(i)
