import models
import yfinance
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from fastapi import FastAPI, Request, Depends, BackgroundTasks
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from models import Stocks

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="templates")


class StockRequest(BaseModel):
	symbol: str


def get_db():
	try:
		db = SessionLocal()
		yield db
	finally:
		db.close()


#Displays stock dashboard
@app.get("/")
def stock_dashboard(request: Request, forward_pe = None, dividend_yield = None, ma50 = None, ma200 = None, db: Session = Depends(get_db)):
    stocks = db.query(Stocks)

    if forward_pe:
    		stocks = stocks.filter(Stocks.forward_pe < forward_pe)

    if dividend_yield:
    		stocks = stocks.filter(Stocks.dividend_yield < dividend_yield)

    if ma50: 
    		stocks = stocks.filter(Stocks.price > Stock.ma50)
    
    if ma200:
    		stocks = stocks.filter(Stocks.price > Stock.ma200)
    		
	

    
   	#going back to the tempalte
    return templates.TemplateResponse("dashboard.html",{
    	"request" : request,
    	"stocks" : stocks,
    	"dividend_yield" : dividend_yield,
    	"forward_pe" : forward_pe,
    	"ma50" : ma50,
    	"ma200" : ma200
    })


#logic references yhoo finance
def fetch_stock_data(id: int):
	db = SessionLocal()
	stock = db.query(Stocks).filter(Stocks.id == id).first()

	yahoo_data = yfinance.Ticker(stock.symbol)
	yahoo_data = yfinance.Ticker(stock.name)
	stock.ma200 = yahoo_data.info['twoHundredDayAverage']
	stock.ma50 = yahoo_data.info['fiftyDayAverage']
	stock.price = yahoo_data.info['previousClose']
	stock.forward_pe = yahoo_data.info['forwardPE']
	stock.forward_eps = yahoo_data.info['forwardEps']
	
	if yahoo_data.info['dividendYield'] is not None:
		stock.dividend_yield = yahoo_data.info['dividendYield'] * 100

	db.add(stock)
	db.commit()


#Creates a stock and stores in database
@app.post("/stock")
async def create_stock(stock_request: StockRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
	stock = Stocks()
	stock.symbol = stock_request.symbol

	db.add(stock)
	db.commit()

	background_tasks.add_task(fetch_stock_data, stock.id)




	return {
		"code": "success",
		"message" : "stock created"
	}

