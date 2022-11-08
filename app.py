from flask import Flask, render_template, request, jsonify, redirect
from flask import session as s_mgt
import psycopg2 # on ubuntu, sudo apt-get install libpq-dev, sudo pip install psycopg2/sudo pip install psycopg2-binary
from binance.client import Client
from datetime import datetime
from decimal import Decimal
import json
import math
import ast
import requests
from psycopg2 import sql
import time
import threading
import decimal
import pybit.spot
import pybit.usdt_perpetual
import pytz

app = Flask(__name__)
app.secret_key = "Notofomo'sdash"

api_key = ""
api_secret = ""

dash_user_name = "tradernb"
dash_password = "NoToFOMO123"

colors = [
    "#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA",
    "#ABCDEF", "#DDDDDD", "#ABCABC", "#4169E1",
    "#C71585", "#FF4500", "#FEDCBA", "#46BFBD"]

#establishing the connection
conn = psycopg2.connect(
   database="gpu", user='postgres', password='postgres', host='127.0.0.1', port= '5432')
#Creating a cursor object using the cursor() method
cursor = conn.cursor()

#Executing an MYSQL function using the execute() method
cursor.execute("select version()")

# Fetch a single row using fetchone() method.
data = cursor.fetchone()
print("Connection established to: ",data)

cursor.execute("ALTER DATABASE gpu SET timezone TO 'Europe/Berlin';")
conn.commit()


client = Client(api_key, api_secret)

try:
    cursor.execute("select api_key from binance_keys")
    r_2 = cursor.fetchall()
    binance_api_key = r_2[0][0]
except:
    binance_api_key = "Enter Api Key"
    cursor.execute("insert into binance_keys(api_key) values (%s)",
                   [binance_api_key])
    conn.commit()
    print("Records inserted")

try:
    cursor.execute("select api_secret from binance_keys")
    r_2 = cursor.fetchall()
    binance_api_secret = r_2[0][0]
except:
    binance_api_secret = "Enter Api Secret"
    cursor.execute("insert into binance_keys(api_secret) values (%s)",
                   [binance_api_secret])
    conn.commit()
    print("Records inserted")

try:
    cursor.execute("select api_key from bybit_keys")
    r_2 = cursor.fetchall()
    bybit_api_key = r_2[0][0]
except:
    bybit_api_key = "Enter Api Key"
    cursor.execute("insert into bybit_keys(api_key) values (%s)",
                   [bybit_api_key])
    conn.commit()
    print("Records inserted")

try:
    cursor.execute("select api_secret from bybit_keys")
    r_2 = cursor.fetchall()
    bybit_api_secret = r_2[0][0]
except:
    bybit_api_secret = "Enter Api Secret"
    cursor.execute("insert into bybit_keys(api_secret) values (%s)",
                   [bybit_api_secret])
    conn.commit()
    print("Records inserted")


@app.route('/')
def welcome():
    return render_template('welcome.html')

@app.route('/profile',methods=["POST","GET"])
def get_profile():
    if "password" in s_mgt:
        entered_pw = s_mgt["password"]
        if request.method == "GET":
            try:
                cursor.execute("select api_key from binance_keys")
                r_2 = cursor.fetchall()
                binance_api_key = r_2[0][0]
            except:
                binance_api_key = "Enter Api Key"

            try:
                cursor.execute("select api_secret from binance_keys")
                r_2 = cursor.fetchall()
                binance_api_secret = r_2[0][0]
            except:
                binance_api_secret = "Enter Api Secret"

            try:
                cursor.execute("select api_key from bybit_keys")
                r_2 = cursor.fetchall()
                bybit_api_key = r_2[0][0]
            except:
                bybit_api_key = "Enter Api Key"

            try:
                cursor.execute("select api_secret from bybit_keys")
                r_2 = cursor.fetchall()
                bybit_api_secret = r_2[0][0]
            except:
                bybit_api_secret = "Enter Api Secret"


            return render_template('profile.html',bi_key=binance_api_key,bi_secret=binance_api_secret,by_key=bybit_api_key,by_secret=bybit_api_secret)
        if request.method == "POST":
            binance_api_key = request.form["binance_key"]
            binance_api_secret = request.form["binance_secret"]
            bybit_api_key = request.form["bybit_key"]
            bybit_api_secret = request.form["bybit_secret"]

            cursor.execute("update binance_keys set api_key = %s, api_secret = %s",[binance_api_key, binance_api_secret])
            conn.commit()
            print("Records inserted")
            print("Done")

            cursor.execute("update bybit_keys set api_key = %s, api_secret = %s", [bybit_api_key, bybit_api_secret])
            conn.commit()
            print("Records inserted")
            print("Done")

            return render_template('profile.html',bi_key=binance_api_key,bi_secret=binance_api_secret,by_key=bybit_api_key,by_secret=bybit_api_secret)
    else:
        return redirect("/")

correct_un = ""
correct_pw = ""
entered_ex = "Select Exchange"
entered_tt = "Select Trade Type"
entered_bc = "Select Base Coin"

@app.route('/copy_msg',methods=["POST"])
def get_json():
    if "password" in s_mgt:
        entered_pw = s_mgt["password"]
        try:
            exchange1 = '{"exchange"'
            exchange2 = entered_ex
            trade_type1 = "trade_type"
            trade_type2 = entered_tt
            base_coin1 = "base_coin"
            base_coin2 = entered_bc
            coin_pair = request.form["coin_pair"]
            coin_pair1 = "coin_pair"
            coin_pair2 = coin_pair
            entry_type = request.form["entry_type"]
            entry_type1 = "entry_type"
            entry_type2 = entry_type
            exit_type = request.form["exit_type"]
            exit_type1 = "exit_type"
            exit_type2 = exit_type
            margin_mode = request.form["margin_mode"]
            margin_mode1 = "margin_mode"
            margin_mode2 = margin_mode
            amt_type = request.form["amt_type"]
            amt_type1 = "qty_type"
            amt_type2 = amt_type
            enter_amt = request.form["enter_amt"]
            enter_amt1 = "qty"
            enter_amt2 = enter_amt
            long_lev = request.form["long_lev"]
            long_lev1 = "long_leverage"
            long_lev2 = long_lev
            short_lev = request.form["short_lev"]
            short_lev1 = "short_leverage"
            short_lev2 = short_lev
            long_sl = request.form["long_sl"]
            long_sl1 = "long_stop_loss_percent"
            long_sl2 = long_sl
            long_tp = request.form["long_tp"]
            long_tp1 = "long_take_profit_percent"
            long_tp2 = long_tp
            short_sl = request.form["short_sl"]
            short_sl1 = "short_stop_loss_percent"
            short_sl2 = short_sl
            short_tp = request.form["short_tp"]
            short_tp1 = "short_take_profit_percent"
            short_tp2 = short_tp
            multi_tp = request.form["multi_tp"]
            multi_tp1 = "enable_multi_tp"
            multi_tp2 = multi_tp
            tp1_pos_size = request.form["tp1_pos_size"]
            tp1_pos_size1 = "tp_1_pos_size"
            tp1_pos_size2 = tp1_pos_size
            tp2_pos_size = request.form["tp2_pos_size"]
            tp2_pos_size1 = "tp_2_pos_size"
            tp2_pos_size2 = tp2_pos_size
            tp3_pos_size = request.form["tp3_pos_size"]
            tp3_pos_size1 = "tp_3_pos_size"
            tp3_pos_size2 = tp3_pos_size
            tp1_percent = request.form["tp1_percent"]
            tp1_percent1 = "tp1_percent"
            tp1_percent2 = tp1_percent
            tp2_percent = request.form["tp2_percent"]
            tp2_percent1 = "tp2_percent"
            tp2_percent2 = tp2_percent
            tp3_percent = request.form["tp3_percent"]
            tp3_percent1 = "tp3_percent"
            tp3_percent2 = tp3_percent
            stop_bot = request.form["stop_bot"]
            stop_bot1 = "stop_bot_below_balance"
            stop_bot2 = stop_bot
            time_out = request.form["time_out"]
            time_out1 = "order_time_out"
            time_out2 = time_out

            enterlong1 = "position_type"
            enterlong2 = '"Enter_long"}'
            entershort1 = "position_type"
            entershort2 = '"Enter_short"}'
            exitlong1 = "position_type"
            exitlong2 = '"Exit_long"}'
            exitshort1 = "position_type"
            exitshort2 = '"Exit_short"}'


            return render_template('copy_msg.html',exchange1=exchange1,exchange2=exchange2,trade_type1=trade_type1,trade_type2=trade_type2,base_coin1=base_coin1,base_coin2=base_coin2,coin_pair1=coin_pair1,coin_pair2=coin_pair2,entry_type1=entry_type1,entry_type2=entry_type2,exit_type1=exit_type1,exit_type2=exit_type2,margin_mode1=margin_mode1,margin_mode2=margin_mode2,amt_type1=amt_type1,amt_type2=amt_type2,enter_amt1=enter_amt1,enter_amt2=enter_amt2,long_lev1=long_lev1,long_lev2=long_lev2,short_lev1=short_lev1,short_lev2=short_lev2,long_sl1=long_sl1,long_sl2=long_sl2,long_tp1=long_tp1,long_tp2=long_tp2,short_sl1=short_sl1,short_sl2=short_sl2,short_tp1=short_tp1,short_tp2=short_tp2,multi_tp1=multi_tp1,multi_tp2=multi_tp2,tp1_pos_size1=tp1_pos_size1,tp1_pos_size2=tp1_pos_size2,tp2_pos_size1=tp2_pos_size1,tp2_pos_size2=tp2_pos_size2,tp3_pos_size1=tp3_pos_size1,tp3_pos_size2=tp3_pos_size2,tp1_percent1=tp1_percent1,tp1_percent2=tp1_percent2,tp2_percent1=tp2_percent1,tp2_percent2=tp2_percent2,tp3_percent1=tp3_percent1,tp3_percent2=tp3_percent2,stop_bot1=stop_bot1,stop_bot2=stop_bot2,time_out1=time_out1,time_out2=time_out2,enterlong1=enterlong1,enterlong2=enterlong2,entershort1=entershort1,entershort2=entershort2,exitlong1=exitlong1,exitlong2=exitlong2,exitshort1=exitshort1,exitshort2=exitshort2)
        except:
            return render_template('missing_fields.html')
    else:
        return redirect("/")

@app.route('/json_generator',methods=["POST", "GET"])
def gen_json():
    global correct_pw
    global correct_un
    global entered_ex
    global entered_tt
    global entered_bc
    list_of_coin_pairs = []
    dup_removed_list = []
    base_url = "https://api.bybit.com"
    session = pybit.spot.HTTP(base_url, api_key, api_secret)
    f_session = pybit.usdt_perpetual.HTTP(base_url, api_key, api_secret)

    try:
        entered_ex = request.form["exchange"]
    except:
        pass
    try:
        entered_tt = request.form["trade_type"]
    except:
        pass
    try:
        entered_bc = request.form["base_coin"]
    except:
        pass

    if entered_tt != "Select Trade Type" and entered_ex != "Select Exchange" and entered_bc != "Select Base Coin":
        if entered_ex == "Binance":
            if entered_tt == "Spot":
                spot_e_i = client.get_exchange_info()
                spot_e_info = spot_e_i["symbols"]

                for item in spot_e_info:
                    quote_asset = item["quoteAsset"]
                    if quote_asset == entered_bc:
                        cp = item["symbol"]
                        list_of_coin_pairs.append(cp)
            if entered_tt == "Futures":
                futures_e_i = client.futures_exchange_info()
                futures_e_info = futures_e_i["symbols"]

                for item in futures_e_info:
                    quote_asset = item["quoteAsset"]
                    if quote_asset == entered_bc:
                        cp = item["symbol"]
                        list_of_coin_pairs.append(cp)
        if entered_ex == "Bybit":
            if entered_tt == "Spot":
                exchange_info = session.query_symbol()

                for s in exchange_info['result']:
                    quote_asset = s['quoteCurrency']
                    if quote_asset == entered_bc:
                        cp = s["name"]
                        list_of_coin_pairs.append(cp)
            if entered_tt == "Futures":
                exchange_info = f_session.query_symbol()

                for s in exchange_info['result']:
                    quote_asset = s['quote_currency']
                    if quote_asset == entered_bc:
                        cp = s["name"]
                        list_of_coin_pairs.append(cp)

        dup_removed_list = list(dict.fromkeys(list_of_coin_pairs))


    if request.method == "POST":
        try:
            entered_un = request.form["Username"]
            entered_pw = request.form["Password"]
            correct_un = entered_un
            correct_pw = entered_pw
        except:
            pass
        s_mgt["password"] = correct_pw

        if correct_un == dash_user_name and correct_pw == dash_password:

            if list_of_coin_pairs == []:
                list_with_error = ["Required fields missing or incorrect to generate coin pairs"]
                return render_template('json_gen.html', coin_list=list_with_error,exchange_name=entered_ex,trade_name=entered_tt,base_coin_name=entered_bc)
            else:
                return render_template('json_gen.html', coin_list=dup_removed_list,exchange_name=entered_ex,trade_name=entered_tt,base_coin_name=entered_bc)
        else:
            return render_template('welcome_incorrect_credentials.html')

    if request.method == "GET":
        if list_of_coin_pairs == []:
            list_with_error = ["Required fields missing to generate coin pairs"]
            return render_template('json_gen.html', coin_list=list_with_error,exchange_name=entered_ex,trade_name=entered_tt,base_coin_name=entered_bc)
        else:
            return render_template('json_gen.html',coin_list=dup_removed_list,exchange_name=entered_ex,trade_name=entered_tt,base_coin_name=entered_bc)

@app.route('/binance_spot',methods=["POST", "GET"])
def index():
    if "password" in s_mgt:
        entered_pw = s_mgt["password"]
        # establishing the connection
        conn = psycopg2.connect(
            database="gpu", user='postgres', password='postgres', host='127.0.0.1', port='5432')
        # Creating a cursor object using the cursor() method
        cursor = conn.cursor()

        # Executing an MYSQL function using the execute() method
        cursor.execute("select version()")

        # Fetch a single row using fetchone() method.
        data = cursor.fetchone()
        print("Connection established to: ", data)

        cursor.execute("ALTER DATABASE gpu SET timezone TO 'Europe/Berlin';")
        conn.commit()

        print(request)
        global api_key
        global api_secret

        try:
            cursor.execute("select api_key from binance_keys")
            r_2 = cursor.fetchall()
            if r_2[0][0] == "Enter Api Key":
                api_key = ""
            else:
                api_key = r_2[0][0]
        except:
            api_key = ""

        try:
            cursor.execute("select api_secret from binance_keys")
            r_2 = cursor.fetchall()
            if r_2[0][0] == "Enter Api Secret":
                api_secret = ""
            else:
                api_secret = r_2[0][0]
        except:
            api_secret = ""

        if api_key and api_secret != "":
            try:
                client = Client(api_key, api_secret)
            except:
                return render_template('invalid_key.html')


            try:

                open_orders = client.get_open_orders()

                sql = ''' DELETE FROM open_orders '''
                cursor.execute(sql)
                conn.commit()


                for order in open_orders:

                    create_time = order["time"]
                    SPOT_OR_CREATE_DATE = datetime.fromtimestamp((create_time / 1000)).strftime("%Y-%m-%d")
                    # SPOT_OR_CREATE_TIME = datetime.fromtimestamp((create_time / 1000)).strftime("%I:%M:%S")
                    SPOT_SYM = order["symbol"]
                    SPOT_OR_ID = order["orderId"]
                    p = order["price"]
                    num = Decimal(p)
                    SPOT_PRICE = num.normalize()
                    q = order["origQty"]
                    q_num = Decimal(q)
                    SPOT_QUANTITY = q_num.normalize()
                    SPOT_OR_ACTION = order["side"]
                    SPOT_OR_TYPE = order["type"]

                    prices = client.get_all_tickers()
                    for ticker in prices:
                        if ticker["symbol"] == SPOT_SYM:
                            SPOT_SYM_CURRENT_PRICE = float(ticker["price"])
                            break

                    try:
                        cursor.execute("select entry_price from s_id_list where order_id = %s", [SPOT_OR_ID])
                        result = cursor.fetchall()
                        ENTRY_PRICE_OF_BUY_ORDER = float(result[0][0])

                        # p_o_l = ((SPOT_SYM_CURRENT_PRICE - ENTRY_PRICE_OF_BUY_ORDER)/ENTRY_PRICE_OF_BUY_ORDER)
                        # p_o_l_r = round(p_o_l,6)
                        #
                        # PROFIT_OR_LOSS_FROM_ENTRY = ("{:.3%}".format(p_o_l_r))
                        p_n_l = round((SPOT_SYM_CURRENT_PRICE - ENTRY_PRICE_OF_BUY_ORDER),3)
                        p_o_l = ((SPOT_SYM_CURRENT_PRICE - ENTRY_PRICE_OF_BUY_ORDER) / ENTRY_PRICE_OF_BUY_ORDER) * 100
                        PROFIT_OR_LOSS_FROM_ENTRY = str((round(p_o_l, 3))) + "%"

                        print(PROFIT_OR_LOSS_FROM_ENTRY)

                        cursor.execute(
                            "insert into open_orders(created_date, symbol, order_id, price, quantity, order_action, order_type, entry_price, current_price, pnl,pnl_per) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s)",
                            [SPOT_OR_CREATE_DATE, SPOT_SYM, SPOT_OR_ID, SPOT_PRICE, SPOT_QUANTITY, SPOT_OR_ACTION,
                             SPOT_OR_TYPE, ENTRY_PRICE_OF_BUY_ORDER, SPOT_SYM_CURRENT_PRICE, p_n_l,
                             PROFIT_OR_LOSS_FROM_ENTRY])
                        conn.commit()
                    except:
                        cursor.execute(
                            "insert into open_orders(created_date, symbol, order_id, price, quantity, order_action, order_type, current_price) values (%s, %s, %s, %s, %s, %s, %s, %s)",
                            [SPOT_OR_CREATE_DATE, SPOT_SYM, SPOT_OR_ID, SPOT_PRICE, SPOT_QUANTITY, SPOT_OR_ACTION,
                             SPOT_OR_TYPE, SPOT_SYM_CURRENT_PRICE])
                        conn.commit()


            except:
                pass

            cursor.execute("SELECT to_char(created_date, 'DD-mon-YYYY HH12:MIPM'),order_id,symbol,price,quantity,order_action,order_type,entry_price,current_price,pnl,pnl_per FROM open_orders;")
            rowResults=cursor.fetchall()
            list_length = len(rowResults)

            exchange_info = client.get_exchange_info()
            list_of_coin_pairs = []
            for s in exchange_info['symbols']:
                baseAsset = s['baseAsset']
                list_of_coin_pairs.append((baseAsset + "USD"))
            dup_removed_list = list(dict.fromkeys(list_of_coin_pairs))

            cursor.execute("SELECT to_char(occured_time, 'DD-mon-YYYY HH12:MIPM'),symbol,order_action,entry_order_type,exit_order_type,quantity,error_description FROM error_log;")
            error_rowResults = cursor.fetchall()
            error_list_length = len(error_rowResults)

            cursor.execute("SELECT to_char(date_time, 'DD-mon-YYYY HH12:MIPM'),order_id,symbol,order_action,order_type,executed_price,executed_qty,execution,pnl,percentage FROM trade_log;")
            trade_rowResults = cursor.fetchall()
            trade_list_length = len(trade_rowResults)

            try:
                deposits = client.get_deposit_history()
                total_deposited_amt = float(0)
                for deposit in deposits:
                    deposited_coin_name = deposit["coin"]
                    deposited_amount = float(deposit["amount"])
                    if deposited_coin_name == "USDT":
                        total_deposited_amt += deposited_amount
                    else:
                        current_price_USDT = client.get_symbol_ticker(symbol=deposited_coin_name + "USDT")["price"]
                        total_deposited_amt += deposited_amount * float(current_price_USDT)
                deposits_display = f"Deposited Amt (USD): {round((total_deposited_amt), 2)}"
            except:
                return render_template('invalid_key.html')

            try:
                margin_info = client.get_margin_account()["userAssets"]
                margin_balance = float(0)
                for margin_asset in margin_info:
                    value = float(margin_asset["free"]) + float(margin_asset["locked"])
                    margin_balance += value
                print(f"Margin balance = {margin_balance}")

                futures_info = client.futures_account_balance()
                futures_usd = 0.0
                for futures_asset in futures_info:
                    name = futures_asset["asset"]
                    balance = float(futures_asset["balance"])
                    if name == "USDT":
                        futures_usd += balance

                    else:
                        current_price_USDT = client.get_symbol_ticker(symbol=name + "USDT")["price"]
                        futures_usd += balance * float(current_price_USDT)
                print(f"Futures balance = {futures_usd}")

                sum_SPOT = 0.0
                balances = client.get_account()
                for _balance in balances["balances"]:
                    asset = _balance["asset"]
                    if float(_balance["free"]) != 0.0 or float(_balance["locked"]) != 0.0:
                        if asset == "USDT":
                            usdt_quantity = float(_balance["free"]) + float(_balance["locked"])
                            sum_SPOT += usdt_quantity
                        try:
                            btc_quantity = float(_balance["free"]) + float(_balance["locked"])
                            _price = client.get_symbol_ticker(symbol=asset + "USDT")
                            sum_SPOT += btc_quantity * float(_price["price"])
                        except:
                            pass
                print(f"Spot balance = {sum_SPOT}")
                total_asset_balance = sum_SPOT + futures_usd + margin_balance
                asset_balance_display = f"Asset Balance (USD): {round((total_asset_balance), 2)}"
                spot_balance_display = f"Asset Balance (USD): {round((sum_SPOT), 2)}"
            except:
                asset_balance_display = "Asset Balance (USD): NA"
                spot_balance_display = "Asset Balance (USD): NA"

            cursor.execute("select sum(pnl) as total from trade_log")
            results = cursor.fetchall()
            try:
                overall_pnl = float(round((results[0][0]), 2))
                pnl_display = f"Spot PnL (USD): {overall_pnl}"
            except:
                overall_pnl = "NA"
                pnl_display = "Spot PnL (USD): NA"

            labels = []
            values = []

            labels.clear()
            values.clear()

            try:
                acc_info = client.get_account()
                prices = client.get_all_tickers()
                for asset in acc_info["balances"]:
                    if float(asset["free"]) != 0.0 or float(asset["locked"]) != 0.0:
                        pair_name = asset["asset"]
                        total_bal = float(asset["free"]) + float(asset["locked"])
                        for price in prices:
                            sym_for_price = price["symbol"]
                            if pair_name + "USDT" == sym_for_price:
                                usdt_price = float(price["price"])
                                value_in_usdt = (total_bal * usdt_price)
                                break
                        if pair_name == "USDT" and total_bal > 2:
                            labels.append(pair_name)
                            values.append(round(total_bal, 2))
                        if value_in_usdt > 2:
                            labels.append(pair_name)
                            values.append(round(value_in_usdt, 2))
            except:
                pass

            try:
                coin_pair_name = request.form["coins"]
                href_modified = f"https://www.tradingview.com/symbols/{coin_pair_name}/?exchange=BITSTAMP"
            except:
                coin_pair_name = "BTCUSD"
                href_modified = f"https://www.tradingview.com/symbols/{coin_pair_name}/?exchange=BITSTAMP"


            return render_template('index.html',recentRecords=rowResults,list_length=list_length,coin_list=dup_removed_list,coin_pair_name=coin_pair_name,modified_link=href_modified,labels=labels,values=values,colors=colors,error_recentRecords=error_rowResults,error_list_length=error_list_length,trade_recentRecords=trade_rowResults,trade_list_length=trade_list_length,deposits=deposits_display,assets=asset_balance_display,pnl=pnl_display,spot=spot_balance_display)

        else:
            return render_template('error.html')

    else:
        return redirect("/")

@app.route('/bybit_spot',methods=["POST", "GET"])
def get_bybit_spot():
    if "password" in s_mgt:
        entered_pw = s_mgt["password"]
        # establishing the connection
        conn = psycopg2.connect(database="gpu", user='postgres', password='postgres', host='127.0.0.1', port='5432')
        # Creating a cursor object using the cursor() method
        cursor = conn.cursor()

        # Executing an MYSQL function using the execute() method
        cursor.execute("select version()")

        # Fetch a single row using fetchone() method.
        data = cursor.fetchone()
        print("Connection established to: ", data)

        cursor.execute("ALTER DATABASE gpu SET timezone TO 'Europe/Berlin';")
        conn.commit()

        print(request)
        global api_key
        global api_secret

        try:
            cursor.execute("select api_key from bybit_keys")
            r_2 = cursor.fetchall()
            if r_2[0][0] == "Enter Api Key":
                api_key = ""
            else:
                api_key = r_2[0][0]
        except:
            api_key = ""

        try:
            cursor.execute("select api_secret from bybit_keys")
            r_2 = cursor.fetchall()
            if r_2[0][0] == "Enter Api Secret":
                api_secret = ""
            else:
                api_secret = r_2[0][0]
        except:
            api_secret = ""

        if api_key and api_secret != "":
            try:
                base_url = "https://api.bybit.com"
                session = pybit.spot.HTTP(base_url, api_key, api_secret)
            except:
                return render_template('invalid_key.html')


            try:

                open_orders = session.query_active_order()

                sql = ''' DELETE FROM bybit_open_orders '''
                cursor.execute(sql)
                conn.commit()


                for order in open_orders["result"]["list"]:

                    create_time = order["createTime"]
                    SPOT_OR_CREATE_DATE = datetime.fromtimestamp((create_time / 1000)).strftime("%Y-%m-%d")
                    # SPOT_OR_CREATE_TIME = datetime.fromtimestamp((create_time / 1000)).strftime("%I:%M:%S")
                    SPOT_SYM = order["symbol"]
                    SPOT_OR_ID = order["orderId"]
                    SPOT_PRICE = order["orderPrice"]
                    SPOT_QUANTITY = order["orderQty"]
                    SPOT_OR_ACTION = order["side"]
                    SPOT_OR_TYPE = order["orderType"]

                    symbol_data = (session.latest_information_for_symbol(symbol=SPOT_SYM))
                    SPOT_SYM_CURRENT_PRICE = float(symbol_data['result']['lastPrice'])


                    try:
                        cursor.execute("select entry_price from s_id_list where order_id = %s", [SPOT_OR_ID])
                        result = cursor.fetchall()
                        ENTRY_PRICE_OF_BUY_ORDER = float(result[0][0])

                        # p_o_l = ((SPOT_SYM_CURRENT_PRICE - ENTRY_PRICE_OF_BUY_ORDER)/ENTRY_PRICE_OF_BUY_ORDER)
                        # p_o_l_r = round(p_o_l,6)
                        #
                        # PROFIT_OR_LOSS_FROM_ENTRY = ("{:.3%}".format(p_o_l_r))
                        p_n_l = round((SPOT_SYM_CURRENT_PRICE - ENTRY_PRICE_OF_BUY_ORDER),3)
                        p_o_l = ((SPOT_SYM_CURRENT_PRICE - ENTRY_PRICE_OF_BUY_ORDER) / ENTRY_PRICE_OF_BUY_ORDER) * 100
                        PROFIT_OR_LOSS_FROM_ENTRY = str((round(p_o_l, 3))) + "%"

                        print(PROFIT_OR_LOSS_FROM_ENTRY)

                        cursor.execute(
                            "insert into bybit_open_orders(created_date, symbol, order_id, price, quantity, order_action, order_type, entry_price, current_price, pnl,pnl_per) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s)",
                            [SPOT_OR_CREATE_DATE, SPOT_SYM, SPOT_OR_ID, SPOT_PRICE, SPOT_QUANTITY, SPOT_OR_ACTION,
                             SPOT_OR_TYPE, ENTRY_PRICE_OF_BUY_ORDER, SPOT_SYM_CURRENT_PRICE, p_n_l,
                             PROFIT_OR_LOSS_FROM_ENTRY])
                        conn.commit()
                    except:
                        cursor.execute(
                            "insert into bybit_open_orders(created_date, symbol, order_id, price, quantity, order_action, order_type, current_price) values (%s, %s, %s, %s, %s, %s, %s, %s)",
                            [SPOT_OR_CREATE_DATE, SPOT_SYM, SPOT_OR_ID, SPOT_PRICE, SPOT_QUANTITY, SPOT_OR_ACTION,
                             SPOT_OR_TYPE, SPOT_SYM_CURRENT_PRICE])
                        conn.commit()


                open_orders_2 = session.query_active_order(orderCategory=1)

                for order in open_orders_2["result"]["list"]:
                    create_time = order["createTime"]
                    SPOT_OR_CREATE_DATE = datetime.fromtimestamp((create_time / 1000)).strftime("%Y-%m-%d")
                    # SPOT_OR_CREATE_TIME = datetime.fromtimestamp((create_time / 1000)).strftime("%I:%M:%S")
                    SPOT_SYM = order["symbol"]
                    SPOT_OR_ID = order["orderId"]
                    SPOT_PRICE = order["triggerPrice"]
                    SPOT_QUANTITY = order["orderQty"]
                    SPOT_OR_ACTION = order["side"]
                    SPOT_OR_TYPE = order["orderType"]

                    symbol_data = (session.latest_information_for_symbol(symbol=SPOT_SYM))
                    SPOT_SYM_CURRENT_PRICE = float(symbol_data['result']['lastPrice'])

                    try:
                        cursor.execute("select entry_price from s_id_list where order_id = %s", [SPOT_OR_ID])
                        result = cursor.fetchall()
                        ENTRY_PRICE_OF_BUY_ORDER = float(result[0][0])

                        # p_o_l = ((SPOT_SYM_CURRENT_PRICE - ENTRY_PRICE_OF_BUY_ORDER)/ENTRY_PRICE_OF_BUY_ORDER)
                        # p_o_l_r = round(p_o_l,6)
                        #
                        # PROFIT_OR_LOSS_FROM_ENTRY = ("{:.3%}".format(p_o_l_r))
                        p_n_l = round((SPOT_SYM_CURRENT_PRICE - ENTRY_PRICE_OF_BUY_ORDER), 3)
                        p_o_l = ((SPOT_SYM_CURRENT_PRICE - ENTRY_PRICE_OF_BUY_ORDER) / ENTRY_PRICE_OF_BUY_ORDER) * 100
                        PROFIT_OR_LOSS_FROM_ENTRY = str((round(p_o_l, 3))) + "%"

                        print(PROFIT_OR_LOSS_FROM_ENTRY)

                        cursor.execute(
                            "insert into bybit_open_orders(created_date, symbol, order_id, price, quantity, order_action, order_type, entry_price, current_price, pnl,pnl_per) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s)",
                            [SPOT_OR_CREATE_DATE, SPOT_SYM, SPOT_OR_ID, SPOT_PRICE, SPOT_QUANTITY, SPOT_OR_ACTION,
                             SPOT_OR_TYPE, ENTRY_PRICE_OF_BUY_ORDER, SPOT_SYM_CURRENT_PRICE, p_n_l,
                             PROFIT_OR_LOSS_FROM_ENTRY])
                        conn.commit()
                    except:
                        cursor.execute(
                            "insert into bybit_open_orders(created_date, symbol, order_id, price, quantity, order_action, order_type, current_price) values (%s, %s, %s, %s, %s, %s, %s, %s)",
                            [SPOT_OR_CREATE_DATE, SPOT_SYM, SPOT_OR_ID, SPOT_PRICE, SPOT_QUANTITY, SPOT_OR_ACTION,
                             SPOT_OR_TYPE, SPOT_SYM_CURRENT_PRICE])
                        conn.commit()


            except:
                pass

            try:
                cursor.execute("SELECT to_char(created_date, 'DD-mon-YYYY HH12:MIPM'),order_id,symbol,price,quantity,order_action,order_type,entry_price,current_price,pnl,pnl_per FROM bybit_open_orders;")
                rowResults=cursor.fetchall()
                list_length = len(rowResults)
            except:
                rowResults = []
                list_length = 0

            exchange_info = session.query_symbol()
            list_of_coin_pairs = []
            for s in exchange_info['result']:
                baseAsset = s['baseCurrency']
                list_of_coin_pairs.append((baseAsset + "USD"))
            dup_removed_list = list(dict.fromkeys(list_of_coin_pairs))

            try:
                cursor.execute("SELECT to_char(occured_time, 'DD-mon-YYYY HH12:MIPM'),symbol,order_action,entry_order_type,exit_order_type,quantity,error_description FROM bybit_error_log;")
                error_rowResults = cursor.fetchall()
                error_list_length = len(error_rowResults)
            except:
                error_rowResults = []
                error_list_length = 0

            try:
                cursor.execute("SELECT to_char(date_time, 'DD-mon-YYYY HH12:MIPM'),symbol,order_id,order_action,order_type,executed_price,executed_qty,execution,pnl,percentage FROM bybit_trade_log;")
                trade_rowResults = cursor.fetchall()
                trade_list_length = len(trade_rowResults)
            except:
                trade_rowResults = []
                trade_list_length = 0

            try:
                spot_balance = session.get_wallet_balance()
                spot_total_asset_balance = 0
                for bals in spot_balance["result"]["balances"]:
                    if bals["coin"] == "USDT":
                        USD_BAL = float(bals["total"])
                        spot_total_asset_balance += USD_BAL
                    else:
                        other_coin = bals["coin"]
                        other_coin_bal = float(bals["total"])
                        sym_for_bal = other_coin+"USDT"
                        symbol_data = (session.latest_information_for_symbol(symbol=sym_for_bal))
                        usdt_price_of_other_coin = float(symbol_data['result']['lastPrice'])
                        OTHER_COIN_BALANCE = other_coin_bal * usdt_price_of_other_coin
                        spot_total_asset_balance += OTHER_COIN_BALANCE

                f_session = pybit.usdt_perpetual.HTTP(base_url, api_key, api_secret)

                futures_balance = f_session.get_wallet_balance()
                futures_total_asset_balance = 0
                for bals in futures_balance["result"]:
                    if bals == "USDT":
                        USD_BAL = float(futures_balance["result"][bals]["equity"])
                        futures_total_asset_balance += USD_BAL
                    else:
                        other_coin = bals
                        other_coin_bal = float(futures_balance["result"][bals]["equity"])
                        sym_for_bal = other_coin + "USDT"
                        print(sym_for_bal)
                        try:
                            symbol_data = (f_session.latest_information_for_symbol(symbol=sym_for_bal))
                            usdt_price_of_other_coin = float(symbol_data['result'][0]['last_price'])
                            OTHER_COIN_BALANCE = other_coin_bal * usdt_price_of_other_coin
                            futures_total_asset_balance += OTHER_COIN_BALANCE
                        except:
                            pass

                total_asset_balance = spot_total_asset_balance + futures_total_asset_balance
                asset_balance_display = f"Asset Balance (USD): {round((total_asset_balance), 2)}"
                spot_balance_display = f"Asset Balance (USD): {round((spot_total_asset_balance), 2)}"
            except:
                asset_balance_display = "Asset Balance (USD): NA"
                spot_balance_display = "Asset Balance (USD): NA"

            try:
                cursor.execute("select sum(pnl) as total from bybit_trade_log")
                results = cursor.fetchall()

                overall_pnl = float(round((results[0][0]), 2))
                pnl_display = f"Spot PnL (USD): {overall_pnl}"
            except:
                overall_pnl = "NA"
                pnl_display = "Spot PnL (USD): NA"

            labels = []
            values = []

            labels.clear()
            values.clear()

            try:
                spot_balance = session.get_wallet_balance()

                for bals in spot_balance["result"]["balances"]:
                    pair_name = bals["coin"]
                    labels.append(pair_name)

                    if pair_name == "USDT":
                        USD_BAL = round(float(bals["total"]), 2)
                        values.append(USD_BAL)
                    else:
                        other_coin = bals["coin"]
                        other_coin_bal = float(bals["total"])
                        sym_for_bal = other_coin + "USDT"
                        symbol_data = (session.latest_information_for_symbol(symbol=sym_for_bal))
                        usdt_price_of_other_coin = float(symbol_data['result']['lastPrice'])
                        OTHER_COIN_BALANCE = round((other_coin_bal * usdt_price_of_other_coin), 2)
                        values.append(OTHER_COIN_BALANCE)
            except:
                pass

            try:
                coin_pair_name = request.form["coins"]
                href_modified = f"https://www.tradingview.com/symbols/{coin_pair_name}/?exchange=BITSTAMP"
            except:
                coin_pair_name = "BTCUSD"
                href_modified = f"https://www.tradingview.com/symbols/{coin_pair_name}/?exchange=BITSTAMP"


            return render_template('bybit_index.html',recentRecords=rowResults,list_length=list_length,coin_list=dup_removed_list,coin_pair_name=coin_pair_name,modified_link=href_modified,labels=labels,values=values,colors=colors,error_recentRecords=error_rowResults,error_list_length=error_list_length,trade_recentRecords=trade_rowResults,trade_list_length=trade_list_length,assets=asset_balance_display,pnl=pnl_display,spot=spot_balance_display)

        else:
            return render_template('error.html')

    else:
        return redirect("/")

@app.route('/binance_futures',methods=["POST", "GET"])
def get_futures():
    if "password" in s_mgt:
        entered_pw = s_mgt["password"]
        # establishing the connection
        conn = psycopg2.connect(
            database="gpu", user='postgres', password='postgres', host='127.0.0.1', port='5432')
        # Creating a cursor object using the cursor() method
        cursor = conn.cursor()

        # Executing an MYSQL function using the execute() method
        cursor.execute("select version()")

        # Fetch a single row using fetchone() method.
        data = cursor.fetchone()
        print("Connection established to: ", data)

        cursor.execute("ALTER DATABASE gpu SET timezone TO 'Europe/Berlin';")
        conn.commit()

        print(request)
        global api_key
        global api_secret

        try:
            cursor.execute("select api_key from binance_keys")
            r_2 = cursor.fetchall()
            api_key = r_2[0][0]
        except:
            api_key = ""

        try:
            cursor.execute("select api_secret from binance_keys")
            r_2 = cursor.fetchall()
            api_secret = r_2[0][0]
        except:
            api_secret = ""

        if api_key and api_secret != "":
            try:
                client = Client(api_key, api_secret)
            except:
                return render_template('invalid_key.html')

            try:

                open_orders = client.futures_get_open_orders()

                sql = ''' DELETE FROM f_o_orders '''
                cursor.execute(sql)
                conn.commit()


                for order in open_orders:

                    create_time = order["time"]
                    create_date = datetime.fromtimestamp((create_time / 1000)).strftime("%Y-%m-%d")
                    # SPOT_OR_CREATE_TIME = datetime.fromtimestamp((create_time / 1000)).strftime("%I:%M:%S")
                    sym = order["symbol"]
                    id = order["orderId"]
                    p = order["stopPrice"]
                    num = Decimal(p)
                    price = num.normalize()

                    action= order["side"]
                    type = order["type"]

                    prices = client.get_all_tickers()
                    for ticker in prices:
                        if ticker["symbol"] == sym:
                            sym_current_price = float(ticker["price"])
                            break

                    try:
                        cursor.execute("select entry_price from f_id_list where order_id = %s", [id])
                        result = cursor.fetchall()
                        ENTRY_PRICE_OF_INITIAL_ORDER = float(result[0][0])

                        cursor.execute("select qty from f_id_list where order_id = %s", [id])
                        result = cursor.fetchall()
                        QTY_OF_OPEN_ORDER = float(result[0][0])

                        p_n_l = round((sym_current_price - ENTRY_PRICE_OF_INITIAL_ORDER),3)
                        p_o_l = ((sym_current_price - ENTRY_PRICE_OF_INITIAL_ORDER) / ENTRY_PRICE_OF_INITIAL_ORDER) * 100
                        PROFIT_OR_LOSS_FROM_ENTRY = str((round(p_o_l, 3))) + "%"


                        cursor.execute("insert into f_o_orders(created_date, symbol, order_id, price, quantity, order_action, order_type, entry_price, current_price, pnl, pnl_per) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",[create_date, sym, id, price, QTY_OF_OPEN_ORDER, action,type, ENTRY_PRICE_OF_INITIAL_ORDER, sym_current_price, p_n_l, PROFIT_OR_LOSS_FROM_ENTRY])
                        conn.commit()
                    except:
                        cursor.execute(
                            "insert into f_o_orders(created_date, symbol, order_id, price, order_action, order_type, current_price) values (%s, %s, %s, %s, %s, %s, %s)",
                            [create_date, sym, id, price, action, type, sym_current_price])
                        conn.commit()

            except:
                pass

            try:

                open_positions = client.futures_position_information()

                sql = ''' DELETE FROM f_o_positions '''
                cursor.execute(sql)
                conn.commit()

                for order in open_positions:
                    sym = order["symbol"]
                    create_time = order["updateTime"]
                    create_date = datetime.fromtimestamp((create_time / 1000)).strftime("%Y-%m-%d")
                    # SPOT_OR_CREATE_TIME = datetime.fromtimestamp((create_time / 1000)).strftime("%I:%M:%S")
                    pos_entry_price = float(order["entryPrice"])
                    liquidation_price = float(order["liquidationPrice"])
                    pos_current_price = float(order["markPrice"])

                    margin_type = order["marginType"]
                    leverage = int(order["leverage"])

                    if float(order["positionAmt"]) < 0:
                        pos_qty = (float(order["positionAmt"]))*-1
                        pos_side = "SELL"
                    else:
                        pos_qty = float(order["positionAmt"])
                        pos_side = "BUY"

                    PROFIT_OR_LOSS_FROM_ENTRY = round((float(order["unRealizedProfit"])),6)

                    if float(order["positionAmt"]) != 0:
                        cursor.execute(
                            "insert into f_o_positions(created_date, symbol, side, entry_price, current_price, liq_price, margin_type, leverage, quantity, pnl) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                            [create_date, sym, pos_side, pos_entry_price, pos_current_price, liquidation_price, margin_type, leverage, pos_qty,PROFIT_OR_LOSS_FROM_ENTRY])
                        conn.commit()
            except Exception as e:
                print(f"open position error = {e}")
                pass

            cursor.execute("SELECT to_char(created_date, 'DD-mon-YYYY HH12:MIPM'),order_id,symbol,price,quantity,order_action,order_type,entry_price,current_price,pnl,pnl_per FROM f_o_orders;")
            rowResults=cursor.fetchall()
            list_length = len(rowResults)

            cursor.execute("SELECT to_char(created_date, 'DD-mon-YYYY HH12:MIPM') symbol,side,entry_price,current_price,liq_price,margin_type,leverage,quantity,pnl FROM f_o_positions;")
            pos_rowResults = cursor.fetchall()
            pos_list_length = len(pos_rowResults)


            exchange_info = client.get_exchange_info()
            list_of_coin_pairs = []
            for s in exchange_info['symbols']:
                baseAsset = s['baseAsset']
                list_of_coin_pairs.append((baseAsset + "USD"))
            dup_removed_list = list(dict.fromkeys(list_of_coin_pairs))

            cursor.execute("SELECT to_char(occured_time, 'DD-mon-YYYY HH12:MIPM'),symbol,order_action,entry_order_type,exit_order_type,quantity,error_description FROM futures_e_log;")
            error_rowResults = cursor.fetchall()
            error_list_length = len(error_rowResults)

            cursor.execute("SELECT to_char(date_time, 'DD-mon-YYYY HH12:MIPM'),order_id,symbol,order_action,order_type,executed_price,executed_qty,execution,pnl FROM futures_t_log;")
            trade_rowResults = cursor.fetchall()
            trade_list_length = len(trade_rowResults)
            for i in range(0, trade_list_length)[::-1]:
                print(i)

            try:
                deposits = client.get_deposit_history()
                total_deposited_amt = float(0)
                for deposit in deposits:
                    deposited_coin_name = deposit["coin"]
                    deposited_amount = float(deposit["amount"])
                    if deposited_coin_name == "USDT":
                        total_deposited_amt += deposited_amount
                    else:
                        current_price_USDT = client.get_symbol_ticker(symbol=deposited_coin_name + "USDT")["price"]
                        total_deposited_amt += deposited_amount * float(current_price_USDT)
                deposits_display = f"Deposited Amt (USD): {round((total_deposited_amt), 2)}"
            except:
                return render_template('invalid_key.html')


            try:
                margin_info = client.get_margin_account()["userAssets"]
                margin_balance = float(0)
                for margin_asset in margin_info:
                    value = float(margin_asset["free"]) + float(margin_asset["locked"])
                    margin_balance += value
                print(f"Margin balance = {margin_balance}")

                futures_info = client.futures_account_balance()
                futures_usd = 0.0
                for futures_asset in futures_info:
                    name = futures_asset["asset"]
                    balance = float(futures_asset["balance"])
                    if name == "USDT":
                        futures_usd += balance

                    else:
                        current_price_USDT = client.get_symbol_ticker(symbol=name + "USDT")["price"]
                        futures_usd += balance * float(current_price_USDT)
                print(f"Futures balance = {futures_usd}")

                sum_SPOT = 0.0
                balances = client.get_account()
                for _balance in balances["balances"]:
                    asset = _balance["asset"]
                    if float(_balance["free"]) != 0.0 or float(_balance["locked"]) != 0.0:
                        if asset == "USDT":
                            usdt_quantity = float(_balance["free"]) + float(_balance["locked"])
                            sum_SPOT += usdt_quantity
                        try:
                            btc_quantity = float(_balance["free"]) + float(_balance["locked"])
                            _price = client.get_symbol_ticker(symbol=asset + "USDT")
                            sum_SPOT += btc_quantity * float(_price["price"])
                        except:
                            pass
                print(f"Spot balance = {sum_SPOT}")
                total_asset_balance = sum_SPOT + futures_usd + margin_balance
                asset_balance_display = f"Asset Balance (USD): {round((total_asset_balance), 2)}"
                futures_balance_display = f"Asset Balance (USD): {round((futures_usd), 2)}"
            except:
                asset_balance_display = "Asset Balance (USD): NA"
                futures_balance_display = "Asset Balance (USD): NA"

            cursor.execute("select sum(pnl) as total from futures_t_log")
            results = cursor.fetchall()
            try:
                overall_pnl = float(round((results[0][0]), 2))
                pnl_display = f"Futures PnL (USD): {overall_pnl}"
            except:
                overall_pnl = "NA"
                pnl_display = "Futures PnL (USD): NA"

            labels = []
            values = []

            labels.clear()
            values.clear()

            try:
                acc_info = client.futures_account_balance()
                prices = client.get_all_tickers()
                for asset in acc_info:
                    pair_name = asset["asset"]
                    total_bal = float(asset["balance"])
                    for price in prices:
                        sym_for_price = price["symbol"]
                        if pair_name + "USDT" == sym_for_price:
                            usdt_price = float(price["price"])
                            value_in_usdt = (total_bal * usdt_price)
                            break
                    if pair_name == "USDT" and total_bal > 2:
                        labels.append(pair_name)
                        values.append(round(total_bal, 2))
                    if value_in_usdt > 2:
                        labels.append(pair_name)
                        values.append(round(value_in_usdt, 2))
            except:
                pass

            try:
                coin_pair_name = request.form["coins"]
                href_modified = f"https://www.tradingview.com/symbols/{coin_pair_name}/?exchange=BITSTAMP"
            except:
                coin_pair_name = "BTCUSD"
                href_modified = f"https://www.tradingview.com/symbols/{coin_pair_name}/?exchange=BITSTAMP"


            return render_template('futures.html',pos_rowResults=pos_rowResults,pos_list_length=pos_list_length,recentRecords=rowResults,list_length=list_length,coin_list=dup_removed_list,coin_pair_name=coin_pair_name,modified_link=href_modified,labels=labels,values=values,colors=colors,error_recentRecords=error_rowResults,error_list_length=error_list_length,trade_recentRecords=trade_rowResults,trade_list_length=trade_list_length,deposits=deposits_display,assets=asset_balance_display,pnl=pnl_display,spot=futures_balance_display)

        else:
            return render_template('error.html')

    else:
        return redirect("/")

@app.route('/bybit_futures',methods=["POST", "GET"])
def get_bybit_futures():
    if "password" in s_mgt:
        entered_pw = s_mgt["password"]
        # establishing the connection
        conn = psycopg2.connect(
            database="gpu", user='postgres', password='postgres', host='127.0.0.1', port='5432')
        # Creating a cursor object using the cursor() method
        cursor = conn.cursor()

        # Executing an MYSQL function using the execute() method
        cursor.execute("select version()")

        # Fetch a single row using fetchone() method.
        data = cursor.fetchone()
        print("Connection established to: ", data)

        cursor.execute("ALTER DATABASE gpu SET timezone TO 'Europe/Berlin';")
        conn.commit()

        print(request)
        global api_key
        global api_secret

        try:
            cursor.execute("select api_key from bybit_keys")
            r_2 = cursor.fetchall()
            api_key = r_2[0][0]
        except:
            api_key = ""

        try:
            cursor.execute("select api_secret from bybit_keys")
            r_2 = cursor.fetchall()
            api_secret = r_2[0][0]
        except:
            api_secret = ""

        if api_key and api_secret != "":
            try:
                base_url = "https://api.bybit.com"
                f_session = pybit.usdt_perpetual.HTTP(base_url, api_key, api_secret)
            except:
                return render_template('invalid_key.html')

            try:

                sql = ''' DELETE FROM bybit_f_o_orders '''
                cursor.execute(sql)
                conn.commit()

                list_of_p = []

                try:
                    query = cursor.execute("select pair from bybit_futures_coin_pairs")
                    result = cursor.fetchall()
                    for r in result:
                        coin_p = r[0]
                        list_of_p.append(coin_p)
                except Exception as e:
                    print(e)
                    pass

                list_of_pairs = list(dict.fromkeys(list_of_p))

                for pair in list_of_pairs:
                    try:
                        query_r = f_session.query_active_order(symbol=pair)
                        query_result = query_r["result"]
                        if query_result == []:
                            pass
                        else:
                            for order in query_result:
                                # create_time = order["created_time"]
                                # create_date = datetime.fromtimestamp((create_time / 1000)).strftime("%Y-%m-%d")
                                # SPOT_OR_CREATE_TIME = datetime.fromtimestamp((create_time / 1000)).strftime("%I:%M:%S")
                                sym = order["symbol"]
                                id = order["order_id"]
                                price = order["price"]

                                action = order["side"]
                                type = order["order_type"]

                                symbol_data = (f_session.latest_information_for_symbol(symbol=sym))
                                sym_current_price = float(symbol_data['result'][0]['last_price'])

                                try:
                                    cursor.execute("select entry_price from bybit_f_id_list where order_id = %s", [id])
                                    result = cursor.fetchall()
                                    ENTRY_PRICE_OF_INITIAL_ORDER = float(result[0][0])

                                    QTY_OF_OPEN_ORDER = float(order["qty"])

                                    p_n_l = round((sym_current_price - ENTRY_PRICE_OF_INITIAL_ORDER), 3)
                                    p_o_l = ((sym_current_price - ENTRY_PRICE_OF_INITIAL_ORDER) / ENTRY_PRICE_OF_INITIAL_ORDER) * 100
                                    PROFIT_OR_LOSS_FROM_ENTRY = str((round(p_o_l, 3))) + "%"

                                    cursor.execute(
                                        "insert into bybit_f_o_orders(symbol, order_id, price, quantity, order_action, order_type, entry_price, current_price, pnl, pnl_per) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                                        [sym, id, price, QTY_OF_OPEN_ORDER, action, type,
                                         ENTRY_PRICE_OF_INITIAL_ORDER, sym_current_price, p_n_l, PROFIT_OR_LOSS_FROM_ENTRY])
                                    conn.commit()
                                except:
                                    cursor.execute(
                                        "insert into bybit_f_o_orders(symbol, order_id, price, order_action, order_type, current_price) values (%s, %s, %s, %s, %s, %s)",
                                        [sym, id, price, action, type, sym_current_price])
                                    conn.commit()
                    except:
                        pass

                for pair in list_of_pairs:
                    try:
                        query_r = f_session.query_conditional_order(symbol=pair)
                        query_result = query_r["result"]
                        if query_result == []:
                            pass
                        else:
                            for order in query_result:
                                # create_time = order["time"]
                                # create_date = datetime.fromtimestamp((create_time / 1000)).strftime("%Y-%m-%d")
                                # SPOT_OR_CREATE_TIME = datetime.fromtimestamp((create_time / 1000)).strftime("%I:%M:%S")
                                sym = order["symbol"]
                                id = order["stop_order_id"]
                                price = order["trigger_price"]

                                action = order["side"]
                                type = order["order_type"]

                                symbol_data = (f_session.latest_information_for_symbol(symbol=sym))
                                sym_current_price = float(symbol_data['result'][0]['last_price'])

                                try:
                                    cursor.execute("select entry_price from bybit_f_id_list where order_id = %s", [id])
                                    result = cursor.fetchall()
                                    ENTRY_PRICE_OF_INITIAL_ORDER = float(result[0][0])

                                    cursor.execute("select qty from bybit_f_id_list where order_id = %s", [id])
                                    result = cursor.fetchall()
                                    QTY_OF_OPEN_ORDER = float(order["qty"])

                                    p_n_l = round((sym_current_price - ENTRY_PRICE_OF_INITIAL_ORDER), 3)
                                    p_o_l = ((
                                                         sym_current_price - ENTRY_PRICE_OF_INITIAL_ORDER) / ENTRY_PRICE_OF_INITIAL_ORDER) * 100
                                    PROFIT_OR_LOSS_FROM_ENTRY = str((round(p_o_l, 3))) + "%"

                                    cursor.execute(
                                        "insert into bybit_f_o_orders(symbol, order_id, price, quantity, order_action, order_type, entry_price, current_price, pnl, pnl_per) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                                        [sym, id, price, QTY_OF_OPEN_ORDER, action, type,
                                         ENTRY_PRICE_OF_INITIAL_ORDER, sym_current_price, p_n_l, PROFIT_OR_LOSS_FROM_ENTRY])
                                    conn.commit()
                                except:
                                    cursor.execute(
                                        "insert into f_o_orders(symbol, order_id, price, order_action, order_type, current_price) values (%s, %s, %s, %s, %s, %s)",
                                        [sym, id, price, action, type, sym_current_price])
                                    conn.commit()
                    except:
                        pass

            except:
                pass

            try:
                open_positions = f_session.my_position()

                sql = ''' DELETE FROM bybit_f_o_positions '''
                cursor.execute(sql)
                conn.commit()

                for item in open_positions["result"]:
                    i = item["data"]
                    if i["size"] != 0:
                        pos_qty = float(i["size"])
                        sym = i["symbol"]
                        # create_date = datetime.fromtimestamp((create_time / 1000)).strftime("%Y-%m-%d")
                        # # SPOT_OR_CREATE_TIME = datetime.fromtimestamp((create_time / 1000)).strftime("%I:%M:%S")
                        pos_entry_price = float(i["entry_price"])
                        liquidation_price = float(i["liq_price"])
                        symbol_data = (f_session.latest_information_for_symbol(symbol=sym))
                        pos_current_price = float(symbol_data['result'][0]['last_price'])

                        type = i["is_isolated"]
                        if type == "False":
                            margin_type = "Cross"
                        else:
                            margin_type = "Isolated"
                        leverage = int(i["leverage"])

                        pos_side = i["side"]

                        PROFIT_OR_LOSS_FROM_ENTRY = round((float(i["unrealised_pnl"])),6)

                        cursor.execute(
                            "insert into bybit_f_o_positions(symbol, side, entry_price, current_price, liq_price, margin_type, leverage, quantity, pnl) values (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                            [sym, pos_side, pos_entry_price, pos_current_price, liquidation_price, margin_type, leverage, pos_qty,PROFIT_OR_LOSS_FROM_ENTRY])
                        conn.commit()
            except Exception as e:
                print(f"open position error = {e}")
                pass

            try:
                order_statement='SELECT * FROM bybit_f_o_orders;'
                cursor.execute(order_statement)
                rowResults=cursor.fetchall()
                list_length = len(rowResults)
            except:
                rowResults = []
                list_length = 0

            try:
                order_statement = 'SELECT * FROM bybit_f_o_positions;'
                cursor.execute(order_statement)
                pos_rowResults = cursor.fetchall()
                pos_list_length = len(pos_rowResults)
            except:
                pos_rowResults = []
                pos_list_length = 0

            exchange_info = f_session.query_symbol()
            list_of_coin_pairs = []
            for s in exchange_info["result"]:
                baseAsset = s["base_currency"]
                list_of_coin_pairs.append((baseAsset + "USD"))
            dup_removed_list = list(dict.fromkeys(list_of_coin_pairs))

            try:
                cursor.execute("SELECT to_char(occured_time, 'DD-mon-YYYY HH12:MIPM'),symbol,order_action,entry_order_type,exit_order_type,quantity,error_description FROM bybit_futures_e_log;")
                error_rowResults = cursor.fetchall()
                error_list_length = len(error_rowResults)
            except:
                error_rowResults = []
                error_list_length = 0

            try:
                cursor.execute("SELECT to_char(date_time, 'DD-mon-YYYY HH12:MIPM'),order_id,symbol,order_action,order_type,executed_price,executed_qty,execution,pnl FROM bybit_futures_t_log;")
                trade_rowResults = cursor.fetchall()
                trade_list_length = len(trade_rowResults)
                for i in range(0, trade_list_length)[::-1]:
                    print(i)
            except:
                trade_rowResults = []
                trade_list_length = 0

            try:
                session = pybit.spot.HTTP(base_url, api_key, api_secret)

                spot_balance = session.get_wallet_balance()
                spot_total_asset_balance = 0
                for bals in spot_balance["result"]["balances"]:
                    if bals["coin"] == "USDT":
                        USD_BAL = float(bals["total"])
                        spot_total_asset_balance += USD_BAL
                    else:
                        other_coin = bals["coin"]
                        other_coin_bal = float(bals["total"])
                        sym_for_bal = other_coin+"USDT"
                        symbol_data = (session.latest_information_for_symbol(symbol=sym_for_bal))
                        usdt_price_of_other_coin = float(symbol_data['result']['lastPrice'])
                        OTHER_COIN_BALANCE = other_coin_bal * usdt_price_of_other_coin
                        spot_total_asset_balance += OTHER_COIN_BALANCE

                f_session = pybit.usdt_perpetual.HTTP(base_url, api_key, api_secret)

                futures_balance = f_session.get_wallet_balance()
                futures_total_asset_balance = 0
                for bals in futures_balance["result"]:
                    if bals == "USDT":
                        USD_BAL = float(futures_balance["result"][bals]["equity"])
                        futures_total_asset_balance += USD_BAL
                    else:
                        other_coin = bals
                        other_coin_bal = float(futures_balance["result"][bals]["equity"])
                        sym_for_bal = other_coin + "USDT"
                        print(sym_for_bal)
                        try:
                            symbol_data = (f_session.latest_information_for_symbol(symbol=sym_for_bal))
                            usdt_price_of_other_coin = float(symbol_data['result'][0]['last_price'])
                            OTHER_COIN_BALANCE = other_coin_bal * usdt_price_of_other_coin
                            futures_total_asset_balance += OTHER_COIN_BALANCE
                        except:
                            pass

                total_asset_balance = spot_total_asset_balance + futures_total_asset_balance
                asset_balance_display = f"Asset Balance (USD): {round((total_asset_balance), 2)}"
                futures_balance_display = f"Asset Balance (USD): {round((futures_total_asset_balance), 2)}"
            except:
                asset_balance_display = "Asset Balance (USD): NA"
                futures_balance_display = "Asset Balance (USD): NA"

            try:
                cursor.execute("select sum(pnl) as total from bybit_futures_t_log")
                results = cursor.fetchall()

                overall_pnl = float(round((results[0][0]), 2))
                pnl_display = f"Futures PnL (USD): {overall_pnl}"
            except:
                overall_pnl = "NA"
                pnl_display = "Futures PnL (USD): NA"

            labels = []
            values = []

            labels.clear()
            values.clear()

            try:
                futures_balance = f_session.get_wallet_balance()

                for bals in futures_balance["result"]:
                    future_available_bal = float(futures_balance["result"][bals]["equity"])
                    if future_available_bal > 0:
                        pair_name = bals
                        if pair_name == "USDT":
                            labels.append(pair_name)
                            values.append(round(future_available_bal, 2))
                        else:
                            other_coin = bals
                            sym_for_bal = other_coin + "USDT"
                            try:
                                symbol_data = (f_session.latest_information_for_symbol(symbol=sym_for_bal))
                                usdt_price_of_other_coin = float(symbol_data['result'][0]['last_price'])
                                OTHER_COIN_BALANCE = future_available_bal * usdt_price_of_other_coin
                                labels.append(other_coin)
                                values.append(round(OTHER_COIN_BALANCE, 2))
                            except:
                                pass
            except:
                pass

            try:
                coin_pair_name = request.form["coins"]
                href_modified = f"https://www.tradingview.com/symbols/{coin_pair_name}/?exchange=BITSTAMP"
            except:
                coin_pair_name = "BTCUSD"
                href_modified = f"https://www.tradingview.com/symbols/{coin_pair_name}/?exchange=BITSTAMP"


            return render_template('bybit_futures.html',pos_rowResults=pos_rowResults,pos_list_length=pos_list_length,recentRecords=rowResults,list_length=list_length,coin_list=dup_removed_list,coin_pair_name=coin_pair_name,modified_link=href_modified,labels=labels,values=values,colors=colors,error_recentRecords=error_rowResults,error_list_length=error_list_length,trade_recentRecords=trade_rowResults,trade_list_length=trade_list_length,assets=asset_balance_display,pnl=pnl_display,spot=futures_balance_display)

        else:
            return render_template('error.html')

    else:
        return redirect("/")

@app.route('/webhook', methods=["POST"])
def process_alert():
    cursor.execute("ALTER DATABASE gpu SET timezone TO 'Europe/Berlin';")
    conn.commit()
    IST = pytz.timezone('Europe/Berlin')
    try:
        cursor.execute("select api_key from binance_keys")
        r_2 = cursor.fetchall()
        binance_api_key = r_2[0][0]
    except:
        binance_api_key = ""

    try:
        cursor.execute("select api_secret from binance_keys")
        r_2 = cursor.fetchall()
        binance_api_secret = r_2[0][0]
    except:
        binance_api_secret = ""

    try:
        cursor.execute("select api_key from bybit_keys")
        r_2 = cursor.fetchall()
        bybit_api_key = r_2[0][0]
    except:
        bybit_api_key = ""

    try:
        cursor.execute("select api_secret from bybit_keys")
        r_2 = cursor.fetchall()
        bybit_api_secret = r_2[0][0]
    except:
        bybit_api_secret = ""


    print("Webhook triggered")
    print(request)
    alert = request.get_data(as_text=True)

    alert_res = json.loads(json.dumps(alert))
    alert_response = json.loads(alert_res)
    print(f"Alert = {alert_response}")

    try:
        req_exchange = (alert_response["exchange"]).title()
    except Exception as e:
        print(e)
        error_occured_time = datetime.now(IST)
        error_occured = "Invalid/Empty exchange type"
        cursor.execute("insert into error_log(occured_time, error_description) values (%s, %s)",
                       [error_occured_time, error_occured])
        conn.commit()

    if req_exchange == "Binance":

        if binance_api_key and binance_api_secret != "":
            try:
                client = Client(binance_api_key, binance_api_secret)
            except:
                print("Alert failed due to invalid keys")

        try:
            req_trade_type = alert_response["trade_type"]
        except Exception as e:
            print(e)
            error_occured_time = datetime.now(IST)
            error_occured = "Invalid/Empty trade type"
            cursor.execute("insert into error_log(occured_time, error_description) values (%s, %s)",
                           [error_occured_time, error_occured])
            conn.commit()

        try:
            if req_trade_type == "Spot":

                try:
                    try:
                        req_base_coin = alert_response["base_coin"]
                    except Exception as e:
                        print(e)
                        error_occured_time = datetime.now(IST)
                        error_occured = "Invalid/Empty base coin"
                        cursor.execute("insert into error_log(occured_time, error_description) values (%s, %s)",
                                       [error_occured_time, error_occured])
                        conn.commit()

                    try:
                        req_coin_pair = alert_response["coin_pair"]
                    except Exception as e:
                        print(e)
                        error_occured_time = datetime.now(IST)
                        error_occured = "Invalid/Empty coin pair"
                        cursor.execute("insert into error_log(occured_time, error_description) values (%s, %s)",
                                       [error_occured_time, error_occured])
                        conn.commit()

                    req_entry_type = alert_response["entry_type"].upper()
                    req_exit_type = alert_response["exit_type"].upper()
                    req_margin_mode = alert_response["margin_mode"]
                    req_long_leverage = float(alert_response["long_leverage"])
                    req_short_leverage = float(alert_response["short_leverage"])

                    try:
                        req_qty_type = alert_response["qty_type"]
                    except Exception as e:
                        print(e)
                        error_occured_time = datetime.now(IST)
                        error_occured = "Invalid/Empty qty type"
                        cursor.execute("insert into error_log(occured_time, error_description) values (%s, %s)",
                                       [error_occured_time, error_occured])
                        conn.commit()

                    try:
                        req_qty = float(alert_response["qty"])
                    except Exception as e:
                        print(e)
                        error_occured_time = datetime.now(IST)
                        error_occured = "Invalid/Empty qty"
                        cursor.execute("insert into error_log(occured_time, error_description) values (%s, %s)",
                                       [error_occured_time, error_occured])
                        conn.commit()

                    req_long_leverage = alert_response["long_leverage"]
                    req_short_leverage = alert_response["short_leverage"]

                    req_long_stop_loss_percent = (float(alert_response["long_stop_loss_percent"])) / 100
                    req_long_take_profit_percent = (float(alert_response["long_take_profit_percent"])) / 100
                    req_short_stop_loss_percent = (float(alert_response["short_stop_loss_percent"])) / 100
                    req_short_take_profit_percent = (float(alert_response["short_take_profit_percent"])) / 100
                    print(f"req short tp = {req_short_take_profit_percent}")
                    req_multi_tp = alert_response["enable_multi_tp"]

                    req_tp1_qty_size = (float(alert_response["tp_1_pos_size"])) / 100
                    req_tp2_qty_size = (float(alert_response["tp_2_pos_size"])) / 100
                    req_tp3_qty_size = (float(alert_response["tp_3_pos_size"])) / 100

                    req_tp1_percent = (float(alert_response["tp1_percent"])) / 100
                    req_tp2_percent = (float(alert_response["tp2_percent"])) / 100
                    req_tp3_percent = (float(alert_response["tp3_percent"])) / 100

                    req_stop_bot_balance = float(alert_response["stop_bot_below_balance"])
                    req_order_time_out = float(alert_response["order_time_out"])

                    try:
                        req_position_type = alert_response["position_type"]
                    except Exception as e:
                        print(e)
                        error_occured_time = datetime.now(IST)
                        error_occured = "Invalid/Empty position type"
                        cursor.execute("insert into error_log(occured_time, error_description) values (%s, %s)",
                                       [error_occured_time, error_occured])
                        conn.commit()
                except Exception as e:
                    print(e)
                    error_occured_time = datetime.now(IST)
                    error_occured = "Error in parsing json alert"
                    cursor.execute("insert into error_log(occured_time, error_description) values (%s, %s)",
                                   [error_occured_time, error_occured])
                    conn.commit()

                SPOT_SYMBOL = req_coin_pair
                SPOT_ENTRY = req_entry_type
                SPOT_EXIT = req_exit_type

                # Check usdt balance in spot wallet
                def check_base_coin_balance():
                    balances = client.get_account()
                    for _balance in balances["balances"]:
                        asset = _balance["asset"]
                        if float(_balance["free"]) != 0.0 or float(_balance["locked"]) != 0.0:
                            if asset == req_base_coin:
                                base_coin_bal = float(_balance["free"]) + float(_balance["locked"])
                                break
                        else:
                            base_coin_bal = 0
                    return base_coin_bal

                def calculate_buy_qty_with_precision(SPOT_SYMBOL, qty_in_base_coin):
                    prices = client.get_all_tickers()
                    for ticker in prices:
                        if ticker["symbol"] == SPOT_SYMBOL:
                            current_market_price = float(ticker["price"])
                            break
                    tradeable_qty = qty_in_base_coin / current_market_price
                    info = client.get_symbol_info(SPOT_SYMBOL)
                    for x in info["filters"]:
                        if x["filterType"] == "LOT_SIZE":
                            stepSize = float(x["stepSize"])
                            print(f"step size = {stepSize}")

                    truncate_num = math.log10(1 / stepSize)
                    BUY_QUANTITY = math.floor((tradeable_qty) * 10 ** truncate_num) / 10 ** truncate_num
                    return BUY_QUANTITY

                def calculate_sell_qty_with_precision(SPOT_SYMBOL, buy_qty):
                    info = client.get_symbol_info(SPOT_SYMBOL)
                    for x in info["filters"]:
                        if x["filterType"] == "LOT_SIZE":
                            stepSize = float(x["stepSize"])
                            print(f"step size = {stepSize}")

                    truncate_num = math.log10(1 / stepSize)
                    SELL_QUANTITY = math.floor((buy_qty) * 10 ** truncate_num) / 10 ** truncate_num
                    return SELL_QUANTITY

                def trunc_calculate_sell_qty_with_precision(SPOT_SYMBOL, buy_qty):
                    sellable_qty_after_fees = float(buy_qty) * 0.998
                    info = client.get_symbol_info(SPOT_SYMBOL)
                    for x in info["filters"]:
                        if x["filterType"] == "LOT_SIZE":
                            stepSize = float(x["stepSize"])
                            print(f"step size = {stepSize}")

                    truncate_num = math.log10(1 / stepSize)
                    SELL_QUANTITY = math.floor((sellable_qty_after_fees) * 10 ** truncate_num) / 10 ** truncate_num
                    return SELL_QUANTITY

                def cal_price_with_precision(SPOT_SYMBOL, input_price):
                    data_from_api = client.get_exchange_info()
                    symbol_info = next(filter(lambda x: x['symbol'] == SPOT_SYMBOL, data_from_api['symbols']))
                    price_filters = next(filter(lambda x: x['filterType'] == 'PRICE_FILTER', symbol_info['filters']))
                    tick_size = price_filters["tickSize"]
                    num = Decimal(tick_size)
                    price_precision = int(len(str(num.normalize())) - 2)
                    price = round(input_price, price_precision)
                    return price

                def get_current_open_orders(SPOT_SYMBOL):
                    oo_id_list = []
                    current_open_orders = client.get_open_orders()

                    for oo in current_open_orders:
                        if oo["symbol"] == SPOT_SYMBOL:
                            oo_id_list.append(oo["orderId"])

                    return oo_id_list

                if req_qty_type == "Percentage":
                    current_bal = check_base_coin_balance()
                    qty_in_base_coin = current_bal * req_qty
                elif req_qty_type == "Fixed":
                    qty_in_base_coin = req_qty

                def execute_limit_oco_order(SPOT_SIDE, req_position_type, BUY_ORDER_ID, SPOT_SYMBOL, SPOT_SELL_QUANTITY,
                                            TAKE_PROFIT_PRICE_FINAL, STOP_LOSS_PRICE_FINAL, SPOT_ENTRY, req_multi_tp,
                                            req_qty_size, req_order_time_out,tp_type):
                    SPOT_EXIT = "LIMIT"
                    print(SPOT_SIDE)

                    # STOP_LOSS_PRICE_FINAL_S = cal_price_with_precision(SPOT_SYMBOL=SPOT_SYMBOL,input_price=(STOP_LOSS_PRICE_FINAL * 0.9999))
                    STOP_LOSS_PRICE_FINAL_B = cal_price_with_precision(SPOT_SYMBOL=SPOT_SYMBOL,
                                                                       input_price=(STOP_LOSS_PRICE_FINAL * 1.0009))

                    try:
                        if SPOT_SIDE == "SELL":
                            limit_oco_order = client.order_oco_sell(symbol=SPOT_SYMBOL, quantity=SPOT_SELL_QUANTITY,
                                                                    price=TAKE_PROFIT_PRICE_FINAL,
                                                                    stopPrice=STOP_LOSS_PRICE_FINAL,
                                                                    stopLimitPrice=STOP_LOSS_PRICE_FINAL,
                                                                    stopLimitTimeInForce="GTC")

                            for o in limit_oco_order["orders"]:
                                o_id_for_table = o["orderId"]
                                cursor.execute("select entry_price from long_entry where symbol = %s", [SPOT_SYMBOL])
                                r_3 = cursor.fetchall()
                                price_results = r_3[0][0]
                                p_for_table = float(price_results)

                                cursor.execute("insert into s_id_list(order_id, entry_price) values (%s, %s)",
                                               [o_id_for_table, p_for_table])
                                conn.commit()

                            for o_report in limit_oco_order["orderReports"]:
                                if o_report["type"] == "STOP_LOSS_LIMIT":
                                    oco_sl_order_i = o_report["orderId"]
                                if o_report["type"] == "LIMIT_MAKER":
                                    oco_tp_order_i = o_report["orderId"]

                            print(f"limit oco order = {limit_oco_order}")
                        if SPOT_SIDE == "BUY":
                            limit_oco_order = client.order_oco_buy(symbol=SPOT_SYMBOL, quantity=SPOT_SELL_QUANTITY,
                                                                   price=TAKE_PROFIT_PRICE_FINAL,
                                                                   stopPrice=STOP_LOSS_PRICE_FINAL_B,
                                                                   stopLimitPrice=STOP_LOSS_PRICE_FINAL,
                                                                   stopLimitTimeInForce="GTC")
                            print(f"limit oco order = {limit_oco_order}")

                            for o in limit_oco_order["orders"]:
                                o_id_for_table = o["orderId"]
                                cursor.execute("select entry_price from short_entry where symbol = %s", [SPOT_SYMBOL])
                                r_3 = cursor.fetchall()
                                price_results = r_3[0][0]
                                p_for_table = float(price_results)

                                cursor.execute("insert into s_id_list(order_id, entry_price) values (%s, %s)",
                                               [o_id_for_table, p_for_table])
                                conn.commit()

                    except Exception as e:

                        error_occured = f"{e}"
                        print(error_occured)

                        error_occured_time = datetime.now(IST)

                        cursor.execute(
                            "insert into error_log(symbol, order_action, entry_order_type, exit_order_type, quantity, occured_time, error_description) values (%s, %s, %s, %s, %s, %s, %s)",
                            [SPOT_SYMBOL, SPOT_SIDE, SPOT_ENTRY, SPOT_EXIT, SPOT_SELL_QUANTITY, error_occured_time,
                             error_occured])
                        conn.commit()

                        error = "APIError(code=-2010): Account has insufficient balance for requested action."
                        if str(e) == error and req_position_type == "Exit_long":
                            no_qty = True
                            oo_list = get_current_open_orders(SPOT_SYMBOL)

                            while no_qty == True:
                                for item in oo_list:
                                    client.cancel_order(symbol=SPOT_SYMBOL, orderId=item)
                                    try:
                                        if SPOT_SIDE == "SELL":
                                            limit_oco_order = client.order_oco_sell(symbol=SPOT_SYMBOL,
                                                                                    quantity=SPOT_SELL_QUANTITY,
                                                                                    price=TAKE_PROFIT_PRICE_FINAL,
                                                                                    stopPrice=STOP_LOSS_PRICE_FINAL,
                                                                                    stopLimitPrice=STOP_LOSS_PRICE_FINAL,
                                                                                    stopLimitTimeInForce="GTC")
                                            print(f"limit oco order = {limit_oco_order}")

                                            for o in limit_oco_order["orders"]:
                                                o_id_for_table = o["orderId"]
                                                cursor.execute("select entry_price from long_entry where symbol = %s",
                                                               [SPOT_SYMBOL])
                                                r_3 = cursor.fetchall()
                                                price_results = r_3[0][0]
                                                p_for_table = float(price_results)

                                                cursor.execute(
                                                    "insert into s_id_list(order_id, entry_price) values (%s, %s)",
                                                    [o_id_for_table, p_for_table])
                                                conn.commit()

                                        if SPOT_SIDE == "BUY":
                                            limit_oco_order = client.order_oco_buy(symbol=SPOT_SYMBOL,
                                                                                   quantity=SPOT_SELL_QUANTITY,
                                                                                   price=TAKE_PROFIT_PRICE_FINAL,
                                                                                   stopPrice=STOP_LOSS_PRICE_FINAL_B,
                                                                                   stopLimitPrice=STOP_LOSS_PRICE_FINAL,
                                                                                   stopLimitTimeInForce="GTC")
                                            print(f"limit oco order = {limit_oco_order}")

                                            for o in limit_oco_order["orders"]:
                                                o_id_for_table = o["orderId"]
                                                cursor.execute("select entry_price from short_entry where symbol = %s",
                                                               [SPOT_SYMBOL])
                                                r_3 = cursor.fetchall()
                                                price_results = r_3[0][0]
                                                p_for_table = float(price_results)

                                                cursor.execute(
                                                    "insert into s_id_list(order_id, entry_price) values (%s, %s)",
                                                    [o_id_for_table, p_for_table])
                                                conn.commit()

                                        no_qty = False
                                        break
                                    except Exception as e:
                                        print(e)
                                        pass

                    oco_order_ids = []

                    for item in limit_oco_order["orderReports"]:
                        limit_oco_order_ID = item["orderId"]
                        oco_order_ids.append(limit_oco_order_ID)
                        print(limit_oco_order_ID)

                    print(oco_order_ids)

                    def add_to_trade_oco():
                        while True:
                            time.sleep(4)
                            try:
                                for order_id in oco_order_ids:
                                    active_order = client.get_order(symbol=SPOT_SYMBOL, orderId=order_id)
                                    active_order_status = active_order["status"]
                                    if active_order_status == "FILLED":
                                        print("Filled")
                                        break
                                if active_order_status == "FILLED":
                                    break
                            except Exception as e:
                                print(e)
                                pass
                        if active_order_status == "FILLED":
                            oco_limit_sell_order = active_order
                            print(f"oco limit sell order = {oco_limit_sell_order}")
                        else:
                            for order_id in oco_order_ids:
                                check_for_partial = client.get_order(symbol=SPOT_SYMBOL, orderId=order_id)
                                if check_for_partial["status"] == "PARTIALLY_FILLED":
                                    oco_limit_sell_order = check_for_partial
                                check_for_cancel = client.get_order(symbol=SPOT_SYMBOL, orderId=order_id)
                                if check_for_cancel["status"] == "CANCELED" or check_for_cancel[
                                    "status"] != "PARTIALLY_FILLED" or check_for_cancel["status"] != "FILLED":
                                    print("Already cancelled")
                                else:
                                    cancel_oco_order = client.cancel_order(symbol=SPOT_SYMBOL, orderId=order_id)
                                error_occured = "Order time limit reached! Pending open oco sell orders have been cancelled"
                                print(error_occured)
                                error_occured_time = datetime.now(IST)
                                cursor.execute(
                                    "insert into error_log(symbol, order_action, entry_order_type, exit_order_type, quantity, occured_time, error_description) values (%s, %s, %s, %s, %s, %s, %s)",
                                    [SPOT_SYMBOL, SPOT_SIDE, SPOT_ENTRY, SPOT_EXIT, SPOT_SELL_QUANTITY, error_occured_time,
                                     error_occured])
                                conn.commit()

                        try:
                            OCO_SELL_ORDER_ID = oco_limit_sell_order["orderId"]
                            OCO_SELL_ORDER_SYMBOL = oco_limit_sell_order["symbol"]
                            OCO_SELL_ORDER_QTY = float(oco_limit_sell_order["executedQty"])
                            sell_cum_qty = float(oco_limit_sell_order["cummulativeQuoteQty"])
                            TOTAL_SELL_SPEND = (sell_cum_qty / 100) * 99.9
                            TOTAL_BUY_SPEND = float(oco_limit_sell_order["cummulativeQuoteQty"])
                            OCO_SELL_ORDER_PRICE = round((float(oco_limit_sell_order["cummulativeQuoteQty"]) / float(
                                oco_limit_sell_order["executedQty"])), 3)
                            OCO_SELL_ORDER_ACTION = oco_limit_sell_order["side"]
                            OCO_SELL_ORDER_TYPE = oco_limit_sell_order["type"]
                            sell_order_executed_time = datetime.now(IST)

                            if OCO_SELL_ORDER_ID == oco_sl_order_i:
                                execution = "Executed for Stop Loss"
                            if OCO_SELL_ORDER_ID == oco_tp_order_i:
                                if tp_type == "None":
                                    execution = "Executed for Take Profit"
                                if tp_type == "One":
                                    execution = "Executed for Take Profit 1"
                                if tp_type == "Two":
                                    execution = "Executed for Take Profit 2"
                                if tp_type == "Three":
                                    execution = "Executed for Take Profit 3"

                            if req_position_type == "Enter_long":
                                cursor.execute("select total_spend from id_list where order_id = %s", [BUY_ORDER_ID])
                                r_2 = cursor.fetchall()
                                price_results = r_2[0][0]
                                total_buy_spend = float(price_results)
                                print(f"Total buy spend from DB= {total_buy_spend}")

                                if req_multi_tp == "No":
                                    OCO_SELL_PNL = round((TOTAL_SELL_SPEND - total_buy_spend), 2)
                                    oco_sell_per = (OCO_SELL_PNL / total_buy_spend) * 100
                                    OCO_SELL_PNL_PERCENTAGE = str((round(oco_sell_per, 2))) + "%"
                                if req_multi_tp == "Yes":
                                    buy_spend_per = float(total_buy_spend) * float(req_qty_size)
                                    OCO_SELL_PNL = round((TOTAL_SELL_SPEND - buy_spend_per), 2)
                                    oco_sell_per = (OCO_SELL_PNL / buy_spend_per) * 100
                                    OCO_SELL_PNL_PERCENTAGE = str((round(oco_sell_per, 2))) + "%"

                                cursor.execute(sql.SQL(
                                    "insert into trade_log(date_time, symbol, order_id, order_action, order_type, executed_price, executed_qty, execution, pnl, percentage) values (%s, %s, %s, %s, %s, %s, %s, %s, %s,%s)"),
                                               [sell_order_executed_time, OCO_SELL_ORDER_SYMBOL, OCO_SELL_ORDER_ID,
                                                OCO_SELL_ORDER_ACTION, OCO_SELL_ORDER_TYPE, OCO_SELL_ORDER_PRICE,
                                                OCO_SELL_ORDER_QTY, execution, OCO_SELL_PNL, OCO_SELL_PNL_PERCENTAGE])
                                conn.commit()

                            if req_position_type == "Exit_long":
                                cursor.execute("select qty from long_entry where symbol = %s", [SPOT_SYMBOL])
                                r_3 = cursor.fetchall()
                                price_results = r_3[0][0]
                                previous_long_entry_qty = float(price_results)
                                print(f"previous_long_entry_qty = {previous_long_entry_qty}")

                                cursor.execute("select total_spend from long_entry where symbol = %s", [SPOT_SYMBOL])
                                r_3 = cursor.fetchall()
                                price_results = r_3[0][0]
                                previous_long_entry_spend = float(price_results)
                                print(f"previous_long_entry_spend = {previous_long_entry_spend}")

                                proportional_buy_spend = (
                                                                     previous_long_entry_spend / previous_long_entry_qty) * OCO_SELL_ORDER_QTY
                                OCO_SELL_PNL = round((TOTAL_SELL_SPEND - proportional_buy_spend), 2)
                                oco_sell_per = (OCO_SELL_PNL / proportional_buy_spend) * 100
                                OCO_SELL_PNL_PERCENTAGE = str((round(oco_sell_per, 2))) + "%"

                                cursor.execute(sql.SQL(
                                    "insert into trade_log(date_time, symbol, order_id, order_action, order_type, executed_price, executed_qty, execution, pnl, percentage) values (%s, %s, %s, %s, %s, %s, %s, %s, %s,%s)"),
                                               [sell_order_executed_time, OCO_SELL_ORDER_SYMBOL, OCO_SELL_ORDER_ID,
                                                OCO_SELL_ORDER_ACTION, OCO_SELL_ORDER_TYPE, OCO_SELL_ORDER_PRICE,
                                                OCO_SELL_ORDER_QTY, execution, OCO_SELL_PNL, OCO_SELL_PNL_PERCENTAGE])
                                conn.commit()

                            if req_position_type == "Enter_short":

                                cursor.execute("select exists (select 1 from short_entry)")
                                r_1 = cursor.fetchall()
                                live_r = r_1[0][0]

                                if live_r == False:
                                    cursor.execute(sql.SQL(
                                        "insert into short_entry(order_id, entry_price, total_spend, symbol, qty) values (%s, %s, %s, %s, %s)"),
                                                   [OCO_SELL_ORDER_ID, OCO_SELL_ORDER_PRICE, TOTAL_SELL_SPEND,
                                                    OCO_SELL_ORDER_SYMBOL, OCO_SELL_ORDER_QTY])
                                    conn.commit()
                                if live_r == True:
                                    cursor.execute(
                                        "update short_entry set order_id = %s, entry_price = %s, total_spend = %s, symbol = %s, qty = %s",
                                        [OCO_SELL_ORDER_ID, OCO_SELL_ORDER_PRICE, TOTAL_SELL_SPEND, OCO_SELL_ORDER_SYMBOL,
                                         OCO_SELL_ORDER_QTY])
                                    conn.commit()
                                    print("Records inserted")

                                cursor.execute(sql.SQL(
                                    "insert into trade_log(date_time, symbol, order_id, order_action, order_type, executed_price, executed_qty,execution) values (%s, %s, %s, %s, %s, %s, %s,%s)"),
                                               [sell_order_executed_time, OCO_SELL_ORDER_SYMBOL, OCO_SELL_ORDER_ID,
                                                OCO_SELL_ORDER_ACTION, OCO_SELL_ORDER_TYPE, OCO_SELL_ORDER_PRICE,
                                                OCO_SELL_ORDER_QTY,execution])
                                conn.commit()

                            if req_position_type == "Exit_short":
                                cursor.execute("select total_spend from short_entry where symbol = %s", [SPOT_SYMBOL])
                                r_3 = cursor.fetchall()
                                price_results = r_3[0][0]
                                previous_short_entry_income = float(price_results)
                                print(f"previous_short_entry_price = {previous_short_entry_income}")

                                cursor.execute("select qty from short_entry where symbol = %s", [SPOT_SYMBOL])
                                r_3 = cursor.fetchall()
                                price_results = r_3[0][0]
                                previous_short_entry_qty = float(price_results)
                                print(f"previous_short_entry_price = {previous_short_entry_qty}")

                                actual_sell_income = (previous_short_entry_income / 100) * 99.9
                                proportional_sell_income = (
                                                                       actual_sell_income / previous_short_entry_qty) * OCO_SELL_ORDER_QTY
                                OCO_SELL_PNL = round((proportional_sell_income - TOTAL_BUY_SPEND), 2)
                                oco_sell_per = (OCO_SELL_PNL / proportional_sell_income) * 100
                                OCO_SELL_PNL_PERCENTAGE = str((round(oco_sell_per, 2))) + "%"

                                cursor.execute(sql.SQL(
                                    "insert into trade_log(date_time, symbol, order_id, order_action, order_type, executed_price, executed_qty,execution, pnl, percentage) values (%s, %s, %s, %s, %s, %s, %s, %s, %s,%s)"),
                                    [sell_order_executed_time, OCO_SELL_ORDER_SYMBOL, OCO_SELL_ORDER_ID,
                                     OCO_SELL_ORDER_ACTION,
                                     OCO_SELL_ORDER_TYPE, OCO_SELL_ORDER_PRICE, OCO_SELL_ORDER_QTY, execution, OCO_SELL_PNL,
                                     OCO_SELL_PNL_PERCENTAGE])
                                conn.commit()


                        except Exception as e:
                            print(e)

                    t22 = threading.Thread(target=add_to_trade_oco)
                    t22.start()

                def execute_limit_stop_loss_order(SPOT_SIDE, req_position_type, BUY_ORDER_ID, SPOT_SYMBOL,
                                                  SPOT_SELL_QUANTITY, STOP_LOSS_PRICE_FINAL, SPOT_ENTRY,
                                                  req_order_time_out):
                    print(SPOT_SIDE)
                    SPOT_EXIT = "LIMIT"

                    STOP_LOSS_PRICE_FINAL_A = cal_price_with_precision(SPOT_SYMBOL=SPOT_SYMBOL,
                                                                       input_price=(STOP_LOSS_PRICE_FINAL * 0.9999))

                    try:
                        limit_stop_loss_order = client.create_order(symbol=SPOT_SYMBOL, side=SPOT_SIDE,
                                                                    type="STOP_LOSS_LIMIT",
                                                                    quantity=SPOT_SELL_QUANTITY,
                                                                    price=STOP_LOSS_PRICE_FINAL,
                                                                    stopPrice=STOP_LOSS_PRICE_FINAL_A, timeInForce="GTC")
                        print(f"limit stop loss order = {limit_stop_loss_order}")

                        if SPOT_SIDE == "BUY":
                            o_id_for_table = limit_stop_loss_order["orderId"]
                            cursor.execute("select entry_price from short_entry where symbol = %s", [SPOT_SYMBOL])
                            r_3 = cursor.fetchall()
                            price_results = r_3[0][0]
                            p_for_table = float(price_results)

                            cursor.execute("insert into s_id_list(order_id, entry_price) values (%s, %s)",
                                           [o_id_for_table, p_for_table])
                            conn.commit()
                        if SPOT_SIDE == "SELL":
                            o_id_for_table = limit_stop_loss_order["orderId"]
                            cursor.execute("select entry_price from long_entry where symbol = %s", [SPOT_SYMBOL])
                            r_3 = cursor.fetchall()
                            price_results = r_3[0][0]
                            p_for_table = float(price_results)

                            cursor.execute("insert into s_id_list(order_id, entry_price) values (%s, %s)",
                                           [o_id_for_table, p_for_table])
                            conn.commit()

                    except Exception as e:
                        error_occured = f"{e}"
                        print(error_occured)
                        error_occured_time = datetime.now(IST)

                        cursor.execute(
                            "insert into error_log(symbol, order_action, entry_order_type, exit_order_type, quantity, occured_time, error_description) values (%s, %s, %s, %s, %s, %s, %s)",
                            [SPOT_SYMBOL, SPOT_SIDE, SPOT_ENTRY, SPOT_EXIT, SPOT_SELL_QUANTITY, error_occured_time,
                             error_occured])
                        conn.commit()

                        error = "APIError(code=-2010): Account has insufficient balance for requested action."
                        if str(e) == error and req_position_type == "Exit_long":
                            no_qty = True
                            oo_list = get_current_open_orders(SPOT_SYMBOL)

                            while no_qty == True:
                                for item in oo_list:
                                    client.cancel_order(symbol=SPOT_SYMBOL, orderId=item)
                                    try:
                                        limit_stop_loss_order = client.create_order(symbol=SPOT_SYMBOL, side=SPOT_SIDE,
                                                                                    type="STOP_LOSS_LIMIT",
                                                                                    quantity=SPOT_SELL_QUANTITY,
                                                                                    price=STOP_LOSS_PRICE_FINAL,
                                                                                    stopPrice=STOP_LOSS_PRICE_FINAL_A,
                                                                                    timeInForce="GTC")
                                        print(f"limit stop loss order = {limit_stop_loss_order}")

                                        if SPOT_SIDE == "BUY":
                                            o_id_for_table = limit_stop_loss_order["orderId"]
                                            cursor.execute("select entry_price from short_entry where symbol = %s",
                                                           [SPOT_SYMBOL])
                                            r_3 = cursor.fetchall()
                                            price_results = r_3[0][0]
                                            p_for_table = float(price_results)

                                            cursor.execute("insert into s_id_list(order_id, entry_price) values (%s, %s)",
                                                           [o_id_for_table, p_for_table])
                                            conn.commit()
                                        if SPOT_SIDE == "SELL":
                                            o_id_for_table = limit_stop_loss_order["orderId"]
                                            cursor.execute("select entry_price from long_entry where symbol = %s",
                                                           [SPOT_SYMBOL])
                                            r_3 = cursor.fetchall()
                                            price_results = r_3[0][0]
                                            p_for_table = float(price_results)

                                            cursor.execute("insert into s_id_list(order_id, entry_price) values (%s, %s)",
                                                           [o_id_for_table, p_for_table])
                                            conn.commit()

                                        no_qty = False
                                        break
                                    except Exception as e:
                                        print(e)
                                        pass

                    limit_stop_loss_order_ID = limit_stop_loss_order["orderId"]
                    print(limit_stop_loss_order_ID)

                    def add_to_trade_sl():

                        while True:
                            time.sleep(4)
                            try:
                                active_order = client.get_order(symbol=SPOT_SYMBOL, orderId=limit_stop_loss_order_ID)
                                active_order_status = active_order["status"]
                                if active_order_status == "FILLED":
                                    break
                            except Exception as e:
                                print(e)
                                pass
                        if active_order_status == "FILLED":
                            enter_long_sell_stop_loss_order = active_order
                            print(f"enter long sell stop loss order={enter_long_sell_stop_loss_order}")
                        else:
                            check_for_partial = client.get_order(symbol=SPOT_SYMBOL, orderId=limit_stop_loss_order_ID)
                            if check_for_partial["status"] == "PARTIALLY_FILLED":
                                enter_long_sell_stop_loss_order = check_for_partial
                            check_for_cancel = client.get_order(symbol=SPOT_SYMBOL, orderId=limit_stop_loss_order_ID)
                            if check_for_cancel["status"] == "CANCELED" or check_for_cancel[
                                "status"] != "PARTIALLY_FILLED" or check_for_cancel["status"] != "FILLED":
                                print("Already cancelled")
                            else:
                                cancel_stop_loss_order = client.cancel_order(symbol=SPOT_SYMBOL,
                                                                             orderId=limit_stop_loss_order_ID)
                            error_occured = "Order time limit reached! Pending open oco sell orders have been cancelled"
                            print(error_occured)
                            error_occured_time = datetime.now(IST)
                            cursor.execute(
                                "insert into error_log(symbol, order_action, entry_order_type, exit_order_type, quantity, occured_time, error_description) values (%s, %s, %s, %s, %s, %s, %s)",
                                [SPOT_SYMBOL, SPOT_SIDE, SPOT_ENTRY, SPOT_EXIT, SPOT_SELL_QUANTITY, error_occured_time,
                                 error_occured])
                            conn.commit()
                        try:
                            STOP_LOSS_SELL_ORDER_ID = enter_long_sell_stop_loss_order["orderId"]
                            STOP_LOSS_SELL_ORDER_SYMBOL = enter_long_sell_stop_loss_order["symbol"]
                            STOP_LOSS_SELL_ORDER_QTY = float(enter_long_sell_stop_loss_order["executedQty"])
                            sell_cum_qty = float(enter_long_sell_stop_loss_order["cummulativeQuoteQty"])
                            TOTAL_SELL_SPEND = (sell_cum_qty / 100) * 99.9
                            TOTAL_BUY_SPEND = float(enter_long_sell_stop_loss_order["cummulativeQuoteQty"])
                            STOP_LOSS_SELL_ORDER_PRICE = round((float(
                                enter_long_sell_stop_loss_order["cummulativeQuoteQty"]) / float(
                                enter_long_sell_stop_loss_order["executedQty"])), 3)
                            STOP_LOSS_SELL_ORDER_ACTION = enter_long_sell_stop_loss_order["side"]
                            STOP_LOSS_SELL_ORDER_TYPE = enter_long_sell_stop_loss_order["type"]
                            sell_order_executed_time = datetime.now(IST)

                            execution = "Executed for Stop Loss"

                            if req_position_type == "Enter_long":
                                cursor.execute("select total_spend from id_list where order_id = %s", [BUY_ORDER_ID])
                                r_2 = cursor.fetchall()
                                price_results = r_2[0][0]
                                total_buy_spend = float(price_results)

                                STOP_LOSS_SELL_PNL = round((TOTAL_SELL_SPEND - total_buy_spend), 2)
                                stop_loss_sell_per = (STOP_LOSS_SELL_PNL / total_buy_spend) * 100
                                STOP_LOSS_SELL_PNL_PERCENTAGE = str((round(stop_loss_sell_per, 2))) + "%"

                                cursor.execute(sql.SQL(
                                    "insert into trade_log(date_time, symbol, order_id, order_action, order_type, executed_price, executed_qty, execution, pnl, percentage) values (%s, %s, %s, %s, %s, %s, %s, %s, %s,%s)"),
                                    [sell_order_executed_time, STOP_LOSS_SELL_ORDER_SYMBOL, STOP_LOSS_SELL_ORDER_ID,
                                     STOP_LOSS_SELL_ORDER_ACTION, STOP_LOSS_SELL_ORDER_TYPE, STOP_LOSS_SELL_ORDER_PRICE,
                                     STOP_LOSS_SELL_ORDER_QTY, execution, STOP_LOSS_SELL_PNL, STOP_LOSS_SELL_PNL_PERCENTAGE])
                                conn.commit()

                            if req_position_type == "Exit_long":
                                cursor.execute("select qty from long_entry where symbol = %s", [SPOT_SYMBOL])
                                r_3 = cursor.fetchall()
                                price_results = r_3[0][0]
                                previous_long_entry_qty = float(price_results)
                                print(f"previous_long_entry_qty = {previous_long_entry_qty}")

                                cursor.execute("select total_spend from long_entry where symbol = %s", [SPOT_SYMBOL])
                                r_3 = cursor.fetchall()
                                price_results = r_3[0][0]
                                previous_long_entry_spend = float(price_results)
                                print(f"previous_long_entry_spend = {previous_long_entry_spend}")

                                proportional_buy_spend = (
                                                                     previous_long_entry_spend / previous_long_entry_qty) * STOP_LOSS_SELL_ORDER_QTY
                                STOP_LOSS_SELL_PNL = round((TOTAL_SELL_SPEND - proportional_buy_spend), 2)
                                sl_sell_per = (STOP_LOSS_SELL_PNL / proportional_buy_spend) * 100
                                STOP_LOSS_SELL_PNL_PERCENTAGE = str((round(sl_sell_per, 2))) + "%"

                                cursor.execute(sql.SQL(
                                    "insert into trade_log(date_time, symbol, order_id, order_action, order_type, executed_price, executed_qty, execution, pnl, percentage) values (%s, %s, %s, %s, %s, %s, %s, %s, %s,%s)"),
                                               [sell_order_executed_time, STOP_LOSS_SELL_ORDER_SYMBOL,
                                                STOP_LOSS_SELL_ORDER_ID, STOP_LOSS_SELL_ORDER_ACTION,
                                                STOP_LOSS_SELL_ORDER_TYPE, STOP_LOSS_SELL_ORDER_PRICE,
                                                STOP_LOSS_SELL_ORDER_QTY, execution, STOP_LOSS_SELL_PNL,
                                                STOP_LOSS_SELL_PNL_PERCENTAGE])
                                conn.commit()

                            if req_position_type == "Enter_short":

                                cursor.execute("select exists (select 1 from short_entry)")
                                r_1 = cursor.fetchall()
                                live_r = r_1[0][0]

                                if live_r == False:
                                    cursor.execute(sql.SQL(
                                        "insert into short_entry(order_id, entry_price, total_spend, symbol, qty) values (%s, %s, %s, %s, %s)"),
                                        [STOP_LOSS_SELL_ORDER_ID, STOP_LOSS_SELL_ORDER_PRICE, TOTAL_SELL_SPEND,
                                         STOP_LOSS_SELL_ORDER_SYMBOL, STOP_LOSS_SELL_ORDER_QTY])
                                    conn.commit()
                                if live_r == True:
                                    cursor.execute(
                                        "update short_entry set order_id = %s, entry_price = %s, total_spend = %s, symbol = %s, qty = %s",
                                        [STOP_LOSS_SELL_ORDER_ID, STOP_LOSS_SELL_ORDER_PRICE, TOTAL_SELL_SPEND,
                                         STOP_LOSS_SELL_ORDER_SYMBOL, STOP_LOSS_SELL_ORDER_QTY])
                                    conn.commit()
                                    print("Records inserted")

                                cursor.execute(sql.SQL(
                                    "insert into trade_log(date_time, symbol, order_id, order_action, order_type, executed_price, executed_qty,execution) values (%s, %s, %s, %s, %s, %s, %s,%s)"),
                                    [sell_order_executed_time, STOP_LOSS_SELL_ORDER_SYMBOL, STOP_LOSS_SELL_ORDER_ID,
                                     STOP_LOSS_SELL_ORDER_ACTION, STOP_LOSS_SELL_ORDER_TYPE, STOP_LOSS_SELL_ORDER_PRICE,
                                     STOP_LOSS_SELL_ORDER_QTY,execution])
                                conn.commit()

                            if req_position_type == "Exit_short":
                                cursor.execute("select total_spend from short_entry where symbol = %s", [SPOT_SYMBOL])
                                r_3 = cursor.fetchall()
                                price_results = r_3[0][0]
                                previous_short_entry_income = float(price_results)
                                print(f"previous_short_entry_price = {previous_short_entry_income}")

                                cursor.execute("select qty from short_entry where symbol = %s", [SPOT_SYMBOL])
                                r_3 = cursor.fetchall()
                                price_results = r_3[0][0]
                                previous_short_entry_qty = float(price_results)
                                print(f"previous_short_entry_price = {previous_short_entry_qty}")

                                actual_sell_income = (previous_short_entry_income / 100) * 99.9
                                proportional_sell_income = (
                                                                       actual_sell_income / previous_short_entry_qty) * STOP_LOSS_SELL_ORDER_QTY
                                STOP_LOSS_SELL_PNL = round((proportional_sell_income - TOTAL_BUY_SPEND), 2)
                                sl_sell_per = (STOP_LOSS_SELL_PNL / proportional_sell_income) * 100
                                STOP_LOSS_SELL_PNL_PERCENTAGE = str((round(sl_sell_per, 2))) + "%"

                                cursor.execute(sql.SQL(
                                    "insert into trade_log(date_time, symbol, order_id, order_action, order_type, executed_price, executed_qty, execution, pnl, percentage) values (%s, %s, %s, %s, %s, %s, %s, %s, %s,%s)"),
                                    [sell_order_executed_time, STOP_LOSS_SELL_ORDER_SYMBOL, STOP_LOSS_SELL_ORDER_ID,
                                     STOP_LOSS_SELL_ORDER_ACTION, STOP_LOSS_SELL_ORDER_TYPE, STOP_LOSS_SELL_ORDER_PRICE,
                                     STOP_LOSS_SELL_ORDER_QTY, execution, STOP_LOSS_SELL_PNL, STOP_LOSS_SELL_PNL_PERCENTAGE])
                                conn.commit()

                        except Exception as e:
                            print(e)

                    t20 = threading.Thread(target=add_to_trade_sl)
                    t20.start()

                def execute_limit_take_profit_order(SPOT_SIDE, req_position_type, BUY_ORDER_ID, SPOT_SYMBOL,
                                                    SPOT_SELL_QUANTITY, TAKE_PROFIT_PRICE_FINAL, SPOT_ENTRY, req_multi_tp,
                                                    req_qty_size, req_order_time_out,tp_type):
                    print(SPOT_SIDE)
                    SPOT_EXIT = "LIMIT"

                    try:
                        limit_take_proft_order = client.create_order(symbol=SPOT_SYMBOL, side=SPOT_SIDE,
                                                                     type="TAKE_PROFIT_LIMIT",
                                                                     quantity=SPOT_SELL_QUANTITY,
                                                                     price=TAKE_PROFIT_PRICE_FINAL,
                                                                     stopPrice=TAKE_PROFIT_PRICE_FINAL, timeInForce="GTC")
                        print(f"limit take profit order = {limit_take_proft_order}")

                        if SPOT_SIDE == "BUY":
                            o_id_for_table = limit_take_proft_order["orderId"]
                            cursor.execute("select entry_price from short_entry where symbol = %s", [SPOT_SYMBOL])
                            r_3 = cursor.fetchall()
                            price_results = r_3[0][0]
                            p_for_table = float(price_results)

                            cursor.execute("insert into s_id_list(order_id, entry_price) values (%s, %s)",
                                           [o_id_for_table, p_for_table])
                            conn.commit()
                        if SPOT_SIDE == "SELL":
                            o_id_for_table = limit_take_proft_order["orderId"]
                            cursor.execute("select entry_price from long_entry where symbol = %s", [SPOT_SYMBOL])
                            r_3 = cursor.fetchall()
                            price_results = r_3[0][0]
                            p_for_table = float(price_results)

                            cursor.execute("insert into s_id_list(order_id, entry_price) values (%s, %s)",
                                           [o_id_for_table, p_for_table])
                            conn.commit()


                    except Exception as e:
                        error_occured = f"{e}"
                        print(error_occured)
                        error_occured_time = datetime.now(IST)

                        cursor.execute(
                            "insert into error_log(symbol, order_action, entry_order_type, exit_order_type, quantity, occured_time, error_description) values (%s, %s, %s, %s, %s, %s, %s)",
                            [SPOT_SYMBOL, SPOT_SIDE, SPOT_ENTRY, SPOT_EXIT, SPOT_SELL_QUANTITY, error_occured_time,
                             error_occured])
                        conn.commit()

                        error = "APIError(code=-2010): Account has insufficient balance for requested action."
                        if str(e) == error and req_position_type == "Exit_long":
                            no_qty = True
                            oo_list = get_current_open_orders(SPOT_SYMBOL)

                            while no_qty == True:
                                for item in oo_list:
                                    client.cancel_order(symbol=SPOT_SYMBOL, orderId=item)
                                    try:
                                        limit_take_proft_order = client.create_order(symbol=SPOT_SYMBOL, side=SPOT_SIDE,
                                                                                     type="TAKE_PROFIT_LIMIT",
                                                                                     quantity=SPOT_SELL_QUANTITY,
                                                                                     price=TAKE_PROFIT_PRICE_FINAL,
                                                                                     stopPrice=TAKE_PROFIT_PRICE_FINAL,
                                                                                     timeInForce="GTC")
                                        print(f"limit take profit order = {limit_take_proft_order}")

                                        if SPOT_SIDE == "BUY":
                                            o_id_for_table = limit_take_proft_order["orderId"]
                                            cursor.execute("select entry_price from short_entry where symbol = %s",
                                                           [SPOT_SYMBOL])
                                            r_3 = cursor.fetchall()
                                            price_results = r_3[0][0]
                                            p_for_table = float(price_results)

                                            cursor.execute("insert into s_id_list(order_id, entry_price) values (%s, %s)",
                                                           [o_id_for_table, p_for_table])
                                            conn.commit()
                                        if SPOT_SIDE == "SELL":
                                            o_id_for_table = limit_take_proft_order["orderId"]
                                            cursor.execute("select entry_price from long_entry where symbol = %s",
                                                           [SPOT_SYMBOL])
                                            r_3 = cursor.fetchall()
                                            price_results = r_3[0][0]
                                            p_for_table = float(price_results)

                                            cursor.execute("insert into s_id_list(order_id, entry_price) values (%s, %s)",
                                                           [o_id_for_table, p_for_table])
                                            conn.commit()

                                        no_qty = False
                                        break
                                    except Exception as e:
                                        print(e)
                                        pass

                    limit_take_proft_order_ID = limit_take_proft_order["orderId"]
                    print(limit_take_proft_order_ID)

                    def add_to_trade_tp():
                        while True:
                            time.sleep(4)
                            try:
                                time.sleep(1)
                                active_order = client.get_order(symbol=SPOT_SYMBOL, orderId=limit_take_proft_order_ID)
                                active_order_status = active_order["status"]
                                if active_order_status == "FILLED":
                                    break
                            except Exception as e:
                                print(e)
                                pass
                        if active_order_status == "FILLED":
                            enter_long_take_profit_order = active_order
                            print(f"enter long take profit order = {enter_long_take_profit_order}")
                        else:
                            check_for_partial = client.get_order(symbol=SPOT_SYMBOL, orderId=limit_take_proft_order_ID)
                            if check_for_partial["status"] == "PARTIALLY_FILLED":
                                enter_long_take_profit_order = check_for_partial
                            check_for_cancel = client.get_order(symbol=SPOT_SYMBOL, orderId=limit_take_proft_order_ID)
                            if check_for_cancel["status"] == "CANCELED" or check_for_cancel[
                                "status"] != "PARTIALLY_FILLED" or check_for_cancel["status"] != "FILLED":
                                print("Already cancelled")
                            else:
                                cancel_stop_loss_order = client.cancel_order(symbol=SPOT_SYMBOL,
                                                                             orderId=limit_take_proft_order_ID)
                            error_occured = "Order time limit reached! Pending open oco sell orders have been cancelled"
                            print(error_occured)
                            error_occured_time = datetime.now(IST)
                            cursor.execute(
                                "insert into error_log(symbol, order_action, entry_order_type, exit_order_type, quantity, occured_time, error_description) values (%s, %s, %s, %s, %s, %s, %s)",
                                [SPOT_SYMBOL, SPOT_SIDE, SPOT_ENTRY, SPOT_EXIT, SPOT_SELL_QUANTITY, error_occured_time,
                                 error_occured])
                            conn.commit()

                        try:
                            TAKE_PROFIT_SELL_ORDER_ID = enter_long_take_profit_order["orderId"]
                            TAKE_PROFIT_SELL_ORDER_SYMBOL = enter_long_take_profit_order["symbol"]
                            TAKE_PROFIT_SELL_ORDER_QTY = float(enter_long_take_profit_order["executedQty"])
                            sell_cum_qty = float(enter_long_take_profit_order["cummulativeQuoteQty"])
                            TOTAL_SELL_SPEND = (sell_cum_qty / 100) * 99.9
                            TOTAL_BUY_SPEND = float(enter_long_take_profit_order["cummulativeQuoteQty"])
                            TAKE_PROFIT_SELL_ORDER_PRICE = round((float(
                                enter_long_take_profit_order["cummulativeQuoteQty"]) / float(
                                enter_long_take_profit_order["executedQty"])), 3)
                            TAKE_PROFIT_SELL_ORDER_ACTION = enter_long_take_profit_order["side"]
                            TAKE_PROFIT_SELL_ORDER_TYPE = enter_long_take_profit_order["type"]
                            sell_order_executed_time = datetime.now(IST)

                            if tp_type == "None":
                                execution = "Executed for Take Profit"
                            if tp_type == "One":
                                execution = "Executed for Take Profit 1"
                            if tp_type == "Two":
                                execution = "Executed for Take Profit 2"
                            if tp_type == "Three":
                                execution = "Executed for Take Profit 3"

                            if req_position_type == "Enter_long":
                                cursor.execute("select total_spend from id_list where order_id = %s", [BUY_ORDER_ID])
                                r_2 = cursor.fetchall()
                                price_results = r_2[0][0]
                                total_buy_spend = float(price_results)

                                if req_multi_tp == "No":
                                    TAKE_PROFIT_SELL_PNL = round((TOTAL_SELL_SPEND - total_buy_spend), 2)
                                    take_profit_sell_per = (TAKE_PROFIT_SELL_PNL / total_buy_spend) * 100
                                    TAKE_PROFIT_SELL_PNL_PERCENTAGE = str((round(take_profit_sell_per, 2))) + "%"
                                if req_multi_tp == "Yes":
                                    buy_spend_per = float(total_buy_spend) * float(req_qty_size)
                                    TAKE_PROFIT_SELL_PNL = round((TOTAL_SELL_SPEND - buy_spend_per), 2)
                                    take_profit_sell_per = (TAKE_PROFIT_SELL_PNL / buy_spend_per) * 100
                                    TAKE_PROFIT_SELL_PNL_PERCENTAGE = str((round(take_profit_sell_per, 2))) + "%"

                                cursor.execute(sql.SQL(
                                    "insert into trade_log(date_time, symbol, order_id, order_action, order_type, executed_price, executed_qty, execution, pnl, percentage) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"),
                                    [sell_order_executed_time, TAKE_PROFIT_SELL_ORDER_SYMBOL, TAKE_PROFIT_SELL_ORDER_ID,
                                     TAKE_PROFIT_SELL_ORDER_ACTION, TAKE_PROFIT_SELL_ORDER_TYPE,
                                     TAKE_PROFIT_SELL_ORDER_PRICE,
                                     TAKE_PROFIT_SELL_ORDER_QTY, execution, TAKE_PROFIT_SELL_PNL, TAKE_PROFIT_SELL_PNL_PERCENTAGE])
                                conn.commit()

                            if req_position_type == "Exit_long":
                                cursor.execute("select qty from long_entry where symbol = %s", [SPOT_SYMBOL])
                                r_3 = cursor.fetchall()
                                price_results = r_3[0][0]
                                previous_long_entry_qty = float(price_results)
                                print(f"previous_long_entry_qty = {previous_long_entry_qty}")

                                cursor.execute("select total_spend from long_entry where symbol = %s", [SPOT_SYMBOL])
                                r_3 = cursor.fetchall()
                                price_results = r_3[0][0]
                                previous_long_entry_spend = float(price_results)
                                print(f"previous_long_entry_spend = {previous_long_entry_spend}")

                                proportional_buy_spend = (
                                                                     previous_long_entry_spend / previous_long_entry_qty) * TAKE_PROFIT_SELL_ORDER_QTY
                                TAKE_PROFIT_SELL_PNL = round((TOTAL_SELL_SPEND - proportional_buy_spend), 2)
                                tp_sell_per = (TAKE_PROFIT_SELL_PNL / proportional_buy_spend) * 100
                                TAKE_PROFIT_SELL_PNL_PERCENTAGE = str((round(tp_sell_per, 2))) + "%"

                                cursor.execute(sql.SQL(
                                    "insert into trade_log(date_time, symbol, order_id, order_action, order_type, executed_price, executed_qty, execution, pnl, percentage) values (%s, %s, %s, %s, %s, %s, %s, %s, %s,%s)"),
                                               [sell_order_executed_time, TAKE_PROFIT_SELL_ORDER_SYMBOL,
                                                TAKE_PROFIT_SELL_ORDER_ID, TAKE_PROFIT_SELL_ORDER_ACTION,
                                                TAKE_PROFIT_SELL_ORDER_TYPE, TAKE_PROFIT_SELL_ORDER_PRICE,
                                                TAKE_PROFIT_SELL_ORDER_QTY, execution, TAKE_PROFIT_SELL_PNL,
                                                TAKE_PROFIT_SELL_PNL_PERCENTAGE])
                                conn.commit()

                            if req_position_type == "Enter_short":

                                cursor.execute("select exists (select 1 from short_entry)")
                                r_1 = cursor.fetchall()
                                live_r = r_1[0][0]

                                if live_r == False:
                                    cursor.execute(sql.SQL(
                                        "insert into short_entry(order_id, entry_price, total_spend, symbol, qty) values (%s, %s, %s, %s, %s)"),
                                        [TAKE_PROFIT_SELL_ORDER_ID, TAKE_PROFIT_SELL_ORDER_PRICE, TOTAL_SELL_SPEND,
                                         TAKE_PROFIT_SELL_ORDER_SYMBOL, TAKE_PROFIT_SELL_ORDER_QTY])
                                    conn.commit()
                                if live_r == True:
                                    cursor.execute(
                                        "update short_entry set order_id = %s, entry_price = %s, total_spend = %s, symbol = %s, qty = %s",
                                        [TAKE_PROFIT_SELL_ORDER_ID, TAKE_PROFIT_SELL_ORDER_PRICE, TOTAL_SELL_SPEND,
                                         TAKE_PROFIT_SELL_ORDER_SYMBOL, TAKE_PROFIT_SELL_ORDER_QTY])
                                    conn.commit()
                                    print("Records inserted")

                                cursor.execute(sql.SQL(
                                    "insert into trade_log(date_time, symbol, order_id, order_action, order_type, executed_price, executed_qty,execution) values (%s, %s, %s, %s, %s, %s, %s,%s)"),
                                    [sell_order_executed_time, TAKE_PROFIT_SELL_ORDER_SYMBOL, TAKE_PROFIT_SELL_ORDER_ID,
                                     TAKE_PROFIT_SELL_ORDER_ACTION, TAKE_PROFIT_SELL_ORDER_TYPE,
                                     TAKE_PROFIT_SELL_ORDER_PRICE,
                                     TAKE_PROFIT_SELL_ORDER_QTY,execution])
                                conn.commit()

                            if req_position_type == "Exit_short":
                                cursor.execute("select total_spend from short_entry where symbol = %s", [SPOT_SYMBOL])
                                r_3 = cursor.fetchall()
                                price_results = r_3[0][0]
                                previous_short_entry_income = float(price_results)
                                print(f"previous_short_entry_price = {previous_short_entry_income}")

                                cursor.execute("select qty from short_entry where symbol = %s", [SPOT_SYMBOL])
                                r_3 = cursor.fetchall()
                                price_results = r_3[0][0]
                                previous_short_entry_qty = float(price_results)
                                print(f"previous_short_entry_price = {previous_short_entry_qty}")

                                actual_sell_income = (previous_short_entry_income / 100) * 99.9
                                proportional_sell_income = (
                                                                       actual_sell_income / previous_short_entry_qty) * TAKE_PROFIT_SELL_ORDER_QTY
                                TAKE_PROFIT_SELL_PNL = round((proportional_sell_income - TOTAL_BUY_SPEND), 2)
                                tp_sell_per = (TAKE_PROFIT_SELL_PNL / proportional_sell_income) * 100
                                TAKE_PROFIT_SELL_PNL_PERCENTAGE = str((round(tp_sell_per, 2))) + "%"

                                cursor.execute(sql.SQL(
                                    "insert into trade_log(date_time, symbol, order_id, order_action, order_type, executed_price, executed_qty, execution, pnl, percentage) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"),
                                    [sell_order_executed_time, TAKE_PROFIT_SELL_ORDER_SYMBOL, TAKE_PROFIT_SELL_ORDER_ID,
                                     TAKE_PROFIT_SELL_ORDER_ACTION, TAKE_PROFIT_SELL_ORDER_TYPE,
                                     TAKE_PROFIT_SELL_ORDER_PRICE,
                                     TAKE_PROFIT_SELL_ORDER_QTY, execution, TAKE_PROFIT_SELL_PNL, TAKE_PROFIT_SELL_PNL_PERCENTAGE])
                                conn.commit()

                        except Exception as e:
                            print(e)

                    t21 = threading.Thread(target=add_to_trade_tp)
                    t21.start()

                def proceed_enter_long(SPOT_BUY_QUANTITY, SPOT_SYMBOL, SPOT_ENTRY, req_long_stop_loss_percent,
                                       req_long_take_profit_percent, req_multi_tp, req_tp1_percent, req_tp2_percent,
                                       req_tp3_percent, req_tp1_qty_size, req_tp2_qty_size, req_tp3_qty_size,
                                       req_order_time_out):
                    SPOT_EXIT = "NA"
                    if SPOT_ENTRY == "MARKET":
                        try:
                            enter_long_buy_order = client.create_order(symbol=SPOT_SYMBOL, side="BUY", type=SPOT_ENTRY,
                                                                       quantity=SPOT_BUY_QUANTITY)
                            time.sleep(5)
                            print(f"enter_long_buy_order = {enter_long_buy_order}")
                        except Exception as e:
                            error_occured = f"{e}"
                            print(error_occured)
                            error_occured_time = datetime.now(IST)

                            cursor.execute(
                                "insert into error_log(symbol, order_action, entry_order_type, exit_order_type, quantity, occured_time, error_description) values (%s, %s, %s, %s, %s, %s, %s)",
                                [SPOT_SYMBOL, "BUY", SPOT_ENTRY, SPOT_EXIT, SPOT_BUY_QUANTITY, error_occured_time,
                                 error_occured])
                            conn.commit()

                    elif SPOT_ENTRY == "LIMIT":
                        prices = client.get_all_tickers()
                        for ticker in prices:
                            if ticker["symbol"] == SPOT_SYMBOL:
                                last_price = float(ticker["price"])
                                break

                        try:
                            limit_buy_order = client.order_limit_buy(symbol=SPOT_SYMBOL, quantity=SPOT_BUY_QUANTITY,
                                                                     price=last_price)
                            print(f"limit_buy_order = {limit_buy_order}")
                            limit_order_id = limit_buy_order["orderId"]
                        except Exception as e:
                            error_occured = f"{e}"
                            print(error_occured)
                            error_occured_time = datetime.now(IST)

                            cursor.execute(
                                "insert into error_log(symbol, order_action, entry_order_type, exit_order_type, quantity, occured_time, error_description) values (%s, %s, %s, %s, %s, %s, %s)",
                                [SPOT_SYMBOL, "BUY", SPOT_ENTRY, SPOT_EXIT, SPOT_BUY_QUANTITY, error_occured_time,
                                 error_occured])
                            conn.commit()

                        # Loop and check if entry order is filled
                        entry_order_timeout_start = time.time()

                        while time.time() < (entry_order_timeout_start + req_order_time_out):
                            try:
                                active_order = client.get_order(symbol=SPOT_SYMBOL, orderId=limit_order_id)
                                active_order_status = active_order["status"]
                                if active_order_status == "FILLED":
                                    break
                            except Exception as e:
                                print(e)
                                pass
                        if active_order_status == "FILLED":
                            enter_long_buy_order = active_order
                            print(f"enter long liit buy order = {enter_long_buy_order}")
                        else:
                            check_for_partial = client.get_order(symbol=SPOT_SYMBOL, orderId=limit_order_id)
                            if check_for_partial["status"] == "PARTIALLY_FILLED":
                                enter_long_buy_order = check_for_partial
                            check_for_cancel = client.get_order(symbol=SPOT_SYMBOL, orderId=limit_order_id)
                            if check_for_cancel["status"] == "CANCELED" or check_for_cancel[
                                "status"] != "PARTIALLY_FILLED" or check_for_cancel["status"] != "FILLED":
                                print("Already cancelled")
                            else:
                                cancel_limit_order = client.cancel_order(symbol=SPOT_SYMBOL, orderId=limit_order_id)
                            error_occured = "Order time limit reached! Pending open limit orders has been cancelled"
                            print(error_occured)
                            error_occured_time = datetime.now(IST)
                            cursor.execute(
                                "insert into error_log(symbol, order_action, entry_order_type, exit_order_type, quantity, occured_time, error_description) values (%s, %s, %s, %s, %s, %s, %s)",
                                [SPOT_SYMBOL, "BUY", SPOT_ENTRY, SPOT_EXIT, SPOT_BUY_QUANTITY, error_occured_time,
                                 error_occured])
                            conn.commit()

                    try:

                        BUY_ORDER_ID = enter_long_buy_order["orderId"]
                        BUY_ORDER_SYMBOL = enter_long_buy_order["symbol"]
                        ask_qty = float(enter_long_buy_order["executedQty"])
                        commision_in_coin = 0
                        try:
                            for fill in enter_long_buy_order["fills"]:
                                comm = float(fill["commission"])
                                commision_in_coin += comm
                        except:
                            commision_in_coin = ask_qty * 0.001
                        BUY_ORDER_QTY = ask_qty - commision_in_coin
                        TOTAL_BUY_SPEND = float(enter_long_buy_order["cummulativeQuoteQty"])
                        print(f"Total buy spend = {TOTAL_BUY_SPEND}")
                        BUY_ORDER_PRICE = round((float(enter_long_buy_order["cummulativeQuoteQty"]) / float(
                            enter_long_buy_order["executedQty"])), 3)
                        BUY_ORDER_ACTION = enter_long_buy_order["side"]
                        BUY_ORDER_TYPE = enter_long_buy_order["type"]
                        buy_order_executed_time = datetime.now(IST)

                        if BUY_ORDER_TYPE == "MARKET":
                            execution = "Entry as Market"
                        if BUY_ORDER_TYPE == "LIMIT":
                            execution = "Entry as Limit"

                        cursor.execute(
                            f"""INSERT INTO id_list (order_id, entry_price, total_spend) VALUES ({BUY_ORDER_ID},{BUY_ORDER_PRICE},{TOTAL_BUY_SPEND})""")
                        conn.commit()
                        print("Records inserted")

                        cursor.execute("select exists (select 1 from long_entry)")
                        r_1 = cursor.fetchall()
                        live_r = r_1[0][0]

                        if live_r == False:
                            cursor.execute(sql.SQL(
                                "insert into long_entry(order_id, entry_price, total_spend, symbol, qty) values (%s, %s, %s, %s, %s)"),
                                [BUY_ORDER_ID, BUY_ORDER_PRICE, TOTAL_BUY_SPEND, BUY_ORDER_SYMBOL, BUY_ORDER_QTY])
                            conn.commit()
                        if live_r == True:
                            cursor.execute(
                                "update long_entry set order_id = %s, entry_price = %s, total_spend = %s, symbol = %s, qty = %s",
                                [BUY_ORDER_ID, BUY_ORDER_PRICE, TOTAL_BUY_SPEND, BUY_ORDER_SYMBOL, BUY_ORDER_QTY])
                            conn.commit()
                            print("Records inserted")

                        cursor.execute(sql.SQL(
                            "insert into trade_log(date_time, symbol, order_id, order_action, order_type, executed_price, executed_qty,execution) values (%s, %s, %s, %s, %s, %s, %s,%s)"),
                                       [buy_order_executed_time, BUY_ORDER_SYMBOL, BUY_ORDER_ID, BUY_ORDER_ACTION,
                                        BUY_ORDER_TYPE, BUY_ORDER_PRICE, BUY_ORDER_QTY,execution])
                        conn.commit()

                        entry_price = BUY_ORDER_PRICE
                        print(f"entry price = {entry_price}")

                        if req_long_stop_loss_percent > 0 or req_long_take_profit_percent > 0 or req_multi_tp == "Yes":
                            SPOT_SIDE = "SELL"

                            long_stop_loss_bp = entry_price - (entry_price * req_long_stop_loss_percent)

                            long_take_profit_bp = entry_price + (entry_price * req_long_take_profit_percent)

                            STOP_LOSS_PRICE_FINAL = cal_price_with_precision(SPOT_SYMBOL=SPOT_SYMBOL,
                                                                             input_price=long_stop_loss_bp)
                            print(f"Stop loss price final = {STOP_LOSS_PRICE_FINAL}")

                            TAKE_PROFIT_PRICE_FINAL = cal_price_with_precision(SPOT_SYMBOL=SPOT_SYMBOL,
                                                                               input_price=long_take_profit_bp)
                            print(f"Take profit price final = {TAKE_PROFIT_PRICE_FINAL}")

                            SPOT_SELL_QUANTITY = calculate_sell_qty_with_precision(SPOT_SYMBOL=SPOT_SYMBOL,
                                                                                   buy_qty=BUY_ORDER_QTY)
                            print(SPOT_SELL_QUANTITY)

                            if req_multi_tp == "No":
                                if req_long_stop_loss_percent > 0 and req_long_take_profit_percent > 0:
                                    execute_limit_oco_order(SPOT_SIDE=SPOT_SIDE, req_position_type="Enter_long",
                                                            BUY_ORDER_ID=BUY_ORDER_ID, SPOT_SYMBOL=SPOT_SYMBOL,
                                                            SPOT_SELL_QUANTITY=SPOT_SELL_QUANTITY,
                                                            TAKE_PROFIT_PRICE_FINAL=TAKE_PROFIT_PRICE_FINAL,
                                                            STOP_LOSS_PRICE_FINAL=STOP_LOSS_PRICE_FINAL,
                                                            SPOT_ENTRY=SPOT_ENTRY, req_multi_tp=req_multi_tp,
                                                            req_qty_size=0, req_order_time_out=req_order_time_out,tp_type="None")
                                elif req_long_stop_loss_percent > 0 and (
                                        req_long_take_profit_percent == "" or req_long_take_profit_percent == 0):
                                    execute_limit_stop_loss_order(SPOT_SIDE=SPOT_SIDE, req_position_type="Enter_long",
                                                                  BUY_ORDER_ID=BUY_ORDER_ID, SPOT_SYMBOL=SPOT_SYMBOL,
                                                                  SPOT_SELL_QUANTITY=SPOT_SELL_QUANTITY,
                                                                  STOP_LOSS_PRICE_FINAL=STOP_LOSS_PRICE_FINAL,
                                                                  SPOT_ENTRY=SPOT_ENTRY,
                                                                  req_order_time_out=req_order_time_out)
                                elif req_long_take_profit_percent > 0 and (
                                        req_long_stop_loss_percent == "" or req_long_stop_loss_percent == 0):
                                    execute_limit_take_profit_order(SPOT_SIDE=SPOT_SIDE, req_position_type="Enter_long",
                                                                    BUY_ORDER_ID=BUY_ORDER_ID, SPOT_SYMBOL=SPOT_SYMBOL,
                                                                    SPOT_SELL_QUANTITY=SPOT_SELL_QUANTITY,
                                                                    TAKE_PROFIT_PRICE_FINAL=TAKE_PROFIT_PRICE_FINAL,
                                                                    SPOT_ENTRY=SPOT_ENTRY, req_multi_tp=req_multi_tp,
                                                                    req_qty_size=0, req_order_time_out=req_order_time_out,tp_type="None")

                            print(f"BUY ORDER QTY = {BUY_ORDER_QTY}")
                            print(f"SIZE={req_tp1_qty_size}")
                            if req_multi_tp == "Yes":
                                SELLABLE_1 = calculate_sell_qty_with_precision(SPOT_SYMBOL,
                                                                               (BUY_ORDER_QTY * req_tp1_qty_size))
                                print(f"Sellable qty_1 = {SELLABLE_1}")
                                SELLABLE_2 = calculate_sell_qty_with_precision(SPOT_SYMBOL,
                                                                               (BUY_ORDER_QTY * req_tp2_qty_size))
                                print(f"Sellable qty_2 = {SELLABLE_2}")
                                SELLABLE_3 = calculate_sell_qty_with_precision(SPOT_SYMBOL,
                                                                               (BUY_ORDER_QTY * req_tp3_qty_size))
                                print(f"Sellable qty_3 = {SELLABLE_3}")

                                long_take_profit_bp_1 = entry_price + (entry_price * req_tp1_percent)
                                long_take_profit_bp_2 = entry_price + (entry_price * req_tp2_percent)
                                long_take_profit_bp_3 = entry_price + (entry_price * req_tp3_percent)
                                TAKE_PROFIT_PRICE_FINAL_1 = cal_price_with_precision(SPOT_SYMBOL=SPOT_SYMBOL,
                                                                                     input_price=long_take_profit_bp_1)
                                TAKE_PROFIT_PRICE_FINAL_2 = cal_price_with_precision(SPOT_SYMBOL=SPOT_SYMBOL,
                                                                                     input_price=long_take_profit_bp_2)
                                TAKE_PROFIT_PRICE_FINAL_3 = cal_price_with_precision(SPOT_SYMBOL=SPOT_SYMBOL,
                                                                                     input_price=long_take_profit_bp_3)
                                print(f"Take profit price final_1 = {TAKE_PROFIT_PRICE_FINAL_1}")
                                print(f"Take profit price final_2 = {TAKE_PROFIT_PRICE_FINAL_2}")
                                print(f"Take profit price final_3 = {TAKE_PROFIT_PRICE_FINAL_3}")

                                if req_long_stop_loss_percent > 0 and (
                                        req_tp1_percent > 0 or req_tp2_percent > 0 or req_tp3_percent > 0):
                                    if req_tp1_percent > 0:
                                        t1 = threading.Thread(target=lambda: execute_limit_oco_order(SPOT_SIDE=SPOT_SIDE,
                                                                                                     req_position_type="Enter_long",
                                                                                                     BUY_ORDER_ID=BUY_ORDER_ID,
                                                                                                     SPOT_SYMBOL=SPOT_SYMBOL,
                                                                                                     SPOT_SELL_QUANTITY=SELLABLE_1,
                                                                                                     TAKE_PROFIT_PRICE_FINAL=TAKE_PROFIT_PRICE_FINAL_1,
                                                                                                     STOP_LOSS_PRICE_FINAL=STOP_LOSS_PRICE_FINAL,
                                                                                                     SPOT_ENTRY=SPOT_ENTRY,
                                                                                                     req_multi_tp=req_multi_tp,
                                                                                                     req_qty_size=req_tp1_qty_size,
                                                                                                     req_order_time_out=req_order_time_out,
                                                                                                     tp_type="One"))
                                        t1.start()
                                    if req_tp2_percent > 0:
                                        t2 = threading.Thread(target=lambda: execute_limit_oco_order(SPOT_SIDE=SPOT_SIDE,
                                                                                                     req_position_type="Enter_long",
                                                                                                     BUY_ORDER_ID=BUY_ORDER_ID,
                                                                                                     SPOT_SYMBOL=SPOT_SYMBOL,
                                                                                                     SPOT_SELL_QUANTITY=SELLABLE_2,
                                                                                                     TAKE_PROFIT_PRICE_FINAL=TAKE_PROFIT_PRICE_FINAL_2,
                                                                                                     STOP_LOSS_PRICE_FINAL=STOP_LOSS_PRICE_FINAL,
                                                                                                     SPOT_ENTRY=SPOT_ENTRY,
                                                                                                     req_multi_tp=req_multi_tp,
                                                                                                     req_qty_size=req_tp2_qty_size,
                                                                                                     req_order_time_out=req_order_time_out,tp_type="Two"))
                                        t2.start()
                                    if req_tp3_percent > 0:
                                        t2 = threading.Thread(target=lambda: execute_limit_oco_order(SPOT_SIDE=SPOT_SIDE,
                                                                                                     req_position_type="Enter_long",
                                                                                                     BUY_ORDER_ID=BUY_ORDER_ID,
                                                                                                     SPOT_SYMBOL=SPOT_SYMBOL,
                                                                                                     SPOT_SELL_QUANTITY=SELLABLE_3,
                                                                                                     TAKE_PROFIT_PRICE_FINAL=TAKE_PROFIT_PRICE_FINAL_3,
                                                                                                     STOP_LOSS_PRICE_FINAL=STOP_LOSS_PRICE_FINAL,
                                                                                                     SPOT_ENTRY=SPOT_ENTRY,
                                                                                                     req_multi_tp=req_multi_tp,
                                                                                                     req_qty_size=req_tp3_qty_size,
                                                                                                     req_order_time_out=req_order_time_out,tp_type="Three"))
                                        t2.start()

                                elif req_long_stop_loss_percent > 0 and (
                                        req_tp1_percent == 0 and req_tp2_percent == 0 and req_tp3_percent == 0):
                                    execute_limit_stop_loss_order(SPOT_SIDE=SPOT_SIDE, req_position_type="Enter_long",
                                                                  BUY_ORDER_ID=BUY_ORDER_ID, SPOT_SYMBOL=SPOT_SYMBOL,
                                                                  SPOT_SELL_QUANTITY=SPOT_SELL_QUANTITY,
                                                                  STOP_LOSS_PRICE_FINAL=STOP_LOSS_PRICE_FINAL,
                                                                  SPOT_ENTRY=SPOT_ENTRY,
                                                                  req_order_time_out=req_order_time_out)

                                elif (req_tp1_percent > 0 or req_tp2_percent > 0 or req_tp3_percent > 0) and (
                                        req_long_stop_loss_percent == "" or req_long_stop_loss_percent == 0):
                                    if req_tp1_percent > 0:
                                        t1 = threading.Thread(
                                            target=lambda: execute_limit_take_profit_order(SPOT_SIDE=SPOT_SIDE,
                                                                                           req_position_type="Enter_long",
                                                                                           BUY_ORDER_ID=BUY_ORDER_ID,
                                                                                           SPOT_SYMBOL=SPOT_SYMBOL,
                                                                                           SPOT_SELL_QUANTITY=SELLABLE_1,
                                                                                           TAKE_PROFIT_PRICE_FINAL=TAKE_PROFIT_PRICE_FINAL_1,
                                                                                           SPOT_ENTRY=SPOT_ENTRY,
                                                                                           req_multi_tp=req_multi_tp,
                                                                                           req_qty_size=req_tp1_qty_size,
                                                                                           req_order_time_out=req_order_time_out,tp_type="One"))
                                        t1.start()
                                    if req_tp2_percent > 0:
                                        t2 = threading.Thread(
                                            target=lambda: execute_limit_take_profit_order(SPOT_SIDE=SPOT_SIDE,
                                                                                           req_position_type="Enter_long",
                                                                                           BUY_ORDER_ID=BUY_ORDER_ID,
                                                                                           SPOT_SYMBOL=SPOT_SYMBOL,
                                                                                           SPOT_SELL_QUANTITY=SELLABLE_2,
                                                                                           TAKE_PROFIT_PRICE_FINAL=TAKE_PROFIT_PRICE_FINAL_2,
                                                                                           SPOT_ENTRY=SPOT_ENTRY,
                                                                                           req_multi_tp=req_multi_tp,
                                                                                           req_qty_size=req_tp2_qty_size,
                                                                                           req_order_time_out=req_order_time_out,tp_type="Two"))
                                        t2.start()
                                    if req_tp3_percent > 0:
                                        t3 = threading.Thread(
                                            target=lambda: execute_limit_take_profit_order(SPOT_SIDE=SPOT_SIDE,
                                                                                           req_position_type="Enter_long",
                                                                                           BUY_ORDER_ID=BUY_ORDER_ID,
                                                                                           SPOT_SYMBOL=SPOT_SYMBOL,
                                                                                           SPOT_SELL_QUANTITY=SELLABLE_3,
                                                                                           TAKE_PROFIT_PRICE_FINAL=TAKE_PROFIT_PRICE_FINAL_3,
                                                                                           SPOT_ENTRY=SPOT_ENTRY,
                                                                                           req_multi_tp=req_multi_tp,
                                                                                           req_qty_size=req_tp2_qty_size,
                                                                                           req_order_time_out=req_order_time_out,tp_type="Three"))
                                        t3.start()


                    except Exception as e:
                        error_occured = f"{e}"
                        print(error_occured)

                def proceed_exit_long(req_position_type, SPOT_SELL_QUANTITY_EL, SPOT_SYMBOL, req_long_stop_loss_percent,
                                      req_long_take_profit_percent, req_multi_tp, req_tp1_percent, req_tp2_percent,
                                      req_tp3_percent, req_tp1_qty_size, req_tp2_qty_size, req_tp3_qty_size,
                                      req_order_time_out):
                    SPOT_ENTRY = "NA"
                    SPOT_SIDE = "SELL"

                    cursor.execute("select entry_price from long_entry where symbol = %s", [SPOT_SYMBOL])
                    r_3 = cursor.fetchall()
                    price_results = r_3[0][0]
                    previous_long_entry_price = float(price_results)
                    print(f"previous_long_entry_price= {previous_long_entry_price}")

                    if req_long_stop_loss_percent > 0 or req_long_take_profit_percent > 0 or req_multi_tp == "Yes":
                        SPOT_EXIT = "LIMIT"

                        long_stop_loss_bp = previous_long_entry_price - (
                                    previous_long_entry_price * req_long_stop_loss_percent)

                        long_take_profit_bp = previous_long_entry_price + (
                                    previous_long_entry_price * req_long_take_profit_percent)

                        STOP_LOSS_PRICE_FINAL = cal_price_with_precision(SPOT_SYMBOL=SPOT_SYMBOL,
                                                                         input_price=long_stop_loss_bp)
                        print(f"Stop loss price final = {STOP_LOSS_PRICE_FINAL}")

                        TAKE_PROFIT_PRICE_FINAL = cal_price_with_precision(SPOT_SYMBOL=SPOT_SYMBOL,
                                                                           input_price=long_take_profit_bp)
                        print(f"Take profit price final = {TAKE_PROFIT_PRICE_FINAL}")

                        BUY_ORDER_ID = 0

                        if req_multi_tp == "No":
                            if req_long_stop_loss_percent > 0 and req_long_take_profit_percent > 0:
                                execute_limit_oco_order(SPOT_SIDE=SPOT_SIDE, req_position_type=req_position_type,
                                                        BUY_ORDER_ID=BUY_ORDER_ID, SPOT_SYMBOL=SPOT_SYMBOL,
                                                        SPOT_SELL_QUANTITY=SPOT_SELL_QUANTITY_EL,
                                                        TAKE_PROFIT_PRICE_FINAL=TAKE_PROFIT_PRICE_FINAL,
                                                        STOP_LOSS_PRICE_FINAL=STOP_LOSS_PRICE_FINAL, SPOT_ENTRY=SPOT_ENTRY,
                                                        req_multi_tp=req_multi_tp, req_qty_size=0,
                                                        req_order_time_out=req_order_time_out,tp_type="None")
                            elif req_long_stop_loss_percent > 0 and (
                                    req_long_take_profit_percent == "" or req_long_take_profit_percent == 0):
                                execute_limit_stop_loss_order(SPOT_SIDE, req_position_type, BUY_ORDER_ID, SPOT_SYMBOL,
                                                              SPOT_SELL_QUANTITY_EL, STOP_LOSS_PRICE_FINAL, SPOT_ENTRY,
                                                              req_order_time_out)
                            elif req_long_take_profit_percent > 0 and (
                                    req_long_stop_loss_percent == "" or req_long_stop_loss_percent == 0):
                                execute_limit_take_profit_order(SPOT_SIDE=SPOT_SIDE, req_position_type=req_position_type,
                                                                BUY_ORDER_ID=BUY_ORDER_ID, SPOT_SYMBOL=SPOT_SYMBOL,
                                                                SPOT_SELL_QUANTITY=SPOT_SELL_QUANTITY_EL,
                                                                TAKE_PROFIT_PRICE_FINAL=TAKE_PROFIT_PRICE_FINAL,
                                                                SPOT_ENTRY=SPOT_ENTRY, req_multi_tp=req_multi_tp,
                                                                req_qty_size=0, req_order_time_out=req_order_time_out,tp_type="None")

                        if req_multi_tp == "Yes":
                            SELLABLE_1 = trunc_calculate_sell_qty_with_precision(SPOT_SYMBOL,
                                                                                 (SPOT_SELL_QUANTITY_EL * req_tp1_qty_size))
                            print(f"Sellable qty_1 = {SELLABLE_1}")
                            SELLABLE_2 = trunc_calculate_sell_qty_with_precision(SPOT_SYMBOL,
                                                                                 (SPOT_SELL_QUANTITY_EL * req_tp2_qty_size))
                            print(f"Sellable qty_2 = {SELLABLE_2}")
                            SELLABLE_3 = trunc_calculate_sell_qty_with_precision(SPOT_SYMBOL,
                                                                                 (SPOT_SELL_QUANTITY_EL * req_tp3_qty_size))
                            print(f"Sellable qty_3 = {SELLABLE_3}")

                            long_take_profit_bp_1 = previous_long_entry_price + (
                                        previous_long_entry_price * req_tp1_percent)
                            long_take_profit_bp_2 = previous_long_entry_price + (
                                        previous_long_entry_price * req_tp2_percent)
                            long_take_profit_bp_3 = previous_long_entry_price + (
                                        previous_long_entry_price * req_tp3_percent)
                            TAKE_PROFIT_PRICE_FINAL_1 = cal_price_with_precision(SPOT_SYMBOL=SPOT_SYMBOL,
                                                                                 input_price=long_take_profit_bp_1)
                            TAKE_PROFIT_PRICE_FINAL_2 = cal_price_with_precision(SPOT_SYMBOL=SPOT_SYMBOL,
                                                                                 input_price=long_take_profit_bp_2)
                            TAKE_PROFIT_PRICE_FINAL_3 = cal_price_with_precision(SPOT_SYMBOL=SPOT_SYMBOL,
                                                                                 input_price=long_take_profit_bp_3)
                            print(f"Take profit price final_1 = {TAKE_PROFIT_PRICE_FINAL_1}")
                            print(f"Take profit price final_2 = {TAKE_PROFIT_PRICE_FINAL_2}")
                            print(f"Take profit price final_3 = {TAKE_PROFIT_PRICE_FINAL_3}")

                            if req_long_stop_loss_percent > 0 and (
                                    req_tp1_percent > 0 or req_tp2_percent > 0 or req_tp3_percent > 0):
                                if req_tp1_percent > 0:
                                    t1 = threading.Thread(target=lambda: execute_limit_oco_order(SPOT_SIDE=SPOT_SIDE,
                                                                                                 req_position_type=req_position_type,
                                                                                                 BUY_ORDER_ID=BUY_ORDER_ID,
                                                                                                 SPOT_SYMBOL=SPOT_SYMBOL,
                                                                                                 SPOT_SELL_QUANTITY=SELLABLE_1,
                                                                                                 TAKE_PROFIT_PRICE_FINAL=TAKE_PROFIT_PRICE_FINAL_1,
                                                                                                 STOP_LOSS_PRICE_FINAL=STOP_LOSS_PRICE_FINAL,
                                                                                                 SPOT_ENTRY=SPOT_ENTRY,
                                                                                                 req_multi_tp=req_multi_tp,
                                                                                                 req_qty_size=req_tp1_qty_size,
                                                                                                 req_order_time_out=req_order_time_out,tp_type="One"))
                                    t1.start()
                                if req_tp2_percent > 0:
                                    t2 = threading.Thread(target=lambda: execute_limit_oco_order(SPOT_SIDE=SPOT_SIDE,
                                                                                                 req_position_type=req_position_type,
                                                                                                 BUY_ORDER_ID=BUY_ORDER_ID,
                                                                                                 SPOT_SYMBOL=SPOT_SYMBOL,
                                                                                                 SPOT_SELL_QUANTITY=SELLABLE_2,
                                                                                                 TAKE_PROFIT_PRICE_FINAL=TAKE_PROFIT_PRICE_FINAL_2,
                                                                                                 STOP_LOSS_PRICE_FINAL=STOP_LOSS_PRICE_FINAL,
                                                                                                 SPOT_ENTRY=SPOT_ENTRY,
                                                                                                 req_multi_tp=req_multi_tp,
                                                                                                 req_qty_size=req_tp2_qty_size,
                                                                                                 req_order_time_out=req_order_time_out,tp_type="Two"))
                                    t2.start()
                                if req_tp3_percent > 0:
                                    t3 = threading.Thread(target=lambda: execute_limit_oco_order(SPOT_SIDE=SPOT_SIDE,
                                                                                                 req_position_type=req_position_type,
                                                                                                 BUY_ORDER_ID=BUY_ORDER_ID,
                                                                                                 SPOT_SYMBOL=SPOT_SYMBOL,
                                                                                                 SPOT_SELL_QUANTITY=SELLABLE_3,
                                                                                                 TAKE_PROFIT_PRICE_FINAL=TAKE_PROFIT_PRICE_FINAL_3,
                                                                                                 STOP_LOSS_PRICE_FINAL=STOP_LOSS_PRICE_FINAL,
                                                                                                 SPOT_ENTRY=SPOT_ENTRY,
                                                                                                 req_multi_tp=req_multi_tp,
                                                                                                 req_qty_size=req_tp3_qty_size,
                                                                                                 req_order_time_out=req_order_time_out,tp_type="Three"))
                                    t3.start()

                            elif req_long_stop_loss_percent > 0 and (
                                    req_tp1_percent == 0 and req_tp2_percent == 0 and req_tp3_percent == 0):
                                execute_limit_stop_loss_order(SPOT_SIDE, req_position_type, BUY_ORDER_ID, SPOT_SYMBOL,
                                                              SPOT_SELL_QUANTITY_EL, STOP_LOSS_PRICE_FINAL, SPOT_ENTRY,
                                                              req_order_time_out)

                            elif (req_tp1_percent > 0 or req_tp2_percent > 0 or req_tp3_percent > 0) and (
                                    req_long_stop_loss_percent == "" or req_long_stop_loss_percent == 0):
                                if req_tp1_percent > 0:
                                    t1 = threading.Thread(
                                        target=lambda: execute_limit_take_profit_order(SPOT_SIDE=SPOT_SIDE,
                                                                                       req_position_type=req_position_type,
                                                                                       BUY_ORDER_ID=BUY_ORDER_ID,
                                                                                       SPOT_SYMBOL=SPOT_SYMBOL,
                                                                                       SPOT_SELL_QUANTITY=SELLABLE_1,
                                                                                       TAKE_PROFIT_PRICE_FINAL=TAKE_PROFIT_PRICE_FINAL_1,
                                                                                       SPOT_ENTRY=SPOT_ENTRY,
                                                                                       req_multi_tp=req_multi_tp,
                                                                                       req_qty_size=req_tp1_qty_size,
                                                                                       req_order_time_out=req_order_time_out,tp_type="One"))
                                    t1.start()
                                if req_tp2_percent > 0:
                                    t2 = threading.Thread(
                                        target=lambda: execute_limit_take_profit_order(SPOT_SIDE=SPOT_SIDE,
                                                                                       req_position_type=req_position_type,
                                                                                       BUY_ORDER_ID=BUY_ORDER_ID,
                                                                                       SPOT_SYMBOL=SPOT_SYMBOL,
                                                                                       SPOT_SELL_QUANTITY=SELLABLE_2,
                                                                                       TAKE_PROFIT_PRICE_FINAL=TAKE_PROFIT_PRICE_FINAL_2,
                                                                                       SPOT_ENTRY=SPOT_ENTRY,
                                                                                       req_multi_tp=req_multi_tp,
                                                                                       req_qty_size=req_tp2_qty_size,
                                                                                       req_order_time_out=req_order_time_out,tp_type="Two"))
                                    t2.start()
                                if req_tp3_percent > 0:
                                    t3 = threading.Thread(
                                        target=lambda: execute_limit_take_profit_order(SPOT_SIDE=SPOT_SIDE,
                                                                                       req_position_type=req_position_type,
                                                                                       BUY_ORDER_ID=BUY_ORDER_ID,
                                                                                       SPOT_SYMBOL=SPOT_SYMBOL,
                                                                                       SPOT_SELL_QUANTITY=SELLABLE_3,
                                                                                       TAKE_PROFIT_PRICE_FINAL=TAKE_PROFIT_PRICE_FINAL_3,
                                                                                       SPOT_ENTRY=SPOT_ENTRY,
                                                                                       req_multi_tp=req_multi_tp,
                                                                                       req_qty_size=req_tp2_qty_size,
                                                                                       req_order_time_out=req_order_time_out,tp_type="Three"))
                                    t3.start()


                    elif req_long_stop_loss_percent == 0 and req_long_take_profit_percent == 0 and req_multi_tp == "No":
                        SPOT_EXIT = "MARKET"
                        try:
                            exit_long_sell_order = client.create_order(symbol=SPOT_SYMBOL, side=SPOT_SIDE, type=SPOT_EXIT,
                                                                       quantity=SPOT_SELL_QUANTITY_EL)

                            time.sleep(5)
                            print(f"exit long sell order = {exit_long_sell_order}")
                        except Exception as e:
                            error_occured = f"{e}"
                            print(error_occured)
                            error_occured_time = datetime.now(IST)

                            cursor.execute(
                                "insert into error_log(symbol, order_action, entry_order_type, exit_order_type, quantity, occured_time, error_description) values (%s, %s, %s, %s, %s, %s, %s)",
                                [SPOT_SYMBOL, SPOT_SIDE, SPOT_ENTRY, SPOT_EXIT, SPOT_SELL_QUANTITY_EL, error_occured_time,
                                 error_occured])
                            conn.commit()

                            error = "APIError(code=-2010): Account has insufficient balance for requested action."
                            if str(e) == error:
                                no_qty = True
                                oo_list = get_current_open_orders(SPOT_SYMBOL)

                                while no_qty == True:
                                    for item in oo_list:
                                        client.cancel_order(symbol=SPOT_SYMBOL, orderId=item)
                                        try:
                                            exit_long_sell_order = client.create_order(symbol=SPOT_SYMBOL, side=SPOT_SIDE,
                                                                                       type=SPOT_EXIT,
                                                                                       quantity=SPOT_SELL_QUANTITY_EL)
                                            no_qty = False
                                            break
                                        except Exception as e:
                                            print(e)
                                            pass

                        try:

                            SELL_ORDER_ID = exit_long_sell_order["orderId"]
                            SELL_ORDER_SYMBOL = exit_long_sell_order["symbol"]
                            SELL_ORDER_QTY = float(exit_long_sell_order["executedQty"])
                            sell_cum_qty = float(exit_long_sell_order["cummulativeQuoteQty"])
                            TOTAL_SELL_SPEND = (sell_cum_qty / 100) * 99.9
                            print(f"Total buy spend = {TOTAL_SELL_SPEND}")
                            SELL_ORDER_PRICE = round((float(exit_long_sell_order["cummulativeQuoteQty"]) / float(
                                exit_long_sell_order["executedQty"])), 3)
                            SELL_ORDER_ACTION = exit_long_sell_order["side"]
                            SELL_ORDER_TYPE = exit_long_sell_order["type"]
                            sell_order_executed_time = datetime.now(IST)

                            execution = "Exit as Market"

                            cursor.execute("select qty from long_entry where symbol = %s", [SPOT_SYMBOL])
                            r_3 = cursor.fetchall()
                            price_results = r_3[0][0]
                            previous_long_entry_qty = float(price_results)
                            print(f"previous_long_entry_qty = {previous_long_entry_qty}")

                            cursor.execute("select total_spend from long_entry where symbol = %s", [SPOT_SYMBOL])
                            r_3 = cursor.fetchall()
                            price_results = r_3[0][0]
                            previous_long_entry_spend = float(price_results)
                            print(f"previous_long_entry_spend = {previous_long_entry_spend}")

                            proportional_buy_spend = (previous_long_entry_spend / previous_long_entry_qty) * SELL_ORDER_QTY
                            SELL_ORDER_SELL_PNL = round((TOTAL_SELL_SPEND - proportional_buy_spend), 2)
                            sell_order_pnl_per = (SELL_ORDER_SELL_PNL / proportional_buy_spend) * 100
                            SELL_ORDER_SELL_PNL_PERCENTAGE = str((round(sell_order_pnl_per, 2))) + "%"

                            cursor.execute(sql.SQL(
                                "insert into trade_log(date_time, symbol, order_id, order_action, order_type, executed_price, executed_qty, execution, pnl, percentage) values (%s, %s, %s, %s, %s, %s, %s, %s, %s,%s)"),
                                           [sell_order_executed_time, SELL_ORDER_SYMBOL, SELL_ORDER_ID, SELL_ORDER_ACTION,
                                            SELL_ORDER_TYPE, SELL_ORDER_PRICE, SELL_ORDER_QTY, execution, SELL_ORDER_SELL_PNL,
                                            SELL_ORDER_SELL_PNL_PERCENTAGE])
                            conn.commit()

                        except Exception as e:
                            error_occured = f"{e}"
                            print(error_occured)

                def proceed_enter_short(req_position_type, SPOT_SELL_QUANTITY_EL, SPOT_SYMBOL, req_short_stop_loss_percent,
                                        req_short_take_profit_percent, req_multi_tp, req_tp1_percent, req_tp2_percent,
                                        req_tp3_percent, req_tp1_qty_size, req_tp2_qty_size, req_tp3_qty_size,
                                        req_order_time_out):

                    SPOT_ENTRY = "NA"
                    SPOT_SIDE = "SELL"

                    prices = client.get_all_tickers()
                    for ticker in prices:
                        if ticker["symbol"] == SPOT_SYMBOL:
                            last_price = float(ticker["price"])
                            break

                    if req_short_stop_loss_percent > 0 or req_short_take_profit_percent > 0 or req_multi_tp == "Yes":
                        SPOT_EXIT = "LIMIT"

                        short_stop_loss_bp = last_price - (last_price * req_short_stop_loss_percent)

                        short_take_profit_bp = last_price + (last_price * req_short_take_profit_percent)

                        STOP_LOSS_PRICE_FINAL = cal_price_with_precision(SPOT_SYMBOL=SPOT_SYMBOL,
                                                                         input_price=short_stop_loss_bp)
                        print(f"Stop loss price final = {STOP_LOSS_PRICE_FINAL}")

                        TAKE_PROFIT_PRICE_FINAL = cal_price_with_precision(SPOT_SYMBOL=SPOT_SYMBOL,
                                                                           input_price=short_take_profit_bp)
                        print(f"Take profit price final = {TAKE_PROFIT_PRICE_FINAL}")

                        BUY_ORDER_ID = 0

                        if req_multi_tp == "No":
                            if req_short_stop_loss_percent > 0 and req_short_take_profit_percent > 0:
                                execute_limit_oco_order(SPOT_SIDE=SPOT_SIDE, req_position_type=req_position_type,
                                                        BUY_ORDER_ID=BUY_ORDER_ID, SPOT_SYMBOL=SPOT_SYMBOL,
                                                        SPOT_SELL_QUANTITY=SPOT_SELL_QUANTITY_EL,
                                                        TAKE_PROFIT_PRICE_FINAL=TAKE_PROFIT_PRICE_FINAL,
                                                        STOP_LOSS_PRICE_FINAL=STOP_LOSS_PRICE_FINAL, SPOT_ENTRY=SPOT_ENTRY,
                                                        req_multi_tp=req_multi_tp, req_qty_size=0,
                                                        req_order_time_out=req_order_time_out,tp_type="None")
                            elif req_short_stop_loss_percent > 0 and (
                                    req_short_take_profit_percent == "" or req_short_take_profit_percent == 0):
                                execute_limit_stop_loss_order(SPOT_SIDE, req_position_type, BUY_ORDER_ID, SPOT_SYMBOL,
                                                              SPOT_SELL_QUANTITY_EL, STOP_LOSS_PRICE_FINAL, SPOT_ENTRY,
                                                              req_order_time_out)
                            elif req_short_take_profit_percent > 0 and (
                                    req_short_stop_loss_percent == "" or req_short_stop_loss_percent == 0):
                                execute_limit_take_profit_order(SPOT_SIDE=SPOT_SIDE, req_position_type=req_position_type,
                                                                BUY_ORDER_ID=BUY_ORDER_ID, SPOT_SYMBOL=SPOT_SYMBOL,
                                                                SPOT_SELL_QUANTITY=SPOT_SELL_QUANTITY_EL,
                                                                TAKE_PROFIT_PRICE_FINAL=TAKE_PROFIT_PRICE_FINAL,
                                                                SPOT_ENTRY=SPOT_ENTRY, req_multi_tp=req_multi_tp,
                                                                req_qty_size=0, req_order_time_out=req_order_time_out,tp_type="None")

                        if req_multi_tp == "Yes":
                            SELLABLE_1 = calculate_sell_qty_with_precision(SPOT_SYMBOL,
                                                                           (SPOT_SELL_QUANTITY_EL * req_tp1_qty_size))
                            print(f"Sellable qty_1 = {SELLABLE_1}")
                            SELLABLE_2 = calculate_sell_qty_with_precision(SPOT_SYMBOL,
                                                                           (SPOT_SELL_QUANTITY_EL * req_tp2_qty_size))
                            print(f"Sellable qty_2 = {SELLABLE_2}")
                            SELLABLE_3 = calculate_sell_qty_with_precision(SPOT_SYMBOL,
                                                                           (SPOT_SELL_QUANTITY_EL * req_tp3_qty_size))
                            print(f"Sellable qty_3 = {SELLABLE_3}")

                            short_take_profit_bp_1 = last_price + (last_price * req_tp1_percent)
                            short_take_profit_bp_2 = last_price + (last_price * req_tp2_percent)
                            short_take_profit_bp_3 = last_price + (last_price * req_tp3_percent)
                            TAKE_PROFIT_PRICE_FINAL_1 = cal_price_with_precision(SPOT_SYMBOL=SPOT_SYMBOL,
                                                                                 input_price=short_take_profit_bp_1)
                            TAKE_PROFIT_PRICE_FINAL_2 = cal_price_with_precision(SPOT_SYMBOL=SPOT_SYMBOL,
                                                                                 input_price=short_take_profit_bp_2)
                            TAKE_PROFIT_PRICE_FINAL_3 = cal_price_with_precision(SPOT_SYMBOL=SPOT_SYMBOL,
                                                                                 input_price=short_take_profit_bp_3)
                            print(f"Take profit price final_1 = {TAKE_PROFIT_PRICE_FINAL_1}")
                            print(f"Take profit price final_2 = {TAKE_PROFIT_PRICE_FINAL_2}")
                            print(f"Take profit price final_3 = {TAKE_PROFIT_PRICE_FINAL_3}")

                            if req_short_stop_loss_percent > 0 and (
                                    req_tp1_percent > 0 or req_tp2_percent > 0 or req_tp3_percent > 0):
                                if req_tp1_percent > 0:
                                    t1 = threading.Thread(target=lambda: execute_limit_oco_order(SPOT_SIDE=SPOT_SIDE,
                                                                                                 req_position_type=req_position_type,
                                                                                                 BUY_ORDER_ID=BUY_ORDER_ID,
                                                                                                 SPOT_SYMBOL=SPOT_SYMBOL,
                                                                                                 SPOT_SELL_QUANTITY=SELLABLE_1,
                                                                                                 TAKE_PROFIT_PRICE_FINAL=TAKE_PROFIT_PRICE_FINAL_1,
                                                                                                 STOP_LOSS_PRICE_FINAL=STOP_LOSS_PRICE_FINAL,
                                                                                                 SPOT_ENTRY=SPOT_ENTRY,
                                                                                                 req_multi_tp=req_multi_tp,
                                                                                                 req_qty_size=req_tp1_qty_size,
                                                                                                 req_order_time_out=req_order_time_out,tp_type="One"))
                                    t1.start()
                                if req_tp2_percent > 0:
                                    t2 = threading.Thread(target=lambda: execute_limit_oco_order(SPOT_SIDE=SPOT_SIDE,
                                                                                                 req_position_type=req_position_type,
                                                                                                 BUY_ORDER_ID=BUY_ORDER_ID,
                                                                                                 SPOT_SYMBOL=SPOT_SYMBOL,
                                                                                                 SPOT_SELL_QUANTITY=SELLABLE_2,
                                                                                                 TAKE_PROFIT_PRICE_FINAL=TAKE_PROFIT_PRICE_FINAL_2,
                                                                                                 STOP_LOSS_PRICE_FINAL=STOP_LOSS_PRICE_FINAL,
                                                                                                 SPOT_ENTRY=SPOT_ENTRY,
                                                                                                 req_multi_tp=req_multi_tp,
                                                                                                 req_qty_size=req_tp2_qty_size,
                                                                                                 req_order_time_out=req_order_time_out,tp_type="Two"))
                                    t2.start()
                                if req_tp3_percent > 0:
                                    t3 = threading.Thread(target=lambda: execute_limit_oco_order(SPOT_SIDE=SPOT_SIDE,
                                                                                                 req_position_type=req_position_type,
                                                                                                 BUY_ORDER_ID=BUY_ORDER_ID,
                                                                                                 SPOT_SYMBOL=SPOT_SYMBOL,
                                                                                                 SPOT_SELL_QUANTITY=SELLABLE_3,
                                                                                                 TAKE_PROFIT_PRICE_FINAL=TAKE_PROFIT_PRICE_FINAL_3,
                                                                                                 STOP_LOSS_PRICE_FINAL=STOP_LOSS_PRICE_FINAL,
                                                                                                 SPOT_ENTRY=SPOT_ENTRY,
                                                                                                 req_multi_tp=req_multi_tp,
                                                                                                 req_qty_size=req_tp3_qty_size,
                                                                                                 req_order_time_out=req_order_time_out,tp_type="Three"))
                                    t3.start()

                            elif req_short_stop_loss_percent > 0 and (
                                    req_tp1_percent == 0 and req_tp2_percent == 0 and req_tp3_percent == 0):
                                execute_limit_stop_loss_order(SPOT_SIDE, req_position_type, BUY_ORDER_ID, SPOT_SYMBOL,
                                                              SPOT_SELL_QUANTITY_EL, STOP_LOSS_PRICE_FINAL, SPOT_ENTRY,
                                                              req_order_time_out)


                            elif (req_tp1_percent > 0 or req_tp2_percent > 0 or req_tp3_percent > 0) and (
                                    req_short_stop_loss_percent == "" or req_short_stop_loss_percent == 0):
                                if req_tp1_percent > 0:
                                    t1 = threading.Thread(
                                        target=lambda: execute_limit_take_profit_order(SPOT_SIDE=SPOT_SIDE,
                                                                                       req_position_type=req_position_type,
                                                                                       BUY_ORDER_ID=BUY_ORDER_ID,
                                                                                       SPOT_SYMBOL=SPOT_SYMBOL,
                                                                                       SPOT_SELL_QUANTITY=SELLABLE_1,
                                                                                       TAKE_PROFIT_PRICE_FINAL=TAKE_PROFIT_PRICE_FINAL_1,
                                                                                       SPOT_ENTRY=SPOT_ENTRY,
                                                                                       req_multi_tp=req_multi_tp,
                                                                                       req_qty_size=req_tp1_qty_size,
                                                                                       req_order_time_out=req_order_time_out,tp_type="One"))
                                    t1.start()
                                if req_tp2_percent > 0:
                                    t2 = threading.Thread(
                                        target=lambda: execute_limit_take_profit_order(SPOT_SIDE=SPOT_SIDE,
                                                                                       req_position_type=req_position_type,
                                                                                       BUY_ORDER_ID=BUY_ORDER_ID,
                                                                                       SPOT_SYMBOL=SPOT_SYMBOL,
                                                                                       SPOT_SELL_QUANTITY=SELLABLE_2,
                                                                                       TAKE_PROFIT_PRICE_FINAL=TAKE_PROFIT_PRICE_FINAL_2,
                                                                                       SPOT_ENTRY=SPOT_ENTRY,
                                                                                       req_multi_tp=req_multi_tp,
                                                                                       req_qty_size=req_tp2_qty_size,
                                                                                       req_order_time_out=req_order_time_out,tp_type="Two"))
                                    t2.start()
                                if req_tp3_percent > 0:
                                    t3 = threading.Thread(
                                        target=lambda: execute_limit_take_profit_order(SPOT_SIDE=SPOT_SIDE,
                                                                                       req_position_type=req_position_type,
                                                                                       BUY_ORDER_ID=BUY_ORDER_ID,
                                                                                       SPOT_SYMBOL=SPOT_SYMBOL,
                                                                                       SPOT_SELL_QUANTITY=SELLABLE_3,
                                                                                       TAKE_PROFIT_PRICE_FINAL=TAKE_PROFIT_PRICE_FINAL_3,
                                                                                       SPOT_ENTRY=SPOT_ENTRY,
                                                                                       req_multi_tp=req_multi_tp,
                                                                                       req_qty_size=req_tp2_qty_size,
                                                                                       req_order_time_out=req_order_time_out,tp_type="Three"))
                                    t3.start()



                    elif req_short_stop_loss_percent == 0 and req_short_take_profit_percent == 0 and req_multi_tp == "No":
                        SPOT_EXIT = "MARKET"
                        try:
                            exit_long_sell_order = client.create_order(symbol=SPOT_SYMBOL, side=SPOT_SIDE, type=SPOT_EXIT,
                                                                       quantity=SPOT_SELL_QUANTITY_EL)

                            time.sleep(5)
                            print(f"exit long sell order = {exit_long_sell_order}")
                        except Exception as e:
                            error_occured = f"{e}"
                            print(error_occured)
                            error_occured_time = datetime.now(IST)

                            cursor.execute(
                                "insert into error_log(symbol, order_action, entry_order_type, exit_order_type, quantity, occured_time, error_description) values (%s, %s, %s, %s, %s, %s, %s)",
                                [SPOT_SYMBOL, SPOT_SIDE, SPOT_ENTRY, SPOT_EXIT, SPOT_SELL_QUANTITY_EL, error_occured_time,
                                 error_occured])
                            conn.commit()

                        try:

                            SELL_ORDER_ID = exit_long_sell_order["orderId"]
                            SELL_ORDER_SYMBOL = exit_long_sell_order["symbol"]
                            SELL_ORDER_QTY = float(exit_long_sell_order["executedQty"])
                            TOTAL_SELL_SPEND = float(exit_long_sell_order["cummulativeQuoteQty"])
                            print(f"Total buy spend = {TOTAL_SELL_SPEND}")
                            SELL_ORDER_PRICE = round((float(exit_long_sell_order["cummulativeQuoteQty"]) / float(
                                exit_long_sell_order["executedQty"])), 3)
                            SELL_ORDER_ACTION = exit_long_sell_order["side"]
                            SELL_ORDER_TYPE = exit_long_sell_order["type"]
                            sell_order_executed_time = datetime.now(IST)

                            execution = "Enter as Market"

                            cursor.execute("select exists (select 1 from short_entry)")
                            r_1 = cursor.fetchall()
                            live_r = r_1[0][0]

                            if live_r == False:
                                cursor.execute(sql.SQL(
                                    "insert into short_entry(order_id, entry_price, total_spend, symbol, qty) values (%s, %s, %s, %s, %s)"),
                                               [SELL_ORDER_ID, SELL_ORDER_PRICE, TOTAL_SELL_SPEND, SELL_ORDER_SYMBOL,
                                                SELL_ORDER_QTY])
                                conn.commit()
                            if live_r == True:
                                cursor.execute(
                                    "update short_entry set order_id = %s, entry_price = %s, total_spend = %s, symbol = %s, qty = %s",
                                    [SELL_ORDER_ID, SELL_ORDER_PRICE, TOTAL_SELL_SPEND, SELL_ORDER_SYMBOL, SELL_ORDER_QTY])
                                conn.commit()
                                print("Records inserted")

                            cursor.execute(sql.SQL(
                                "insert into trade_log(date_time, symbol, order_id, order_action, order_type, executed_price, executed_qty,execution) values (%s, %s, %s, %s, %s, %s, %s,%s)"),
                                           [sell_order_executed_time, SELL_ORDER_SYMBOL, SELL_ORDER_ID, SELL_ORDER_ACTION,
                                            SELL_ORDER_TYPE, SELL_ORDER_PRICE, SELL_ORDER_QTY,execution])
                            conn.commit()

                        except Exception as e:
                            error_occured = f"{e}"
                            print(error_occured)

                def proceed_exit_short(req_position_type, SPOT_BUY_QUANTITY_EL, SPOT_SYMBOL, req_short_stop_loss_percent,
                                       req_short_take_profit_percent, req_multi_tp, req_tp1_percent, req_tp2_percent,
                                       req_tp3_percent, req_tp1_qty_size, req_tp2_qty_size, req_tp3_qty_size,
                                       req_order_time_out):

                    SPOT_EXIT = "NA"
                    SPOT_SIDE = "BUY"

                    if req_short_stop_loss_percent == 0 and req_short_take_profit_percent == 0 and req_multi_tp == "No":
                        SPOT_ENTRY = "MARKET"
                        try:
                            exit_short_buy_order = client.create_order(symbol=SPOT_SYMBOL, side=SPOT_SIDE, type=SPOT_ENTRY,
                                                                       quantity=SPOT_BUY_QUANTITY_EL)
                            time.sleep(5)
                            print(f"exit_short_buy_order = {exit_short_buy_order}")
                        except Exception as e:
                            error_occured = f"{e}"
                            print(error_occured)
                            error_occured_time = datetime.now(IST)

                            cursor.execute(
                                "insert into error_log(symbol, order_action, entry_order_type, exit_order_type, quantity, occured_time, error_description) values (%s, %s, %s, %s, %s, %s, %s)",
                                [SPOT_SYMBOL, SPOT_SIDE, SPOT_ENTRY, SPOT_EXIT, SPOT_BUY_QUANTITY_EL, error_occured_time,
                                 error_occured])
                            conn.commit()
                        try:
                            BUY_ORDER_ID = exit_short_buy_order["orderId"]
                            BUY_ORDER_SYMBOL = exit_short_buy_order["symbol"]
                            commision_in_coin = 0
                            ask_qty = float(exit_short_buy_order["executedQty"])
                            try:
                                for fill in exit_short_buy_order["fills"]:
                                    comm = float(fill["commission"])
                                    commision_in_coin += comm
                            except:
                                commision_in_coin = ask_qty * 0.001
                            BUY_ORDER_QTY = ask_qty - commision_in_coin
                            TOTAL_BUY_SPEND = float(exit_short_buy_order["cummulativeQuoteQty"])
                            print(f"Total buy spend = {TOTAL_BUY_SPEND}")
                            BUY_ORDER_PRICE = float(exit_short_buy_order["cummulativeQuoteQty"]) / float(
                                exit_short_buy_order["executedQty"])
                            BUY_ORDER_ACTION = exit_short_buy_order["side"]
                            BUY_ORDER_TYPE = exit_short_buy_order["type"]
                            buy_order_executed_time = datetime.now(IST)

                            execution = "Exit as Market"

                            cursor.execute("select total_spend from short_entry where symbol = %s", [SPOT_SYMBOL])
                            r_3 = cursor.fetchall()
                            price_results = r_3[0][0]
                            previous_short_entry_income = float(price_results)
                            print(f"previous_buy_income = {previous_short_entry_income}")

                            cursor.execute("select qty from short_entry where symbol = %s", [SPOT_SYMBOL])
                            r_3 = cursor.fetchall()
                            price_results = r_3[0][0]
                            previous_short_entry_qty = float(price_results)
                            print(f"previous_short_entry_qty = {previous_short_entry_qty}")

                            actual_sell_income = (previous_short_entry_income / 100) * 99.9
                            proportional_sell_income = (actual_sell_income / previous_short_entry_qty) * BUY_ORDER_QTY
                            SHORT_BUY_PNL = round((proportional_sell_income - TOTAL_BUY_SPEND), 2)
                            short_buy_per = (SHORT_BUY_PNL / proportional_sell_income) * 100
                            SHORT_BUY_PNL_PERCENTAGE = str((round(short_buy_per, 2))) + "%"

                            cursor.execute(sql.SQL(
                                "insert into trade_log(date_time, symbol, order_id, order_action, order_type, executed_price, executed_qty, execution, pnl, percentage) values (%s, %s, %s, %s, %s, %s, %s, %s, %s,%s)"),
                                [buy_order_executed_time, BUY_ORDER_SYMBOL, BUY_ORDER_ID, BUY_ORDER_ACTION, BUY_ORDER_TYPE,
                                 BUY_ORDER_PRICE, BUY_ORDER_QTY, execution, SHORT_BUY_PNL, SHORT_BUY_PNL_PERCENTAGE])
                            conn.commit()

                        except Exception as e:
                            print(e)

                    if req_short_stop_loss_percent > 0 or req_short_take_profit_percent > 0 or req_multi_tp == "Yes":
                        SPOT_ENTRY = "LIMIT"

                        cursor.execute("select entry_price from short_entry where symbol = %s", [SPOT_SYMBOL])
                        r_3 = cursor.fetchall()
                        price_results = r_3[0][0]
                        previous_short_entry_price = float(price_results)
                        print(f"previous_short_entry_price= {previous_short_entry_price}")

                        short_stop_loss_bp = previous_short_entry_price + (
                                    previous_short_entry_price * req_short_stop_loss_percent)

                        short_take_profit_bp = previous_short_entry_price - (
                                    previous_short_entry_price * req_short_take_profit_percent)

                        STOP_LOSS_PRICE_FINAL = cal_price_with_precision(SPOT_SYMBOL=SPOT_SYMBOL,
                                                                         input_price=short_stop_loss_bp)
                        print(f"Stop loss price final = {STOP_LOSS_PRICE_FINAL}")

                        TAKE_PROFIT_PRICE_FINAL = cal_price_with_precision(SPOT_SYMBOL=SPOT_SYMBOL,
                                                                           input_price=short_take_profit_bp)
                        print(f"Take profit price final = {TAKE_PROFIT_PRICE_FINAL}")

                        BUY_ORDER_ID = 0

                        if req_multi_tp == "No":
                            if req_short_stop_loss_percent > 0 and req_short_take_profit_percent > 0:
                                execute_limit_oco_order(SPOT_SIDE=SPOT_SIDE, req_position_type=req_position_type,
                                                        BUY_ORDER_ID=BUY_ORDER_ID,
                                                        SPOT_SYMBOL=SPOT_SYMBOL, SPOT_SELL_QUANTITY=SPOT_BUY_QUANTITY_EL,
                                                        TAKE_PROFIT_PRICE_FINAL=TAKE_PROFIT_PRICE_FINAL,
                                                        STOP_LOSS_PRICE_FINAL=STOP_LOSS_PRICE_FINAL, SPOT_ENTRY=SPOT_ENTRY,
                                                        req_multi_tp=req_multi_tp, req_qty_size=0,
                                                        req_order_time_out=req_order_time_out,tp_type="None")
                            elif req_short_stop_loss_percent > 0 and (
                                    req_short_take_profit_percent == "" or req_short_take_profit_percent == 0):
                                execute_limit_stop_loss_order(SPOT_SIDE, req_position_type, BUY_ORDER_ID, SPOT_SYMBOL,
                                                              SPOT_BUY_QUANTITY_EL,
                                                              STOP_LOSS_PRICE_FINAL, SPOT_ENTRY, req_order_time_out)
                            elif req_short_take_profit_percent > 0 and (
                                    req_short_stop_loss_percent == "" or req_short_stop_loss_percent == 0):
                                execute_limit_take_profit_order(SPOT_SIDE=SPOT_SIDE, req_position_type=req_position_type,
                                                                BUY_ORDER_ID=BUY_ORDER_ID,
                                                                SPOT_SYMBOL=SPOT_SYMBOL,
                                                                SPOT_SELL_QUANTITY=SPOT_BUY_QUANTITY_EL,
                                                                TAKE_PROFIT_PRICE_FINAL=TAKE_PROFIT_PRICE_FINAL,
                                                                SPOT_ENTRY=SPOT_ENTRY,
                                                                req_multi_tp=req_multi_tp, req_qty_size=0,
                                                                req_order_time_out=req_order_time_out,tp_type="None")

                        if req_multi_tp == "Yes":
                            SELLABLE_1 = calculate_sell_qty_with_precision(SPOT_SYMBOL,
                                                                           (SPOT_BUY_QUANTITY_EL * req_tp1_qty_size))
                            print(f"Sellable qty_1 = {SELLABLE_1}")
                            SELLABLE_2 = calculate_sell_qty_with_precision(SPOT_SYMBOL,
                                                                           (SPOT_BUY_QUANTITY_EL * req_tp2_qty_size))
                            print(f"Sellable qty_2 = {SELLABLE_2}")
                            SELLABLE_3 = calculate_sell_qty_with_precision(SPOT_SYMBOL,
                                                                           (SPOT_BUY_QUANTITY_EL * req_tp3_qty_size))
                            print(f"Sellable qty_3 = {SELLABLE_3}")

                            short_take_profit_bp_1 = previous_short_entry_price - (
                                        previous_short_entry_price * req_tp1_percent)
                            short_take_profit_bp_2 = previous_short_entry_price - (
                                        previous_short_entry_price * req_tp2_percent)
                            short_take_profit_bp_3 = previous_short_entry_price - (
                                        previous_short_entry_price * req_tp3_percent)
                            TAKE_PROFIT_PRICE_FINAL_1 = cal_price_with_precision(SPOT_SYMBOL=SPOT_SYMBOL,
                                                                                 input_price=short_take_profit_bp_1)
                            TAKE_PROFIT_PRICE_FINAL_2 = cal_price_with_precision(SPOT_SYMBOL=SPOT_SYMBOL,
                                                                                 input_price=short_take_profit_bp_2)
                            TAKE_PROFIT_PRICE_FINAL_3 = cal_price_with_precision(SPOT_SYMBOL=SPOT_SYMBOL,
                                                                                 input_price=short_take_profit_bp_3)
                            print(f"Take profit price final_1 = {TAKE_PROFIT_PRICE_FINAL_1}")
                            print(f"Take profit price final_2 = {TAKE_PROFIT_PRICE_FINAL_2}")
                            print(f"Take profit price final_3 = {TAKE_PROFIT_PRICE_FINAL_3}")

                            if req_short_stop_loss_percent > 0 and (
                                    req_tp1_percent > 0 or req_tp2_percent > 0 or req_tp3_percent > 0):
                                if req_tp1_percent > 0:
                                    t1 = threading.Thread(target=lambda: execute_limit_oco_order(SPOT_SIDE=SPOT_SIDE,
                                                                                                 req_position_type=req_position_type,
                                                                                                 BUY_ORDER_ID=BUY_ORDER_ID,
                                                                                                 SPOT_SYMBOL=SPOT_SYMBOL,
                                                                                                 SPOT_SELL_QUANTITY=SELLABLE_1,
                                                                                                 TAKE_PROFIT_PRICE_FINAL=TAKE_PROFIT_PRICE_FINAL_1,
                                                                                                 STOP_LOSS_PRICE_FINAL=STOP_LOSS_PRICE_FINAL,
                                                                                                 SPOT_ENTRY=SPOT_ENTRY,
                                                                                                 req_multi_tp=req_multi_tp,
                                                                                                 req_qty_size=req_tp1_qty_size,
                                                                                                 req_order_time_out=req_order_time_out,tp_type="One"))
                                    t1.start()
                                if req_tp2_percent > 0:
                                    t2 = threading.Thread(target=lambda: execute_limit_oco_order(SPOT_SIDE=SPOT_SIDE,
                                                                                                 req_position_type=req_position_type,
                                                                                                 BUY_ORDER_ID=BUY_ORDER_ID,
                                                                                                 SPOT_SYMBOL=SPOT_SYMBOL,
                                                                                                 SPOT_SELL_QUANTITY=SELLABLE_2,
                                                                                                 TAKE_PROFIT_PRICE_FINAL=TAKE_PROFIT_PRICE_FINAL_2,
                                                                                                 STOP_LOSS_PRICE_FINAL=STOP_LOSS_PRICE_FINAL,
                                                                                                 SPOT_ENTRY=SPOT_ENTRY,
                                                                                                 req_multi_tp=req_multi_tp,
                                                                                                 req_qty_size=req_tp2_qty_size,
                                                                                                 req_order_time_out=req_order_time_out,tp_type="Two"))
                                    t2.start()
                                if req_tp3_percent > 0:
                                    t3 = threading.Thread(target=lambda: execute_limit_oco_order(SPOT_SIDE=SPOT_SIDE,
                                                                                                 req_position_type=req_position_type,
                                                                                                 BUY_ORDER_ID=BUY_ORDER_ID,
                                                                                                 SPOT_SYMBOL=SPOT_SYMBOL,
                                                                                                 SPOT_SELL_QUANTITY=SELLABLE_3,
                                                                                                 TAKE_PROFIT_PRICE_FINAL=TAKE_PROFIT_PRICE_FINAL_3,
                                                                                                 STOP_LOSS_PRICE_FINAL=STOP_LOSS_PRICE_FINAL,
                                                                                                 SPOT_ENTRY=SPOT_ENTRY,
                                                                                                 req_multi_tp=req_multi_tp,
                                                                                                 req_qty_size=req_tp3_qty_size,
                                                                                                 req_order_time_out=req_order_time_out,tp_type="Three"))
                                    t3.start()


                            elif req_short_stop_loss_percent > 0 and (
                                    req_tp1_percent == 0 and req_tp2_percent == 0 and req_tp3_percent == 0):
                                execute_limit_stop_loss_order(SPOT_SIDE, req_position_type, BUY_ORDER_ID, SPOT_SYMBOL,
                                                              SPOT_BUY_QUANTITY_EL,
                                                              STOP_LOSS_PRICE_FINAL, SPOT_ENTRY, req_order_time_out)


                            elif (req_tp1_percent > 0 or req_tp2_percent > 0 or req_tp3_percent > 0) and (
                                    req_short_stop_loss_percent == "" or req_short_stop_loss_percent == 0):
                                if req_tp1_percent > 0:
                                    t1 = threading.Thread(
                                        target=lambda: execute_limit_take_profit_order(SPOT_SIDE=SPOT_SIDE,
                                                                                       req_position_type=req_position_type,
                                                                                       BUY_ORDER_ID=BUY_ORDER_ID,
                                                                                       SPOT_SYMBOL=SPOT_SYMBOL,
                                                                                       SPOT_SELL_QUANTITY=SELLABLE_1,
                                                                                       TAKE_PROFIT_PRICE_FINAL=TAKE_PROFIT_PRICE_FINAL_1,
                                                                                       SPOT_ENTRY=SPOT_ENTRY,
                                                                                       req_multi_tp=req_multi_tp,
                                                                                       req_qty_size=req_tp1_qty_size,
                                                                                       req_order_time_out=req_order_time_out,tp_type="One"))
                                    t1.start()
                                if req_tp2_percent > 0:
                                    t2 = threading.Thread(
                                        target=lambda: execute_limit_take_profit_order(SPOT_SIDE=SPOT_SIDE,
                                                                                       req_position_type=req_position_type,
                                                                                       BUY_ORDER_ID=BUY_ORDER_ID,
                                                                                       SPOT_SYMBOL=SPOT_SYMBOL,
                                                                                       SPOT_SELL_QUANTITY=SELLABLE_2,
                                                                                       TAKE_PROFIT_PRICE_FINAL=TAKE_PROFIT_PRICE_FINAL_2,
                                                                                       SPOT_ENTRY=SPOT_ENTRY,
                                                                                       req_multi_tp=req_multi_tp,
                                                                                       req_qty_size=req_tp2_qty_size,
                                                                                       req_order_time_out=req_order_time_out,tp_type="Two"))
                                    t2.start()
                                if req_tp3_percent > 0:
                                    t3 = threading.Thread(
                                        target=lambda: execute_limit_take_profit_order(SPOT_SIDE=SPOT_SIDE,
                                                                                       req_position_type=req_position_type,
                                                                                       BUY_ORDER_ID=BUY_ORDER_ID,
                                                                                       SPOT_SYMBOL=SPOT_SYMBOL,
                                                                                       SPOT_SELL_QUANTITY=SELLABLE_3,
                                                                                       TAKE_PROFIT_PRICE_FINAL=TAKE_PROFIT_PRICE_FINAL_3,
                                                                                       SPOT_ENTRY=SPOT_ENTRY,
                                                                                       req_multi_tp=req_multi_tp,
                                                                                       req_qty_size=req_tp2_qty_size,
                                                                                       req_order_time_out=req_order_time_out,tp_type="Three"))
                                    t3.start()

                # Stop bot if balance is below user defined amount

                if req_stop_bot_balance != 0:
                    if check_base_coin_balance() > req_stop_bot_balance:
                        # Check order position
                        if req_position_type == "Enter_long":
                            SPOT_BUY_QUANTITY = calculate_buy_qty_with_precision(SPOT_SYMBOL, qty_in_base_coin)
                            proceed_enter_long(SPOT_BUY_QUANTITY, SPOT_SYMBOL, SPOT_ENTRY, req_long_stop_loss_percent,
                                               req_long_take_profit_percent, req_multi_tp, req_tp1_percent, req_tp2_percent,
                                               req_tp3_percent, req_tp1_qty_size, req_tp2_qty_size, req_tp3_qty_size,
                                               req_order_time_out)

                        elif req_position_type == "Exit_short":
                            SPOT_BUY_QUANTITY_EL = calculate_buy_qty_with_precision(SPOT_SYMBOL, qty_in_base_coin)
                            proceed_exit_short(req_position_type, SPOT_BUY_QUANTITY_EL, SPOT_SYMBOL,
                                               req_short_stop_loss_percent,
                                               req_short_take_profit_percent, req_multi_tp, req_tp1_percent,
                                               req_tp2_percent,
                                               req_tp3_percent, req_tp1_qty_size, req_tp2_qty_size, req_tp3_qty_size,
                                               req_order_time_out)

                        elif req_position_type == "Exit_long":
                            SPOT_SELL_QUANTITY_EL = calculate_buy_qty_with_precision(SPOT_SYMBOL, qty_in_base_coin)
                            proceed_exit_long(req_position_type, SPOT_SELL_QUANTITY_EL, SPOT_SYMBOL,
                                              req_long_stop_loss_percent,
                                              req_long_take_profit_percent, req_multi_tp, req_tp1_percent, req_tp2_percent,
                                              req_tp3_percent, req_tp1_qty_size, req_tp2_qty_size, req_tp3_qty_size,
                                              req_order_time_out)

                        elif req_position_type == "Enter_short":
                            SPOT_SELL_QUANTITY_EL = calculate_buy_qty_with_precision(SPOT_SYMBOL, qty_in_base_coin)
                            proceed_enter_short(req_position_type, SPOT_SELL_QUANTITY_EL, SPOT_SYMBOL,
                                                req_short_stop_loss_percent,
                                                req_short_take_profit_percent, req_multi_tp, req_tp1_percent,
                                                req_tp2_percent, req_tp3_percent,
                                                req_tp1_qty_size, req_tp2_qty_size, req_tp3_qty_size, req_order_time_out)
                    else:
                        error_occured_time = datetime.now(IST)
                        error_occured = "Cant initiate the trade! Wallet balance is low!"
                        cursor.execute("insert into error_log(occured_time, error_description) values (%s, %s)",
                                       [error_occured_time, error_occured])
                        conn.commit()
                if req_stop_bot_balance == 0:
                    # Check order position
                    if req_position_type == "Enter_long":
                        SPOT_BUY_QUANTITY = calculate_buy_qty_with_precision(SPOT_SYMBOL, qty_in_base_coin)
                        proceed_enter_long(SPOT_BUY_QUANTITY, SPOT_SYMBOL, SPOT_ENTRY, req_long_stop_loss_percent,
                                           req_long_take_profit_percent, req_multi_tp, req_tp1_percent, req_tp2_percent,
                                           req_tp3_percent, req_tp1_qty_size, req_tp2_qty_size, req_tp3_qty_size,
                                           req_order_time_out)

                    elif req_position_type == "Exit_short":
                        SPOT_BUY_QUANTITY_EL = calculate_buy_qty_with_precision(SPOT_SYMBOL, qty_in_base_coin)
                        proceed_exit_short(req_position_type, SPOT_BUY_QUANTITY_EL, SPOT_SYMBOL,
                                           req_short_stop_loss_percent,
                                           req_short_take_profit_percent, req_multi_tp, req_tp1_percent, req_tp2_percent,
                                           req_tp3_percent, req_tp1_qty_size, req_tp2_qty_size, req_tp3_qty_size,
                                           req_order_time_out)

                    elif req_position_type == "Exit_long":
                        SPOT_SELL_QUANTITY_EL = calculate_buy_qty_with_precision(SPOT_SYMBOL, qty_in_base_coin)
                        proceed_exit_long(req_position_type, SPOT_SELL_QUANTITY_EL, SPOT_SYMBOL, req_long_stop_loss_percent,
                                          req_long_take_profit_percent, req_multi_tp, req_tp1_percent, req_tp2_percent,
                                          req_tp3_percent, req_tp1_qty_size, req_tp2_qty_size, req_tp3_qty_size,
                                          req_order_time_out)

                    elif req_position_type == "Enter_short":
                        SPOT_SELL_QUANTITY_EL = calculate_buy_qty_with_precision(SPOT_SYMBOL, qty_in_base_coin)
                        proceed_enter_short(req_position_type, SPOT_SELL_QUANTITY_EL, SPOT_SYMBOL,
                                            req_short_stop_loss_percent,
                                            req_short_take_profit_percent, req_multi_tp, req_tp1_percent, req_tp2_percent,
                                            req_tp3_percent,
                                            req_tp1_qty_size, req_tp2_qty_size, req_tp3_qty_size, req_order_time_out)


        except Exception as e:
            print(e)
            error_occured_time = datetime.now(IST)
            error_occured = "Error in initiating Spot Order!"
            cursor.execute(
                "insert into error_log(occured_time, error_description) values (%s, %s)",
                [error_occured_time, error_occured])
            conn.commit()

        if req_trade_type == "Futures":
            try:
                try:
                    req_base_coin = alert_response["base_coin"]
                except Exception as e:
                    print(e)
                    error_occured_time = datetime.now(IST)
                    error_occured = "Invalid/Empty base coin"
                    cursor.execute("insert into futures_e_log(occured_time, error_description) values (%s, %s)",
                                   [error_occured_time, error_occured])
                    conn.commit()

                try:
                    req_coin_pair = alert_response["coin_pair"]
                except Exception as e:
                    print(e)
                    error_occured_time = datetime.now(IST)
                    error_occured = "Invalid/Empty coin pair"
                    cursor.execute("insert into futures_e_log(occured_time, error_description) values (%s, %s)",
                                   [error_occured_time, error_occured])
                    conn.commit()

                req_entry_type = alert_response["entry_type"].upper()
                req_exit_type = alert_response["exit_type"].upper()
                req_margin_mode = alert_response["margin_mode"]
                req_long_leverage = float(alert_response["long_leverage"])
                req_short_leverage = float(alert_response["short_leverage"])

                try:
                    req_qty_type = alert_response["qty_type"]
                except Exception as e:
                    print(e)
                    error_occured_time = datetime.now(IST)
                    error_occured = "Invalid/Empty qty type"
                    cursor.execute("insert into futures_e_log(occured_time, error_description) values (%s, %s)",
                                   [error_occured_time, error_occured])
                    conn.commit()

                try:
                    req_qty = float(alert_response["qty"])
                except Exception as e:
                    print(e)
                    error_occured_time = datetime.now(IST)
                    error_occured = "Invalid/Empty qty"
                    cursor.execute("insert into futures_e_log(occured_time, error_description) values (%s, %s)",
                                   [error_occured_time, error_occured])
                    conn.commit()

                req_long_leverage = alert_response["long_leverage"]
                req_short_leverage = alert_response["short_leverage"]

                req_long_stop_loss_percent = (float(alert_response["long_stop_loss_percent"])) / 100
                req_long_take_profit_percent = (float(alert_response["long_take_profit_percent"])) / 100
                req_short_stop_loss_percent = (float(alert_response["short_stop_loss_percent"])) / 100
                req_short_take_profit_percent = (float(alert_response["short_take_profit_percent"])) / 100
                print(f"req short tp = {req_short_take_profit_percent}")
                req_multi_tp = alert_response["enable_multi_tp"]

                req_tp1_qty_size = (float(alert_response["tp_1_pos_size"])) / 100
                req_tp2_qty_size = (float(alert_response["tp_2_pos_size"])) / 100
                req_tp3_qty_size = (float(alert_response["tp_3_pos_size"])) / 100

                req_tp1_percent = (float(alert_response["tp1_percent"])) / 100
                req_tp2_percent = (float(alert_response["tp2_percent"])) / 100
                req_tp3_percent = (float(alert_response["tp3_percent"])) / 100

                req_stop_bot_balance = float(alert_response["stop_bot_below_balance"])
                req_order_time_out = float(alert_response["order_time_out"])

                try:
                    req_position_type = alert_response["position_type"]
                except Exception as e:
                    print(e)
                    error_occured_time = datetime.now(IST)
                    error_occured = "Invalid/Empty position type"
                    cursor.execute("insert into futures_e_log(occured_time, error_description) values (%s, %s)",
                                   [error_occured_time, error_occured])
                    conn.commit()
            except Exception as e:
                print(e)
                error_occured_time = datetime.now(IST)
                error_occured = "Error in parsing json alert"
                cursor.execute("insert into futures_e_log(occured_time, error_description) values (%s, %s)",
                               [error_occured_time, error_occured])
                conn.commit()

            try:
                FUTURES_SYMBOL = req_coin_pair
                print(f"Futures sym = {FUTURES_SYMBOL}")
                FUTURES_ENTRY = req_entry_type
                print(f"Futures entry = {FUTURES_ENTRY}")
                FUTURES_EXIT = req_exit_type
                print(f"Futures exit = {FUTURES_EXIT}")
            except:
                pass

            def futures_calculate_buy_qty_with_precision(FUTURES_SYMBOL, qty_in_base_coin):
                prices = client.get_all_tickers()
                for ticker in prices:
                    if ticker["symbol"] == FUTURES_SYMBOL:
                        current_market_price = float(ticker["price"])
                        break
                tradeable_qty = qty_in_base_coin / current_market_price

                info = client.futures_exchange_info()
                for sym in info["symbols"]:
                    if (sym["symbol"] == FUTURES_SYMBOL):
                        quantity_precision = int(sym["quantityPrecision"])
                        print("quantity_precision: " + str(quantity_precision))
                        break
                BUY_QUANTITY = math.floor((
                                              tradeable_qty) * 10 ** quantity_precision) / 10 ** quantity_precision  # quantity_precision = truncate_num
                print(f"buy qty = {BUY_QUANTITY}")
                return BUY_QUANTITY

            def futures_calculate_sell_qty_with_precision(FUTURES_SYMBOL, qty_in_base_coin):
                info = client.futures_exchange_info()
                for sym in info["symbols"]:
                    if (sym["symbol"] == FUTURES_SYMBOL):
                        quantity_precision = int(sym["quantityPrecision"])
                        print("quantity_precision: " + str(quantity_precision))
                        break
                SELL_QUANTITY = math.floor((
                                               qty_in_base_coin) * 10 ** quantity_precision) / 10 ** quantity_precision  # quantity_precision = truncate_num
                print(f"sell qty = {SELL_QUANTITY}")
                return SELL_QUANTITY

            def futures_cal_price_with_precision(FUTURES_SYMBOL, input_price):
                info = client.futures_exchange_info()
                for sym in info["symbols"]:
                    if (sym["symbol"] == FUTURES_SYMBOL):
                        price_precision = int(sym["pricePrecision"])
                        break
                price = round(input_price, price_precision)
                return price

            def get_opened_position(FUTURES_SYMBOL):
                the_pos = ""
                all_positions = client.futures_position_information()
                for open_pos in all_positions:
                    amt = float(open_pos["positionAmt"])
                    if (open_pos["symbol"] == FUTURES_SYMBOL and (amt > 0 or amt < 0)):
                        the_pos = open_pos
                        break
                return the_pos

            def check_pnl(FUTURES_SYMBOL, stoploss_order_id, tp_order_id, tp_order_id_1, tp_order_id_2, tp_order_id_3,
                          exit_side, FUTURES_QUANTITY, req_multi_tp):
                executed_order_sl = ""
                executed_order_tp = ""
                executed_order1 = ""
                executed_order2 = ""
                executed_order3 = ""
                executed_order_liq = ""
                futures_trade_info = client.futures_account_trades(symbol=FUTURES_SYMBOL)
                for trade in reversed(futures_trade_info):
                    if trade["orderId"] == stoploss_order_id:
                        executed_order_sl = trade
                    if req_multi_tp == "No":
                        if trade["orderId"] == tp_order_id:
                            executed_order_tp = trade
                    if req_multi_tp == "Yes":
                        if trade["orderId"] == tp_order_id_1:
                            executed_order1 = trade
                        if trade["orderId"] == tp_order_id_2:
                            executed_order2 = trade
                        if trade["orderId"] == tp_order_id_3:
                            executed_order3 = trade
                if executed_order_sl == "" and executed_order_tp == "" and executed_order1 == "" and executed_order2 == "" and executed_order3 == "":
                    for rev_trade in reversed(futures_trade_info):
                        if rev_trade["symbol"] == FUTURES_SYMBOL and rev_trade["side"] == exit_side and rev_trade[
                            "qty"] == FUTURES_QUANTITY:
                            executed_order_liq = rev_trade
                            break
                else:
                    pass

                if executed_order_sl != "":
                    realized_pnl = float(executed_order_sl["realizedPnl"])
                    exit_order_commission = float(executed_order_sl["commission"])

                    if executed_order_sl["commissionAsset"] == "USDT":
                        total_pnl = round((realized_pnl - exit_order_commission), 6)
                    else:
                        prices = client.get_all_tickers()
                        bc = executed_order_sl["commissionAsset"]
                        for ticker in prices:
                            if ticker["symbol"] == bc + "USDT":
                                current_market_price = float(ticker["price"])
                                break
                        total_pnl = round(((realized_pnl - exit_order_commission) * current_market_price), 6)

                    FINAL_ORDER_ID = executed_order_sl["orderId"]
                    FINAL_ORDER_SYMBOL = executed_order_sl["symbol"]
                    FINAL_ORDER_QTY = float(executed_order_sl["qty"])
                    FINAL_ORDER_PRICE = float(executed_order_sl["price"])
                    FINAL_ORDER_ACTION = executed_order_sl["side"]
                    FINAL_ORDER_TYPE = "LIMIT"
                    final_order_executed_time = datetime.now(IST)

                    execution = "Executed for Stop Loss"

                    cursor.execute(sql.SQL(
                        "insert into futures_t_log(date_time, symbol, order_id, order_action, order_type, executed_price, executed_qty,execution,pnl) values (%s, %s, %s, %s, %s, %s, %s,%s,%s)"),
                        [final_order_executed_time, FINAL_ORDER_SYMBOL, FINAL_ORDER_ID, FINAL_ORDER_ACTION,
                         FINAL_ORDER_TYPE, FINAL_ORDER_PRICE, FINAL_ORDER_QTY, execution, total_pnl])
                    conn.commit()

                    if req_multi_tp == "No":
                        open_orders = client.futures_get_open_orders()
                        for oo in open_orders:
                            if oo["symbol"] == FUTURES_SYMBOL and oo["orderId"] == tp_order_id:
                                oo_order_id = oo["orderId"]
                                cancel_futures_oo = client.futures_cancel_order(symbol=FUTURES_SYMBOL, orderId=oo_order_id)
                    if req_multi_tp == "Yes":
                        open_orders = client.futures_get_open_orders()
                        for oo in open_orders:
                            if oo["symbol"] == FUTURES_SYMBOL and oo["orderId"] == tp_order_id_1:
                                oo_order_id = oo["orderId"]
                                cancel_futures_oo = client.futures_cancel_order(symbol=FUTURES_SYMBOL, orderId=oo_order_id)
                        open_orders = client.futures_get_open_orders()
                        for oo in open_orders:
                            if oo["symbol"] == FUTURES_SYMBOL and oo["orderId"] == tp_order_id_2:
                                oo_order_id = oo["orderId"]
                                cancel_futures_oo = client.futures_cancel_order(symbol=FUTURES_SYMBOL, orderId=oo_order_id)
                        open_orders = client.futures_get_open_orders()
                        for oo in open_orders:
                            if oo["symbol"] == FUTURES_SYMBOL and oo["orderId"] == tp_order_id_3:
                                oo_order_id = oo["orderId"]
                                cancel_futures_oo = client.futures_cancel_order(symbol=FUTURES_SYMBOL, orderId=oo_order_id)


                if executed_order_tp != "":
                    realized_pnl = float(executed_order_tp["realizedPnl"])
                    exit_order_commission = float(executed_order_tp["commission"])

                    if executed_order_tp["commissionAsset"] == "USDT":
                        total_pnl = round((realized_pnl - exit_order_commission), 6)
                    else:
                        prices = client.get_all_tickers()
                        bc = executed_order_tp["commissionAsset"]
                        for ticker in prices:
                            if ticker["symbol"] == bc + "USDT":
                                current_market_price = float(ticker["price"])
                                break
                        total_pnl = round(((realized_pnl - exit_order_commission) * current_market_price), 6)

                    FINAL_ORDER_ID = executed_order_tp["orderId"]
                    FINAL_ORDER_SYMBOL = executed_order_tp["symbol"]
                    FINAL_ORDER_QTY = float(executed_order_tp["qty"])
                    FINAL_ORDER_PRICE = float(executed_order_tp["price"])
                    FINAL_ORDER_ACTION = executed_order_tp["side"]
                    FINAL_ORDER_TYPE = "LIMIT"
                    final_order_executed_time = datetime.now(IST)

                    execution = "Executed for Take Profit"

                    cursor.execute(sql.SQL(
                        "insert into futures_t_log(date_time, symbol, order_id, order_action, order_type, executed_price, executed_qty,execution,pnl) values (%s, %s, %s, %s, %s, %s, %s,%s,%s)"),
                        [final_order_executed_time, FINAL_ORDER_SYMBOL, FINAL_ORDER_ID, FINAL_ORDER_ACTION,
                         FINAL_ORDER_TYPE, FINAL_ORDER_PRICE, FINAL_ORDER_QTY, execution, total_pnl])
                    conn.commit()

                    open_orders = client.futures_get_open_orders()
                    for oo in open_orders:
                        if oo["symbol"] == FUTURES_SYMBOL and oo["orderId"] == stoploss_order_id:
                            oo_order_id = oo["orderId"]
                            cancel_futures_oo = client.futures_cancel_order(symbol=FUTURES_SYMBOL, orderId=oo_order_id)

                if executed_order1 != "":
                    realized_pnl = float(executed_order1["realizedPnl"])
                    exit_order_commission = float(executed_order1["commission"])

                    if executed_order1["commissionAsset"] == "USDT":
                        total_pnl = round((realized_pnl - exit_order_commission), 6)
                    else:
                        prices = client.get_all_tickers()
                        bc = executed_order1["commissionAsset"]
                        for ticker in prices:
                            if ticker["symbol"] == bc + "USDT":
                                current_market_price = float(ticker["price"])
                                break
                        total_pnl = round(((realized_pnl - exit_order_commission) * current_market_price), 6)

                    FINAL_ORDER_ID = executed_order1["orderId"]
                    FINAL_ORDER_SYMBOL = executed_order1["symbol"]
                    FINAL_ORDER_QTY = float(executed_order1["qty"])
                    FINAL_ORDER_PRICE = float(executed_order1["price"])
                    FINAL_ORDER_ACTION = executed_order1["side"]
                    FINAL_ORDER_TYPE = "LIMIT"
                    final_order_executed_time = datetime.now(IST)

                    execution = "Executed for Take Profit 1"

                    cursor.execute(sql.SQL(
                        "insert into futures_t_log(date_time, symbol, order_id, order_action, order_type, executed_price, executed_qty,execution,pnl) values (%s, %s, %s, %s, %s, %s, %s,%s,%s)"),
                        [final_order_executed_time, FINAL_ORDER_SYMBOL, FINAL_ORDER_ID, FINAL_ORDER_ACTION,
                         FINAL_ORDER_TYPE, FINAL_ORDER_PRICE, FINAL_ORDER_QTY, execution, total_pnl])
                    conn.commit()

                    if tp_order_id_2 == 0 and tp_order_id_3 == 0:
                        open_orders = client.futures_get_open_orders()
                        for oo in open_orders:
                            if oo["symbol"] == FUTURES_SYMBOL and oo["orderId"] == stoploss_order_id:
                                oo_order_id = oo["orderId"]
                                cancel_futures_oo = client.futures_cancel_order(symbol=FUTURES_SYMBOL, orderId=oo_order_id)

                if executed_order2 != "":
                    realized_pnl = float(executed_order2["realizedPnl"])
                    exit_order_commission = float(executed_order2["commission"])

                    if executed_order2["commissionAsset"] == "USDT":
                        total_pnl = round((realized_pnl - exit_order_commission), 6)
                    else:
                        prices = client.get_all_tickers()
                        bc = executed_order2["commissionAsset"]
                        for ticker in prices:
                            if ticker["symbol"] == bc + "USDT":
                                current_market_price = float(ticker["price"])
                                break
                        total_pnl = round(((realized_pnl - exit_order_commission) * current_market_price), 6)

                    FINAL_ORDER_ID = executed_order2["orderId"]
                    FINAL_ORDER_SYMBOL = executed_order2["symbol"]
                    FINAL_ORDER_QTY = float(executed_order2["qty"])
                    FINAL_ORDER_PRICE = float(executed_order2["price"])
                    FINAL_ORDER_ACTION = executed_order2["side"]
                    FINAL_ORDER_TYPE = "LIMIT"
                    final_order_executed_time = datetime.now(IST)

                    execution = "Executed for Take Profit 2"

                    cursor.execute(sql.SQL(
                        "insert into futures_t_log(date_time, symbol, order_id, order_action, order_type, executed_price, executed_qty,execution,pnl) values (%s, %s, %s, %s, %s, %s, %s,%s,%s)"),
                        [final_order_executed_time, FINAL_ORDER_SYMBOL, FINAL_ORDER_ID, FINAL_ORDER_ACTION,
                         FINAL_ORDER_TYPE, FINAL_ORDER_PRICE, FINAL_ORDER_QTY, execution, total_pnl])
                    conn.commit()

                    if tp_order_id_3 == 0:
                        open_orders = client.futures_get_open_orders()
                        for oo in open_orders:
                            if oo["symbol"] == FUTURES_SYMBOL and oo["orderId"] == stoploss_order_id:
                                oo_order_id = oo["orderId"]
                                cancel_futures_oo = client.futures_cancel_order(symbol=FUTURES_SYMBOL, orderId=oo_order_id)

                if executed_order3 != "":
                    realized_pnl = float(executed_order3["realizedPnl"])
                    exit_order_commission = float(executed_order3["commission"])

                    if executed_order3["commissionAsset"] == "USDT":
                        total_pnl = round((realized_pnl - exit_order_commission), 6)
                    else:
                        prices = client.get_all_tickers()
                        bc = executed_order3["commissionAsset"]
                        for ticker in prices:
                            if ticker["symbol"] == bc + "USDT":
                                current_market_price = float(ticker["price"])
                                break
                        total_pnl = round(((realized_pnl - exit_order_commission) * current_market_price), 6)

                    FINAL_ORDER_ID = executed_order3["orderId"]
                    FINAL_ORDER_SYMBOL = executed_order3["symbol"]
                    FINAL_ORDER_QTY = float(executed_order3["qty"])
                    FINAL_ORDER_PRICE = float(executed_order3["price"])
                    FINAL_ORDER_ACTION = executed_order3["side"]
                    FINAL_ORDER_TYPE = "LIMIT"
                    final_order_executed_time = datetime.now(IST)

                    execution = "Executed for Take Profit 3"

                    cursor.execute(sql.SQL(
                        "insert into futures_t_log(date_time, symbol, order_id, order_action, order_type, executed_price, executed_qty,execution,pnl) values (%s, %s, %s, %s, %s, %s, %s,%s,%s)"),
                        [final_order_executed_time, FINAL_ORDER_SYMBOL, FINAL_ORDER_ID, FINAL_ORDER_ACTION,
                         FINAL_ORDER_TYPE, FINAL_ORDER_PRICE, FINAL_ORDER_QTY, execution,total_pnl])
                    conn.commit()

                    open_orders = client.futures_get_open_orders()
                    for oo in open_orders:
                        if oo["symbol"] == FUTURES_SYMBOL and oo["orderId"] == stoploss_order_id:
                            oo_order_id = oo["orderId"]
                            cancel_futures_oo = client.futures_cancel_order(symbol=FUTURES_SYMBOL, orderId=oo_order_id)

                if executed_order_liq != "":
                    realized_pnl = float(executed_order_liq["realizedPnl"])
                    exit_order_commission = float(executed_order_liq["commission"])

                    if executed_order_liq["commissionAsset"] == "USDT":
                        total_pnl = round((realized_pnl - exit_order_commission), 6)
                    else:
                        prices = client.get_all_tickers()
                        bc = executed_order_liq["commissionAsset"]
                        for ticker in prices:
                            if ticker["symbol"] == bc + "USDT":
                                current_market_price = float(ticker["price"])
                                break
                        total_pnl = round(((realized_pnl - exit_order_commission) * current_market_price), 6)

                    FINAL_ORDER_ID = executed_order_liq["orderId"]
                    FINAL_ORDER_SYMBOL = executed_order_liq["symbol"]
                    FINAL_ORDER_QTY = float(executed_order_liq["qty"])
                    FINAL_ORDER_PRICE = float(executed_order_liq["price"])
                    FINAL_ORDER_ACTION = executed_order_liq["side"]
                    FINAL_ORDER_TYPE = "LIMIT"
                    final_order_executed_time = datetime.now(IST)

                    execution = "Liquidated"

                    cursor.execute(sql.SQL(
                        "insert into futures_t_log(date_time, symbol, order_id, order_action, order_type, executed_price, executed_qty,execution,pnl) values (%s, %s, %s, %s, %s, %s, %s,%s,%s)"),
                        [final_order_executed_time, FINAL_ORDER_SYMBOL, FINAL_ORDER_ID, FINAL_ORDER_ACTION,
                         FINAL_ORDER_TYPE, FINAL_ORDER_PRICE, FINAL_ORDER_QTY, execution, total_pnl])
                    conn.commit()

                    open_orders = client.futures_get_open_orders()
                    for oo in open_orders:
                        if oo["symbol"] == FUTURES_SYMBOL:
                            oo_order_id = oo["orderId"]
                            cancel_futures_oo = client.futures_cancel_order(symbol=FUTURES_SYMBOL, orderId=oo_order_id)


            def check_exit_status(FUTURES_SYMBOL, stoploss_order_id, tp_order_id, tp_order_id_1, tp_order_id_2,
                                  tp_order_id_3,
                                  exit_side, FUTURES_QUANTITY, req_multi_tp):
                while True:
                    time.sleep(1)
                    pos_result = get_opened_position(FUTURES_SYMBOL)
                    if pos_result == "":
                        check_pnl(FUTURES_SYMBOL, stoploss_order_id, tp_order_id, tp_order_id_1, tp_order_id_2,
                                  tp_order_id_3,
                                  exit_side, FUTURES_QUANTITY, req_multi_tp)
                        break

            def enter_order(FUTURES_ENTRY, FUTURES_SYMBOL, side, FUTURES_QUANTITY, req_order_time_out,
                            req_long_stop_loss_percent, req_long_take_profit_percent, req_short_stop_loss_percent,
                            req_short_take_profit_percent, req_multi_tp, req_tp1_qty_size, req_tp2_qty_size,
                            req_tp3_qty_size,
                            req_tp1_percent, req_tp2_percent, req_tp3_percent):

                if FUTURES_ENTRY == "MARKET":

                    try:
                        futures_order = client.futures_create_order(symbol=FUTURES_SYMBOL, side=side, type='MARKET',
                                                                    quantity=FUTURES_QUANTITY)
                        print(f"futures order = {futures_order}")
                        order_id = futures_order["orderId"]
                    except Exception as e:
                        error_occured = f"{e}"
                        print(error_occured)
                        error_occured_time = datetime.now(IST)

                        cursor.execute(
                            "insert into futures_e_log(symbol, order_action, entry_order_type, quantity, occured_time, error_description) values (%s, %s, %s, %s, %s, %s)",
                            [FUTURES_SYMBOL, side, FUTURES_ENTRY, FUTURES_QUANTITY, error_occured_time, error_occured])
                        conn.commit()

                    time.sleep(2)

                elif FUTURES_ENTRY == "LIMIT":
                    prices = client.get_all_tickers()
                    for ticker in prices:
                        if ticker["symbol"] == FUTURES_SYMBOL:
                            last_price = float(ticker["price"])
                            break

                    try:
                        futures_order = client.futures_create_order(symbol=FUTURES_SYMBOL, side=side, type='LIMIT',
                                                                    quantity=FUTURES_QUANTITY, price=last_price,
                                                                    timeInForce='GTC')
                        print(f"futures order = {futures_order}")
                        order_id = futures_order["orderId"]
                    except Exception as e:
                        error_occured = f"{e}"
                        print(error_occured)
                        error_occured_time = datetime.now(IST)

                        cursor.execute(
                            "insert into futures_e_log(symbol, order_action, entry_order_type, quantity, occured_time, error_description) values (%s, %s, %s, %s, %s, %s)",
                            [FUTURES_SYMBOL, side, FUTURES_ENTRY, FUTURES_QUANTITY, error_occured_time, error_occured])
                        conn.commit()

                # Loop and check if entry order is filled
                entry_order_timeout_start = time.time()

                while time.time() < (entry_order_timeout_start + req_order_time_out):
                    try:
                        active_order = client.futures_get_order(symbol=FUTURES_SYMBOL, orderId=order_id)
                        active_order_status = active_order["status"]
                        if active_order_status == "FILLED":
                            break
                    except:
                        pass
                if active_order_status == "FILLED":
                    postioned_order = client.futures_get_order(symbol=FUTURES_SYMBOL, orderId=order_id)
                    print(f"postioned futures order = {postioned_order}")
                else:
                    check_for_partial = client.futures_get_order(symbol=FUTURES_SYMBOL, orderId=order_id)
                    if check_for_partial["status"] == "PARTIALLY_FILLED":
                        postioned_order = check_for_partial
                    check_for_cancel = client.futures_get_order(symbol=FUTURES_SYMBOL, orderId=order_id)
                    if check_for_cancel["status"] == "CANCELED" or check_for_cancel["status"] != "PARTIALLY_FILLED" or \
                            check_for_cancel["status"] != "FILLED":
                        print("Already cancelled")
                    else:
                        cancel_futures_limit_order = client.futures_cancel_order(symbol=FUTURES_SYMBOL, orderId=order_id)
                    error_occured = "Order time limit reached! Pending open limit orders has been cancelled"
                    print(error_occured)
                    error_occured_time = datetime.now(IST)
                    cursor.execute(
                        "insert into futures_e_log(symbol, order_action, entry_order_type, quantity, occured_time, error_description) values (%s, %s, %s, %s, %s, %s)",
                        [FUTURES_SYMBOL, side, FUTURES_ENTRY, FUTURES_QUANTITY, error_occured_time, error_occured])
                    conn.commit()

                entry_price = float(postioned_order["avgPrice"])
                print(f"entry price = {entry_price}")

                INITIAL_ORDER_ID = postioned_order["orderId"]
                INITIAL_ORDER_SYMBOL = postioned_order["symbol"]
                INITIAL_ORDER_QTY = float(postioned_order["executedQty"])
                INITIAL_ORDER_PRICE = float(postioned_order["avgPrice"])
                INITIAL_ORDER_ACTION = postioned_order["side"]
                INITIAL_ORDER_TYPE = postioned_order["type"]
                initial_order_executed_time = datetime.now(IST)

                if INITIAL_ORDER_TYPE == "MARKET":
                    execution = "Entry as Market"
                if INITIAL_ORDER_TYPE == "LIMIT":
                    execution = "Entry as Limit"

                live_trades_list = client.futures_account_trades(symbol=FUTURES_SYMBOL)
                for live_trade in reversed(live_trades_list):
                    if live_trade['orderId'] == INITIAL_ORDER_ID:
                        if live_trade["commissionAsset"] == "USDT":
                            entry_order_commission = (float(live_trade["commission"])) * -1
                        else:
                            prices = client.get_all_tickers()
                            bc = live_trade["commissionAsset"]
                            for ticker in prices:
                                if ticker["symbol"] == bc + "USDT":
                                    current_market_price = float(ticker["price"])
                                    break
                            entry_order_commission = ((float(live_trade["commission"])) * -1) * current_market_price

                        break

                cursor.execute(sql.SQL(
                    "insert into futures_t_log(date_time, symbol, order_id, order_action, order_type, executed_price, executed_qty, execution, pnl) values (%s, %s, %s, %s, %s, %s, %s,%s,%s)"),
                    [initial_order_executed_time, INITIAL_ORDER_SYMBOL, INITIAL_ORDER_ID, INITIAL_ORDER_ACTION,
                     INITIAL_ORDER_TYPE, INITIAL_ORDER_PRICE, INITIAL_ORDER_QTY, execution, entry_order_commission])
                conn.commit()

                if req_long_stop_loss_percent > 0 or req_long_take_profit_percent > 0 or req_multi_tp == "Yes" or req_short_stop_loss_percent > 0 or req_short_take_profit_percent > 0:

                    FUTURES_EXIT = "LIMIT"
                    if side == "BUY":
                        exit_side = "SELL"
                        short_stop_loss_bp = entry_price - (entry_price * req_long_stop_loss_percent)

                        STOP_LOSS_PRICE_FINAL = futures_cal_price_with_precision(FUTURES_SYMBOL=FUTURES_SYMBOL,
                                                                                 input_price=short_stop_loss_bp)
                        print(f"Stop loss price final = {STOP_LOSS_PRICE_FINAL}")

                        if req_multi_tp == "No":
                            short_take_profit_bp = entry_price + (entry_price * req_long_take_profit_percent)
                            TAKE_PROFIT_PRICE_FINAL = futures_cal_price_with_precision(FUTURES_SYMBOL=FUTURES_SYMBOL,
                                                                                       input_price=short_take_profit_bp)
                            print(f"Take profit price final = {TAKE_PROFIT_PRICE_FINAL}")

                        elif req_multi_tp == "Yes":
                            SELLABLE_1 = futures_calculate_sell_qty_with_precision(FUTURES_SYMBOL=FUTURES_SYMBOL,
                                                                                   qty_in_base_coin=(
                                                                                               FUTURES_QUANTITY * req_tp1_qty_size))
                            print(f"Sellable qty_1 = {SELLABLE_1}")
                            SELLABLE_2 = futures_calculate_sell_qty_with_precision(FUTURES_SYMBOL=FUTURES_SYMBOL,
                                                                                   qty_in_base_coin=(
                                                                                               FUTURES_QUANTITY * req_tp2_qty_size))
                            print(f"Sellable qty_2 = {SELLABLE_2}")
                            SELLABLE_3 = futures_calculate_sell_qty_with_precision(FUTURES_SYMBOL=FUTURES_SYMBOL,
                                                                                   qty_in_base_coin=(
                                                                                               FUTURES_QUANTITY * req_tp3_qty_size))
                            print(f"Sellable qty_3 = {SELLABLE_3}")

                            short_take_profit_bp_1 = entry_price + (entry_price * req_tp1_percent)
                            short_take_profit_bp_2 = entry_price + (entry_price * req_tp2_percent)
                            short_take_profit_bp_3 = entry_price + (entry_price * req_tp3_percent)
                            TAKE_PROFIT_PRICE_FINAL_1 = futures_cal_price_with_precision(FUTURES_SYMBOL=FUTURES_SYMBOL,
                                                                                         input_price=short_take_profit_bp_1)
                            TAKE_PROFIT_PRICE_FINAL_2 = futures_cal_price_with_precision(FUTURES_SYMBOL=FUTURES_SYMBOL,
                                                                                         input_price=short_take_profit_bp_2)
                            TAKE_PROFIT_PRICE_FINAL_3 = futures_cal_price_with_precision(FUTURES_SYMBOL=FUTURES_SYMBOL,
                                                                                         input_price=short_take_profit_bp_3)

                    elif side == "SELL":
                        exit_side = "BUY"
                        long_stop_loss_bp = entry_price + (entry_price * req_short_stop_loss_percent)
                        STOP_LOSS_PRICE_FINAL = futures_cal_price_with_precision(FUTURES_SYMBOL=FUTURES_SYMBOL,
                                                                                 input_price=long_stop_loss_bp)
                        print(f"Stop loss price final = {STOP_LOSS_PRICE_FINAL}")

                        if req_multi_tp == "No":
                            long_take_profit_bp = entry_price - (entry_price * req_short_take_profit_percent)
                            TAKE_PROFIT_PRICE_FINAL = futures_cal_price_with_precision(FUTURES_SYMBOL=FUTURES_SYMBOL,
                                                                                       input_price=long_take_profit_bp)
                            print(f"Take profit price final = {TAKE_PROFIT_PRICE_FINAL}")

                        elif req_multi_tp == "Yes":
                            SELLABLE_1 = futures_calculate_sell_qty_with_precision(FUTURES_SYMBOL=FUTURES_SYMBOL,
                                                                                   qty_in_base_coin=(
                                                                                               FUTURES_QUANTITY * req_tp1_qty_size))
                            print(f"Sellable qty_1 = {SELLABLE_1}")
                            SELLABLE_2 = futures_calculate_sell_qty_with_precision(FUTURES_SYMBOL=FUTURES_SYMBOL,
                                                                                   qty_in_base_coin=(
                                                                                               FUTURES_QUANTITY * req_tp2_qty_size))
                            print(f"Sellable qty_2 = {SELLABLE_2}")
                            SELLABLE_3 = futures_calculate_sell_qty_with_precision(FUTURES_SYMBOL=FUTURES_SYMBOL,
                                                                                   qty_in_base_coin=(
                                                                                               FUTURES_QUANTITY * req_tp3_qty_size))
                            print(f"Sellable qty_3 = {SELLABLE_3}")

                            long_take_profit_bp_1 = entry_price - (entry_price * req_tp1_percent)
                            long_take_profit_bp_2 = entry_price - (entry_price * req_tp2_percent)
                            long_take_profit_bp_3 = entry_price - (entry_price * req_tp3_percent)
                            TAKE_PROFIT_PRICE_FINAL_1 = futures_cal_price_with_precision(FUTURES_SYMBOL=FUTURES_SYMBOL,
                                                                                         input_price=long_take_profit_bp_1)
                            TAKE_PROFIT_PRICE_FINAL_2 = futures_cal_price_with_precision(FUTURES_SYMBOL=FUTURES_SYMBOL,
                                                                                         input_price=long_take_profit_bp_2)
                            TAKE_PROFIT_PRICE_FINAL_3 = futures_cal_price_with_precision(FUTURES_SYMBOL=FUTURES_SYMBOL,
                                                                                         input_price=long_take_profit_bp_3)
                    if req_long_stop_loss_percent != 0 or req_short_stop_loss_percent != 0:
                        try:
                            stoploss_order = client.futures_create_order(symbol=FUTURES_SYMBOL, side=exit_side,
                                                                         type='STOP_MARKET',
                                                                         stopPrice=STOP_LOSS_PRICE_FINAL,
                                                                         closePosition="true")
                            print(stoploss_order)
                            stoploss_order_id = stoploss_order["orderId"]

                            cursor.execute("insert into f_id_list(order_id, entry_price, qty) values (%s, %s,  %s)",
                                           [stoploss_order_id, entry_price, INITIAL_ORDER_QTY])
                            conn.commit()

                        except Exception as e:
                            stoploss_order_id = 0
                            error_occured = f"{e}"
                            print(error_occured)
                            error_occured_time = datetime.now(IST)

                            cursor.execute(
                                "insert into futures_e_log(symbol, order_action, entry_order_type, exit_order_type, quantity, occured_time, error_description) values (%s, %s, %s, %s, %s, %s, %s)",
                                [FUTURES_SYMBOL, exit_side, FUTURES_ENTRY, FUTURES_EXIT, FUTURES_QUANTITY,
                                 error_occured_time,
                                 error_occured])
                            conn.commit()
                    else:
                        stoploss_order_id = 0

                    if req_multi_tp == "No":
                        tp_order_id_1 = 0
                        tp_order_id_2 = 0
                        tp_order_id_3 = 0
                        if req_long_take_profit_percent != 0 or req_short_take_profit_percent != 0:
                            try:
                                take_profit_order = client.futures_create_order(symbol=FUTURES_SYMBOL, side=exit_side,
                                                                                type='TAKE_PROFIT_MARKET',
                                                                                stopPrice=TAKE_PROFIT_PRICE_FINAL,
                                                                                closePosition="true")
                                print(take_profit_order)
                                tp_order_id = take_profit_order["orderId"]

                                cursor.execute("insert into f_id_list(order_id, entry_price,qty) values (%s, %s,%s)",
                                               [tp_order_id, entry_price, INITIAL_ORDER_QTY])
                                conn.commit()

                            except Exception as e:
                                tp_order_id = 0
                                error_occured = f"{e}"
                                print(error_occured)
                                error_occured_time = datetime.now(IST)

                                cursor.execute(
                                    "insert into futures_e_log(symbol, order_action, entry_order_type, exit_order_type, quantity, occured_time, error_description) values (%s, %s, %s, %s, %s, %s, %s)",
                                    [FUTURES_SYMBOL, exit_side, FUTURES_ENTRY, FUTURES_EXIT, FUTURES_QUANTITY,
                                     error_occured_time,
                                     error_occured])
                                conn.commit()

                        else:
                            tp_order_id = 0

                    if req_multi_tp == "Yes":
                        total_tp = req_tp1_qty_size + req_tp2_qty_size + req_tp3_qty_size
                        if total_tp == 1:
                            close_position = "Yes"
                        else:
                            close_position = "No"
                        tp_order_id = 0
                        if req_tp1_percent > 0:
                            try:
                                take_profit_order_1 = client.futures_create_order(symbol=FUTURES_SYMBOL, side=exit_side,
                                                                                  type='TAKE_PROFIT_MARKET',
                                                                                  stopPrice=TAKE_PROFIT_PRICE_FINAL_1,
                                                                                  quantity=SELLABLE_1)
                                print(take_profit_order_1)
                                tp_order_id_1 = take_profit_order_1["orderId"]

                                cursor.execute("insert into f_id_list(order_id, entry_price,qty) values (%s, %s, %s)",
                                               [tp_order_id_1, entry_price, SELLABLE_1])
                                conn.commit()

                            except Exception as e:
                                tp_order_id_1 = 0
                                error_occured = f"{e}"
                                print(error_occured)
                                error_occured_time = datetime.now(IST)

                                cursor.execute(
                                    "insert into futures_e_log(symbol, order_action, entry_order_type, exit_order_type, quantity, occured_time, error_description) values (%s, %s, %s, %s, %s, %s, %s)",
                                    [FUTURES_SYMBOL, exit_side, FUTURES_ENTRY, FUTURES_EXIT, FUTURES_QUANTITY,
                                     error_occured_time,
                                     error_occured])
                                conn.commit()
                        else:
                            tp_order_id_1 = 0
                        if req_tp2_percent > 0:
                            try:
                                if req_tp3_percent == 0 and close_position == "Yes":
                                    take_profit_order_2 = client.futures_create_order(symbol=FUTURES_SYMBOL, side=exit_side,
                                                                                      type='TAKE_PROFIT_MARKET',
                                                                                      stopPrice=TAKE_PROFIT_PRICE_FINAL_2,closePosition="true")
                                    print(take_profit_order_2)
                                    tp_order_id_2 = take_profit_order_2["orderId"]

                                    cursor.execute("insert into f_id_list(order_id, entry_price, qty) values (%s, %s, %s)",
                                                   [tp_order_id_2, entry_price, SELLABLE_2])
                                    conn.commit()
                                else:
                                    take_profit_order_2 = client.futures_create_order(symbol=FUTURES_SYMBOL, side=exit_side,
                                                                                      type='TAKE_PROFIT_MARKET',
                                                                                      stopPrice=TAKE_PROFIT_PRICE_FINAL_2,
                                                                                      quantity=SELLABLE_2)
                                    print(take_profit_order_2)
                                    tp_order_id_2 = take_profit_order_2["orderId"]

                                    cursor.execute("insert into f_id_list(order_id, entry_price, qty) values (%s, %s, %s)",
                                                   [tp_order_id_2, entry_price, SELLABLE_2])
                                    conn.commit()

                            except Exception as e:
                                tp_order_id_2 = 0
                                error_occured = f"{e}"
                                print(error_occured)
                                error_occured_time = datetime.now(IST)

                                cursor.execute(
                                    "insert into futures_e_log(symbol, order_action, entry_order_type, exit_order_type, quantity, occured_time, error_description) values (%s, %s, %s, %s, %s, %s, %s)",
                                    [FUTURES_SYMBOL, exit_side, FUTURES_ENTRY, FUTURES_EXIT, FUTURES_QUANTITY,
                                     error_occured_time,
                                     error_occured])
                                conn.commit()
                        else:
                            tp_order_id_2 = 0
                        if req_tp3_percent > 0:
                            try:
                                if close_position == "No":
                                    take_profit_order_3 = client.futures_create_order(symbol=FUTURES_SYMBOL, side=exit_side,
                                                                                      type='TAKE_PROFIT_MARKET',
                                                                                      stopPrice=TAKE_PROFIT_PRICE_FINAL_3,
                                                                                      quantity=SELLABLE_3)
                                    print(take_profit_order_3)
                                    tp_order_id_3 = take_profit_order_3["orderId"]

                                    cursor.execute("insert into f_id_list(order_id, entry_price, qty) values (%s, %s, %s)",
                                                   [tp_order_id_3, entry_price, SELLABLE_3])
                                    conn.commit()
                                if close_position == "Yes":
                                    take_profit_order_3 = client.futures_create_order(symbol=FUTURES_SYMBOL, side=exit_side,
                                                                                      type='TAKE_PROFIT_MARKET',
                                                                                      stopPrice=TAKE_PROFIT_PRICE_FINAL_3,closePosition="true")
                                    print(take_profit_order_3)
                                    tp_order_id_3 = take_profit_order_3["orderId"]

                                    cursor.execute("insert into f_id_list(order_id, entry_price, qty) values (%s, %s, %s)",
                                                   [tp_order_id_3, entry_price, SELLABLE_3])
                                    conn.commit()

                            except Exception as e:
                                tp_order_id_3 = 0
                                error_occured = f"{e}"
                                print(error_occured)
                                error_occured_time = datetime.now(IST)

                                cursor.execute(
                                    "insert into futures_e_log(symbol, order_action, entry_order_type, exit_order_type, quantity, occured_time, error_description) values (%s, %s, %s, %s, %s, %s, %s)",
                                    [FUTURES_SYMBOL, exit_side, FUTURES_ENTRY, FUTURES_EXIT, FUTURES_QUANTITY,
                                     error_occured_time,
                                     error_occured])
                                conn.commit()
                        else:
                            tp_order_id_3 = 0

                    t11 = threading.Thread(
                        target=lambda: check_exit_status(FUTURES_SYMBOL=FUTURES_SYMBOL, stoploss_order_id=stoploss_order_id,
                                                         tp_order_id=tp_order_id, tp_order_id_1=tp_order_id_1,
                                                         tp_order_id_2=tp_order_id_2, tp_order_id_3=tp_order_id_3,
                                                         exit_side=exit_side,
                                                         FUTURES_QUANTITY=FUTURES_QUANTITY, req_multi_tp=req_multi_tp))
                    t11.start()

            def exit_order(side, FUTURES_SYMBOL, FUTURES_EXIT, req_order_time_out):
                the_pos = ""
                all_positions = client.futures_position_information()
                for open_pos in all_positions:
                    amt = float(open_pos["positionAmt"])
                    if (open_pos["symbol"] == FUTURES_SYMBOL and (amt > 0 or amt < 0)):
                        the_pos = open_pos
                        break

                open_orders = client.futures_get_open_orders()
                for oo in open_orders:
                    if oo["symbol"] == FUTURES_SYMBOL:
                        oo_order_id = oo["orderId"]
                        cancel_futures_oo = client.futures_cancel_order(symbol=FUTURES_SYMBOL, orderId=oo_order_id)

                if float(the_pos["positionAmt"]) < 0:
                    existing_side = "SELL"
                else:
                    existing_side = "BUY"
                print(f"existing side = {existing_side}")

                if side == "BUY" and existing_side == "SELL":
                    valid_order = "Yes"
                elif side == "SELL" and existing_side == "BUY":
                    valid_order = "Yes"
                elif side == "BUY" and existing_side == "BUY":
                    valid_order = "No"
                elif side == "SELL" and existing_side == "SELL":
                    valid_order = "No"

                if the_pos == "" or valid_order == "No":
                    if side == "BUY":
                        error_occured = "No valid open short position for this symbol. Cannot proceed with the exit order"
                    if side == "SELL":
                        error_occured = "No valid open long position for this symbol. Cannot proceed with the exit order"
                    error_occured_time = datetime.now(IST)

                    cursor.execute(
                        "insert into futures_e_log(symbol, order_action, entry_order_type, occured_time, error_description) values (%s, %s, %s, %s, %s)",
                        [FUTURES_SYMBOL, side, FUTURES_EXIT, error_occured_time, error_occured])
                    conn.commit()
                else:
                    if side == "BUY":
                        exit_qty = (float(the_pos["positionAmt"])) * -1
                    if side == "SELL":
                        exit_qty = float(the_pos["positionAmt"])

                    if FUTURES_EXIT == "MARKET":

                        try:
                            futures_order = client.futures_create_order(symbol=FUTURES_SYMBOL, side=side, type='MARKET',
                                                                        quantity=exit_qty)
                            print(f"futures order = {futures_order}")
                            order_id = futures_order["orderId"]
                        except Exception as e:

                            error_occured = f"{e}"
                            print(error_occured)
                            error_occured_time = datetime.now(IST)

                            cursor.execute(
                                "insert into futures_e_log(symbol, order_action, exit_order_type, quantity, occured_time, error_description) values (%s, %s, %s, %s, %s, %s)",
                                [FUTURES_SYMBOL, side, FUTURES_EXIT, exit_qty, error_occured_time, error_occured])
                            conn.commit()

                        time.sleep(2)

                    elif FUTURES_EXIT == "LIMIT":
                        prices = client.get_all_tickers()
                        for ticker in prices:
                            if ticker["symbol"] == FUTURES_SYMBOL:
                                last_price = float(ticker["price"])
                                break

                        try:
                            futures_order = client.futures_create_order(symbol=FUTURES_SYMBOL, side=side, type='LIMIT',
                                                                        quantity=exit_qty, price=last_price,
                                                                        timeInForce='GTC')
                            print(f"futures order = {futures_order}")
                            order_id = futures_order["orderId"]
                        except Exception as e:
                            error_occured = f"{e}"
                            print(error_occured)
                            error_occured_time = datetime.now(IST)

                            cursor.execute(
                                "insert into futures_e_log(symbol, order_action, exit_order_type, quantity, occured_time, error_description) values (%s, %s, %s, %s, %s, %s)",
                                [FUTURES_SYMBOL, side, FUTURES_EXIT, exit_qty, error_occured_time, error_occured])
                            conn.commit()

                    time.sleep(180)

                    try:
                        live_trades_list = client.futures_account_trades(symbol=FUTURES_SYMBOL)
                        for live_trade in reversed(live_trades_list):
                            while True:
                                if live_trade["orderId"] == order_id:
                                    executed_order = live_trade
                                    realized_pnl = float(live_trade["realizedPnl"])
                                    commission_charged = float(live_trade["commission"])
                                    if live_trade["commissionAsset"] == "USDT":
                                        total_pnl = round((realized_pnl - commission_charged), 6)
                                    else:
                                        prices = client.get_all_tickers()
                                        bc = live_trade["commissionAsset"]
                                        for ticker in prices:
                                            if ticker["symbol"] == bc + "USDT":
                                                current_market_price = float(ticker["price"])
                                                break
                                        total_pnl = round(((realized_pnl - commission_charged) * current_market_price), 6)
                                    break
                                break

                        FINAL_ORDER_ID = executed_order["orderId"]
                        FINAL_ORDER_SYMBOL = executed_order["symbol"]
                        FINAL_ORDER_QTY = float(executed_order["qty"])
                        FINAL_ORDER_PRICE = float(executed_order["price"])
                        FINAL_ORDER_ACTION = executed_order["side"]
                        FINAL_ORDER_TYPE = executed_order["type"]
                        final_order_executed_time = datetime.now(IST)

                        if FINAL_ORDER_TYPE == "MARKET":
                            execution = "Exit as Market"
                        if FINAL_ORDER_TYPE == "LIMIT":
                            execution = "Exit as Limit"

                        cursor.execute(sql.SQL(
                            "insert into futures_t_log(date_time, symbol, order_id, order_action, order_type, executed_price, executed_qty,execution,pnl) values (%s, %s, %s, %s, %s, %s, %s,%s,%s)"),
                            [final_order_executed_time, FINAL_ORDER_SYMBOL, FINAL_ORDER_ID, FINAL_ORDER_ACTION,
                             FINAL_ORDER_TYPE, FINAL_ORDER_PRICE, FINAL_ORDER_QTY, execution, total_pnl])
                        conn.commit()

                    except Exception as e:
                        print(e)

            try:
                # Check if order is entry
                if req_position_type == "Enter_long" or req_position_type == "Enter_short":
                    print("Hello")

                    if req_position_type == "Enter_long":
                        side = "BUY"
                        leverage = req_long_leverage
                    elif req_position_type == "Enter_short":
                        side = "SELL"
                        leverage = req_short_leverage

                    # Fetch wallet balance
                    futures_info = client.futures_account_balance()
                    futures_balance_in_selected_base_coin = 0.0
                    print(req_base_coin)
                    for futures_asset in futures_info:
                        name = futures_asset["asset"]
                        balance = float(futures_asset["balance"])
                        if name == req_base_coin:
                            futures_balance_in_selected_base_coin += balance

                        else:
                            current_price_ff = client.get_symbol_ticker(symbol=name + req_base_coin)["price"]
                            futures_balance_in_selected_base_coin += balance * float(current_price_ff)
                    print(f"Futures balance = {futures_balance_in_selected_base_coin}")

                    # Set Buy/Sell Leverage & Margin Mode
                    if req_margin_mode == "Isolated":
                        try:
                            changed_margin_type = client.futures_change_margin_type(symbol=FUTURES_SYMBOL,
                                                                                    marginType="ISOLATED")
                            print(changed_margin_type)
                        except Exception as e:
                            print(e)
                            error = "APIError(code=-4046): No need to change margin type."
                            if str(e) == error:
                                pass
                            else:
                                FUTURES_SYMBOL = FUTURES_SYMBOL
                                F_SIDE = side
                                JSON_ENTRY = FUTURES_ENTRY
                                error_occured_time = datetime.now(IST)
                                error_occured = e
                                cursor.execute(
                                    "insert into futures_e_log(symbol, order_action, entry_order_type, occured_time, error_description) values (%s, %s, %s, %s, %s)",
                                    [FUTURES_SYMBOL, F_SIDE, JSON_ENTRY, error_occured_time, error_occured])
                                conn.commit()
                    elif req_margin_mode == "Cross":
                        try:
                            changed_margin_type = client.futures_change_margin_type(symbol=FUTURES_SYMBOL,
                                                                                    marginType="CROSSED")
                            print(changed_margin_type)
                        except Exception as e:
                            print(e)
                            error = "APIError(code=-4046): No need to change margin type."
                            if str(e) == error:
                                pass
                            else:
                                FUTURES_SYMBOL = FUTURES_SYMBOL
                                F_SIDE = side
                                JSON_ENTRY = FUTURES_ENTRY
                                error_occured_time = datetime.now(IST)
                                error_occured = e
                                cursor.execute(
                                    "insert into futures_e_log(symbol, order_action, entry_order_type, occured_time, error_description) values (%s, %s, %s, %s, %s)",
                                    [FUTURES_SYMBOL, F_SIDE, JSON_ENTRY, error_occured_time, error_occured])
                                conn.commit()

                    # Set leverage
                    try:
                        changed_leverage = client.futures_change_leverage(symbol=FUTURES_SYMBOL, leverage=leverage)
                        print("Changed leverage to: " + str(changed_leverage))
                    except Exception as e:
                        print(e)
                        error = "APIError(code=-4046): No need to change leverage."
                        if str(e) == error:
                            pass
                        else:
                            FUTURES_SYMBOL = FUTURES_SYMBOL
                            F_SIDE = side
                            JSON_ENTRY = FUTURES_ENTRY
                            error_occured_time = datetime.now(IST)
                            error_occured = e
                            cursor.execute(
                                "insert into futures_e_log(symbol, order_action, entry_order_type, occured_time, error_description) values (%s, %s, %s, %s, %s)",
                                [FUTURES_SYMBOL, F_SIDE, JSON_ENTRY, error_occured_time, error_occured])
                            conn.commit()

                    if req_qty_type == "Percentage":
                        current_bal = futures_balance_in_selected_base_coin
                        qty_in_base_coin = current_bal * req_qty
                    elif req_qty_type == "Fixed":
                        qty_in_base_coin = req_qty

                    FUTURES_QUANTITY = futures_calculate_buy_qty_with_precision(FUTURES_SYMBOL, qty_in_base_coin)
                    print(f"qty = {FUTURES_QUANTITY}")
                    # Stop bot if balance is below user defined amount
                    print(f"stop bot bal = {req_stop_bot_balance}")
                    if req_stop_bot_balance != 0:
                        if futures_balance_in_selected_base_coin < req_stop_bot_balance:
                            FUTURES_SYMBOL = FUTURES_SYMBOL
                            F_SIDE = side
                            JSON_ENTRY = FUTURES_ENTRY
                            error_occured_time = datetime.now(IST)
                            error_occured = "Cant initiate the trade! Wallet balance is low!"
                            cursor.execute(
                                "insert into futures_e_log(symbol, order_action, entry_order_type, occured_time, error_description) values (%s, %s, %s, %s, %s)",
                                [FUTURES_SYMBOL, F_SIDE, JSON_ENTRY, error_occured_time, error_occured])
                            conn.commit()
                        else:
                            # send values to enter trade function
                            enter_order(FUTURES_ENTRY, FUTURES_SYMBOL, side, FUTURES_QUANTITY, req_order_time_out,
                                        req_long_stop_loss_percent, req_long_take_profit_percent,
                                        req_short_stop_loss_percent,
                                        req_short_take_profit_percent, req_multi_tp, req_tp1_qty_size, req_tp2_qty_size,
                                        req_tp3_qty_size, req_tp1_percent, req_tp2_percent, req_tp3_percent)
                    if req_stop_bot_balance == 0:
                        enter_order(FUTURES_ENTRY, FUTURES_SYMBOL, side, FUTURES_QUANTITY, req_order_time_out,
                                    req_long_stop_loss_percent, req_long_take_profit_percent, req_short_stop_loss_percent,
                                    req_short_take_profit_percent, req_multi_tp, req_tp1_qty_size, req_tp2_qty_size,
                                    req_tp3_qty_size, req_tp1_percent, req_tp2_percent, req_tp3_percent)

                # 7) check if order is exit
                elif req_position_type == "Exit_long" or req_position_type == "Exit_short":
                    print("TRYING TO EXIT.....................")

                    if req_position_type == "Exit_long":
                        side = "SELL"
                    elif req_position_type == "Exit_short":
                        side = "BUY"

                    exit_order(side, FUTURES_SYMBOL, FUTURES_EXIT, req_order_time_out)

            except:
                error_occured_time = datetime.now(IST)
                error_occured = "Error in Initiating Futures Order!"
                cursor.execute(
                    "insert into futures_e_log(occured_time, error_description) values (%s, %s)",
                    [error_occured_time, error_occured])
                conn.commit()

    if req_exchange == "Bybit":
        base_url = "https://api.bybit.com"


        try:
            req_trade_type = alert_response["trade_type"]
        except Exception as e:
            print(e)

        if req_trade_type == "Futures":
            if bybit_api_key and bybit_api_secret != "":
                try:
                    f_session = pybit.usdt_perpetual.HTTP(base_url, bybit_api_key, bybit_api_secret)
                except:
                    print("Alert failed due to invalid keys")

            try:
                try:
                    req_base_coin = alert_response["base_coin"]
                except Exception as e:
                    print(e)
                    error_occured_time = datetime.now(IST)
                    error_occured = "Invalid/Empty base coin"
                    cursor.execute("insert into bybit_futures_e_log(occured_time, error_description) values (%s, %s)",
                                   [error_occured_time, error_occured])
                    conn.commit()

                try:
                    req_coin_pair = alert_response["coin_pair"]

                    cursor.execute("insert into bybit_futures_coin_pairs(pair) values (%s)",
                                   [req_coin_pair])
                    conn.commit()
                except Exception as e:
                    print(e)
                    error_occured_time = datetime.now(IST)
                    error_occured = "Invalid/Empty coin pair"
                    cursor.execute("insert into bybit_futures_e_log(occured_time, error_description) values (%s, %s)",
                                   [error_occured_time, error_occured])
                    conn.commit()

                req_entry_type = alert_response["entry_type"].title()
                req_exit_type = alert_response["exit_type"].title()
                req_margin_mode = alert_response["margin_mode"]
                req_long_leverage = float(alert_response["long_leverage"])
                req_short_leverage = float(alert_response["short_leverage"])

                try:
                    req_qty_type = alert_response["qty_type"]
                except Exception as e:
                    print(e)
                    error_occured_time = datetime.now(IST)
                    error_occured = "Invalid/Empty qty type"
                    cursor.execute("insert into bybit_futures_e_log(occured_time, error_description) values (%s, %s)",
                                   [error_occured_time, error_occured])
                    conn.commit()

                try:
                    req_qty = float(alert_response["qty"])
                except Exception as e:
                    print(e)
                    error_occured_time = datetime.now(IST)
                    error_occured = "Invalid/Empty qty"
                    cursor.execute("insert into bybit_futures_e_log(occured_time, error_description) values (%s, %s)",
                                   [error_occured_time, error_occured])
                    conn.commit()

                req_long_leverage = alert_response["long_leverage"]
                req_short_leverage = alert_response["short_leverage"]

                req_long_stop_loss_percent = (float(alert_response["long_stop_loss_percent"])) / 100
                req_long_take_profit_percent = (float(alert_response["long_take_profit_percent"])) / 100
                req_short_stop_loss_percent = (float(alert_response["short_stop_loss_percent"])) / 100
                req_short_take_profit_percent = (float(alert_response["short_take_profit_percent"])) / 100
                print(f"req short tp = {req_short_take_profit_percent}")
                req_multi_tp = alert_response["enable_multi_tp"]

                req_tp1_qty_size = (float(alert_response["tp_1_pos_size"])) / 100
                req_tp2_qty_size = (float(alert_response["tp_2_pos_size"])) / 100
                req_tp3_qty_size = (float(alert_response["tp_3_pos_size"])) / 100

                req_tp1_percent = (float(alert_response["tp1_percent"])) / 100
                req_tp2_percent = (float(alert_response["tp2_percent"])) / 100
                req_tp3_percent = (float(alert_response["tp3_percent"])) / 100

                req_stop_bot_balance = float(alert_response["stop_bot_below_balance"])
                req_order_time_out = float(alert_response["order_time_out"])

                try:
                    req_position_type = alert_response["position_type"]
                except Exception as e:
                    print(e)
                    error_occured_time = datetime.now(IST)
                    error_occured = "Invalid/Empty position type"
                    cursor.execute("insert into bybit_futures_e_log(occured_time, error_description) values (%s, %s)",
                                   [error_occured_time, error_occured])
                    conn.commit()
            except Exception as e:
                print(e)
                error_occured_time = datetime.now(IST)
                error_occured = "Error in parsing json alert"
                cursor.execute("insert into bybit_futures_e_log(occured_time, error_description) values (%s, %s)",
                               [error_occured_time, error_occured])
                conn.commit()

            try:
                FUTURES_SYMBOL = req_coin_pair
                print(f"Futures sym = {FUTURES_SYMBOL}")
                FUTURES_ENTRY = req_entry_type
                print(f"Futures entry = {FUTURES_ENTRY}")
                FUTURES_EXIT = req_exit_type
                print(f"Futures exit = {FUTURES_EXIT}")
            except:
                pass

            def futures_calculate_buy_qty_with_precision(FUTURES_SYMBOL, qty_in_base_coin):
                symbol_data = (f_session.latest_information_for_symbol(symbol=FUTURES_SYMBOL))
                current_market_price = float(symbol_data['result'][0]['last_price'])

                tradeable_qty = qty_in_base_coin / current_market_price

                data = f_session.query_symbol()
                for data in data['result']:
                    if data["name"] == FUTURES_SYMBOL:
                        lot_size_filter = data["lot_size_filter"]
                        qty_step = lot_size_filter["qty_step"]
                        d = decimal.Decimal(str(qty_step))
                        quantity_precision = abs(d.as_tuple().exponent)
                        print("quantity_precision: " + str(quantity_precision))
                        break

                BUY_QUANTITY = math.floor((
                                              tradeable_qty) * 10 ** quantity_precision) / 10 ** quantity_precision  # quantity_precision = truncate_num
                print(f"buy qty = {BUY_QUANTITY}")
                return BUY_QUANTITY

            def futures_calculate_sell_qty_with_precision(FUTURES_SYMBOL, qty_in_base_coin):
                data = f_session.query_symbol()
                for data in data['result']:
                    if data["name"] == FUTURES_SYMBOL:
                        lot_size_filter = data["lot_size_filter"]
                        qty_step = lot_size_filter["qty_step"]
                        d = decimal.Decimal(str(qty_step))
                        quantity_precision = abs(d.as_tuple().exponent)
                        print("quantity_precision: " + str(quantity_precision))
                        break

                SELL_QUANTITY = math.floor((
                                               qty_in_base_coin) * 10 ** quantity_precision) / 10 ** quantity_precision  # quantity_precision = truncate_num
                print(f"sell qty = {SELL_QUANTITY}")
                return SELL_QUANTITY

            def futures_cal_price_with_precision(FUTURES_SYMBOL, input_price):
                data = f_session.query_symbol()
                for data in data['result']:
                    if data["name"] == FUTURES_SYMBOL:
                        price_filter = data["price_filter"]
                        price_step = price_filter["tick_size"]
                        d = decimal.Decimal(str(price_step))
                        price_precision = abs(d.as_tuple().exponent)
                        print("price_precision: " + str(price_precision))
                        break
                price = round(input_price, price_precision)
                return price

            def get_opened_position(FUTURES_SYMBOL):
                the_pos = ""
                all_pos = f_session.my_position()
                all_positions = all_pos["result"]
                for open_pos in all_positions:
                    amt = float(open_pos["data"]["size"])
                    if (open_pos["data"]["symbol"] == FUTURES_SYMBOL and (amt > 0 or amt < 0)):
                        the_pos = open_pos["data"]
                        break
                return the_pos

            def check_pnl(FUTURES_SYMBOL, stoploss_order_id, tp_order_id, tp_order_id_1, tp_order_id_2, tp_order_id_3,
                          exit_side, FUTURES_QUANTITY, req_multi_tp, req_base_coin):

                first_time_trade = None
                trade_num = f_session.user_trade_records(symbol=FUTURES_SYMBOL)
                trade_number = trade_num["result"]["data"]
                if len(trade_number) > 2:
                    first_time_trade = False
                if len(trade_number) <= 2:
                    first_time_trade = True

                executed_order_sl = ""
                executed_order_tp = ""
                executed_order1 = ""
                executed_order2 = ""
                executed_order3 = ""
                executed_order_liq = ""
                time.sleep(15)
                futures_trade_info = f_session.user_trade_records(symbol=FUTURES_SYMBOL)
                for trade in futures_trade_info["result"]["data"]:
                    if trade["order_id"] == stoploss_order_id:
                        executed_order_sl = trade
                    if req_multi_tp == "No":
                        if trade["order_id"] == tp_order_id:
                            executed_order_tp = trade
                    if req_multi_tp == "Yes":
                        if trade["order_id"] == tp_order_id_1:
                            executed_order1 = trade
                        if trade["order_id"] == tp_order_id_2:
                            executed_order2 = trade
                        if trade["order_id"] == tp_order_id_3:
                            executed_order3 = trade

                if executed_order_sl == "" and executed_order_tp == "" and executed_order1 == "" and executed_order2 == "" and executed_order3 == "":
                    print("Shouldn't come here but came")
                    for trade in futures_trade_info["result"]["data"]:
                        if trade["symbol"] == FUTURES_SYMBOL and trade["side"] == exit_side and trade[
                            "exec_qty"] == FUTURES_QUANTITY:
                            executed_order_liq = trade
                            break
                else:
                    pass

                if executed_order_sl != "":
                    print("Executed sl")
                    closed_pos = f_session.my_position(symbol=FUTURES_SYMBOL)
                    closed_position = closed_pos["result"]
                    for pos in closed_position:
                        print(pos["side"])
                        if pos["side"] == "None":
                            print("I should come here")
                            if first_time_trade == True:
                                print("Not here")
                                realized_pnl = float(pos["cum_realised_pnl"])

                                cursor.execute(sql.SQL(
                                    "insert into bybit_futures_pnl_log(symbol, side, pnl) values (%s, %s, %s)"),
                                    [FUTURES_SYMBOL, "None", realized_pnl])
                                conn.commit()

                            if first_time_trade == False:
                                print("but here")
                                query = cursor.execute(
                                    "select pnl from bybit_futures_pnl_log where symbol = %s and side = %s",
                                    [FUTURES_SYMBOL, "None"])
                                result = cursor.fetchall()
                                previous_pnl = float(result[0][0])

                                cum_realized_pnl = float(pos["cum_realised_pnl"])
                                realized_pnl = cum_realized_pnl - previous_pnl

                                cursor.execute(
                                    "update bybit_futures_pnl_log set pnl = %s where symbol = %s and side = %s",
                                    [cum_realized_pnl, FUTURES_SYMBOL, "None"])
                                conn.commit()

                        if pos["side"] == exit_side:
                            if first_time_trade == True:
                                realized_pnl = float(pos["cum_realised_pnl"])

                                cursor.execute(sql.SQL(
                                    "insert into bybit_futures_pnl_log(symbol, side, pnl) values (%s, %s, %s)"),
                                    [FUTURES_SYMBOL, exit_side, realized_pnl])
                                conn.commit()

                            if first_time_trade == False:
                                query = cursor.execute(
                                    "select pnl from bybit_futures_pnl_log where symbol = %s and side = %s",
                                    [FUTURES_SYMBOL, exit_side])
                                result = cursor.fetchall()
                                previous_pnl = float(result[0][0])

                                cum_realized_pnl = float(pos["cum_realised_pnl"])
                                realized_pnl = cum_realized_pnl - previous_pnl

                                cursor.execute(
                                    "update bybit_futures_pnl_log set pnl = %s where symbol = %s and side = %s",
                                    [cum_realized_pnl, FUTURES_SYMBOL, exit_side])
                                conn.commit()

                    exit_order_commission = float(executed_order_sl["exec_fee"])

                    if req_base_coin == "USDT":
                        total_pnl = round((realized_pnl - exit_order_commission), 6)
                    else:
                        amend_sym = f"{req_base_coin}USDT"
                        symbol_data = (f_session.latest_information_for_symbol(symbol=amend_sym))
                        current_market_price = float(symbol_data['result'][0]['last_price'])

                        total_pnl = round(((realized_pnl - exit_order_commission) * current_market_price), 6)

                    FINAL_ORDER_ID = executed_order_sl["order_id"]
                    FINAL_ORDER_SYMBOL = executed_order_sl["symbol"]
                    FINAL_ORDER_QTY = float(executed_order_sl["exec_qty"])
                    FINAL_ORDER_PRICE = float(executed_order_sl["exec_price"])
                    FINAL_ORDER_ACTION = executed_order_sl["side"]
                    FINAL_ORDER_TYPE = executed_order_sl["order_type"]
                    final_order_executed_time = datetime.now(IST)

                    execution = "Executed for Stop Loss"

                    cursor.execute(sql.SQL(
                        "insert into bybit_futures_t_log(date_time, symbol, order_id, order_action, order_type, executed_price, executed_qty,execution,pnl) values (%s, %s, %s, %s, %s, %s, %s,%s,%s)"),
                        [final_order_executed_time, FINAL_ORDER_SYMBOL, FINAL_ORDER_ID, FINAL_ORDER_ACTION,
                         FINAL_ORDER_TYPE, FINAL_ORDER_PRICE, FINAL_ORDER_QTY, execution, total_pnl])
                    conn.commit()

                    if req_multi_tp == "No":
                        open_orders = f_session.get_conditional_order(symbol=FUTURES_SYMBOL)
                        for oo in open_orders["result"]["data"]:
                            if oo["symbol"] == FUTURES_SYMBOL and oo["stop_order_id"] == tp_order_id:
                                oo_order_id = oo["stop_order_id"]
                                try:
                                    cancel_futures_oo = f_session.cancel_conditional_order(symbol=FUTURES_SYMBOL,
                                                                                           stop_order_id=oo_order_id)
                                except:
                                    pass
                    if req_multi_tp == "Yes":
                        open_orders = f_session.get_conditional_order(symbol=FUTURES_SYMBOL)
                        for oo in open_orders["result"]["data"]:
                            if oo["symbol"] == FUTURES_SYMBOL and oo["stop_order_id"] == tp_order_id_1:
                                oo_order_id = oo["stop_order_id"]
                                try:
                                    cancel_futures_oo = f_session.cancel_conditional_order(symbol=FUTURES_SYMBOL,
                                                                                           stop_order_id=oo_order_id)
                                except:
                                    pass
                        open_orders = f_session.get_conditional_order(symbol=FUTURES_SYMBOL)
                        for oo in open_orders["result"]["data"]:
                            if oo["symbol"] == FUTURES_SYMBOL and oo["stop_order_id"] == tp_order_id_2:
                                oo_order_id = oo["stop_order_id"]
                                try:
                                    cancel_futures_oo = f_session.cancel_conditional_order(symbol=FUTURES_SYMBOL,
                                                                                           stop_order_id=oo_order_id)
                                except:
                                    pass
                        open_orders = f_session.get_conditional_order(symbol=FUTURES_SYMBOL)
                        for oo in open_orders["result"]["data"]:
                            if oo["symbol"] == FUTURES_SYMBOL and oo["stop_order_id"] == tp_order_id_3:
                                oo_order_id = oo["stop_order_id"]
                                try:
                                    cancel_futures_oo = f_session.cancel_conditional_order(symbol=FUTURES_SYMBOL,
                                                                                           stop_order_id=oo_order_id)
                                except:
                                    pass

                if executed_order_tp != "":
                    print("Executed tp")
                    closed_pos = f_session.my_position(symbol=FUTURES_SYMBOL)
                    closed_position = closed_pos["result"]
                    for pos in closed_position:
                        print(pos["side"])
                        if pos["side"] == "None":
                            print("I should come here")
                            if first_time_trade == True:
                                print("Not here")
                                realized_pnl = float(pos["cum_realised_pnl"])

                                cursor.execute(sql.SQL(
                                    "insert into bybit_futures_pnl_log(symbol, side, pnl) values (%s, %s, %s)"),
                                    [FUTURES_SYMBOL, "None", realized_pnl])
                                conn.commit()

                            if first_time_trade == False:
                                print("But here")
                                query = cursor.execute(
                                    "select pnl from bybit_futures_pnl_log where symbol = %s and side = %s",
                                    [FUTURES_SYMBOL, "None"])
                                result = cursor.fetchall()
                                previous_pnl = float(result[0][0])

                                cum_realized_pnl = float(pos["cum_realised_pnl"])
                                realized_pnl = cum_realized_pnl - previous_pnl

                                cursor.execute(
                                    "update bybit_futures_pnl_log set pnl = %s where symbol = %s and side = %s",
                                    [cum_realized_pnl, FUTURES_SYMBOL, "None"])
                                conn.commit()

                        if pos["side"] == exit_side:
                            if first_time_trade == True:
                                realized_pnl = float(pos["cum_realised_pnl"])

                                cursor.execute(sql.SQL(
                                    "insert into bybit_futures_pnl_log(symbol, side, pnl) values (%s, %s, %s)"),
                                    [FUTURES_SYMBOL, exit_side, realized_pnl])
                                conn.commit()

                            if first_time_trade == False:
                                query = cursor.execute(
                                    "select pnl from bybit_futures_pnl_log where symbol = %s and side = %s",
                                    [FUTURES_SYMBOL, exit_side])
                                result = cursor.fetchall()
                                previous_pnl = float(result[0][0])

                                cum_realized_pnl = float(pos["cum_realised_pnl"])
                                realized_pnl = cum_realized_pnl - previous_pnl

                                cursor.execute(
                                    "update bybit_futures_pnl_log set pnl = %s where symbol = %s and side = %s",
                                    [cum_realized_pnl, FUTURES_SYMBOL, exit_side])
                                conn.commit()

                    exit_order_commission = float(executed_order_tp["exec_fee"])

                    if req_base_coin == "USDT":
                        total_pnl = round((realized_pnl - exit_order_commission), 6)
                    else:
                        amend_sym = f"{req_base_coin}USDT"
                        symbol_data = (f_session.latest_information_for_symbol(symbol=amend_sym))
                        current_market_price = float(symbol_data['result'][0]['last_price'])

                        total_pnl = round(((realized_pnl - exit_order_commission) * current_market_price), 6)

                    FINAL_ORDER_ID = executed_order_tp["order_id"]
                    FINAL_ORDER_SYMBOL = executed_order_tp["symbol"]
                    FINAL_ORDER_QTY = float(executed_order_tp["exec_qty"])
                    FINAL_ORDER_PRICE = float(executed_order_tp["exec_price"])
                    FINAL_ORDER_ACTION = executed_order_tp["side"]
                    FINAL_ORDER_TYPE = executed_order_tp["order_type"]
                    final_order_executed_time = datetime.now(IST)

                    execution = "Executed for Take Profit"

                    cursor.execute(sql.SQL(
                        "insert into bybit_futures_t_log(date_time, symbol, order_id, order_action, order_type, executed_price, executed_qty,execution,pnl) values (%s, %s, %s, %s, %s, %s, %s,%s,%s)"),
                        [final_order_executed_time, FINAL_ORDER_SYMBOL, FINAL_ORDER_ID, FINAL_ORDER_ACTION,
                         FINAL_ORDER_TYPE, FINAL_ORDER_PRICE, FINAL_ORDER_QTY, execution, total_pnl])
                    conn.commit()

                    open_orders = f_session.get_conditional_order(symbol=FUTURES_SYMBOL)
                    for oo in open_orders["result"]["data"]:
                        if oo["symbol"] == FUTURES_SYMBOL and oo["stop_order_id"] == stoploss_order_id:
                            oo_order_id = oo["stop_order_id"]
                            try:
                                cancel_futures_oo = f_session.cancel_conditional_order(symbol=FUTURES_SYMBOL,
                                                                                       stop_order_id=oo_order_id)
                            except:
                                pass

                if executed_order1 != "":
                    closed_pos = f_session.my_position(symbol=FUTURES_SYMBOL)
                    closed_position = closed_pos["result"]
                    for pos in closed_position:
                        if pos["side"] == "None":
                            if first_time_trade == True:
                                realized_pnl = float(pos["cum_realised_pnl"])

                                cursor.execute(sql.SQL(
                                    "insert into bybit_futures_pnl_log(symbol, side, pnl) values (%s, %s, %s)"),
                                    [FUTURES_SYMBOL, "None", realized_pnl])
                                conn.commit()

                            if first_time_trade == False:
                                query = cursor.execute(
                                    "select pnl from bybit_futures_pnl_log where symbol = %s and side = %s",
                                    [FUTURES_SYMBOL, "None"])
                                result = cursor.fetchall()
                                previous_pnl = float(result[0][0])

                                cum_realized_pnl = float(pos["cum_realised_pnl"])
                                realized_pnl = cum_realized_pnl - previous_pnl

                                cursor.execute(
                                    "update bybit_futures_pnl_log set pnl = %s where symbol = %s and side = %s",
                                    [cum_realized_pnl, FUTURES_SYMBOL, "None"])
                                conn.commit()

                        if pos["side"] == exit_side:
                            if first_time_trade == True:
                                realized_pnl = float(pos["cum_realised_pnl"])

                                cursor.execute(sql.SQL(
                                    "insert into bybit_futures_pnl_log(symbol, side, pnl) values (%s, %s, %s)"),
                                    [FUTURES_SYMBOL, exit_side, realized_pnl])
                                conn.commit()

                            if first_time_trade == False:
                                query = cursor.execute(
                                    "select pnl from bybit_futures_pnl_log where symbol = %s and side = %s",
                                    [FUTURES_SYMBOL, exit_side])
                                result = cursor.fetchall()
                                previous_pnl = float(result[0][0])

                                cum_realized_pnl = float(pos["cum_realised_pnl"])
                                realized_pnl = cum_realized_pnl - previous_pnl

                                cursor.execute(
                                    "update bybit_futures_pnl_log set pnl = %s where symbol = %s and side = %s",
                                    [cum_realized_pnl, FUTURES_SYMBOL, exit_side])
                                conn.commit()

                    exit_order_commission = float(executed_order1["exec_fee"])

                    if req_base_coin == "USDT":
                        total_pnl = round((realized_pnl - exit_order_commission), 6)
                    else:
                        amend_sym = f"{req_base_coin}USDT"
                        symbol_data = (f_session.latest_information_for_symbol(symbol=amend_sym))
                        current_market_price = float(symbol_data['result'][0]['last_price'])

                        total_pnl = round(((realized_pnl - exit_order_commission) * current_market_price), 6)

                    FINAL_ORDER_ID = executed_order1["order_id"]
                    FINAL_ORDER_SYMBOL = executed_order1["symbol"]
                    FINAL_ORDER_QTY = float(executed_order1["exec_qty"])
                    FINAL_ORDER_PRICE = float(executed_order1["exec_price"])
                    FINAL_ORDER_ACTION = executed_order1["side"]
                    FINAL_ORDER_TYPE = executed_order1["order_type"]
                    final_order_executed_time = datetime.now(IST)

                    execution = "Executed for Take Profit 1"

                    cursor.execute(sql.SQL(
                        "insert into bybit_futures_t_log(date_time, symbol, order_id, order_action, order_type, executed_price, executed_qty,execution,pnl) values (%s, %s, %s, %s, %s, %s, %s,%s,%s)"),
                        [final_order_executed_time, FINAL_ORDER_SYMBOL, FINAL_ORDER_ID, FINAL_ORDER_ACTION,
                         FINAL_ORDER_TYPE, FINAL_ORDER_PRICE, FINAL_ORDER_QTY, execution, total_pnl])
                    conn.commit()

                    if tp_order_id_2 == 0 and tp_order_id_3 == 0:
                        open_orders = f_session.get_conditional_order(symbol=FUTURES_SYMBOL)
                        for oo in open_orders["result"]["data"]:
                            if oo["symbol"] == FUTURES_SYMBOL and oo["stop_order_id"] == stoploss_order_id:
                                oo_order_id = oo["stop_order_id"]
                                try:
                                    cancel_futures_oo = f_session.cancel_conditional_order(symbol=FUTURES_SYMBOL,
                                                                                           stop_order_id=oo_order_id)
                                except:
                                    pass

                if executed_order2 != "":
                    closed_pos = f_session.my_position(symbol=FUTURES_SYMBOL)
                    closed_position = closed_pos["result"]
                    for pos in closed_position:
                        if pos["side"] == "None":
                            if first_time_trade == True:
                                realized_pnl = float(pos["cum_realised_pnl"])

                                cursor.execute(sql.SQL(
                                    "insert into bybit_futures_pnl_log(symbol, side, pnl) values (%s, %s, %s)"),
                                    [FUTURES_SYMBOL, "None", realized_pnl])
                                conn.commit()

                            if first_time_trade == False:
                                query = cursor.execute(
                                    "select pnl from bybit_futures_pnl_log where symbol = %s and side = %s",
                                    [FUTURES_SYMBOL, "None"])
                                result = cursor.fetchall()
                                previous_pnl = float(result[0][0])

                                cum_realized_pnl = float(pos["cum_realised_pnl"])
                                realized_pnl = cum_realized_pnl - previous_pnl

                                cursor.execute(
                                    "update bybit_futures_pnl_log set pnl = %s where symbol = %s and side = %s",
                                    [cum_realized_pnl, FUTURES_SYMBOL, "None"])
                                conn.commit()

                        if pos["side"] == exit_side:
                            if first_time_trade == True:
                                realized_pnl = float(pos["cum_realised_pnl"])

                                cursor.execute(sql.SQL(
                                    "insert into bybit_futures_pnl_log(symbol, side, pnl) values (%s, %s, %s)"),
                                    [FUTURES_SYMBOL, exit_side, realized_pnl])
                                conn.commit()

                            if first_time_trade == False:
                                query = cursor.execute(
                                    "select pnl from bybit_futures_pnl_log where symbol = %s and side = %s",
                                    [FUTURES_SYMBOL, exit_side])
                                result = cursor.fetchall()
                                previous_pnl = float(result[0][0])

                                cum_realized_pnl = float(pos["cum_realised_pnl"])
                                realized_pnl = cum_realized_pnl - previous_pnl

                                cursor.execute(
                                    "update bybit_futures_pnl_log set pnl = %s where symbol = %s and side = %s",
                                    [cum_realized_pnl, FUTURES_SYMBOL, exit_side])
                                conn.commit()

                    exit_order_commission = float(executed_order2["exec_fee"])

                    if req_base_coin == "USDT":
                        total_pnl = round((realized_pnl - exit_order_commission), 6)
                    else:
                        amend_sym = f"{req_base_coin}USDT"
                        symbol_data = (f_session.latest_information_for_symbol(symbol=amend_sym))
                        current_market_price = float(symbol_data['result'][0]['last_price'])

                        total_pnl = round(((realized_pnl - exit_order_commission) * current_market_price), 6)

                    FINAL_ORDER_ID = executed_order2["order_id"]
                    FINAL_ORDER_SYMBOL = executed_order2["symbol"]
                    FINAL_ORDER_QTY = float(executed_order2["exec_qty"])
                    FINAL_ORDER_PRICE = float(executed_order2["exec_price"])
                    FINAL_ORDER_ACTION = executed_order2["side"]
                    FINAL_ORDER_TYPE = executed_order2["order_type"]
                    final_order_executed_time = datetime.now(IST)

                    execution = "Executed for Take Profit 2"

                    cursor.execute(sql.SQL(
                        "insert into bybit_futures_t_log(date_time, symbol, order_id, order_action, order_type, executed_price, executed_qty,execution,pnl) values (%s, %s, %s, %s, %s, %s, %s,%s,%s)"),
                        [final_order_executed_time, FINAL_ORDER_SYMBOL, FINAL_ORDER_ID, FINAL_ORDER_ACTION,
                         FINAL_ORDER_TYPE, FINAL_ORDER_PRICE, FINAL_ORDER_QTY, execution, total_pnl])
                    conn.commit()

                    if tp_order_id_3 == 0:
                        open_orders = f_session.get_conditional_order(symbol=FUTURES_SYMBOL)
                        for oo in open_orders["result"]["data"]:
                            if oo["symbol"] == FUTURES_SYMBOL and oo["stop_order_id"] == stoploss_order_id:
                                oo_order_id = oo["stop_order_id"]
                                try:
                                    cancel_futures_oo = f_session.cancel_conditional_order(symbol=FUTURES_SYMBOL,
                                                                                           stop_order_id=oo_order_id)
                                except:
                                    pass

                if executed_order3 != "":
                    closed_pos = f_session.my_position(symbol=FUTURES_SYMBOL)
                    closed_position = closed_pos["result"]
                    for pos in closed_position:
                        if pos["side"] == "None":
                            if first_time_trade == True:
                                realized_pnl = float(pos["cum_realised_pnl"])

                                cursor.execute(sql.SQL(
                                    "insert into bybit_futures_pnl_log(symbol, side, pnl) values (%s, %s, %s)"),
                                    [FUTURES_SYMBOL, "None", realized_pnl])
                                conn.commit()

                            if first_time_trade == False:
                                query = cursor.execute(
                                    "select pnl from bybit_futures_pnl_log where symbol = %s and side = %s",
                                    [FUTURES_SYMBOL, "None"])
                                result = cursor.fetchall()
                                previous_pnl = float(result[0][0])

                                cum_realized_pnl = float(pos["cum_realised_pnl"])
                                realized_pnl = cum_realized_pnl - previous_pnl

                                cursor.execute(
                                    "update bybit_futures_pnl_log set pnl = %s where symbol = %s and side = %s",
                                    [cum_realized_pnl, FUTURES_SYMBOL, "None"])
                                conn.commit()

                        if pos["side"] == exit_side:
                            if first_time_trade == True:
                                realized_pnl = float(pos["cum_realised_pnl"])

                                cursor.execute(sql.SQL(
                                    "insert into bybit_futures_pnl_log(symbol, side, pnl) values (%s, %s, %s)"),
                                    [FUTURES_SYMBOL, exit_side, realized_pnl])
                                conn.commit()

                            if first_time_trade == False:
                                query = cursor.execute(
                                    "select pnl from bybit_futures_pnl_log where symbol = %s and side = %s",
                                    [FUTURES_SYMBOL, exit_side])
                                result = cursor.fetchall()
                                previous_pnl = float(result[0][0])

                                cum_realized_pnl = float(pos["cum_realised_pnl"])
                                realized_pnl = cum_realized_pnl - previous_pnl

                                cursor.execute(
                                    "update bybit_futures_pnl_log set pnl = %s where symbol = %s and side = %s",
                                    [cum_realized_pnl, FUTURES_SYMBOL, exit_side])
                                conn.commit()

                    exit_order_commission = float(executed_order3["exec_fee"])

                    if req_base_coin == "USDT":
                        total_pnl = round((realized_pnl - exit_order_commission), 6)
                    else:
                        amend_sym = f"{req_base_coin}USDT"
                        symbol_data = (f_session.latest_information_for_symbol(symbol=amend_sym))
                        current_market_price = float(symbol_data['result'][0]['last_price'])

                        total_pnl = round(((realized_pnl - exit_order_commission) * current_market_price), 6)

                    FINAL_ORDER_ID = executed_order3["order_id"]
                    FINAL_ORDER_SYMBOL = executed_order3["symbol"]
                    FINAL_ORDER_QTY = float(executed_order3["exec_qty"])
                    FINAL_ORDER_PRICE = float(executed_order3["exec_price"])
                    FINAL_ORDER_ACTION = executed_order3["side"]
                    FINAL_ORDER_TYPE = executed_order3["order_type"]
                    final_order_executed_time = datetime.now(IST)

                    execution = "Executed for Take Profit 3"

                    cursor.execute(sql.SQL(
                        "insert into bybit_futures_t_log(date_time, symbol, order_id, order_action, order_type, executed_price, executed_qty,execution,pnl) values (%s, %s, %s, %s, %s, %s, %s,%s,%s)"),
                        [final_order_executed_time, FINAL_ORDER_SYMBOL, FINAL_ORDER_ID, FINAL_ORDER_ACTION,
                         FINAL_ORDER_TYPE, FINAL_ORDER_PRICE, FINAL_ORDER_QTY, execution, total_pnl])
                    conn.commit()

                    open_orders = f_session.get_conditional_order(symbol=FUTURES_SYMBOL)
                    for oo in open_orders["result"]["data"]:
                        if oo["symbol"] == FUTURES_SYMBOL and oo["stop_order_id"] == stoploss_order_id:
                            oo_order_id = oo["stop_order_id"]
                            try:
                                cancel_futures_oo = f_session.cancel_conditional_order(symbol=FUTURES_SYMBOL,
                                                                                       stop_order_id=oo_order_id)
                            except:
                                pass

                if executed_order_liq != "":
                    closed_pos = f_session.my_position(symbol=FUTURES_SYMBOL)
                    closed_position = closed_pos["result"]
                    for pos in closed_position:
                        if pos["side"] == "None":
                            if first_time_trade == True:
                                realized_pnl = float(pos["cum_realised_pnl"])

                                cursor.execute(sql.SQL(
                                    "insert into bybit_futures_pnl_log(symbol, side, pnl) values (%s, %s, %s)"),
                                    [FUTURES_SYMBOL, "None", realized_pnl])
                                conn.commit()

                            if first_time_trade == False:
                                query = cursor.execute(
                                    "select pnl from bybit_futures_pnl_log where symbol = %s and side = %s",
                                    [FUTURES_SYMBOL, "None"])
                                result = cursor.fetchall()
                                previous_pnl = float(result[0][0])

                                cum_realized_pnl = float(pos["cum_realised_pnl"])
                                realized_pnl = cum_realized_pnl - previous_pnl

                                cursor.execute(
                                    "update bybit_futures_pnl_log set pnl = %s where symbol = %s and side = %s",
                                    [cum_realized_pnl, FUTURES_SYMBOL, "None"])
                                conn.commit()

                        if pos["side"] == exit_side:
                            if first_time_trade == True:
                                realized_pnl = float(pos["cum_realised_pnl"])

                                cursor.execute(sql.SQL(
                                    "insert into bybit_futures_pnl_log(symbol, side, pnl) values (%s, %s, %s)"),
                                    [FUTURES_SYMBOL, exit_side, realized_pnl])
                                conn.commit()

                            if first_time_trade == False:
                                query = cursor.execute(
                                    "select pnl from bybit_futures_pnl_log where symbol = %s and side = %s",
                                    [FUTURES_SYMBOL, exit_side])
                                result = cursor.fetchall()
                                previous_pnl = float(result[0][0])

                                cum_realized_pnl = float(pos["cum_realised_pnl"])
                                realized_pnl = cum_realized_pnl - previous_pnl

                                cursor.execute(
                                    "update bybit_futures_pnl_log set pnl = %s where symbol = %s and side = %s",
                                    [cum_realized_pnl, FUTURES_SYMBOL, exit_side])
                                conn.commit()

                    exit_order_commission = float(executed_order_liq["exec_fee"])

                    if req_base_coin == "USDT":
                        total_pnl = round((realized_pnl - exit_order_commission), 6)
                    else:
                        amend_sym = f"{req_base_coin}USDT"
                        symbol_data = (f_session.latest_information_for_symbol(symbol=amend_sym))
                        current_market_price = float(symbol_data['result'][0]['last_price'])

                        total_pnl = round(((realized_pnl - exit_order_commission) * current_market_price), 6)

                    FINAL_ORDER_ID = executed_order_liq["order_id"]
                    FINAL_ORDER_SYMBOL = executed_order_liq["symbol"]
                    FINAL_ORDER_QTY = float(executed_order_liq["exec_qty"])
                    FINAL_ORDER_PRICE = float(executed_order_liq["exec_price"])
                    FINAL_ORDER_ACTION = executed_order_liq["side"]
                    FINAL_ORDER_TYPE = executed_order_liq["order_type"]
                    final_order_executed_time = datetime.now(IST)

                    execution = "Liquidated"

                    cursor.execute(sql.SQL(
                        "insert into bybit_futures_t_log(date_time, symbol, order_id, order_action, order_type, executed_price, executed_qty,execution,pnl) values (%s, %s, %s, %s, %s, %s, %s,%s,%s)"),
                        [final_order_executed_time, FINAL_ORDER_SYMBOL, FINAL_ORDER_ID, FINAL_ORDER_ACTION,
                         FINAL_ORDER_TYPE, FINAL_ORDER_PRICE, FINAL_ORDER_QTY, execution, total_pnl])
                    conn.commit()

                    open_orders = f_session.get_conditional_order(symbol=FUTURES_SYMBOL)
                    for oo in open_orders["result"]["data"]:
                        if oo["symbol"] == FUTURES_SYMBOL:
                            oo_order_id = oo["stop_order_id"]
                            try:
                                cancel_futures_oo = f_session.cancel_conditional_order(symbol=FUTURES_SYMBOL,
                                                                                       stop_order_id=oo_order_id)
                            except:
                                pass

            def check_exit_status(FUTURES_SYMBOL, stoploss_order_id, tp_order_id, tp_order_id_1, tp_order_id_2,
                                  tp_order_id_3,
                                  exit_side, FUTURES_QUANTITY, req_multi_tp, req_base_coin):
                while True:
                    time.sleep(1)
                    pos_result = get_opened_position(FUTURES_SYMBOL)
                    if pos_result == "":
                        check_pnl(FUTURES_SYMBOL, stoploss_order_id, tp_order_id, tp_order_id_1, tp_order_id_2,
                                  tp_order_id_3,
                                  exit_side, FUTURES_QUANTITY, req_multi_tp, req_base_coin)
                        break

            def enter_order(FUTURES_ENTRY, FUTURES_SYMBOL, side, FUTURES_QUANTITY, req_order_time_out,
                            req_long_stop_loss_percent, req_long_take_profit_percent, req_short_stop_loss_percent,
                            req_short_take_profit_percent, req_multi_tp, req_tp1_qty_size, req_tp2_qty_size,
                            req_tp3_qty_size,
                            req_tp1_percent, req_tp2_percent, req_tp3_percent):

                if FUTURES_ENTRY == "Market":

                    try:
                        futures_o = f_session.place_active_order(symbol=FUTURES_SYMBOL, qty=FUTURES_QUANTITY,
                                                                 time_in_force="GoodTillCancel", side=side,
                                                                 order_type="Market", reduce_only=False,
                                                                 close_on_trigger=False, position_idx=0)
                        futures_order = futures_o["result"]
                        print(f"futures order = {futures_order}")
                        order_id = futures_order["order_id"]
                    except Exception as e:
                        error_occured = f"{e}"
                        print(error_occured)
                        error_occured_time = datetime.now(IST)
                        cursor.execute(
                            "insert into bybit_futures_e_log(symbol, order_action, entry_order_type, quantity, occured_time, error_description) values (%s, %s, %s, %s, %s, %s)",
                            [FUTURES_SYMBOL, side, FUTURES_ENTRY, FUTURES_QUANTITY, error_occured_time, error_occured])
                        conn.commit()

                    time.sleep(2)

                elif FUTURES_ENTRY == "Limit":
                    symbol_data = (f_session.latest_information_for_symbol(symbol=FUTURES_SYMBOL))
                    last_price = float(symbol_data['result'][0]['last_price'])

                    try:
                        futures_o = f_session.place_active_order(symbol=FUTURES_SYMBOL, qty=FUTURES_QUANTITY,
                                                                 time_in_force="GoodTillCancel", side=side,
                                                                 order_type="Limit",
                                                                 reduce_only=False, close_on_trigger=False,
                                                                 position_idx=0, price=last_price)
                        futures_order = futures_o["result"]
                        print(f"futures order = {futures_order}")
                        order_id = futures_order["order_id"]
                    except Exception as e:
                        error_occured = f"{e}"
                        print(error_occured)
                        error_occured_time = datetime.now(IST)

                        cursor.execute(
                            "insert into bybit_futures_e_log(symbol, order_action, entry_order_type, quantity, occured_time, error_description) values (%s, %s, %s, %s, %s, %s)",
                            [FUTURES_SYMBOL, side, FUTURES_ENTRY, FUTURES_QUANTITY, error_occured_time, error_occured])
                        conn.commit()

                # Loop and check if entry order is filled
                entry_order_timeout_start = time.time()

                while time.time() < (entry_order_timeout_start + req_order_time_out):
                    try:
                        time.sleep(1)
                        active_or = f_session.get_active_order(order_id=order_id, symbol=FUTURES_SYMBOL)
                        active_order = active_or["result"]["data"][0]
                        active_order_status = active_order["order_status"]
                        print(active_order_status)
                        if active_order_status == "Filled":
                            break
                    except Exception as e:
                        print(e)
                        pass
                if active_order_status == "Filled":
                    postioned_or = f_session.get_active_order(order_id=order_id, symbol=FUTURES_SYMBOL)
                    postioned_order = postioned_or["result"]["data"][0]
                    print(f"postioned futures order = {postioned_order}")
                else:
                    check_for_par = f_session.get_active_order(order_id=order_id, symbol=FUTURES_SYMBOL)
                    check_for_partial = check_for_par["result"]["data"][0]
                    if check_for_partial["order_status"] == "PartiallyFilled":
                        postioned_order = check_for_partial
                    check_for_can = f_session.get_active_order(order_id=order_id, symbol=FUTURES_SYMBOL)
                    check_for_cancel = check_for_can["result"]["data"][0]
                    if check_for_cancel["order_status"] == "Cancelled" or check_for_cancel[
                        "order_status"] != "PartiallyFilled" or check_for_cancel["order_status"] != "Filled":
                        print("Already cancelled")
                    else:
                        cancel_futures_limit_order = f_session.cancel_active_order(symbol=FUTURES_SYMBOL,
                                                                                   order_id=order_id)
                    error_occured = "Order time limit reached! Pending open limit orders has been cancelled"
                    print(error_occured)
                    error_occured_time = datetime.now(IST)
                    cursor.execute(
                        "insert into bybit_futures_e_log(symbol, order_action, entry_order_type, quantity, occured_time, error_description) values (%s, %s, %s, %s, %s, %s)",
                        [FUTURES_SYMBOL, side, FUTURES_ENTRY, FUTURES_QUANTITY, error_occured_time, error_occured])
                    conn.commit()

                the_pos = ""
                all_pos = f_session.my_position()
                all_positions = all_pos["result"]
                for open_pos in all_positions:
                    amt = float(open_pos["data"]["size"])
                    if (open_pos["data"]["symbol"] == FUTURES_SYMBOL and (amt > 0 or amt < 0)):
                        the_pos = open_pos["data"]

                entry_price = float(the_pos["entry_price"])
                print(f"entry price = {entry_price}")

                INITIAL_ORDER_ID = postioned_order["order_id"]
                INITIAL_ORDER_SYMBOL = postioned_order["symbol"]
                INITIAL_ORDER_QTY = float(postioned_order["cum_exec_qty"])
                INITIAL_ORDER_PRICE = float(postioned_order["price"])
                INITIAL_ORDER_ACTION = postioned_order["side"]
                INITIAL_ORDER_TYPE = postioned_order["order_type"]
                initial_order_executed_time = datetime.now(IST)

                if req_base_coin == "USDT":
                    entry_order_commission = (float(postioned_order["cum_exec_fee"])) * -1
                else:
                    amend_sym = f"{req_base_coin}USDT"
                    symbol_data = (f_session.latest_information_for_symbol(symbol=amend_sym))
                    current_market_price = float(symbol_data['result'][0]['last_price'])

                    entry_order_commission = ((float(postioned_order["cum_exec_fee"])) * -1) * current_market_price

                if INITIAL_ORDER_TYPE == "Market":
                    execution = "Entry as Market"
                if INITIAL_ORDER_TYPE == "Limit":
                    execution = "Entry as Limit"

                cursor.execute(sql.SQL(
                    "insert into bybit_futures_t_log(date_time, symbol, order_id, order_action, order_type, executed_price, executed_qty, execution,pnl) values (%s, %s, %s, %s, %s, %s, %s,%s,%s)"),
                    [initial_order_executed_time, INITIAL_ORDER_SYMBOL, INITIAL_ORDER_ID, INITIAL_ORDER_ACTION,
                     INITIAL_ORDER_TYPE, INITIAL_ORDER_PRICE, INITIAL_ORDER_QTY, execution, entry_order_commission])
                conn.commit()

                if req_long_stop_loss_percent > 0 or req_long_take_profit_percent > 0 or req_multi_tp == "Yes" or req_short_stop_loss_percent > 0 or req_short_take_profit_percent > 0:
                    if side == "Buy":
                        exit_side = "Sell"
                        short_stop_loss_bp = entry_price - (entry_price * req_long_stop_loss_percent)

                        STOP_LOSS_PRICE_FINAL = futures_cal_price_with_precision(FUTURES_SYMBOL=FUTURES_SYMBOL,
                                                                                 input_price=short_stop_loss_bp)
                        print(f"Stop loss price final = {STOP_LOSS_PRICE_FINAL}")

                        if req_multi_tp == "No":
                            short_take_profit_bp = entry_price + (entry_price * req_long_take_profit_percent)
                            TAKE_PROFIT_PRICE_FINAL = futures_cal_price_with_precision(FUTURES_SYMBOL=FUTURES_SYMBOL,
                                                                                       input_price=short_take_profit_bp)
                            print(f"Take profit price final = {TAKE_PROFIT_PRICE_FINAL}")

                        elif req_multi_tp == "Yes":
                            SELLABLE_1 = futures_calculate_sell_qty_with_precision(FUTURES_SYMBOL=FUTURES_SYMBOL,
                                                                                   qty_in_base_coin=(
                                                                                           FUTURES_QUANTITY * req_tp1_qty_size))
                            print(f"Sellable qty_1 = {SELLABLE_1}")
                            SELLABLE_2 = futures_calculate_sell_qty_with_precision(FUTURES_SYMBOL=FUTURES_SYMBOL,
                                                                                   qty_in_base_coin=(
                                                                                           FUTURES_QUANTITY * req_tp2_qty_size))
                            print(f"Sellable qty_2 = {SELLABLE_2}")
                            SELLABLE_3 = futures_calculate_sell_qty_with_precision(FUTURES_SYMBOL=FUTURES_SYMBOL,
                                                                                   qty_in_base_coin=(
                                                                                           FUTURES_QUANTITY * req_tp3_qty_size))
                            print(f"Sellable qty_3 = {SELLABLE_3}")

                            short_take_profit_bp_1 = entry_price + (entry_price * req_tp1_percent)
                            short_take_profit_bp_2 = entry_price + (entry_price * req_tp2_percent)
                            short_take_profit_bp_3 = entry_price + (entry_price * req_tp3_percent)
                            TAKE_PROFIT_PRICE_FINAL_1 = futures_cal_price_with_precision(FUTURES_SYMBOL=FUTURES_SYMBOL,
                                                                                         input_price=short_take_profit_bp_1)
                            TAKE_PROFIT_PRICE_FINAL_2 = futures_cal_price_with_precision(FUTURES_SYMBOL=FUTURES_SYMBOL,
                                                                                         input_price=short_take_profit_bp_2)
                            TAKE_PROFIT_PRICE_FINAL_3 = futures_cal_price_with_precision(FUTURES_SYMBOL=FUTURES_SYMBOL,
                                                                                         input_price=short_take_profit_bp_3)

                    elif side == "Sell":
                        exit_side = "Buy"
                        long_stop_loss_bp = entry_price + (entry_price * req_short_stop_loss_percent)
                        STOP_LOSS_PRICE_FINAL = futures_cal_price_with_precision(FUTURES_SYMBOL=FUTURES_SYMBOL,
                                                                                 input_price=long_stop_loss_bp)
                        print(f"Stop loss price final = {STOP_LOSS_PRICE_FINAL}")

                        if req_multi_tp == "No":
                            long_take_profit_bp = entry_price - (entry_price * req_short_take_profit_percent)
                            TAKE_PROFIT_PRICE_FINAL = futures_cal_price_with_precision(FUTURES_SYMBOL=FUTURES_SYMBOL,
                                                                                       input_price=long_take_profit_bp)
                            print(f"Take profit price final = {TAKE_PROFIT_PRICE_FINAL}")

                        elif req_multi_tp == "Yes":
                            SELLABLE_1 = futures_calculate_sell_qty_with_precision(FUTURES_SYMBOL=FUTURES_SYMBOL,
                                                                                   qty_in_base_coin=(
                                                                                           FUTURES_QUANTITY * req_tp1_qty_size))
                            print(f"Sellable qty_1 = {SELLABLE_1}")
                            SELLABLE_2 = futures_calculate_sell_qty_with_precision(FUTURES_SYMBOL=FUTURES_SYMBOL,
                                                                                   qty_in_base_coin=(
                                                                                           FUTURES_QUANTITY * req_tp2_qty_size))
                            print(f"Sellable qty_2 = {SELLABLE_2}")
                            SELLABLE_3 = futures_calculate_sell_qty_with_precision(FUTURES_SYMBOL=FUTURES_SYMBOL,
                                                                                   qty_in_base_coin=(
                                                                                           FUTURES_QUANTITY * req_tp3_qty_size))
                            print(f"Sellable qty_3 = {SELLABLE_3}")

                            long_take_profit_bp_1 = entry_price - (entry_price * req_tp1_percent)
                            long_take_profit_bp_2 = entry_price - (entry_price * req_tp2_percent)
                            long_take_profit_bp_3 = entry_price - (entry_price * req_tp3_percent)
                            TAKE_PROFIT_PRICE_FINAL_1 = futures_cal_price_with_precision(FUTURES_SYMBOL=FUTURES_SYMBOL,
                                                                                         input_price=long_take_profit_bp_1)
                            TAKE_PROFIT_PRICE_FINAL_2 = futures_cal_price_with_precision(FUTURES_SYMBOL=FUTURES_SYMBOL,
                                                                                         input_price=long_take_profit_bp_2)
                            TAKE_PROFIT_PRICE_FINAL_3 = futures_cal_price_with_precision(FUTURES_SYMBOL=FUTURES_SYMBOL,
                                                                                         input_price=long_take_profit_bp_3)
                    if req_long_stop_loss_percent != 0 or req_short_stop_loss_percent != 0:
                        try:
                            if FUTURES_EXIT == "Market":
                                stoploss_or = f_session.place_conditional_order(symbol=FUTURES_SYMBOL,
                                                                                qty=INITIAL_ORDER_QTY,
                                                                                time_in_force="GoodTillCancel",
                                                                                side=exit_side,
                                                                                order_type="Market",
                                                                                reduce_only=True,
                                                                                close_on_trigger=False,
                                                                                position_idx=0,
                                                                                stop_px=STOP_LOSS_PRICE_FINAL,
                                                                                base_price=entry_price,
                                                                                trigger_by="LastPrice")
                                stoploss_order = stoploss_or["result"]
                                print(f"stoploss_order = {stoploss_order}")
                                stoploss_order_id = stoploss_order["stop_order_id"]

                            if FUTURES_EXIT == "Limit":
                                symbol_data = (f_session.latest_information_for_symbol(symbol=FUTURES_SYMBOL))
                                price_now = symbol_data['result'][0]['last_price']

                                stoploss_or = f_session.place_conditional_order(symbol=FUTURES_SYMBOL,
                                                                                qty=INITIAL_ORDER_QTY,
                                                                                time_in_force="GoodTillCancel",
                                                                                side=exit_side,
                                                                                order_type="Limit",
                                                                                reduce_only=True,
                                                                                close_on_trigger=False,
                                                                                position_idx=0,
                                                                                stop_px=STOP_LOSS_PRICE_FINAL,
                                                                                base_price=entry_price,
                                                                                trigger_by="LastPrice", price=price_now)
                                stoploss_order = stoploss_or["result"]
                                print(f"stoploss_order = {stoploss_order}")
                                stoploss_order_id = stoploss_order["stop_order_id"]

                            cursor.execute(
                                "insert into bybit_f_id_list(order_id, entry_price, qty) values (%s, %s,  %s)",
                                [stoploss_order_id, entry_price, INITIAL_ORDER_QTY])
                            conn.commit()

                        except Exception as e:
                            stoploss_order_id = 0
                            error_occured = f"{e}"
                            print(error_occured)
                            error_occured_time = datetime.now(IST)

                            cursor.execute(
                                "insert into bybit_futures_e_log(symbol, order_action, entry_order_type, exit_order_type, quantity, occured_time, error_description) values (%s, %s, %s, %s, %s, %s, %s)",
                                [FUTURES_SYMBOL, exit_side, FUTURES_ENTRY, FUTURES_EXIT, FUTURES_QUANTITY,
                                 error_occured_time,
                                 error_occured])
                            conn.commit()
                    else:
                        stoploss_order_id = 0

                    if req_multi_tp == "No":
                        tp_order_id_1 = 0
                        tp_order_id_2 = 0
                        tp_order_id_3 = 0
                        if req_long_take_profit_percent != 0 or req_short_take_profit_percent != 0:
                            try:
                                if FUTURES_EXIT == "Market":
                                    take_profit_or = f_session.place_conditional_order(symbol=FUTURES_SYMBOL,
                                                                                       qty=INITIAL_ORDER_QTY,
                                                                                       time_in_force="GoodTillCancel",
                                                                                       side=exit_side,
                                                                                       order_type="Market",
                                                                                       reduce_only=True,
                                                                                       close_on_trigger=False,
                                                                                       position_idx=0,
                                                                                       stop_px=TAKE_PROFIT_PRICE_FINAL,
                                                                                       base_price=entry_price,
                                                                                       trigger_by="LastPrice")
                                    take_profit_order = take_profit_or["result"]
                                    print(f"stoploss_order = {take_profit_order}")
                                    tp_order_id = take_profit_order["stop_order_id"]

                                if FUTURES_EXIT == "Limit":
                                    symbol_data = (f_session.latest_information_for_symbol(symbol=FUTURES_SYMBOL))
                                    price_now = symbol_data['result'][0]['last_price']

                                    take_profit_or = f_session.place_conditional_order(symbol=FUTURES_SYMBOL,
                                                                                       qty=INITIAL_ORDER_QTY,
                                                                                       time_in_force="GoodTillCancel",
                                                                                       side=exit_side,
                                                                                       order_type="Limit",
                                                                                       reduce_only=True,
                                                                                       close_on_trigger=False,
                                                                                       position_idx=0,
                                                                                       stop_px=TAKE_PROFIT_PRICE_FINAL,
                                                                                       base_price=entry_price,
                                                                                       trigger_by="LastPrice",
                                                                                       price=price_now)
                                    take_profit_order = take_profit_or["result"]
                                    print(f"stoploss_order = {take_profit_order}")
                                    tp_order_id = take_profit_order["stop_order_id"]

                                cursor.execute(
                                    "insert into bybit_f_id_list(order_id, entry_price,qty) values (%s, %s,%s)",
                                    [tp_order_id, entry_price, INITIAL_ORDER_QTY])
                                conn.commit()

                            except Exception as e:
                                tp_order_id = 0
                                error_occured = f"{e}"
                                print(error_occured)
                                error_occured_time = datetime.now(IST)

                                cursor.execute(
                                    "insert into bybit_futures_e_log(symbol, order_action, entry_order_type, exit_order_type, quantity, occured_time, error_description) values (%s, %s, %s, %s, %s, %s, %s)",
                                    [FUTURES_SYMBOL, exit_side, FUTURES_ENTRY, FUTURES_EXIT, FUTURES_QUANTITY,
                                     error_occured_time,
                                     error_occured])
                                conn.commit()

                        else:
                            tp_order_id = 0

                    if req_multi_tp == "Yes":
                        tp_order_id = 0
                        if req_tp1_percent > 0:
                            try:
                                if FUTURES_EXIT == "Market":
                                    take_profit_or_1 = f_session.place_conditional_order(symbol=FUTURES_SYMBOL,
                                                                                         qty=SELLABLE_1,
                                                                                         time_in_force="GoodTillCancel",
                                                                                         side=exit_side,
                                                                                         order_type="Market",
                                                                                         reduce_only=True,
                                                                                         close_on_trigger=False,
                                                                                         position_idx=0,
                                                                                         stop_px=TAKE_PROFIT_PRICE_FINAL_1,
                                                                                         base_price=entry_price,
                                                                                         trigger_by="LastPrice")
                                    take_profit_order_1 = take_profit_or_1["result"]
                                    print(f"stoploss_order = {take_profit_order_1}")
                                    tp_order_id_1 = take_profit_order_1["stop_order_id"]

                                if FUTURES_EXIT == "Limit":
                                    symbol_data = (f_session.latest_information_for_symbol(symbol=FUTURES_SYMBOL))
                                    price_now = symbol_data['result'][0]['last_price']

                                    take_profit_or_1 = f_session.place_conditional_order(symbol=FUTURES_SYMBOL,
                                                                                         qty=SELLABLE_1,
                                                                                         time_in_force="GoodTillCancel",
                                                                                         side=exit_side,
                                                                                         order_type="Limit",
                                                                                         reduce_only=True,
                                                                                         close_on_trigger=False,
                                                                                         position_idx=0,
                                                                                         stop_px=TAKE_PROFIT_PRICE_FINAL_1,
                                                                                         base_price=entry_price,
                                                                                         trigger_by="LastPrice",
                                                                                         price=price_now)
                                    take_profit_order_1 = take_profit_or_1["result"]
                                    print(f"stoploss_order = {take_profit_order_1}")
                                    tp_order_id_1 = take_profit_order_1["stop_order_id"]

                                cursor.execute(
                                    "insert into bybit_f_id_list(order_id, entry_price,qty) values (%s, %s, %s)",
                                    [tp_order_id_1, entry_price, SELLABLE_1])
                                conn.commit()

                            except Exception as e:
                                tp_order_id_1 = 0
                                error_occured = f"{e}"
                                print(error_occured)
                                error_occured_time = datetime.now(IST)

                                cursor.execute(
                                    "insert into bybit_futures_e_log(symbol, order_action, entry_order_type, exit_order_type, quantity, occured_time, error_description) values (%s, %s, %s, %s, %s, %s, %s)",
                                    [FUTURES_SYMBOL, exit_side, FUTURES_ENTRY, FUTURES_EXIT, FUTURES_QUANTITY,
                                     error_occured_time,
                                     error_occured])
                                conn.commit()
                        else:
                            tp_order_id_1 = 0
                        if req_tp2_percent > 0:
                            try:
                                if FUTURES_EXIT == "Market":
                                    take_profit_or_2 = f_session.place_conditional_order(symbol=FUTURES_SYMBOL,
                                                                                         qty=SELLABLE_2,
                                                                                         time_in_force="GoodTillCancel",
                                                                                         side=exit_side,
                                                                                         order_type="Market",
                                                                                         reduce_only=True,
                                                                                         close_on_trigger=False,
                                                                                         position_idx=0,
                                                                                         stop_px=TAKE_PROFIT_PRICE_FINAL_2,
                                                                                         base_price=entry_price,
                                                                                         trigger_by="LastPrice")
                                    take_profit_order_2 = take_profit_or_2["result"]
                                    print(f"stoploss_order = {take_profit_order_2}")
                                    tp_order_id_2 = take_profit_order_2["stop_order_id"]

                                if FUTURES_EXIT == "Limit":
                                    symbol_data = (f_session.latest_information_for_symbol(symbol=FUTURES_SYMBOL))
                                    price_now = symbol_data['result'][0]['last_price']

                                    take_profit_or_2 = f_session.place_conditional_order(symbol=FUTURES_SYMBOL,
                                                                                         qty=SELLABLE_2,
                                                                                         time_in_force="GoodTillCancel",
                                                                                         side=exit_side,
                                                                                         order_type="Limit",
                                                                                         reduce_only=True,
                                                                                         close_on_trigger=False,
                                                                                         position_idx=0,
                                                                                         stop_px=TAKE_PROFIT_PRICE_FINAL_2,
                                                                                         base_price=entry_price,
                                                                                         trigger_by="LastPrice",
                                                                                         price=price_now)
                                    take_profit_order_2 = take_profit_or_2["result"]
                                    print(f"stoploss_order = {take_profit_order_2}")
                                    tp_order_id_2 = take_profit_order_2["stop_order_id"]

                                cursor.execute(
                                    "insert into bybit_f_id_list(order_id, entry_price, qty) values (%s, %s, %s)",
                                    [tp_order_id_2, entry_price, SELLABLE_2])
                                conn.commit()

                            except Exception as e:
                                tp_order_id_2 = 0
                                error_occured = f"{e}"
                                print(error_occured)
                                error_occured_time = datetime.now(IST)

                                cursor.execute(
                                    "insert into bybit_futures_e_log(symbol, order_action, entry_order_type, exit_order_type, quantity, occured_time, error_description) values (%s, %s, %s, %s, %s, %s, %s)",
                                    [FUTURES_SYMBOL, exit_side, FUTURES_ENTRY, FUTURES_EXIT, FUTURES_QUANTITY,
                                     error_occured_time,
                                     error_occured])
                                conn.commit()
                        else:
                            tp_order_id_2 = 0
                        if req_tp3_percent > 0:
                            try:
                                if FUTURES_EXIT == "Market":
                                    take_profit_or_3 = f_session.place_conditional_order(symbol=FUTURES_SYMBOL,
                                                                                         qty=SELLABLE_3,
                                                                                         time_in_force="GoodTillCancel",
                                                                                         side=exit_side,
                                                                                         order_type="Market",
                                                                                         reduce_only=True,
                                                                                         close_on_trigger=False,
                                                                                         position_idx=0,
                                                                                         stop_px=TAKE_PROFIT_PRICE_FINAL_3,
                                                                                         base_price=entry_price,
                                                                                         trigger_by="LastPrice")
                                    take_profit_order_3 = take_profit_or_3["result"]
                                    print(f"stoploss_order = {take_profit_order_3}")
                                    tp_order_id_3 = take_profit_order_3["stop_order_id"]

                                if FUTURES_EXIT == "Limit":
                                    symbol_data = (f_session.latest_information_for_symbol(symbol=FUTURES_SYMBOL))
                                    price_now = symbol_data['result'][0]['last_price']

                                    take_profit_or_3 = f_session.place_conditional_order(symbol=FUTURES_SYMBOL,
                                                                                         qty=SELLABLE_3,
                                                                                         time_in_force="GoodTillCancel",
                                                                                         side=exit_side,
                                                                                         order_type="Limit",
                                                                                         reduce_only=True,
                                                                                         close_on_trigger=False,
                                                                                         position_idx=0,
                                                                                         stop_px=TAKE_PROFIT_PRICE_FINAL_3,
                                                                                         base_price=entry_price,
                                                                                         trigger_by="LastPrice",
                                                                                         price=price_now)
                                    take_profit_order_3 = take_profit_or_3["result"]
                                    print(f"stoploss_order = {take_profit_order_3}")
                                    tp_order_id_3 = take_profit_order_3["stop_order_id"]

                                cursor.execute(
                                    "insert into bybit_f_id_list(order_id, entry_price, qty) values (%s, %s, %s)",
                                    [tp_order_id_3, entry_price, SELLABLE_3])
                                conn.commit()

                            except Exception as e:
                                tp_order_id_3 = 0
                                error_occured = f"{e}"
                                print(error_occured)
                                error_occured_time = datetime.now(IST)

                                cursor.execute(
                                    "insert into bybit_futures_e_log(symbol, order_action, entry_order_type, exit_order_type, quantity, occured_time, error_description) values (%s, %s, %s, %s, %s, %s, %s)",
                                    [FUTURES_SYMBOL, exit_side, FUTURES_ENTRY, FUTURES_EXIT, FUTURES_QUANTITY,
                                     error_occured_time,
                                     error_occured])
                                conn.commit()
                        else:
                            tp_order_id_3 = 0

                    t11 = threading.Thread(
                        target=lambda: check_exit_status(FUTURES_SYMBOL=FUTURES_SYMBOL,
                                                         stoploss_order_id=stoploss_order_id,
                                                         tp_order_id=tp_order_id, tp_order_id_1=tp_order_id_1,
                                                         tp_order_id_2=tp_order_id_2, tp_order_id_3=tp_order_id_3,
                                                         exit_side=exit_side,
                                                         FUTURES_QUANTITY=FUTURES_QUANTITY, req_multi_tp=req_multi_tp,
                                                         req_base_coin=req_base_coin))
                    t11.start()

            def exit_order(side, FUTURES_SYMBOL, FUTURES_EXIT, req_order_time_out, req_base_coin):
                the_pos = ""
                all_pos = f_session.my_position()
                all_positions = all_pos["result"]
                for open_pos in all_positions:
                    amt = float(open_pos["data"]["size"])
                    if (open_pos["data"]["symbol"] == FUTURES_SYMBOL and (amt > 0 or amt < 0)):
                        the_pos = open_pos["data"]
                        existing_side = the_pos["side"]
                        print(existing_side)
                        break
                print(the_pos)

                open_orders = f_session.get_conditional_order(symbol=FUTURES_SYMBOL)
                for oo in open_orders["result"]["data"]:
                    if oo["symbol"] == FUTURES_SYMBOL:
                        oo_order_id = oo["stop_order_id"]
                        try:
                            cancel_futures_oo = f_session.cancel_conditional_order(symbol=FUTURES_SYMBOL,
                                                                                   stop_order_id=oo_order_id)
                        except:
                            pass

                if side == "Buy" and existing_side == "Sell":
                    valid_order = "Yes"
                elif side == "Sell" and existing_side == "Buy":
                    valid_order = "Yes"
                elif side == "Buy" and existing_side == "Buy":
                    valid_order = "No"
                elif side == "Sell" and existing_side == "Sell":
                    valid_order = "No"

                if the_pos == "" or valid_order == "No":
                    if side == "Buy":
                        error_occured = "No valid open short position for this symbol. Cannot proceed with the exit order"
                    if side == "Sell":
                        error_occured = "No valid open long position for this symbol. Cannot proceed with the exit order"
                    error_occured_time = datetime.now(IST)

                    cursor.execute(
                        "insert into bybit_futures_e_log(symbol, order_action, entry_order_type, occured_time, error_description) values (%s, %s, %s, %s, %s)",
                        [FUTURES_SYMBOL, side, FUTURES_EXIT, error_occured_time, error_occured])
                    conn.commit()
                else:
                    if side == "Buy":
                        exit_qty = (float(the_pos["size"]))
                        print(f"exit qty = {exit_qty}")
                    if side == "Sell":
                        exit_qty = float(the_pos["size"])
                        print(f"exit qty = {exit_qty}")

                    # if FUTURES_EXIT == "Market":

                    try:
                        futures_o = f_session.place_active_order(symbol=FUTURES_SYMBOL, qty=exit_qty,
                                                                 time_in_force="GoodTillCancel", side=side,
                                                                 order_type="Market", reduce_only=False,
                                                                 close_on_trigger=False, position_idx=0)
                        futures_order = futures_o["result"]
                        print(f"futures order = {futures_order}")
                        order_id = futures_order["order_id"]

                    except Exception as e:
                        error_occured = f"{e}"
                        print(error_occured)
                        error_occured_time = datetime.now(IST)

                        cursor.execute(
                            "insert into bybit_futures_e_log(symbol, order_action, exit_order_type, quantity, occured_time, error_description) values (%s, %s, %s, %s, %s, %s)",
                            [FUTURES_SYMBOL, side, FUTURES_EXIT, exit_qty, error_occured_time, error_occured])
                        conn.commit()

                    # elif FUTURES_EXIT == "Limit":
                    #     symbol_data = (f_session.latest_information_for_symbol(symbol=FUTURES_SYMBOL))
                    #     last_price = float(symbol_data['result'][0]['last_price'])
                    #
                    #     try:
                    #         futures_o = f_session.place_active_order(symbol=FUTURES_SYMBOL, qty=exit_qty,
                    #                                                time_in_force="GoodTillCancel", side=side,
                    #                                                order_type="Limit",
                    #                                                reduce_only=False, close_on_trigger=False,
                    #                                                position_idx=0,
                    #                                                price=last_price)
                    #         futures_order = futures_o["result"]
                    #         print(f"futures order = {futures_order}")
                    #         order_id = futures_order["order_id"]
                    #     except Exception as e:
                    #         error_occured = f"{e}"
                    #         print(error_occured)
                    #         error_occured_time = datetime.now(IST).strftime('%d-%m-%Y %H:%M:%S')
                    #
                    #         cursor.execute(
                    #             "insert into bybit_futures_e_log(symbol, order_action, exit_order_type, quantity, occured_time, error_description) values (%s, %s, %s, %s, %s, %s)",
                    #             [FUTURES_SYMBOL, side, FUTURES_EXIT, exit_qty, error_occured_time, error_occured])
                    #         conn.commit()

                    time.sleep(10)

                    try:
                        first_time_trade = None
                        trade_num = f_session.user_trade_records(symbol=FUTURES_SYMBOL)
                        trade_number = trade_num["result"]["data"]
                        if len(trade_number) > 2:
                            first_time_trade = False
                        if len(trade_number) <= 2:
                            first_time_trade = True

                        while True:
                            live_trades_list = f_session.user_trade_records(symbol=FUTURES_SYMBOL)
                            for live_trade in live_trades_list["result"]["data"]:
                                if live_trade["order_id"] == order_id:
                                    executed_order = live_trade

                                    closed_pos = f_session.my_position(symbol=FUTURES_SYMBOL)
                                    closed_position = closed_pos["result"]
                                    for pos in closed_position:
                                        if pos["side"] == "None":
                                            if first_time_trade == True:
                                                realized_pnl = float(pos["cum_realised_pnl"])

                                                cursor.execute(sql.SQL(
                                                    "insert into bybit_futures_pnl_log(symbol, side, pnl) values (%s, %s, %s)"),
                                                    [FUTURES_SYMBOL, "None", realized_pnl])
                                                conn.commit()

                                            if first_time_trade == False:
                                                query = cursor.execute(
                                                    "select pnl from bybit_futures_pnl_log where symbol = %s and side = %s",
                                                    [FUTURES_SYMBOL, "None"])
                                                result = cursor.fetchall()
                                                previous_pnl = float(result[0][0])

                                                cum_realized_pnl = float(pos["cum_realised_pnl"])
                                                realized_pnl = cum_realized_pnl - previous_pnl

                                                cursor.execute(
                                                    "update bybit_futures_pnl_log set pnl = %s where symbol = %s and side = %s",
                                                    [cum_realized_pnl, FUTURES_SYMBOL, "None"])
                                                conn.commit()

                                        if pos["side"] == side:
                                            if first_time_trade == True:
                                                realized_pnl = float(pos["cum_realised_pnl"])

                                                cursor.execute(sql.SQL(
                                                    "insert into bybit_futures_pnl_log(symbol, side, pnl) values (%s, %s, %s)"),
                                                    [FUTURES_SYMBOL, side, realized_pnl])
                                                conn.commit()

                                            if first_time_trade == False:
                                                query = cursor.execute(
                                                    "select pnl from bybit_futures_pnl_log where symbol = %s and side = %s",
                                                    [FUTURES_SYMBOL, side])
                                                result = cursor.fetchall()
                                                previous_pnl = float(result[0][0])

                                                cum_realized_pnl = float(pos["cum_realised_pnl"])
                                                realized_pnl = cum_realized_pnl - previous_pnl

                                                cursor.execute(
                                                    "update bybit_futures_pnl_log set pnl = %s where symbol = %s and side = %s",
                                                    [cum_realized_pnl, FUTURES_SYMBOL, side])
                                                conn.commit()

                                    exit_order_commission = float(executed_order["exec_fee"])

                                    if req_base_coin == "USDT":
                                        total_pnl = round((realized_pnl - exit_order_commission), 6)
                                    else:
                                        amend_sym = f"{req_base_coin}USDT"
                                        symbol_data = (f_session.latest_information_for_symbol(symbol=amend_sym))
                                        current_market_price = float(symbol_data['result'][0]['last_price'])

                                        total_pnl = round(
                                            ((realized_pnl - exit_order_commission) * current_market_price),
                                            6)
                                    break
                            break

                        FINAL_ORDER_ID = executed_order["order_id"]
                        FINAL_ORDER_SYMBOL = executed_order["symbol"]
                        FINAL_ORDER_QTY = float(executed_order["exec_qty"])
                        FINAL_ORDER_PRICE = float(executed_order["exec_price"])
                        FINAL_ORDER_ACTION = executed_order["side"]
                        FINAL_ORDER_TYPE = executed_order["order_type"]
                        final_order_executed_time = datetime.now(IST)

                        if FINAL_ORDER_TYPE == "Market":
                            execution = "Exit as Market"
                        if FINAL_ORDER_TYPE == "Limit":
                            execution = "Exit as Limit"

                        cursor.execute(sql.SQL(
                            "insert into bybit_futures_t_log(date_time, symbol, order_id, order_action, order_type, executed_price, executed_qty,execution,pnl) values (%s, %s, %s, %s, %s, %s, %s,%s,%s)"),
                            [final_order_executed_time, FINAL_ORDER_SYMBOL, FINAL_ORDER_ID, FINAL_ORDER_ACTION,
                             FINAL_ORDER_TYPE, FINAL_ORDER_PRICE, FINAL_ORDER_QTY, execution, total_pnl])
                        conn.commit()
                        print("Records on exit inserted")

                    except Exception as e:
                        print(e)

            try:
                # Check if order is entry
                if req_position_type == "Enter_long" or req_position_type == "Enter_short":
                    print("Hello I came here now")

                    if req_position_type == "Enter_long":
                        side = "Buy"
                        leverage = req_long_leverage
                    elif req_position_type == "Enter_short":
                        side = "Sell"
                        leverage = req_short_leverage

                    try:
                        f_session.position_mode_switch(mode="MergedSingle", symbol=FUTURES_SYMBOL)
                    except:
                        pass

                    # Fetch wallet balance
                    wallet = f_session.get_wallet_balance(coin=req_base_coin)
                    futures_balance_in_selected_base_coin = float(wallet['result'][req_base_coin]['equity'])
                    print(f"Futures balance = {futures_balance_in_selected_base_coin}")

                    # Set Buy/Sell Leverage & Margin Mode
                    if req_margin_mode == "Isolated":
                        try:
                            f_session.cross_isolated_margin_switch(symbol=FUTURES_SYMBOL, is_isolated=True,
                                                                   buy_leverage=req_long_leverage,
                                                                   sell_leverage=req_short_leverage)
                        except Exception as e:
                            print(e)
                    elif req_margin_mode == "Cross":
                        try:
                            f_session.cross_isolated_margin_switch(symbol=FUTURES_SYMBOL, is_isolated=False,
                                                                   buy_leverage=req_long_leverage,
                                                                   sell_leverage=req_short_leverage)
                        except Exception as e:
                            print(e)

                    # Set leverage
                    try:
                        f_session.set_leverage(symbol=FUTURES_SYMBOL, buy_leverage=req_long_leverage,
                                               sell_leverage=req_short_leverage)
                    except Exception as e:
                        print(e)

                    if req_qty_type == "Percentage":
                        current_bal = futures_balance_in_selected_base_coin
                        qty_in_base_coin = current_bal * req_qty
                    elif req_qty_type == "Fixed":
                        qty_in_base_coin = req_qty

                    FUTURES_QUANTITY = futures_calculate_buy_qty_with_precision(FUTURES_SYMBOL, qty_in_base_coin)
                    print(f"qty = {FUTURES_QUANTITY}")

                    # Stop bot if balance is below user defined amount
                    print(f"stop bot bal = {req_stop_bot_balance}")
                    if req_stop_bot_balance != 0:
                        if futures_balance_in_selected_base_coin < req_stop_bot_balance:
                            FUTURES_SYMBOL = FUTURES_SYMBOL
                            F_SIDE = side
                            JSON_ENTRY = FUTURES_ENTRY
                            error_occured_time = datetime.now(IST)
                            error_occured = "Cant initiate the trade! Wallet balance is low!"
                            cursor.execute(
                                "insert into bybit_futures_e_log(symbol, order_action, entry_order_type, occured_time, error_description) values (%s, %s, %s, %s, %s)",
                                [FUTURES_SYMBOL, F_SIDE, JSON_ENTRY, error_occured_time, error_occured])
                            conn.commit()
                        else:
                            # send values to enter trade function
                            enter_order(FUTURES_ENTRY, FUTURES_SYMBOL, side, FUTURES_QUANTITY, req_order_time_out,
                                        req_long_stop_loss_percent, req_long_take_profit_percent,
                                        req_short_stop_loss_percent,
                                        req_short_take_profit_percent, req_multi_tp, req_tp1_qty_size, req_tp2_qty_size,
                                        req_tp3_qty_size, req_tp1_percent, req_tp2_percent, req_tp3_percent)
                    if req_stop_bot_balance == 0:
                        enter_order(FUTURES_ENTRY, FUTURES_SYMBOL, side, FUTURES_QUANTITY, req_order_time_out,
                                    req_long_stop_loss_percent, req_long_take_profit_percent,
                                    req_short_stop_loss_percent,
                                    req_short_take_profit_percent, req_multi_tp, req_tp1_qty_size, req_tp2_qty_size,
                                    req_tp3_qty_size, req_tp1_percent, req_tp2_percent, req_tp3_percent)

                    # 7) check if order is exit
                elif req_position_type == "Exit_long" or req_position_type == "Exit_short":
                    print("TRYING TO EXIT.....................")

                    if req_position_type == "Exit_long":
                        side = "Sell"
                    elif req_position_type == "Exit_short":
                        side = "Buy"

                    exit_order(side, FUTURES_SYMBOL, FUTURES_EXIT, req_order_time_out, req_base_coin)


            except:
                error_occured_time = datetime.now(IST)
                error_occured = "Error in Initiating Futures Order!"
                cursor.execute(
                    "insert into bybit_futures_e_log(occured_time, error_description) values (%s, %s)",
                    [error_occured_time, error_occured])
                conn.commit()

        try:
            if req_trade_type == "Spot":

                if bybit_api_key and bybit_api_secret != "":
                    try:
                        session = pybit.spot.HTTP(base_url, bybit_api_key, bybit_api_secret)
                    except:
                        print("Alert failed due to invalid keys")

                try:
                    try:
                        req_base_coin = alert_response["base_coin"]
                    except Exception as e:
                        print(e)
                        error_occured_time = datetime.now(IST)
                        error_occured = "Invalid/Empty base coin"
                        cursor.execute("insert into bybit_error_log(occured_time, error_description) values (%s, %s)",
                                       [error_occured_time, error_occured])
                        conn.commit()

                    try:
                        req_coin_pair = alert_response["coin_pair"]
                    except Exception as e:
                        print(e)
                        error_occured_time = datetime.now(IST)
                        error_occured = "Invalid/Empty coin pair"
                        cursor.execute("insert into bybit_error_log(occured_time, error_description) values (%s, %s)",
                                       [error_occured_time, error_occured])
                        conn.commit()

                    req_entry_type = alert_response["entry_type"].title()
                    req_exit_type = alert_response["exit_type"].title()
                    req_margin_mode = alert_response["margin_mode"]
                    req_long_leverage = float(alert_response["long_leverage"])
                    req_short_leverage = float(alert_response["short_leverage"])

                    try:
                        req_qty_type = alert_response["qty_type"]
                    except Exception as e:
                        print(e)
                        error_occured_time = datetime.now(IST)
                        error_occured = "Invalid/Empty qty type"
                        cursor.execute("insert into bybit_error_log(occured_time, error_description) values (%s, %s)",
                                       [error_occured_time, error_occured])
                        conn.commit()

                    try:
                        req_qty = float(alert_response["qty"])
                    except Exception as e:
                        print(e)
                        error_occured_time = datetime.now(IST)
                        error_occured = "Invalid/Empty qty"
                        cursor.execute("insert into bybit_error_log(occured_time, error_description) values (%s, %s)",
                                       [error_occured_time, error_occured])
                        conn.commit()

                    req_long_leverage = alert_response["long_leverage"]
                    req_short_leverage = alert_response["short_leverage"]

                    req_long_stop_loss_percent = (float(alert_response["long_stop_loss_percent"])) / 100
                    req_long_take_profit_percent = (float(alert_response["long_take_profit_percent"])) / 100
                    req_short_stop_loss_percent = (float(alert_response["short_stop_loss_percent"])) / 100
                    req_short_take_profit_percent = (float(alert_response["short_take_profit_percent"])) / 100
                    print(f"req short tp = {req_short_take_profit_percent}")
                    req_multi_tp = alert_response["enable_multi_tp"]

                    req_tp1_qty_size = (float(alert_response["tp_1_pos_size"])) / 100
                    req_tp2_qty_size = (float(alert_response["tp_2_pos_size"])) / 100
                    req_tp3_qty_size = (float(alert_response["tp_3_pos_size"])) / 100

                    req_tp1_percent = (float(alert_response["tp1_percent"])) / 100
                    req_tp2_percent = (float(alert_response["tp2_percent"])) / 100
                    req_tp3_percent = (float(alert_response["tp3_percent"])) / 100

                    req_stop_bot_balance = float(alert_response["stop_bot_below_balance"])
                    req_order_time_out = float(alert_response["order_time_out"])

                    try:
                        req_position_type = alert_response["position_type"]
                    except Exception as e:
                        print(e)
                        error_occured_time = datetime.now(IST)
                        error_occured = "Invalid/Empty position type"
                        cursor.execute("insert into bybit_error_log(occured_time, error_description) values (%s, %s)",
                                       [error_occured_time, error_occured])
                        conn.commit()
                except Exception as e:
                    print(e)
                    error_occured_time = datetime.now(IST)
                    error_occured = "Error in parsing json alert"
                    cursor.execute("insert into bybit_error_log(occured_time, error_description) values (%s, %s)",
                                   [error_occured_time, error_occured])
                    conn.commit()

                SPOT_SYMBOL = req_coin_pair
                SPOT_ENTRY = req_entry_type
                SPOT_EXIT = req_exit_type

                # Check usdt balance in spot wallet
                def check_base_coin_balance():
                    # Fetch wallet balance
                    wallet = session.get_wallet_balance(coin=req_base_coin)
                    wallet_in = wallet['result']['balances']
                    for coin in wallet_in:
                        if coin["coin"] == req_base_coin:
                            base_coin_bal = float(coin["total"])
                            print(f"Spot balance = {base_coin_bal}")
                        else:
                            base_coin_bal = 0
                    return base_coin_bal

                def calculate_buy_qty_with_precision(SPOT_SYMBOL, qty_in_base_coin):
                    symbol_data = (session.latest_information_for_symbol(symbol=SPOT_SYMBOL))
                    current_market_price = float(symbol_data['result']['lastPrice'])

                    tradeable_qty = qty_in_base_coin / current_market_price

                    data = session.query_symbol()

                    for data in data['result']:
                        if data["name"] == SPOT_SYMBOL:
                            stepSize = float(data["minTradeQuantity"])
                            print(f"step size = {stepSize}")
                            d = decimal.Decimal(str(stepSize))
                            quantity_precision = abs(d.as_tuple().exponent)
                            print("quantity_precision: " + str(quantity_precision))
                            break

                    BUY_QUANTITY = math.floor((
                                                  tradeable_qty) * 10 ** quantity_precision) / 10 ** quantity_precision  # quantity_precision = truncate_num
                    print(f"buy qty = {BUY_QUANTITY}")
                    return BUY_QUANTITY

                def calculate_sell_qty_with_precision(SPOT_SYMBOL, buy_qty):
                    data = session.query_symbol()

                    for data in data['result']:
                        if data["name"] == SPOT_SYMBOL:
                            stepSize = float(data["minTradeQuantity"])
                            print(f"step size = {stepSize}")
                            d = decimal.Decimal(str(stepSize))
                            quantity_precision = abs(d.as_tuple().exponent)
                            print("quantity_precision: " + str(quantity_precision))
                            break

                    SELL_QUANTITY = math.floor((
                                                   buy_qty) * 10 ** quantity_precision) / 10 ** quantity_precision  # quantity_precision = truncate_num
                    print(f"sell qty = {SELL_QUANTITY}")
                    return SELL_QUANTITY

                def trunc_calculate_sell_qty_with_precision(SPOT_SYMBOL, buy_qty):
                    sellable_qty_after_fees = float(buy_qty) * 0.998

                    data = session.query_symbol()

                    for data in data['result']:
                        if data["name"] == SPOT_SYMBOL:
                            stepSize = float(data["minTradeQuantity"])
                            print(f"step size = {stepSize}")
                            d = decimal.Decimal(str(stepSize))
                            quantity_precision = abs(d.as_tuple().exponent)
                            print("quantity_precision: " + str(quantity_precision))
                            break

                    SELL_QUANTITY = math.floor((
                                                   sellable_qty_after_fees) * 10 ** quantity_precision) / 10 ** quantity_precision  # quantity_precision = truncate_num
                    print(f"sell qty = {SELL_QUANTITY}")
                    return SELL_QUANTITY

                def cal_price_with_precision(SPOT_SYMBOL, input_price):
                    data = session.query_symbol()

                    for data in data['result']:
                        if data["name"] == SPOT_SYMBOL:
                            stepSize = float(data["minPricePrecision"])
                            print(f"step size = {stepSize}")
                            d = decimal.Decimal(str(stepSize))
                            price_precision = abs(d.as_tuple().exponent)
                            print("price_precision: " + str(price_precision))
                            break
                    price = round(input_price, price_precision)
                    return price

                def get_current_open_orders(SPOT_SYMBOL):
                    oo_id_list = []
                    current_open_orders = session.query_active_order()

                    for oo in current_open_orders["result"]["list"]:
                        if oo["symbol"] == SPOT_SYMBOL:
                            oo_id_list.append(oo["orderId"])

                    return oo_id_list

                if req_qty_type == "Percentage":
                    current_bal = check_base_coin_balance()
                    qty_in_base_coin = current_bal * req_qty
                elif req_qty_type == "Fixed":
                    qty_in_base_coin = req_qty

                def execute_limit_oco_order(SPOT_SIDE, req_position_type, BUY_ORDER_ID, SPOT_SYMBOL, SPOT_SELL_QUANTITY,
                                            TAKE_PROFIT_PRICE_FINAL, STOP_LOSS_PRICE_FINAL, SPOT_ENTRY, req_multi_tp,
                                            req_qty_size, req_order_time_out,tp_type):
                    SPOT_EXIT = "Limit"
                    print(SPOT_SIDE)

                    # STOP_LOSS_PRICE_FINAL_S = cal_price_with_precision(SPOT_SYMBOL=SPOT_SYMBOL,input_price=(STOP_LOSS_PRICE_FINAL * 0.9999))
                    STOP_LOSS_PRICE_FINAL_B = cal_price_with_precision(SPOT_SYMBOL=SPOT_SYMBOL,
                                                                       input_price=(STOP_LOSS_PRICE_FINAL * 1.0009))

                    oco_order_ids = []

                    try:
                        if SPOT_SIDE == "Sell":
                            limit_tp_order = session.place_active_order(symbol=SPOT_SYMBOL, orderQty=SPOT_SELL_QUANTITY,
                                                                        side="Sell", orderType="MARKET",
                                                                        timeInForce="GTC", orderCategory=1,
                                                                        triggerPrice=TAKE_PROFIT_PRICE_FINAL)
                            o_tp_id_for_table = limit_tp_order["result"]["orderId"]
                            oco_order_ids.append(o_tp_id_for_table)
                            limit_sl_order = session.place_active_order(symbol=SPOT_SYMBOL, orderQty=SPOT_SELL_QUANTITY,
                                                                        side="Sell", orderType="MARKET",
                                                                        timeInForce="GTC",
                                                                        orderCategory=1,
                                                                        triggerPrice=STOP_LOSS_PRICE_FINAL)
                            o_sl_id_for_table = limit_sl_order["result"]["orderId"]
                            oco_order_ids.append(o_sl_id_for_table)

                            cursor.execute("select entry_price from bybit_long_entry where symbol = %s", [SPOT_SYMBOL])
                            r_3 = cursor.fetchall()
                            price_results = r_3[0][0]
                            p_for_table = float(price_results)

                            cursor.execute("insert into bybit_s_id_list(order_id, entry_price) values (%s, %s)",
                                           [o_tp_id_for_table, p_for_table])
                            conn.commit()

                            cursor.execute("insert into bybit_s_id_list(order_id, entry_price) values (%s, %s)",
                                           [o_sl_id_for_table, p_for_table])
                            conn.commit()

                        if SPOT_SIDE == "Buy":
                            limit_tp_order = session.place_active_order(symbol=SPOT_SYMBOL, orderQty=SPOT_SELL_QUANTITY,
                                                                        side="Buy", orderType="MARKET",
                                                                        timeInForce="GTC",
                                                                        orderCategory=1,
                                                                        triggerPrice=TAKE_PROFIT_PRICE_FINAL)
                            o_tp_id_for_table = limit_tp_order["result"]["orderId"]
                            oco_order_ids.append(o_tp_id_for_table)

                            limit_sl_order = session.place_active_order(symbol=SPOT_SYMBOL, orderQty=SPOT_SELL_QUANTITY,
                                                                        side="Buy", orderType="MARKET",
                                                                        timeInForce="GTC",
                                                                        orderCategory=1,
                                                                        triggerPrice=STOP_LOSS_PRICE_FINAL_B)
                            o_sl_id_for_table = limit_sl_order["result"]["orderId"]
                            oco_order_ids.append(o_sl_id_for_table)

                            cursor.execute("select entry_price from bybit_short_entry where symbol = %s", [SPOT_SYMBOL])
                            r_3 = cursor.fetchall()
                            price_results = r_3[0][0]
                            p_for_table = float(price_results)

                            cursor.execute("insert into bybit_s_id_list(order_id, entry_price) values (%s, %s)",
                                           [o_tp_id_for_table, p_for_table])
                            conn.commit()

                            cursor.execute("insert into bybit_s_id_list(order_id, entry_price) values (%s, %s)",
                                           [o_sl_id_for_table, p_for_table])
                            conn.commit()

                    except Exception as e:

                        error_occured = f"{e}"
                        print(error_occured)

                        error_occured_time = datetime.now(IST)

                        cursor.execute(
                            "insert into bybit_error_log(symbol, order_action, entry_order_type, exit_order_type, quantity, occured_time, error_description) values (%s, %s, %s, %s, %s, %s, %s)",
                            [SPOT_SYMBOL, SPOT_SIDE, SPOT_ENTRY, SPOT_EXIT, SPOT_SELL_QUANTITY, error_occured_time,
                             error_occured])
                        conn.commit()

                    def add_to_trade_oco():
                        while True:
                            time.sleep(4)
                            try:
                                for order_id in oco_order_ids:
                                    active_order = session.get_active_order(orderCategory=1)
                                    for act_or in active_order["result"]:
                                        if act_or["orderId"] == order_id:
                                            active_order_status = act_or["status"]
                                            if active_order_status == "ORDER_FILLED":
                                                filled_or_id = order_id
                                                print("Filled")
                                                break
                                if active_order_status == "ORDER_FILLED":
                                    break
                            except Exception as e:
                                print(e)
                                pass
                        if active_order_status == "ORDER_FILLED":
                            oco_order_ids.remove(filled_or_id)
                            oco_limit_sell_order = active_order
                            print(f"oco limit sell order = {oco_limit_sell_order}")

                            for id in oco_order_ids:
                                cancel_unfilled_order = session.cancel_active_order(orderId=order_id, orderCategory=1)

                        if filled_or_id == o_tp_id_for_table:
                            if tp_type == "None":
                                execution = "Executed for Take Profit"
                            if tp_type == "One":
                                execution = "Executed for Take Profit 1"
                            if tp_type == "Two":
                                execution = "Executed for Take Profit 2"
                            if tp_type == "Three":
                                execution = "Executed for Take Profit 3"
                        if filled_or_id == o_sl_id_for_table:
                            execution = "Executed for Stop Loss"

                        try:
                            OCO_SELL_ORDER_ID = oco_limit_sell_order["orderId"]
                            OCO_SELL_ORDER_SYMBOL = oco_limit_sell_order["symbol"]
                            OCO_SELL_ORDER_QTY = float(oco_limit_sell_order["executedQty"])
                            sell_cum_qty = float(oco_limit_sell_order["cummulativeQuoteQty"])
                            TOTAL_SELL_SPEND = (sell_cum_qty / 100) * 99.9
                            TOTAL_BUY_SPEND = float(oco_limit_sell_order["cummulativeQuoteQty"])
                            OCO_SELL_ORDER_PRICE = round((float(oco_limit_sell_order["cummulativeQuoteQty"]) / float(
                                oco_limit_sell_order["executedQty"])), 3)
                            OCO_SELL_ORDER_ACTION = oco_limit_sell_order["side"]
                            OCO_SELL_ORDER_TYPE = oco_limit_sell_order["type"]
                            sell_order_executed_time = datetime.now(IST)

                            if req_position_type == "Enter_long":
                                cursor.execute("select total_spend from bybit_id_list where order_id = %s",
                                               [BUY_ORDER_ID])
                                r_2 = cursor.fetchall()
                                price_results = r_2[0][0]
                                total_buy_spend = float(price_results)
                                print(f"Total buy spend from DB= {total_buy_spend}")

                                if req_multi_tp == "No":
                                    OCO_SELL_PNL = round((TOTAL_SELL_SPEND - total_buy_spend), 2)
                                    oco_sell_per = (OCO_SELL_PNL / total_buy_spend) * 100
                                    OCO_SELL_PNL_PERCENTAGE = str((round(oco_sell_per, 2))) + "%"
                                if req_multi_tp == "Yes":
                                    buy_spend_per = float(total_buy_spend) * float(req_qty_size)
                                    OCO_SELL_PNL = round((TOTAL_SELL_SPEND - buy_spend_per), 2)
                                    oco_sell_per = (OCO_SELL_PNL / buy_spend_per) * 100
                                    OCO_SELL_PNL_PERCENTAGE = str((round(oco_sell_per, 2))) + "%"

                                cursor.execute(sql.SQL(
                                    "insert into bybit_trade_log(date_time, symbol, order_id, order_action, order_type, executed_price, executed_qty,execution, pnl, percentage) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"),
                                    [sell_order_executed_time, OCO_SELL_ORDER_SYMBOL, OCO_SELL_ORDER_ID,
                                     OCO_SELL_ORDER_ACTION, OCO_SELL_ORDER_TYPE, OCO_SELL_ORDER_PRICE,
                                     OCO_SELL_ORDER_QTY, execution, OCO_SELL_PNL, OCO_SELL_PNL_PERCENTAGE])
                                conn.commit()

                            if req_position_type == "Exit_long":
                                cursor.execute("select qty from bybit_long_entry where symbol = %s", [SPOT_SYMBOL])
                                r_3 = cursor.fetchall()
                                price_results = r_3[0][0]
                                previous_long_entry_qty = float(price_results)
                                print(f"previous_long_entry_qty = {previous_long_entry_qty}")

                                cursor.execute("select total_spend from bybit_long_entry where symbol = %s",
                                               [SPOT_SYMBOL])
                                r_3 = cursor.fetchall()
                                price_results = r_3[0][0]
                                previous_long_entry_spend = float(price_results)
                                print(f"previous_long_entry_spend = {previous_long_entry_spend}")

                                proportional_buy_spend = (
                                                                 previous_long_entry_spend / previous_long_entry_qty) * OCO_SELL_ORDER_QTY
                                OCO_SELL_PNL = round((TOTAL_SELL_SPEND - proportional_buy_spend), 2)
                                oco_sell_per = (OCO_SELL_PNL / proportional_buy_spend) * 100
                                OCO_SELL_PNL_PERCENTAGE = str((round(oco_sell_per, 2))) + "%"

                                cursor.execute(sql.SQL(
                                    "insert into bybit_trade_log(date_time, symbol, order_id, order_action, order_type, executed_price, executed_qty, execution, pnl, percentage) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"),
                                    [sell_order_executed_time, OCO_SELL_ORDER_SYMBOL, OCO_SELL_ORDER_ID,
                                     OCO_SELL_ORDER_ACTION, OCO_SELL_ORDER_TYPE, OCO_SELL_ORDER_PRICE,
                                     OCO_SELL_ORDER_QTY, execution, OCO_SELL_PNL, OCO_SELL_PNL_PERCENTAGE])
                                conn.commit()

                            if req_position_type == "Enter_short":

                                cursor.execute("select exists (select 1 from bybit_short_entry)")
                                r_1 = cursor.fetchall()
                                live_r = r_1[0][0]

                                if live_r == False:
                                    cursor.execute(sql.SQL(
                                        "insert into bybit_short_entry(order_id, entry_price, total_spend, symbol, qty) values (%s, %s, %s, %s, %s)"),
                                        [OCO_SELL_ORDER_ID, OCO_SELL_ORDER_PRICE, TOTAL_SELL_SPEND,
                                         OCO_SELL_ORDER_SYMBOL, OCO_SELL_ORDER_QTY])
                                    conn.commit()
                                if live_r == True:
                                    cursor.execute(
                                        "update bybit_short_entry set order_id = %s, entry_price = %s, total_spend = %s, symbol = %s, qty = %s",
                                        [OCO_SELL_ORDER_ID, OCO_SELL_ORDER_PRICE, TOTAL_SELL_SPEND,
                                         OCO_SELL_ORDER_SYMBOL,
                                         OCO_SELL_ORDER_QTY])
                                    conn.commit()
                                    print("Records inserted")

                                cursor.execute(sql.SQL(
                                    "insert into bybit_trade_log(date_time, symbol, order_id, order_action, order_type, executed_price, executed_qty,execution) values (%s, %s, %s, %s, %s, %s, %s, %s)"),
                                    [sell_order_executed_time, OCO_SELL_ORDER_SYMBOL, OCO_SELL_ORDER_ID,
                                     OCO_SELL_ORDER_ACTION, OCO_SELL_ORDER_TYPE, OCO_SELL_ORDER_PRICE,
                                     OCO_SELL_ORDER_QTY, execution])
                                conn.commit()

                            if req_position_type == "Exit_short":
                                cursor.execute("select total_spend from bybit_short_entry where symbol = %s",
                                               [SPOT_SYMBOL])
                                r_3 = cursor.fetchall()
                                price_results = r_3[0][0]
                                previous_short_entry_income = float(price_results)
                                print(f"previous_short_entry_price = {previous_short_entry_income}")

                                cursor.execute("select qty from bybit_short_entry where symbol = %s", [SPOT_SYMBOL])
                                r_3 = cursor.fetchall()
                                price_results = r_3[0][0]
                                previous_short_entry_qty = float(price_results)
                                print(f"previous_short_entry_price = {previous_short_entry_qty}")

                                actual_sell_income = (previous_short_entry_income / 100) * 99.9
                                proportional_sell_income = (
                                                                   actual_sell_income / previous_short_entry_qty) * OCO_SELL_ORDER_QTY
                                OCO_SELL_PNL = round((proportional_sell_income - TOTAL_BUY_SPEND), 2)
                                oco_sell_per = (OCO_SELL_PNL / proportional_sell_income) * 100
                                OCO_SELL_PNL_PERCENTAGE = str((round(oco_sell_per, 2))) + "%"

                                cursor.execute(sql.SQL(
                                    "insert into bybit_trade_log(date_time, symbol, order_id, order_action, order_type, executed_price, executed_qty, execution,pnl, percentage) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"),
                                    [sell_order_executed_time, OCO_SELL_ORDER_SYMBOL, OCO_SELL_ORDER_ID,
                                     OCO_SELL_ORDER_ACTION,
                                     OCO_SELL_ORDER_TYPE, OCO_SELL_ORDER_PRICE, OCO_SELL_ORDER_QTY, execution,
                                     OCO_SELL_PNL,
                                     OCO_SELL_PNL_PERCENTAGE])
                                conn.commit()


                        except Exception as e:
                            print(e)

                    t22 = threading.Thread(target=add_to_trade_oco)
                    t22.start()

                def execute_limit_stop_loss_order(SPOT_SIDE, req_position_type, BUY_ORDER_ID, SPOT_SYMBOL,
                                                  SPOT_SELL_QUANTITY, STOP_LOSS_PRICE_FINAL, SPOT_ENTRY,
                                                  req_order_time_out):
                    print(SPOT_SIDE)
                    SPOT_EXIT = "Limit"

                    STOP_LOSS_PRICE_FINAL_A = cal_price_with_precision(SPOT_SYMBOL=SPOT_SYMBOL,
                                                                       input_price=(STOP_LOSS_PRICE_FINAL * 0.9999))

                    try:
                        limit_stop_loss_order = session.place_active_order(symbol=SPOT_SYMBOL,
                                                                           orderQty=SPOT_SELL_QUANTITY,
                                                                           side=SPOT_SIDE, orderType="MARKET",
                                                                           timeInForce="GTC",
                                                                           orderCategory=1,
                                                                           triggerPrice=STOP_LOSS_PRICE_FINAL_A)
                        print(f"limit stop loss order = {limit_stop_loss_order}")

                        if SPOT_SIDE == "Buy":
                            o_id_for_table = limit_stop_loss_order["result"]["orderId"]
                            cursor.execute("select entry_price from bybit_short_entry where symbol = %s", [SPOT_SYMBOL])
                            r_3 = cursor.fetchall()
                            price_results = r_3[0][0]
                            p_for_table = float(price_results)

                            cursor.execute("insert into bybit_s_id_list(order_id, entry_price) values (%s, %s)",
                                           [o_id_for_table, p_for_table])
                            conn.commit()
                        if SPOT_SIDE == "Sell":
                            o_id_for_table = limit_stop_loss_order["result"]["orderId"]
                            cursor.execute("select entry_price from bybit_long_entry where symbol = %s", [SPOT_SYMBOL])
                            r_3 = cursor.fetchall()
                            price_results = r_3[0][0]
                            p_for_table = float(price_results)

                            cursor.execute("insert into bybit_s_id_list(order_id, entry_price) values (%s, %s)",
                                           [o_id_for_table, p_for_table])
                            conn.commit()

                    except Exception as e:
                        error_occured = f"{e}"
                        print(error_occured)
                        error_occured_time = datetime.now(IST)

                        cursor.execute(
                            "insert into bybit_error_log(symbol, order_action, entry_order_type, exit_order_type, quantity, occured_time, error_description) values (%s, %s, %s, %s, %s, %s, %s)",
                            [SPOT_SYMBOL, SPOT_SIDE, SPOT_ENTRY, SPOT_EXIT, SPOT_SELL_QUANTITY, error_occured_time,
                             error_occured])
                        conn.commit()

                    limit_stop_loss_order_ID = limit_stop_loss_order["result"]["orderId"]
                    print(limit_stop_loss_order_ID)

                    def add_to_trade_sl():

                        while True:
                            time.sleep(4)
                            try:
                                active_order = session.get_active_order(orderCategory=1)
                                for act_or in active_order["result"]:
                                    if act_or["orderId"] == limit_stop_loss_order_ID:
                                        active_order_status = act_or["status"]
                                        if active_order_status == "ORDER_FILLED":
                                            print("Filled")
                                            break
                                if active_order_status == "ORDER_FILLED":
                                    break
                            except Exception as e:
                                print(e)
                                pass
                        if active_order_status == "ORDER_FILLED":
                            enter_long_sell_stop_loss_order = active_order
                            print(f"enter long sell stop loss order={enter_long_sell_stop_loss_order}")

                        execution = "Executed for Stop Loss"

                        try:
                            STOP_LOSS_SELL_ORDER_ID = enter_long_sell_stop_loss_order["orderId"]
                            STOP_LOSS_SELL_ORDER_SYMBOL = enter_long_sell_stop_loss_order["symbol"]
                            STOP_LOSS_SELL_ORDER_QTY = float(enter_long_sell_stop_loss_order["executedQty"])
                            sell_cum_qty = float(enter_long_sell_stop_loss_order["cummulativeQuoteQty"])
                            TOTAL_SELL_SPEND = (sell_cum_qty / 100) * 99.9
                            TOTAL_BUY_SPEND = float(enter_long_sell_stop_loss_order["cummulativeQuoteQty"])
                            STOP_LOSS_SELL_ORDER_PRICE = round((float(
                                enter_long_sell_stop_loss_order["cummulativeQuoteQty"]) / float(
                                enter_long_sell_stop_loss_order["executedQty"])), 3)
                            STOP_LOSS_SELL_ORDER_ACTION = enter_long_sell_stop_loss_order["side"]
                            STOP_LOSS_SELL_ORDER_TYPE = enter_long_sell_stop_loss_order["type"]
                            sell_order_executed_time = datetime.now(IST)

                            if req_position_type == "Enter_long":
                                cursor.execute("select total_spend from bybit_id_list where order_id = %s",
                                               [BUY_ORDER_ID])
                                r_2 = cursor.fetchall()
                                price_results = r_2[0][0]
                                total_buy_spend = float(price_results)

                                STOP_LOSS_SELL_PNL = round((TOTAL_SELL_SPEND - total_buy_spend), 2)
                                stop_loss_sell_per = (STOP_LOSS_SELL_PNL / total_buy_spend) * 100
                                STOP_LOSS_SELL_PNL_PERCENTAGE = str((round(stop_loss_sell_per, 2))) + "%"

                                cursor.execute(sql.SQL(
                                    "insert into bybit_trade_log(date_time, symbol, order_id, order_action, order_type, executed_price, executed_qty, execution,pnl, percentage) values (%s, %s, %s, %s, %s, %s, %s, %s, %s,%s)"),
                                    [sell_order_executed_time, STOP_LOSS_SELL_ORDER_SYMBOL, STOP_LOSS_SELL_ORDER_ID,
                                     STOP_LOSS_SELL_ORDER_ACTION, STOP_LOSS_SELL_ORDER_TYPE, STOP_LOSS_SELL_ORDER_PRICE,
                                     STOP_LOSS_SELL_ORDER_QTY, execution, STOP_LOSS_SELL_PNL,
                                     STOP_LOSS_SELL_PNL_PERCENTAGE])
                                conn.commit()

                            if req_position_type == "Exit_long":
                                cursor.execute("select qty from bybit_long_entry where symbol = %s", [SPOT_SYMBOL])
                                r_3 = cursor.fetchall()
                                price_results = r_3[0][0]
                                previous_long_entry_qty = float(price_results)
                                print(f"previous_long_entry_qty = {previous_long_entry_qty}")

                                cursor.execute("select total_spend from bybit_long_entry where symbol = %s",
                                               [SPOT_SYMBOL])
                                r_3 = cursor.fetchall()
                                price_results = r_3[0][0]
                                previous_long_entry_spend = float(price_results)
                                print(f"previous_long_entry_spend = {previous_long_entry_spend}")

                                proportional_buy_spend = (
                                                                 previous_long_entry_spend / previous_long_entry_qty) * STOP_LOSS_SELL_ORDER_QTY
                                STOP_LOSS_SELL_PNL = round((TOTAL_SELL_SPEND - proportional_buy_spend), 2)
                                sl_sell_per = (STOP_LOSS_SELL_PNL / proportional_buy_spend) * 100
                                STOP_LOSS_SELL_PNL_PERCENTAGE = str((round(sl_sell_per, 2))) + "%"

                                cursor.execute(sql.SQL(
                                    "insert into bybit_trade_log(date_time, symbol, order_id, order_action, order_type, executed_price, executed_qty, execution, pnl, percentage) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"),
                                    [sell_order_executed_time, STOP_LOSS_SELL_ORDER_SYMBOL,
                                     STOP_LOSS_SELL_ORDER_ID, STOP_LOSS_SELL_ORDER_ACTION,
                                     STOP_LOSS_SELL_ORDER_TYPE, STOP_LOSS_SELL_ORDER_PRICE,
                                     STOP_LOSS_SELL_ORDER_QTY, execution, STOP_LOSS_SELL_PNL,
                                     STOP_LOSS_SELL_PNL_PERCENTAGE])
                                conn.commit()

                            if req_position_type == "Enter_short":

                                cursor.execute("select exists (select 1 from bybit_short_entry)")
                                r_1 = cursor.fetchall()
                                live_r = r_1[0][0]

                                if live_r == False:
                                    cursor.execute(sql.SQL(
                                        "insert into bybit_short_entry(order_id, entry_price, total_spend, symbol, qty) values (%s, %s, %s, %s, %s)"),
                                        [STOP_LOSS_SELL_ORDER_ID, STOP_LOSS_SELL_ORDER_PRICE, TOTAL_SELL_SPEND,
                                         STOP_LOSS_SELL_ORDER_SYMBOL, STOP_LOSS_SELL_ORDER_QTY])
                                    conn.commit()
                                if live_r == True:
                                    cursor.execute(
                                        "update bybit_short_entry set order_id = %s, entry_price = %s, total_spend = %s, symbol = %s, qty = %s",
                                        [STOP_LOSS_SELL_ORDER_ID, STOP_LOSS_SELL_ORDER_PRICE, TOTAL_SELL_SPEND,
                                         STOP_LOSS_SELL_ORDER_SYMBOL, STOP_LOSS_SELL_ORDER_QTY])
                                    conn.commit()
                                    print("Records inserted")

                                cursor.execute(sql.SQL(
                                    "insert into bybit_trade_log(date_time, symbol, order_id, order_action, order_type, executed_price, executed_qty,execution) values (%s, %s, %s, %s, %s, %s, %s,%s)"),
                                    [sell_order_executed_time, STOP_LOSS_SELL_ORDER_SYMBOL, STOP_LOSS_SELL_ORDER_ID,
                                     STOP_LOSS_SELL_ORDER_ACTION, STOP_LOSS_SELL_ORDER_TYPE, STOP_LOSS_SELL_ORDER_PRICE,
                                     STOP_LOSS_SELL_ORDER_QTY, execution])
                                conn.commit()

                            if req_position_type == "Exit_short":
                                cursor.execute("select total_spend from bybit_short_entry where symbol = %s",
                                               [SPOT_SYMBOL])
                                r_3 = cursor.fetchall()
                                price_results = r_3[0][0]
                                previous_short_entry_income = float(price_results)
                                print(f"previous_short_entry_price = {previous_short_entry_income}")

                                cursor.execute("select qty from bybit_short_entry where symbol = %s", [SPOT_SYMBOL])
                                r_3 = cursor.fetchall()
                                price_results = r_3[0][0]
                                previous_short_entry_qty = float(price_results)
                                print(f"previous_short_entry_price = {previous_short_entry_qty}")

                                actual_sell_income = (previous_short_entry_income / 100) * 99.9
                                proportional_sell_income = (
                                                                   actual_sell_income / previous_short_entry_qty) * STOP_LOSS_SELL_ORDER_QTY
                                STOP_LOSS_SELL_PNL = round((proportional_sell_income - TOTAL_BUY_SPEND), 2)
                                sl_sell_per = (STOP_LOSS_SELL_PNL / proportional_sell_income) * 100
                                STOP_LOSS_SELL_PNL_PERCENTAGE = str((round(sl_sell_per, 2))) + "%"

                                cursor.execute(sql.SQL(
                                    "insert into bybit_trade_log(date_time, symbol, order_id, order_action, order_type, executed_price, executed_qty, execution,pnl, percentage) values (%s, %s, %s, %s, %s, %s, %s, %s, %s,%s)"),
                                    [sell_order_executed_time, STOP_LOSS_SELL_ORDER_SYMBOL, STOP_LOSS_SELL_ORDER_ID,
                                     STOP_LOSS_SELL_ORDER_ACTION, STOP_LOSS_SELL_ORDER_TYPE, STOP_LOSS_SELL_ORDER_PRICE,
                                     STOP_LOSS_SELL_ORDER_QTY, execution, STOP_LOSS_SELL_PNL,
                                     STOP_LOSS_SELL_PNL_PERCENTAGE])
                                conn.commit()

                        except Exception as e:
                            print(e)

                    t20 = threading.Thread(target=add_to_trade_sl)
                    t20.start()

                def execute_limit_take_profit_order(SPOT_SIDE, req_position_type, BUY_ORDER_ID, SPOT_SYMBOL,
                                                    SPOT_SELL_QUANTITY, TAKE_PROFIT_PRICE_FINAL, SPOT_ENTRY,
                                                    req_multi_tp,
                                                    req_qty_size, req_order_time_out,tp_type):
                    print(SPOT_SIDE)
                    SPOT_EXIT = "Limit"

                    try:
                        limit_take_proft_order = session.place_active_order(symbol=SPOT_SYMBOL,
                                                                            orderQty=SPOT_SELL_QUANTITY,
                                                                            side=SPOT_SIDE, orderType="MARKET",
                                                                            timeInForce="GTC",
                                                                            orderCategory=1,
                                                                            triggerPrice=TAKE_PROFIT_PRICE_FINAL)

                        if SPOT_SIDE == "Buy":
                            o_id_for_table = limit_take_proft_order["result"]["orderId"]
                            cursor.execute("select entry_price from bybit_short_entry where symbol = %s", [SPOT_SYMBOL])
                            r_3 = cursor.fetchall()
                            price_results = r_3[0][0]
                            p_for_table = float(price_results)

                            cursor.execute("insert into bybit_s_id_list(order_id, entry_price) values (%s, %s)",
                                           [o_id_for_table, p_for_table])
                            conn.commit()
                        if SPOT_SIDE == "Sell":
                            o_id_for_table = limit_take_proft_order["orderId"]
                            cursor.execute("select entry_price from bybit_long_entry where symbol = %s", [SPOT_SYMBOL])
                            r_3 = cursor.fetchall()
                            price_results = r_3[0][0]
                            p_for_table = float(price_results)

                            cursor.execute("insert into bybit_s_id_list(order_id, entry_price) values (%s, %s)",
                                           [o_id_for_table, p_for_table])
                            conn.commit()


                    except Exception as e:
                        error_occured = f"{e}"
                        print(error_occured)
                        error_occured_time = datetime.now(IST)

                        cursor.execute(
                            "insert into bybit_error_log(symbol, order_action, entry_order_type, exit_order_type, quantity, occured_time, error_description) values (%s, %s, %s, %s, %s, %s, %s)",
                            [SPOT_SYMBOL, SPOT_SIDE, SPOT_ENTRY, SPOT_EXIT, SPOT_SELL_QUANTITY, error_occured_time,
                             error_occured])
                        conn.commit()

                    limit_take_proft_order_ID = limit_take_proft_order["result"]["orderId"]
                    print(limit_take_proft_order_ID)

                    def add_to_trade_tp():
                        while True:
                            time.sleep(4)
                            try:
                                time.sleep(1)
                                active_order = session.get_active_order(orderCategory=1)
                                for act_or in active_order["result"]:
                                    if act_or["orderId"] == limit_take_proft_order_ID:
                                        active_order_status = act_or["status"]
                                        if active_order_status == "ORDER_FILLED":
                                            print("Filled")
                                            break
                                if active_order_status == "ORDER_FILLED":
                                    break
                            except Exception as e:
                                print(e)
                                pass
                        if active_order_status == "ORDER_FILLED":
                            enter_long_take_profit_order = active_order
                            print(f"enter long take profit order = {enter_long_take_profit_order}")

                        if tp_type == "None":
                            execution = "Executed for Take Profit"
                        if tp_type == "One":
                            execution = "Executed for Take Profit 1"
                        if tp_type == "Two":
                            execution = "Executed for Take Profit 2"
                        if tp_type == "Three":
                            execution = "Executed for Take Profit 3"

                        try:
                            TAKE_PROFIT_SELL_ORDER_ID = enter_long_take_profit_order["orderId"]
                            TAKE_PROFIT_SELL_ORDER_SYMBOL = enter_long_take_profit_order["symbol"]
                            TAKE_PROFIT_SELL_ORDER_QTY = float(enter_long_take_profit_order["executedQty"])
                            sell_cum_qty = float(enter_long_take_profit_order["cummulativeQuoteQty"])
                            TOTAL_SELL_SPEND = (sell_cum_qty / 100) * 99.9
                            TOTAL_BUY_SPEND = float(enter_long_take_profit_order["cummulativeQuoteQty"])
                            TAKE_PROFIT_SELL_ORDER_PRICE = round((float(
                                enter_long_take_profit_order["cummulativeQuoteQty"]) / float(
                                enter_long_take_profit_order["executedQty"])), 3)
                            TAKE_PROFIT_SELL_ORDER_ACTION = enter_long_take_profit_order["side"]
                            TAKE_PROFIT_SELL_ORDER_TYPE = enter_long_take_profit_order["type"]
                            sell_order_executed_time = datetime.now(IST)

                            if req_position_type == "Enter_long":
                                cursor.execute("select total_spend from bybit_id_list where order_id = %s",
                                               [BUY_ORDER_ID])
                                r_2 = cursor.fetchall()
                                price_results = r_2[0][0]
                                total_buy_spend = float(price_results)

                                if req_multi_tp == "No":
                                    TAKE_PROFIT_SELL_PNL = round((TOTAL_SELL_SPEND - total_buy_spend), 2)
                                    take_profit_sell_per = (TAKE_PROFIT_SELL_PNL / total_buy_spend) * 100
                                    TAKE_PROFIT_SELL_PNL_PERCENTAGE = str((round(take_profit_sell_per, 2))) + "%"
                                if req_multi_tp == "Yes":
                                    buy_spend_per = float(total_buy_spend) * float(req_qty_size)
                                    TAKE_PROFIT_SELL_PNL = round((TOTAL_SELL_SPEND - buy_spend_per), 2)
                                    take_profit_sell_per = (TAKE_PROFIT_SELL_PNL / buy_spend_per) * 100
                                    TAKE_PROFIT_SELL_PNL_PERCENTAGE = str((round(take_profit_sell_per, 2))) + "%"

                                cursor.execute(sql.SQL(
                                    "insert into bybit_trade_log(date_time, symbol, order_id, order_action, order_type, executed_price, executed_qty, execution,pnl, percentage) values (%s, %s, %s, %s, %s, %s, %s, %s, %s,%s)"),
                                    [sell_order_executed_time, TAKE_PROFIT_SELL_ORDER_SYMBOL, TAKE_PROFIT_SELL_ORDER_ID,
                                     TAKE_PROFIT_SELL_ORDER_ACTION, TAKE_PROFIT_SELL_ORDER_TYPE,
                                     TAKE_PROFIT_SELL_ORDER_PRICE,
                                     TAKE_PROFIT_SELL_ORDER_QTY, execution, TAKE_PROFIT_SELL_PNL,
                                     TAKE_PROFIT_SELL_PNL_PERCENTAGE])
                                conn.commit()

                            if req_position_type == "Exit_long":
                                cursor.execute("select qty from bybit_long_entry where symbol = %s", [SPOT_SYMBOL])
                                r_3 = cursor.fetchall()
                                price_results = r_3[0][0]
                                previous_long_entry_qty = float(price_results)
                                print(f"previous_long_entry_qty = {previous_long_entry_qty}")

                                cursor.execute("select total_spend from bybit_long_entry where symbol = %s",
                                               [SPOT_SYMBOL])
                                r_3 = cursor.fetchall()
                                price_results = r_3[0][0]
                                previous_long_entry_spend = float(price_results)
                                print(f"previous_long_entry_spend = {previous_long_entry_spend}")

                                proportional_buy_spend = (
                                                                 previous_long_entry_spend / previous_long_entry_qty) * TAKE_PROFIT_SELL_ORDER_QTY
                                TAKE_PROFIT_SELL_PNL = round((TOTAL_SELL_SPEND - proportional_buy_spend), 2)
                                tp_sell_per = (TAKE_PROFIT_SELL_PNL / proportional_buy_spend) * 100
                                TAKE_PROFIT_SELL_PNL_PERCENTAGE = str((round(tp_sell_per, 2))) + "%"

                                cursor.execute(sql.SQL(
                                    "insert into bybit_trade_log(date_time, symbol, order_id, order_action, order_type, executed_price, executed_qty, execution, pnl, percentage) values (%s, %s, %s, %s, %s, %s, %s, %s, %s,%s)"),
                                    [sell_order_executed_time, TAKE_PROFIT_SELL_ORDER_SYMBOL,
                                     TAKE_PROFIT_SELL_ORDER_ID, TAKE_PROFIT_SELL_ORDER_ACTION,
                                     TAKE_PROFIT_SELL_ORDER_TYPE, TAKE_PROFIT_SELL_ORDER_PRICE,
                                     TAKE_PROFIT_SELL_ORDER_QTY, execution, TAKE_PROFIT_SELL_PNL,
                                     TAKE_PROFIT_SELL_PNL_PERCENTAGE])
                                conn.commit()

                            if req_position_type == "Enter_short":

                                cursor.execute("select exists (select 1 from bybit_short_entry)")
                                r_1 = cursor.fetchall()
                                live_r = r_1[0][0]

                                if live_r == False:
                                    cursor.execute(sql.SQL(
                                        "insert into bybit_short_entry(order_id, entry_price, total_spend, symbol, qty) values (%s, %s, %s, %s, %s)"),
                                        [TAKE_PROFIT_SELL_ORDER_ID, TAKE_PROFIT_SELL_ORDER_PRICE, TOTAL_SELL_SPEND,
                                         TAKE_PROFIT_SELL_ORDER_SYMBOL, TAKE_PROFIT_SELL_ORDER_QTY])
                                    conn.commit()
                                if live_r == True:
                                    cursor.execute(
                                        "update bybit_short_entry set order_id = %s, entry_price = %s, total_spend = %s, symbol = %s, qty = %s",
                                        [TAKE_PROFIT_SELL_ORDER_ID, TAKE_PROFIT_SELL_ORDER_PRICE, TOTAL_SELL_SPEND,
                                         TAKE_PROFIT_SELL_ORDER_SYMBOL, TAKE_PROFIT_SELL_ORDER_QTY])
                                    conn.commit()
                                    print("Records inserted")

                                cursor.execute(sql.SQL(
                                    "insert into bybit_trade_log(date_time, symbol, order_id, order_action, order_type, executed_price, executed_qty,execution) values (%s, %s, %s, %s, %s, %s, %s,%s)"),
                                    [sell_order_executed_time, TAKE_PROFIT_SELL_ORDER_SYMBOL, TAKE_PROFIT_SELL_ORDER_ID,
                                     TAKE_PROFIT_SELL_ORDER_ACTION, TAKE_PROFIT_SELL_ORDER_TYPE,
                                     TAKE_PROFIT_SELL_ORDER_PRICE,
                                     TAKE_PROFIT_SELL_ORDER_QTY, execution])
                                conn.commit()

                            if req_position_type == "Exit_short":
                                cursor.execute("select total_spend from bybit_short_entry where symbol = %s",
                                               [SPOT_SYMBOL])
                                r_3 = cursor.fetchall()
                                price_results = r_3[0][0]
                                previous_short_entry_income = float(price_results)
                                print(f"previous_short_entry_price = {previous_short_entry_income}")

                                cursor.execute("select qty from bybit_short_entry where symbol = %s", [SPOT_SYMBOL])
                                r_3 = cursor.fetchall()
                                price_results = r_3[0][0]
                                previous_short_entry_qty = float(price_results)
                                print(f"previous_short_entry_price = {previous_short_entry_qty}")

                                actual_sell_income = (previous_short_entry_income / 100) * 99.9
                                proportional_sell_income = (
                                                                   actual_sell_income / previous_short_entry_qty) * TAKE_PROFIT_SELL_ORDER_QTY
                                TAKE_PROFIT_SELL_PNL = round((proportional_sell_income - TOTAL_BUY_SPEND), 2)
                                tp_sell_per = (TAKE_PROFIT_SELL_PNL / proportional_sell_income) * 100
                                TAKE_PROFIT_SELL_PNL_PERCENTAGE = str((round(tp_sell_per, 2))) + "%"

                                cursor.execute(sql.SQL(
                                    "insert into bybit_trade_log(date_time, symbol, order_id, order_action, order_type, executed_price, executed_qty,execution,  pnl, percentage) values (%s, %s, %s, %s, %s, %s, %s, %s, %s,%s)"),
                                    [sell_order_executed_time, TAKE_PROFIT_SELL_ORDER_SYMBOL, TAKE_PROFIT_SELL_ORDER_ID,
                                     TAKE_PROFIT_SELL_ORDER_ACTION, TAKE_PROFIT_SELL_ORDER_TYPE,
                                     TAKE_PROFIT_SELL_ORDER_PRICE,
                                     TAKE_PROFIT_SELL_ORDER_QTY, execution, TAKE_PROFIT_SELL_PNL,
                                     TAKE_PROFIT_SELL_PNL_PERCENTAGE])
                                conn.commit()

                        except Exception as e:
                            print(e)

                    t21 = threading.Thread(target=add_to_trade_tp)
                    t21.start()

                def proceed_enter_long(SPOT_BUY_QUANTITY, SPOT_SYMBOL, SPOT_ENTRY, req_long_stop_loss_percent,
                                       req_long_take_profit_percent, req_multi_tp, req_tp1_percent, req_tp2_percent,
                                       req_tp3_percent, req_tp1_qty_size, req_tp2_qty_size, req_tp3_qty_size,
                                       req_order_time_out):
                    SPOT_EXIT = "NA"
                    if SPOT_ENTRY == "Market":
                        try:
                            enter_long_buy_order = session.place_active_order(symbol=SPOT_SYMBOL, side="Buy",
                                                                              orderType=SPOT_ENTRY,
                                                                              orderQty=SPOT_BUY_QUANTITY)
                            time.sleep(5)
                            print(f"enter_long_buy_order = {enter_long_buy_order}")
                            enter_long_buy_order_id = enter_long_buy_order["result"]["orderId"]
                        except Exception as e:
                            error_occured = f"{e}"
                            print(error_occured)
                            error_occured_time = datetime.now(IST)

                            cursor.execute(
                                "insert into bybit_error_log(symbol, order_action, entry_order_type, exit_order_type, quantity, occured_time, error_description) values (%s, %s, %s, %s, %s, %s, %s)",
                                [SPOT_SYMBOL, "Buy", SPOT_ENTRY, SPOT_EXIT, SPOT_BUY_QUANTITY, error_occured_time,
                                 error_occured])
                            conn.commit()

                    elif SPOT_ENTRY == "Limit":
                        prices = session.last_traded_price(symbol=SPOT_SYMBOL)
                        last_price = float(prices["result"]["price"])

                        try:
                            limit_buy_order = session.place_active_order(symbol=SPOT_SYMBOL, side="Buy",
                                                                         orderType=SPOT_ENTRY,
                                                                         orderQty=SPOT_BUY_QUANTITY,
                                                                         orderPrice=last_price)
                            print(f"limit_buy_order = {limit_buy_order}")
                            enter_long_buy_order_id = limit_buy_order["result"]["orderId"]
                        except Exception as e:
                            error_occured = f"{e}"
                            print(error_occured)
                            error_occured_time = datetime.now(IST)

                            cursor.execute(
                                "insert into bybit_error_log(symbol, order_action, entry_order_type, exit_order_type, quantity, occured_time, error_description) values (%s, %s, %s, %s, %s, %s, %s)",
                                [SPOT_SYMBOL, "Buy", SPOT_ENTRY, SPOT_EXIT, SPOT_BUY_QUANTITY, error_occured_time,
                                 error_occured])
                            conn.commit()

                        # Loop and check if entry order is filled
                        entry_order_timeout_start = time.time()

                        while time.time() < (entry_order_timeout_start + req_order_time_out):
                            try:
                                active_order = session.get_active_order(orderCategory=1)
                                for act_or in active_order["result"]:
                                    if act_or["orderId"] == enter_long_buy_order_id:
                                        active_order_status = act_or["status"]
                                        if active_order_status == "FILLED":
                                            enter_long_buy_order = act_or
                                            filled_order_id = enter_long_buy_order_id
                                            print("Filled")
                                            break
                                if active_order_status == "FILLED":
                                    break

                            except Exception as e:
                                print(e)
                                pass

                    if active_order_status == "FILLED":

                        trades = session.user_trade_records(symbol=SPOT_SYMBOL, orderId=filled_order_id)
                        filled_trade = trades["result"]

                        try:

                            BUY_ORDER_ID = enter_long_buy_order["orderId"]
                            BUY_ORDER_SYMBOL = enter_long_buy_order["symbol"]
                            ask_qty = float(enter_long_buy_order["executedQty"])
                            commision_in_coin = 0
                            try:
                                for fill in filled_trade["fee"]:
                                    comm = float(fill["fee"])
                                    commision_in_coin += comm
                            except:
                                commision_in_coin = ask_qty * 0.001
                            BUY_ORDER_QTY = ask_qty - commision_in_coin
                            TOTAL_BUY_SPEND = float(enter_long_buy_order["cummulativeQuoteQty"])
                            print(f"Total buy spend = {TOTAL_BUY_SPEND}")
                            BUY_ORDER_PRICE = round((float(enter_long_buy_order["cummulativeQuoteQty"]) / float(
                                enter_long_buy_order["executedQty"])), 3)
                            BUY_ORDER_ACTION = enter_long_buy_order["side"]
                            BUY_ORDER_TYPE = (enter_long_buy_order["type"]).title()
                            buy_order_executed_time = datetime.now(IST)

                            if BUY_ORDER_TYPE == "Market":
                                execution = "Entry as Market"
                            if BUY_ORDER_TYPE == "Limit":
                                execution = "Entry as Limit"

                            cursor.execute(
                                f"""INSERT INTO bybit_id_list (order_id, entry_price, total_spend) VALUES ({BUY_ORDER_ID},{BUY_ORDER_PRICE},{TOTAL_BUY_SPEND})""")
                            conn.commit()
                            print("Records inserted")

                            cursor.execute("select exists (select 1 from bybit_long_entry)")
                            r_1 = cursor.fetchall()
                            live_r = r_1[0][0]

                            if live_r == False:
                                cursor.execute(sql.SQL(
                                    "insert into bybit_long_entry(order_id, entry_price, total_spend, symbol, qty) values (%s, %s, %s, %s, %s)"),
                                    [BUY_ORDER_ID, BUY_ORDER_PRICE, TOTAL_BUY_SPEND, BUY_ORDER_SYMBOL, BUY_ORDER_QTY])
                                conn.commit()
                            if live_r == True:
                                cursor.execute(
                                    "update bybit_long_entry set order_id = %s, entry_price = %s, total_spend = %s, symbol = %s, qty = %s",
                                    [BUY_ORDER_ID, BUY_ORDER_PRICE, TOTAL_BUY_SPEND, BUY_ORDER_SYMBOL, BUY_ORDER_QTY])
                                conn.commit()
                                print("Records inserted")

                            cursor.execute(sql.SQL(
                                "insert into bybit_trade_log(date_time, symbol, order_id, order_action, order_type, executed_price, executed_qty,execution) values (%s, %s, %s, %s, %s, %s, %s,%s)"),
                                [buy_order_executed_time, BUY_ORDER_SYMBOL, BUY_ORDER_ID, BUY_ORDER_ACTION,
                                 BUY_ORDER_TYPE, BUY_ORDER_PRICE, BUY_ORDER_QTY, execution])
                            conn.commit()

                            entry_price = BUY_ORDER_PRICE
                            print(f"entry price = {entry_price}")

                            if req_long_stop_loss_percent > 0 or req_long_take_profit_percent > 0 or req_multi_tp == "Yes":
                                SPOT_SIDE = "Sell"

                                long_stop_loss_bp = entry_price - (entry_price * req_long_stop_loss_percent)

                                long_take_profit_bp = entry_price + (entry_price * req_long_take_profit_percent)

                                STOP_LOSS_PRICE_FINAL = cal_price_with_precision(SPOT_SYMBOL=SPOT_SYMBOL,
                                                                                 input_price=long_stop_loss_bp)
                                print(f"Stop loss price final = {STOP_LOSS_PRICE_FINAL}")

                                TAKE_PROFIT_PRICE_FINAL = cal_price_with_precision(SPOT_SYMBOL=SPOT_SYMBOL,
                                                                                   input_price=long_take_profit_bp)
                                print(f"Take profit price final = {TAKE_PROFIT_PRICE_FINAL}")

                                SPOT_SELL_QUANTITY = calculate_sell_qty_with_precision(SPOT_SYMBOL=SPOT_SYMBOL,
                                                                                       buy_qty=BUY_ORDER_QTY)
                                print(SPOT_SELL_QUANTITY)

                                if req_multi_tp == "No":
                                    if req_long_stop_loss_percent > 0 and req_long_take_profit_percent > 0:
                                        execute_limit_oco_order(SPOT_SIDE=SPOT_SIDE, req_position_type="Enter_long",
                                                                BUY_ORDER_ID=BUY_ORDER_ID, SPOT_SYMBOL=SPOT_SYMBOL,
                                                                SPOT_SELL_QUANTITY=SPOT_SELL_QUANTITY,
                                                                TAKE_PROFIT_PRICE_FINAL=TAKE_PROFIT_PRICE_FINAL,
                                                                STOP_LOSS_PRICE_FINAL=STOP_LOSS_PRICE_FINAL,
                                                                SPOT_ENTRY=SPOT_ENTRY, req_multi_tp=req_multi_tp,
                                                                req_qty_size=0, req_order_time_out=req_order_time_out,tp_type="None")
                                    elif req_long_stop_loss_percent > 0 and (
                                            req_long_take_profit_percent == "" or req_long_take_profit_percent == 0):
                                        execute_limit_stop_loss_order(SPOT_SIDE=SPOT_SIDE,
                                                                      req_position_type="Enter_long",
                                                                      BUY_ORDER_ID=BUY_ORDER_ID,
                                                                      SPOT_SYMBOL=SPOT_SYMBOL,
                                                                      SPOT_SELL_QUANTITY=SPOT_SELL_QUANTITY,
                                                                      STOP_LOSS_PRICE_FINAL=STOP_LOSS_PRICE_FINAL,
                                                                      SPOT_ENTRY=SPOT_ENTRY,
                                                                      req_order_time_out=req_order_time_out)
                                    elif req_long_take_profit_percent > 0 and (
                                            req_long_stop_loss_percent == "" or req_long_stop_loss_percent == 0):
                                        execute_limit_take_profit_order(SPOT_SIDE=SPOT_SIDE,
                                                                        req_position_type="Enter_long",
                                                                        BUY_ORDER_ID=BUY_ORDER_ID,
                                                                        SPOT_SYMBOL=SPOT_SYMBOL,
                                                                        SPOT_SELL_QUANTITY=SPOT_SELL_QUANTITY,
                                                                        TAKE_PROFIT_PRICE_FINAL=TAKE_PROFIT_PRICE_FINAL,
                                                                        SPOT_ENTRY=SPOT_ENTRY,
                                                                        req_multi_tp=req_multi_tp,
                                                                        req_qty_size=0,
                                                                        req_order_time_out=req_order_time_out,tp_type="None")

                                print(f"BUY ORDER QTY = {BUY_ORDER_QTY}")
                                print(f"SIZE={req_tp1_qty_size}")
                                if req_multi_tp == "Yes":
                                    SELLABLE_1 = calculate_sell_qty_with_precision(SPOT_SYMBOL,
                                                                                   (BUY_ORDER_QTY * req_tp1_qty_size))
                                    print(f"Sellable qty_1 = {SELLABLE_1}")
                                    SELLABLE_2 = calculate_sell_qty_with_precision(SPOT_SYMBOL,
                                                                                   (BUY_ORDER_QTY * req_tp2_qty_size))
                                    print(f"Sellable qty_2 = {SELLABLE_2}")
                                    SELLABLE_3 = calculate_sell_qty_with_precision(SPOT_SYMBOL,
                                                                                   (BUY_ORDER_QTY * req_tp3_qty_size))
                                    print(f"Sellable qty_3 = {SELLABLE_3}")

                                    long_take_profit_bp_1 = entry_price + (entry_price * req_tp1_percent)
                                    long_take_profit_bp_2 = entry_price + (entry_price * req_tp2_percent)
                                    long_take_profit_bp_3 = entry_price + (entry_price * req_tp3_percent)
                                    TAKE_PROFIT_PRICE_FINAL_1 = cal_price_with_precision(SPOT_SYMBOL=SPOT_SYMBOL,
                                                                                         input_price=long_take_profit_bp_1)
                                    TAKE_PROFIT_PRICE_FINAL_2 = cal_price_with_precision(SPOT_SYMBOL=SPOT_SYMBOL,
                                                                                         input_price=long_take_profit_bp_2)
                                    TAKE_PROFIT_PRICE_FINAL_3 = cal_price_with_precision(SPOT_SYMBOL=SPOT_SYMBOL,
                                                                                         input_price=long_take_profit_bp_3)
                                    print(f"Take profit price final_1 = {TAKE_PROFIT_PRICE_FINAL_1}")
                                    print(f"Take profit price final_2 = {TAKE_PROFIT_PRICE_FINAL_2}")
                                    print(f"Take profit price final_3 = {TAKE_PROFIT_PRICE_FINAL_3}")

                                    if req_long_stop_loss_percent > 0 and (
                                            req_tp1_percent > 0 or req_tp2_percent > 0 or req_tp3_percent > 0):
                                        if req_tp1_percent > 0:
                                            t1 = threading.Thread(
                                                target=lambda: execute_limit_oco_order(SPOT_SIDE=SPOT_SIDE,
                                                                                       req_position_type="Enter_long",
                                                                                       BUY_ORDER_ID=BUY_ORDER_ID,
                                                                                       SPOT_SYMBOL=SPOT_SYMBOL,
                                                                                       SPOT_SELL_QUANTITY=SELLABLE_1,
                                                                                       TAKE_PROFIT_PRICE_FINAL=TAKE_PROFIT_PRICE_FINAL_1,
                                                                                       STOP_LOSS_PRICE_FINAL=STOP_LOSS_PRICE_FINAL,
                                                                                       SPOT_ENTRY=SPOT_ENTRY,
                                                                                       req_multi_tp=req_multi_tp,
                                                                                       req_qty_size=req_tp1_qty_size,
                                                                                       req_order_time_out=req_order_time_out,tp_type="One"))
                                            t1.start()
                                        if req_tp2_percent > 0:
                                            t2 = threading.Thread(
                                                target=lambda: execute_limit_oco_order(SPOT_SIDE=SPOT_SIDE,
                                                                                       req_position_type="Enter_long",
                                                                                       BUY_ORDER_ID=BUY_ORDER_ID,
                                                                                       SPOT_SYMBOL=SPOT_SYMBOL,
                                                                                       SPOT_SELL_QUANTITY=SELLABLE_2,
                                                                                       TAKE_PROFIT_PRICE_FINAL=TAKE_PROFIT_PRICE_FINAL_2,
                                                                                       STOP_LOSS_PRICE_FINAL=STOP_LOSS_PRICE_FINAL,
                                                                                       SPOT_ENTRY=SPOT_ENTRY,
                                                                                       req_multi_tp=req_multi_tp,
                                                                                       req_qty_size=req_tp2_qty_size,
                                                                                       req_order_time_out=req_order_time_out,tp_type="Two"))
                                            t2.start()
                                        if req_tp3_percent > 0:
                                            t2 = threading.Thread(
                                                target=lambda: execute_limit_oco_order(SPOT_SIDE=SPOT_SIDE,
                                                                                       req_position_type="Enter_long",
                                                                                       BUY_ORDER_ID=BUY_ORDER_ID,
                                                                                       SPOT_SYMBOL=SPOT_SYMBOL,
                                                                                       SPOT_SELL_QUANTITY=SELLABLE_3,
                                                                                       TAKE_PROFIT_PRICE_FINAL=TAKE_PROFIT_PRICE_FINAL_3,
                                                                                       STOP_LOSS_PRICE_FINAL=STOP_LOSS_PRICE_FINAL,
                                                                                       SPOT_ENTRY=SPOT_ENTRY,
                                                                                       req_multi_tp=req_multi_tp,
                                                                                       req_qty_size=req_tp3_qty_size,
                                                                                       req_order_time_out=req_order_time_out,tp_type="Three"))
                                            t2.start()

                                    elif req_long_stop_loss_percent > 0 and (
                                            req_tp1_percent == 0 and req_tp2_percent == 0 and req_tp3_percent == 0):
                                        execute_limit_stop_loss_order(SPOT_SIDE=SPOT_SIDE,
                                                                      req_position_type="Enter_long",
                                                                      BUY_ORDER_ID=BUY_ORDER_ID,
                                                                      SPOT_SYMBOL=SPOT_SYMBOL,
                                                                      SPOT_SELL_QUANTITY=SPOT_SELL_QUANTITY,
                                                                      STOP_LOSS_PRICE_FINAL=STOP_LOSS_PRICE_FINAL,
                                                                      SPOT_ENTRY=SPOT_ENTRY,
                                                                      req_order_time_out=req_order_time_out)

                                    elif (req_tp1_percent > 0 or req_tp2_percent > 0 or req_tp3_percent > 0) and (
                                            req_long_stop_loss_percent == "" or req_long_stop_loss_percent == 0):
                                        if req_tp1_percent > 0:
                                            t1 = threading.Thread(
                                                target=lambda: execute_limit_take_profit_order(SPOT_SIDE=SPOT_SIDE,
                                                                                               req_position_type="Enter_long",
                                                                                               BUY_ORDER_ID=BUY_ORDER_ID,
                                                                                               SPOT_SYMBOL=SPOT_SYMBOL,
                                                                                               SPOT_SELL_QUANTITY=SELLABLE_1,
                                                                                               TAKE_PROFIT_PRICE_FINAL=TAKE_PROFIT_PRICE_FINAL_1,
                                                                                               SPOT_ENTRY=SPOT_ENTRY,
                                                                                               req_multi_tp=req_multi_tp,
                                                                                               req_qty_size=req_tp1_qty_size,
                                                                                               req_order_time_out=req_order_time_out,tp_type="One"))
                                            t1.start()
                                        if req_tp2_percent > 0:
                                            t2 = threading.Thread(
                                                target=lambda: execute_limit_take_profit_order(SPOT_SIDE=SPOT_SIDE,
                                                                                               req_position_type="Enter_long",
                                                                                               BUY_ORDER_ID=BUY_ORDER_ID,
                                                                                               SPOT_SYMBOL=SPOT_SYMBOL,
                                                                                               SPOT_SELL_QUANTITY=SELLABLE_2,
                                                                                               TAKE_PROFIT_PRICE_FINAL=TAKE_PROFIT_PRICE_FINAL_2,
                                                                                               SPOT_ENTRY=SPOT_ENTRY,
                                                                                               req_multi_tp=req_multi_tp,
                                                                                               req_qty_size=req_tp2_qty_size,
                                                                                               req_order_time_out=req_order_time_out,tp_type="Two"))
                                            t2.start()
                                        if req_tp3_percent > 0:
                                            t3 = threading.Thread(
                                                target=lambda: execute_limit_take_profit_order(SPOT_SIDE=SPOT_SIDE,
                                                                                               req_position_type="Enter_long",
                                                                                               BUY_ORDER_ID=BUY_ORDER_ID,
                                                                                               SPOT_SYMBOL=SPOT_SYMBOL,
                                                                                               SPOT_SELL_QUANTITY=SELLABLE_3,
                                                                                               TAKE_PROFIT_PRICE_FINAL=TAKE_PROFIT_PRICE_FINAL_3,
                                                                                               SPOT_ENTRY=SPOT_ENTRY,
                                                                                               req_multi_tp=req_multi_tp,
                                                                                               req_qty_size=req_tp2_qty_size,
                                                                                               req_order_time_out=req_order_time_out,tp_type="Three"))
                                            t3.start()


                        except Exception as e:
                            error_occured = f"{e}"
                            print(error_occured)

                def proceed_exit_long(req_position_type, SPOT_SELL_QUANTITY_EL, SPOT_SYMBOL, req_long_stop_loss_percent,
                                      req_long_take_profit_percent, req_multi_tp, req_tp1_percent, req_tp2_percent,
                                      req_tp3_percent, req_tp1_qty_size, req_tp2_qty_size, req_tp3_qty_size,
                                      req_order_time_out):
                    SPOT_ENTRY = "NA"
                    SPOT_SIDE = "Sell"

                    cursor.execute("select entry_price from bybit_long_entry where symbol = %s", [SPOT_SYMBOL])
                    r_3 = cursor.fetchall()
                    price_results = r_3[0][0]
                    previous_long_entry_price = float(price_results)
                    print(f"previous_long_entry_price= {previous_long_entry_price}")

                    if req_long_stop_loss_percent > 0 or req_long_take_profit_percent > 0 or req_multi_tp == "Yes":
                        SPOT_EXIT = "Limit"

                        long_stop_loss_bp = previous_long_entry_price - (
                                previous_long_entry_price * req_long_stop_loss_percent)

                        long_take_profit_bp = previous_long_entry_price + (
                                previous_long_entry_price * req_long_take_profit_percent)

                        STOP_LOSS_PRICE_FINAL = cal_price_with_precision(SPOT_SYMBOL=SPOT_SYMBOL,
                                                                         input_price=long_stop_loss_bp)
                        print(f"Stop loss price final = {STOP_LOSS_PRICE_FINAL}")

                        TAKE_PROFIT_PRICE_FINAL = cal_price_with_precision(SPOT_SYMBOL=SPOT_SYMBOL,
                                                                           input_price=long_take_profit_bp)
                        print(f"Take profit price final = {TAKE_PROFIT_PRICE_FINAL}")

                        BUY_ORDER_ID = 0

                        if req_multi_tp == "No":
                            if req_long_stop_loss_percent > 0 and req_long_take_profit_percent > 0:
                                execute_limit_oco_order(SPOT_SIDE=SPOT_SIDE, req_position_type=req_position_type,
                                                        BUY_ORDER_ID=BUY_ORDER_ID, SPOT_SYMBOL=SPOT_SYMBOL,
                                                        SPOT_SELL_QUANTITY=SPOT_SELL_QUANTITY_EL,
                                                        TAKE_PROFIT_PRICE_FINAL=TAKE_PROFIT_PRICE_FINAL,
                                                        STOP_LOSS_PRICE_FINAL=STOP_LOSS_PRICE_FINAL,
                                                        SPOT_ENTRY=SPOT_ENTRY,
                                                        req_multi_tp=req_multi_tp, req_qty_size=0,
                                                        req_order_time_out=req_order_time_out,tp_type="None")
                            elif req_long_stop_loss_percent > 0 and (
                                    req_long_take_profit_percent == "" or req_long_take_profit_percent == 0):
                                execute_limit_stop_loss_order(SPOT_SIDE, req_position_type, BUY_ORDER_ID, SPOT_SYMBOL,
                                                              SPOT_SELL_QUANTITY_EL, STOP_LOSS_PRICE_FINAL, SPOT_ENTRY,
                                                              req_order_time_out)
                            elif req_long_take_profit_percent > 0 and (
                                    req_long_stop_loss_percent == "" or req_long_stop_loss_percent == 0):
                                execute_limit_take_profit_order(SPOT_SIDE=SPOT_SIDE,
                                                                req_position_type=req_position_type,
                                                                BUY_ORDER_ID=BUY_ORDER_ID, SPOT_SYMBOL=SPOT_SYMBOL,
                                                                SPOT_SELL_QUANTITY=SPOT_SELL_QUANTITY_EL,
                                                                TAKE_PROFIT_PRICE_FINAL=TAKE_PROFIT_PRICE_FINAL,
                                                                SPOT_ENTRY=SPOT_ENTRY, req_multi_tp=req_multi_tp,
                                                                req_qty_size=0, req_order_time_out=req_order_time_out,tp_type="None")

                        if req_multi_tp == "Yes":
                            SELLABLE_1 = trunc_calculate_sell_qty_with_precision(SPOT_SYMBOL,
                                                                                 (
                                                                                             SPOT_SELL_QUANTITY_EL * req_tp1_qty_size))
                            print(f"Sellable qty_1 = {SELLABLE_1}")
                            SELLABLE_2 = trunc_calculate_sell_qty_with_precision(SPOT_SYMBOL,
                                                                                 (
                                                                                             SPOT_SELL_QUANTITY_EL * req_tp2_qty_size))
                            print(f"Sellable qty_2 = {SELLABLE_2}")
                            SELLABLE_3 = trunc_calculate_sell_qty_with_precision(SPOT_SYMBOL,
                                                                                 (
                                                                                             SPOT_SELL_QUANTITY_EL * req_tp3_qty_size))
                            print(f"Sellable qty_3 = {SELLABLE_3}")

                            long_take_profit_bp_1 = previous_long_entry_price + (
                                    previous_long_entry_price * req_tp1_percent)
                            long_take_profit_bp_2 = previous_long_entry_price + (
                                    previous_long_entry_price * req_tp2_percent)
                            long_take_profit_bp_3 = previous_long_entry_price + (
                                    previous_long_entry_price * req_tp3_percent)
                            TAKE_PROFIT_PRICE_FINAL_1 = cal_price_with_precision(SPOT_SYMBOL=SPOT_SYMBOL,
                                                                                 input_price=long_take_profit_bp_1)
                            TAKE_PROFIT_PRICE_FINAL_2 = cal_price_with_precision(SPOT_SYMBOL=SPOT_SYMBOL,
                                                                                 input_price=long_take_profit_bp_2)
                            TAKE_PROFIT_PRICE_FINAL_3 = cal_price_with_precision(SPOT_SYMBOL=SPOT_SYMBOL,
                                                                                 input_price=long_take_profit_bp_3)
                            print(f"Take profit price final_1 = {TAKE_PROFIT_PRICE_FINAL_1}")
                            print(f"Take profit price final_2 = {TAKE_PROFIT_PRICE_FINAL_2}")
                            print(f"Take profit price final_3 = {TAKE_PROFIT_PRICE_FINAL_3}")

                            if req_long_stop_loss_percent > 0 and (
                                    req_tp1_percent > 0 or req_tp2_percent > 0 or req_tp3_percent > 0):
                                if req_tp1_percent > 0:
                                    t1 = threading.Thread(target=lambda: execute_limit_oco_order(SPOT_SIDE=SPOT_SIDE,
                                                                                                 req_position_type=req_position_type,
                                                                                                 BUY_ORDER_ID=BUY_ORDER_ID,
                                                                                                 SPOT_SYMBOL=SPOT_SYMBOL,
                                                                                                 SPOT_SELL_QUANTITY=SELLABLE_1,
                                                                                                 TAKE_PROFIT_PRICE_FINAL=TAKE_PROFIT_PRICE_FINAL_1,
                                                                                                 STOP_LOSS_PRICE_FINAL=STOP_LOSS_PRICE_FINAL,
                                                                                                 SPOT_ENTRY=SPOT_ENTRY,
                                                                                                 req_multi_tp=req_multi_tp,
                                                                                                 req_qty_size=req_tp1_qty_size,
                                                                                                 req_order_time_out=req_order_time_out,tp_type="One"))
                                    t1.start()
                                if req_tp2_percent > 0:
                                    t2 = threading.Thread(target=lambda: execute_limit_oco_order(SPOT_SIDE=SPOT_SIDE,
                                                                                                 req_position_type=req_position_type,
                                                                                                 BUY_ORDER_ID=BUY_ORDER_ID,
                                                                                                 SPOT_SYMBOL=SPOT_SYMBOL,
                                                                                                 SPOT_SELL_QUANTITY=SELLABLE_2,
                                                                                                 TAKE_PROFIT_PRICE_FINAL=TAKE_PROFIT_PRICE_FINAL_2,
                                                                                                 STOP_LOSS_PRICE_FINAL=STOP_LOSS_PRICE_FINAL,
                                                                                                 SPOT_ENTRY=SPOT_ENTRY,
                                                                                                 req_multi_tp=req_multi_tp,
                                                                                                 req_qty_size=req_tp2_qty_size,
                                                                                                 req_order_time_out=req_order_time_out,tp_type="Two"))
                                    t2.start()
                                if req_tp3_percent > 0:
                                    t3 = threading.Thread(target=lambda: execute_limit_oco_order(SPOT_SIDE=SPOT_SIDE,
                                                                                                 req_position_type=req_position_type,
                                                                                                 BUY_ORDER_ID=BUY_ORDER_ID,
                                                                                                 SPOT_SYMBOL=SPOT_SYMBOL,
                                                                                                 SPOT_SELL_QUANTITY=SELLABLE_3,
                                                                                                 TAKE_PROFIT_PRICE_FINAL=TAKE_PROFIT_PRICE_FINAL_3,
                                                                                                 STOP_LOSS_PRICE_FINAL=STOP_LOSS_PRICE_FINAL,
                                                                                                 SPOT_ENTRY=SPOT_ENTRY,
                                                                                                 req_multi_tp=req_multi_tp,
                                                                                                 req_qty_size=req_tp3_qty_size,
                                                                                                 req_order_time_out=req_order_time_out,tp_type="Three"))
                                    t3.start()

                            elif req_long_stop_loss_percent > 0 and (
                                    req_tp1_percent == 0 and req_tp2_percent == 0 and req_tp3_percent == 0):
                                execute_limit_stop_loss_order(SPOT_SIDE, req_position_type, BUY_ORDER_ID, SPOT_SYMBOL,
                                                              SPOT_SELL_QUANTITY_EL, STOP_LOSS_PRICE_FINAL, SPOT_ENTRY,
                                                              req_order_time_out)

                            elif (req_tp1_percent > 0 or req_tp2_percent > 0 or req_tp3_percent > 0) and (
                                    req_long_stop_loss_percent == "" or req_long_stop_loss_percent == 0):
                                if req_tp1_percent > 0:
                                    t1 = threading.Thread(
                                        target=lambda: execute_limit_take_profit_order(SPOT_SIDE=SPOT_SIDE,
                                                                                       req_position_type=req_position_type,
                                                                                       BUY_ORDER_ID=BUY_ORDER_ID,
                                                                                       SPOT_SYMBOL=SPOT_SYMBOL,
                                                                                       SPOT_SELL_QUANTITY=SELLABLE_1,
                                                                                       TAKE_PROFIT_PRICE_FINAL=TAKE_PROFIT_PRICE_FINAL_1,
                                                                                       SPOT_ENTRY=SPOT_ENTRY,
                                                                                       req_multi_tp=req_multi_tp,
                                                                                       req_qty_size=req_tp1_qty_size,
                                                                                       req_order_time_out=req_order_time_out,tp_type="One"))
                                    t1.start()
                                if req_tp2_percent > 0:
                                    t2 = threading.Thread(
                                        target=lambda: execute_limit_take_profit_order(SPOT_SIDE=SPOT_SIDE,
                                                                                       req_position_type=req_position_type,
                                                                                       BUY_ORDER_ID=BUY_ORDER_ID,
                                                                                       SPOT_SYMBOL=SPOT_SYMBOL,
                                                                                       SPOT_SELL_QUANTITY=SELLABLE_2,
                                                                                       TAKE_PROFIT_PRICE_FINAL=TAKE_PROFIT_PRICE_FINAL_2,
                                                                                       SPOT_ENTRY=SPOT_ENTRY,
                                                                                       req_multi_tp=req_multi_tp,
                                                                                       req_qty_size=req_tp2_qty_size,
                                                                                       req_order_time_out=req_order_time_out,tp_type="Two"))
                                    t2.start()
                                if req_tp3_percent > 0:
                                    t3 = threading.Thread(
                                        target=lambda: execute_limit_take_profit_order(SPOT_SIDE=SPOT_SIDE,
                                                                                       req_position_type=req_position_type,
                                                                                       BUY_ORDER_ID=BUY_ORDER_ID,
                                                                                       SPOT_SYMBOL=SPOT_SYMBOL,
                                                                                       SPOT_SELL_QUANTITY=SELLABLE_3,
                                                                                       TAKE_PROFIT_PRICE_FINAL=TAKE_PROFIT_PRICE_FINAL_3,
                                                                                       SPOT_ENTRY=SPOT_ENTRY,
                                                                                       req_multi_tp=req_multi_tp,
                                                                                       req_qty_size=req_tp2_qty_size,
                                                                                       req_order_time_out=req_order_time_out,tp_type="Three"))
                                    t3.start()


                    elif req_long_stop_loss_percent == 0 and req_long_take_profit_percent == 0 and req_multi_tp == "No":
                        SPOT_EXIT = "Market"
                        try:
                            exit_long_sell_or = session.place_active_order(symbol=SPOT_SYMBOL, side=SPOT_SIDE,
                                                                           orderType=SPOT_EXIT,
                                                                           orderQty=SPOT_SELL_QUANTITY_EL)
                            exit_long_sell_order = exit_long_sell_or["result"]
                            time.sleep(10)
                            print(f"exit_long_sell_order = {exit_long_sell_order}")
                            exit_long_sell_order_id = exit_long_sell_order["orderId"]
                        except Exception as e:
                            error_occured = f"{e}"
                            print(error_occured)
                            error_occured_time = datetime.now(IST)

                            cursor.execute(
                                "insert into bybit_error_log(symbol, order_action, entry_order_type, exit_order_type, quantity, occured_time, error_description) values (%s, %s, %s, %s, %s, %s, %s)",
                                [SPOT_SYMBOL, SPOT_SIDE, SPOT_ENTRY, SPOT_EXIT, SPOT_SELL_QUANTITY_EL,
                                 error_occured_time,
                                 error_occured])
                            conn.commit()

                        try:

                            SELL_ORDER_ID = exit_long_sell_order["orderId"]
                            SELL_ORDER_SYMBOL = exit_long_sell_order["symbol"]
                            SELL_ORDER_QTY = float(exit_long_sell_order["executedQty"])
                            sell_cum_qty = float(exit_long_sell_order["cummulativeQuoteQty"])
                            TOTAL_SELL_SPEND = (sell_cum_qty / 100) * 99.9
                            print(f"Total buy spend = {TOTAL_SELL_SPEND}")
                            SELL_ORDER_PRICE = round((float(exit_long_sell_order["cummulativeQuoteQty"]) / float(
                                exit_long_sell_order["executedQty"])), 3)
                            SELL_ORDER_ACTION = exit_long_sell_order["side"]
                            SELL_ORDER_TYPE = (exit_long_sell_order["type"]).title()
                            sell_order_executed_time = datetime.now(IST)

                            execution = "Exit as Market"

                            cursor.execute("select qty from bybit_long_entry where symbol = %s", [SPOT_SYMBOL])
                            r_3 = cursor.fetchall()
                            price_results = r_3[0][0]
                            previous_long_entry_qty = float(price_results)
                            print(f"previous_long_entry_qty = {previous_long_entry_qty}")

                            cursor.execute("select total_spend from bybit_long_entry where symbol = %s", [SPOT_SYMBOL])
                            r_3 = cursor.fetchall()
                            price_results = r_3[0][0]
                            previous_long_entry_spend = float(price_results)
                            print(f"previous_long_entry_spend = {previous_long_entry_spend}")

                            proportional_buy_spend = (
                                                                 previous_long_entry_spend / previous_long_entry_qty) * SELL_ORDER_QTY
                            SELL_ORDER_SELL_PNL = round((TOTAL_SELL_SPEND - proportional_buy_spend), 2)
                            sell_order_pnl_per = (SELL_ORDER_SELL_PNL / proportional_buy_spend) * 100
                            SELL_ORDER_SELL_PNL_PERCENTAGE = str((round(sell_order_pnl_per, 2))) + "%"

                            cursor.execute(sql.SQL(
                                "insert into bybit_trade_log(date_time, symbol, order_id, order_action, order_type, executed_price, executed_qty, execution,pnl, percentage) values (%s, %s, %s, %s, %s, %s, %s, %s, %s,%s)"),
                                [sell_order_executed_time, SELL_ORDER_SYMBOL, SELL_ORDER_ID, SELL_ORDER_ACTION,
                                 SELL_ORDER_TYPE, SELL_ORDER_PRICE, SELL_ORDER_QTY, execution, SELL_ORDER_SELL_PNL,
                                 SELL_ORDER_SELL_PNL_PERCENTAGE])
                            conn.commit()

                        except Exception as e:
                            error_occured = f"{e}"
                            print(error_occured)

                def proceed_enter_short(req_position_type, SPOT_SELL_QUANTITY_EL, SPOT_SYMBOL,
                                        req_short_stop_loss_percent,
                                        req_short_take_profit_percent, req_multi_tp, req_tp1_percent, req_tp2_percent,
                                        req_tp3_percent, req_tp1_qty_size, req_tp2_qty_size, req_tp3_qty_size,
                                        req_order_time_out):

                    SPOT_ENTRY = "NA"
                    SPOT_SIDE = "Sell"

                    prices = session.last_traded_price(symbol=SPOT_SYMBOL)
                    last_price = float(prices["result"]["price"])

                    if req_short_stop_loss_percent > 0 or req_short_take_profit_percent > 0 or req_multi_tp == "Yes":
                        SPOT_EXIT = "Limit"

                        short_stop_loss_bp = last_price - (last_price * req_short_stop_loss_percent)

                        short_take_profit_bp = last_price + (last_price * req_short_take_profit_percent)

                        STOP_LOSS_PRICE_FINAL = cal_price_with_precision(SPOT_SYMBOL=SPOT_SYMBOL,
                                                                         input_price=short_stop_loss_bp)
                        print(f"Stop loss price final = {STOP_LOSS_PRICE_FINAL}")

                        TAKE_PROFIT_PRICE_FINAL = cal_price_with_precision(SPOT_SYMBOL=SPOT_SYMBOL,
                                                                           input_price=short_take_profit_bp)
                        print(f"Take profit price final = {TAKE_PROFIT_PRICE_FINAL}")

                        BUY_ORDER_ID = 0

                        if req_multi_tp == "No":
                            if req_short_stop_loss_percent > 0 and req_short_take_profit_percent > 0:
                                execute_limit_oco_order(SPOT_SIDE=SPOT_SIDE, req_position_type=req_position_type,
                                                        BUY_ORDER_ID=BUY_ORDER_ID, SPOT_SYMBOL=SPOT_SYMBOL,
                                                        SPOT_SELL_QUANTITY=SPOT_SELL_QUANTITY_EL,
                                                        TAKE_PROFIT_PRICE_FINAL=TAKE_PROFIT_PRICE_FINAL,
                                                        STOP_LOSS_PRICE_FINAL=STOP_LOSS_PRICE_FINAL,
                                                        SPOT_ENTRY=SPOT_ENTRY,
                                                        req_multi_tp=req_multi_tp, req_qty_size=0,
                                                        req_order_time_out=req_order_time_out,tp_type="None")
                            elif req_short_stop_loss_percent > 0 and (
                                    req_short_take_profit_percent == "" or req_short_take_profit_percent == 0):
                                execute_limit_stop_loss_order(SPOT_SIDE, req_position_type, BUY_ORDER_ID, SPOT_SYMBOL,
                                                              SPOT_SELL_QUANTITY_EL, STOP_LOSS_PRICE_FINAL, SPOT_ENTRY,
                                                              req_order_time_out)
                            elif req_short_take_profit_percent > 0 and (
                                    req_short_stop_loss_percent == "" or req_short_stop_loss_percent == 0):
                                execute_limit_take_profit_order(SPOT_SIDE=SPOT_SIDE,
                                                                req_position_type=req_position_type,
                                                                BUY_ORDER_ID=BUY_ORDER_ID, SPOT_SYMBOL=SPOT_SYMBOL,
                                                                SPOT_SELL_QUANTITY=SPOT_SELL_QUANTITY_EL,
                                                                TAKE_PROFIT_PRICE_FINAL=TAKE_PROFIT_PRICE_FINAL,
                                                                SPOT_ENTRY=SPOT_ENTRY, req_multi_tp=req_multi_tp,
                                                                req_qty_size=0, req_order_time_out=req_order_time_out,tp_type="None")

                        if req_multi_tp == "Yes":
                            SELLABLE_1 = calculate_sell_qty_with_precision(SPOT_SYMBOL,
                                                                           (SPOT_SELL_QUANTITY_EL * req_tp1_qty_size))
                            print(f"Sellable qty_1 = {SELLABLE_1}")
                            SELLABLE_2 = calculate_sell_qty_with_precision(SPOT_SYMBOL,
                                                                           (SPOT_SELL_QUANTITY_EL * req_tp2_qty_size))
                            print(f"Sellable qty_2 = {SELLABLE_2}")
                            SELLABLE_3 = calculate_sell_qty_with_precision(SPOT_SYMBOL,
                                                                           (SPOT_SELL_QUANTITY_EL * req_tp3_qty_size))
                            print(f"Sellable qty_3 = {SELLABLE_3}")

                            short_take_profit_bp_1 = last_price + (last_price * req_tp1_percent)
                            short_take_profit_bp_2 = last_price + (last_price * req_tp2_percent)
                            short_take_profit_bp_3 = last_price + (last_price * req_tp3_percent)
                            TAKE_PROFIT_PRICE_FINAL_1 = cal_price_with_precision(SPOT_SYMBOL=SPOT_SYMBOL,
                                                                                 input_price=short_take_profit_bp_1)
                            TAKE_PROFIT_PRICE_FINAL_2 = cal_price_with_precision(SPOT_SYMBOL=SPOT_SYMBOL,
                                                                                 input_price=short_take_profit_bp_2)
                            TAKE_PROFIT_PRICE_FINAL_3 = cal_price_with_precision(SPOT_SYMBOL=SPOT_SYMBOL,
                                                                                 input_price=short_take_profit_bp_3)
                            print(f"Take profit price final_1 = {TAKE_PROFIT_PRICE_FINAL_1}")
                            print(f"Take profit price final_2 = {TAKE_PROFIT_PRICE_FINAL_2}")
                            print(f"Take profit price final_3 = {TAKE_PROFIT_PRICE_FINAL_3}")

                            if req_short_stop_loss_percent > 0 and (
                                    req_tp1_percent > 0 or req_tp2_percent > 0 or req_tp3_percent > 0):
                                if req_tp1_percent > 0:
                                    t1 = threading.Thread(target=lambda: execute_limit_oco_order(SPOT_SIDE=SPOT_SIDE,
                                                                                                 req_position_type=req_position_type,
                                                                                                 BUY_ORDER_ID=BUY_ORDER_ID,
                                                                                                 SPOT_SYMBOL=SPOT_SYMBOL,
                                                                                                 SPOT_SELL_QUANTITY=SELLABLE_1,
                                                                                                 TAKE_PROFIT_PRICE_FINAL=TAKE_PROFIT_PRICE_FINAL_1,
                                                                                                 STOP_LOSS_PRICE_FINAL=STOP_LOSS_PRICE_FINAL,
                                                                                                 SPOT_ENTRY=SPOT_ENTRY,
                                                                                                 req_multi_tp=req_multi_tp,
                                                                                                 req_qty_size=req_tp1_qty_size,
                                                                                                 req_order_time_out=req_order_time_out,tp_type="One"))
                                    t1.start()
                                if req_tp2_percent > 0:
                                    t2 = threading.Thread(target=lambda: execute_limit_oco_order(SPOT_SIDE=SPOT_SIDE,
                                                                                                 req_position_type=req_position_type,
                                                                                                 BUY_ORDER_ID=BUY_ORDER_ID,
                                                                                                 SPOT_SYMBOL=SPOT_SYMBOL,
                                                                                                 SPOT_SELL_QUANTITY=SELLABLE_2,
                                                                                                 TAKE_PROFIT_PRICE_FINAL=TAKE_PROFIT_PRICE_FINAL_2,
                                                                                                 STOP_LOSS_PRICE_FINAL=STOP_LOSS_PRICE_FINAL,
                                                                                                 SPOT_ENTRY=SPOT_ENTRY,
                                                                                                 req_multi_tp=req_multi_tp,
                                                                                                 req_qty_size=req_tp2_qty_size,
                                                                                                 req_order_time_out=req_order_time_out,tp_type="Two"))
                                    t2.start()
                                if req_tp3_percent > 0:
                                    t3 = threading.Thread(target=lambda: execute_limit_oco_order(SPOT_SIDE=SPOT_SIDE,
                                                                                                 req_position_type=req_position_type,
                                                                                                 BUY_ORDER_ID=BUY_ORDER_ID,
                                                                                                 SPOT_SYMBOL=SPOT_SYMBOL,
                                                                                                 SPOT_SELL_QUANTITY=SELLABLE_3,
                                                                                                 TAKE_PROFIT_PRICE_FINAL=TAKE_PROFIT_PRICE_FINAL_3,
                                                                                                 STOP_LOSS_PRICE_FINAL=STOP_LOSS_PRICE_FINAL,
                                                                                                 SPOT_ENTRY=SPOT_ENTRY,
                                                                                                 req_multi_tp=req_multi_tp,
                                                                                                 req_qty_size=req_tp3_qty_size,
                                                                                                 req_order_time_out=req_order_time_out,tp_type="Three"))
                                    t3.start()

                            elif req_short_stop_loss_percent > 0 and (
                                    req_tp1_percent == 0 and req_tp2_percent == 0 and req_tp3_percent == 0):
                                execute_limit_stop_loss_order(SPOT_SIDE, req_position_type, BUY_ORDER_ID, SPOT_SYMBOL,
                                                              SPOT_SELL_QUANTITY_EL, STOP_LOSS_PRICE_FINAL, SPOT_ENTRY,
                                                              req_order_time_out)


                            elif (req_tp1_percent > 0 or req_tp2_percent > 0 or req_tp3_percent > 0) and (
                                    req_short_stop_loss_percent == "" or req_short_stop_loss_percent == 0):
                                if req_tp1_percent > 0:
                                    t1 = threading.Thread(
                                        target=lambda: execute_limit_take_profit_order(SPOT_SIDE=SPOT_SIDE,
                                                                                       req_position_type=req_position_type,
                                                                                       BUY_ORDER_ID=BUY_ORDER_ID,
                                                                                       SPOT_SYMBOL=SPOT_SYMBOL,
                                                                                       SPOT_SELL_QUANTITY=SELLABLE_1,
                                                                                       TAKE_PROFIT_PRICE_FINAL=TAKE_PROFIT_PRICE_FINAL_1,
                                                                                       SPOT_ENTRY=SPOT_ENTRY,
                                                                                       req_multi_tp=req_multi_tp,
                                                                                       req_qty_size=req_tp1_qty_size,
                                                                                       req_order_time_out=req_order_time_out,tp_type="One"))
                                    t1.start()
                                if req_tp2_percent > 0:
                                    t2 = threading.Thread(
                                        target=lambda: execute_limit_take_profit_order(SPOT_SIDE=SPOT_SIDE,
                                                                                       req_position_type=req_position_type,
                                                                                       BUY_ORDER_ID=BUY_ORDER_ID,
                                                                                       SPOT_SYMBOL=SPOT_SYMBOL,
                                                                                       SPOT_SELL_QUANTITY=SELLABLE_2,
                                                                                       TAKE_PROFIT_PRICE_FINAL=TAKE_PROFIT_PRICE_FINAL_2,
                                                                                       SPOT_ENTRY=SPOT_ENTRY,
                                                                                       req_multi_tp=req_multi_tp,
                                                                                       req_qty_size=req_tp2_qty_size,
                                                                                       req_order_time_out=req_order_time_out,tp_type="Two"))
                                    t2.start()
                                if req_tp3_percent > 0:
                                    t3 = threading.Thread(
                                        target=lambda: execute_limit_take_profit_order(SPOT_SIDE=SPOT_SIDE,
                                                                                       req_position_type=req_position_type,
                                                                                       BUY_ORDER_ID=BUY_ORDER_ID,
                                                                                       SPOT_SYMBOL=SPOT_SYMBOL,
                                                                                       SPOT_SELL_QUANTITY=SELLABLE_3,
                                                                                       TAKE_PROFIT_PRICE_FINAL=TAKE_PROFIT_PRICE_FINAL_3,
                                                                                       SPOT_ENTRY=SPOT_ENTRY,
                                                                                       req_multi_tp=req_multi_tp,
                                                                                       req_qty_size=req_tp2_qty_size,
                                                                                       req_order_time_out=req_order_time_out,tp_type="Three"))
                                    t3.start()



                    elif req_short_stop_loss_percent == 0 and req_short_take_profit_percent == 0 and req_multi_tp == "No":
                        SPOT_EXIT = "Market"
                        try:
                            enter_short_sell_or = session.place_active_order(symbol=SPOT_SYMBOL, side=SPOT_SIDE,
                                                                             orderType=SPOT_EXIT,
                                                                             orderQty=SPOT_SELL_QUANTITY_EL)
                            time.sleep(10)
                            enter_short_sell_order = enter_short_sell_or["result"]
                            print(f"enter_short_sell_order = {enter_short_sell_order}")
                            enter_short_sell_order_id = enter_short_sell_order["orderId"]

                        except Exception as e:
                            error_occured = f"{e}"
                            print(error_occured)
                            error_occured_time = datetime.now(IST)

                            cursor.execute(
                                "insert into bybit_error_log(symbol, order_action, entry_order_type, exit_order_type, quantity, occured_time, error_description) values (%s, %s, %s, %s, %s, %s, %s)",
                                [SPOT_SYMBOL, SPOT_SIDE, SPOT_ENTRY, SPOT_EXIT, SPOT_SELL_QUANTITY_EL,
                                 error_occured_time,
                                 error_occured])
                            conn.commit()

                        try:

                            SELL_ORDER_ID = enter_short_sell_order["orderId"]
                            SELL_ORDER_SYMBOL = enter_short_sell_order["symbol"]
                            SELL_ORDER_QTY = float(enter_short_sell_order["executedQty"])
                            TOTAL_SELL_SPEND = float(enter_short_sell_order["cummulativeQuoteQty"])
                            print(f"Total buy spend = {TOTAL_SELL_SPEND}")
                            SELL_ORDER_PRICE = round((float(enter_short_sell_order["cummulativeQuoteQty"]) / float(
                                enter_short_sell_order["executedQty"])), 3)
                            SELL_ORDER_ACTION = enter_short_sell_order["side"]
                            SELL_ORDER_TYPE = enter_short_sell_order["type"]
                            sell_order_executed_time = datetime.now(IST)

                            execution = "Enter as Market"

                            cursor.execute("select exists (select 1 from bybit_short_entry)")
                            r_1 = cursor.fetchall()
                            live_r = r_1[0][0]

                            if live_r == False:
                                cursor.execute(sql.SQL(
                                    "insert into bybit_short_entry(order_id, entry_price, total_spend, symbol, qty) values (%s, %s, %s, %s, %s)"),
                                    [SELL_ORDER_ID, SELL_ORDER_PRICE, TOTAL_SELL_SPEND, SELL_ORDER_SYMBOL,
                                     SELL_ORDER_QTY])
                                conn.commit()
                            if live_r == True:
                                cursor.execute(
                                    "update bybit_short_entry set order_id = %s, entry_price = %s, total_spend = %s, symbol = %s, qty = %s",
                                    [SELL_ORDER_ID, SELL_ORDER_PRICE, TOTAL_SELL_SPEND, SELL_ORDER_SYMBOL,
                                     SELL_ORDER_QTY])
                                conn.commit()
                                print("Records inserted")

                            cursor.execute(sql.SQL(
                                "insert into bybit_trade_log(date_time, symbol, order_id, order_action, order_type, executed_price, executed_qty,execution) values (%s, %s, %s, %s, %s, %s, %s,%s)"),
                                [sell_order_executed_time, SELL_ORDER_SYMBOL, SELL_ORDER_ID, SELL_ORDER_ACTION,
                                 SELL_ORDER_TYPE, SELL_ORDER_PRICE, SELL_ORDER_QTY, execution])
                            conn.commit()

                        except Exception as e:
                            error_occured = f"{e}"
                            print(error_occured)

                def proceed_exit_short(req_position_type, SPOT_BUY_QUANTITY_EL, SPOT_SYMBOL,
                                       req_short_stop_loss_percent,
                                       req_short_take_profit_percent, req_multi_tp, req_tp1_percent, req_tp2_percent,
                                       req_tp3_percent, req_tp1_qty_size, req_tp2_qty_size, req_tp3_qty_size,
                                       req_order_time_out):

                    SPOT_EXIT = "NA"
                    SPOT_SIDE = "Buy"

                    if req_short_stop_loss_percent == 0 and req_short_take_profit_percent == 0 and req_multi_tp == "No":
                        SPOT_ENTRY = "Market"
                        try:
                            exit_short_buy_or = session.place_active_order(symbol=SPOT_SYMBOL, side=SPOT_SIDE,
                                                                           orderType=SPOT_ENTRY,
                                                                           orderQty=SPOT_SELL_QUANTITY_EL)
                            time.sleep(10)
                            exit_short_buy_order = exit_short_buy_or["result"]
                            print(f"exit_short_buy_order = {exit_short_buy_order}")
                            exit_short_buy_order_id = exit_short_buy_order["orderId"]

                        except Exception as e:
                            error_occured = f"{e}"
                            print(error_occured)
                            error_occured_time = datetime.now(IST)

                            cursor.execute(
                                "insert into bybit_error_log(symbol, order_action, entry_order_type, exit_order_type, quantity, occured_time, error_description) values (%s, %s, %s, %s, %s, %s, %s)",
                                [SPOT_SYMBOL, SPOT_SIDE, SPOT_ENTRY, SPOT_EXIT, SPOT_BUY_QUANTITY_EL,
                                 error_occured_time,
                                 error_occured])
                            conn.commit()

                        trades = session.user_trade_records(symbol=SPOT_SYMBOL, orderId=exit_short_buy_order_id)
                        filled_trade = trades["result"]

                        try:
                            BUY_ORDER_ID = exit_short_buy_order["orderId"]
                            BUY_ORDER_SYMBOL = exit_short_buy_order["symbol"]
                            commision_in_coin = 0
                            ask_qty = float(exit_short_buy_order["executedQty"])
                            try:
                                for fill in filled_trade["fee"]:
                                    comm = float(fill["fee"])
                                    commision_in_coin += comm
                            except:
                                commision_in_coin = ask_qty * 0.001
                            BUY_ORDER_QTY = ask_qty - commision_in_coin
                            TOTAL_BUY_SPEND = float(exit_short_buy_order["cummulativeQuoteQty"])
                            print(f"Total buy spend = {TOTAL_BUY_SPEND}")
                            BUY_ORDER_PRICE = float(exit_short_buy_order["cummulativeQuoteQty"]) / float(
                                exit_short_buy_order["executedQty"])
                            BUY_ORDER_ACTION = exit_short_buy_order["side"]
                            BUY_ORDER_TYPE = exit_short_buy_order["type"]
                            buy_order_executed_time = datetime.now(IST)

                            execution = "Exit as Market"

                            cursor.execute("select total_spend from bybit_short_entry where symbol = %s", [SPOT_SYMBOL])
                            r_3 = cursor.fetchall()
                            price_results = r_3[0][0]
                            previous_short_entry_income = float(price_results)
                            print(f"previous_buy_income = {previous_short_entry_income}")

                            cursor.execute("select qty from bybit_short_entry where symbol = %s", [SPOT_SYMBOL])
                            r_3 = cursor.fetchall()
                            price_results = r_3[0][0]
                            previous_short_entry_qty = float(price_results)
                            print(f"previous_short_entry_qty = {previous_short_entry_qty}")

                            actual_sell_income = (previous_short_entry_income / 100) * 99.9
                            proportional_sell_income = (actual_sell_income / previous_short_entry_qty) * BUY_ORDER_QTY
                            SHORT_BUY_PNL = round((proportional_sell_income - TOTAL_BUY_SPEND), 2)
                            short_buy_per = (SHORT_BUY_PNL / proportional_sell_income) * 100
                            SHORT_BUY_PNL_PERCENTAGE = str((round(short_buy_per, 2))) + "%"

                            cursor.execute(sql.SQL(
                                "insert into bybit_trade_log(date_time, symbol, order_id, order_action, order_type, executed_price, executed_qty, execution, pnl, percentage) values (%s, %s, %s, %s, %s, %s, %s, %s, %s,%s)"),
                                [buy_order_executed_time, BUY_ORDER_SYMBOL, BUY_ORDER_ID, BUY_ORDER_ACTION,
                                 BUY_ORDER_TYPE,
                                 BUY_ORDER_PRICE, BUY_ORDER_QTY, execution, SHORT_BUY_PNL, SHORT_BUY_PNL_PERCENTAGE])
                            conn.commit()

                        except Exception as e:
                            print(e)

                    if req_short_stop_loss_percent > 0 or req_short_take_profit_percent > 0 or req_multi_tp == "Yes":
                        SPOT_ENTRY = "Limit"

                        cursor.execute("select entry_price from bybit_short_entry where symbol = %s", [SPOT_SYMBOL])
                        r_3 = cursor.fetchall()
                        price_results = r_3[0][0]
                        previous_short_entry_price = float(price_results)
                        print(f"previous_short_entry_price= {previous_short_entry_price}")

                        short_stop_loss_bp = previous_short_entry_price + (
                                previous_short_entry_price * req_short_stop_loss_percent)

                        short_take_profit_bp = previous_short_entry_price - (
                                previous_short_entry_price * req_short_take_profit_percent)

                        STOP_LOSS_PRICE_FINAL = cal_price_with_precision(SPOT_SYMBOL=SPOT_SYMBOL,
                                                                         input_price=short_stop_loss_bp)
                        print(f"Stop loss price final = {STOP_LOSS_PRICE_FINAL}")

                        TAKE_PROFIT_PRICE_FINAL = cal_price_with_precision(SPOT_SYMBOL=SPOT_SYMBOL,
                                                                           input_price=short_take_profit_bp)
                        print(f"Take profit price final = {TAKE_PROFIT_PRICE_FINAL}")

                        BUY_ORDER_ID = 0

                        if req_multi_tp == "No":
                            if req_short_stop_loss_percent > 0 and req_short_take_profit_percent > 0:
                                execute_limit_oco_order(SPOT_SIDE=SPOT_SIDE, req_position_type=req_position_type,
                                                        BUY_ORDER_ID=BUY_ORDER_ID,
                                                        SPOT_SYMBOL=SPOT_SYMBOL,
                                                        SPOT_SELL_QUANTITY=SPOT_BUY_QUANTITY_EL,
                                                        TAKE_PROFIT_PRICE_FINAL=TAKE_PROFIT_PRICE_FINAL,
                                                        STOP_LOSS_PRICE_FINAL=STOP_LOSS_PRICE_FINAL,
                                                        SPOT_ENTRY=SPOT_ENTRY,
                                                        req_multi_tp=req_multi_tp, req_qty_size=0,
                                                        req_order_time_out=req_order_time_out,tp_type="None")
                            elif req_short_stop_loss_percent > 0 and (
                                    req_short_take_profit_percent == "" or req_short_take_profit_percent == 0):
                                execute_limit_stop_loss_order(SPOT_SIDE, req_position_type, BUY_ORDER_ID, SPOT_SYMBOL,
                                                              SPOT_BUY_QUANTITY_EL,
                                                              STOP_LOSS_PRICE_FINAL, SPOT_ENTRY, req_order_time_out)
                            elif req_short_take_profit_percent > 0 and (
                                    req_short_stop_loss_percent == "" or req_short_stop_loss_percent == 0):
                                execute_limit_take_profit_order(SPOT_SIDE=SPOT_SIDE,
                                                                req_position_type=req_position_type,
                                                                BUY_ORDER_ID=BUY_ORDER_ID,
                                                                SPOT_SYMBOL=SPOT_SYMBOL,
                                                                SPOT_SELL_QUANTITY=SPOT_BUY_QUANTITY_EL,
                                                                TAKE_PROFIT_PRICE_FINAL=TAKE_PROFIT_PRICE_FINAL,
                                                                SPOT_ENTRY=SPOT_ENTRY,
                                                                req_multi_tp=req_multi_tp, req_qty_size=0,
                                                                req_order_time_out=req_order_time_out,tp_type="None")

                        if req_multi_tp == "Yes":
                            SELLABLE_1 = calculate_sell_qty_with_precision(SPOT_SYMBOL,
                                                                           (SPOT_BUY_QUANTITY_EL * req_tp1_qty_size))
                            print(f"Sellable qty_1 = {SELLABLE_1}")
                            SELLABLE_2 = calculate_sell_qty_with_precision(SPOT_SYMBOL,
                                                                           (SPOT_BUY_QUANTITY_EL * req_tp2_qty_size))
                            print(f"Sellable qty_2 = {SELLABLE_2}")
                            SELLABLE_3 = calculate_sell_qty_with_precision(SPOT_SYMBOL,
                                                                           (SPOT_BUY_QUANTITY_EL * req_tp3_qty_size))
                            print(f"Sellable qty_3 = {SELLABLE_3}")

                            short_take_profit_bp_1 = previous_short_entry_price - (
                                    previous_short_entry_price * req_tp1_percent)
                            short_take_profit_bp_2 = previous_short_entry_price - (
                                    previous_short_entry_price * req_tp2_percent)
                            short_take_profit_bp_3 = previous_short_entry_price - (
                                    previous_short_entry_price * req_tp3_percent)
                            TAKE_PROFIT_PRICE_FINAL_1 = cal_price_with_precision(SPOT_SYMBOL=SPOT_SYMBOL,
                                                                                 input_price=short_take_profit_bp_1)
                            TAKE_PROFIT_PRICE_FINAL_2 = cal_price_with_precision(SPOT_SYMBOL=SPOT_SYMBOL,
                                                                                 input_price=short_take_profit_bp_2)
                            TAKE_PROFIT_PRICE_FINAL_3 = cal_price_with_precision(SPOT_SYMBOL=SPOT_SYMBOL,
                                                                                 input_price=short_take_profit_bp_3)
                            print(f"Take profit price final_1 = {TAKE_PROFIT_PRICE_FINAL_1}")
                            print(f"Take profit price final_2 = {TAKE_PROFIT_PRICE_FINAL_2}")
                            print(f"Take profit price final_3 = {TAKE_PROFIT_PRICE_FINAL_3}")

                            if req_short_stop_loss_percent > 0 and (
                                    req_tp1_percent > 0 or req_tp2_percent > 0 or req_tp3_percent > 0):
                                if req_tp1_percent > 0:
                                    t1 = threading.Thread(target=lambda: execute_limit_oco_order(SPOT_SIDE=SPOT_SIDE,
                                                                                                 req_position_type=req_position_type,
                                                                                                 BUY_ORDER_ID=BUY_ORDER_ID,
                                                                                                 SPOT_SYMBOL=SPOT_SYMBOL,
                                                                                                 SPOT_SELL_QUANTITY=SELLABLE_1,
                                                                                                 TAKE_PROFIT_PRICE_FINAL=TAKE_PROFIT_PRICE_FINAL_1,
                                                                                                 STOP_LOSS_PRICE_FINAL=STOP_LOSS_PRICE_FINAL,
                                                                                                 SPOT_ENTRY=SPOT_ENTRY,
                                                                                                 req_multi_tp=req_multi_tp,
                                                                                                 req_qty_size=req_tp1_qty_size,
                                                                                                 req_order_time_out=req_order_time_out,tp_type="One"))
                                    t1.start()
                                if req_tp2_percent > 0:
                                    t2 = threading.Thread(target=lambda: execute_limit_oco_order(SPOT_SIDE=SPOT_SIDE,
                                                                                                 req_position_type=req_position_type,
                                                                                                 BUY_ORDER_ID=BUY_ORDER_ID,
                                                                                                 SPOT_SYMBOL=SPOT_SYMBOL,
                                                                                                 SPOT_SELL_QUANTITY=SELLABLE_2,
                                                                                                 TAKE_PROFIT_PRICE_FINAL=TAKE_PROFIT_PRICE_FINAL_2,
                                                                                                 STOP_LOSS_PRICE_FINAL=STOP_LOSS_PRICE_FINAL,
                                                                                                 SPOT_ENTRY=SPOT_ENTRY,
                                                                                                 req_multi_tp=req_multi_tp,
                                                                                                 req_qty_size=req_tp2_qty_size,
                                                                                                 req_order_time_out=req_order_time_out,tp_type="Two"))
                                    t2.start()
                                if req_tp3_percent > 0:
                                    t3 = threading.Thread(target=lambda: execute_limit_oco_order(SPOT_SIDE=SPOT_SIDE,
                                                                                                 req_position_type=req_position_type,
                                                                                                 BUY_ORDER_ID=BUY_ORDER_ID,
                                                                                                 SPOT_SYMBOL=SPOT_SYMBOL,
                                                                                                 SPOT_SELL_QUANTITY=SELLABLE_3,
                                                                                                 TAKE_PROFIT_PRICE_FINAL=TAKE_PROFIT_PRICE_FINAL_3,
                                                                                                 STOP_LOSS_PRICE_FINAL=STOP_LOSS_PRICE_FINAL,
                                                                                                 SPOT_ENTRY=SPOT_ENTRY,
                                                                                                 req_multi_tp=req_multi_tp,
                                                                                                 req_qty_size=req_tp3_qty_size,
                                                                                                 req_order_time_out=req_order_time_out,tp_type="Three"))
                                    t3.start()


                            elif req_short_stop_loss_percent > 0 and (
                                    req_tp1_percent == 0 and req_tp2_percent == 0 and req_tp3_percent == 0):
                                execute_limit_stop_loss_order(SPOT_SIDE, req_position_type, BUY_ORDER_ID, SPOT_SYMBOL,
                                                              SPOT_BUY_QUANTITY_EL,
                                                              STOP_LOSS_PRICE_FINAL, SPOT_ENTRY, req_order_time_out)


                            elif (req_tp1_percent > 0 or req_tp2_percent > 0 or req_tp3_percent > 0) and (
                                    req_short_stop_loss_percent == "" or req_short_stop_loss_percent == 0):
                                if req_tp1_percent > 0:
                                    t1 = threading.Thread(
                                        target=lambda: execute_limit_take_profit_order(SPOT_SIDE=SPOT_SIDE,
                                                                                       req_position_type=req_position_type,
                                                                                       BUY_ORDER_ID=BUY_ORDER_ID,
                                                                                       SPOT_SYMBOL=SPOT_SYMBOL,
                                                                                       SPOT_SELL_QUANTITY=SELLABLE_1,
                                                                                       TAKE_PROFIT_PRICE_FINAL=TAKE_PROFIT_PRICE_FINAL_1,
                                                                                       SPOT_ENTRY=SPOT_ENTRY,
                                                                                       req_multi_tp=req_multi_tp,
                                                                                       req_qty_size=req_tp1_qty_size,
                                                                                       req_order_time_out=req_order_time_out,tp_type="One"))
                                    t1.start()
                                if req_tp2_percent > 0:
                                    t2 = threading.Thread(
                                        target=lambda: execute_limit_take_profit_order(SPOT_SIDE=SPOT_SIDE,
                                                                                       req_position_type=req_position_type,
                                                                                       BUY_ORDER_ID=BUY_ORDER_ID,
                                                                                       SPOT_SYMBOL=SPOT_SYMBOL,
                                                                                       SPOT_SELL_QUANTITY=SELLABLE_2,
                                                                                       TAKE_PROFIT_PRICE_FINAL=TAKE_PROFIT_PRICE_FINAL_2,
                                                                                       SPOT_ENTRY=SPOT_ENTRY,
                                                                                       req_multi_tp=req_multi_tp,
                                                                                       req_qty_size=req_tp2_qty_size,
                                                                                       req_order_time_out=req_order_time_out,tp_type="Two"))
                                    t2.start()
                                if req_tp3_percent > 0:
                                    t3 = threading.Thread(
                                        target=lambda: execute_limit_take_profit_order(SPOT_SIDE=SPOT_SIDE,
                                                                                       req_position_type=req_position_type,
                                                                                       BUY_ORDER_ID=BUY_ORDER_ID,
                                                                                       SPOT_SYMBOL=SPOT_SYMBOL,
                                                                                       SPOT_SELL_QUANTITY=SELLABLE_3,
                                                                                       TAKE_PROFIT_PRICE_FINAL=TAKE_PROFIT_PRICE_FINAL_3,
                                                                                       SPOT_ENTRY=SPOT_ENTRY,
                                                                                       req_multi_tp=req_multi_tp,
                                                                                       req_qty_size=req_tp2_qty_size,
                                                                                       req_order_time_out=req_order_time_out,tp_type="Three"))
                                    t3.start()

                # Stop bot if balance is below user defined amount

                if req_stop_bot_balance != 0:
                    if check_base_coin_balance() > req_stop_bot_balance:
                        # Check order position
                        if req_position_type == "Enter_long":
                            SPOT_BUY_QUANTITY = calculate_buy_qty_with_precision(SPOT_SYMBOL, qty_in_base_coin)
                            proceed_enter_long(SPOT_BUY_QUANTITY, SPOT_SYMBOL, SPOT_ENTRY, req_long_stop_loss_percent,
                                               req_long_take_profit_percent, req_multi_tp, req_tp1_percent,
                                               req_tp2_percent,
                                               req_tp3_percent, req_tp1_qty_size, req_tp2_qty_size, req_tp3_qty_size,
                                               req_order_time_out)

                        elif req_position_type == "Exit_short":
                            SPOT_BUY_QUANTITY_EL = calculate_buy_qty_with_precision(SPOT_SYMBOL, qty_in_base_coin)
                            proceed_exit_short(req_position_type, SPOT_BUY_QUANTITY_EL, SPOT_SYMBOL,
                                               req_short_stop_loss_percent,
                                               req_short_take_profit_percent, req_multi_tp, req_tp1_percent,
                                               req_tp2_percent,
                                               req_tp3_percent, req_tp1_qty_size, req_tp2_qty_size, req_tp3_qty_size,
                                               req_order_time_out)

                        elif req_position_type == "Exit_long":
                            SPOT_SELL_QUANTITY_EL = calculate_buy_qty_with_precision(SPOT_SYMBOL, qty_in_base_coin)
                            proceed_exit_long(req_position_type, SPOT_SELL_QUANTITY_EL, SPOT_SYMBOL,
                                              req_long_stop_loss_percent,
                                              req_long_take_profit_percent, req_multi_tp, req_tp1_percent,
                                              req_tp2_percent,
                                              req_tp3_percent, req_tp1_qty_size, req_tp2_qty_size, req_tp3_qty_size,
                                              req_order_time_out)

                        elif req_position_type == "Enter_short":
                            SPOT_SELL_QUANTITY_EL = calculate_buy_qty_with_precision(SPOT_SYMBOL, qty_in_base_coin)
                            proceed_enter_short(req_position_type, SPOT_SELL_QUANTITY_EL, SPOT_SYMBOL,
                                                req_short_stop_loss_percent,
                                                req_short_take_profit_percent, req_multi_tp, req_tp1_percent,
                                                req_tp2_percent, req_tp3_percent,
                                                req_tp1_qty_size, req_tp2_qty_size, req_tp3_qty_size,
                                                req_order_time_out)
                    else:
                        error_occured_time = datetime.now(IST)
                        error_occured = "Cant initiate the trade! Wallet balance is low!"
                        cursor.execute("insert into bybit_error_log(occured_time, error_description) values (%s, %s)",
                                       [error_occured_time, error_occured])
                        conn.commit()
                if req_stop_bot_balance == 0:
                    # Check order position
                    if req_position_type == "Enter_long":
                        SPOT_BUY_QUANTITY = calculate_buy_qty_with_precision(SPOT_SYMBOL, qty_in_base_coin)
                        proceed_enter_long(SPOT_BUY_QUANTITY, SPOT_SYMBOL, SPOT_ENTRY, req_long_stop_loss_percent,
                                           req_long_take_profit_percent, req_multi_tp, req_tp1_percent, req_tp2_percent,
                                           req_tp3_percent, req_tp1_qty_size, req_tp2_qty_size, req_tp3_qty_size,
                                           req_order_time_out)

                    elif req_position_type == "Exit_short":
                        SPOT_BUY_QUANTITY_EL = calculate_buy_qty_with_precision(SPOT_SYMBOL, qty_in_base_coin)
                        proceed_exit_short(req_position_type, SPOT_BUY_QUANTITY_EL, SPOT_SYMBOL,
                                           req_short_stop_loss_percent,
                                           req_short_take_profit_percent, req_multi_tp, req_tp1_percent,
                                           req_tp2_percent,
                                           req_tp3_percent, req_tp1_qty_size, req_tp2_qty_size, req_tp3_qty_size,
                                           req_order_time_out)

                    elif req_position_type == "Exit_long":
                        SPOT_SELL_QUANTITY_EL = calculate_buy_qty_with_precision(SPOT_SYMBOL, qty_in_base_coin)
                        proceed_exit_long(req_position_type, SPOT_SELL_QUANTITY_EL, SPOT_SYMBOL,
                                          req_long_stop_loss_percent,
                                          req_long_take_profit_percent, req_multi_tp, req_tp1_percent, req_tp2_percent,
                                          req_tp3_percent, req_tp1_qty_size, req_tp2_qty_size, req_tp3_qty_size,
                                          req_order_time_out)

                    elif req_position_type == "Enter_short":
                        SPOT_SELL_QUANTITY_EL = calculate_buy_qty_with_precision(SPOT_SYMBOL, qty_in_base_coin)
                        proceed_enter_short(req_position_type, SPOT_SELL_QUANTITY_EL, SPOT_SYMBOL,
                                            req_short_stop_loss_percent,
                                            req_short_take_profit_percent, req_multi_tp, req_tp1_percent,
                                            req_tp2_percent,
                                            req_tp3_percent,
                                            req_tp1_qty_size, req_tp2_qty_size, req_tp3_qty_size, req_order_time_out)


        except Exception as e:
            print(e)
            error_occured_time = datetime.now(IST)
            error_occured = "Error in initiating Spot Order!"
            cursor.execute(
                "insert into bybit_error_log(occured_time, error_description) values (%s, %s)",
                [error_occured_time, error_occured])
            conn.commit()

    success_message = "Success"

    return success_message


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=80,debug=True)


# Webhook triggered
# <Request 'http://3.126.245.49/webhook' [POST]>
# first method worked = {"use_bybit":"1","coin_pair":"BTCUSDT","entry_order_type":"0","exit_order_type":"0","margin_mode":"1","qty_in_percentage": "true","qty":"1476.2828415986","buy_leverage":"1","sell_leverage":"1","long_stop_loss_percent":0.2032130914,"long_take_profit_percent":0.3048196371,"short_stop_loss_percent":0.2032130914,"short_take_profit_percent":0.3048196371,"enable_multi_tp":"true","tp_1_pos_size":"33","tp_1_percent":"0.1005904802","tp_2_pos_size":"33","tp_2_percent":"0.2011809605","tp_3_pos_size":"100","tp_3_percent":"0.3048196371","advanced_mode": "1","stop_bot_below_balance":"20","order_time_out":"240","exit_existing_trade": "True","comment": "","position": "Enter Short",}
# 34.212.75.30 - - [17/Sep/2022 20:37:00] "POST /webhook HTTP/1.1" 200 -
