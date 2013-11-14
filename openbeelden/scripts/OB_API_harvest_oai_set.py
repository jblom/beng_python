#!/usr/bin/python

"""
OpenBeelden OAI harvester 

REQUIRED LIBRARIES:

PyOAI: https://svn.infrae.com/pyoai/tag/pyoai-2.4/doc/API.html
XLWT: 

"""
import xlwt
from oaipmh.client import Client
from oaipmh.metadata import MetadataRegistry, oai_dc_reader, MetadataReader
from oaipmh.server import oai_dc_writer
import itertools
import codecs
from dateutil.parser import parse

OUTPUT_DIR = '/tmp' # change this directory
OUTPUT_FILE = 'openbeelden_beeldengeluid_oai.xls' # change to whatever
OAI_SET = u'beeldengeluid' # change the set (unless you want to harvest beeldengeluid ^^)
EXCEL_SHEET_NAME = 'Sheet 1' # change if you care about the name of the Excel sheet

#Een specifieke reader voor de oai_oi namespace van de Openbeelden OAI data provider
oai_oi_reader = MetadataReader(
    fields={
    'title':       ('textList', 'oai_oi:oi/oi:title/text()'),
    'alternative':       ('textList', 'oai_oi:oi/oi:alternative/text()'),
    'creator':     ('textList', 'oai_oi:oi/oi:creator/text()'),
    'subject':     ('textList', 'oai_oi:oi/oi:subject/text()'),
    'description': ('textList', 'oai_oi:oi/oi:description/text()'),
    'abstract': ('textList', 'oai_oi:oi/oi:abstract/text()'),
    'publisher':   ('textList', 'oai_oi:oi/oi:publisher/text()'),
    'contributor': ('textList', 'oai_oi:oi/oi:contributor/text()'),
    'date':        ('textList', 'oai_oi:oi/oi:date/text()'),
    'type':        ('textList', 'oai_oi:oi/oi:type/text()'),
    'extent':        ('textList', 'oai_oi:oi/oi:extent/text()'),
    'medium':        ('textList', 'oai_oi:oi/oi:medium/text()'),    
    'identifier':  ('textList', 'oai_oi:oi/oi:identifier/text()'),
    'source':      ('textList', 'oai_oi:oi/oi:source/text()'),
    'language':    ('textList', 'oai_oi:oi/oi:language/text()'),
    'references':    ('textList', 'oai_oi:oi/oi:references/text()'),
    'spatial':    ('textList', 'oai_oi:oi/oi:spatial/text()'),
    'attributionName':    ('textList', 'oai_oi:oi/oi:attributionName/text()'),
    'attributionURL':    ('textList', 'oai_oi:oi/oi:attributionURL/text()'),
    'license':      ('textList', 'oai_oi:oi/oi:license/text()')
    },
    
    #TODO notitie maken van het feit dat oai_oi dezelfde ns heeft als oai_dc
    namespaces={
    'oai_oi': 'http://www.openbeelden.nl/feeds/oai/', #'http://www.openarchives.org/OAI/2.0/oai_oi/',
    'oi': 'http://www.openbeelden.nl/oai/'}
    )

URL = 'http://www.openbeelden.nl/feeds/oai/'

#Initieer de OAI client
registry = MetadataRegistry()
registry.registerReader('oai_oi', oai_oi_reader)
client = Client(URL, registry)
x = client.updateGranularity()

#Controleer of de OAI service goed geidentificeerd kan worden
x = client.identify()
print 'identity %s' % x.repositoryName()
print 'identity %s' % x.protocolVersion()
print 'identity %s' % x.baseURL()

def processOpenbeelden():
	i=0
	iarecs = []
	extent = None
	secs = 0
	
	wbk = xlwt.Workbook()
	sheet = wbk.add_sheet(EXCEL_SHEET_NAME) 
	i = 1
	
	sheet.write(0,0,'#')
	sheet.write(0,1,'TITLE')
	sheet.write(0,2,'ALTERNATIVE')
	sheet.write(0,3,'CREATOR')
	sheet.write(0,4,'SUBJECT')
	sheet.write(0,5,'DESCRIPTION')
	sheet.write(0,6,'ABSTRACT')
	sheet.write(0,7,'PUBLISHER')
	sheet.write(0,8,'CONTRIBUTOR')
	sheet.write(0,9,'DATE')
	sheet.write(0,10,'TYPE')
	sheet.write(0,11,'EXTENT')
	sheet.write(0,12,'MEDIUM')
	sheet.write(0,13,'IDENTIFIER')
	sheet.write(0,14,'SOURCE')
	sheet.write(0,15,'LANGUAGE')
	sheet.write(0,16,'REFERENCES')
	sheet.write(0,17,'SPATIAL')
	sheet.write(0,18,'ATTRIBUTION NAME')
	sheet.write(0,19,'ATTRIBUTION URL')
	sheet.write(0,20,'LICENSE')
		
	for rec in client.listRecords(metadataPrefix=u'oai_oi', set=OAI_SET):
		header, metadata, about = rec
						
		title = getFieldData(metadata, 'title')				
		alternative = getFieldData(metadata, 'alternative')				
		creator = getFieldData(metadata, 'creator')			
		subject = getFieldData(metadata, 'subject')		
		description = getFieldData(metadata, 'description')					
		abstract = getFieldData(metadata, 'abstract')
		publisher = getFieldData(metadata, 'publisher')
		contributor = getFieldData(metadata, 'contributor')	
		date = getFieldData(metadata, 'date')
		type = getFieldData(metadata, 'type')
		
		extent = metadata.getField('extent')[0]
		
		medium = getFieldData(metadata, 'medium')
		identifier = getFieldData(metadata, 'identifier')		
		source = getFieldData(metadata, 'source')
		language = getFieldData(metadata, 'language')
		references = getFieldData(metadata, 'references')
		spatial = getFieldData(metadata, 'spatial')
		attributionName = getFieldData(metadata, 'attributionName')
		attributionURL = getFieldData(metadata, 'attributionURL')
		license = getFieldData(metadata, 'license')
		
		sheet.write(i,0,i)
		sheet.write(i,1,title)
		sheet.write(i,2,alternative)
		sheet.write(i,3,creator)
		sheet.write(i,4,subject)
		sheet.write(i,5,description)
		sheet.write(i,6,abstract)
		sheet.write(i,7,publisher)
		sheet.write(i,8,contributor)
		sheet.write(i,9,date)
		sheet.write(i,10,type)
		sheet.write(i,11,getExtentInSeconds(extent))
		sheet.write(i,12,medium)
		sheet.write(i,13,identifier)
		sheet.write(i,14,source)
		sheet.write(i,15,language)
		sheet.write(i,16,references)
		sheet.write(i,17,spatial)
		sheet.write(i,18,attributionName)
		sheet.write(i,19,attributionURL)
		sheet.write(i,20,license)
		
		i += 1				
		secs += getExtentInSeconds(extent)
	#393307
	wbk.save('%s/%s' % (OUTPUT_DIR, OUTPUT_FILE))
	print 'saved'
	print secs
	print 'TOTAL TIME: %s' % secsToTimeString(secs)
	
	#you can use this to list all the available sets
	"""
	for s in client.listSets():
		print s
	"""

def getFieldData(metadata, fn):
	return '; '.join(metadata.getField(fn))

def getExtentInSeconds(ext):
	secs = 0
	if ext and ext.find('PT') != -1:
		ext = ext[2:len(ext)]
		if ext.find('H') != -1:			
			secs = int(ext[0:ext.find('H')]) * 3600
			ext = ext[ext.find('H') + 1:len(ext)]
		if ext.find('M') != -1:			
			secs = int(ext[0:ext.find('M')]) * 60
			ext = ext[ext.find('M') + 1:len(ext)]
		if ext.find('S') != -1:			
			secs += int(ext[0:ext.find('S')])
	return secs

def secsToTimeString(secs):
	h = m = s = 0
	while secs - 3600 >= 0:
		h += 1
		secs -= 3600	
	while secs - 60 >= 0:
		m += 1
		secs -= 60
	return '%d:%d:%d' % (h, m, s)
	
#Run the main function
processOpenbeelden()
