import requests
import json
import sys

class c:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

base = "http://localhost/api"

def request(type,url,data,headers):
    if(type == 'post'): r = requests.post(base+url,data=data,headers=headers)
    if(type == 'get'): r = requests.get(base+url,headers=headers)
    if(type == 'put'): r = requests.put(base+url,data=data,headers=headers)
    if(type == 'delete'): r = requests.delete(base+url,headers=headers)
    try:
        data = r.json()
        return {"status":r.status_code,"body":data};
    except Exception as e:
        return {"status":r.status_code, 'body':[]}

# Test to check if property exists and print colored response
class hasProperty:
    def __init__(self,property, should):
        self.assertion = {'property':property,'should':should}
    def check(self, url, body):
        if(not isinstance(body,list)):
            if self.assertion['property'] not in body:
                exception = "✗ POST ⤰ "+url+": should "+self.assertion['should']
                print(c.FAIL + exception+ c.ENDC)
                sys.exit(1)
                return
            print(c.OKGREEN + "✓ POST ⤳ "+url+": should "+self.assertion['should'] + c.ENDC)
        else:
            for element in body:
                if self.assertion['property'] not in element:
                    exception = "✗ POST ⤰ "+url+": should "+self.assertion['should']
                    print(c.FAIL + exception+ c.ENDC)
                    sys.exit(1)
                    return
                print(c.OKGREEN + "✓ POST ⤳ "+url+": should "+self.assertion['should']+ c.ENDC)
class hasTrueProperty:
    def __init__(self,property):
        self.property = property
    def check(self, url, body):
        try:
            if body[self.property]:
                print(c.OKGREEN + "✓ POST ⤳ "+url+": should have property "+str(self.property)+":true" + c.ENDC)
                return
            exception = "✗ POST ⤰ "+url+": should have property "+str(self.property)+":true but it is "+str(body[self.property])
            print(c.FAIL + exception+ c.ENDC)
            sys.exit(1)
        except Exception as e:
            exception = "✗ POST ⤰ "+url+": should have property "+str(self.property)+":true but the property does not exist "+str(body[self.property])
            print(c.FAIL + exception+ str(e) +c.ENDC)
            sys.exit(1)
class hasFalseProperty:
    def __init__(self,property):
        self.property = property
    def check(self, url, body):
        try:
            if not body[self.property]:
                print(c.OKGREEN + "✓ POST ⤳ "+url+": should have property "+self.property+":false" + c.ENDC)
                return
            exception = "✗ POST ⤰ "+url+": should have property "+self.property+":false but it is "+str(body[self.property])
            print(c.FAIL + exception+ c.ENDC)
            sys.exit(1)
        except:
            exception = "✗ POST ⤰ "+url+": should have property "+self.property+":false but the property does not exist "+str(body[self.property])
            print(c.FAIL + exception+ c.ENDC)
            sys.exit(1)
class hasPropertyEqualTo:
    def __init__(self,property,equals,should):
        self.property = property
        self.equals = equals
        self.should = should
    def check(self, url, body):
        try:
            if(not isinstance(body,list)):
                if body[self.property] != self.equals:
                    exception = "✗ POST ⤰ "+url+": should "+self.should + " but instead equals "+self.equals
                    print(c.FAIL + exception+ c.ENDC)
                    sys.exit(1)
                    return
                print(c.OKGREEN + "✓ POST ⤳ "+url+": should "+self.should + c.ENDC)
            else:
                #should have at least one element with property equal to value
                success=False
                for element in body:
                    if element[self.property] == self.equals:
                        print(c.OKGREEN + "✓ POST ⤳ "+url+": should "+self.should + " at least once" + c.ENDC)
                        success=True
                    else:
                        exception = "✗ POST ⤰ "+url+": should "+self.should + " but instead equals "+self.equals
                        print(c.WARNING + exception+ c.ENDC)
                if(not success):
                    exception = "✗ POST ⤰ "+url+": should "+self.should
                    print(c.FAIL + exception+ c.ENDC)
                    sys.exit(1)
        except:
            exception = "✗ POST ⤰ "+url+": should have property "+self.property+":"+self.equals+" but the property does not exist"
            print(c.FAIL + exception+ c.ENDC)
            sys.exit(1)
#to be used for all tests
#tests can be empty or contain the same tests such as succcess property existing, etc.
def anyAssert(type,url,description, data=[], tests=[], headers={}, statusExpected=200):
    print(c.OKBLUE + description + c.ENDC)
    try:
        response = request(type,url,data,headers)
        body = response['body']
        status = response['status']
        exception = "✗ POST ⤰ "+url+" response status not "+str(statusExpected)+" ("+str(status)+")"
        if not status == statusExpected:
            print(c.FAIL + exception+ c.ENDC)
            sys.exit(1)
            return []
        print(c.OKGREEN + "✓ POST ⤳ "+url+" response status "+str(statusExpected) + c.ENDC)
        for test in tests:
            test.check(url,body)
        return body;
    except Exception as e:
        print(c.FAIL + "✗ POST failed " + str(e) + c.ENDC)
        sys.exit(1)
def getValuesFromResponse(response,key):
    try:
        return [r[key] for r in response]
    except Exception as e:
        print(c.FAIL + "✗ Unable to get value for property " + key + c.ENDC)
        sys.exit(1)
def getValueFromResponse(response,key):
    try:
        return response[key]
    except Exception as e:
        print(c.FAIL + "✗ Unable to get value for property " + key + c.ENDC)
        sys.exit(1)
