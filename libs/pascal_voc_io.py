#!/usr/bin/env python
# -*- coding: utf8 -*-
import _init_path
import sys
from xml.etree import ElementTree
from xml.etree.ElementTree import Element, SubElement
from lxml import etree
import codecs

XML_EXT = '.xml'


class PascalVocWriter:

    def __init__(self, username, foldername, filename, imgSize, databaseSrc='Unknown', localImgPath=None):
        # print 'filename is ',filename,'type:',type(filename)
        # print 'username is ',username,'type:',type(username)
        self.username = unicode(username)
        self.foldername = foldername
        self.filename = filename

        # self.boxmaker = boxmaker
        self.databaseSrc = databaseSrc
        self.imgSize = imgSize
        self.boxlist = []
        self.localImgPath = localImgPath
        self.verified = False

    def prettify(self, elem):
        """
            Return a pretty-printed XML string for the Element.
        """
        rough_string = etree.tostring(elem, encoding='UTF-8')
        # rough_string = str(rough_string, encoding="UTF-8")
        root = etree.XML(rough_string)
        return etree.tostring(root, encoding='UTF-8', pretty_print=True)

    def genXML(self):
        """
            Return XML root
        """
        # Check conditions
        if self.filename is None or \
                self.foldername is None or \
                self.imgSize is None:
            return None

        top = etree.Element('annotation')
        top.set('verified', 'yes' if self.verified else 'no')

# <<<<<<< HEAD
        user = SubElement(top, 'username')
        user.text = self.username

        # folder = SubElement(top, 'folder')
# =======
        folder = etree.SubElement(top, 'folder')
# >>>>>>> 2198c34077d078b45eb055b73fcf6715354a3a0e
        folder.text = self.foldername

        filename = etree.SubElement(top, 'filename')
        filename.text = self.filename

        localImgPath = etree.SubElement(top, 'path')
        localImgPath.text = self.localImgPath

# <<<<<<< HEAD
    #>>>> delete(3)
        # source = SubElement(top, 'source')
        # database = SubElement(source, 'database')
        # database.text = self.databaseSrc
# =======
        # source = etree.SubElement(top, 'source')
        # database = etree.SubElement(source, 'database')
        # database.text = self.databaseSrc
# >>>>>>> 2198c34077d078b45eb055b73fcf6715354a3a0e

        size_part = etree.SubElement(top, 'size')
        width = etree.SubElement(size_part, 'width')
        height = etree.SubElement(size_part, 'height')
        depth = etree.SubElement(size_part, 'depth')
        width.text = str(self.imgSize[1])
        height.text = str(self.imgSize[0])
        if len(self.imgSize) == 3:
            depth.text = str(self.imgSize[2])
        else:
            depth.text = '1'
# <<<<<<< HEAD
    #>>>> delete(3)
        # segmented = SubElement(top, 'segmented')
        # segmented.text = '0'
# =======

        # segmented = etree.SubElement(top, 'segmented')
        # segmented.text = '0'
# >>>>>>> 2198c34077d078b45eb055b73fcf6715354a3a0e
        return top

    def addBndBox(self, xmin, ymin, xmax, ymax):#delete(1), name
        bndbox = {'xmin': xmin, 'ymin': ymin, 'xmax': xmax, 'ymax': ymax}
        #delete (1) bndbox['name'] = name
        self.boxlist.append(bndbox)

    def appendObjects(self, top):
        for each_object in self.boxlist:
# <<<<<<< HEAD
        #     object_item = SubElement(top, 'object')
        # #>>>> delete(3)
        #     #name = SubElement(object_item, 'name')
        #     # try:
        #     #     name.text = unicode(each_object['name'])
        #     # except NameError:
        #     #     # Py3: NameError: name 'unicode' is not defined
        #     #     name.text = each_object['name']
        #     # pose = SubElement(object_item, 'pose')
        #     # pose.text = "Unspecified"
        #     # truncated = SubElement(object_item, 'truncated')
        #     # truncated.text = "0"
        #     # difficult = SubElement(object_item, 'difficult')
        #     # difficult.text = "0"
        #     bndbox = SubElement(object_item, 'bndbox')
        #     xmin = SubElement(bndbox, 'xmin')
# =======
            object_item = etree.SubElement(top, 'object')
            # name = etree.SubElement(object_item, 'name')
            # try:
            #     name.text = unicode(each_object['name'])
            # except NameError:
            #     # Py3: NameError: name 'unicode' is not defined
            #     name.text = each_object['name']
            # pose = etree.SubElement(object_item, 'pose')
            # pose.text = "Unspecified"
            # truncated = etree.SubElement(object_item, 'truncated')
            # truncated.text = "0"
            # difficult = etree.SubElement(object_item, 'difficult')
            # difficult.text = "0"
            bndbox = SubElement(object_item, 'bndbox')
            xmin = SubElement(bndbox, 'xmin')
            xmin.text = str(each_object['xmin'])
            ymin = SubElement(bndbox, 'ymin')
            ymin.text = str(each_object['ymin'])
            xmax = SubElement(bndbox, 'xmax')
            xmax.text = str(each_object['xmax'])
            ymax = SubElement(bndbox, 'ymax')
            ymax.text = str(each_object['ymax'])
#             bndbox = etree.SubElement(object_item, 'bndbox')
#             xmin = etree.SubElement(bndbox, 'xmin')
# # >>>>>>> 2198c34077d078b45eb055b73fcf6715354a3a0e
#             xmin.text = str(each_object['xmin'])
#             ymin = etree.SubElement(bndbox, 'ymin')
#             ymin.text = str(each_object['ymin'])
#             xmax = etree.SubElement(bndbox, 'xmax')
#             xmax.text = str(each_object['xmax'])
#             ymax = etree.SubElement(bndbox, 'ymax')
#             ymax.text = str(each_object['ymax'])

    def save(self, targetFile=None):
        root = self.genXML()
        self.appendObjects(root)
        out_file = None
        if targetFile is None:
            out_file = codecs.open(
                self.filename + XML_EXT, 'w', encoding='utf-8')
        else:
            out_file = codecs.open(targetFile, 'w', encoding='utf-8')

        prettifyResult = self.prettify(root)
        out_file.write(prettifyResult.decode('utf8'))
        out_file.close()


class PascalVocReader:

    def __init__(self, filepath):
        # shapes type:
        # [labbel, [(x1,y1), (x2,y2), (x3,y3), (x4,y4)], color, color]
        self.shapes = []
        self.filepath = filepath
        self.verified = False
        self.parseXML()

    def getShapes(self):
        return self.shapes

    def addShape(self,  bndbox):#delete(3) label,
        xmin = int(bndbox.find('xmin').text)
        ymin = int(bndbox.find('ymin').text)
        xmax = int(bndbox.find('xmax').text)
        ymax = int(bndbox.find('ymax').text)
        points = [(xmin, ymin), (xmax, ymin), (xmax, ymax), (xmin, ymax)]
        self.shapes.append(( points, None, None))#delete(3) label,

    def parseXML(self):
        # assert self.filepath.endswith('.xml'), "Unsupport file format"
        # # content = None
        # with open(self.filepath, 'r') as xmlFile:
        #     content = xmlFile.read()
        #
        # if content is None:
        #     return False

        # xmltree = etree.XML(content)
        # filename = xmltree.find('filename').text
        # try:
        #     verified = xmltree.attrib['verified']
        #     if verified == 'yes':
        #         self.verified = True
        # except KeyError:
        #     self.verified = False
        #
        # for object_iter in xmltree.findall('object'):
        #     bndbox = object_iter.find("bndbox")
        #     #delete(3) label = object_iter.find('name').text
        #     self.addShape(bndbox)#delete(1) label,
        # return True
        assert self.filepath.endswith('.xml'), "Unsupport file format"
        parser = etree.XMLParser(encoding='utf-8')
        # print 'self.filepath',self.filepath
        # print 'parser',parser
        xmltree = ElementTree.parse(self.filepath, parser=parser).getroot()
        filename = xmltree.find('filename').text
        try:
            verified = xmltree.attrib['verified']
            if verified == 'yes':
                self.verified = True
        except KeyError:
            self.verified = False

        for object_iter in xmltree.findall('object'):
            bndbox = object_iter.find("bndbox")
            # label = object_iter.find('name').text
            self.addShape(bndbox)
        return True


# tempParseReader = PascalVocReader('test.xml')
# print tempParseReader.getShapes()
"""
# Test
tmp = PascalVocWriter('temp','test', (10,20,3))
tmp.addBndBox(10,10,20,30,'chair')
tmp.addBndBox(1,1,600,600,'car')
tmp.save()
"""
