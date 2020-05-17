# -*- coding: utf-8 -*-

import os
import logging

from inventree import base
from inventree import part


class StockLocation(base.InventreeObject):
    """ Class representing the StockLocation database model """

    URL = 'stock/location'
    FILTERS = ['parent']

    def getStockItems(self):
        return StockItem.list(self._api, location=self.pk)


class StockItem(base.InventreeObject):
    """ Class representing the StockItem database model.
    
    Stock items can be filtered by:
    
    - location: Where the stock item is stored
    - category: The category of the part this stock item points to
    - supplier: Who supplied this stock item
    - part: The part referenced by this stock item
    - supplier_part: Matching SupplierPart object
    """

    URL = 'stock'
    FILTERS = [
        'location',
        'category',
        'cascade',
        'supplier',
        'part',
        'supplier_part'
        'build',
        'build_order',
        'belongs_to',
        'sales_order',
        'customer',
        'serialized',
        'serial_number',
        'allocated',
        'active',
        'ancestor',
        'status',
        'company',
        'supplier',
        'manufacturer',
    ]

    def getPart(self):
        """ Return the base Part object associated with this StockItem """
        return part.Part(self._api, self.part)

    def getAttachments(self):
        """ Return all file attachments for this StockItem """

        return StockItemAttachment.list(
            self._api,
            stock_item=self.pk
        )

    def getTestResults(self, **kwargs):

        kwargs['stock_item'] = self.pk

        return StockItemTestResult.list(
            self._api,
            **kwargs
        )


class StockItemAttachment(base.Attachment):
    """ Class representing a file attachment for a StockItem """

    URL = 'stock/attachment'
    FILTERS = ['stock_item']


class StockItemTracking(base.InventreeObject):
    """ Class representing a StockItem tracking object """

    URL = 'stock/track'
    FILTERS = ['item', 'user']


class StockItemTestResult(base.InventreeObject):
    """ Class representing a StockItemTestResult object """

    URL = 'stock/test'
    FILTERS = ['stock_item', 'test', 'result', 'value', 'user']

    @classmethod
    def upload_result(cls, api, stock_item, test, result, **kwargs):
        """
        Upload a test result.

        args:
            api: Authenticated InvenTree API object
            stock_item: pk of the StockItem object to upload the test result against
            test: Name of the test (string)
            result: Test result (boolean)

        kwargs:
            attachment: Optionally attach a file to the test result
            notes: Add extra notes
            value: Add a "value" to the test (e.g. an actual measurement made during the test)
        """

        attachment = kwargs.get('attachment', None)

        files = {}

        if attachment:
            if os.path.exists(attachment):
                f = os.path.basename(attachment)
                files['attachment'] = (f, open(attachment, 'rb'))
            else:
                logging.error("File does not exist: '{f}'".format(f=attachment))

        notes = kwargs.get('notes', '')
        value = kwargs.get('value', '')

        data = {
            'stock_item': stock_item,
            'test': test,
            'result': result,
            'notes': notes,
            'value': value,
        }

        # Send the data to the serever
        if api.post(cls.URL, data, files=files):
            logging.info("Uploaded test result: '{test}'".format(test=test))
        else:
            logging.warning("Test upload failed")
