import collections

Coordinate = collections.namedtuple('Coordinate',['x1', 'x2', 'y1', 'y2'])

hash_map_capacity = 1000000

class Hash_Node:
    def __init__(self, key):
        self.key = key
        self.next = None


#hash tabulku vyuzivam aby sa mi ziadne stavy neopakovali
class Hash_Table:
    def __init__(self):
        self.capacity = hash_map_capacity
        self.size = 0
        self.buckets = [None] * self.capacity

    def hash(self, key):
        hashsum = abs(hash(key)) % (10 ** 8)
        hashsum = hashsum % self.capacity

        return hashsum

    def insert(self, key):
        self.size += 1
        index = self.hash(key)
        node = self.buckets[index]

        if node == None:
            self.buckets[index] = Hash_Node(key)
            return
        prev = node
        while node is not None:
            prev = node
            node = node.next
        prev.next = Hash_Node(key)

    def find(self, key):
        index = self.hash(key)
        node = self.buckets[index]

        while node is not None and node.key != key:
            node = node.next

        if node is None:
            return None
        return node.key

#trieda reprezentujuca jedno auto
class Car:
    def __init__(self, color, orientation, size, x, y):
        self.color = color
        self.orientation = orientation
        self.size = size
        self.x = x
        self.y = y

    #ziskavam pociatocne a koncove suradnice auta
    #teda naprikald ked je auto horizontalne a ma x==0, y==0
    #a velkost auta je 3 tak koncove suradnice budu x==2, y==0
    def getCoordinates(self):
        if(self.orientation == 'H'):
            return Coordinate(self.x, self.x + self.size - 1, self.y, self.y)
        else:
            return Coordinate(self.x, self.x, self.y, self.y + self.size - 1)

    def getCarInfo(self, car):
        info = car.split(", ")

        color = info[0]
        orientation = info[1]
        size = int(info[2])
        carX = int(info[3])
        carY = int(info[4])

        return color, orientation, size, carX, carY

    #pozeram ci sa auto nahodou nekrizi s inym autom
    def intersects(self, otherCar):
        c1 = self.getCoordinates()
        intersects = False

        if(otherCar.color != self.color):
            c2 = otherCar.getCoordinates()

            if(self.orientation == 'H'):
                if(otherCar.orientation == 'H'):
                    intersects = c1.y1 == c2.y1 and (c1.x1 < c2.x1 <= c1.x2 <= c2.x2 or c1.x1 <= c2.x2 <= c1.x2)
                else:
                    intersects = c1.x1 <= c2.x1 <= c1.x2 and c2.y1 <= c1.y1 <= c2.y2

            elif(otherCar.orientation == 'H'):
                intersects = c2.x1 <= c1.x1 <= c2.x2 and c1.y1 <= c2.y1 <= c1.y2
            else:
                intersects = c1.x1 == c2.x1 and (c1.y1 < c2.y1 <= c1.y2 <= c2.y2 or c1.y1 <= c2.y2 <= c1.y2)

        return intersects

#trieda reprezentujuca jeden stav
#teda mapu s konkretnym rozlozenim aut
class Node:
    children = []
    parent = None

    def __init__(self, cars, depth):
        self.cars = cars
        self.depth = depth

    def createCar(self, car):
        car = car.split(", ")
        return Car(car[0], car[1], int(car[2]), int(car[3]), int(car[4]))

    def recreateString(self, parts):
        arr = ""
        for j in range(0, 5):
            arr += parts[j]
            if (j != 4):
                arr += ", "
        return arr

    #pozeram ci je stav koncovy
    def isGoal(self):
        for x in self.cars:
            car = x.split(", ")
            if(car[0] == "red"):
                #koncovy stav je ked ma cervene auto suradnice (4,2) na mape 6x6
                if(car[3] == '4' and car[4] == '2'):
                    return True
        return False

    #vytvaram kopiu mapy
    def copyPuzzle(self):
        copy = []
        for car in self.cars:
            copy.append(car)

        return copy

    #metoda na prepisovanie suradnic aut
    #pomocou tejto metody sa auta pohybuju po mape
    def move(self, car, numOfSteps, position, depth):
        j = 0
        #zakazdym ked vytvaram novy stav musim ho vytvorit z kopie rodica
        new_puzzle = self.copyPuzzle()

        for i in new_puzzle:
            c = i.split(", ")
            if(c[0] == car.color):
                newPos = int(c[position]) + numOfSteps
                c[position] = str(newPos)

                i = self.recreateString(c)

                new_puzzle[j] = i

                #novovytvoreny stav pridam do listu potomkov
                #takto si zarucim ze kazdy stav bude mat svoje deti a predchodcu
                child = Node(new_puzzle, depth)
                self.children.append(child)
                child.parent = self

                return
            j += 1

    #pomocou tejto funkcie zistujem ci sa auto moze posunut
    #do daneho smeru o dany pocet policok
    #bez toho aby vyslo z mapy alebo narazilo do druheho auta
    def canMove(self, car, direction, numOfSteps):
        map = self.cars

        if(car.orientation == 'H'):
            if(direction == 'R'):
                for i in range(0, numOfSteps):
                    car.x += 1
                    #pozeram ci auto nevyslo z mapy
                    if(car.x + car.size - 1 > 5):
                        return False

                    #pre kazde auto na mape pozeram ci sa nekrizi s autom, ktorym hybem
                    for c2 in map:
                        c2 = c2.split(", ")
                        otherCar = Car(c2[0], c2[1], int(c2[2]), int(c2[3]), int(c2[4]))
                        if(car.intersects(otherCar)):
                            return False

            if (direction == 'L'):
                for i in range(0, numOfSteps):
                    car.x -= 1
                    # pozeram ci auto nevyslo z mapy
                    if (car.x < 0):
                        return False

                    # pre kazde auto na mape pozeram ci sa nekrizi s autom, ktorym hybem
                    for c2 in map:
                        c2 = c2.split(", ")
                        otherCar = Car(c2[0], c2[1], int(c2[2]), int(c2[3]), int(c2[4]))
                        if (car.intersects(otherCar)):
                            return False

        if (car.orientation == 'V'):
            if (direction == 'D'):
                for i in range(0, numOfSteps):
                    car.y += 1
                    # pozeram ci auto nevyslo z mapy
                    if (car.y + car.size - 1 > 5):
                        return False

                    # pre kazde auto na mape pozeram ci sa nekrizi s autom, ktorym hybem
                    for c2 in map:
                        c2 = c2.split(", ")
                        otherCar = Car(c2[0], c2[1], int(c2[2]), int(c2[3]), int(c2[4]))
                        if (car.intersects(otherCar)):
                            return False

            if (direction == 'U'):
                for i in range(0, numOfSteps):
                    car.y -= 1
                    # pozeram ci auto nevyslo z mapy
                    if (car.y < 0):
                        return False

                    # pre kazde auto na mape pozeram ci sa nekrizi s autom, ktorym hybem
                    for c2 in map:
                        c2 = c2.split(", ")
                        otherCar = Car(c2[0], c2[1], int(c2[2]), int(c2[3]), int(c2[4]))
                        if (car.intersects(otherCar)):
                            return False

        return True

    def moveUp(self, car, n, depth):
        return self.move(car, -n, 4, depth)

    def moveDown(self, car, n, depth):
        return self.move(car, n, 4, depth)

    def moveRight(self, car, n, depth):
        return self.move(car, n, 3, depth)

    def moveLeft(self, car, n, depth):
        return self.move(car, -n, 3, depth)

    #metoda na vytvaranie potomkov stavu
    def expandNode(self, depth):
        steps = 1
        for car in self.cars:
            c = self.createCar(car)
            x = c.x
            y = c.y

            #ak je auto orientovane horizontalne
            #hybem s nim najprv co najviac dolava a potom doprava
            if(c.orientation == "H"):
                #pokial sa mozem hybat dolava tak sa hybem
                #zakazdym o jedno policko viac
                while(self.canMove(c, "L", steps)):
                    c.x += 1
                    self.moveLeft(c, steps, depth)
                    c.x = x
                    c.y = y
                    steps += 1
                steps = 1
                c.x = x
                c.y = y
                # pokial sa mozem hybat doprava tak sa hybem
                # zakazdym o jedno policko viac
                while (self.canMove(c, "R", steps)):
                    c.x -= 1
                    self.moveRight(c, steps, depth)
                    c.x = x
                    c.y = y
                    steps += 1
                steps = 1
            #ak auto nie je orientovane horizontalne je vertikalne
            #cize hybem sa hore a dole
            else:
                # pokial sa mozem hybat hore tak sa hybem
                # zakazdym o jedno policko viac
                while (self.canMove(c, "U", steps)):
                    c.y += 1
                    self.moveUp(c, steps, depth)
                    c.x = x
                    c.y = y
                    steps += 1
                steps = 1
                c.x = x
                c.y = y
                # pokial sa mozem hybat dole tak sa hybem
                # zakazdym o jedno policko viac
                while (self.canMove(c, "D", steps)):
                    c.y -= 1
                    self.moveDown(c, steps, depth)
                    c.x = x
                    c.y = y
                    steps += 1
                steps = 1

#trieda, v ktorej riesim konkretnu mapu
class Puzzle:
    solution = []

    def __init__(self, cars):
        self.cars = cars

    #kontrolujem ci sa mi stav uz nenachadza v hash tabulke
    def inHashTable(self, node, hash_table):
        if(hash_table.find(str(node.cars))):
            return True
        return False

    #metoda, kde riesim mapu pomocu algoritmu cyklicky sa prehlbujuceho hladania
    def solvePuzzle(self):
        goal = False
        depth = 1
        max_depth = 100 #musim si nastavit maximalnu hlbku do ktorej pojdem, aby som nemal nekonecny cyklus
        root = Node(self.cars, 0)
        lifo = [] #list ktory sa bude spravat ako stack
        hash_table = Hash_Table()

        #prehladavam pokial nemam ciel, alebo som nedovrsil max. hlbku
        while(not goal and depth != max_depth):
            #generujem nove stavy z pociatocneho stavu
            root.expandNode(1)

            #pre kazde dieta pociatocneho stavu pozeram ci ho uz nemam v hash tabulke
            #ak nie pridam ho a tiez ho pridam do "stacku"
            for child in root.children:
                if(not self.inHashTable(child, hash_table)):
                    hash_table.insert(str(child.cars))
                    lifo.append(child)

            #kontrolujem ci mam koncovy stav pokial mam nieco v "stacku"
            while(lifo):
                current = lifo.pop()

                #az ked som dovrsil danu hlbku kontrolujem ci mam koncovy stav
                #pokial nemam hlbku vytvaram nove deti
                if(current.depth == depth):
                    goal = current.isGoal()
                else:
                    current.expandNode(current.depth + 1)

                    for child in current.children:
                        if (not self.inHashTable(child, hash_table)):
                            hash_table.insert(str(child.cars))
                            lifo.append(child)

                if(goal):
                    break
            hash_table = Hash_Table()
            depth += 1

        if (goal):
            print("Goal found!")
            self.getSolution(current)
            self.printSolution()
            return
        else:
            print("Solution doesn't exist!")

    #metoda ktora vypise mapu tak ako vyzera
    def visualize(self, cars):
        c = Node(cars, 0)
        car_pos = False

        for i in range(0,6):
            for j in range(0,6):
                for car in cars:
                    car = c.createCar(car)

                    if(car.orientation == "H"):
                        x2 = car.x + car.size -1
                        y2 = car.y
                    else:
                        x2 = car.x
                        y2 = car.y + car.size - 1
                    if(car.orientation == "H"):
                        if(j >= car.x and j <= x2 and car.y == i):
                            print(car.color[0].upper(), end = " ")
                            car_pos = True
                    else:
                        if(i >= car.y and i <= y2 and car.x == j):
                            print(car.color[0].upper(), end=" ")
                            car_pos = True
                if(not car_pos):
                    print(".", end = " ")
                car_pos = False

            print(" ")

    #vypis riesenia
    def printSolution(self):
        self.solution.reverse()

        i = 1
        for x in self.solution:
            print(i, ".")
            self.visualize(x)
            print()
            i += 1

    def getSolution(self, node):
        self.solution.append(node.cars)
        if(node.parent):
            self.getSolution(node.parent)
        else:
            return



def main():

    #TESTOVACIE MAPY:

    cars = ["red, H, 2, 1, 2", "purpel, V, 3, 3, 2", "blue, H, 2, 0, 4", "orange, H, 3, 3, 0"]

    # cars = ["red, H, 2, 0, 2", "purple, V, 3, 3, 2", "blue, H, 2, 0, 4"]

    # cars = ["blue, V, 3, 0, 0", "green, H, 2, 1, 0", "red, H, 2, 1, 2", "kaki, V, 3, 3, 1", "orange, V, 2, 0, 3",
    #        "white, H, 2, 1, 4", "pink, H, 3, 2, 5", "yellow, V, 3, 5, 3"]

    # cars = ["yellow, V, 3, 0, 0", "green, H, 2, 1, 0", "orange, V, 2, 4, 0", "white, V, 2, 1, 1", "pink, V, 2, 2, 1",
    #         "red, H, 2, 3, 2", "purple, V, 3, 5, 1", "blue, H, 3, 0, 3", "blue2, V, 2, 3, 3", "black, H, 2, 4, 4",
    #         "brown, H, 2, 0, 5", "green2, V, 2, 2, 4", "kaki, H, 2, 3, 5"]

    # cars = ["green, V, 2, 2, 0", "yellow, H, 3, 3, 0", "red, H, 2, 1, 2", "purple, V, 3, 3, 1", "orange, H, 2, 4, 1",
    #         "blue, V, 2, 1, 3", "dark, H, 2, 2, 4", "pink, H, 2, 4, 3", "blue2, V, 2, 0, 4", "blue3, H, 3, 1, 5"]

    # cars = ["red, H, 2, 1, 2", "orange, V, 2, 3, 0", "yellow, V, 3, 4, 1", "pink, V, 3, 5, 1", "blue, V, 3, 3, 2",
    #         "pink2, H, 2, 0, 3"]

    #cars = ["red, H, 2, 1, 2", "blue, V, 4, 3, 0"]

    puzzle = Puzzle(cars)

    puzzle.solvePuzzle()


main()