# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
from flask import Flask, Blueprint, request, render_template, url_for, send_from_directory
import logging
import datetime
import requests
import urllib
import json
import uuid
import os
from openpyxl import load_workbook, Workbook
from pyexcel_xlsx import get_data
import csv

from .forms import BankForm
from .utils import *

logger = logging.getLogger(__name__)
app = Flask(__name__, template_folder="templates", static_folder="statics")
#app.config.from_object("at.config")
app.secret_key = 'citibankfajdslkf'

@app.route('/robots.txt')
@app.route('/sitemap.xml')
def static_from_root():
    return send_from_directory(app.static_folder, request.path[1:])

@app.route("/", methods=['POST', 'GET'])
def index():

    form = BankForm()
    PARTH_LOCHANGE = "/media/mebao/DATA1"

    if not form.day_logchange.data:
        form.day_logchange.data = "30/11/2016"

    if not form.folder_logchange.data:
        form.folder_logchange.data = "logcha"

    total_amount_Approved = 0
    quantity_Approved = 0
    quantity_Hold = 0
    quantity_Rejected = 0
    quantity_UpdateAmount = 0


    first_Title = ["ID", "TransID", "Date", "ProductID", "Quantity", "Sales Amount", "Reward Amount",
                   "Identifies", "Session ID", "device", "Check Date", "Result Target", "Creative",
                   "Partner Site Name", "Fee ID", "Fee Amount", "DeadLine", "Update Status"]

    updateamount_Title = ["ID", "TransID", "Date", "ProductID", "Quantity", "Update Sales Amount", "Reward Amount",
                          "Identifies",
                          "Session ID", "device", "Check Date", "Result Target", "Creative", "Partner Site Name",
                          "Fee ID",
                          "Fee Amount", "DeadLine", "Target"]

    data_Approved = []
    data_Hold = []
    data_Rejected = []
    data_UpdateAmount = []

    if request.method == 'POST':
        file_obj = request.files['datafile']
        wb = load_workbook(file_obj)
        sheets = wb.worksheets

        day_logchange = form.day_logchange.data
        folder_logchange = form.folder_logchange.data

        parth_File_Approved = PARTH_LOCHANGE + '/' + folder_logchange+'/Approved.csv'
        parth_File_Hold = PARTH_LOCHANGE + '/' + folder_logchange + '/Hold.csv'
        parth_File_Rejected = PARTH_LOCHANGE + '/' + folder_logchange + '/Rejected.csv'
        parth_File_UpdateAmount = PARTH_LOCHANGE + '/' + folder_logchange + '/UpdateAmount.csv'

        if len(sheets) > 0:
            if not os.path.exists(PARTH_LOCHANGE + '/' + folder_logchange):
                os.makedirs(PARTH_LOCHANGE + '/' + folder_logchange)

            if not os.path.exists(parth_File_Approved):
                os.mknod(parth_File_Approved)
            Approved = open(parth_File_Approved, "wb")
            writer_Approved = csv.writer(Approved, delimiter='	', quotechar='"', quoting=csv.QUOTE_ALL)

            if not os.path.exists(parth_File_Hold):
                os.mknod(parth_File_Hold)
            Hold = open(parth_File_Hold, "wb")
            writer_Hold = csv.writer(Hold, delimiter='	', quotechar='"', quoting=csv.QUOTE_ALL)

            if not os.path.exists(parth_File_Rejected):
                os.mknod(parth_File_Rejected)
            Rejected = open(parth_File_Rejected, "wb")
            writer_Rejected = csv.writer(Rejected, delimiter='	', quotechar='"', quoting=csv.QUOTE_ALL)

            if not os.path.exists(parth_File_UpdateAmount):
                os.mknod(parth_File_UpdateAmount)
            UpdateAmount = open(parth_File_UpdateAmount, "wb")
            writer_UpdateAmount = csv.writer(UpdateAmount, delimiter='	', quotechar='"', quoting=csv.QUOTE_ALL)

            writer_Approved.writerow(first_Title)
            writer_Hold.writerow(first_Title)
            writer_Rejected.writerow(first_Title)

            writer_UpdateAmount.writerow(updateamount_Title)

            sheet = sheets[0]
            for row in sheet.iter_rows():
                if row[17].value.lower() == "approved" or row[17].value.lower() == "approve":
                    item = [row[0].value,"","","","","","","","","",day_logchange,"","","","","","","Approved"]
                    writer_Approved.writerow(item)
                    quantity_Approved = quantity_Approved + int(row[4].value)
                    total_amount_Approved = total_amount_Approved + float(row[5].value)
                    data_Approved.append(item)

                    if row[20].value != '' and row[20].value != '-':
                        item = [row[0].value,"","","","", row[20].value,"","","","","","","","","","","","Approved"]
                        writer_UpdateAmount.writerow(item)
                        quantity_UpdateAmount = quantity_UpdateAmount + int(row[4].value)
                        data_UpdateAmount.append(item)

                if row[17].value.lower() == "hold":
                    item = [row[0].value, "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "",
                                     "Hold"]
                    writer_Hold.writerow(item)
                    quantity_Hold = quantity_Hold + int(row[4].value)
                    data_Hold.append(item)

                if row[17].value.lower() == "reject" or row[17].value.lower() == "rejecte" or row[17].value.lower() == "rejected":
                    item = [row[0].value, "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "",
                                     "Rejected"]
                    writer_Rejected.writerow(item)
                    quantity_Rejected = quantity_Rejected + int(row[4].value)
                    data_Rejected.append(item)


            Approved.close()
            Hold.close()
            Rejected.close()
            UpdateAmount.close()

    return render_template('index.html',
                           form = form,
                           PARTH_LOCHANGE=PARTH_LOCHANGE ,
                           folder_logchange=form.folder_logchange.data,
                           first_Title=first_Title,
                           updateamount_Title=updateamount_Title,

                           total_amount_Approved=total_amount_Approved,

                           quantity_Approved=quantity_Approved,
                           quantity_Hold=quantity_Hold,
                           quantity_Rejected=quantity_Rejected,
                           quantity_UpdateAmount=quantity_UpdateAmount,

                           data_Approved=data_Approved,
                           data_Hold=data_Hold,
                           data_Rejected=data_Rejected,
                           data_UpdateAmount=data_UpdateAmount
                           )
