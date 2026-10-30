import json
import random
import string
from pathlib import Path

class Bank():
    database='datafile.json'
    data=[]
    try:
        if Path(database).exists():
            with open(database) as fs:
                data=json.loads(fs.read())
        else:
            print("File doesn't exist")

    except Exception as err:
        print("{err} occured")

    @staticmethod
    def __update():
        with open(Bank.database,'w') as fl:
            fl.write(json.dumps(Bank.data))

    @classmethod
    def __accountgenerate(cls):
        alpha=random.choices(string.ascii_letters,k=3)
        num=random.choices(string.digits,k=3)
        spchar=random.choices("!@#$%^&*",k=1)
        id=alpha+num+spchar
        random.shuffle(id)
        return "".join(id)



    def CreateAccount(self):
        info ={
            "name":input("Kindly enter your Name:- "),
            "age": int(input("Kindly tell me your age:- ")),
            "email":input("Kindly mention your E-mail id:- "),
            "pin":int(input("Please make your pin:- ")),
            "accountno":Bank.__accountgenerate(),
            "balance": 0
        }
        if info['age']<18 or len(str(info['pin']))!=4:
            print("You are not eligible to open the account")
        else:
            print("Your account is succefully opened")
            for i in info:
                print(f"{i}:{info[i]}")
            print("Please note downn your Account Number")

            Bank.data.append(info)

            Bank.__update()

    def DepositMoney(self):
        acc=input("Please tell your account number")
        pin=int(input("Please tell your pin number"))

        userdata=[i for i in Bank.data if i['accountno']==acc and i['pin']== pin]

        if userdata==False:
            print("Sorry no data found")
        else:
            amount=int(input("Please enter your ammount"))
            if amount>10000 or amount<0:
                print("Sorry Amount should be below 10,000 and above 0")
            else:
                # print(userdata)
                userdata[0]['balance']+=amount # Using 0 because dictionary is stored inside list of userdata
                Bank.__update()
                print("The amount is deposited")


    def WithdrawMoney(self):
        acc=input("Please tell your account number")
        pin=int(input("Please tell your pin number"))
        
    
        userdata=[i for i in Bank.data if i['accountno']==acc and i['pin']== pin]
    
        if userdata==False:
            print("Sorry no data found")
        else:
            amount=int(input("Please enter your ammount you want to withdraw"))
            if userdata[0]['balance']<amount:
                print("Sorry You have insufficient balance")
            else:
                # print(userdata)
                userdata[0]['balance']-=amount # Using 0 because dictionary is stored inside list of userdata
                Bank.__update()
                print(f"The amount is withdrawn is {amount}")

    def ShowDetails(self):
        acc=input("Please tell your account number")
        pin=int(input("Please tell your pin number"))

        userdata=[i for i in Bank.data if i['accountno']==acc and i['pin']== pin]

        if userdata==False:
            print("Sorry no data found")
        else:
            print("YOur information are:")

            for i in userdata[0]:
                print(f"{i}:{userdata[0][i]}")
        
    def UpdateDetails(self):
        acc=input("Please tell your account number")
        pin=int(input("Please tell your pin number"))
        
        userdata=[i for i in Bank.data if i['accountno']==acc and i['pin']== pin]
        
        if userdata==False:
            print("Sorry no data found")
        else:
            print("You cannot change age, account number, balance")
            print("Fill details to fill the data or else keep it blank")
            newdata={
                "name": input("Please enter your Name or press enter to skip: "),
                "email":input("Please enter new email or press enter to skip: "),
                "pin":input("Please enter new pin or else press enter to skip: ")
            }

            if newdata["name"]=="":
                newdata["name"]=userdata[0]["name"]

            if newdata["email"]=="":
                newdata["name"]=userdata[0]["email"]

            if newdata["pin"]=="":
                newdata["name"]=userdata[0]["pin"]   

            newdata['age']=userdata[0]['age']
            newdata['accountno']=userdata[0]['accountno']
            newdata['balance']=userdata[0]['balance']

            if type(newdata['pin'])==str:
                newdata['pin']=int(newdata['pin'])

            for i in newdata:
                if newdata[i]==userdata[0][i]:
                    continue
                else:
                    userdata[0][i]=newdata[i]
            Bank.__update()

            print("Details updatd successfully")


    def DeleteUser(self):
            acc=input("Please tell your account number")
            pin=int(input("Please tell your pin number"))
            
            userdata=[i for i in Bank.data if i['accountno']==acc and i['pin']== pin]
            
            if userdata==False:
                print("Sorry no data found")
            else:
                check=input("Press Y if you actually want to delete your account or press N  to not delete it:-:- ")
                if check=='y' or check=='Y':
                    index = Bank.data.index(userdata[0])
                    Bank.data.pop(index)
                    Bank.__update()
                    print("Record deleted succefully")

                
                elif check=='n' or check=='N':
                    print("Bypass")

                else:
                    print("Kinldy press Y or N ")


user=Bank()
print("Press 1 for creating a account")
print("Press 2 for Depositiong money in the bank")
print("Press 3 To withdraw the money")
print("Press 4 to know your details")
print("Press 5 for updating details")
print("Press 6 for deletng your account")

check=int(input ("Tell us your response"))

if check==1:
    user.CreateAccount()

if check==2:
    user.DepositMoney()

if check==3:
    user.WithdrawMoney()

if check==4:
    user.ShowDetails()

if check==5:
    user.UpdateDetails()

if check==6:
    user.DeleteUser()