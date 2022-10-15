import asyncio
import pprint
import random
import warnings

warnings.filterwarnings("ignore")

# Ant colony optimization algorithm
# Find a path between points 1 and 7

START = 1
END = 7

TIME_MODIFIER = 0.0001

CHEAT = False

graph = {
    1: {
        2: 10,
        3: 3,
        4: 7
    },
    2: {
        1: 10,
        3: 1,
        6: 9,
        7: 17
    },
    3: {
        1: 3,
        2: 1,
        5: 4
    },
    4: {
        1: 7,
        5: 12,
    },
    5: {
        3: 4,
        4: 12,
        6: 5
    },
    6: {
        5: 5,
        2: 9,
        7: 1
    },
    7: {
        2: 17,
        6: 1,
    }
}

weights = {
    1: {
        2: 0,
        3: 0.38 if CHEAT else 0,
        4: 0
    },
    2: {
        1: 0,
        3: 0,
        6: 0,
        7: 0
    },
    3: {
        1: 0,
        2: 0,
        5: 0
    },
    4: {
        1: 0,
        5: 0,
    },
    5: {
        3: 0,
        4: 0,
        6: 0
    },
    6: {
        5: 0,
        2: 0,
        7: 0
    },
    7: {
        2: 0,
        6: 0,
    }
}


class Ant:
    def __init__(self):
        self.path = [START]
        self.current_node = START

    async def live(self):
        while True:
            if self.current_node == END:
                break

            current_weights = weights[self.current_node].copy()

            next_node = self.current_node
            while current_weights and next_node in self.path:
                w = [1 / graph[self.current_node][i] + current_weights[i] for i in current_weights]
                s = sum(w)

                normalized = [i / s for i in w]
                next_node = random.choices(list(current_weights.keys()), weights=normalized)[0]

                del current_weights[next_node]

            if next_node in self.path:
                print('ded')
                return

            path_length = graph[self.current_node][next_node]

            await asyncio.sleep(path_length * TIME_MODIFIER)

            self.path.append(next_node)
            self.current_node = next_node

        print(self.path)
        total_length = sum(graph[i][j] for i, j in zip(self.path, self.path[1:]))
        for i in range(len(self.path) - 1):
            weights[self.path[i]][self.path[i + 1]] += graph[self.path[i]][self.path[i + 1]] / total_length


ant_tasks = []


async def main():
    while True:
        ant_tasks.append(Ant().live())
        print('Spawned')
        print(weights)

        await asyncio.sleep(0.1 * TIME_MODIFIER)

        for task in ant_tasks:
            if not task.cr_running:
                await task
                ant_tasks.remove(task)


if __name__ == '__main__':

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nExiting...")
        pprint.pprint(weights)

        path = [START]

        r = START

        while r != END:
            r = max(weights[r], key=weights[r].get)
            path.append(r)

        print()
        print()
        print(f'Path: {path}, length: {sum(graph[i][j] for i, j in zip(path, path[1:]))}')

        exit(0)
