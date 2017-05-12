import requests
import browser_cookie3
import json
from os.path import expanduser
import datetime
import sys
import re
import os
import urllib
import argparse

BROWSER_CHROMIUM = 'chromium'
BROWSER_CHROME = 'chrome'
BROWSER_FIREFOX = 'firefox'

URL_ME = 'https://clickup.up.ac.za/learn/api/public/v1/users/me'
URL_BASE_USER = 'https://clickup.up.ac.za/learn/api/public/v1/users'
URL_BASE = 'https://clickup.up.ac.za'
URL_BASE_COURSE = 'https://clickup.up.ac.za/learn/api/public/v1/courses'

URL_BASE_LINK = 'https://clickup.up.ac.za/webapps/blackboard/execute/content/file?cmd=view&content_id='

TYPE_FOLDER = 'resource/x-bb-folder'
TYPE_FILE = 'resource/x-bb-file'
TYPE_DOCUMENT = 'resource/x-bb-document'

YEAR = 2017

VERSION = 'v1.0.2'

def main():
    parser = argparse.ArgumentParser(description='Create a file mirror from ClickUP')
    parser.add_argument('-b', '--browser', help='The browser to be used for authentication [default: chromium]', required=False, type=str, default='chromium')
    parser.add_argument('-o', '--outpur-dir', help='The directory to create the mirror in [default: mirror/]', required=False, type=str, default='mirror/')
    parser.add_argument('-t', '--file-types', help='Comma-separated list of file types to download [default: pdf]', required=False, type=str, default='pdf')
    parser.add_argument('-d', '--data-file', help='File to be used for the database cache. \
    Will be created if it does not exist [default: mirror/database.json]', required=False, type=str, default='mirror/database.json')
    #parser.add_argument('-f', '--force-overwrite', help='Overwrite existing files in the mirror directroy [default: False]', required=False, action='store_true', default=False)
    parser.add_argument('-n', '--dry-run', help='Only generate the database file. Do not download anything [default: False]', required=False, action='store_true', default=False)
    parser.add_argument('--version', action='version', version='%(prog)s ' + VERSION)

    args = parser.parse_args()

    fileTypes = args.file_types.split(',')
    rootFolder = expanduser(args.outpur_dir)

    if not os.path.exists(rootFolder):
        os.makedirs(rootFolder)

    dataFile = args.data_file

    if args.data_file == 'mirror/database.json':
        dataFile = rootFolder + 'database.json'

    print('File types: ' + str(fileTypes))
    print('Mirror directory: ' + rootFolder)
    print('Database file: ' + dataFile)

    if args.dry_run:
        print('DRY RUN...')

    print('Fetching Session Token from ' + args.browser)
    s_session_id = getCookie(args.browser)

    if not isLoggedIn(s_session_id):
        print("Please log into ClickUP using " + args.browser)
        exit(1)

    if os.path.isfile(dataFile):
        data = loadDataFile(dataFile)
    else:
        data = getStructure(s_session_id)
        saveDataFile(args.data_file, data)

    printData(data)

    if not args.dry_run:
        downloadData(s_session_id, data, rootFolder, fileTypes)

def saveDataFile(filePath, data):
    if not os.path.exists(os.path.dirname(filePath)):
        try:
            os.makedirs(os.path.dirname(filePath))
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise

    f = open(filePath, 'w')
    json.dump(data, f)
    f.close()

def loadDataFile(filePath):

    data = []

    if os.path.isfile(filePath):
        f = open(filePath, 'r')
        data = json.load(f)
        f.close()

    return data

def getCookie(browser):

    cj = {}
    s_session_id = -1;

    if browser == BROWSER_CHROMIUM:
        cj = browser_cookie3.chrome(expanduser('~/.config/chromium/Default/Cookies'))
    elif browser == BROWSER_CHROME:
        cj = browser_cookie3.chrome()
    elif browser == BROWSER_FIREFOX:
        cj = browser_cookie3.firefox()
    else:
        print('[ERROR] Invalid Browser String! See --help')
        exit(1)

    if len(cj) > 0:
        for cookie in cj:
            if cookie.domain == 'clickup.up.ac.za' and cookie.name == 's_session_id':
                s_session_id = cookie.value

    return s_session_id;

def getResponse(s_session_id, method, url):
    headers = {'Cookie': 's_session_id=' + s_session_id, 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36'}

    r = requests.request(method, url, headers=headers, allow_redirects=False)
    return r

def isLoggedIn(s_session_id):
    r = getResponse(s_session_id, 'GET', URL_ME)

    if (r.status_code == 200):
        return True
    else:
        return False

def getUID(s_session_id):
    r = getResponse(s_session_id, 'GET', URL_ME)

    if r.status_code == 200:
        data = json.loads(r.text)
        return data['id']
    else:
        return -1

def getCoursesUrl(uid):
    return URL_BASE_USER + '/' + uid + '/courses'

def getCourses(s_session_id, uid):
    print("Fetching course list...")

    courseList = []
    data = {}
    done = False
    nextUrl = getCoursesUrl(uid)

    while not done:
        r = getResponse(s_session_id, 'GET', nextUrl)

        if (r.status_code == 200):
            data = json.loads(r.text)
        else:
            break

        for row in data['results']:
            # 2016-02-21T15:13:05.000Z
            courseYear = datetime.datetime.strptime(row['created'], '%Y-%m-%dT%H:%M:%S.000z').date().year

            if courseYear == YEAR:
                tmpCourse = {}
                tmpCourse['id'] = row['courseId']
                tmpCourse['title'] = getCourseName(s_session_id, row['courseId'])
                courseList.append(tmpCourse)

        if 'paging' in data:
            nextUrl = URL_BASE + data['paging']['nextPage']
        else:
            done = True

    return courseList

def getCourseName(s_session_id, courseId):
    r = getResponse(s_session_id, 'GET', URL_BASE_COURSE + '/' + courseId)

    if r.status_code == 200:
        data = json.loads(r.text)
        return data['name']
    else:
        print('Error getting course name for id ' + courseId)
        return -1

def getJson(s_session_id, url):
    r = getResponse(s_session_id, 'GET', url)

    data = {}

    if r.status_code == 200:
        data = json.loads(r.text)
    else:
        print('Error getting JSON for ' + url)
        print('status_code: ' + str(r.status_code))
        print('response: ' + r.text)

    return data

# Get the initial ids
# Get the initial folders from base
# Recrusively get the children if they are folder

def getCourseFolders(s_session_id, courseId):
    print('Fetching Course folders for ' + courseId)

    data = getJson(s_session_id, URL_BASE_COURSE + '/' + courseId + '/contents')

    folderList = []

    if 'results' in data and len(data['results']) > 0:
        for row in data['results']:
            if 'contentHandler' in row and row['contentHandler']['id'] == TYPE_FOLDER:

                folder = {}
                folder['id'] = row['id']
                folder['title'] = row['title']
                folder['type'] = TYPE_FOLDER

                folderList.append(folder)

    return folderList

def getChildren(s_session_id, courseId, itemId):
    print("Fetching children for " + itemId)

    data = getJson(s_session_id, URL_BASE_COURSE + '/' + courseId + '/contents/' + itemId + '/children')

    itemList = []

    if 'results' in data and len(data['results']) > 0:
        for row in data['results']:
            item = {}
            item['id'] = row['id']
            item['title'] = row['title']
            item['type'] = row['contentHandler']['id']

            if item['type'] == TYPE_FILE:
                link = getFileLinks(s_session_id, courseId, item['id'], item['type'])
                print(str(len(link)) + ' links found')

                if len(link) > 0:
                    item['link'] = link[0];

            elif item['type'] == TYPE_DOCUMENT:
                #print("RESOLVE FOR DOCUMENT...")
                # We need to get the document children here because it is an endpoint
                links = getFileLinks(s_session_id, courseId, item['id'], item['type'])

                print(str(len(links)) + ' links found')

                if len(links) > 0:
                    item['children'] = []
                    for l in links:
                        #print("DOCUMENT CHILDREN FOUND!")
                        child = {}
                        child['title'] = getNameFromUrl(l)
                        child['link'] = l
                        item['children'].append(child)

            itemList.append(item)

    return itemList

def getCourseStructure(s_session_id, courseId):
    print('Fetching course structure for ' + courseId)

    initialFolderList = getCourseFolders(s_session_id, courseId)

    # 0 (id, title, type, children[])
    # 0['children'][0]
    #   (id, title, type, children)

    for folder in initialFolderList:
        getChildrenRec(s_session_id, courseId, folder['id'], folder)

    return initialFolderList

def getChildrenRec(s_session_id, courseId, itemId, parent):
    data = getChildren(s_session_id, courseId, itemId)

    # data belongs to parentChildList

    for item in data:
        # Add children
        if not 'children' in parent:
            parent['children'] = []

        parent['children'].append(item)

        if item['type'] == TYPE_FOLDER:
            getChildrenRec(s_session_id, courseId, item['id'], item)


def getStructure(s_session_id):
    uid = getUID(s_session_id)
    courseList = getCourses(s_session_id, uid) # array

    for course in courseList:
        course['children'] = getCourseStructure(s_session_id, course['id'])

    return courseList

def getFileLinks(s_session_id, courseId, itemId, itemType):
    print('Resolving links for ' + courseId + '/' + itemId)

    if itemType == TYPE_FILE:
        r = getResponse(s_session_id, 'GET', URL_BASE_LINK + itemId + '&course_id=' + courseId + '&launch_in_new=true')
    elif itemType == TYPE_DOCUMENT:
        r = getResponse(s_session_id, 'GET', URL_BASE_LINK + itemId + '&course_id=' + courseId + '&framesetWrapped=true')

    redirPage = re.compile('document.location = ')

    filePageReg = re.compile('Your download will start shortly. If it does not, click')
    docPageReg = re.compile('If this item does not open automatically you can')
    noFilesErrorReg = re.compile('<span style="color:;">Error</span>  </span></h1>')

    goodLinks = []
    checkedInitLinks = []

    if r.status_code == 302:
        print("REDIRECT too early!")
        print(r)
        return []

    if r.status_code == 200:
        #print(r.text)
        if filePageReg.search(r.text) or docPageReg.search(r.text) or redirPage.search(r.text):
            # document.location = '/bbcswebdav/pid-963363-dt-content-rid-11056085_1/xid-11056085_1';
            # https://clickup.up.ac.za/bbcswebdav/pid-963311-dt-content-rid-10514149_1/xid-10514149_1

            # TODO: Better name
            reg = re.compile('(/bbcswebdav/pid-[0-9]*-dt-content-rid-[0-9]*_1/xid-[0-9]*_1)')
            #regex = '(/bbcswebdav/pid-[0-9]*-dt-content-rid-[0-9]*_1/xid-[0-9]*_1)'

            l = reg.findall(r.text, 0, len(r.text))

            #print(l)
            #print(str(len(l)) + ' links found by regex')

            for initLink in l:
                if initLink not in checkedInitLinks:
                    checkedInitLinks.append(initLink)

                    # Yet again
                    #print('Resolve: ' + link)
                    r2 = getResponse(s_session_id, 'GET', URL_BASE + initLink)

                    if r2.status_code == 302:
                        goodLinks.append(r2.headers['Location'])
                        print('    -> ' + r2.headers['Location'])
        elif noFilesErrorReg.search(r.text):
            print('No files for document at ' + URL_BASE_LINK + itemId + '&course_id=' + courseId)
        else:
            print("Error Getting link for " + URL_BASE_LINK + itemId + '&course_id=' + courseId)

    return goodLinks

def getExtFromUrl(url):
    fname = url.split('/')
    fname = fname[-1].replace('%20', ' ')
    ext = fname.split('.')
    ext = ext[-1]

    return ext

def getNameFromUrl(url):
    fname = url.split('/')
    fname = fname[-1]

    fname = urllib.parse.unquote(fname)

    return fname

def downloadFile(s_session_id, url, destFolder):

    if not os.path.exists(destFolder):
        os.makedirs(destFolder)

    fname = getNameFromUrl(url)

    print("Downloading " + fname + ' to ' + destFolder)
    r = getResponse(s_session_id, 'GET', url)
    #print("Done")

    f = open(destFolder + fname, 'wb')
    f.write(r.content)
    f.close()

def hasFilesRec(item):
    result = False

    if 'children' in item:
        for child in item['children']:
            result = result or hasFilesRec(child)

        return result
    else:
        if 'link' in item:
            return True
        else:
            return False

def printRec(data, wrapper):

    for item in data:

        if 'link' in item or ('children' in item and hasFilesRec(item)):
            for i in range(0, wrapper[0]):
                sys.stdout.write('    |')
            if wrapper[0] > 0:
                sys.stdout.write('- ')

        if 'link' in item:
            print(getNameFromUrl(item['link']))
        elif 'children' in item:
            if hasFilesRec(item):
                print(item['title'])

        if 'children' in item:
            wrapper[0] += 1
            printRec(item['children'], wrapper)
            wrapper[0] -= 1

def printData(data):

    wrapper = [0]
    printRec(data, wrapper)

def downloadRec(s_session_id, dataList, rootFolder, fileTypes, rollingPath):
    # Check every type in the array
    # If file, check the ext from the link

    for item in dataList:
        if 'link' in item:
            if getExtFromUrl(item['link']) in fileTypes:
                if not os.path.isfile(rootFolder + rollingPath[0] + getNameFromUrl(item['link'])):
                    downloadFile(s_session_id, item['link'], rootFolder + rollingPath[0])

        if 'children' in item:
            origRollingPath = rollingPath[0]
            rollingPath[0] += item['title'] + '/'

            downloadRec(s_session_id, item['children'], rootFolder, fileTypes, rollingPath)
            rollingPath[0] = origRollingPath

def downloadData(s_session_id, data, rootFolder, fileTypes):

    if not os.path.exists(rootFolder):
        os.makedirs(rootFolder)

    rollingPath = ['']

    downloadRec(s_session_id, data, rootFolder, fileTypes, rollingPath)

main()
