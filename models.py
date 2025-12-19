from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Date, DateTime, Numeric, ForeignKey

class Base(DeclarativeBase):
    pass

class Venue(Base):
    __tablename__ = "venues"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    location: Mapped[str] = mapped_column(String(200), nullable=False)
    bookings: Mapped[list["Booking"]] = relationship(back_populates="venue")

class Member(Base):
    __tablename__ = "members"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False)
    is_trial_user: Mapped[bool] = mapped_column()
    converted_from_trial: Mapped[bool] = mapped_column()
    join_date: Mapped[Date] = mapped_column(Date)

class Booking(Base):
    __tablename__ = "bookings"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    venue_id: Mapped[int] = mapped_column(ForeignKey("venues.id"), index=True)
    sport_id: Mapped[int] = mapped_column(Integer, index=True)
    member_id: Mapped[int] = mapped_column(ForeignKey("members.id"), index=True)
    booking_date: Mapped[DateTime] = mapped_column(DateTime, index=True)
    amount: Mapped[Numeric] = mapped_column(Numeric(12, 2))
    coupon_code: Mapped[str | None] = mapped_column(String(50), nullable=True)
    status: Mapped[str] = mapped_column(String(50), index=True)
    venue: Mapped["Venue"] = relationship(back_populates="bookings")
    transactions: Mapped[list["Transaction"]] = relationship(back_populates="booking")

class Transaction(Base):
    __tablename__ = "transactions"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    booking_id: Mapped[int] = mapped_column(ForeignKey("bookings.id"), index=True)
    type: Mapped[str] = mapped_column(String(50), index=True)
    amount: Mapped[Numeric] = mapped_column(Numeric(12, 2))
    status: Mapped[str] = mapped_column(String(50), index=True)
    transaction_date: Mapped[Date] = mapped_column(Date, index=True)
    booking: Mapped["Booking"] = relationship(back_populates="transactions")
