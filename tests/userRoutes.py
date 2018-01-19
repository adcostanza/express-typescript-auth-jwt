from subprocess import call
call(["docker-compose", "down","-v"])
call(["docker-compose","up","-d"])

import time
time.sleep(2)

import TestServer as test

success = test.hasTrueProperty('success')
body = test.anyAssert('get','/setup/09809asdf09dfadsf3','first time setup',[success])


hasToken = test.hasProperty("token","have token in response")

body = test.anyAssert('post','/login','first login as adam',{'username':'adam','password':'tacos'},[hasToken])
token = test.getValueFromResponse(body,'token')

#success = test.hasProperty('success','have success property')
fail = test.hasFalseProperty("success")

test.anyAssert('post','/passwords','change adams password to tac0', {'password':'tac0'},[success],{'x-access-token':token})
test.anyAssert('post','/login','login as adam with password tac0',{'username':'adam','password':'tac0'},[hasToken])
test.anyAssert('post','/users/george','create new user george', {'password':'potato','role':'user'},[success],{'x-access-token':token})
claims = test.anyAssert('get','/claims/george','get claims for george',headers={'x-access-token':token})
print(claims)
test.anyAssert('post','/login','login as george',{'username':'george','password':'potato'},[hasToken])
test.anyAssert('delete','/users/george','delete new user george',tests=[success],headers={'x-access-token':token})
test.anyAssert('post','/login','fail to login as george',{'username':'george','password':'potato'},statusExpected=401)
