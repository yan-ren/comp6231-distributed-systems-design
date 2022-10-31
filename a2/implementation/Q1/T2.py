'''
Q1: Which Airline had the most canceled flights in September 2021?
T2. multiprocessing

header
FlightDate,Airline,Origin,Dest,Cancelled,Diverted,CRSDepTime,DepTime,DepDelayMinutes,DepDelay,ArrTime,ArrDelayMinutes,AirTime,CRSElapsedTime,ActualElapsedTime,Distance,Year,Quarter,Month,DayofMonth,DayOfWeek,Marketing_Airline_Network,Operated_or_Branded_Code_Share_Partners,DOT_ID_Marketing_Airline,IATA_Code_Marketing_Airline,Flight_Number_Marketing_Airline,Operating_Airline,DOT_ID_Operating_Airline,IATA_Code_Operating_Airline,Tail_Number,Flight_Number_Operating_Airline,OriginAirportID,OriginAirportSeqID,OriginCityMarketID,OriginCityName,OriginState,OriginStateFips,OriginStateName,OriginWac,DestAirportID,DestAirportSeqID,DestCityMarketID,DestCityName,DestState,DestStateFips,DestStateName,DestWac,DepDel15,DepartureDelayGroups,DepTimeBlk,TaxiOut,WheelsOff,WheelsOn,TaxiIn,CRSArrTime,ArrDelay,ArrDel15,ArrivalDelayGroups,ArrTimeBlk,DistanceGroup,DivAirportLandings
'''
import concurrent.futures

import numpy as np
import pandas as pd


def task(data: pd.DataFrame):
    # print(data.dtypes)
    data = data[(data['Year'] == 2021) & (data['Month'] == 9) & (data['Cancelled'] == True)]
    return data.iloc[:, 1:2].value_counts()


def load_data_in_chunks(data: str, chucks: int = 4) -> list:
    df = pd.read_csv(data)
    return np.array_split(df, chucks)


def reduce_task(mapping_output: list):
    reduce_out = {}
    for out in mapping_output:
        for key, value in out.to_dict().items():
            if key in reduce_out:
                reduce_out[key] = reduce_out.get(key) + value
            else:
                reduce_out[key] = value
    print(reduce_out)
    print('Airline had the most canceled flights in September 2021', max(reduce_out, key=reduce_out.get))


if __name__ == '__main__':
    process_num = 4
    data_frame = load_data_in_chunks('../datasets/Combined_Flights_2021.csv', process_num)
    results = []
    with concurrent.futures.ProcessPoolExecutor(max_workers=process_num) as executor:
        future_list = [executor.submit(task, df) for df in data_frame]
        for future in concurrent.futures.as_completed(future_list):
            results.append(future.result())

    reduce_task(results)
