Encapsulated interface��

1��getKline(symbol, klinePeriod, size) ->dict

2��getDepth(symbol) -> dict
   
3��getJumpPrice(symbol) -> float
   
4��buy(symbol, price, amount) -> str // orderId 
     
5��sell(symbol, price, amount) -> str // orderId 

6��short(symbol, price, amount) -> str // orderId 

7��cover(symbol, price, amount) -> str // orderId 
 
8��cancelOrder(symbol, orderId) -> str // true:�����ɹ� false:ʧ��
  
9��getOrderInfoState(symbol, orderId) -> str // -2:"����",-1:"������",0:"ȫ���ɽ�" 1: "���ֳɽ�",2:"δ�ɽ�" 3:"������" 4:"�ѳ���" 5:"���ֳɽ�����"
                                                                               6:"�ܾ�����" 7:"����" 8:"ʧ��" 9:"�µ���

10��getPosition(symbol) -> float
 
11��getUsdt() -> float

12��getLastPrice(symbol) -> float
 
13��getPositionSt(symbol) -> float
 
PS������������ 1��huobi 2:binance 3:okex
 