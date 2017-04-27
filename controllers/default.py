# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from datetime import datetime
import time
def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    return dict()

def graph():
    t=db().select(db.instap.ALL)
    if len(t)>50:
        t=t[-50:]
    data=[]
    for i in t:
        data.append({
                "time":time.mktime(i.timestamp.timetuple()),
                "power":i.power
            }
                   )
    return dict(data=data)
def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())


@cache.action()
def getdata():
    p=request.vars.power
    t=datetime.now()
    db.instap.insert(timestamp=t,power=p)
    if len(db().select(db.p_limit.ALL))==0:
        db.p_limit.insert(cur=p,max_limit=50000)
    else:
        cur1=float(db().select(db.p_limit.ALL)[0].cur)+float(p)
        max_limit=float(db().select(db.p_limit.ALL)[0].max_limit)
        if cur1==(0.5*max_limit):
            fromaddr = "projectenergy666@gmail.com"
            toaddr = "sriram.t15@iiits.in"
            msg = MIMEMultipart()
            msg['From'] = fromaddr
            msg['To'] = toaddr
            msg['Subject'] = "Consumption of Power reaching 50% of your Limit"
            body = "You Sir/Madam have been using a lot of energy. You have reached 50% of your limit. Save power or the klan is coming for you. Long live KKK."
            msg.attach(MIMEText(body, 'plain'))
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(fromaddr, "zombieslayer69")
            text = msg.as_string()
            server.sendmail(fromaddr, toaddr, text)
            server.quit()
        elif cur1>=max_limit:
            fromaddr = "projectenergy666@gmail.com"
            toaddr = "sriram.t15@iiits.in"
            msg = MIMEMultipart()
            msg['From'] = fromaddr
            msg['To'] = "sriram.t15@iiits.in"
            msg['Subject'] = "Energy consumption has reached your limit."
            body = "You Sir/Madam have just been over-using the resource bestowed upon you by Mother nature and your government. You should learn to save power. You have just reached 100% of your limit. Your current power usage is "+str(cur1)+"KWh. Shame on you. Save power or the klan is coming for you. Long live KKK."
            msg.attach(MIMEText(body, 'plain'))
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(fromaddr, "zombieslayer69")
            text = msg.as_string()
            server.sendmail(fromaddr, toaddr, text)
            server.quit()
        if len(db().select(db.dailyp.ALL))==30:
            cur1=0
        db(db.p_limit.id==2).update(cur=cur1)
    return dict()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()
def retseconds():
    all_records=db().select(db.instap.ALL)
    last=all_records[-1]
    last['timestamp']=time.mktime(last['timestamp'].timetuple())
    return last['timestamp']
def ret_last_power():
    all_records=db().select(db.instap.ALL)
    last=all_records[-1]
    return last['power']
def ret_curr():
    last=db().select(db.p_limit.ALL)[0]
    return last['cur']
def ret_max():
    last=db().select(db.p_limit.ALL)[0]
    return last['max_limit']
