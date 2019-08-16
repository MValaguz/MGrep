# -*- coding: utf-8 -*-

# serve per la visualizzazione delle info di programma
import wx.adv
from   wx.lib.wordwrap import wordwrap

def info(p_version):
    # First we create and fill the info object
    info = wx.adv.AboutDialogInfo()
    info.Name = "SmiGrep"
    info.Version = p_version
    info.Copyright = "(c) 2016-2018 SmiTec"
    info.Description = """\nSmiGrep is a set of utilities created to facilitate
the programming work in the Oracle Forms environment."""
    info.Developers = ["Marco Valaguzza"]
    wx.adv.AboutBox(info)
