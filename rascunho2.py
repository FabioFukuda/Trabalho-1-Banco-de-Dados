d = {1 : 'e',
2: 'a',
3: 'c',
4: 'b',
5: 'y'}



print({k: v for k, v in sorted(d.items(), key=lambda item: item[1])})
