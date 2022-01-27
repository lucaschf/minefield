matrizConfig = []
config1 = {'player': 1, 'line': 8, 'column': 10, 'bombs': 10, 'availableFields': 70}
config2 = {'player': 2, 'line': 14, 'column': 18, 'bombs': 40, 'availableFields': 212}
config3 = {'player': 3, 'line': 20, 'column': 24, 'bombs': 100, 'availableFields': 380}
config4 = {'player': 4, 'line': 26, 'column': 28, 'bombs': 150, 'availableFields': 578}

matrizConfig.append(config1)
matrizConfig.append(config2)
matrizConfig.append(config3)
matrizConfig.append(config4)


def config(players):
    for i in matrizConfig:
        n = i.get('player')
        if n == players:
            return i
