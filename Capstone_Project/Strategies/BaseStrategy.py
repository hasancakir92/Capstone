from pickle import NONE
from types import NoneType
import backtrader as bt
import backtrader.indicators as btind

class BaseStrategy(bt.Strategy):
    """
        Generic abstract base class that can be interface for different strategies.
        It includes methods:
        - To notify about order situation
        - To printout any log
        - To notify about trade situation when a trade is closed or open.
        - To apply generic stop loss technique for any strategy
        - To apply generic time based stop loss strategy
        - To apply position sizing based on volatility

        Paramaters:
        ---------------
        printout:boolean
            to set if logs will be printed out
        apply_stop_loss:boolean
            to set if stop loss will be applied
        stop_loss_type:str
            to set what kind of stop loss will be applied. 
            It will be static percentage stop loss or volatility adjusted stop loss.
        stop_loss_percentage:float
            to set static stop loss percentage.
  

    """
    params = (
        ('printout',False),
        ('apply_stop_loss',False),
        ('stop_loss_type','static_percentage'),
        ('stop_loss_percentage',0.01)
    )
    def __init__(self):
        #last_buy_price keeps the latest price that is used for buy security
        self.last_buy_price=None
        #current_number_of_bar keeps how many price bars are passed since the security bought
        self.current_number_of_bar=0
        self.bollinger_band_dev_factor=2
        #position_size keeps number of security that will be bought
        self.position_size=None

        #In case volatility adjusted stop loss will be applied or position will be adjusted based on volatility,
        #Bollinger bands will be used to measure volatility
        if self.p.stop_loss_type=='volatility_adjusted':
            self.boll = bt.indicators.BollingerBands(period=20, devfactor= self.bollinger_band_dev_factor)

    def notify_order(self, order):
        """
            Notify about the order situation
            
            Paramaters:
            ----------------
            order:
                order(buy, sell, stop loss etc)
        """
        if order.status in [bt.Order.Submitted, bt.Order.Accepted]:
            return  # Await further notifications

        #if order is completed successfully
        if order.status == order.Completed:
            #Restart counting number of bar 
            self.current_number_of_bar=0

            #if order is a buy ordeer
            if order.isbuy():
                #set last_buy_price with execution price of buy order
                self.last_buy_price=order.executed.price
                buytxt = 'BUY COMPLETE, %.2f' % order.executed.price
                self.log(buytxt, order.executed.dt)
            #otherwise, it is a sell order
            else:
                selltxt = 'SELL COMPLETE, %.2f' % order.executed.price
                self.log(selltxt, order.executed.dt)

        elif order.status in [order.Expired, order.Canceled, order.Margin]:
            self.log('%s ,' % order.Status[order.status])
            pass 
        # Allow new orders
        self.orderid = None
     
    def log(self, txt, dt=None):
        """
            Create logs

            Paramaters:
            ---------------
            txt:str
                log text
            dt:datetime
                to print out datetime of log
        """
        if self.p.printout:
            dt = dt or self.data.datetime[0]
            dt = bt.num2date(dt)
            print('%s, %s' % (dt.isoformat(), txt))

    

    def notify_trade(self, trade):
        if trade.isclosed:
            self.log('TRADE PROFIT, GROSS %.2f, NET %.2f' %
                     (trade.pnl, trade.pnlcomm))

        elif trade.justopened:
            self.log('TRADE OPENED, SIZE %2d' % trade.size)

    def stop_loss(self):
        is_stop_loss_applied=False
        """
            Applies stop loss
        """
        #if stop loss is open
        if not self.p.apply_stop_loss:
            return is_stop_loss_applied

        #if there is existing position
        if self.position.size:
            #static percentage stop loss. if there is a certain amount of loss in existing order, it closes the existing order
            if self.p.stop_loss_type=='static_percentage' and  self.data.close<self.last_buy_price*(1-self.p.stop_loss_percentage):
                self.sell(size=self.position.size)
                self.log("Stop Loss Sale")
                is_stop_loss_applied=True
            #volatility adjusted stop loss
            if self.p.stop_loss_type=='volatility_adjusted':
                #sigma to calculate volatility
                sigma= (self.boll.lines.top-self.boll.lines.mid)/ self.bollinger_band_dev_factor

                #recalculate stop loss percentage based on sigma
                new_stop_loss_percentage=self.p.stop_loss_percentage*(1+sigma)
                if self.data.close<self.last_buy_price*(1-new_stop_loss_percentage):
                    self.sell(size=self.position.size)
                    self.log("Volatility Adjusted Stop Loss Sale %.3f" % new_stop_loss_percentage)
                    is_stop_loss_applied=True

        return is_stop_loss_applied