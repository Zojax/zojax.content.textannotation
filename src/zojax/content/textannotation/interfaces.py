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
import sys

from zope import interface, schema
from zope.i18n import MessageFactory

from zojax.content.type.interfaces import ISearchableContent

_ = MessageFactory('zojax.content.textannotation')


class ITextAnnotationConfiglet(interface.Interface):
    """ configlet """

    minLength = schema.Int(
        title = _(u'Min annotation length'),
        description = _(u'Minimum annotation length in characters.'),
        required = True,
        min=1,
        default=100)

    maxLength = schema.Int(
        title = _(u'Max annotation length'),
        description = _(u'Maximum annotation length in characters.'),
        required = True,
        min=1,
        default=sys.maxint)


class ITextAnnotation(interface.Interface):

    def getText(min_length, max_length, text=None):
        pass
