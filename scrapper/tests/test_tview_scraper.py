import requests

ticker_list = {
    'Mercedes-Benz Group, 8.5%': 'US233835AQ08',
    'Philip Morris International, 6.375%': 'PM3673419',
    'Verizon Communications, 4.5%': 'VZ4526725',
    'Deutsche Telekom, 8.75%': 'US25156PAC77',
    'Ford Motor, 7.45%' : 'US345370CA64',
    'Ovintiv, 6.5%': 'ECA.GD',
    'Paramount Global, 7.875%': 'US925524AH30',
    'Romania, 5.25%': 'XS2829209720',
    'Regal Rexnord, 6.05%': 'RBLT5808343',
    'Brazil, 7.125%': 'US105756BK57',
    'Türkei, 6.875%': 'US900123AY60',
}

for name, isin in ticker_list.items():
    resp = requests.get(f'http://localhost:8088/scrape?symbol={isin}')
    data = resp.json()
    print(f'{name}: {data['price']}%')