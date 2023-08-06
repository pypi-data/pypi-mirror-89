import json
import os
import tkinter
from tkinter import filedialog

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import pyplot


def _extract_data():
    root = tkinter.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    with open(file_path, 'r') as file:
        lines = file.readlines()
        title = lines[0]
        names, data = [], []
        for line in lines[1:]:
            cols = line.strip().split(',')
            names.append(cols[0].strip().title())
            data.append([int(x) for x in cols[1:]])
    return title, names, data


def _get_config():
    if not os.path.isfile('./config.json'):
        with open('./config.json', 'w+') as cnf:
            cnf.write(json.dumps({}))
    with open('./config.json', 'r') as cnf:
        config = json.loads(cnf.read())
    return config


def _write_config(config):
    with open('./config.json', 'w') as cnf:
        cnf.write(json.dumps(config))


def _get_class_list():
    config = _get_config()
    return [cls for cls in config]


def _add_new_names(cls, new_names=None):
    config = _get_config()
    all_name = config[cls]['all_name']
    if new_names:
        pass
    else:
        new_names = []
        while True:
            name = input("Enter a name. Type 'Exit' to stop").strip().title()
            if name == "Exit":
                break
            else:
                new_names.append(name)
    new_all_name = sorted([*all_name, *new_names])
    config[cls]['all_name'] = new_all_name
    _write_config(config)


def _add_name_changes(cls, change_names):
    config = _get_config()
    config[cls]['change_names'] = change_names
    _write_config(config)


def _get_all_name_and_changes(cls=None):
    config = _get_config()
    if not cls:
        while True:
            available_classes = '\n'.join(_get_class_list())
            print(f'Available classes: \n{available_classes}')
            cls = input("Enter class: ").lower()
            if config.get(cls):
                return config[cls]['all_name'], config[cls]['change_names'], cls
            else:
                yn = input(f'Class {cls} does not exist. Do you want to create? (yes, no)').lower()
                if yn == "yes":
                    config[cls] = {"all_name": [], "change_names": {}}
                    _write_config(config)
                    return [], {}, cls
    return config[cls]['all_name'], config[cls]['change_names']


def _suggest_name_change(names, change_names):
    cs = ''
    for name in names:
        if name in change_names:
            cs += f'{name} --> {change_names[name]}\n'
    if len(cs) != 0:
        yn = input(f'{cs}Above will be changed. Do you want to continue?(yes, no)').lower()
        if yn == 'yes':
            for index, name in enumerate(names):
                if name in change_names:
                    names[index] = change_names[name]
    return names


def _refine_data_name(names, data):
    all_names, change_names, cls = _get_all_name_and_changes()
    new_names = []
    names = _suggest_name_change(names, change_names)
    for index, name in enumerate(names):
        if name not in all_names:
            yn = input(f'Type actual name of "{name}" press Enter to skip. ').title()
            if len(yn) != 0:
                change_names[name] = yn
                names[index] = yn
            new_names.append(names[index])
            all_names.append(names[index])
    if new_names:
        _add_new_names(cls, new_names)
    all_names_str = '\n'.join(all_names)
    yn = input(f'Available names:\n{all_names_str}\n Do you want to add new?(yes, no)').strip().lower()
    if yn == 'yes':
        _add_new_names(cls)
    _add_name_changes(cls, change_names)
    all_names, change_names = _get_all_name_and_changes(cls)
    meeting_length = len(data[0])
    for name in all_names:
        if name not in names:
            names.append(name)
            data.append([0 for _ in range(meeting_length)])
    return names, data


def _show_graph(title, names, data):
    data = np.array(data)
    a4_dims = (11.7, 8.27)
    fig, ax = pyplot.subplots(figsize=a4_dims)
    sns.heatmap(ax=ax, data=data, cbar=False)
    ax.set_title(title)
    ax.set_yticklabels(names)
    plt.setp(ax.get_yticklabels(), rotation=0, ha="right",
             rotation_mode="anchor")
    for i in range(data.shape[0] + 1):
        ax.axhline(i, color='white', lw=2)
    plt.show()


def run_attendance_helper():
    title, names, data = _extract_data()
    names, data = _refine_data_name(names, data)
    _show_graph(title, names, data)
