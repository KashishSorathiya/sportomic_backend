from datetime import datetime, date
from sqlalchemy import select
from db import engine, SessionLocal
from models import Base, Venue, Member, Booking, Transaction

def run():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        if db.scalar(select(Venue).limit(1)):
            return

        venues = [
            Venue(id=1, name="Grand Slam Arena", location="North Hills"),
            Venue(id=2, name="City Kickers Turf", location="Downtown"),
            Venue(id=3, name="AquaBlue Pool Center", location="Westside"),
            Venue(id=4, name="Smash Point Badminton", location="East District"),
            Venue(id=5, name="Legends Cricket Ground", location="Suburbs"),
        ]
        db.add_all(venues)

        members = [
            Member(id=1, name="Rahul Sharma", status="Active", is_trial_user=False, converted_from_trial=False, join_date=date(2025,10,15)),
            Member(id=2, name="Priya Singh", status="Active", is_trial_user=True, converted_from_trial=True, join_date=date(2025,11,1)),
            Member(id=3, name="Amit Patel", status="Inactive", is_trial_user=False, converted_from_trial=False, join_date=date(2025,9,10)),
            Member(id=4, name="Sneha Gupta", status="Active", is_trial_user=False, converted_from_trial=True, join_date=date(2025,11,20)),
            Member(id=5, name="Vikram Malhotra", status="Active", is_trial_user=True, converted_from_trial=False, join_date=date(2025,12,10)),
            Member(id=6, name="Anjali Desai", status="Inactive", is_trial_user=True, converted_from_trial=False, join_date=date(2025,11,5)),
            Member(id=7, name="John Doe", status="Active", is_trial_user=False, converted_from_trial=False, join_date=date(2025,8,15)),
            Member(id=8, name="Sarah Lee", status="Active", is_trial_user=True, converted_from_trial=True, join_date=date(2025,12,1)),
        ]
        db.add_all(members)

        bookings = [
            Booking(id=1, venue_id=1, sport_id=1, member_id=1, booking_date=datetime(2025,12,12,10,0), amount=500.00, coupon_code=None, status="Completed"),
            Booking(id=2, venue_id=2, sport_id=2, member_id=2, booking_date=datetime(2025,12,13,14,0), amount=1200.00, coupon_code=None, status="Confirmed"),
            Booking(id=3, venue_id=3, sport_id=3, member_id=7, booking_date=datetime(2025,12,13,7,0), amount=300.00, coupon_code="EARLYBIRD", status="Confirmed"),
            Booking(id=4, venue_id=4, sport_id=4, member_id=4, booking_date=datetime(2025,12,13,18,0), amount=400.00, coupon_code="WELCOME50", status="Confirmed"),
            Booking(id=5, venue_id=5, sport_id=5, member_id=5, booking_date=datetime(2025,12,14,9,0), amount=1500.00, coupon_code=None, status="Confirmed"),
            Booking(id=6, venue_id=1, sport_id=1, member_id=1, booking_date=datetime(2025,12,13,10,0), amount=500.00, coupon_code="SAVE10", status="Confirmed"),
            Booking(id=7, venue_id=2, sport_id=2, member_id=8, booking_date=datetime(2025,12,15,16,0), amount=600.00, coupon_code=None, status="Confirmed"),
            Booking(id=8, venue_id=3, sport_id=3, member_id=3, booking_date=datetime(2025,12,10,15,0), amount=300.00, coupon_code=None, status="Cancelled"),
        ]
        db.add_all(bookings)

        txs = [
            Transaction(id=101, booking_id=1, type="Booking", amount=500.00, status="Success", transaction_date=date(2025,12,12)),
            Transaction(id=102, booking_id=2, type="Coaching", amount=1200.00, status="Success", transaction_date=date(2025,12,13)),
            Transaction(id=103, booking_id=3, type="Booking", amount=270.00, status="Success", transaction_date=date(2025,12,13)),
            Transaction(id=104, booking_id=4, type="Booking", amount=200.00, status="Success", transaction_date=date(2025,12,13)),
            Transaction(id=105, booking_id=5, type="Booking", amount=1500.00, status="Success", transaction_date=date(2025,12,14)),
            Transaction(id=106, booking_id=6, type="Booking", amount=450.00, status="Success", transaction_date=date(2025,12,13)),
            Transaction(id=107, booking_id=7, type="Coaching", amount=600.00, status="Dispute", transaction_date=date(2025,12,15)),
            Transaction(id=108, booking_id=8, type="Booking", amount=300.00, status="Refunded", transaction_date=date(2025,12,10)),
        ]
        db.add_all(txs)

        db.commit()
    finally:
        db.close()

if __name__ == "__main__":
    run()
