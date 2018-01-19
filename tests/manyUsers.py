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

names = ['Grant-Blanchard','Jaqueline-Ho','Molly-Zimmerman','Dominic-Dennis','Daniela-Shaw','Clarence-Bowen','Keegan-Strong','Ryder-Ross','Kimora-Medina','Hailee-Crane','Kianna-Aguilar','Cash-Long','Bryanna-White','June-Haynes','Lainey-Mcintosh','Raegan-Valencia','Kallie-Frye','Edward-Villegas','Jesus-Patrick','Jessie-Branch','Nancy-Mahoney','Eliezer-Carlson','Erica-Benitez','Paola-Spencer','Lydia-Gamble','Zachariah-Trujillo','Aimee-Barrett','Finley-Estrada','Andy-Hodge','Kaya-Rush','Jonas-Yang','Malachi-Bender','Yasmin-Rodriguez','Nathanial-Reyes','Jaylynn-Melton','Kayden-Barker','Kate-Humphrey','Sloane-French','Omar-Garrett','Wyatt-Lindsey','Ibrahim-Sosa','Mareli-Cisneros','Courtney-Rivas','Riley-Cummings','Kristin-Wright','Alonso-Mccarty','Britney-Vargas','Breanna-Lewis','Carina-Oconnell','Nathanael-Cline','Valeria-Smith','Khloe-Oneill','Erik-Nichols','Darien-Bowers','Jaida-Romero','Lorelei-Leblanc','Malakai-Proctor','Carter-Moody','Marley-Olson','Lamar-David','Gracie-Coleman','Deegan-Michael','Jake-Banks','Anabelle-Huff','Callum-Weber','Jayden-Morrow','Franklin-Lam','Jazmyn-Blake','Justine-Chavez','Mauricio-Charles','Zaria-Potts','Alisson-Clements','Alina-Holt','Dana-Powers','Aubrey-Rosales','Sawyer-Perkins','Kenyon-Norman','Lindsay-Glover','Alexa-Kidd','Daphne-Harper','Alejandra-Maldonado','Kendall-Mcdaniel','Giada-Bolton','Patrick-Mcdonald','Kaiya-Aguirre','Alana-Rivera','Felicity-Brandt','Renee-Brooks','Jerimiah-Sellers','Rigoberto-Blackwell','Kamryn-Boyd','Ryan-Alexander','Kyson-Wheeler','Yair-Harvey','Marcus-Avila','Jaydan-Bradshaw','Araceli-Massey','Carolyn-Crawford','Taniyah-Thomas','Jaelynn-Mullins','Van-Clarke','Leila-Sims','Adelyn-Doyle','Luis-Cohen','Kailyn-Bradley','Chase-Ramsey','Madeleine-Ball','Kash-Kennedy','Lesly-Cole','Austin-Holden','Graham-Trevino','Ezra-Kramer','Fernanda-Huang','Grady-Oliver','Billy-Harrington','Sophia-Barajas','Walker-Lozano','Quintin-Schaefer','Dallas-Larson','Kamila-Schwartz','Kaelyn-Holder','Luna-Welch','Carmen-Burns','Sandra-Wilkinson','Kaiden-Ayers','Bridget-Stafford','Shania-Sanders','Charity-Hensley','Alicia-Carney','Davon-Sutton','Mylie-Cain','Morgan-Blevins','Xzavier-Ortega','Addisyn-Cooke','Dustin-Merritt','Thaddeus-Scott','Memphis-Stephens','Leyla-Mcfarland','Aryana-Berry','Neveah-Pennington','Mckinley-Salas','Mariah-Roth','Cora-Bird','Malik-Potter','Skyler-Goodwin','Gillian-Leonard','Abigayle-Johns','Donna-Poole','Samuel-Mendoza','Kaylee-Santos','Tristan-Solis','Riley-Patel','Easton-Franklin','Cristian-Waller','Cadence-Hammond','Donavan-Morgan','Annabella-Gallegos','Alexus-Mayo','Jayvon-Stephenson','Maxwell-Foley','Randy-Dunlap','Harry-Eaton','Sincere-Hayden','Ashton-Barnes','Charlize-Brady','Roger-Vaughan','Savanah-Peters','Dayami-Anthony','Trace-Rojas','Sienna-Santana','Demetrius-Bryan','Dashawn-Lin','Leonardo-Warren','Oswaldo-Cantrell','Haven-Foster','Genesis-Byrd','Axel-Callahan','Cheyenne-Harris','Braeden-Benjamin','Rubi-Novak','Paloma-Bell','Aaron-Gross','Madelynn-Logan','Raina-Hughes','Marshall-Hardy','Cara-Gonzalez','Damari-Molina','Maddison-Conley','Joel-Sherman','Miguel-Simmons','Sydnee-Beltran','Zaiden-Oconnor','Matilda-Weiss','Levi-Chung','Abraham-Flores','Angela-Frey','Giovanna-Fletcher','Gaven-Rice','Devan-Davenport','Daniel-Chen']
from random import randint
lastUser = names[0];
for name in names:
    user = {"username":name,"pw":str(randint(0, 23424)), "role":"user"}
    test.anyAssert('post','/users/'+name,'create user '+name,{'password':user['pw'],'role':user['role']},[success], {'x-access-token':token})
    test.anyAssert('post','/users/'+name,'fail to create another user '+name,{'password':'tac0s','role':'user'},[fail], {'x-access-token':token})
    token2 = test.anyAssert('post','/login','login as '+name,{'username':name,'password':user['pw']},[hasToken])
    token2 = test.getValueFromResponse(token2,'token')
    new_pw = str(randint(0, 23424))
    test.anyAssert('post','/passwords/','change password as '+name,{'password':new_pw},[success], {'x-access-token':token2})
    new_pw2 = str(randint(0, 23424))
    test.anyAssert('post','/passwords/'+lastUser,'fail to change '+lastUser+' another user password as user '+name,{'password':new_pw2},headers={'x-access-token':token2},statusExpected=401)

    test.anyAssert('post','/login','login as '+name+' with new pw',{'username':name,'password':new_pw},[hasToken])
    test.anyAssert('post','/login','fail to login as '+name+' with old pw',{'username':name,'password':user['pw']},statusExpected=401)
    test.anyAssert('post','/login','fail to login as '+lastUser+' with new pw',{'username':lastUser,'password':new_pw2},statusExpected=401)



    lastUser = name
