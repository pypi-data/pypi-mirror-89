

class Student:
    def __init__(self,name):
        self.name = name
        self.exp = 0
        self.lesson = 0
        #self.addEXP(10)
    
    def Hello(self):
        print('Hello my name is {}'.format(self.name))

    def coding(self):
        print('{} : coding...'.format(self.name))
        self.exp += 5
        self.lesson += 1
    
    def showEXP(self):
        print('{} have exp {} EXP'.format(self.name,self.exp))
        print('total {} time'.format(self.lesson))
    
    def addEXP(self,score):
        self.exp += score
        self.lesson += 1


class SpecialStudent(Student):

    def __init__(self,name,father):
        super().__init__(name)
        self.father = father
        deviluke = ['Gid Lucione Deviluke','Sephie Michaela Deviluke']
        if father in deviluke:
            self.exp += 100

    def addEXP(self,score):
        self.exp += (score * 3)
        self.lesson += 1

    def BoostScore(self,score = 10):
        print('Main ability : Harem plan! (EXP+ {})'.format(score))
        self.addEXP(score)



print(__name__)


if __name__ == '__main__':

    print('==== 1 Jan ====')
    student0 = SpecialStudent('Momo','Gid Lucione Deviluke')
    student0.BoostScore()
    student0.showEXP()


    student1 = Student('Mea')
    print(student1.name)
    student1.Hello()



    print('--------')
    student2 = Student('Yami')
    print(student2.name)
    student2.Hello()
    print('==== 2 Jan ====')
    print('------Rito: who like coding ? (10 exp) ------')

    student1.addEXP(10)
    print('==== 3 Jan ====')

    print('How much is the exp of each person now?')

    print(student1.name,student1.exp)
    print(student2.name,student2.exp)

    print('==== 4 Jan ====')

    for i in range(5):
        student1.coding()

    student1.showEXP()
    student2.showEXP()