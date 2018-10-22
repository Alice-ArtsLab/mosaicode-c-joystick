# -*- coding: utf-8 -*-
# [MOSAICODE PROJECT]
#
"""
This module contains the JavascriptTemplate class.
"""
from mosaicode.model.codetemplate import CodeTemplate


class CFile(CodeTemplate):
    """
    This class contains methods related the JavascriptTemplate class.
    """
    # ----------------------------------------------------------------------

    def __init__(self):
        CodeTemplate.__init__(self)
        self.name = "joystick"
        self.language = "c"
        self.description = "A full template to generate joystick code"
        self.extension = ".c"
        self.command = "g++ -std=c++11 -g -Wall -pthread $dir_name$$filename$$extension$ -o $dir_name$$filename$\n"
        self.command += "$dir_name$./$filename$"
        self.code_parts = ["global", "declaration"]
        self.code = r"""
#include <stdio.h>
#include <unistd.h>
#include <fcntl.h>
#include <linux/joystick.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <pthread.h>
#include <vector>
#include <iostream> // for cout

typedef struct {
    int type;
    int event; /* 0-pressed; 1- released*/
    int axis;
    int value;
} t_mosaic_button_event;

typedef void (t_mosaic_joystick_event_callback_function)(
                t_mosaic_button_event *event
                );

typedef void (t_mosaic_joystick_register_callback_function)(
                char * device,
                char * name,
                char number_of_axes,
                char number_of_buttons,
                int driver_version
                );

typedef struct {
    t_mosaic_joystick_event_callback_function * event_callback_function;
    t_mosaic_joystick_register_callback_function * register_callback_function;
    char * device;
} t_mosaic_device_data;

void *joystick_thread(void *data){
    if (((t_mosaic_device_data *)data)->event_callback_function == NULL){
        pthread_exit((void *)NULL);
    }

    int fd = open(((t_mosaic_device_data *)data)->device, O_RDONLY);
    char name[128];
    if (ioctl(fd, JSIOCGNAME(sizeof(name)), name) < 0)
        strncpy(name, "Unknown", sizeof(name));
    char number_of_axes;
    ioctl(fd, JSIOCGAXES, &number_of_axes);
    char number_of_buttons;
    ioctl(fd, JSIOCGBUTTONS, &number_of_buttons);
    int driver_version;
    ioctl(fd,JSIOCGVERSION,&driver_version);
    if (((t_mosaic_device_data *)data)->register_callback_function != NULL)
        ((t_mosaic_device_data *)data)->register_callback_function(
                    ((t_mosaic_device_data *)data)->device,
                    name,
                    number_of_axes,
                    number_of_buttons,
                    driver_version);


    t_mosaic_button_event *btn_event = (t_mosaic_button_event *) malloc(sizeof(btn_event));
    struct js_event msg;

    while(1) {
        if(read(fd, &msg, sizeof(struct js_event)) != sizeof(struct js_event)){
            pthread_exit((void *)NULL);
        } else {
            if(msg.type == JS_EVENT_BUTTON){
                 btn_event->type = JS_EVENT_BUTTON;
                if (msg.value == 1) {
                    btn_event->event = 1;
                    btn_event->value = msg.number;
                    ((t_mosaic_device_data *)data)->event_callback_function(btn_event);
                } else if (msg.value == 0) {
                    btn_event->event = 0;
                    btn_event->value = msg.number;
                    ((t_mosaic_device_data *)data)->event_callback_function(btn_event);
               }
            } else if (msg.type == JS_EVENT_AXIS){
                    btn_event->type = JS_EVENT_AXIS;
                    btn_event->axis = msg.number;
                    btn_event->value = msg.value;
                ((t_mosaic_device_data *)data)->event_callback_function(btn_event);
            }
            if (msg.type == JS_EVENT_INIT){
            }
        }
    }
}


void joystick_inicialize(const char * device,
                t_mosaic_joystick_event_callback_function * event_callback_function,
                t_mosaic_joystick_register_callback_function * register_callback_function){
    t_mosaic_device_data * data = (t_mosaic_device_data *) malloc(sizeof(t_mosaic_device_data));
    data->device = (char *) malloc(strlen(device));
    strcpy(data->device, device);
    data->event_callback_function = event_callback_function;
    data->register_callback_function = register_callback_function;
    pthread_t tid;
    pthread_create(&tid, NULL, joystick_thread, data);
}

$code[global]$

int main(int argc, char *argv[]) {
    $code[declaration]$
    $connections$
    while(1) usleep(10000);
    return 0;
}
"""

# -------------------------------------------------------------------------
