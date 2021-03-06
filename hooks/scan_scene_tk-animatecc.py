# Copyright (c) 2013 Shotgun Software Inc.
# 
# CONFIDENTIAL AND PROPRIETARY
# 
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit 
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your 
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights 
# not expressly granted therein are reserved by Shotgun Software Inc.

import os

import sgtk

from sgtk import Hook
from sgtk import TankError

class ScanSceneHook(Hook):
    """
    Hook to scan scene for items to publish
    """
    
    def execute(self, **kwargs):
        """
        Main hook entry point
        :returns:       A list of any items that were found to be published.  
                        Each item in the list should be a dictionary containing 
                        the following keys:
                        {
                            type:   String
                                    This should match a scene_item_type defined in
                                    one of the outputs in the configuration and is 
                                    used to determine the outputs that should be 
                                    published for the item
                                    
                            name:   String
                                    Name to use for the item in the UI
                            
                            description:    String
                                            Description of the item to use in the UI
                                            
                            selected:       Bool
                                            Initial selected state of item in the UI.  
                                            Items are selected by default.
                                            
                            required:       Bool
                                            Required state of item in the UI.  If True then
                                            item will not be deselectable.  Items are not
                                            required by default.
                                            
                            other_params:   Dictionary
                                            Optional dictionary that will be passed to the
                                            pre-publish and publish hooks
                        }
        """   
                
        items = []
        adobe = self.parent.engine.adobe

        # get the main scene:
        try:
            doc = adobe.rpc_eval("fl.getDocumentDOM();")
        except RuntimeError:
            raise TankError("There is no active document!")
        
        try:
            scene_path = self.sanitise_path(adobe.rpc_eval("fl.getDocumentDOM().pathURI;"))
        except RuntimeError:
            raise TankError("Please save your file before publishing!")

        name = os.path.basename(scene_path)

        # create the primary item - this will match the primary output 'scene_item_type':            
        items.append({"type": "work_file", "name": name})

        return items

    def sanitise_path(self, path):
        if isinstance(path, unicode):
            path = path.encode("utf-8")
            
        path = str.replace(path, "///", "")
        path = str.replace(path, "file:", "")
        path = str.replace(path, "/", "\\")
        path = str.replace(path, "|", ":")
        return path
