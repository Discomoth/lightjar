# -*- coding: utf-8 -*-
# colors.py

def hex_to_rgb(hex_str):
    hex_str = hex_str.replace('#', '')
    return (int(hex_str[0:2],16), int(hex_str[2:4],16), int(hex_str[4:6],16))

gradient_1 = [hex_to_rgb(color) for color in ["F83D5C","F83D5A","F83E59","F93E57","F93F56","F93F54","F94053","F94051","F94150","FA414E","FA424C","FA424B","FA4349","FA4348","FA4446","FB4445","FB4543","FB4542","FB4640","FB463F","FB473D","FC473B","FC483A","FC4838","FC4937","FC4935","FC4A34","FD4A32","FD4B31","FD4B2F"]]
gradient_2 = [hex_to_rgb(color) for color in ["3EC9F7","3FC2F7","3FBBF8","40B4F8","41ADF8","41A6F8","429FF9","4398F9","4392F9","448BF9","4584FA","457DFA","4676FA","476FFB","4768FB","4861FB","485AFB","4953FC","4A4CFC","4A45FC","4B3EFD","4C37FD","4C31FD","4D2AFD","4E23FE","4E1CFE","4F15FE","500EFE","5007FF","5100FF"]]
