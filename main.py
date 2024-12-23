import pandas as pd
df = pd.read_csv("hotel.csv")


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
        Your Name = {self.customer_name}
        Hotel Name = {self.hotel_name.name}
        """
        return content


print(df)
Id = int(input("Enter the id of Hotel: "))
hotel = Hotel(Id)

if hotel.available():
    hotel.book()
    name = input("Enter your name: ")
    reservation_ticket = ReservationTicket(customer_name=name, hotel_object=hotel)
    print(reservation_ticket.generate())
else:
    print("Hotel is not free")