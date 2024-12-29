import pandas as pd

df = pd.read_csv("hotel.csv")
df_cards = pd.read_csv("cards.csv", dtype=str).to_dict(orient="records")
df_security_cards = pd.read_csv("card-security.csv", dtype=str)


class Hotel:
    def __init__(self, hotel_id):
        self.hotel_id = hotel_id
        self.name = df.loc[df["id"] == self.hotel_id, "name"].squeeze()

    def available(self):
        """Check if the hotel is available"""
        availability = df.loc[df["id"] == self.hotel_id, "available"].squeeze()
        if availability == "yes":
            return True
        else:
            return False

    def book(self):
        """Book the hotel by changing is availability to no"""
        df.loc[df["id"] == self.hotel_id, "available"] = "no"
        df.to_csv("hotel.csv", index=False)


class ReservationTicket:
    def __init__(self, customer_name, hotel_object):
        self.customer_name = customer_name
        self.hotel_name = hotel_object

    def generate(self):
        content = f"""
        Thank you for your Reservation!
        Here are your booking data:
        Your Name = {self.customer_name}
        Hotel Name = {self.hotel_name.name}
        """
        return content


"""
    def spa_generate(self):
        spa_content = f""
        Thank you for your SPA Reservation!
        Here are your SPA booking data:
        Your Name = {self.customer_name}
        Hotel Name = {self.hotel_name.name}
        ""
        return spa_content
"""


class SpaHotel(Hotel):
    def book_spa_package(self):
        pass


class SpaTicket:
    def __init__(self, customer_name, hotel_object):
        self.customer_name = customer_name
        self.hotel = hotel_object

    def generate(self):
        content = f"""
        Thank you for your SPA reservation!
        Here are you SPA booking data:
        Name: {self.customer_name}
        Hotel name: {self.hotel.name}
        """
        return content


class CreditCard:
    def __init__(self, number):
        self.number = number

    def validate(self, expiration, cvc, holder):
        card_data = {"number": self.number, "expiration": expiration, "cvc": cvc, "holder": holder}
        if card_data in df_cards:
            return True
        else:
            return False


class SecurityCreditCard(CreditCard):

    def authenticate(self, given_password):
        paswrd = df_security_cards.loc[df_security_cards["number"] == self.number, "password"].squeeze()
        if paswrd == given_password:
            return True
        else:
            return False


print(df)
Id = int(input("Enter the id of Hotel: "))
hotel = SpaHotel(Id)

if hotel.available():
    credit_number = input("Enter Credit card number(1234): ")
    credit_card = SecurityCreditCard(number=credit_number)

    if credit_card.validate(expiration="12/26", cvc="123", holder="JOHN SMITH"):
        password = input("Enter the password(mypass)")

        if credit_card.authenticate(given_password=password):
            hotel.book()
            name = input("Enter your name: ")
            reservation_ticket = ReservationTicket(customer_name=name, hotel_object=hotel)
            print(reservation_ticket.generate())
            spa_que = input("Do you want to book a spa package?(yes/no)\n").lower()

            if spa_que == "yes":
                hotel.book_spa_package()
                spa_ticket = SpaTicket(customer_name=name, hotel_object=hotel)
                print(spa_ticket.generate())
            else:
                print(reservation_ticket.generate())
                
        else:
            print("Wrong Password!!")

    else:
        print("Credit card not vaild")

else:
    print("Hotel is not free")
