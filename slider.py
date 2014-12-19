#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from kivy.app import App
from kivy.uix.slider import Slider
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.uix.image import Image

import os
import database


class RTBoundarySlider(Widget):
    def __init__(self, **kwargs):
        super(RTBoundarySlider, self).__init__(**kwargs)
        self._border = 3
        self._day = kwargs.get('day', 'Son')
        
        #Set varibales for calculation
        self.last_size = 0, 0
        self.last_pos = self.pos
        self.delta_x_pos = 0
        self.delta_x_size = 0
        
        #Inital graphic
        self.g_values = Widget()
        self.add_widget(self.g_values)
        self.graphic = Widget()
        self.add_widget(self.graphic)
        
        self.min = Label(pos=(self.last_size[0]+self.delta_x_size+self.x-30,
                              self.y-102),
                         text="0", color=(0, 0, 0, 1),
                         bold=True)
        self.add_widget(self.min)
        self.max = Label(pos=(self.last_pos[0]-70, self.y-102), text="0",
                         color=(0, 0, 0, 1), bold=True)
        self.add_widget(self.max)
        
        self.slider_butR = Image(source=os.path.join("images/icons/slider-but.png"))
        self.slider_butR.size = (50, 100)
        self.add_widget(self.slider_butR)
        self.slider_butL = Image(source=os.path.join("images/icons/slider-but.png"))
        self.slider_butL.size = (50, 100)
        self.add_widget(self.slider_butL)
        
        self.num_0 = Label(pos=(self.x-49, self.y-79),
                           text="00:00", color=(0, 0, 0, 1))
        self.add_widget(self.num_0)
        self.num_12 = Label(pos=(self.x+(self.width/2)-49, self.y-79),
                            text="12:00", color=(0, 0, 0, 1))
        self.add_widget(self.num_12)
        self.num_24 = Label(pos=(self.x+self.width-49, self.y-79),
                            text="24:00", color=(0, 0, 0, 1))
        self.add_widget(self.num_24)
        
        #Add all new things to stage
        self.draw_unchangable()
        
        #read from DB an fill-in        
        self.fill_in()
    
    def fill_in(self):
        self.fill = False
        self.times = database.database.read_day(day=self._day)
        self.touch_x = ((self.times["stop_hour"]*60.0) + (self.times["stop_min"]))*700.0/1440+self.x
        self.draw_right()
        self.fill = True
        self.touch_x = ((self.times["start_hour"]*60.0)+(self.times["start_min"]))*700.0/1440+self.x
        self.draw_right()
        self.fill = False

    def set_value(self):
        self.min_time = 1440.0/self.width*self.delta_x_size
        self.min_M = self.min_time/60-int(self.min_time/60)
        if round(self.min_M*60, -1) < 10:
            self.value_min = "%i:0%i" %(int(self.min_time/60), round(self.min_M*60, -1))
            self.value_h_min = int(self.min_time/60)
            self.value_m_min = round(self.min_M*60, -1)
        elif round(self.min_M*60,-1) == 60:
            self.value_min = "%i:0%i" %(int(self.min_time/60+1), 00)
            self.value_h_min = int(self.min_time/60+1)
            self.value_m_min = round(00, -1)
        else:
            self.value_min = "%i:%i" %(int(self.min_time/60), round(self.min_M*60, -1))
            self.value_h_min = int(self.min_time/60)
            self.value_m_min = round(self.min_M*60, -1)
        
        self.test = self.last_size[0]+self.delta_x_size
        self.max_time = 1440.0/self.width*self.test
        self.max_M = self.max_time/60-int(self.max_time/60)
        if round(self.max_M*60,-1) < 10:
            self.value_max = "%i:0%i" %(int(self.max_time/60), round(self.max_M*60, -1))
            self.value_h_max = int(self.max_time/60)
            self.value_m_max = round(self.max_M*60, -1)
        elif round(self.max_M*60,-1) == 60:
            self.value_max = "%i:%i0" %(int(self.max_time/60+1), 00)
            self.value_h_max = int(self.max_time/60+1)
            self.value_m_max = round(00, -1)
        else:
            self.value_max = "%i:%i" %(int(self.max_time/60), round(self.max_M*60, -1))
            self.value_h_max = int(self.max_time/60)
            self.value_m_max = round(self.max_M*60, -1)
        
        if self.max_time-self.min_time < 120:
            self.stay_off = True 
            self.graphic.canvas.add(Color(0, 0, 0, 0.4))
            self.graphic.canvas.add(Rectangle(size=(self.width+80, self.height+90),
                                              pos=(self.x-40, self.y-67)))
        else:
            self.stay_off = False
            
    def draw_unchangable(self):
        #Draw Black border
        self.g_values.canvas.clear()
        self.g_values.canvas.add(Color(0, 0, 0, 1))
        self.g_values.canvas.add(Rectangle(size=(1, 40),
                                           pos=(self.x, self.y-20)))
        self.g_values.canvas.add(Rectangle(size=(1, 40),
                                           pos=(self.x+(self.width/2),
                                                self.y-20)))
        self.g_values.canvas.add(Rectangle(size=(1, 40),
                                           pos=(self.x+self.width,
                                                self.y-20)))
        
        self.g_values.canvas.add(Color(0, 0, 0, 1))
        self.g_values.canvas.add(Rectangle(size=(self.width+self._border*2,
                                                 self.height+self._border*2),
                                           pos=(self.x-self._border,
                                                self.y-self._border)))
        
        self.g_values.canvas.add(Color(0.73725, 0.73725, 0.73725, 1))
        self.g_values.canvas.add(Rectangle(size=self.size, pos=self.pos))
        
    def draw_right(self):
        #Calculate all things        
        if self.touch_x > (self.last_size[0]/2)+22+self.last_pos[0] and not self.fill:
            if self.touch_x > self.x+self.width:
                self.touch_x = self.x+self.width
            if self.touch_x < 0+self.x:
                self.touch_x = 0+self.x
            self.last_size = self.touch_x-self.x-self.delta_x_size, self.height
        elif self.touch_x < (self.last_size[0]/2)-22+self.last_pos[0] or self.fill:
            if self.touch_x > self.x+self.width:
                self.touch_x = self.x+self.width
            if self.touch_x < 0+self.x:
                self.touch_x = 0+self.x
            self.delta_x_pos = self.touch_x - self.last_pos[0]
            self.delta_x_size = self.touch_x - self.x
            self.last_pos = self.touch_x, self.y
            self.last_size = (self.last_size[0]-self.delta_x_pos, self.last_size[1])
        self.middle = (self.last_size[0]/2)+self.last_pos[0], self.y
        
        #Delete all from stage
        self.graphic.canvas.clear()
        
        #Draw actual value(blue)
        self.graphic.canvas.add(Color(0, 0.68235294, 0.941176470, 1))
        self.graphic.canvas.add(Rectangle(size=self.last_size, pos=self.last_pos))
        
        #Draw lines to label value
        with self.graphic.canvas:
            Color(0, 0, 0, 1)
            Rectangle(size=(1, 80), pos=(self.last_pos[0], self.last_pos[1]-60))
            Rectangle(size=(1, 80), pos=(self.last_pos[0]+self.last_size[0], self.last_pos[1]-60))
        
        #Change text values
        self.set_value()
        self.max.text=str(self.value_max)
        self.max.pos = (self.last_size[0]+self.delta_x_size+self.x-30, self.y-102)
        self.min.text=str(self.value_min) 
        self.min.pos = (self.last_pos[0]-70, self.y-102)
        
        #Change slider-but image
        self.slider_butR.pos = ((self.last_size[0]+self.delta_x_size+self.x)-self.slider_butR.width/2,
                                self.y-40)
        self.slider_butL.pos = ((self.last_pos[0]-self.slider_butL.width/2,
                                 self.y-40))
           
    def on_touch_down(self, touch):
        if not self.collide_point(touch.x, touch.y):
            return False
        touch.grab(self)
        self.touch_x = touch.x
        self.draw_right()
    
    def on_touch_move(self, touch):
        if touch.grab_current == self:
            self.touch_x = touch.x
            self.draw_right()
    
    def on_touch_up(self, touch, *kwargs):
        if touch.grab_current == self:
            database.database.insert_day(day=self._day,
                                                start_hour=self.value_h_min,
                                                start_min=self.value_m_min,
                                                stop_hour=self.value_h_max,
                                                stop_min=self.value_m_max,
                                                stay_off=self.stay_off)


class Slider(App):

    def build(self):
        self.root = Widget()

        #Draw background for testing
        self.root.canvas.add(Color(1, 1, 1, 1))
        self.root.canvas.add(Rectangle(size=Window.size))
        
        s = RTBoundarySlider(pos=(345, 120), size=(700, 20))
        self.root.add_widget(s)
        return self.root
    
if __name__ == '__main__':
    Slider().run()
