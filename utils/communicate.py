from urllib import request, parse
from urllib.error import HTTPError
import re
import copy
import os
import json

ROOT_URL = 'https://adventofcode.com'

TEMPLATE_HEADER = {
    'Accept-Language': 'en-US,en;q=0.8', 
    'Accept-Encoding': 'none', 
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3', 
    'Connection': 'keep-alive', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 
    'User-Agent': 'Mozilla/5.0 (Linux; Android 7.0.1; MotoG4 Build/MPI24.107-55) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.81 Mobile Safari/537.36'
}

ENCODING_TYPE = 'utf-8'

class AOCMiscUtil:
    @staticmethod
    def get_input_file_url(year, day):
        global ROOT_URL
        return ROOT_URL + '/' +  "%d/day/%d/input"%(year, day)

    @staticmethod
    def get_question_url(year, day):
        global ROOT_URL
        return ROOT_URL + '/' +  "%d/day/%d"%(year, day)

    @staticmethod
    def get_answer_url(year, day):
        global ROOT_URL
        return ROOT_URL + '/' +  "%d/day/%d/answer"%(year, day)

    @staticmethod
    def get_cookie(cookie_file_path):
        data = None
        if not os.path.exists(cookie_file_path):
            raise Exception("Invalid cookie-file path - %s"%cookie_file_path)
        with open(cookie_file_path, 'r') as cf:
            try:
                data = json.load(cf)
            except:
                raise Exception("Invalid json file - %s"%cookie_file_path)
            
        cookie = data.get('aoc-session-cookie', None) if data else None
        if cookie is None:
            raise Exception("Invalid cookie file")

        return cookie
        
    @staticmethod
    def get_clean_response(page):
        page = re.findall("article\>(.*)\</article", page, re.DOTALL)[0]
        page = re.sub('\<a href.*?\</a\>', "", page)
        page = page.replace('<p>','').replace('</p>','')
        return page
        

class AOCCommunicator:
    INPUT_CACHE_DIR = 'inputs'
    def __init__(self, usession, uname = None):
        global TEMPLATE_HEADER
        self.headers = copy.deepcopy(TEMPLATE_HEADER)
        self.headers['Cookie'] = 'session=%s'%usession
        self.network_call_count = 0
        if uname is not None:
            self.validate_session(uname.strip())
        os.makedirs(AOCCommunicator.INPUT_CACHE_DIR, exist_ok=True)

    def get_user_name(self):
        global ROOT_URL
        page = self.get_response(ROOT_URL)
        #print(page)
        match = re.search('div class="user"\>(.*?) \<', page)
        if match:
            uname = match.group(1).strip()
            return uname
        return None

    def validate_session(self, uname):
        if uname == self.get_user_name():
            return True
        else:
            raise Exception("Invalid Session")
            
    def get_response(self, url, post_data = None):
        global ENCODING_TYPE
        req = request.Request(url, headers=self.headers)
        try:
            if post_data:
                post_data_raw =  parse.urlencode(post_data).encode()
                res = request.urlopen(req, data = post_data_raw)
            else:
                res = request.urlopen(req)
        except HTTPError as ee:
            ss = "Link: %s\n"%(url)
            ss = ss + "is post request? %r\n"%(bool(post_data))
            ss = ss + "session-cookie: %s\n"%(self.headers['Cookie'])
            raise Exception(ss)
            
        self.network_call_count += 1
        print("<DBG> Network call #%d" % (self.network_call_count))
        page = res.read().decode(ENCODING_TYPE)
        return page

    def get_input_file(self, year, day, force = False):
        file_path = os.path.join(AOCCommunicator.INPUT_CACHE_DIR, f'{year}_{day}.txt')
        if (not force) and os.path.exists(file_path):
            print("<DBG> Input file for challenge - %d/day_%d already exists. Using the data from file"%(year, day))
            page = ''
            with open(file_path, 'r') as inp_file:
                page = inp_file.read()     
        else:
            page = self.get_response(AOCMiscUtil.get_input_file_url(year, day))
            with open(file_path, 'w') as inp_file:
                inp_file.write(page)
        return page

    
    def submit_answer(self, year, day, level, answer):
        url = AOCMiscUtil.get_answer_url(year, day) 
        post_data = {
            'level' : level,
            'answer' : str(answer)
        }
        page = self.get_response(url, post_data = post_data)
        return AOCMiscUtil.get_clean_response(page)






def aoc_comm(settings, level):
    def deco(func):
        nonlocal settings
        session_cookie = AOCMiscUtil.get_cookie(settings['cookie-path'])
        comm = AOCCommunicator(session_cookie)
        def new_func():
            nonlocal comm
            nonlocal settings, level
            page = comm.get_input_file(settings['year'], settings['day'])
            ans = func(page)
            if (ans == None) or ( "y" != input("Submit answer - %s  for level %d? " %(str(ans), level) ) ):
                return "Ans for level - %d not submitted"%(level)
            response = comm.submit_answer(settings['year'], settings['day'], level, ans)
            return "Response from AOC: %s"%response
        new_func.raw_ = func
        return new_func
    return deco


def run_example(solver, example):
    return solver.raw_(example)
