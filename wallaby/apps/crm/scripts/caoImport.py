#!/usr/bin/python
# Copyright (c) by it's authors. 
# Some rights reserved. See LICENSE, AUTHORS.

# -*- coding: UTF-8 -*-

import MySQLdb.cursors, copy, re
from twisted.enterprise import adbapi 
from twisted.internet import defer, task
from decimal import Decimal
from datetime import date
from wallaby.plugins.couchdb.client.database import *

def calcTotal(doc):
    if 'articles' in doc:
        total = 0
        for item in doc['articles']:
            if 'total' in item:
                try:
                    total = total + float(item['total'])
                except:
                    pass

        vat = total*0.19

        doc['netto'] = str(total)
        doc['vat'] = str(vat)
        doc['brutto'] = str(total + vat)

process = {
    'ADRESSEN': False,
    'JOURNAL': False,
    'ARTIKEL': False,
    'VERTRAG': True
}

mappings = {
    'ADRESSEN': {
        'identifier': 'KUNNUM1',
        'prefix': 'CAOCUSTOMER',
        'skip': 'NAME1',
        'proto': {
            'type': 'CUSTOMER'
        },
        'mapping': {
            'title': 'ANREDE',
            'street': 'STRASSE',
            'customerNumber': 'KUNNUM1',
            'zip': 'PLZ',
            'city': 'ORT',
            'country': {
                'column': 'LAND',
                'mapping': {
                    'DE': 'Deutschland',
                    'CH': 'Schweiz',
                    'ES': 'Spanien',
                    'AT': 'Österreich'
                }
            },
            'name': 'NAME1',
            'name2': 'NAME2',
            'notes': [
                {
                    'column': 'INFO',
                    'field': 'text',
                    'proto': {
                        'title': 'CAO Notiz'
                    }
                }
            ],
            'contact': [
                {
                    'column': 'TELE1',
                    'field': 'value',
                    'proto': {
                        'type': 'telefon'
                    }
                },
                {
                    'column': 'TELE2',
                    'field': 'value',
                    'proto': {
                        'type': 'telefon'
                    }
                },
                {
                    'column': 'FAX',
                    'field': 'value',
                    'proto': {
                        'type': 'fax'
                    }
                },
                {
                    'column': 'EMAIL',
                    'field': 'value',
                    'proto': {
                        'type': 'email'
                    }
                },
                {
                    'column': 'EMAIL2',
                    'field': 'value',
                    'proto': {
                        'type': 'email'
                    }
                },
                {
                    'column': 'INTERNET',
                    'field': 'value',
                    'proto': {
                        'type': 'www'
                    }
                }
            ]
        }
    },
    'ARTIKEL': {
        'identifier': 'REC_ID',
        'prefix': 'CAOARTICLE',
        'skip': 'KURZNAME',
        'proto': {
            'type': 'ARTICLE'
        },
        'mapping': {
            'articleNumber': {
                'column': 'REC_ID',
                'prefix': 'CAO'
            },
            'shortdescription': 'KURZNAME',
            'description': 'LANGNAME',
            'description': 'LANGNAME',
            'price': 'VK5'

        }
    },
    'VERTRAG': {
        'identifier': 'VVTNUM',
        'prefix': 'CAOCONTRACT',
        'skip': 'KUN_NAME1',
        'proto': {
            'type': 'INVOICE',
            'status': 'CONTRACT'
        },
        'callback': calcTotal,
        'mapping': {
            'title': 'PROJEKT',
            'customerID': {
                'column': 'KUN_NUM',
                'prefix': 'CAOCUSTOMER'
            },
            'contract.nextInvoice': 'DATUM_NEXT',
            'contract.startDate': 'DATUM_START',
            'interval': {
                'column': 'INTERVALL',
                'mapping': {
                    'J': 'Jährlich',
                    'M': 'Monatlich',
                    'Q': 'Quartalsweise'
                }
            },
            'articles': {
                'relation': 'VERTRAGPOS',
                'key': 'VVTNUM',
                'order': 'POSITION',
                'proto': {
                    'type': 'ARTICLE'
                },
                'mapping':
                {
                    '_id': {
                        'column': 'ARTIKEL_ID',
                        'prefix': 'CAOARTICLE'
                    },
                    'count': 'MENGE',
                    'description': 'BEZEICHNUNG',
                    'price': 'EPREIS',
                    'total': 'GPREIS',
                    'unit': 'ME_EINHEIT'
                }
            }
        }
    },
    'JOURNAL': {
        'identifier': 'VRENUM',
        'prefix': 'CAOINVOICE',
        'skip': 'VRENUM',
        'callback': calcTotal,
        'proto': {
            'type': 'INVOICE',
            'status': 'PENDING'
        },
        'mapping': {
            'title': 'PROJEKT',
            'invoiceNumber': 'VRENUM',
            'invoiceDate': 'RDATUM',
            'status': {
                'column': 'STADIUM',
                'mapping': {
                    '2': 'PENDING',
                    '9': 'PAID',  
                    '8': 'PAIDSKONTO',
                    '7': 'PAIDFRACTION',
                    '30': 'STORNO',
                    '6': 'STORNO'
                }
            },
            'customerID': {
                'column': 'KUN_NUM',
                'prefix': 'CAOCUSTOMER'
            },
            'customer.name': 'KUN_NAME1',
            'customer.name2': 'KUN_NAME2',
            'customer.street': 'KUN_STRASSE',
            'customer.zip': 'KUN_PLZ',
            'customer.city': 'KUN_ORT',
            'customer.number': 'KUN_NUM',
            'customer.country': {
                'column': 'KUN_LAND',
                'mapping': {
                    'DE': 'Deutschland',
                    'CH': 'Schweiz',
                    'ES': 'Spanien',
                    'AT': 'Österreich'
                }
            },
            'articles': {
                'relation': 'JOURNALPOS',
                'key': 'VRENUM',
                'order': 'POSITION',
                'proto': {
                    'type': 'ARTICLE'
                },
                'mapping':
                {
                    '_id': {
                        'column': 'ARTIKEL_ID',
                        'prefix': 'CAOARTICLE'
                    },
                    'count': 'MENGE',
                    'description': 'BEZEICHNUNG',
                    'price': 'EPREIS',
                    'total': 'GPREIS',
                    'unit': 'ME_EINHEIT'
                }
            }
        }
    }

}

def set(data, path, val):
    if '.' in path:
        path = path.split('.')
    else:
        path = [path]

    for p in range(len(path)-1):
        key = path[p]
        if not key in data:
            data[key] = {}

        data = data[key]

    data[path[-1]] = val

@defer.inlineCallbacks
def addEntities(table, dct, cond = None, superList = None):
    global mappings, db, couchdb

    query = "SELECT * FROM " + table

    if cond:
        query = query + " WHERE " + cond

    if 'order' in dct:
        query = query + " ORDER BY " + dct['order']

    c = yield db.runQuery(query)

    for row in c:
        if superList == None:
            if dct['identifier'] not in row or row[dct['identifier']] == None:
                print "Skipping", row[dct['skip']]
                continue

            ident = dct['prefix'] + str(row[dct['identifier']])

            ident = re.sub(r'[-\s]', '', ident)

            if 'STORNO' in ident:
                print "Skipping", ident
                continue

            try:
                data = yield couchdb.get(ident)
            except Exception as e:
                print "EXCEPTION", e
                data = None

            if data == None:
                print "Creating", ident, "(", row[dct['skip']], ")"
                data = copy.deepcopy(dct['proto'])
                data['_id'] = ident
            else:
                print "Updating", ident, "(", row[dct['skip']], ")"
        else:
            if 'proto' in dct:
                data = copy.deepcopy(dct['proto'])
            else:
                data = {}

        for entry, column in dct['mapping'].items():
            if isinstance(column, dict):
                if 'relation' in column:
                    val = []

                    from twisted.internet import reactor
                    yield task.deferLater(reactor, 0, addEntities, column['relation'], column, cond=column['key'] + ' = "' + str(row[dct['identifier']]) + '"', superList=val)

                elif 'column' in column:
                    val = unicode(row[column['column']])
                    if 'mapping' in column and val in column['mapping']:
                        val = column['mapping'][val]
                    if column['column'] == 'INTERVALL': print "INTERVALL:", val

                    if 'prefix' in column:
                        val = column['prefix'] + val
                else:
                    print "Error: unknown dict for", entry
                    continue

            elif isinstance(column, list) or isinstance(column, tuple):
                val = []
                for col in column:
                    if col['column'] in row and row[col['column']] != None:
                        p = copy.deepcopy(col['proto'])
                        p[col['field']] = row[col['column']]
                        val.append(p)

                if len(val) == 0:
                    continue

            else:
                val = row[column]

            if isinstance(val, Decimal):
                val = unicode(val)
            elif isinstance(val, date):
                val = [val.year, val.month, val.day]
            elif isinstance(val, str):
                try:
                    val = unicode(val)
                except:
                    print "Fehler bein kodieren von", val
                    # continue

            set(data, entry, val)

        if superList != None:
            superList.append(data)

        if superList == None:
            if 'callback' in dct:
                dct['callback'](data)

            try:
                yield couchdb.save(data)
            except Exception as e:
                print "EXCEPTION", e

@defer.inlineCallbacks
def doImport():
    global mappings, db, couchdb, process

    db = adbapi.ConnectionPool("MySQLdb", host="127.0.0.1", port=3306, user="sqluser", passwd="password", db="cao", cursorclass=MySQLdb.cursors.DictCursor, use_unicode=True)
    couchdb = Database.getDatabase("http://localhost:5984/crm", username="user", password="password")

    from twisted.internet import reactor

    for table, dct in mappings.items():
        if process[table]:
            yield task.deferLater(reactor, 0, addEntities, table, dct)

    reactor.stop()

if __name__ == "__main__":
    from twisted.internet import reactor
    reactor.callLater(0, doImport)
    reactor.run()
