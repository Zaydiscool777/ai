def mult(it, by):
    return it * by

this = [1, 2, 3, 4, 5]

this.sort(key=lambda x: mult(x, -1/2))

print(this, sum(this), this[-3:])

for i in this[0:3]:
    i += 1

this = [i+1 for i in this[0:3]] + this[3:]

print(this)