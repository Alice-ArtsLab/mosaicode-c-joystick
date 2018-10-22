#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This module contains the Window class.
"""
from mosaicode.GUI.fieldtypes import *
from mosaicode.model.blockmodel import BlockModel

class WindowProperties(BlockModel):

    # -------------------------------------------------------------------------
    def __init__(self):
        BlockModel.__init__(self)

        self.language = "c"
        self.framework = "joystick"
        self.help = "Not to declare"
        self.label = "Joystick"
        self.color = "250:150:150:150"
        self.group = "Joystick"
        self.ports = [
                {"type":"mosaicode_lib_c_opengl.extensions.ports.float",
                "label":"Type",
                "conn_type":"Output",
                "name":"type"},
                {"type":"mosaicode_lib_c_opengl.extensions.ports.float",
                "label":"Event",
                "conn_type":"Output",
                "name":"event"},
                {"type":"mosaicode_lib_c_opengl.extensions.ports.float",
                "label":"Axis",
                "conn_type":"Output",
                "name":"axis"},
                {"type":"mosaicode_lib_c_opengl.extensions.ports.float",
                "label":"Value",
                "conn_type":"Output",
                "name":"value"},
                ]

        self.properties = [{"name": "device",
                            "label": "Device",
                            "type": MOSAICODE_STRING,
                            "value": "/dev/input/js0",
                            }]

        self.codes["global"] = r"""
    std::vector<void (*)(float)> $port[type]$;
    std::vector<void (*)(float)> $port[event]$;
    std::vector<void (*)(float)> $port[axis]$;
    std::vector<void (*)(float)> $port[value]$;

void joystick_callback_$id$(t_mosaic_button_event *event) {
    for(auto n : $port[type]$)
        n((float)event->type);
    for(auto n : $port[event]$)
        n((float)event->event);
    for(auto n : $port[axis]$)
        n((float)event->axis);
    for(auto n : $port[value]$)
        n((float)event->value);
}

void register_callback_$id$(char * device,
                char * name,
                char number_of_axes,
                char number_of_buttons,
                int driver_version){
    printf("%s \n%s \n number_of_axes: %d\n number_of_buttons: %d\n  driver_version: %d\n",
                        device,
                        name,
                        number_of_axes,
                        number_of_buttons,
                        driver_version);
    }
"""

        self.codes["declaration"] = r"""
    joystick_inicialize("$prop[device]$", &joystick_callback_$id$, &register_callback_$id$);
"""
