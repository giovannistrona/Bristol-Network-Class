from igraph import Graph, Layout, plot
from random import random
import string

def show_diam(vn,con,name):
	g = Graph.Erdos_Renyi(vn,con)
	g.vs['size'] = 10
	g.vs['color'] = 'darkblue'
	g.es['color'] = 'black'
	d = g.get_diameter(directed=False)
	lay = g.layout_fruchterman_reingold()
	plot(g,'./images/'+name,layout = lay,dpi = 600)
	g.es['color'] = '#00000020'
	dpath = g.es.select(_within=d)
	for e in dpath:
		g.es[e.index]['width'] = 2
		g.es[e.index]['color'] = 'darkblue'
	#lay = g.layout_reingold_tilford()
	#lay = g.layout_kamada_kawai()
	plot(g,'./images/diam_'+name,layout = lay,dpi = 600)





def plot_bk(g,layout,fname = 'movie.gif',res = 5,size = 500):
	layout.fit_into((0,0,0,size,size,size),keep_aspect_ratio=False)
	hs = size/2.0	
	for rot in range((360+(2*res))/res):
		for i in range(len(g.vs)):
			g.vs[i]['size']=int(round(30*(0.5+((1-abs(hs-layout[i][0])/hs)+(1-abs(hs-layout[i][1])/hs))/4.0)))
		layout.rotate(res,0,2)
		layout.fit_into((0,0,0,size,size,size),keep_aspect_ratio=False)
		xy=[[i[0],i[1]] for i in layout]
		z=[int(round(40*(0.5+i[2]/float(size*2)))) for i in layout]
		for i in range(len(z)):
			g.vs[i]['size']=z[i]
		plot(g,'./images/frames/'+str(rot)+'.png',vertex_frame_width=0,bbox=(size,size),layout=xy,dpi=300,margin=50)
	images = []
	for frame in range((360+(2*res))/res):
		filename = './images/frames/'+str(frame)+'.png'
		images.append(imageio.imread(filename))
		os.remove(filename)
	#kwargs_write = {'fps':5.0, 'quantizer':'nq'}
	imageio.mimsave(fname, images)


#show_diam(30,0.2,'prova.png')
#show_diam(10,0.2,'small.png')


###networks kinds
###directed/undirected
name = 'directed.png'
vn = 10
con = 0.2
g = Graph.Erdos_Renyi(vn,con,directed = True)
#g = Graph.Barabasi(10,1)
g = g.simplify()
g.vs['size'] = 15
g.vs['color'] = 'darkblue'
g.es['color'] = 'black'


#lay0 = g.layout_fruchterman_reingold()
lay=g.layout('kk3d')
plot_bk(g,lay,'./gifs/directed.gif',res=3)
#plot(g,'./images/'+name,layout = lay,dpi = 600)
g.to_undirected()
name = 'undirected.png'
plot_bk(g,lay,'./gifs/undirected.gif',res=3)
#plot(g,'./images/'+name,layout = lay,dpi = 600)

aaa = list(string.ascii_uppercase)
g.es['color'] = '#00000080'
for e in range(len(g.es)):
	g.es[e]['width'] = int(round(random()*10))+1


lay=g.layout('kk3d')	
plot_bk(g,lay,'./gifs/w_undirected.gif',res=3)
g.es['width'] = 1
xy=[[i[0],i[1]] for i in lay]
plot(g,'./images/undirected.png',layout = xy,dpi = 600)


plt.figure(figsize=(4,2))
g = Graph.Random_Bipartite(5,5,m = 10)
name = 'bipartite.png'
g.vs['size'] = 50

g.vs.select(type = True)['color'] = 'darkblue'
g.vs.select(type = False)['color'] = 'darkorange'

g.es['color'] = 'black'


#lay = g.layout_bipartite()
plot(g,'./images/'+name,layout = lay,dpi = 600,margin = 50)

g.to_directed()
>>> for i in range(len(g.es)):
...     g.es[i]['arrow_size'] = 2*(g.es[i]['width']/float(max(g.es['width'])))

for e in range(len(g.es)):
	g.es[e]['width'] = int(round(random()*10))+1

plot(g,'./images/bipartite_w_d.png',layout = lay,dpi = 600,margin = 50)

###edglist vs matrix unimode
name = 'edgelist.png'
vn = 5
con = 0.3
g = Graph.Erdos_Renyi(vn,con,directed = True)
#g = Graph.Barabasi(10,1)
g = g.simplify()
g.vs['size'] = 50
g.vs['color'] = 'white'
g.es['color'] = 'black'
g.vs['label'] = aaa[:len(g.vs)]
g.vs['label_size']=40

lay = g.layout_fruchterman_reingold()
plot(g,'./images/'+name,layout = lay,dpi = 300,bbox = (500,500),margin=50)


for i in g.es:
	s,t = i.tuple
	print g.vs['label'][s]+','+g.vs['label'][t]


m = g.get_adjacency()
for i in m:
	print i

######matrix bipartite
g = Graph.Random_Bipartite(2,3,m = 4)
lay = g.layout_bipartite()

name = 'edgelist_bipartite.png'
g.vs['size'] = 50
g.vs['color'] = 'white'
g.es['color'] = 'black'
g.vs['label'] = aaa[:len(g.vs)]
g.vs['label_size']=40

plot(g,'./images/'+name,layout = lay,dpi = 300,bbox = (500,500),margin=50)


for i in g.es:
	s,t = i.tuple
	print g.vs['label'][s]+','+g.vs['label'][t]


m = g.get_adjacency()
for i in m:
	print i





###Node degree
name = 'degree.png'
g = Graph.Barabasi(10,1.5,directed=False)
g = g.simplify()
g.vs['size'] = 50
g.vs['color'] = 'white'
g.es['color'] = 'black'
g.vs['label'] = g.degree()
g.vs['label_size']=40

lay = g.layout_fruchterman_reingold()
plot(g,'./images/'+name,layout = lay,dpi = 300,bbox = (500,500),margin=50)


for i in g.es:
	s,t = i.tuple
	print g.vs['label'][s]+','+g.vs['label'][t]



###Degree distribution
from collections import Counter
from math import log
import matplot
import matplotlib.pyplot as plt
 

name = 'degree_distribution.png'

g = Graph.Barabasi(1000,1,directed=False)
d = g.degree()
max_d = float(max(d))
c = Counter(d)

d_i = sorted(list(set(d)))
x = [log(i,10) for i in d_i]
y = [log(c[i],10) for i in d_i]
plt.figure(figsize=(4,4))
plt.scatter(x, y)
plt.title('degree distribution')
plt.xlabel('log(degree)')
plt.ylabel('log(freq)')
plt.savefig('./images/'+name,dpi = 300,margin=25)
plt.clf()

from colormaps import plasma
from matplotlib.cm import get_cmap
grey = get_cmap('Greys')

g = Graph.Barabasi(100,1,directed=False)
g = g.simplify()
d = g.degree()

max_d = float(log(max(d)))
g.vs['size'] = 25
for i in range(len(g.vs)):
	node_d = round(log(g.vs[i].degree()),1)
	g.vs[i]['color'] = plasma(node_d/max_d)
	if g.vs[i].degree()<6:
		g.vs[i]['label_color'] = 'white'
	else:
		g.vs[i]['label_color'] = 'black'


g.es['color'] = 'black'
g.vs['label'] = g.degree()
g.vs['label_size']=15

lay = g.layout_fruchterman_reingold()
plot(g,'./images/net_'+name,layout = lay,dpi = 300,bbox = (500,500),margin=50)

########################same but for random network
from collections import Counter
from math import log
import matplot
import matplotlib.pyplot as plt
 

name = 'degree_distribution_random.png'

g = Graph.Erdos_Renyi(1000,0.01,directed = False)
d = g.degree()
max_d = float(max(d))
c = Counter(d)

d_i = sorted(list(set(d)))
x = [log(i,10) for i in d_i]
y = [log(c[i],10) for i in d_i]
plt.figure(figsize=(4,4))
plt.scatter(x, y)
plt.title('degree distribution')
plt.xlabel('log(degree)')
plt.ylabel('log(freq)')
plt.savefig('./images/'+name,dpi = 300,margin=25)
plt.clf()

from colormaps import plasma
from matplotlib.cm import get_cmap
grey = get_cmap('Greys')

g = Graph.Erdos_Renyi(50,0.1,directed = False)
g = g.simplify()

from numpy import where,array
g.delete_vertices(where(array(g.degree())==0)[0])
d = g.degree()

max_d = float(log(max(d)))
g.vs['size'] = 25
for i in range(len(g.vs)):
	node_d = round(log(g.vs[i].degree()),1)
	g.vs[i]['color'] = plasma(node_d/max_d)
	if g.vs[i].degree()<6:
		g.vs[i]['label_color'] = 'white'
	else:
		g.vs[i]['label_color'] = 'black'


g.es['color'] = 'black'
g.vs['label'] = g.degree()
g.vs['label_size']=15

lay = g.layout_fruchterman_reingold()
plot(g,'./images/net_'+name,layout = lay,dpi = 300,bbox = (500,500),margin=50)





