# -*- coding: utf-8 -*-
"""
Created on Mon Jun  8 15:42:28 2020

@author: harshv
"""

function letterToColumn(letter)
{
  var column = 0, length = letter.length;
  for (var i = 0; i < length; i++)
  {
    column += (letter.charCodeAt(i) - 64) * Math.pow(26, length - i - 1);
  }
  return column;
}