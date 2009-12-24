##############################################################################
#
# Copyright (c) 2009 Zope Foundation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
"""

$Id$
"""
import re
import sys

from zope import interface, component

from zojax.richtext.interfaces import IRichTextData
from zojax.content.type.interfaces import IItem

from interfaces import ITextAnnotation, ITextAnnotationConfiglet


class TextAnnotation(object):

    component.adapts(interface.Interface, interface.Interface)
    interface.implements(ITextAnnotation)

    def __init__(self, context, request):
        self.context, self.request = context, request

    def getContentText(self):
        try:
            description = IItem(self.context).description
        except TypeError:
            description = ''
        res = description or \
              getattr(self.context, 'text', description)
        if IRichTextData.providedBy(res):
            if not res.cooked:
                return description
            return res.cooked
        if res:
            return res
        return u''

    def getText(self, min_length=None, max_length=None, text=None):
        configlet = component.getUtility(ITextAnnotationConfiglet)
        if min_length is None:
            min_length = configlet.minLength
        if max_length is None:
            max_length = configlet.maxLength
        if text is None:
            text = self.getContentText()
        temp = re.sub("(?u)<[^>]+>", " ",
            re.sub("(?u)\s+", " ", text))
        s = re.sub("(?u)\s+([\.,!?:;])", "\g<1>", temp)
        s = re.sub("(?u)&nbsp;", " ", s)
        s = re.sub("(?u)&quot;", '"', s)
        s = re.sub("(?u)&lt;", "<", s)
        s = re.sub("(?u)&gt;", ">", s)
        s = re.sub("(?u)&amp;", "&", s)

        return self.toNearPoint(s, min_length, max_length)

    def toNearPoint(self, data, min_length, max_length):
        ln = len(data)
        if ln < min_length:
            return data
        n = self.getNearPoint(data, u'.', min_length, max_length)
        if n > -1 and n <= max_length and n>=min_length:
            return data[:n] + u'..'
        else:
            n = self.getNearPoint(data, u' ', min_length, max_length)
            if n > -1 and n <= max_length and n>=min_length:
                return data[:n-1] + u'...'
            else:
                return data[:max_length] + u'...'

    def getNearPoint(self, data, c, min_length, max_length):
        l = data.rfind(c, 0, min_length -1)
        r = data.find(c, min_length, max_length)
        if l > -1 and l <= max_length and l>=min_length:
            return l + 1
        elif r > -1 and r <= max_length and r >=min_length:
            return r + 1
        else:
            return -1
