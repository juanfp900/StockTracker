from sqlalchemy import Column, String, Numeric, Integer


from database import Base


#table in database will be named stocks
class Stocks(Base):
    __tablename__ = "stocks"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, unique=True, index=True)
    price = Column(Numeric(10,2))
    forward_pe = Column(Numeric(10,2))
    forward_eps = Column(Numeric(10,2))
    dividend_yield = Column(Numeric(10,2))
    ma50 = Column(Numeric(10,2))
    ma200 = Column(Numeric(10,2))
    
    #email = Column(String, unique=True, index=True)
    #hashed_password = Column(String)
    #is_active = Column(Boolean, default=True)

