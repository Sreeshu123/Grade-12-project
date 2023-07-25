import mysql.connector,csv,os
from datetime import datetime
obj=mysql.connector.connect(host="localhost",user="root",database="project",password="Sree1234$",autocommit=True,buffered=True)
c1=obj.cursor()
c2=obj.cursor()
#COMMANDS
q1='SELECT * FROM INFO'
q2='INSERT INTO CUSTOMER(CNAME) VALUES(%s)'
q3='SELECT PRICE,RTYPE FROM INFO WHERE RCODE=%s'
q4='SELECT CNAME FROM BOOKING'
q5='SELECT RCODE FROM BOOKING WHERE ROOMNO=%s'
q6='SELECT PRICE FROM INFO WHERE RCODE=%s'
q7='UPDATE CUSTOMER SET AMOUNT=%s,PAYSTATUS=%s WHERE CCODE=%s'
q8='SELECT DATE_ADD(%s,INTERVAL %s DAY)'
q9='SELECT CCODE FROM CUSTOMER WHERE CCODE=(SELECT MAX(CCODE) FROM CUSTOMER)'
q10='SELECT DATEDIFF(%s,%s)'
q11='INSERT INTO BOOKING(ROOMNO,RCODE,RTYPE,CCODE,CNAME,MEAL,CHECKIN,CHECKOUT,DAYS) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)'
q12='SELECT ROOMNO FROM ROOMS WHERE RCODE=%s'
q13='SELECT CHECKIN,CHECKOUT FROM BOOKING WHERE ROOMNO=%s'
q14='SELECT PRICEPERDAY FROM MEALS WHERE MCODE=%s'
q15='SELECT * FROM MEALS'
q16='UPDATE BOOKING SET CHECKOUT=%s,DAYS=DAYS+%s WHERE CNAME=%s AND ROOMNO=%s'
q17='SELECT CHECKOUT FROM BOOKING WHERE CNAME=%s AND ROOMNO=%s'
q18='SELECT CHECKIN FROM BOOKING WHERE ROOMNO=%s AND CNAME<>%s AND CHECKIN>%s ORDER BY CHECKIN'
q19='SELECT DATE_ADD(%s,INTERVAL %s DAY)'
q20='UPDATE BOOKING SET CHECKOUT=%s,DAYS=DAYS+%s WHERE CNAME=%s AND ROOMNO=%s'
q21='SELECT DAYS,CHECKIN FROM BOOKING WHERE CNAME=%s AND ROOMNO=%s'
q22='UPDATE BOOKING SET CHECKOUT=%s,DAYS=DAYS-%s WHERE CNAME=%s AND ROOMNO=%s'
q23='SELECT ROOMNO FROM BOOKING WHERE CNAME=%s'
q25='UPDATE CUSTOMER SET AMOUNT=AMOUNT+%s WHERE CNAME=%s'
q26='SELECT RCODE FROM BOOKING WHERE ROOMNO=%s'
q27='SELECT PRICE FROM INFO WHERE RCODE=%s'
q28='UPDATE CUSTOMER SET AMOUNT=AMOUNT+%s WHERE CNAME=%s'
q29='SELECT AMOUNT,PAYSTATUS FROM CUSTOMER WHERE CNAME=%s'
q30='SELECT AMOUNT,PAYSTATUS FROM CUSTOMER WHERE CNAME=%s'
q31='UPDATE CUSTOMER SET PAYSTATUS=PAYSTATUS+%s WHERE CNAME=%s'
q32='SELECT CCODE,DAYS FROM BOOKING WHERE CNAME=%s AND ROOMNO=%s'
q33='SELECT PRICEPERDAY FROM MEALS WHERE MCODE=(SELECT MEAL FROM BOOKING WHERE CNAME=%s AND ROOMNO=%s)'
q34="DELETE FROM BOOKING WHERE CNAME=%s and ROOMNO=%s"
def input1():
    cost=0
    a=input("Enter your name:")
    n=int(input("Enter number of rooms:"))
    print()
    for i in range(1,n+1):
        s1=[]
        print("ROOM",i)
        rc=int(input("Enter your required room code:"))
        d1=input("Enter your check-in date (yyyy-mm-dd):")
        k=int(input("Enter the number of days of your stay:"))
        m=int(input("Enter your required meal code:"))
        print()
        c1.execute(q8,(d1,k))
        t=c1.fetchone()
        d2=t[0]
        c1.execute(q12,(rc,))
        t=c1.fetchall()
        check=0
        for i in t:
            r=i[0]
            c1.execute(q13,(r,))
            s=c1.fetchall()
            s1+=s
            d3=datetime.strptime(d1,"%Y-%m-%d").date()
            d4=datetime.strptime(d2,"%Y-%m-%d").date()
            if s is None:
                print("YOUR ROOM NUMBER:",r)
                print()
                check=1
                break
            else:
                for j in s:
                    di=j[0]
                    do=j[1]
                    if d3>=di and do>=d3:
                        break
                    elif d4>=di and do>=d4:
                        break
                else:
                    print("YOUR ROOM NUMBER:",r)
                    print()
                    check=1
                    break
        else:
            print("The room you have requested for is not available on the given day. Please try choosing an other room or another date.")
            print("The room is not available on the following days:")
            for i in s1:
                print(i[0],"to",i[1])
            print()
        if check==1:
            c1.execute(q2,(a,))
            c2=obj.cursor()
            c2.execute(q14,(m,))
            obj.commit()
            mp=c2.fetchone()
            c2.execute(q3,(rc,))
            obj.commit()
            p=c2.fetchone()
            rt=p[1]
            cost+=k*(p[0])
            cost+=k*(mp[0])
            c2.execute(q9)
            obj.commit()
            t=c2.fetchone()
            ccode=t[0]
            c2.execute(q11,(r,rc,rt,ccode,a,m,d1,d2,k))
            obj.commit()
    print()
    if cost!=0:
        print("Total cost of your stay:",cost)
        ps=int(input("Amount you have paid:"))
        print("Amount left to be paid:",cost-ps)
        t=(cost,ps,ccode)
        c1.execute(q7,t)
        obj.commit()
        print()
def fdback():
    fr=open("feedback.csv","r",newline="")
    r=csv.reader(fr,delimiter=",")
    fw=open("feedback1.csv","w",newline="")
    w=csv.writer(fw,delimiter=",")
    for i in r:
        w.writerow(i)
    name=input("Enter your name:")
    c2.execute(q23,(name,))
    t=c2.fetchall()
    roomno=eval(input("Enter your room number for your stay:"))
    c2.execute(q32,(name,roomno))
    fbdet=c2.fetchone()
    if fbdet is not None:   
        exp=eval(input("On a scale of 1 to 10, how was your overall experience at our hotel?: "))
        fbtext=input("What can we do to improve customer's experience?: ")
        row=[fbdet[0],name,fbdet[1],exp,fbtext]
        print("Thank you for your review and feeback, we will work hard on it for your better future experience at our hotel. :)")
        w.writerow(row)
        fw.close()
        fr.close()
        os.remove("feedback.csv")
        os.rename("feedback1.csv","feedback.csv")
    else:
        print("There is no such room number under your name ",name,". Please try again.",sep="")
while True:
    print()
    print("1-About us")
    print("2-To make a new entry")
    print("3-To modify the days of your stay")
    print("4-Update payment")
    print("5-Feedback")
    print("6-Cancel booking")
    print("7.To exit")
    print()
    c=int(input("Enter choice:"))
    if c==1:
        print()
        f=open("aboutus.txt","r")
        for i in f:
            print(i)
        print()
    elif c==2:
        print()
        c1.execute(q1)
        d={}
        for i in range(4):
            x=c1.fetchone()
            d[x[0]]=[x[1],x[2],x[3],x[4]]
        print("{:<9} {:22} {:<86} {:<10} {:<10}".format('RCODE','RTYPE','DESCRIPTION','PRICE','AVAILABILITY'))
        for k,v in d.items():
              rtype,description,price,availability=v
              print("{:<9} {:22} {:<86} {:<10} {:<10}".format(k,rtype,description,price,availability))
        print()
        c1.execute(q15)
        d1={}
        for i in range(3):
            x=c1.fetchone()
            d1[x[0]]=[x[1],x[2]]
        print("{:<9} {:<18} {:<10}".format('MCODE','MEAL','PRICE PER DAY'))
        for k,v in d1.items():
            meal,priceperday=v
            print("{:<9} {:<18} {:<10}".format(k,meal,priceperday))
        print()
        input1()
    elif c==3:
        a=input("Enter your name:")
        c2.execute(q4)
        all_names=c2.fetchall()
        for checking_name in all_names:
            if checking_name[0]==a:
                break
        else:
            print("Entered customer name not found.")
            print()
            continue        
        updateroomno=eval(input("Enter your room number to be updated for the stay:"))
        c2.execute(q23,(a,))
        room_nos=c2.fetchall()
        for room_of_name in room_nos:
            if room_of_name[0]==updateroomno:
                break
        else:
            print("Entered room number not found.")
            print()
            continue
        c2.execute(q33,(a,updateroomno))
        meal_perday=c2.fetchone()[0]
        c2.execute(q5,(updateroomno,))
        room_code=c2.fetchone()[0]
        c2.execute(q6,(room_code,))
        price_update=c2.fetchone()[0]
        print("1.To increase the number of days of your stay")
        print("2.To reduce the number of days of stay")
        choiceforupdate=eval(input("Enter your choice:"))
        if choiceforupdate==1:
            updatedays=eval(input("Enter days to be increased in your stay:"))
            c2.execute(q17,(a,updateroomno))
            t=c2.fetchone()
            updcheckout=t[0]
            c2.execute(q18,(updateroomno,a,updcheckout))
            t=c2.fetchone()
            if t is None:
                c2.execute(q19,(updcheckout,updatedays))
                t=c2.fetchone()
                updatedcheckout=t[0]
                c2.execute(q16,(updatedcheckout,updatedays,a,updateroomno))
                print("Your stay has been extended. Thank you for staying with us. :)")
                price_to_be_added=updatedays*(price_update+meal_perday)
                c2.execute(q28,(price_to_be_added,a))
                print()
            earliestothercheckin=t[0]
            c2.execute(q19,(updcheckout,updatedays))
            t=c2.fetchone()
            updatedcheckout=t[0]
            if updatedcheckout<str(earliestothercheckin):
                c2.execute(q20,(updatedcheckout,updatedays,a,updateroomno))
                print("Your stay has been extended. Thank you for staying with us. :)")
                print()
            if str(updatedcheckout)>str(earliestothercheckin):
                c2.execute(q10,(earliestothercheckin,updcheckout))
                t=c2.fetchone()
                alternate_extendlength=t[0]
                if alternate_extendlength>1: 
                    c2.execute(q8,(updcheckout,alternate_extendlength))
                    t=c2.fetchone()
                    alternate_checkout=t[0]
                    print("Sorry due to already booked customers, your current can only extended for",alternate_extendlength,"days, upto",alternate_checkout,".",sep="")
                    print("1.To proceed with the given date")
                    print("2.To cancel extending stay")
                    idek=eval(input("Enter your choice:"))
                    if idek==1:
                        c2.execute(q20,(alternate_checkout,alternate_extendlength,a,updateroomno))
                        print("Your stay has been increased to",alternate_checkout,".",sep="")
                        price_to_be_added=price_update*alternate_extendlength
                        c2.execute(q25,(price_to_be_added,a))
                    elif idek==2:
                        print("Sorry we couldn't extend your stay with us.")
                    elif idek not in (1,2):
                        print("Invalid choice")
                        break
                elif alternate_extendlength<=1:
                    print("Sorry we couldn't extend your stay with us.")
                print()
        elif choiceforupdate==2:
            update_descreased_days=eval(input("Enter days to be decreased in your stay:"))
            c2.execute(q26,(updateroomno,))
            room_code=c2.fetchone()[0]
            c2.execute(q27,(room_code,))
            price_update=c2.fetchone()[0]
            c2.execute(q21,(a,updateroomno))
            t=c2.fetchone()
            first_days=t[0]
            checkindate=t[1]
            reduced_days=first_days-update_descreased_days
            c2.execute(q8,(checkindate,reduced_days))
            t=c2.fetchone()
            final_checkout=t[0]
            c2.execute(q22,(final_checkout,update_descreased_days,a,updateroomno))
            price_to_be_reduced=-(update_descreased_days*(price_update+meal_perday))
            c2.execute(q28,(price_to_be_reduced,a))
            print("We are sorry that you will be leaving us earlier than expected :(")
            print()
        else:
            print("Invalid choice")
            print()
    elif c==4:
        cname=input("Enter your name:")
        c1.execute(q30,(cname,))
        t=c1.fetchone()
        if t is None:
            print("Entered customer name not found.")
        else:
            amt,ps=t[0],t[1]
            print("The total amount of your stay:",amt)
            print("Amount left to be paid:",amt-ps)
            m=eval(input("Enter amount to pay:"))
            c1.execute(q31,(m,cname))
            print("Transaction has been completed.")
            c1.execute(q29,(cname,))
            t=c1.fetchone()
            amt,ps=t[0],t[1]
            print("Amount left to be paid:",amt-ps)
            if amt-ps==0:
                print("Payment settled.")
            print()
    elif c==5:
        print("1. To enter your(customer's) feedback")
        print("2. To view all existing feedback(Admin)")
        feedback_choices=eval(input("Enter your choice:"))
        if feedback_choices==1:
            fdback()
            print()
        if feedback_choices==2:
            password=input("enter password:")
            if password=="ss1234":
                print()
                fr=open("feedback.csv","r",newline="")
                r=csv.reader(fr,delimiter=",")
                d={}
                for i in r:
                    d[i[0]]=[i[1],i[2],i[3],i[4]]
                for k,v in d.items():
                      Customer_Name,Number_of_days_of_stay,Experience,Feedback=v
                      print("{:<20} {:<20} {:<27} {:<20} {:<43}".format(k,Customer_Name,Number_of_days_of_stay,Experience,Feedback))
                print()
                d1={}
                fr.close()
            else:
                print("wrong password-access denied")
        elif feedback_choices not in (1,2):
            print("Invalid choice entered.")
            print()
    elif c==6:
        a=input("Enter your name:")
        c2.execute(q4)
        all_names=c2.fetchall()
        for checking_name in all_names:
            if checking_name[0]==a:
                break
        else:
            print("Entered customer name not found.")
            print()
            continue        
        updateroomno=eval(input("Enter your room number to be updated for the stay:"))
        c2.execute(q23,(a,))
        room_nos=c2.fetchall()
        for room_of_name in room_nos:
            if room_of_name[0]==updateroomno:
                break
        else:
            print("Entered room number not found.")
            print()
            continue
        c2.execute(q34,(a,updateroomno))
        obj.commit()
        print("Your booking has been cancelled.")
    elif c==7:
        print("Thank you for joining us. We hope to see you here again :)")
        print("_o0o_")
        break
    elif c not in (1,2,3,4,5,6):
        print("Invalid choice entered.")
        print()