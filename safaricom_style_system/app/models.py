# Simple SQLAlchemy models using SQLite for a demo system.
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, JSON, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import datetime, os, json

BASE_DIR = os.path.dirname(__file__)
DB_URL = f"sqlite:///{os.path.join(BASE_DIR, '..', 'data.db')}"
engine = create_engine(DB_URL, connect_args={'check_same_thread': False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class Customer(Base):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    msisdn = Column(String, unique=True, nullable=False)
    email = Column(String, nullable=True)
    balance = Column(Float, default=0.0)

class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey('customers.id'), nullable=True)
    amount = Column(Float, default=0.0)
    method = Column(String, default='mpesa')
    provider_ref = Column(String, nullable=True)
    status = Column(String, default='pending')
    metadata = Column(JSON, default={})
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    fraud_flagged = Column(Boolean, default=False)
    fraud_score = Column(Float, default=0.0)
    fraud_reason = Column(String, nullable=True)

def init_db():
    Base.metadata.create_all(bind=engine)
    # seed a demo customer if none
    db = SessionLocal()
    if db.query(Customer).count() == 0:
        c = Customer(name='Demo Customer', msisdn='+254700000000', email='demo@example.com', balance=2350.0)
        db.add(c)
        db.commit()
    db.close()

def get_balance_by_msisdn(msisdn):
    db = SessionLocal()
    c = db.query(Customer).filter(Customer.msisdn == msisdn).first()
    bal = c.balance if c else 0.0
    db.close()
    return bal

def create_transaction(payload, fraud_resp):
    db = SessionLocal()
    customer = None
    msisdn = payload.get('msisdn') or payload.get('phone') or payload.get('phone_number')
    if msisdn:
        customer = db.query(Customer).filter(Customer.msisdn == msisdn).first()
    tx = Transaction(
        customer_id = customer.id if customer else None,
        amount = float(payload.get('amount', 0)),
        method = payload.get('method', 'mpesa'),
        provider_ref = payload.get('provider_ref'),
        status = 'blocked' if fraud_resp.get('decision') == 'BLOCK' else 'approved',
        metadata = payload,
        fraud_flagged = True if fraud_resp.get('decision') in ['BLOCK', 'REVIEW'] else False,
        fraud_score = float(fraud_resp.get('fraud_score', 0.0)),
        fraud_reason = fraud_resp.get('reason'),
    )
    db.add(tx)
    db.commit()
    txid = tx.id
    db.close()
    return {"id": txid, "status": tx.status, "fraud_score": tx.fraud_score, "fraud_reason": tx.fraud_reason}

def count_customers():
    db = SessionLocal()
    n = db.query(Customer).count()
    db.close()
    return n

def count_transactions():
    db = SessionLocal()
    n = db.query(Transaction).count()
    db.close()
    return n

def count_flagged():
    db = SessionLocal()
    n = db.query(Transaction).filter(Transaction.fraud_flagged == True).count()
    db.close()
    return n
