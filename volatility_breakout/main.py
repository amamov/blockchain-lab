from config import get_secret
import pyupbit

UPBIT_ACCESS_KEY = get_secret("UPBIT_ACCESS_KEY")
UPBIT_SECRET_KEY = get_secret("UPBIT_SECRET_KEY")

upbit = pyupbit.Upbit(access=UPBIT_ACCESS_KEY, secret=UPBIT_SECRET_KEY)

if __name__ == "__main__":
    print(upbit.get_balance("KRW-BTC"))  # 비트코인
    print(upbit.get_balance("KRW-ETH"))  # 이더리움
    print(upbit.get_balance("KRW"))
