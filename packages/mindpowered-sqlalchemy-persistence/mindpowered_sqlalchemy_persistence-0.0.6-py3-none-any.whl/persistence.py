import maglev

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Numeric, DateTime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import time

Base = declarative_base()

class Auction(Base):
	__tablename__ = 'auctions'
	id = Column(Integer, primary_key=True, autoincrement=True)
	item_id = Column(String)
	user_id = Column(String)
	start = Column(DateTime)
	end = Column(DateTime)
	starting_price = Column(Numeric)
	reserve_price = Column(Numeric)
	price_increment = Column(Numeric)

class Bid(Base):
	__tablename__ = 'bids'
	id = Column(Integer, primary_key=True, autoincrement=True)
	auction_id = Column(Integer)
	user_id = Column(String)
	price = Column(Numeric)

class persistence_Persistence:
	def __init__(self, bus):
		self.pybus = maglev.maglev_MagLevPy(bus)
		self.pybus.register('Persistence.Setup', self.Persistence_Setup)
		self.pybus.register('Persistence.EnglishAuction.Create', self.Persistence_EnglishAuction_Create)
		self.pybus.register('Persistence.EnglishAuction.Auction.CreateNew', self.Persistence_EnglishAuction_Auction_CreateNew)
		self.pybus.register('Persistence.EnglishAuction.Auction.FindById', self.Persistence_EnglishAuction_Auction_FindById)
		self.pybus.register('Persistence.EnglishAuction.Auction.FindStarting', self.Persistence_EnglishAuction_Auction_FindStarting)
		self.pybus.register('Persistence.EnglishAuction.Auction.FindEnding', self.Persistence_EnglishAuction_Auction_FindEnding)
		self.pybus.register('Persistence.EnglishAuction.Auction.FindOpen', self.Persistence_EnglishAuction_Auction_FindOpen)
		self.pybus.register('Persistence.EnglishAuction.Bid.CountForAuction', self.Persistence_EnglishAuction_Bid_CountForAuction)
		self.pybus.register('Persistence.EnglishAuction.Bid.FindByHighestPriceForAuction', self.Persistence_EnglishAuction_Bid_FindByHighestPriceForAuction)
		self.pybus.register('Persistence.EnglishAuction.Bid.New', self.Persistence_EnglishAuction_Bid_New)
	def Persistence_Setup(self, args):
		connect_str = args[0]
		connect_params = args[1]
		self.engine = create_engine(connect_str, **connect_params)
		self.Session = sessionmaker(bind=self.engine)
	def Persistence_EnglishAuction_Create(self, args):
		Auction.__table__.create(self.engine)
		Bid.__table__.create(self.engine)
	def Persistence_EnglishAuction_Auction_CreateNew(self, args):
		o = args[0]
		item_id = ''#o['item_id']
		user_id = ''#o['user_id']
		start = datetime.fromtimestamp(o['start'])
		end = datetime.fromtimestamp(o['end'])
		starting_price = o['startingPrice']
		reserve_price = o['reservePrice']
		price_increment = o['priceIncrement']
		session = self.Session()
		new_auction = Auction(item_id=item_id, user_id=user_id, start=start, end=end, starting_price=starting_price, reserve_price=reserve_price, price_increment=price_increment)
		session.add(new_auction)
		session.commit()
		return str(new_auction.id)
	def Persistence_EnglishAuction_Auction_FindById(self, args):
		id = args[0]
		session = self.Session()
		for instance in session.query(Auction).filter(Auction.id == id):
			row = {}
			row['id'] = instance.id
			row['item_id'] = instance.item_id
			row['user_id'] = instance.user_id
			row['start'] = time.mktime(instance.start.timetuple())
			row['end'] = time.mktime(instance.end.timetuple())
			row['starting_price'] = float(instance.starting_price)
			row['reserve_price'] = float(instance.reserve_price)
			row['price_increment'] = float(instance.price_increment)
			return row
		return None
	def Persistence_EnglishAuction_Auction_FindStarting(self, args):
		self.noimpl('Persistence.EnglishAuction.Auction.FindStarting')
	def Persistence_EnglishAuction_Auction_FindEnding(self, args):
		self.noimpl('Persistence.EnglishAuction.Auction.FindEnding')
	def Persistence_EnglishAuction_Auction_FindOpen(self, args):
		self.noimpl('Persistence.EnglishAuction.Auction.FindOpen')
	def Persistence_EnglishAuction_Bid_CountForAuction(self, args):
		self.noimpl('Persistence.EnglishAuction.Bid.CountForAuction')
	def Persistence_EnglishAuction_Bid_FindByHighestPriceForAuction(self, args):
		self.noimpl('Persistence.EnglishAuction.Bid.FindByHighestPriceForAuction')
	def Persistence_EnglishAuction_Bid_New(self, args):
		self.noimpl('Persistence.EnglishAuction.Bid.New')
	def noimpl(self, method):
		data = ["_not_implemented_", "sql-persistence", "python", method]
		def donothing():
			pass
		self.pybus.call("MindPowered.Telemetry.Send", data, donothing);
		msg = "You are trying to use the '" + method + "' method but it's not quite done yet. Please email support@mindpowered.dev to find out when it will be done."
		raise Exception(msg)
