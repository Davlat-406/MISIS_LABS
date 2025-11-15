import argparse, sys
sys.path.append('src')
from lib import *
from pathlib import Path

parser = argparse.ArgumentParser(description ='Конвертер' )
subparsers = parser.add_subparsers(dest = 'command')

json_t_scv = subparsers.add_parser('j_to_csv', help = 'Перевод из json в CSV')
json_t_scv.add_argument('--input', required = True, help = 'Введите путь файла (input)')
json_t_scv.add_argument('--output', required = True, help = 'Введите путь вывода')

csv_t_json = subparsers.add_parser('csv_to_j', help = 'Перевод из CSV в json')
csv_t_json.add_argument('--input', required = True, help = 'Введите путь файла (input)')
csv_t_json.add_argument('--output', required = True, help = 'Введите путь вывода')

csv_t_xlsx = subparsers.add_parser('csv_to_xl', help = 'Перевод из CSV в xlsx')
csv_t_xlsx.add_argument('--input', required = True, help = 'Введите путь файла (input)')
csv_t_xlsx.add_argument('--output', required = True, help = 'Введите путь вывода')

args = parser.parse_args()

if args.command == 'j_to_csv':
    if Path(args.input).stat().st_size and  Path(args.output).stat().st_size != 0:
        print (json_to_csv(Path(args.input), Path(args.output)))
    else:
        raise TypeError

elif args.command == 'csv_to_j':
    if Path(args.input).stat().st_size and  Path(args.output).stat().st_size != 0:
        print (csv_to_json(Path(args.input), Path(args.output)))
    else: 
        raise TypeError

elif  args.command == 'csv_to_xl':
    if Path(args.input).stat().st_size and  Path(args.output).stat().st_size != 0:
        print (csv_to_xlsx(Path(args.input), Path(args.output)))
    else:
        raise TypeError

