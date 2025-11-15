import argparse, sys
sys.path.append('src')
from lib import *
from pathlib import Path
def main():
    parser = argparse.ArgumentParser(description = 'Работа с текстом')
    subparsers = parser.add_subparsers(dest = 'command')
    
    cat_parser = subparsers.add_parser('cat', help='Вывести содержимое')
    cat_parser.add_argument('--input', required = True, help = 'Введите путь к файлу' )
    cat_parser.add_argument('-n', action = 'store_true'  ,help = 'Нумерация строк')
    
    stats_parser = subparsers.add_parser('stats', help='Частота слов')
    stats_parser.add_argument('--input', required = True, help = 'Введите путь к файлу')
    
    args = parser.parse_args()
    
    if args.command == 'cat':
        if Path(args.input).stat().st_size != 0:
            content = read_text(Path(args.input))
            if args.n:
                for i, word in enumerate (content.split(), 1):
                    print (f'{i}.{word}')
    elif args.command == 'stats':
        if Path(args.input).stat().st_size != 0:
            print (table(read_text(Path(args.input))))
                
    else:
        print('Введенными данными должен быть путь')
main()

