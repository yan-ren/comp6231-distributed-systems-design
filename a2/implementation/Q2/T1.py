'''
Q2: How many flights were diverted between the period of 20th-30th November 2021?
T1. Multi-threading

header
FlightDate,Airline,Origin,Dest,Cancelled,Diverted,CRSDepTime,DepTime,DepDelayMinutes,DepDelay,ArrTime,ArrDelayMinutes,AirTime,CRSElapsedTime,ActualElapsedTime,Distance,Year,Quarter,Month,DayofMonth,DayOfWeek,Marketing_Airline_Network,Operated_or_Branded_Code_Share_Partners,DOT_ID_Marketing_Airline,IATA_Code_Marketing_Airline,Flight_Number_Marketing_Airline,Operating_Airline,DOT_ID_Operating_Airline,IATA_Code_Operating_Airline,Tail_Number,Flight_Number_Operating_Airline,OriginAirportID,OriginAirportSeqID,OriginCityMarketID,OriginCityName,OriginState,OriginStateFips,OriginStateName,OriginWac,DestAirportID,DestAirportSeqID,DestCityMarketID,DestCityName,DestState,DestStateFips,DestStateName,DestWac,DepDel15,DepartureDelayGroups,DepTimeBlk,TaxiOut,WheelsOff,WheelsOn,TaxiIn,CRSArrTime,ArrDelay,ArrDel15,ArrivalDelayGroups,ArrTimeBlk,DistanceGroup,DivAirportLandings
'''
import concurrent.futures

import numpy as np
import pandas as pd


def task(data: pd.DataFrame):
    data = data[(data['Year'] == 2021) & (data['Month'] == 9) & (
        20 <= data['DayofMonth']) & (data['DayofMonth'] <= 30) & (data['Diverted'] == True)]
    return len(data.index)


def load_data_in_chunks(data: str, chucks: int = 4) -> list:
    df = pd.read_csv(data)
    return np.array_split(df, chucks)


def reduce_task(mapping_output: list):
    total = 0
    for out in mapping_output:
        total += out
    print('Flights were diverted between the period of 20th-30th November 2021:', total)


if __name__ == '__main__':
    threads = 10
    # Combined_Flights_2021
    data_frame = load_data_in_chunks(
        '../datasets/Combined_Flights_2021.csv', threads)
    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        future_list = [executor.submit(task, df) for df in data_frame]
        for future in concurrent.futures.as_completed(future_list):
            results.append(future.result())

    reduce_task(results)
