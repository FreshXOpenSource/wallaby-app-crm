# Copyright (c) by it's authors. 
# Some rights reserved. See LICENSE, AUTHORS.

from wallaby.pf.room import *

from wallaby.pf.peer.viewer import *
from wallaby.pf.peer.editor import *

class Invoice(Room):

    def __init__(self, name):
        Room.__init__(self, name)

        self._count = None
        self._price = None
        self._document = None

    def customPeers(self):
        Viewer(self._name, self._countChanged, 'articles.*.count', raw=True) 
        Viewer(self._name, self._priceChanged, 'articles.*.price', raw=True) 
        self._subTotal = Editor(self._name, path='articles.*.total', raw=True)

        self._netto = Editor(self._name, path='netto', raw=True)
        self._vat   = Editor(self._name, path='vat', raw=True)
        self._brutto = Editor(self._name, path='brutto', raw=True)

        self.catch(Viewer.In.Document, self._setDocument)

    def _setDocument(self, action, doc):
        self._document = doc

    def _countChanged(self, value):
        try:
            self._count = float(value)
        except:
            self._count = 0.0

        self.changeTotal()

    def _priceChanged(self, value):
        try:
            self._price = float(value)
        except:
            self._price = 0.0

        self.changeTotal()

    def changeTotal(self):
        if self._document == None or self._count == None or self._price == None: return

        if self._subTotal.isReadOnly(): return

        self._subTotal.changeValue(self._count * self._price)

        articles = self._document.get('articles')

        if not articles: return

        total = 0.0

        for article in articles:
            if 'total' in article:
                try:
                    total = total + float(article['total'])
                except:
                    pass

        vat = total*0.19

        self._vat.changeValue(vat)
        self._netto.changeValue(total)
        self._brutto.changeValue(total + vat)
