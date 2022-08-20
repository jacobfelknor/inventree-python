# -*- coding: utf-8 -*-

import logging

import inventree.base
import os

logger = logging.getLogger('inventree')


class LabelPrintingMixing:
    """Mixin class for label printing"""
    
    def printlabel(self, label, plugin=None, destination=None, *args, **kwargs):
        """Print the label belonging to the given item.
        
        Set the label with 'label' argument, as the ID of the corresponding
        label.
        
        If a plugin is given, the plugin will determine
        how the label is printed, and a message is returned.
        
        Otherwise, if a destination is given, the file will be downloaded to 'destination'.
        Use overwrite=True to overwrite an existing file.
        
        If neither plugin nor destination is given, nothing will be done
        """

        # Set URL to use
        URL = f'label/{self.LABELNAME}/{label}/print/?{self.LABELITEM}[]={self.pk}'

        if plugin is not None:
            # Append profile
            URL += f'&plugin={plugin}'

            # Get response
            return self._api.get(URL)

        if destination is not None:
            if os.path.exists(destination) and os.path.isdir(destination):
                # No file name given, construct one
                # Otherwise, filename will be something like '?parts[]=37'
                destination = os.path.join(
                    destination,
                    f'Label_{self.LABELNAME}{label}_{self.pk}.pdf'
                )

            # Use downloadFile method to get the file
            return self._api.downloadFile(url=f'api/{URL}', destination=destination, *args, **kwargs)

        return False


class LabelLocation(inventree.base.InventreeObject):
    """ Class representing the Label/Location database model """

    URL = 'label/location'


class LabelPart(inventree.base.InventreeObject):
    """ Class representing the Label/Part database model """

    URL = 'label/part'


class LabelStock(inventree.base.InventreeObject):
    """ Class representing the Label/stock database model """

    URL = 'label/stock'
