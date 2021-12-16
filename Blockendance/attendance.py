import tkinter as tk
import csv
import cv2
import os
import numpy as np
from PIL import Image
import pandas as pd
import datetime
import time


def ListToBlockchain():
    file = open("AttendanceFile.csv")
    next(file)

    resultat = []
    for row in file:
        numb = row.split(',')[0]
        resultat.append(numb)
    print(resultat)
    return resultat

