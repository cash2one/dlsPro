# coding=utf-8
from django.db import connection,transaction
from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import render_to_response
from transport.models import *
from django.core.paginator import Paginator
from django.core.paginator import PageNotAnInteger
from django.core.paginator import EmptyPage
from django.db.models import Q
import simplejson as json
from singon import *
import string
import os
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.sessions.models import Session
import hashlib 
import sys
import cStringIO
from datetime import *
from models import *
from storage import *
from django.core.mail import send_mail
from PIL import Image, ImageDraw, ImageFont
import random
import time
import re
from random import choice
import string
import urllib2
from xlwt import *
import sys 
reload(sys) 
sys.setdefaultencoding('utf8')
