#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import json
import _init_path
import sys
from xml.etree import ElementTree
from xml.etree.ElementTree import Element, SubElement
from lxml import etree
import codecs

XML_EXT = '.xml'

def genXML(filename,username = 'ROOT',foldername = 'ROOT',localImgPath = "ROOT",imgSize = ['-1','-1','-1']):
    """
        Return XML root
    """
    top = etree.Element('annotation')
    top.set('verified', 'yes')

    user = SubElement(top, 'username')
    user.text = username
    folder = etree.SubElement(top, 'folder')
    folder.text = foldername

    filename = etree.SubElement(top, 'filename')
    filename.text = str(filename)

    localImgPath = etree.SubElement(top, 'path')
    localImgPath.text = str(localImgPath)
    size_part = etree.SubElement(top, 'size')
    width = etree.SubElement(size_part, 'width')
    height = etree.SubElement(size_part, 'height')
    depth = etree.SubElement(size_part, 'depth')
    width.text = str(imgSize[1])
    height.text = str(imgSize[0])
    if len(imgSize) == 3:
        depth.text = str(imgSize[2])
    else:
        depth.text = '1'
    return top

def get_json(imgfile):
    OtherBoundingBoxs = []
    fn=imgfile
    # print path_ + fn + ".json"
    otherf = file(path_ + fn + ".json")
    others = json.load(otherf)
    index = 0
    for region in others['regions']:
        for line in region['lines']:
            for word in line['words']:
                OtherBoundingBoxs.append(word['boundingBox'])#print word
                # print word['boundingBox'],word['text']
    otherf.close
    return OtherBoundingBoxs

def prettify(elem):
    """
        Return a pretty-printed XML string for the Element.
    """
    rough_string = etree.tostring(elem, encoding='UTF-8')
    root = etree.XML(rough_string)
    return etree.tostring(root, encoding='UTF-8', pretty_print=True)

def addBndBox(xmin, ymin, xmax, ymax):
    bndbox = {'xmin': xmin, 'ymin': ymin, 'xmax': xmax, 'ymax': ymax}
    return bndbox

def appendObjects(top,boxlist):
    for each_object in boxlist:
        object_item = etree.SubElement(top, 'object')
        bndbox = SubElement(object_item, 'bndbox')
        xmin = SubElement(bndbox, 'xmin')
        xmin.text = str(each_object['xmin'])
        ymin = SubElement(bndbox, 'ymin')
        ymin.text = str(each_object['ymin'])
        xmax = SubElement(bndbox, 'xmax')
        xmax.text = str(each_object['xmax'])
        ymax = SubElement(bndbox, 'ymax')
        ymax.text = str(each_object['ymax'])

def json2xml():
    files = os.listdir('OriImgs')
    pics = [file_ for file_ in files if file_.endswith('json')]
    for pic in pics:
        filename = pic.split('.')[0]
        Boxs = get_json(pic.split('.')[0])
        boxlist = []
        for box in Boxs:
            xmin = int(box.split(',')[0])
            ymin = int(box.split(',')[1])
            xmax = xmin + int(box.split(',')[2])
            ymax = ymin + int(int(box.split(',')[3]))
            boxlist.append(addBndBox(xmin, ymin, xmax, ymax))
        root = genXML(pic.split('.')[0])
        appendObjects(root,boxlist)
        out_file = None
        out_file = codecs.open(
                filename + XML_EXT, 'w', encoding='utf-8')
        prettifyResult = prettify(root)
        out_file.write(prettifyResult.decode('utf8'))
        out_file.close()

        print 'pic:', Boxs
        print 'boxlist',boxlist

if __name__ == '__main__':
    path_ = os.path.join(os.getcwd(),'OriImgs/')
    json2xml()
