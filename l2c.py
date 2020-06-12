# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 15:52:52 2020

@author: harshv
"""
def l2c(letter):
  var column = 0, length = letter.length;
  for (var i = 0; i < length; i++)
  {
    column += (letter.charCodeAt(i) - 64) * Math.pow(26, length - i - 1);
  }
  return column;

