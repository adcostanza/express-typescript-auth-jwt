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
body = test.anyAssert('post','/login','login as adam with password tac0',{'username':'adam','password':'tac0'},[hasToken])
test.anyAssert('post','/passwords','change adams password back to tacos',{'password':'tacos'},[success],{'x-access-token':token})

test.anyAssert('post','/users/george','create user george',{'password':'tac0s','role':'user'},[success], {'x-access-token':token})
test.anyAssert('post','/users/george','create another user george',{'password':'tac0s','role':'user'},[fail], {'x-access-token':token})

body2 = test.anyAssert('post','/login','login as user george',{'username':'george','password':'tac0s'},[hasToken])
userToken = test.getValueFromResponse(body2,'token')

test.anyAssert('post','/passwords/adam','fail to change adams password (only a user)',{'password':'potato'},headers={'x-access-token':userToken},statusExpected=401);
test.anyAssert('post','/login','login as adam with password potato',{'username':'adam','password':'potato'}, statusExpected=401)

test.anyAssert('post','/users/amy','create admin amy as user george',{'password':'tac0s','role':'admin'},headers={'x-access-token':userToken},statusExpected=401)
body = test.anyAssert('post','/login','login as admin amy with password tac0s',{'username':'amy','password':'tac0s'},statusExpected=401)

test.anyAssert('post','/passwords/george','successfully change georges password as adam (admin)',{'password':'potato'},[success],{'x-access-token':token})
test.anyAssert('post','/login','login as user george with new password',{'username':'george','password':'potato'},[hasToken])
test.anyAssert('post','/passwords/george','successfully change georges password back to original as adam (admin)',{'password':'tac0s'},[success],{'x-access-token':token})
test.anyAssert('post','/login','fail to login as george with older password',{'username':'george','password':'potato'},statusExpected=401)

##need to add getAssert
