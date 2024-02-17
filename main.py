import configparser
import ctypes
import sys
import os
from pathlib import Path
import PySimpleGUI as sg
import win32gui
import win32con
import win32api

user32 = ctypes.windll.user32
PROFILE_FILE = 'profiles.ini'


def profile_file_path():
    script_path = Path(sys.argv[0])
    if script_path is not None:
        return str(os.path.join(script_path.parent, PROFILE_FILE))
    else:
        return PROFILE_FILE


def read_profiles():
    profiles = []

    config = configparser.ConfigParser()
    config.read(profile_file_path())

    for section in config.sections():
        print(f"Found profile: {section}")
        profiles.append(
            {
                "name": section,
                "x": config[section]['x'],
                "y": config[section]['y'],
                "width": config[section]['width'],
                "height": config[section]['height']
            }
        )

    return profiles


def load_profile(profiles, title):
    for profile in profiles:
        print(profile['name'])
        if profile['name'] in title:
            return profile

    return None


def save_window_profile(title, x, y, hres, vres):
    profile_path = profile_file_path()

    config = configparser.ConfigParser()
    config.read(profile_path)

    output_config = Path(profile_path)
    output_config.parent.mkdir(exist_ok=True, parents=True)
    with output_config.open("w") as output_file:
        config.remove_section(title)
        config.add_section(title)
        config[title]['x'] = x
        config[title]['y'] = y
        config[title]['width'] = hres
        config[title]['height'] = vres

        config.write(output_file)


def windowsizeupdate(hwnd):
    windowrect = win32gui.GetWindowRect(hwnd)
    windowrect = win32gui.GetWindowRect(hwnd)
    title = win32gui.GetWindowText(hwnd)
    profiles = read_profiles()
    profile = load_profile(profiles, title)
    if profile is not None:
        window['X'].update(profile['x'])
        window['Y'].update(profile['y'])
        window['HRes'].update(profile['width'])
        window['VRes'].update(profile['height'])
    else:
        window['X'].update(int(windowrect[0]))
        window['Y'].update(int(windowrect[1]))
        window['HRes'].update(int(windowrect[2] - windowrect[0]))
        window['VRes'].update(int(windowrect[3] - windowrect[1]))


def winEnumHandler(hwnd, _):
    if win32gui.IsWindowVisible(hwnd):
        n = win32gui.GetWindowText(hwnd)
        s = win32api.GetWindowLong(hwnd, win32con.GWL_STYLE)
        x = win32api.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
        if n:
            allvisiblewindows.update(
                {n: {'hwnd': hwnd, 'STYLE': s, 'EXSTYLE': x}})


allvisiblewindows = {}

win32gui.EnumWindows(winEnumHandler, None)

sg.theme('DarkGrey11')
layout = [[sg.Text('Window Selection: ')],
          [sg.Combo(list(allvisiblewindows.keys()), enable_events=True,
                    key='combo'), sg.Button('Refresh')],
          [sg.Text("X Pos:"), sg.InputText("0", size=(7, 7), key='X'),
           sg.Text("Y Pos:"), sg.InputText("0", size=(7, 7), key='Y')],
          [sg.Text("H Res:"), sg.InputText("2560", size=(7, 7), key='HRes'), sg.Text(
              "V Res:"), sg.InputText("1440", size=(7, 7), key='VRes')],
          [sg.Button('Borderless Window'), sg.Button('Revert Changes'), sg.Button(
              'Resize/Position', key="Resize"), sg.Button('Save Window Profile'), sg.Exit(key='Cancel')]
          ]


window = sg.Window('Borderless Window Utility', layout)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel':
        break

    if event == 'Borderless Window':
        hwnd = allvisiblewindows.get(values['combo'], {}).get('hwnd')
        try:
            win32gui.GetWindowRect(hwnd)
        except:
            print('Window not found, reloading list')
            allvisiblewindows = {}
            win32gui.EnumWindows(winEnumHandler, None)
            window.Element('combo').update(
                values=list(allvisiblewindows.keys()))
        else:
            XPos = int(values["X"])
            YPos = int(values["Y"])
            user32.SetWindowLongW(hwnd, win32con.GWL_STYLE,
                                  win32con.WS_VISIBLE | win32con.WS_CLIPCHILDREN)
            user32.SetWindowLongW(hwnd, win32con.GWL_EXSTYLE, 0)
            HRes = int(values["HRes"])-1
            VRes = int(values["VRes"])-1
            user32.MoveWindow(hwnd, XPos, YPos, HRes, VRes, True)
            VRes = VRes + 1
            HRes = HRes + 1
            win32gui.SetWindowPos(hwnd, None, XPos, YPos, HRes, VRes, win32con.SWP_FRAMECHANGED | win32con.SWP_NOZORDER |
                                  win32con.SWP_NOOWNERZORDER)
            windowsizeupdate(hwnd)

    if event == 'Revert Changes':
        hwnd = allvisiblewindows.get(values['combo'], {}).get('hwnd')
        try:
            win32gui.GetWindowRect(hwnd)
        except:
            print('Window not found, reloading list')
            allvisiblewindows = {}
            win32gui.EnumWindows(winEnumHandler, None)
            window.Element('combo').update(
                values=list(allvisiblewindows.keys()))
        else:
            style = allvisiblewindows.get(values['combo'], {}).get('STYLE')
            exstyle = allvisiblewindows.get(values['combo'], {}).get('EXSTYLE')
            hwnd = allvisiblewindows.get(values['combo'], {}).get('hwnd')
            rect = win32gui.GetWindowRect(hwnd)
            user32.SetWindowLongW(hwnd, win32con.GWL_STYLE, style)
            user32.SetWindowLongW(hwnd, win32con.GWL_EXSTYLE, exstyle)
            win32gui.SetWindowPos(hwnd, None, 0, 0, 0, 0, win32con.SWP_FRAMECHANGED | win32con.SWP_NOMOVE |
                                  win32con.SWP_NOSIZE | win32con.SWP_NOZORDER | win32con.SWP_NOOWNERZORDER)
            windowsizeupdate(hwnd)

    if event == 'Resize':
        hwnd = allvisiblewindows.get(values['combo'], {}).get('hwnd')
        try:
            win32gui.GetWindowRect(hwnd)
        except:
            print('Window not found, reloading list')
            allvisiblewindows = {}
            win32gui.EnumWindows(winEnumHandler, None)
            window.Element('combo').update(
                values=list(allvisiblewindows.keys()))
        else:
            XPos = int(values["X"])
            YPos = int(values["Y"])
            HRes = int(values["HRes"])
            VRes = int(values["VRes"])
            user32.MoveWindow(hwnd, XPos, YPos, HRes, VRes, True)
            windowsizeupdate(hwnd)

    if event == 'Refresh':
        allvisiblewindows = {}
        win32gui.EnumWindows(winEnumHandler, None)
        window.Element('combo').update(values=list(allvisiblewindows.keys()))

    if event == 'Save Window Profile':
        save_window_profile(values['combo'], values['X'], values['Y'], values['HRes'], values['VRes'])

    if event == 'combo':
        hwnd = allvisiblewindows.get(values['combo'], {}).get('hwnd')
        try:
            win32gui.GetWindowRect(hwnd)
        except:
            print('Window not found, reloading list')
            allvisiblewindows = {}
            win32gui.EnumWindows(winEnumHandler, None)
            window.Element('combo').update(
                values=list(allvisiblewindows.keys()))
        else:
            windowsizeupdate(hwnd)
