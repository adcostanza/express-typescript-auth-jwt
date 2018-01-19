from subprocess import call
call(["docker-compose", "down","-v"])
call(["docker-compose","up","-d","db"])

import time
time.sleep(2)

import TestServer as test

#setup first user
success = test.hasTrueProperty('success')
body = test.anyAssert('get','/setup/09809asdf09dfadsf3','first time setup',[success])

hasToken = test.hasProperty("token","have token in response")

body = test.anyAssert('post','/login','first login as adam',{'username':'adam','password':'tacos'},[hasToken])
token = test.getValueFromResponse(body,'token')
token = {'x-access-token':token}

hasUsername = test.hasPropertyEqualTo('username',"adam","have username:adam in response")
claims = test.anyAssert('get','/claims','getting all claims',tests=[hasUsername],headers=token)
#print(claims)
