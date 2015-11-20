#!/usr/bin/env python  
#-*-coding:utf-8 -*-        


#基于用户日志的查询扩展


import anydbm
import re
import jieba

class QueryExtention:

	#读取用户点击日志
	
	def seg(self,word):
		mat = []
		seg_list = jieba.cut(word,cut_all=False)
		for i in seg_list:
			if len(i) > 1:
				mat.append(i.encode('gbk'))
		return mat


	def processHash(self,key,newkey,inhash,index):
		if index == 1:
			if inhash.has_key(key):
				temphash = inhash[key]
				temphash[newkey] = ''
				inhash[key] = temphash
			else:
				temphash = {}
				temphash[newkey] = ''
				inhash[key] = temphash
			
		if index == 2:
			if inhash.has_key(key):
				inhash[key] += newkey
			else:
				inhash[key] = newkey
		return inhash


	def calculateParameter(self,inhash1,inhash2,docLen):
		vals = sum(inhash1.values())
		hashA = {}
		for i in inhash1:
			hashA[i] = float(inhash1[i])/float(vals)
		hashB = {}
		for i in inhash2:
			hashB[i] = float(inhash2[i])/float(docLen)
		temphash = {}
		for i in hashA:
			temphash[i] = 0.1 * hashA[i] + 0.1 * hashB[i]
			#print hashA[i],hashB[i]
		#keys = sorted(temphash.iteritems(),key=lambda temphash:temphash[1],reverse=True)
		#return keys
		return temphash

	def combi(self,hash1,hash2):
		for i in hash1:
			if hash2.has_key(i):
				hash2[i] = hash2[i] + hash1[i]
			else:
				hash2[i] = hash1[i]
		return hash2

	def readData(self,filename):
		data = open(filename,'r')
		queryHash = {}
		for i in data:
			mat = re.compile('	').split(i.strip('\n'))
			c = 0
			doc = len(mat) - 1
			seghash = {}
			seghash2 = {}
			for j in mat:
				c += 1
				mat2 = re.compile(',').split(j)
				if len(mat2) != 2 :continue
				if c == 1:
					query = mat2[0]
					queryHash[query] = {}
				segs = self.seg(mat2[0])
				for k in segs:
					seghash = self.processHash(k,int(mat2[1]),seghash,2)
					seghash2 = self.processHash(k,1,seghash2,2)

			queryHash[query] = self.calculateParameter(seghash,seghash2,doc)

		outhash = {}
		for i in queryHash:
			segs = self.seg(i)
			for j in segs:
				if outhash.has_key(j):
					temphash = outhash[j]
					outhash[j] = self.combi(queryHash[i],temphash)
				else:
					outhash[j] = queryHash[i]
		for i in outhash:
			temphash = outhash[i]
			total = sum(temphash.values())
			for j in temphash:
				temphash[j] = temphash[j]/total
			keys = sorted(temphash.iteritems(),key=lambda temphash:temphash[1],reverse=True)
			outhash[i] = keys

		return outhash	
			

#--------------------------------------------------------------------------------------
#example
#searchQuery.txt 是搜索词与用户点击结果的log
#分词需要安装jieba分词  eg:pip install jieba   或者 easy_install jieba		
'''	
QE = QueryExtention()
outhash = QE.readData('searchQuery.txt')
out = open('QueryExtentionResult2.txt','w')
p = 0 
for i in outhash:
	c = 0
	for k in outhash[i]:
		try:
			if re.search(k[0],i):continue
		except:
			continue
		c += 1
		if c == 1:out.write(i)
		#if c > 5:break
		out.write('	'+k[0]+'|'+str(k[1]))
	if len(k) > 0:
		out.write('\n')
'''
out = open('QueryExtentionResult2.txt','r')
out2 = open('QueryExtention.txt','w')
for i in out:
	if len(i) > 2:
		out2.write(i)
