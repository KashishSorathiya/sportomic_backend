from datetime import date, datetime
from decimal import Decimal
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from models import Booking, Transaction, Member, Venue

CONFIRMED_STATUSES = {"confirmed", "completed"}
NEGATIVE_TX = {"refunded", "dispute"}

def _norm(s: str) -> str:
    return (s or "").replace(" ", "").lower()

def _date_bounds():
    return datetime.min, datetime.max

def general_metrics(db: Session, start_date: date | None, end_date: date | None, venue_id: int | None, sport_id: int | None):
    sdt, edt = start_date or _date_bounds()[0].date(), end_date or _date_bounds()[1].date()

    bq = select(Booking).where(func.date(Booking.booking_date).between(sdt, edt))
    if venue_id: bq = bq.where(Booking.venue_id == venue_id)
    if sport_id: bq = bq.where(Booking.sport_id == sport_id)
    bookings = db.execute(bq).scalars().all()

    total_bookings = len(bookings)
    confirmed_bookings = [b for b in bookings if _norm(b.status) in CONFIRMED_STATUSES]
    booking_ids = [b.id for b in bookings]

    txq = select(Transaction).where(Transaction.transaction_date.between(sdt, edt))
    if booking_ids: txq = txq.where(Transaction.booking_id.in_(booking_ids))
    txs = db.execute(txq).scalars().all()

    success_txs = [t for t in txs if _norm(t.status) == "success"]
    coaching_success = [t for t in success_txs if _norm(t.type) == "coaching"]
    booking_success = [t for t in success_txs if _norm(t.type) == "booking"]
    negative_txs = [t for t in txs if _norm(t.status) in NEGATIVE_TX]

    coupon_redemptions = sum(1 for b in confirmed_bookings if (b.coupon_code or "").strip())
    active_members = db.scalar(select(func.count()).select_from(Member).where(Member.status == "Active")) or 0
    inactive_members = db.scalar(select(func.count()).select_from(Member).where(Member.status == "Inactive")) or 0
    trials = db.scalar(select(func.count()).select_from(Member).where(Member.is_trial_user == True)) or 0
    converted = db.scalar(select(func.count()).select_from(Member).where(Member.converted_from_trial == True)) or 0
    trial_conversion_rate = float((converted / trials) * 100) if trials else 0.0

    mb_counts: dict[int, int] = {}
    for b in confirmed_bookings:
        mb_counts[b.member_id] = mb_counts.get(b.member_id, 0) + 1
    members_with_booking = sum(1 for c in mb_counts.values() if c >= 1)
    members_with_repeat = sum(1 for c in mb_counts.values() if c > 1)
    repeat_booking_pct = float((members_with_repeat / members_with_booking) * 100) if members_with_booking else 0.0

    booking_revenue = sum(Decimal(t.amount) for t in booking_success)
    coaching_revenue = sum(Decimal(t.amount) for t in coaching_success)
    total_revenue = sum(Decimal(t.amount) for t in success_txs)
    refunds_disputes = sum(Decimal(t.amount) for t in negative_txs)

    slots_utilization = float((len(confirmed_bookings) / total_bookings) * 100) if total_bookings else 0.0

    return {
        "active_members": active_members,
        "inactive_members": inactive_members,
        "bookings": len(confirmed_bookings),
        "booking_revenue": float(booking_revenue),
        "coaching_revenue": float(coaching_revenue),
        "total_revenue": float(total_revenue),
        "repeat_booking_pct": round(repeat_booking_pct, 2),
        "slots_utilization_pct": round(slots_utilization, 2),
        "coupon_redemption": coupon_redemptions,
        "trial_conversion_rate_pct": round(trial_conversion_rate, 2),
        "refunds_disputes_amount": float(refunds_disputes),
        "refunds_disputes_count": len(negative_txs),
    }

def revenue_timeseries(db: Session, start_date: date | None, end_date: date | None, venue_id: int | None, sport_id: int | None):
    sdt, edt = start_date or date.min, end_date or date.max
    stmt = (
        select(
            func.date(Transaction.transaction_date).label("dt"),
            func.sum(Transaction.amount).label("revenue")
        )
        .join(Booking, Booking.id == Transaction.booking_id)
        .where(Transaction.status == "Success")
        .where(Transaction.transaction_date.between(sdt, edt))
        .group_by(func.date(Transaction.transaction_date))
        .order_by(func.date(Transaction.transaction_date))
    )
    if venue_id: stmt = stmt.where(Booking.venue_id == venue_id)
    if sport_id: stmt = stmt.where(Booking.sport_id == sport_id)
    rows = db.execute(stmt).all()
    return [{"date": str(r.dt), "revenue": float(r.revenue or 0)} for r in rows]

def list_venues(db: Session):
    rows = db.execute(select(Venue)).scalars().all()
    return [{"id": v.id, "name": v.name, "location": v.location} for v in rows]

def list_sports(db: Session):
    rows = db.execute(select(func.distinct(Booking.sport_id))).all()
    return sorted([r[0] for r in rows if r[0] is not None])
