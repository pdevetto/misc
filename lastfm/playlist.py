# -*- coding: utf-8 -*-
import ConfigParser, sys, os, urllib2, json, time, shutil, filecmp
import Levenshtein

config = ConfigParser.ConfigParser()
config.read("config.ini")

def clean(chaine):
    #print chaine
    return chaine.lower().strip()
def decode(chaine):
    chaine = chaine.replace(u"\u2018", "'").replace(u"\u2019", "'")
    try:
        chaine = unicodedata.normalize('NFKD', chaine).encode('ascii','ignore')
        return chaine
    except:
        return chaine
def remove_accents(input_str):
    try:
        nkfd_form = unicodedata.normalize('NFKD', unicode(input_str))
        return u"".join([c for c in nkfd_form if not unicodedata.combining(c)])
    except:
        return input_str
def cc(i):
    return decode(clean(remove_accents(i)))
def getKey(item):
    return item[0]

class playlist:
    def __init__(self, limit, page=1, period="overall"):
        self.api_key = config.get("lastfm",'key')
        self.music_dir = config.get("lastfm",'directory')
        self.page = page
        self.mp_dir = config.get("lastfm",'mudir')
        self.user = config.get("lastfm",'user')
        self.dossier = os.listdir(self.music_dir)
        self.period = period

        self.limit = limit
        self.notfound = []
        #for i in req!

    def lastfm(self, meth):
        try:
            url = 'http://ws.audioscrobbler.com/2.0/?api_key='+self.api_key+'&autocorrect=1'+meth+'&format=json&page='+str(self.page)
            txt = urllib2.urlopen(url).read()
            return json.loads(txt)
        except urllib2.HTTPError:
            #print '\n Error : '+art
            return None

    def toptracks(self):
        url = '&method=user.gettoptracks&user='+self.user+'&limit='+self.limit+'&period='+self.period;
        req = self.lastfm(url)
        for i in req["toptracks"]["track"]:
            #if cc(i['artist']['name']) == "high tone":
            yield {'name':i['name'],'artist':cc(i['artist']['name'])}

    """Rechercher le dossier artiste, exacte ou levenshtein inferieure a longueur moins 2"""
    def findartist(self, artist):
        textlog = " find (" + artist + "):\n"
        lev = {}
        # Chaque artiste dans le dossier
        for art in self.dossier:
            ar = cc(art)
            # Correspondance exacte (pas de majuscule, pas d'accents, pas d'expace)
            if ar == artist:
                ##print "YES BITCH"
                return art
            # Distance de levenshtein: on stocke si pas trop de difference
            elif abs(len(ar) - len(artist)) < 5:
                l = Levenshtein.distance(ar, artist)
                if l < (len(art)/2):
                    if not l in lev.keys():
                        lev[l] = []
                    lev[l].append(art)
        # On process
        textlog += str(lev) + "\n"
        if lev != {} and len( lev[min(lev.keys())] ) == 1:
            ##print lev[min(lev.keys())][0]
            ##print "YES BIS BITCHY BITCH"
            return lev[min(lev.keys())][0]
        else:
            pass ##print textlog

    """Rechercher le dossier artiste, exacte ou levenshtein inferieure a longueur moins 2"""
    def findtrack(self, artist, track, i=0, lev=False):
        # Chaque truc dans le dossier
        base = self.music_dir + "/" + artist
        for fil in os.listdir(base):
            if os.path.isdir(base +"/"+ fil):
                ##print ("findtrack " + artist + " / " + fil + " - " + track)
                try:
                    for result in self.findtrack(artist + "/" + fil, track, i=i+1, lev=lev):

                        yield result
                except UnicodeDecodeError:
                    pass
            if os.path.isfile(base +"/"+ fil):
                if lev:
                    nfil = cc(clean(unicode(fil[:-4],'utf-8')))
                    ntr = cc(clean(track))
                    l = Levenshtein.distance(ntr, nfil)
                    if l < len(ntr):
                        ##print "lev |"  + ntr + "|" + nfil + "|"
                        ##print str(l) + " - " + str(len(cc(track)))
                        yield [l, base+"/"+fil]
                else:
                    if clean(track) in clean(unicode(fil,'utf-8')):
                        ##print base+"/"+fil
                        yield base+"/"+fil


    def mkdirs(self, li, pat):
        if li != []:
            dd = os.path.join(pat, li[0])
            if not os.path.isdir( dd ):
                ##print "mkdir(" + dd+")"
                os.mkdir(dd)
            return self.mkdirs(li[1:], dd)
        else:
            return pat

    def move(self, t):
        dirs = t[len(self.music_dir)+1:].split("/")
        new = self.mkdirs(dirs[:-1], self.mp_dir)
        dst = os.path.join(new, dirs[-1])
        if os.path.isfile( dst ):
            if os.path.getsize(t) != os.path.getsize(dst):
                os.remove(dst)
            else:
                return 1
        shutil.copyfile(t, dst)
        ##print "exist"
        #shutil.copyfile(t, dst)

    def findtrackall(self, a, i):
        for t in self.findtrack(a, i['name']):
            return t
        ##print "### :: " + i['artist'] + '-' + i['name'] + ""
        ties = []
        for t in self.findtrack(a, i['name'], lev=True):
            ties.append(t)
        if len(ties) == 0:
            return 0
        if len(ties) == 1:
            ##print ties[0][1]
            return ties[0][1]
        else:
            ties = sorted(ties, key=getKey)
            ##print ties[0][1]
            return ties[0][1]

    def run(self):
        file = time.strftime("TOP"+self.limit+"_%m%d%H%M.m3u")
        fo = open(file, 'w+')
        number = 0
        for i in self.toptracks():
            number += 1
            print number
            #for i in [{'name':u"The sound of silence",'artist':u"Simon and Garfunkel"}]:
            a = self.findartist(i['artist'])
            t = 0
            if a:
                t = self.findtrackall(a, i)
            if t == 0:
                t = self.findtrackall("Various Artists", i)
                ##print t
            if t != 0:
                fo.write(t+"\n")
                if os.path.isdir( self.mp_dir ):
                    self.move(t)
            else:
                #print "###########"
                #print i['artist'] + '-' + i['name']
                pass

        #print self.notfound
        #print '--finished--'
        fo.close()
    # <?xml version="1.0" encoding="UTF-8"?>
    # <playlist version="1" xmlns="http://xspf.org/ns/0/">
    # <trackList>
    #     <track><location>file:///media/data/Musique/Cypress Hill/2010 - Rise Up/Cypress Hill - Rise Up - 13 - Armed and Dangerous.mp3</location></track>
    #     <track><location>file:///media/data/Musique/The Black Keys/Attack &amp; Release/The Black Keys - Psychotic Girl.mp3</location></track>
    #     <track><location>file:///media/data/Musique/Odezenne/2012 - OVNI edition Louis XIV/13 - Hirondelles.mp3</location></track>
    # </trackList>
    # </playlist>
    pass

if len(sys.argv) == 0 :
    print "usage : python playlist.py length page"
else:
    if len(sys.argv) <= 1 :
        p = playlist(100)
    elif len(sys.argv) <= 2 :
        p = playlist(sys.argv[1])
    elif len(sys.argv) <= 3 :
        p = playlist(sys.argv[1], sys.argv[2])
    else: p = playlist(sys.argv[1], sys.argv[2], sys.argv[3])
    p.run()
