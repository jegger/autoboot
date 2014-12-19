#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.uix.label import Label

import os

# Create local folder
path = os.path.expanduser("~/apps/autoboot")
if not os.path.isdir(path):
    os.mkdir(path)

import slider


class RunProg(Widget):
    def __init__(self, **kwargs):
        super(RunProg, self).__init__(**kwargs)

        self.root = Widget()

        #Draw background for testing
        self.root.canvas.add(Color(1, 1, 1, 1))
        self.root.canvas.add(Rectangle(size=Window.size))
        
        self.space = Window.height/8
        
        self.mon = slider.RTBoundarySlider(day="Mon", size=(700, 20),
                                           pos=(Window.width-800,
                                                Window.height-self.space))
        self.root.add_widget(self.mon)
        self.mon_l = Label(text="Montag:",
                           pos=(Window.width-1000,
                                Window.height-self.space-40),
                           color=(0, 0, 0, 1), bold=True, font_size=15)
        self.root.add_widget(self.mon_l)
        
        self.die = slider.RTBoundarySlider(day="Tue", size=(700, 20),
                                           pos=(Window.width-800,
                                                self.mon.y-self.space))
        self.root.add_widget(self.die)
        self.die_l = Label(text="Dienstag:",
                           pos=(Window.width-1000, self.mon_l.y-self.space),
                           color=(0, 0, 0, 1), bold=True, font_size=15)
        self.root.add_widget(self.die_l)
        
        self.mit = slider.RTBoundarySlider(day="Wed", size=(700, 20),
                                           pos=(Window.width-800,
                                                self.die.y-self.space))
        self.root.add_widget(self.mit)
        self.mit_l = Label(text="Mittwoch:",
                           pos=(Window.width-1000, self.die_l.y-self.space),
                           color=(0, 0, 0, 1), bold=True, font_size=15)
        self.root.add_widget(self.mit_l)
        
        self.don = slider.RTBoundarySlider(day="Thu", size=(700, 20),
                                           pos=(Window.width-800,
                                                self.mit.y-self.space))
        self.root.add_widget(self.don)
        self.don_l = Label(text="Donnerstag:",
                           pos=(Window.width-1000, self.mit_l.y-self.space),
                           color=(0, 0, 0, 1), bold=True, font_size=15)
        self.root.add_widget(self.don_l)
        
        self.fre = slider.RTBoundarySlider(day="Fri", size=(700, 20),
                                           pos=(Window.width-800,
                                                self.don.y-self.space))
        self.root.add_widget(self.fre)
        self.fre_l = Label(text="Freitag:",
                           pos=(Window.width-1000, self.don_l.y-self.space),
                           color=(0, 0, 0, 1), bold=True, font_size=15)
        self.root.add_widget(self.fre_l)
        
        self.sam = slider.RTBoundarySlider(day="Sat", size=(700, 20),
                                           pos=(Window.width-800,
                                                self.fre.y-self.space))
        self.root.add_widget(self.sam)
        self.sam_l = Label(text="Samstag:",
                           pos=(Window.width-1000, self.fre_l.y-self.space),
                           color=(0, 0, 0, 1), bold=True, font_size=15)
        self.root.add_widget(self.sam_l)
        
        self.son = slider.RTBoundarySlider(day="Sun", size=(700, 20),
                                           pos=(Window.width-800,
                                                self.sam.y-self.space))
        self.root.add_widget(self.son)
        self.son_l = Label(text="Sonntag:",
                           pos=(Window.width-1000, self.sam_l.y-self.space),
                           color=(0, 0, 0, 1), bold=True, font_size=15)
        self.root.add_widget(self.son_l)
        
        self.add_widget(self.root)


class RTBootTime(App):

    def build(self):
        return RunProg()


if __name__ == '__main__':
    RTBootTime().run()
