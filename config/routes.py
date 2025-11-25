def get_tomorrow_jakarta_yogyakarta():
    import datetime
    tomorrow = datetime.datetime.today() + datetime.timedelta(days=1)
    date_str = tomorrow.strftime("%d-%m-%Y")
    url = f"https://www.traveloka.com/id-id/bus-and-shuttle/search?st=a102813.a107442&stt=CITY_GEO.CITY_GEO&stn=Jakarta.Yogyakarta&dt={date_str}.null&ps=1&stc=."
    return {
        'url': url,
        'route': 'Jakarta - Yogyakarta',
        'date': date_str
    }