import random as rm
import time

def help():
    print("example")
    print(" torancell.red()")
    print(" str = torancell.getred()")
    print(" torancell.quiz()")
    print(" torancell.art()")
    print(" torancell.bogo(int)")
def red():
    str = "かたい カラに つつまれているが なかみは やわらかいので つよい こうげきには たえられない。"
    print(str)
def blue():
    str = "カラが かたくなるまえに つよい しょうげきを うけると なかみが でてしまうので ちゅうい。"
    print(str)
def pikachu():
    str = "みをまもるため ひたすら カラを かたくしても つよい しょうげきを うけると なかみが でてしまう。"
    print(str)
def gold():
    str = "カラのなかは しんかの じゅんびで とても やわらかく くずれやすい。 なるべく うごかないようにしている。"
    print(str)
def silver():
    str = "いっしょうけんめい そとがわの カラをかため しんかの じゅんびで やわらかい からだを まもっている。"
    print(str)
def crystal():
    str = "しんかを まっている じょうたい。かたくなる ことしか できないので おそわれないよう じっとしている。"
    print(str)
def ruby():
    str = "からだの カラは てっぱんの ように かたい。あまり うごかないのは カラのなかで やわらかい なかみが しんかの じゅんびを しているからだ。"
    print(str)
def diamond():
    str = "こうてつのように かたい カラで やわらかい なかみを まもっている。しんかするまで じっと たえている。"
    print(str)
def sun():
    str = "カラのなかには トロトロの なかみが つまっている。ほぼうごかないのは ウッカリ なかみが こぼれないため。"
    print(str)
def moon():
    str = "かたいと いっても むしの カラ。われてしまうことも あるので はげしい たたかいは きんもつ。"
    print(str)
def ultrasun():
    str = "カラのなかは ドロドロの えきたい。 しんかに そなえて からだじゅうの さいぼうを つくりなおしている。"
    print(str)
def ultramoon():
    str = "とても かたいカラは ツツケラに つつかれても びくともしないが ゆれて なかみが こぼれてしまう。"
    print(str)
def green():
    red()
def firered():
    red()
def shield():
    red()
def leafgreen():
    blue()
def y():
    blue()
def heartgold():
    gold()
def soulsilver():
    silver()
def sword():
    crystal()
def sapphire():
    ruby()
def emerald():
    ruby()
def omegaruby():
    ruby()
def alphasapphire():
    ruby()
def pearl():
    diamond()
def platinum():
    diamond()
def black():
    diamond()
def white():
    diamond()
def black2():
    diamond()
def white2():
    diamond()
def x():
    diamond()

def getred():
    str = "かたい カラに つつまれているが なかみは やわらかいので つよい こうげきには たえられない。"
    return(str)
def getblue():
    str = "カラが かたくなるまえに つよい しょうげきを うけると なかみが でてしまうので ちゅうい。"
    return(str)
def getpikachu():
    str = "みをまもるため ひたすら カラを かたくしても つよい しょうげきを うけると なかみが でてしまう。"
    return(str)
def getgold():
    str = "カラのなかは しんかの じゅんびで とても やわらかく くずれやすい。 なるべく うごかないようにしている。"
    return(str)
def getsilver():
    str = "いっしょうけんめい そとがわの カラをかため しんかの じゅんびで やわらかい からだを まもっている。"
    return(str)
def getcrystal():
    str = "しんかを まっている じょうたい。かたくなる ことしか できないので おそわれないよう じっとしている。"
    return(str)
def getruby():
    str = "からだの カラは てっぱんの ように かたい。あまり うごかないのは カラのなかで やわらかい なかみが しんかの じゅんびを しているからだ。"
    return(str)
def getdiamond():
    str = "こうてつのように かたい カラで やわらかい なかみを まもっている。しんかするまで じっと たえている。"
    return(str)
def getsun():
    str = "カラのなかには トロトロの なかみが つまっている。ほぼうごかないのは ウッカリ なかみが こぼれないため。"
    return(str)
def getmoon():
    str = "かたいと いっても むしの カラ。われてしまうことも あるので はげしい たたかいは きんもつ。"
    return(str)
def getultrasun():
    str = "カラのなかは ドロドロの えきたい。 しんかに そなえて からだじゅうの さいぼうを つくりなおしている。"
    return(str)
def getultramoon():
    str = "とても かたいカラは ツツケラに つつかれても びくともしないが ゆれて なかみが こぼれてしまう。"
    return(str)
def getgreen():
    return(getred())
def getfirered():
    return(getred())
def getshield():
    return(getred())
def getleafgreen():
    return(getblue())
def gety():
    return(getblue())
def getheartgold():
    return(getgold())
def getsoulsilver():
    return(getsilver())
def getsword():
    return(getcrystal())
def getsapphire():
    return(getruby())
def getemerald():
    return(getruby())
def getomegaruby():
    return(getruby())
def getalphasapphire():
    return(getruby())
def getpearl():
    return(getdiamond())
def getplatinum():
    return(getdiamond())
def getblack():
    return(getdiamond())
def getwhite():
    return(getdiamond())
def getblack2():
    return(getdiamond())
def getwhite2():
    return(getdiamond())
def getx():
    return(getdiamond())

def checkver(i):
    if i==1:
        return("red")
    elif i==2:
        return("green")
    elif i==3:
        return("blue")
    elif i==4:
        return("pikachu")
    elif i==5:
        return("gold")
    elif i==6:
        return("silver")
    elif i==7:
        return("crystal")
    elif i==8:
        return("ruby")
    elif i==9:
        return("sapphire")
    elif i==10:
        return("emerald")
    elif i==11:
        return("firered")
    elif i==12:
        return("leafgreen")
    elif i==13:
        return("pearl")
    elif i==14:
        return("diamond")
    elif i==15:
        return("platinum")
    elif i==16:
        return("heartgold")
    elif i==17:
        return("soulsilver")
    elif i==18:
        return("black")
    elif i==19:
        return("white")
    elif i==20:
        return("black2")
    elif i==21:
        return("white2")
    elif i==22:
        return("x")
    elif i==23:
        return("y")
    elif i==24:
        return("omegaruby")
    elif i==25:
        return("alphasapphire")
    elif i==26:
        return("sun")
    elif i==27:
        return("moon")
    elif i==28:
        return("ultrasun")
    elif i==29:
        return("ultramoon")
    elif i==30:
        return("sword")
    elif i==31:
        return("shield")

def quiz():
    i = rm.randint(1,31)
    if i==1:
        red()
    elif i==2:
        green()
    elif i==3:
        blue()
    elif i==4:
        pikachu()
    elif i==5:
        gold()
    elif i==6:
        silver()
    elif i==7:
        crystal()
    elif i==8:
        ruby()
    elif i==9:
        sapphire()
    elif i==10:
        emerald()
    elif i==11:
        firered()
    elif i==12:
        leafgreen()
    elif i==13:
        pearl()
    elif i==14:
        diamond()
    elif i==15:
        platinum()
    elif i==16:
        heartgold()
    elif i==17:
        soulsilver()
    elif i==18:
        black()
    elif i==19:
        white()
    elif i==20:
        black2()
    elif i==21:
        white2()
    elif i==22:
        x()
    elif i==23:
        y()
    elif i==24:
        omegaruby()
    elif i==25:
        alphasapphire()
    elif i==26:
        sun()
    elif i==27:
        moon()
    elif i==28:
        ultrasun()
    elif i==29:
        ultramoon()
    elif i==30:
        sword()
    elif i==31:
        shield()
    a = rm.randint(1,31)
    while a==i:
        a= rm.randint(1,31)
    b = rm.randint(1,31)
    while b==a or b==i:
        b = rm.randint(1,31)
    c = rm.randint(1,31)
    while c==a or c==b or c==i:
        c = rm.randint(1,31)
    l = list()
    l.append(checkver(a))
    l.append(checkver(b))
    l.append(checkver(c))
    l.append(checkver(i))
    rm.shuffle(l)
    print(l)
    str = input()
    if eval("get"+str)()==eval("get"+checkver(i))():
        print("True")
    else:
        print("False, correct answer is "+checkver(i))

def art():
    print("@@@@@@@@@@@@,%::S@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    print("@@@@@@@@@@@+::***,@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    print("@@@@@@@@@@********@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    print("@@@@@@@@@*********?@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    print("@@@@@@@@#**********#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    print("@@@@@@@S***********+.@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    print("@@@@@@@************++S@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    print("@@@@@@************.++.S@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    print("@@@@@:************%***.#*@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    print("@@@@:************#:#+..+++@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    print("@@,?************.,,,#??#++++@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    print("@@?************#+#:::::::.+++.#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    print("@@***********++....:::::+.++++.**#@@@@@@@@@@@@@@@@@@@@@@@@@@")
    print("@,***.**.+++:********.+.+++++++..***#@@@@@@@@@@@@@@@@@@@@@@@")
    print("@+:+******+*********.++++++++++++..**:*..@@@@@@@@@@@@@@@@@@@")
    print(",S:***********?****.+++++++++++++++..*****?@@@@@@@@@@@@@@@@@")
    print(",#:*************.?++++++++++++++++++++++*,@@@@@@@@@@@@@@@@@@")
    print(".+:*****?*********.#+++++++++++++++++++.,@@@@@@@@@@@@@@@@@@@")
    print("::*****.************+#++++++++++++++++?@@@@@@@@@@@@@@@@@@@@@")
    print(",:+**.+?************+++++++++++++++++#@@@@@@@@@@@@@@@@@@@@@@")
    print("@@+#+S..*********.+S+++++++++++++++++@@@@@@@@@@@@@@@@@@@@@@@")
    print("@@@?+SSSS#.++++++++.+++++++++++++++++,@@@@@@@@@@@@@@@@@@@@@@")
    print("@@@@@@#+++++#++++%+++++++++++++++++++++#@@@@@@@@@@@@@@@@@@@@")
    print("@@@@@@@@+.+++++.#++.+++++++++++++++++++++*@@@@@@@@@@@@@@@@@@")
    print("@@@@@@@@@#%++++++S++++..++++++++++++++++++?@@@@@@@@@@@@@@@@@")
    print("@@@@@@@@@@,**......+.++..*+++.+++++++++++++.,@@@@@@@@@@@@@@@")
    print("@@@@@@@@@@@@S?....*#+++..........++++++++++....@@@@@@@@@@@@@")
    print("@@@@@@@@@@@@@@@+....*+++............++++++++.....@@@@@@@@@@@")
    print("@@@@@@@@@@@@@@@@@...+..S++.........+++++++SSS+...+.@@@@@@@@@")
    print("@@@@@@@@@@@@@@@@@@@@,##+SS++#+++++++++++#SSSSSSS#++SS#@@@@@@")
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@.%SSS%SSSS#SSSSSSS###SSSSS+++?@@@")
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#SSS+#SSSSSSSSSSSS+?%+++++#")
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@,#S+S#+S%SSSSSSSSSSS+@@")
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@S#%+?#SS.#%,@@@@")

def printf(str):
    print(str, end='')

def bogo(i=200):
    l = list()
    l.append("ト")
    l.append("ラ")
    l.append("ン")
    l.append("セ")
    l.append("ル")
    s = list()
    s.append("ト")
    s.append("ラ")
    s.append("ン")
    s.append("セ")
    s.append("ル")
    t = 0
    while t!=i:
        t = t+1
        rm.shuffle(l)
        printf(l)
        print(t)
        if l==s:
            print("success!")
            t = i
        elif t==i:
            print("failure…")
        time.sleep(0.2)